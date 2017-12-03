#!/usr/bin/env python3
#pylint: disable=R0914
#pylint: disable=C0301

"""
this tests bentley ottmann on given .bo files.
for each file:
    - we display segments
    - run bentley ottmann
    - display results
    - print some statistics
"""


from time import time
from os.path import isfile, exists
from os import makedirs
import re
import matplotlib.pyplot as plt
from naive import naive
from geo.segment import load_segments
from geo.save_svg import save_svg
from geo.tycat import tycat
from events import Events
from helpers import living_key, nearest_living, find_new_event, get_entries, progress_bar



def bentley_ottmann(adjuster, segments):
    """
    implementation of the Bentley Ottmann algorithm
    """

    events = Events(segments)
    living = []
    results = {}

    graph = [[0], [0]] # This will be useful to observe the time complexity
    start = time()
    finished = len(events.heap) # This will be useful to print a progress bar in the console

    while events.heap and time() - start < 1200:

        current_point, intersection, lower, upper, horizontal = events.pop_event()
        """
        - lower = [segments that have the current_point as a lower endpoint]
        - upper = [segments that have the current_point as an upper endpoint]
        - intersection [segments that strike through the current_point but where
          the current_point is not an endpoint of the said segments]
        - horizontal = [horizontal segments that have the current_point as an endpoint]
        """

        for segment in horizontal:
            for other_segment in living:
                find_new_event(segment, other_segment, current_point, events, results, adjuster)

        for segment in upper:
            left_segment, right_segment = nearest_living(segment, living)
            find_new_event(left_segment, right_segment, current_point, events, results, adjuster)
            living.remove(segment)


        for segment in lower:
            living.append(segment)
            living.sort(key=lambda segment: living_key(segment, current_point, adjuster))
            left_segment, right_segment = nearest_living(segment, living)
            find_new_event(segment, right_segment, current_point, events, results, adjuster)
            find_new_event(left_segment, segment, current_point, events, results, adjuster)

        for segment in intersection:
            living.sort(key=lambda segment: living_key(segment, current_point, adjuster))
            left_segment, right_segment = nearest_living(segment, living)
            find_new_event(segment, right_segment, current_point, events, results, adjuster)
            find_new_event(left_segment, segment, current_point, events, results, adjuster)

        graph[0] += [time() - start]
        graph[1] += [len(list(set().union(*results.values())))]
        progress_bar(len(events.heap), finished)

    return results, graph



def test(filepath, bool_save, bool_tycat, bool_log):
    """
    - runs bentley ottmann and naive algorithm
    - prints the number of intersections and crossings within segments found with b_o
    - prints the runtime for both algorithm
    - if bool_save = True, saves the figure with all the crossings found with b_o
    - if bool_tycat = True, displays the figure with all the crossings found with b_o
    - if bool_log = True, save statistics in a log.csv file
    """

    adjuster, segments = load_segments(filepath)
    name_of_figure = re.match(r"(.*/|.*)(.+).bo", filepath).group(2)

    # Launching Bentley-Ottmann
    print("\n   Running Bentley Ottmann on {} ...\n".format(name_of_figure))
    results_bo, graph_bo = bentley_ottmann(adjuster, segments)

    # Printing some statistics
    unique_intersections = list(set().union(*results_bo.values()))
    number_of_unique_intersections = len(unique_intersections)
    number_of_crossings = sum([len(list) for list in results_bo.values()])
    if graph_bo[0][-1] >= 1199:
        runtime_bo = ">20m"
    else:
        runtime_bo = "{}m {}s".format(round(graph_bo[0][-1]//60), graph_bo[0][-1]%60)
    print("   Unique intersections          :   {}".format(number_of_unique_intersections))
    print("   Crossings within segments     :   {}".format(number_of_crossings))
    print("   Runtime for Bentley Ottmann   :   {}\n".format(runtime_bo))

    # Launching naive algorithm
    print("\n   Running naive algorithm on {} ...\n".format(name_of_figure))
    results_na, graph_na = naive(adjuster, segments)
    if graph_na[0][-1] >= 1199:
        runtime_na = ">20m"
    else:
        runtime_na = "{}m {}s".format(round(graph_na[0][-1]//60), graph_na[0][-1]%60)
    print("   Runtime for naive algorithm   :   {}\n".format(runtime_na))


    # Ploting the results to png file
    directory = "./outputs"
    if not exists(directory):
        makedirs(directory)
    plt.xlabel('Time elapsed (s)')
    plt.ylabel('Intersections processed')
    plt.title('{}.png'.format(name_of_figure))
    plt.plot(graph_bo[0], graph_bo[1], label='Bentley Ottmann')
    plt.plot(graph_na[0], graph_na[1], label='Naive algorithm')
    plt.legend()
    plt.savefig('./outputs/{}.png'.format(name_of_figure))
    plt.clf()


    # If Bentley-Ottmann didn't end before 20m, we save the results from the naive algorithm
    if runtime_bo == ">20m":
        unique_intersections = list(set().union(*results_na.values()))
        number_of_unique_intersections = len(unique_intersections)
        number_of_crossings = sum([len(list) for list in results_na.values()])


    # Printing and/or saving the figure with all the found crossings
    if bool_save:
        save_svg([segments, unique_intersections], filepath)
    if bool_tycat:
        tycat(segments, unique_intersections)


    #Saving the statistics in a csv file
    if bool_log:
        if not isfile("./log.csv"):
            with open("log.csv", "w") as file:
                file.write("File; Unique intersections;Crossings;Runtime with Bentley-Ottmann;Runtime with naive algorithm\n")
        with open("log.csv", "a") as file:
            file.write("{}; {}; {}; {}; {}\n".format(name_of_figure, number_of_unique_intersections, number_of_crossings, runtime_bo, runtime_na))


def main():
    """
    launch test on each file.
    """
    bool_save, bool_tycat, bool_log, filepaths = get_entries()

    for filepath in filepaths:
        test(filepath, bool_save, bool_tycat, bool_log)

if __name__ == "__main__":
    main()
