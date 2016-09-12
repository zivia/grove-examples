import numpy as np
import os
import random

from evolution import ga, selection, crossover, mutation
from evolution.agent import Agent
from grove import config


class CPFAAgent(Agent):

    def __init__(self):

        super(CPFAAgent, self).__init__()

        self.genotype = [random.uniform(lower, upper) for lower, upper in zip(self.genotype_lb, self.genotype_ub)]
        self.genotype_len = len(self.genotype)

    @staticmethod
    def init_agents(population):

        agents = []

        for i in xrange(population):

            agent = CPFAAgent.factory()
            mean = float(i) / population

            for idx, param in enumerate(agent.genotype):

                param = agent.genotype_ub[idx] * np.random.normal(loc=mean, scale=0.05)

                if param < agent.genotype_lb[idx]:
                    param = agent.genotype_lb[idx]
                elif param > agent.genotype_ub[idx]:
                    param = agent.genotype_ub[idx]

                agent.genotype[idx] = param

            agents.append(agent)

        return agents


def pre_evaluation(agents=None):

    from xml.dom.minidom import parse

    for agent in agents:

        argos_xml = './experiments/xml/CPFA-' + str(agent.id % 8) + '.xml'
        xml = parse(argos_xml)
        cpfa = xml.getElementsByTagName("CPFA")
        attrs = cpfa[0]

        attrs.setAttribute('ProbabilityOfSwitchingToSearching', str(round(agent.genotype[0], 5)))
        attrs.setAttribute('ProbabilityOfReturningToNest', str(round(agent.genotype[1], 5)))
        attrs.setAttribute('UninformedSearchVariation', str(round(agent.genotype[2], 5)))
        attrs.setAttribute('RateOfInformedSearchDecay', str(round(agent.genotype[3], 5)))
        attrs.setAttribute('RateOfSiteFidelity', str(round(agent.genotype[4], 5)))
        attrs.setAttribute('RateOfLayingPheromone', str(round(agent.genotype[5], 5)))
        attrs.setAttribute('RateOfPheromoneDecay', str(round(agent.genotype[6], 5)))

        xml.writexml(open(argos_xml, 'w'))

    return agents


def evaluation(agent=None):
    """
    Evaluation function that executes ARGoS with the specified agent.
    :param agent: The agent to evaluate in the ARGoS simulation.
    :return: The agent with updated evaluation value.
    """

    import re
    import subprocess
    from subprocess import CalledProcessError

    output = None

    try:
        output = subprocess.check_output(
            ['/usr/local/bin/argos3 -c ./experiments/xml/CPFA-' + str(agent.id % 8) + '.xml'],
            shell=True,
            stderr=subprocess.STDOUT)
    except CalledProcessError as e:
        output = e.output

    result = re.search(r'\s(\d+),\s(\d+),\s(\d+)', output)

    return result


def post_evaluation(agents=None):

    return agents


if __name__ == "__main__":

    import argparse

    # Parser for command line arguments.
    parser = argparse.ArgumentParser(description='grove')
    parser.add_argument('-config', action='store', type=str, default='grove-config.json')
    parser.add_argument('-p', '--population', action='store', type=int)
    parser.add_argument('-g', '--generations', action='store', type=int)
    parser.add_argument('-c', '--crossover_function', action='store', type=str, default='truncation')
    parser.add_argument('-m', '--mutation_function', action='store', type=str, default='one_point')
    parser.add_argument('-s', '--selection_function', action='store', type=str, default='gaussian')
    args = parser.parse_args()

    # Load the grove configuration.
    config.load_config(args.config)

    # Initialize logging handler.
    from logbook import FileHandler, Logger
    import time

    log_handler = FileHandler('grove-' + time.strftime("%I:%M-M%mD%dY%Y" + '.log'))
    log = Logger('Grove Logger')

    # Change the current directory to ARGoS (required by the simulator).
    os.chdir(os.path.expanduser('~') + '/ARGoS/iAnt-ARGoS-master')

    # Run the genetic algorithm.
    with log_handler.applicationbound():

        ga.evolve(
            args.population or config.grove_config['ga']['parameters']['population'],
            args.generations or config.grove_config['ga']['parameters']['generations'],
            CPFAAgent,
            pre_evaluation,
            evaluation,
            post_evaluation,
            selection.tournament(4, 5),
            crossover.one_point(),
            mutation.gaussian(),
            [],
            [],
            log
        )
