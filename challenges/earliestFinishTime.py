# 3635. Earliest Finish Time for Land and Water Rides II
# Medium
# Topics
# premium lock icon
# Companies
# Hint
# You are given two categories of theme park attractions: land rides and water rides.

# Land rides
# landStartTime[i] – the earliest time the ith land ride can be boarded.
# landDuration[i] – how long the ith land ride lasts.
# Water rides
# waterStartTime[j] – the earliest time the jth water ride can be boarded.
# waterDuration[j] – how long the jth water ride lasts.
# A tourist must experience exactly one ride from each category, in either order.

# A ride may be started at its opening time or any later moment.
# If a ride is started at time t, it finishes at time t + duration.
# Immediately after finishing one ride the tourist may board the other (if it is already open) or wait until it opens.
# Return the earliest possible time at which the tourist can finish both rides.

 

# Example 1:

# Input: landStartTime = [2,8], landDuration = [4,1], waterStartTime = [6], waterDuration = [3]

# Output: 9

# Explanation:​​​​​​​

# Plan A (land ride 0 → water ride 0):
# Start land ride 0 at time landStartTime[0] = 2. Finish at 2 + landDuration[0] = 6.
# Water ride 0 opens at time waterStartTime[0] = 6. Start immediately at 6, finish at 6 + waterDuration[0] = 9.
# Plan B (water ride 0 → land ride 1):
# Start water ride 0 at time waterStartTime[0] = 6. Finish at 6 + waterDuration[0] = 9.
# Land ride 1 opens at landStartTime[1] = 8. Start at time 9, finish at 9 + landDuration[1] = 10.
# Plan C (land ride 1 → water ride 0):
# Start land ride 1 at time landStartTime[1] = 8. Finish at 8 + landDuration[1] = 9.
# Water ride 0 opened at waterStartTime[0] = 6. Start at time 9, finish at 9 + waterDuration[0] = 12.
# Plan D (water ride 0 → land ride 0):
# Start water ride 0 at time waterStartTime[0] = 6. Finish at 6 + waterDuration[0] = 9.
# Land ride 0 opened at landStartTime[0] = 2. Start at time 9, finish at 9 + landDuration[0] = 13.
# Plan A gives the earliest finish time of 9.

# Example 2:

# Input: landStartTime = [5], landDuration = [3], waterStartTime = [1], waterDuration = [10]

# Output: 14

# Explanation:​​​​​​​

# Plan A (water ride 0 → land ride 0):
# Start water ride 0 at time waterStartTime[0] = 1. Finish at 1 + waterDuration[0] = 11.
# Land ride 0 opened at landStartTime[0] = 5. Start immediately at 11 and finish at 11 + landDuration[0] = 14.
# Plan B (land ride 0 → water ride 0):
# Start land ride 0 at time landStartTime[0] = 5. Finish at 5 + landDuration[0] = 8.
# Water ride 0 opened at waterStartTime[0] = 1. Start immediately at 8 and finish at 8 + waterDuration[0] = 18.
# Plan A provides the earliest finish time of 14.​​​​​​​

 

# Constraints:

# 1 <= n, m <= 5 * 104
# landStartTime.length == landDuration.length == n
# waterStartTime.length == waterDuration.length == m
# 1 <= landStartTime[i], landDuration[i], waterStartTime[j], waterDuration[j] <= 105


def earliestFinishTime(self, landStartTime, landDuration, waterStartTime, waterDuration):
    land_trips = sorted(zip(landStartTime, landDuration))
    water_trips = sorted(zip(waterStartTime, waterDuration))

    n, m = len(land_trips), len(water_trips)

        # prefix min duration: shortest land ride among first i+1 (sorted by open time)
    land_prefix_min_dur = [0]*n
    land_prefix_min_dur[0] = land_trips[0][1]
    for i in range(1, n):
        land_prefix_min_dur[i] = min(land_prefix_min_dur[i-1], land_trips[i][1])

    water_prefix_min_dur = [0]*m
    water_prefix_min_dur[0] = water_trips[0][1]
    for i in range(1, m):
        water_prefix_min_dur[i] = min(water_prefix_min_dur[i-1], water_trips[i][1])

        # suffix min finish time: earliest finish among rides from i to end
    land_suffix_min_finish = [0]*n
    land_suffix_min_finish[n-1] = land_trips[n-1][0] + land_trips[n-1][1]
    for i in range(n-2, -1, -1):
        finish = land_trips[i][0] + land_trips[i][1]
        land_suffix_min_finish[i] = min(land_suffix_min_finish[i+1], finish)

    water_suffix_min_finish = [0]*m
    water_suffix_min_finish[m-1] = water_trips[m-1][0] + water_trips[m-1][1]
    for i in range(m-2, -1, -1):
        finish = water_trips[i][0] + water_trips[i][1]
        water_suffix_min_finish[i] = min(water_suffix_min_finish[i+1], finish)

    result = float('inf')

        # Case 1: land first, then water
    for i in range(n):
        land_finish = land_trips[i][0] + land_trips[i][1]
            # binary search: first water ride with start >= land_finish
        lo, hi = 0, m
        while lo < hi:
            mid = (lo + hi) // 2
            if water_trips[mid][0] >= land_finish:
                hi = mid
            else:
                lo = mid + 1
        if lo < m:
             # water ride opens after we're free -> board immediately, use shortest from here on
            result = min(result, land_finish + water_suffix_min_finish[lo] - water_trips[lo][0])
        else:
            # all water rides already open -> last one's prefix min duration applies
            result = min(result, land_finish + water_prefix_min_dur[m-1])

    # Case 2: water first, then land (symmetric)
    for j in range(m):
        water_finish = water_trips[j][0] + water_trips[j][1]
        lo, hi = 0, n
        while lo < hi:
            mid = (lo + hi) // 2
            if land_trips[mid][0] >= water_finish:
                hi = mid
            else:
                lo = mid + 1
        if lo < n:
            result = min(result, water_finish + land_suffix_min_finish[lo] - land_trips[lo][0])
        else:
            result = min(result, water_finish + land_prefix_min_dur[n-1])

    return result