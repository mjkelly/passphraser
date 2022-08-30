# Bias (numerical)

This is my amateur attempt at looking for bias in the generated results. I'm
not going to try to show that the random number generator is sufficiently
strong -- that is beyond me. Instead:

1. We're using a method of random number generation that is as simple as
   possible, leaving the distribution untampered.
2. We look at some stats that may convince us that the distribution is even
   enough that we're making good use of the whole word list.


## RNG Method 1

Here's the output of bias-checks.py on sample data generated with the following
method:

```
function randomNumberBetweenZeroAndOne() {
  var crypto = window.crypto || window.msCrypto;
  return crypto.getRandomValues(new Uint32Array(1))[0] / 4294967295;
}

function randomIndexes(num, wordListLength) {
  var output = [];
  for (var i = 0; i < num; i++) {
      var index = Math.floor(randomNumberBetweenZeroAndOne() * wordListLength);
      output.push(index);
  }
  return output;
}
```

This is what [useapassphrase](https://github.com/mike-hearn/useapassphrase)
does. I'm including this because it's a baseline of a well-known passphrase
generator.

Here, we generate a double between 0 and 1, then scale it to the length of the
word list.


```
mkelly@merlin:~/git/passphraser$ python3 ./bias-checks.py ~/old-output/output-all
2500000 samples
[11881. 24688.  3312. ... 18300. 13797. 15994.]
Mean: actual=22170.97, expected=22184.00, % difference = 0.06%

Evens: actual=1250541.00, expected=1250000.00, % difference = -0.04%
Odds: actual=1249459.00, expected=1250000.00, % difference = 0.04%

Distribution:
16th #1: actual=155945.00, expected=156250.00, % difference = 0.20%
16th #2: actual=156503.00, expected=156250.00, % difference = -0.16%
16th #3: actual=156710.00, expected=156250.00, % difference = -0.29%
16th #4: actual=156463.00, expected=156250.00, % difference = -0.14%
16th #5: actual=156353.00, expected=156250.00, % difference = -0.07%
16th #6: actual=156357.00, expected=156250.00, % difference = -0.07%
16th #7: actual=156921.00, expected=156250.00, % difference = -0.43%
16th #8: actual=155946.00, expected=156250.00, % difference = 0.19%
16th #9: actual=156425.00, expected=156250.00, % difference = -0.11%
16th #10: actual=156610.00, expected=156250.00, % difference = -0.23%
16th #11: actual=156387.00, expected=156250.00, % difference = -0.09%
16th #12: actual=155116.00, expected=156250.00, % difference = 0.73%
16th #13: actual=155545.00, expected=156250.00, % difference = 0.45%
16th #14: actual=156502.00, expected=156250.00, % difference = -0.16%
16th #15: actual=156614.00, expected=156250.00, % difference = -0.23%
```

## RNG Method 2

Here's the output for data generated with the following method:

```
function randomInt() {
  if (WORDS.length > 2 ** 16) {
    throw new Exception(`WORDS.length = ${WORDS.length}, too large`);
  }
  if (WORDS.length < 2 ** 15) {
    throw new Exception(`WORDS.length = ${WORDS.length}, too small`);
  }
  var crypto = window.crypto || window.msCrypto;

  do {
    // Generate a random int, and throw it away if it's larger than the max.
    // This works well for word lists of approximately our size. If WORDS is
    // too small, we'll retry too many times.
    r = crypto.getRandomValues(new Uint16Array(1))[0];
  } while (r >= WORDS.length)
  return r;
}

function randomInts(count) {
  var result = [];
  for (var i = 0; i < count; i++) {
    result.push(randomInt());
  }
  return result;
}
```

Here, we take advantage of the fact that the word list length is reasonably
close to 2^16, and generate a 16-bit unsigned int, then throw the result away
if it's too high.

```
mkelly@merlin:~/git/passphraser$ python3 ./bias-checks.py ~/new-output/output-all.v2
2500000 samples
[41011.  5946. 25489. ...  9539. 30542. 32427.]
Mean: actual=22194.71, expected=22184.00, % difference = -0.05%

Evens: actual=1249679.00, expected=1250000.00, % difference = 0.03%
Odds: actual=1250321.00, expected=1250000.00, % difference = -0.03%

Distribution:
16th #1: actual=156058.00, expected=156250.00, % difference = 0.12%
16th #2: actual=156152.00, expected=156250.00, % difference = 0.06%
16th #3: actual=155860.00, expected=156250.00, % difference = 0.25%
16th #4: actual=156252.00, expected=156250.00, % difference = -0.00%
16th #5: actual=156384.00, expected=156250.00, % difference = -0.09%
16th #6: actual=156558.00, expected=156250.00, % difference = -0.20%
16th #7: actual=156218.00, expected=156250.00, % difference = 0.02%
16th #8: actual=156006.00, expected=156250.00, % difference = 0.16%
16th #9: actual=155259.00, expected=156250.00, % difference = 0.63%
16th #10: actual=156122.00, expected=156250.00, % difference = 0.08%
16th #11: actual=156054.00, expected=156250.00, % difference = 0.13%
16th #12: actual=156625.00, expected=156250.00, % difference = -0.24%
16th #13: actual=157453.00, expected=156250.00, % difference = -0.77%
16th #14: actual=156420.00, expected=156250.00, % difference = -0.11%
16th #15: actual=156764.00, expected=156250.00, % difference = -0.33%
```

## References

- https://www.random.org/analysis/
