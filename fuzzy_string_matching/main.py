import os
import random

# If testing with local files, then include the following two lines. Otherwise ensure grove has been installed
# by pip so that importing the following modules is possible.
import sys
sys.path.insert(0, '/Users/Zivia/Research/grove')

from evolution.agent import Agent
from evolution.ga import evolve
from evolution.crossover import one_point
from evolution.selection import truncation
from evolution.mutation import gaussian
from grove import config, logger


target_string = 'Troy Squillaci'


class FuzzyAgent(Agent):

    """
    An agent targeting GESwarm simulations. Such agents include a parse tree that represents a set of rules that are
    used by the simulator to (hopefully) produce interesting collective behaviors.
    """

    grammar = None

    def __init__(self):

        super(FuzzyAgent, self).__init__(genome=None)

        self.genome = [random.randint(lower, upper) for lower, upper in zip(self.genome_lb, self.genome_ub)]


def agent_init(population_size=None):

    """
    A function used by the genetic algorithm that initializes a population of agents.
    :param population_size: The size of the population.
    :return: A list of initialized agents, length equal to the population size.
    """

    return [FuzzyAgent() for _ in xrange(population_size)]


def pre_evaluation(agents=None):

    """
    Pre-evaluation function prepares agents for evaluation. In this case, a genome is used to generate a parse tree,
    which is used during evaluation.
    :param agents: The list of agents to map the generation of parse trees over.
    :return: The updated list of agents with generated parse trees.
    """

    for agent in agents:

        agent.payload = {'genome': agent.genome, 'target': target_string}

    return agents


def evaluation(payload=None):

    """
    Evaluation function that performs fuzzy string matching on the given agent.
    :param payload: The payload (agent genome and the target string) to evaluate.
    :return: The evaluation value determined by executing the evaluation function with the payload.
    """

    from fuzzywuzzy import fuzz

    return {'random_seed': None, 'value': fuzz.ratio(''.join([chr(char) for char in payload['genome']]), payload['target'])}


def post_evaluation(agents=None):

    """
    Post-evaluation function performs data collection and/or alters agents after evaluation. In this case, no action
    is needed, so the agents are simply returned.
    :param agents: The list of agents.
    :return: The list of agents.
    """

    return agents


if __name__ == "__main__":

    # Parser for command line arguments.
    import argparse

    parser = argparse.ArgumentParser(description='grove')
    parser.add_argument('-config', action='store', type=str, default='./fuzzy_string_matching/grove-config.json')
    parser.add_argument('-p', '--population', action='store', type=int)
    parser.add_argument('-g', '--generations', action='store', type=int)
    parser.add_argument('-c', '--crossover_function', action='store', type=str, default='truncation')
    parser.add_argument('-m', '--mutation_function', action='store', type=str, default='one_point')
    parser.add_argument('-s', '--selection_function', action='store', type=str, default='gaussian')
    parser.add_argument('-b', '--grammar', action='store', type=str)
    parser.add_argument('-l', '--log_path', action='store', type=str)
    args = parser.parse_args()

    # Load the grove configuration.
    config.load_config(args.config)

    # Initialize the grove logger.
    logger.init_logger(args.log_path)

    # Change the current directory, for logging purposes.
    os.chdir(args.log_path)

    # Run the genetic algorithm.
    evolve(
        population_size=args.population or config.grove_config['ga']['parameters']['population'],
        generations=args.generations or config.grove_config['ga']['parameters']['generations'],
        repeats=config.grove_config['ga']['parameters']['repeats'],
        agent_func=agent_init,
        pre_evaluation=pre_evaluation,
        evaluation=evaluation,
        post_evaluation=post_evaluation,
        selection=truncation(0.2),
        crossover=one_point(),
        mutation=gaussian(),
        nodes=[],
        depends=[],
        debug=config.grove_config['debug']
    )
