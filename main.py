import os
import random

from evolution.agent import Agent
from evolution.ga import evolve
from evolution.crossover import one_point
from evolution.selection import truncation
from evolution.mutation import gaussian
from grammar.parse_tree import ParseTree
from grove import config, logger


class GESAgent(Agent):

    """
    An agent targeting GESwarm simulations. Such agents include a parse tree that represents a set of rules that are
    used by the simulator to (hopefully) produce interesting collective behaviors.
    """

    grammar = None

    def __init__(self):

        super(GESAgent, self).__init__(genome=None)

        self.genome = [random.randint(lower, upper) for lower, upper in zip(self.genome_lb, self.genome_ub)]
        self.parse_tree = ParseTree(GESAgent.grammar, self.genome)


def setup():

    import os
    import thriftpy

    # Path to Thrift
    thrift_path = './cpfa_ges/thrift/foraging.thrift'

    # Compile the grammar into a module.
    module_name = os.path.splitext(os.path.basename(thrift_path))[0] + '_thrift'

    global grammar
    grammar = thriftpy.load(thrift_path, module_name=module_name)

    return 0


def agent_init(population_size=None):

    """
    A function used by the genetic algorithm that initializes a population of agents.
    :param population_size: The size of the population.
    :return: A list of initialized agents, length equal to the population size.
    """

    return [GESAgent() for _ in xrange(population_size)]


def pre_evaluation(agents=None):

    """
    Pre-evaluation function prepares agents for evaluation. In this case, a genome is used to generate a parse tree,
    which is used during evaluation.
    :param agents: The list of agents to map the generation of parse trees over.
    :return: The updated list of agents with generated parse trees.
    """

    for agent in agents:

        agent.parse_tree.generate()
        agent.payload = agent.parse_tree.serialize()

    return agents


def evaluation(payload=None):

    """
    Evaluation function that executes a simulation with the specified payload. In this case the payload is a serialized
    parse tree that defines the possible transformations that can take place in the dynamic state machine. This function
    is executed across the cluster.
    :param payload: The payload (serialized parse tree) to evaluate.
    :return: The evaluation value determined by executing the evaluation function with the payload.
    """

    from simulation.entity import SimAgent, Food, Nest
    from simulation.environment import Environment
    from simulation.simulation import Simulation
    from simulation.utils import rand, seed

    import sys
    import thriftpy.transport as tp
    import thriftpy.protocol as pc

    transportIn = tp.TMemoryBuffer(payload)
    protocolIn = pc.TBinaryProtocol(transportIn)

    global grammar
    root = grammar.Root()
    root.read(protocolIn)

    seed = random.randint(0, sys.maxint)
    rand = random.Random(seed)

    # If the parse tree contains an empty ruleset, then no need to evaluate it.
    if not root.rules:

        return {'random_seed': seed, 'value': 0}

    # Create the entities for the simulation.
    agents = [SimAgent(position=(rand.randint(8, 11), rand.randint(8, 11))) for _ in xrange(5)]
    nest = Nest(position=(8, 8), size=(4, 4))
    food = [Food(position=(rand.choice([rand.randint(0, 7), rand.randint(12, 20)]), rand.choice([rand.randint(0, 7), rand.randint(12, 20)]))) for _ in xrange(80)]

    entities = agents + [nest] + food

    # Create the environment for the simulation.
    env = Environment()

    # Create and execute the simulation.
    sim = Simulation(duration=2000, environment=env, entities=entities, parse_tree=root)
    sim.execute_all()

    # Get the food tags collected, and return as the evaluation score.
    nest = filter(lambda x: isinstance(x, Nest), sim.entities)

    return {'random_seed': seed, 'value': nest[0].food_count}


if __name__ == "__main__":

    # Parser for command line arguments.
    import argparse

    parser = argparse.ArgumentParser(description='grove')
    parser.add_argument('-config', action='store', type=str, default='./cpfa_ges/grove-config.json')
    parser.add_argument('-p', '--population', action='store', type=int)
    parser.add_argument('-g', '--generations', action='store', type=int)
    parser.add_argument('-c', '--crossover_function', action='store', type=str, default='truncation')
    parser.add_argument('-m', '--mutation_function', action='store', type=str, default='one_point')
    parser.add_argument('-s', '--selection_function', action='store', type=str, default='gaussian')
    parser.add_argument('-b', '--grammar', action='store', type=str)
    args = parser.parse_args()

    # Load the grammar file.
    from grammar.grammar import Grammar

    GESAgent.grammar = Grammar(args.grammar)

    # Load the grove configuration.
    config.load_config(args.config)

    # Initialize the grove logger.
    # logger.init_logger(config.grove_config['logging']['path'])
    logger.init_logger()

    # Change the current directory, for logging purposes.
    # os.chdir(args.log_path)

    # Run the genetic algorithm.
    evolve(
        population_size=args.population or config.grove_config['ga']['parameters']['population'],
        generations=args.generations or config.grove_config['ga']['parameters']['generations'],
        repeats=config.grove_config['ga']['parameters']['repeats'],
        depends=['/Users/Zivia/Research/grove-examples/cpfa_ges/thrift/foraging.thrift'],
        dest_path=os.path.expanduser('~'),
        setup=setup,
        agent_func=agent_init,
        pre_evaluation=pre_evaluation,
        evaluation=evaluation,
        post_evaluation=lambda agents: agents,
        selection=truncation(0.2),
        crossover=one_point(),
        mutation=gaussian(),
        nodes=[str(node) for node in config.grove_config['ga']['nodes']],
        debug=config.grove_config['debug']
    )
