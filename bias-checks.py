#!/usr/bin/python3
# This is my amateur-statistician attempt at determining if the output is
# skewed in one way or another.
#
# Usage:
#   python3 ./bias-checks.py <file-with-indices>
#
# The input file is the output of the /benchmark/ endpoint: integers
# in [0, WORDS), five per line, as many lines as you copied. It also
# accepts one integer per line.
#
# References:
# - https://www.random.org/analysis/
import argparse
import math
import re
import sys
import warnings
from pathlib import Path

import numpy as np
from scipy.stats import chi2 as _chi2

def chi2_sf(x, df):
    """Survival function P(Chi2_df > x), i.e. the chi-squared p-value.

    Uses scipy when available (most accurate). Otherwise falls back to
    a pure-Python regularised upper incomplete gamma function
    (Numerical Recipes gammq), which is exact for this purpose and
    needs no extra dependency.
    """
    if x <= 0:
        return 1.0
    return float(_chi2.sf(x, df))


def compare(label, actual, expected):
    print(f"{label}: actual={actual:.2f}, expected={expected:.2f}, ", end="")
    pct_diff(actual, expected)


def pct_diff(actual, expected):
    diff = (expected - actual) / expected
    print(f"% difference = {diff * 100.0:.2f}%")


def chi2_report(label, chi2, df):
    p = chi2_sf(chi2, df)
    print(f"{label} chi-squared: chi2={chi2:.2f}, df={df}, p={p:.4g}")
    return p


def count_words(wordlist_path):
    text = Path(wordlist_path).read_text()
    return len(re.findall(r"'([^']+)'", text))


def count_wordlist():
    script_dir = Path(__file__).resolve().parent
    for candidate in (script_dir / "assets" / "wordlist.js",
                      Path.cwd() / "assets" / "wordlist.js"):
        if candidate.is_file():
            try:
                words = count_words(candidate)
                print(f"{words} words in {candidate}")
                return words
            except OSError:
                continue
    raise ValueError("Could not find wordlist.js")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Check a benchmark output file for bias in the "
                    "generated word indices.")
    parser.add_argument("filename", help="file of indices, e.g. benchmark output")
    parser.add_argument("--words", type=int, default=None,
                        help="wordlist size; default: count assets/wordlist.js")
    parser.add_argument("--buckets", type=int, default=16,
                        help="number of distribution buckets (default: 16)")
    args = parser.parse_args(argv)

    if args.buckets < 2:
        parser.error("--buckets must be at least 2")

    if args.words is not None:
        words = args.words
    else:
        words = count_wordlist()
    if args.buckets > words:
        parser.error("--buckets cannot exceed the wordlist size")

    try:
        with warnings.catch_warnings():
            # loadtxt warns on empty input; we report that ourselves below.
            warnings.simplefilter("ignore")
            arr = np.loadtxt(args.filename, dtype=np.int64).flatten()
    except (OSError, ValueError) as exc:
        print(f"error: cannot read indices from {args.filename}: {exc}",
              file=sys.stderr)
        return 2

    n = len(arr)
    if n == 0:
        print("error: no samples in input", file=sys.stderr)
        return 2

    print(f"{n} samples, wordlist size {words}")
    print(f"first 10 samples: {arr[:10].tolist()}")
    print(f"min={arr.min()}, max={arr.max()}")

    out_of_range = int(((arr < 0) | (arr >= words)).sum())
    if out_of_range:
        print(f"ERROR: {out_of_range} sample(s) outside [0, {words}) -- "
              f"the generator produced an index the word list cannot hold",
              file=sys.stderr)
        return 2
    print()

    # Mean, with its standard error, so the deviation can be judged.
    mean = float(arr.mean())
    expected_mean = (words - 1) / 2.0
    sd = math.sqrt((words ** 2 - 1) / 12.0)
    se = sd / math.sqrt(n)
    compare("Mean", mean, expected_mean)
    print(f"Mean z-score: {(mean - expected_mean) / se:.2f} "
          f"(SE={se:.2f}; |z| > ~3 is worth investigating)")
    print()

    # Even/odd: 0 is even, so evens are (words + 1) // 2 values.
    n_even = (words + 1) // 2
    n_odd = words // 2
    expected_even = n * (n_even / words)
    expected_odd = n * (n_odd / words)
    even = int((arr % 2 == 0).sum())
    odd = n - even
    compare("Evens", even, expected_even)
    compare("Odds", odd, expected_odd)
    chi2_report("Even/odd",
                (even - expected_even) ** 2 / expected_even
                + (odd - expected_odd) ** 2 / expected_odd, 1)
    print()

    # Buckets: partition [0, words) exactly, no dropped tail.
    k = args.buckets
    edges = [(i * words) // k for i in range(k + 1)]
    counts, _ = np.histogram(arr, bins=edges)
    print("Distribution:")
    chi2 = 0.0
    for i in range(k):
        expected = n * (edges[i + 1] - edges[i]) / words
        chi2 += (counts[i] - expected) ** 2 / expected
        compare(f"{k}th #{i + 1} [{edges[i]}..{edges[i + 1] - 1}]",
                float(counts[i]), expected)
    chi2_report(f"{k}-bucket distribution", chi2, k - 1)
    print()

    # Full per-word distribution. With n samples the expected count per
    # word is n / words; if that is below ~5 the p-value is only
    # approximate, and the bucket test above is the more reliable one.
    per_word = np.bincount(arr, minlength=words)
    expected_per_word = n / words
    full_chi2 = float(((per_word - expected_per_word) ** 2
                       / expected_per_word).sum())
    if expected_per_word < 5:
        print(f"note: expected count per word is {expected_per_word:.2f} "
              f"(< 5), so the full-distribution p-value is approximate; "
              f"rely on the bucket test")
    chi2_report("Full per-word distribution", full_chi2, words - 1)
    print(f"per-word counts: min={per_word.min()}, max={per_word.max()}, "
          f"expected={expected_per_word:.2f}")
    print()
    print("Reading the p-values: a small p (e.g. < 0.01) is evidence "
          "against uniformity. A large p is not proof of uniformity, "
          "only that this sample did not detect a deviation.")
    print("Reading the chi2 values: under a truly uniform generator, chi2 is "
          "expected to be about equal to df, give or take roughly sqrt(2*df).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
