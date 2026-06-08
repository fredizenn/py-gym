def shuffle(nums, n):
    if nums.length == 2 * n and n <= 500 and n >= 1:
        return [val for i in range(n) for val in (nums[i], nums[i + n])]