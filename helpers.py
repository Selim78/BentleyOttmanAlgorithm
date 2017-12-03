#!/usr/bin/env python3
#pylint: disable=C0301
#pylint: disable=R0913

"""
definition of some useful functions
- nearest_living                :   finds nearest living at the left and the right of a segment
                                    and is not an endpoint of the said segments
- angle                         :   clockwise angle % pi between segment and the horizontal
- living_key                    :   key used to sort segments according to their angle
                                    and there intersection with a horizontal line defined by a point
- find_new_event                :   finds new event and updates results and events if necessary
- get_entries                   :   a parser
- progress_bar                  :   displays a progress bar in the console
"""

import sys
from math import pi, atan2
from pathlib import Path
import argparse
import re
from geo.point import Point
from geo.segment import Segment

def nearest_living(segment, living):
    """
    finds nearest living at the left and the right of a segment
    """
    index = living.index(segment)
    try:
        assert index < len(living) - 1
        right_segment = living[index + 1]
    except (IndexError, AssertionError):
        right_segment = None
    try:
        assert index > 0
        left_segment = living[index - 1]
    except (IndexError, AssertionError):
        left_segment = None
    return left_segment, right_segment

def angle(segment, adjuster):
    """
    clockwise angle % pi between segment and the horizontal
    """
    #we start by calculating the coordinates of the vector direction of the segment
    x_coordinate = segment.endpoints[0].coordinates[0] - segment.endpoints[1].coordinates[0]
    y_coordinate = segment.endpoints[0].coordinates[1] - segment.endpoints[1].coordinates[1]
    point = Point([x_coordinate, y_coordinate])
    point = adjuster.hash_point(point)
    [x_coordinate, y_coordinate] = point.coordinates
    atan2_angle = atan2(y_coordinate, x_coordinate)
    if atan2_angle >= 0:
        return pi - atan2_angle
    else:
        return - atan2_angle

def living_key(segment, current_point, adjuster):
    """
    key
    """
    point = Point([current_point.coordinates[0] + 10, current_point.coordinates[1]])
    other_point = Point([current_point.coordinates[0] - 10, current_point.coordinates[1]])
    swipe_line = Segment([point, other_point])
    intersection = segment.line_intersection_with(swipe_line)
    intersection = adjuster.hash_point(intersection)

    if intersection.coordinates[0] < current_point.coordinates[0]:
        return(intersection.coordinates[0], angle(segment, adjuster))
    else:
        return(intersection.coordinates[0], angle(segment, adjuster))


def find_new_event(segment_1, segment_2, current_point, events, results, adjuster):
    """
    finds new event and updates results and events if necessary
    """
    if segment_1 is None or segment_2 is None:
        return None
    else:
        new_intersection = segment_1.intersection_with(segment_2)
        if new_intersection is not None and new_intersection not in segment_1.endpoints + segment_2.endpoints:
            new_intersection = adjuster.hash_point(new_intersection)
            if new_intersection.coordinates[1] > current_point.coordinates[1]:
                # this condition is used to exclude crossings that have already been found
                events.add_event(new_intersection, [segment_1, segment_2], [], [], [])
                for segment in [segment_1, segment_2]:
                    if segment in results:
                        results[segment] += [new_intersection]
                    else:
                        results[segment] = [new_intersection]
            elif segment_1.endpoints[0].coordinates[1] == segment_1.endpoints[1].coordinates[1]:
                # this means 'segment' is in 'horizontal'
                for segment in [segment_1, segment_2]:
                    if segment in results:
                        results[segment] += [new_intersection]
                    else:
                        results[segment] = [new_intersection]
        else:
            return None


def get_entries():
    """
    parser
    """
    def bo_file(filepath):
        """
        'bo_file' type
        used in the parser
        """
        if not (Path(filepath).is_file() and re.compile(".*(.bo)$").match(filepath)):
            raise argparse.ArgumentTypeError("{} is not a .bo file or hasn't been found.".\
            format(filepath))
        return filepath

    parser = argparse.ArgumentParser(description='List all crossings in a set of line segments\
    using the Bentley–Ottmann algorithm.')

    parser.add_argument('-s', action='store_true', help='save the results as svg in ./outputs', default=False)
    parser.add_argument('-t', action='store_true', help='tycat the results', default=False)
    parser.add_argument('-l', action='store_true', help='add results to a log.csv file', default=False)
    parser.add_argument(dest='filepaths', nargs='+', type=bo_file, help='filepaths of the .bo files to analyse')

    bool_save, bool_tycat, bool_log, filepaths = parser.parse_args().s, parser.parse_args().t, parser.parse_args().l, parser.parse_args().filepaths

    return bool_save, bool_tycat, bool_log, filepaths

def progress_bar(events_left, finished):
    """
    displays a progress bar in the console
    """
    sys.stdout.write('\r')
    if events_left > finished:
        finished = events_left
    step = int((finished - events_left)/finished*100)
    print("   [{}{}] {}%".format('='*(step//4), ' '*(25-step//4), step), end='', flush=True)
    if step == 100:
        print("\n")
