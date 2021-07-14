def bubblesort(arr):
    while True:
        i = 0
        swaps = 0
        while i < len(arr) - 2:
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swaps += 1
            i += 1

        if swaps == 0:
            break

    return arr
