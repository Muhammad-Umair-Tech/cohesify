# Quicksort for Users
# Mergesort for posts

def swap(arr, i, j):
    arr[i], arr[j] = arr[j], arr[i]

def quick_sort(arr, low, high):
    if low < high:
        p = partition(arr, low, high)
        quick_sort(arr, low, p - 1)
        quick_sort(arr, p + 1, high)

def partition(arr, low, high):
    pivot = ord(arr[high].username[0])
    i = low - 1
    for j in range(low, high):
        if ord(arr[j].username[0]) <= pivot:
            i = i + 1
            swap(arr, i, j)
    swap(arr, i + 1, high)
    return i + 1

def quick_sort_descending(arr, low, high):
    if low < high:
        p = partition_descending(arr, low, high) # Partition index
        quick_sort_descending(arr, low, p - 1)
        quick_sort_descending(arr, p + 1, high)

def partition_descending(arr, low, high):
    pivot = ord(arr[high].username[0])
    i = low - 1
    for j in range(low, high):
        if ord(arr[j].username[0]) >= pivot:
            i = i + 1
            swap(arr, i, j)
    swap(arr, i + 1, high)
    return i + 1

def merge(arr, left, mid, right):
    n1 = mid - left + 1
    n2 = right - mid

    L = [0] * n1
    R = [0] * n2

    for i in range(n1):
        L[i] = arr[left + i]
    for i in range(n2):
        R[i] = arr[mid + 1 + i]

    i = 0
    j = 0
    k = left

    while i < n1 and j < n2:
        if L[i].created_at <= R[j].created_at:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1

    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1

def merge_sort(arr, left, right):
    if left < right:
        mid = (left + right) // 2

        merge_sort(arr, left, mid)
        merge_sort(arr, mid + 1, right)
        merge(arr, left, mid, right)

def merge_descending(arr, left, mid, right):
    n1 = mid - left + 1
    n2 = right - mid

    L = [0] * n1
    R = [0] * n2

    for i in range(n1):
        L[i] = arr[left + i]
    for i in range(n2):
        R[i] = arr[mid + 1 + i]

    i = 0
    j = 0
    k = left

    while i < n1 and j < n2:
        if L[i].created_at >= R[j].created_at:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1

    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1

def merge_sort_descending(arr, left, right):
    if left < right:
        mid = (left + right) // 2

        merge_sort_descending(arr, left, mid)
        merge_sort_descending(arr, mid + 1, right)
        merge_descending(arr, left, mid, right)

def mergesort_descending_queryset(queryset):
    arr = [q for q in queryset]
    merge_sort_descending(arr, 0, len(arr) - 1)
    return arr

def mergesort_queryset(queryset):
    arr = [q for q in queryset]
    merge_sort(arr, 0, len(arr) - 1)
    return arr    

def sort_by_trend(posts):
    n = len(posts)
    for i in range(1, n):
        key = posts[i]
        j = i - 1
        while j >= 0 and posts[j].like_count < key.like_count:
            posts[j + 1] = posts[j] # Shift right
            j -= 1
        posts[j + 1] = key