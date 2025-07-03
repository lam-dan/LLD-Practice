"""
Problem Statement
Keep track of average transit times between stations in a subway system.
Each rider has a card, which they swipe in when entering a station AND swipe out when exiting a station.
The cards have unique identifiers, and we can assume that riders do not share or lose cards.
We wish to implement an application that uses entry/exit swipe information (card, time, station) to answer
queries of average transit time between a pair of stations.

RiderTrip	Composition — system has-a RiderTrip
TripStats	Composition — system has-a TripStats
SwipeEvent	Behavioral — represents an external action
TransitSystem - Composes other classes, processes behavior
"""
from io import StringIO
import csv

# Represents in-progress trip for a rider
class RiderTrip:
    def __init__(self, start_station, start_time):
        self.start_station = start_station
        self.start_time = start_time

# Holds aggregate stats for each station pair
class TripStats:
    def __init__(self):
        self.total_time = 0
        self.trip_count = 0

    def add_trip(self, duration):
        self.total_time += duration
        self.trip_count += 1

    def get_average(self):
        if self.trip_count == 0:
            return 0.0
        return self.total_time / self.trip_count

# Represents a swipe event
class SwipeEvent:
    def __init__(self, card_id, station_id, is_entry, timestamp):
        self.card_id = card_id
        self.station_id = station_id
        self.is_entry = is_entry
        self.timestamp = timestamp

# Transit system using explicit composition
class TransitSystem:
    def __init__(self):
        self.active_rides = {}  # card_id -> RiderTrip
        self.trip_stats = {}    # (start, end) -> TripStats

    def process_swipe(self, event: SwipeEvent):
        if event.is_entry:
            self.active_rides[event.card_id] = RiderTrip(event.station_id, event.timestamp)
        else:
            if event.card_id not in self.active_rides:
                return  # Defensive coding for invalid exit
            trip = self.active_rides.pop(event.card_id)
            duration = event.timestamp - trip.start_time
            key = (trip.start_station, event.station_id)
            
            if key not in self.trip_stats:
                self.trip_stats[key] = TripStats()
                
            self.trip_stats[key].add_trip(duration)

    def get_average_time(self, start_station, end_station):
        stats = self.trip_stats.get((start_station, end_station))
        if not stats:
            return 0.0
        return stats.get_average()

    def print_trip_stats(self):
        for (start, end), stats in self.trip_stats.items():
            print(f"From '{start}' to '{end}': total_time = {stats.total_time}, trip_count = {stats.trip_count}, average_time = {stats.get_average():.2f}")

csv_data = StringIO(
    """card_id, station_id, is_entry, timestamp
2, Spring Street, true, 500
1, Times Square, true, 1000
3, Times Square, true, 1000
1, Grand Central, false, 2000
1, Grand Central, true, 10000
2, Main Street, false, 20000
3, Grand Central, false, 30000
4, Grand Central, true, 30000
4, Grand Central, false, 30500
""")
system = TransitSystem()
reader = csv.DictReader(csv_data, skipinitialspace=True)

for row in reader:
    event = SwipeEvent(
        card_id=row["card_id"],
        station_id=row["station_id"],
        is_entry=row["is_entry"].lower() == "true",
        timestamp=int(row["timestamp"])
    )
    system.process_swipe(event)

# Example Queries
# print(system.get_average_time("Times Square", "Grand Central"))  # 15000.0
# print(system.get_average_time("Spring Street", "Main Street"))   # 19500.0
# print(system.get_average_time("Grand Central", "Grand Central")) # 500.0
print(system.print_trip_stats())

'''
S — Single Responsibility Principle (SRP)
Each class should have only one reason to change.
Class	Responsibility
SwipeEvent	Holds swipe event data (card, station, time)
RiderTrip	Tracks the state of an active trip (start station/time)
TripStats	Manages total time and trip counts for station pairs
TransitSystem	Coordinates behavior by composing these objects

O — Open/Closed Principle (OCP)
Classes should be open for extension but closed for modification.
You can:
Extend TripStats to track more stats (min/max time)
Add methods to RiderTrip for future features (e.g., distance tracking)
Introduce new types of events (e.g., failed swipes)
Without modifying:
TransitSystem's core logic
System structure allows feature growth via new classes or enhancements without breaking existing code

L — Liskov Substitution Principle (LSP)
Subtypes must be substitutable for their base types.
You currently don't use inheritance, but:
If you introduced subclasses for TripStats or RiderTrip (e.g., PremiumRiderTrip), they could cleanly replace base types
Your composition approach avoids fragile inheritance chains
Design is LSP-compliant by being inherently modular and substitution-friendly

I — Interface Segregation Principle (ISP)
Clients shouldn't be forced to depend on interfaces they don't use.
Your system keeps responsibilities narrow:
TripStats only exposes aggregation methods
RiderTrip only tracks start station/time
No "fat" interfaces forcing unrelated dependencies
Small, focused classes prevent unnecessary coupling or bloated dependencies

D — Dependency Inversion Principle (DIP)
Depend on abstractions, not concretions.
Current example is minimal, but with factories or interfaces:
You could inject different implementations of TripStats (e.g., for testing, logging, advanced stats)
Even now, your use of composition prepares the system for DIP by structuring logic around smaller, replaceable objects'''
