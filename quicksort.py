import random


def quicksort(arr, l, r):
    if len(arr) == 1:
        return arr
    if l < r:
        pivot_index = random.randint(l, r)
        pivot = arr[pivot_index]
        arr[l], arr[pivot_index] = arr[pivot_index], arr[l]
        i = l + 1

        j = l
        while j <= r:
            if arr[j] < pivot:
                arr[j], arr[i] = arr[i], arr[j]
                i += 1
            j += 1

        pi = i - 1
        arr[l], arr[pi] = arr[pi], arr[l]

        quicksort(arr, l, pi - 1)
        quicksort(arr, pi + 1, r)
