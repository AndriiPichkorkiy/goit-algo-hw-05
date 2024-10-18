def binary_search(arr, x):
    low = 0
    high = len(arr) - 1
    mid = 0
    count_itterations = 0
    upper = None

    while low <= high:
        mid = (high + low) // 2
        count_itterations += 1

        if arr[mid] == x:
            return [count_itterations, arr[mid]]
        elif arr[mid] < x:
            low = mid + 1
        else:
            high = mid - 1
            upper = arr[mid]

    return [count_itterations, upper]


if __name__ == "__main__":
    x = [1.1, 2.2, 3.3, 4.4, 5.5]
    print(binary_search(x, 4))
