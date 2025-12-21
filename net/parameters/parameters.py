import os
import argparse

from net.initialization.get_yaml import get_yaml


def parameters_parsing(parameters_path: str) -> argparse.Namespace:
    """
    Definition of parameters-parsing for each execution mode

    :param parameters_path: path to the parameters YAML configuation file
    :return: parser of parameters parsing
    """

    # parser
    parser = argparse.ArgumentParser(description='Argument Parser')

    # parameters
    parameters = get_yaml(yaml_path=parameters_path)

    parser.add_argument('--task',
                        type=str,
                        choices=parameters['task']['choices'],
                        help=parameters['task']['help'])

    parser.add_argument('--dataset',
                        type=str,
                        default=parameters['dataset']['default'],
                        choices=parameters['dataset']['choices'],
                        help=parameters['dataset']['help'])

    parser.add_argument('--output_folder',
                        type=str,
                        default=parameters['output_folder']['default'],
                        help=parameters['output_folder']['help'])

    # parser arguments
    parser = parser.parse_args()

    return parser
