#!/usr/bin/env python3
#pylint: disable=R0914
#pylint: disable=C0301

"""
naive algorithm to find the crossigs between segments
"""


from time import time
from itertools import combinations
from scipy import special
from helpers import progress_bar


def naive(adjuster, segments):
    """
    implementation of the naive algorithl to find crossing
    between segments
    """

    results = {}
    graph = [[0], [0]] # This will be useful to observe the time complexity
    start = time()
    finished = special.binom(len(segments), 2) # This will be useful to print a progress bar in the console
    segments_processed = 0

    for segment_1, segment_2 in combinations(segments, 2):
        if time() - start >= 1200:
            return results, graph
        new_intersection = segment_1.intersection_with(segment_2)
        if new_intersection is not None:
            new_intersection = adjuster.hash_point(new_intersection)
            if new_intersection not in segment_1.endpoints + segment_2.endpoints:
                for segment in [segment_1, segment_2]:
                    if segment in results:
                        results[segment] += [new_intersection]
                    else:
                        results[segment] = [new_intersection]
        segments_processed += 1
        graph[0] += [time() - start]
        graph[1] += [len(list(set().union(*results.values())))]
        progress_bar(finished - segments_processed, finished)

    return results, graph
