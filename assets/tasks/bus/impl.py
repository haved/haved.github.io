#!/bin/env python3

n = int(input())
trips = []
for _ in range(n):
    times = input().split(' ')
    trips.append((int(times[0]), int(times[1])))

# Sort by decreasing arrive_time when the leave_time is the same
trips.sort(key=lambda x:x[1], reverse=True)
# By increasing leave_time
trips.sort(key=lambda x:x[0])

trips = [trips[0]] + [b for a,b in zip(trips, trips[1:]) if a!=b] #Remove duplicates

stack = []
for trip in trips:
    while stack and stack[-1][1] >= trip[1]:
        #The trip on the stack is worse than trip
        stack.pop()
    stack.append(trip)

# The stack contains trips not yet determined to be bad.
# The trips are processed in acending leave_time.
# This means any trip already on the stack, has a lower or equal
# leave_time than the trip we are currently looking at
# If the trip on the stack arrives later than the current trip
# that means the trip on the stack starts earlier and ends later
# than the current trip. Therefore the stack trip is worse, and the stack is popped.
# This is repeated until the trip on the top of the stack ends before the current trip.
# At that point, all trips down the stack are safe, because
# no trip further down the stack ends after the top trip.
# After the stack-popping is done, we add the current trip.

# If multiple trips start at the same time, the one
# with the larger arrive_time comes first, because
# it needs to be popped by the better trip, when it comes later.
# The sorting we do at the start makes sure
# that a trip always comes before the trip it is objectivly worse than.
# This means the last trip is guarranteed to be good.

print(len(stack))
for a, b in stack:
    print(a, b)
