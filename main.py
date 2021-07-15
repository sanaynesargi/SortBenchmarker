from quicksort import quicksort
from mergesort import mergesort
from selectionsort import selectionsort
from insertionsort import insertionsort
from bubblesort import bubblesort
from multiprocessing import Process
from multiprocessing import Queue
import random
import json
import time
import matplotlib.pyplot as plt
import numpy as np

TIMEOUT = 7
PRECISION = 6


def _create_arrays(limit, exp):
    arrays = {}
    for i in range(limit):
        arr = []
        for j in range(exp ** i):
            arr.append(random.randint(0, 10 ** 6))
        random.shuffle(arr)
        arrays[f"{exp}^{i}"] = arr

    return arrays


class SortBenchmarker:
    def __init__(self, limit=6, exp=10):
        print("-----STARTING TESTS-----")
        print("-----CREATING TEST ARRAYS-----")
        self.exp = exp
        self.limit = limit
        self.times = dict()
        self.arrays = _create_arrays(self.limit, self.exp)

    def __str__(self):
        string = ""
        for k in self.arrays.keys():
            string += k + "\n"

        return string

    @staticmethod
    def sort(size, sort_func, arr, optional_args, q):
        start_time = time.time()
        if optional_args:
            sort_func(arr, 0, len(arr) - 1)
        else:
            sort_func(arr)
        end_time = time.time()

        q.put(round(end_time - start_time, PRECISION))

    def run_sort(self, size, sort_func, arr, optional_args):
        queue = Queue()
        process = Process(target=self.sort, args=(size, sort_func, arr, optional_args, queue))
        process.start()
        process.join(timeout=TIMEOUT)
        process.terminate()

        if process.exitcode == 0:
            return queue.get()
        else:
            return 10

    def run_tests(self):
        self.times["Qs"] = {}
        self.times["Ms"] = {}
        self.times["Ss"] = {}
        self.times["Is"] = {}
        self.times["Bs"] = {}

        print("-----STARTING BENCHMARKS-----")

        i = 1
        for title, arr in self.arrays.items():
            print(f"QUICKSORT TEST #{i}\n")
            self.times["Qs"][title] = self.run_sort(title, quicksort, arr, True)

            print(f"MERGESORT TEST #{i}\n")
            self.times["Ms"][title] = self.run_sort(title, mergesort, arr, False)

            print(f"INSERTION SORT TEST #{i}\n")
            self.times["Is"][title] = self.run_sort(title, insertionsort, arr, False)

            print(f"BUBBLESORT TEST #{i}\n")
            self.times["Bs"][title] = self.run_sort(title, bubblesort, arr, False)

            print(f"SELECTIONSORT TEST #{i}\n")
            self.times["Ss"][title] = self.run_sort(title, selectionsort, arr, False)

            i += 1

        print("-----DUMPING DATA TO RESULTS FILE-----\n")
        with open("results.json", "w") as results:
            json.dump(self.times, results)

        self.plot(self.times)

    def plot(self, data):
        fig = plt.figure()

        fig.canvas.manager.set_window_title("Sorting Benchmarks")

        i = 0
        plots = []
        for k, v in self.times.items():
            p, = plt.plot(list(self.times[k].values()), [x for x in range(6)], label=k)
            plots.append(p)
            i += 1

        plt.legend(handles=plots, title='Legend')
        plt.xticks(np.arange(0, 10, 0.5))

        graph, ax = plt.subplots()
        graph.canvas.manager.set_window_title("Table")
        plt.xlabel("Time Taken (seconds)")
        plt.ylabel("Array Size (powers of 10)")

        keys = list(self.times.keys())
        val2 = [x for x in self.times.keys()]
        val1 = [10**i for i in range(self.limit)]
        val3 = [
            [str(list(self.times[keys[r]].values())[c]) for c in range(self.limit)] for r in range(len(list(self.times.keys())))
        ]

        ax.set_axis_off()
        table = ax.table(
            cellText=val3,
            rowLabels=val2,
            colLabels=val1,
            rowColours=["palegreen"] * len(list(self.times.keys())),
            colColours=["palegreen"] * self.limit,
            cellLoc='center',
            loc='center')

        ax.set_title('Sorting Algorithm Comparisons',
                     fontweight="bold")

        plt.show()


def main():
    sorter = SortBenchmarker()
    sorter.run_tests()
    # arr = [34, 3, 1, 93, 9]
    # mergesort(arr)
    # print(arr)


if __name__ == "__main__":
    main()
