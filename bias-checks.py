#!/usr/bin/python3
# This is my amateur-statistician attempt at determining if the output is
# skewed in one way or another.
#
# References:
# - https://www.random.org/analysis/
import sys
import math
import numpy as np


def compare(label, actual, expected):
    print(f"{label}: actual={actual:.2f}, expected={expected:.2f}, ", end="")
    pct_diff(actual, expected)

def pct_diff(actual, expected):
    diff = (expected - actual) / expected
    print(f"% difference = {diff * 100.0:.2f}%")


WORDS = 44344

filename = sys.argv[1]
arr = np.loadtxt(filename).flatten()

print(f"{len(arr)} samples")
print(arr)

mean = arr.mean()
expected_mean = WORDS / 2
compare("Mean", mean, expected_mean)
print()

# we start at 0, and the max value is WORDS - 1. So if WORDS = 6, we generate
# 0-5 inclusive. even = 3 (0, 2, 4), odd = 3 (1, 3, 5). So
# WORDS // 2 = even and odd if WORDS is even.
# If WORDS is odd, we lose 1 odd value but have the same number of
# even values. Odd = WORDS // 2 still works, but even is math.ceil(WORDS / 2).
n_even = WORDS // 2
n_odd = math.ceil(WORDS / 2)
expected_even = len(arr) * (n_even / WORDS)
expected_odd = len(arr) * (n_odd / WORDS)

even = len([i for i in arr if (i % 2) == 0])
odd = len([i for i in arr if (i % 2) != 0])
compare("Evens", even, expected_even)
compare("Odds", odd, expected_odd)
print()

print(f"Distribution:")
lower = 0
for i, upper in enumerate(range(WORDS // 16, WORDS, WORDS // 16)):
    expected = len(arr) // 16
    actual = len([i for i in arr if lower <= i < upper])
    compare(f"16th #{i+1}", actual, expected)
    lower = upper
