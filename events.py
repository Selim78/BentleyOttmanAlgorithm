#!/usr/bin/env python3
#pylint: disable=R0913
#pylint: disable=C0301

"""
Definition of the Event class
Event objects are a heaps where priority = y axis coordinates, x axis coordinates, counter
"""

import itertools
from heapq import heappush, heappop

class Events():
    """
    Events Class
    """
    def __init__(self, segments):
        self.heap = []                    # list of events arranged in a heap
        self.event_finder = {}            # mapping of points to events
        self.counter = itertools.count()  # unique sequence count : events can all be differentied
        for segment in segments:          # creation of the events from the iterable segments
            upper_point = max(segment.endpoints, key=lambda point: point.coordinates[::-1])
            lower_point = min(segment.endpoints, key=lambda point: point.coordinates[::-1])
            if upper_point.coordinates[1] != lower_point.coordinates[1]:
                self.add_event(lower_point, [], [segment], [], [])
                self.add_event(upper_point, [], [], [segment], [])
            else:
                self.add_event(lower_point, [], [], [], [segment])

    def add_event(self, point, intersection, lower, upper, horizontal):
        """
        Adds a new event or updates an existing event
        - lower = [segments that have the point as a lower endpoint]
        - upper = [segments that have the point as an upper endpoint]
        - intersection [segments that strike through the point but where
          the point is not an endpoint of the said segments]
        - horizontal = [horizontal segments that have the point as an endpoint]

        The events are sorted by priority where priority = event.coordinates[::-1], count
        """
        if point is None:
            return
        else:
            if point not in self.event_finder:
                count = next(self.counter)
                event = [point.coordinates[::-1], count, point, intersection, lower, upper, horizontal]
                self.event_finder[point] = event
                heappush(self.heap, event)
            else:
                event = self.event_finder[point]
                event[3] += intersection
                event[4] += lower
                event[5] += upper
                event[6] += horizontal


    def pop_event(self):
        """
        Removes and returns the lowest priority event. Raises KeyError if empty.
        """
        #pylint: disable=unused-variable
        while self.heap:
            [_, _, point, intersection, lower, upper, horizontal] = heappop(self.heap)
            del self.event_finder[point]
            return point, intersection, lower, upper, horizontal
        raise KeyError('pop from an empty priority queue')
