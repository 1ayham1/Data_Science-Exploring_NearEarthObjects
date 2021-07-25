"""Extract data on near-Earth objects and close approaches
from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at
the command line, and uses the resulting collections to build an `NEODatabase`.

"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about
    near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """

    neo_obj_lst = []

    with open(neo_csv_path, 'r') as cv_file:

        neo_reader = csv.DictReader(cv_file)

        for neo_elem in neo_reader:

            neo_obj = NearEarthObject(**neo_elem)
            neo_obj_lst.append(neo_obj)

    return neo_obj_lst


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param neo_csv_path: A path to a JSON file containing data about
    close approaches.
    :return: A collection of `CloseApproach`es.
    """

    with open(cad_json_path, 'r') as json_file:

        close_reader = json.load(json_file)

        close_obj_keys = close_reader["fields"]
        close_obj_data = close_reader["data"]
        close_reader_dict = [
            dict(zip(close_obj_keys, value))
            for value in close_obj_data]

        close_approach_lst = []

        for elem in close_reader_dict:
            close_approach = CloseApproach(**elem)
            close_approach_lst.append(close_approach)

    return close_approach_lst
