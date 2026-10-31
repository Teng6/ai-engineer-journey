def main():
    nums = [1, 2, 2, 3, 3, 3]
    k = 2
    
    d = {}
    for num in nums:
        if num in d:
            d[num] += 1
        else:
            d[num] = 1
    
    sorted_d = sorted(d, key=d.get, reverse=True)

    return sorted_d[:k]


print(main())