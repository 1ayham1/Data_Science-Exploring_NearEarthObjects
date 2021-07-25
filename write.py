"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

"""
import csv
import json


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    Each output row corresponds to the information in a single close approach
    from the `results` stream and its associated near-Earth object.

    - A missing name is represented by the empty string.
    - A missing diameter is represented by either an empty string or by the string 'nan'.
    - The potentially_hazardous flag is represented either by the string 'False' or
    the string 'True'.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """

    fieldnames = (
        'datetime_utc',
        'distance_au',
        'velocity_km_s',
        'designation',
        'name',
        'diameter_km',
        'potentially_hazardous')

    with open(filename, "w") as out_stream:
        writer = csv.DictWriter(out_stream, fieldnames=fieldnames)
        writer.writeheader()

        for result in results:

            # get a dictionary of items of interests for every object
            approach_summary = list(result)[0]
            neo_summary = list(result)[1]

            # merge the two dictionaries
            approach_summary.update(neo_summary)
            # OR: approach_summary = dict(approach_summary, **neo_summary)

            writer.writerow(approach_summary)


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """

    json_data_list = []

    for result in results:

        # get a dictionary of items of interests for every object
        approach_summary = list(result)[0]
        neo_summary = list(result)[1]

        json_data = approach_summary
        # create a new key for neo and update it with the required summary
        json_data['neo'] = neo_summary

        json_data_list.append(json_data)
        # print(json_data)
        # input("ddd")

    with open(filename, 'w') as out_stream:
        json.dump(json_data_list, out_stream, indent='\t')
