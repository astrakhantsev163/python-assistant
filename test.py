nums = [2, 7, 11, 15]
target = 9

nums_copy = nums.copy()
list_sum = []
for i, num1 in enumerate(nums):
    for num2 in nums_copy[i+1:]:
        if num1 + num2 == target:
            list_sum.append(i)
    
print(list_sum)