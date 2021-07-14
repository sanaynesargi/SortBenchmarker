def selectionsort(arr):
    least_index = 0
    while least_index < len(arr) - 2:
        shortened_arr = arr[least_index:]
        minimum_element = min(shortened_arr)
        minimum_element_index = arr.index(minimum_element)
        arr[least_index], arr[minimum_element_index] = arr[minimum_element_index], arr[least_index]
        least_index += 1

    return arr
