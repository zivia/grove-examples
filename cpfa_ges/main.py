import os
import random

from evolution import agent, ga, selection, crossover, mutation
from grammar.parse_tree import ParseTree
from grove import config, logger


class GESAgent(agent.Agent):

    """
    An agent targeted for GES.
    """

    grammar = None

    def __init__(self):

        super(GESAgent, self).__init__()

        self.genome = [random.randint(lower, upper) for lower, upper in zip(self.genome_lb, self.genome_ub)]
        self.parse_tree = ParseTree(GESAgent.grammar, self.genome)


def agent_init(population_size=None):

    return [GESAgent() for _ in xrange(population_size)]


def pre_evaluation(agents=None):

    """
    Pre-evaluation function prepares agents for evaluation. In this case, a genome is used to generate a parse tree,
    which is used during evaluation.
    :param agents: The population of agents to map the generation of parse trees over.
    :return: The updated agents with generated parse trees.
    """

    for agent in agents:

        agent.parse_tree.generate()
        agent.payload = agent.parse_tree.serialize()

    return agents


def evaluation(payload=None):

    """
    Evaluation function that executes a simulation with the specified payload. In this case the payload is a serialized
    parse tree that defines the legal transformation that can take place in the dynamic state machine.
    :param payload: The payload (serialized parse tree) to evaluate.
    :return: The evaluation value determined by executing the evaluation function with the payload.
    """

    import os
    os.chdir('/Users/Zivia/Research/output/simulations')

    import traceback

    try:

        import sys
        sys.path.append('/Users/Zivia/Research/grove')

        from simulation.entity import SimAgent, Food, Nest
        from simulation.environment import Environment
        from simulation.simulation import Simulation

        import thriftpy.transport as tp
        import thriftpy.protocol as pc
        import thriftpy

        # Path to Thrift
        thrift_path = '/Users/Zivia/Research/grove/examples/ges_lyssa/thrift/foraging.thrift'

        # Compile the Thrift and read the grammar.
        module_name = os.path.splitext(os.path.basename(thrift_path))[0] + '_thrift'
        thrift = thriftpy.load(thrift_path, module_name=module_name)

        transportIn = tp.TMemoryBuffer(payload)
        protocolIn = pc.TBinaryProtocol(transportIn)
        root = thrift.Root()
        root.read(protocolIn)

        seed = random.randint(0, sys.maxint)
        rand = random.Random(seed)

        # Create the entities for the simulation.
        agents = [SimAgent(position=(rand.randint(8, 11), rand.randint(8, 11))) for _ in xrange(5)]
        nest = Nest(position=(8, 8), size=(4, 4))
        food = [Food(position=(rand.choice([rand.randint(0, 7), rand.randint(12, 20)]), rand.choice([rand.randint(0, 7), rand.randint(12, 20)]))) for _ in xrange(80)]

        entities = agents + [nest] + food

        # Create the environment for the simulation.
        env = Environment()

        # Create and execute the simulation.
        sim = Simulation(environment=env, entities=entities, parse_tree=root)
        sim.execute()

        # Get the food tags collected, and return as the evaluation score.
        nest = filter(lambda x: isinstance(x, Nest), sim.entities)

        return {'random_seed': seed, 'value': nest[0].food_count}

    except Exception:

        print traceback.format_exc()
        return traceback.format_exc()


def post_evaluation(agents=None):

    """
    Post-evaluation function performs data collection and/or alters agents after evaluation. In this case, no action
    is needed, so the agents are simply returned.
    :param agents: The population of agents.
    :return: The population of agents.
    """

    return agents


if __name__ == "__main__":

    # Parser for command line arguments.
    import argparse

    parser = argparse.ArgumentParser(description='grove')
    parser.add_argument('-config', action='store', type=str, default='examples/ges_lyssa/grove-config.json')
    parser.add_argument('-p', '--population', action='store', type=int)
    parser.add_argument('-g', '--generations', action='store', type=int)
    parser.add_argument('-c', '--crossover_function', action='store', type=str, default='truncation')
    parser.add_argument('-m', '--mutation_function', action='store', type=str, default='one_point')
    parser.add_argument('-s', '--selection_function', action='store', type=str, default='gaussian')
    parser.add_argument('-b', '--grammar', action='store', type=str)
    parser.add_argument('-l', '--log_path', action='store', type=str)
    args = parser.parse_args()

    # Load the grammar file.
    from grammar.grammar import Grammar

    GESAgent.grammar = Grammar(args.grammar)

    # Load the grove configuration.
    config.load_config(args.config)

    # Initialize the grove logger.
    logger.init_logger(args.log_path)

    # Change the current directory, for logging purposes.
    os.chdir(args.log_path)

    # Run the genetic algorithm.
    ga.evolve(
        population_size=args.population or config.grove_config['ga']['parameters']['population'],
        generations=args.generations or config.grove_config['ga']['parameters']['generations'],
        repeats=config.grove_config['ga']['parameters']['repeats'],
        agent_func=agent_init,
        pre_evaluation=pre_evaluation,
        evaluation=evaluation,
        post_evaluation=post_evaluation,
        selection=selection.tournament(4, 5),
        crossover=crossover.one_point(),
        mutation=mutation.gaussian(),
        nodes=[],
        depends=[],
        debug=config.grove_config['debug']
    )
