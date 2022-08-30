'use strict;'

// When comparing to a traditional password, we generously assume 
// traditional passwords draw from almost every typeable character.
const equivalentPasswordCharsetSize = 89;

// Generates a random integer >= 0 and < WORDS.length. 
// There is a more sophisticated version of this here:
// https://stackoverflow.com/questions/41437492/how-to-use-window-crypto-getrandomvalues-to-get-random-values-in-a-specific-rang
function randomInt() {
  // Our method is hardcoded to work in a specific size range.
  // If we need to generate larger numbers, we can replace
  // Uint16Array with Uint32Array etc below.
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

// Returns `count` random ints that are >= 0 and < WORDS.length.
function randomInts(count) {
  var result = [];
  for (var i = 0; i < count; i++) {
    result.push(randomInt());
  }
  return result;
}

// Returns `count` random words from WORDS separated by `separator`.
function passphrase(words, separator) {
  var indexes = randomInts(words);
  return indexes.map(i => WORDS[i]).join(separator);
}

// Updates UI with a new passphrase. Suitable as a button callback etc.
function newPassphrase() {
  const passphraseElem = document.getElementById('passphrase');
  const lengthElem = document.getElementById('length');
  const separatorElem = document.getElementById('separator');
  const numberOfWords = parseInt(lengthElem.value);
  passphraseElem.innerHTML = passphrase(numberOfWords, separatorElem.value);
  showStats(numberOfWords);
}

// Copies current passphrase to the clipboard.
function copyPassphrase() {
  const copyElem = document.getElementById('copy-btn');
  const passphraseElem = document.getElementById('passphrase');
  const originalText = copyElem.innerHTML;

  navigator.clipboard.writeText(passphraseElem.innerHTML);
  copyElem.textContent = '✨ Copied!';
  window.setTimeout(() => {
    copyElem.innerHTML = originalText;
  }, 1000);
}

// Shows strength of current password, and determines an equivalently-strong traditional password.
function showStats(numberOfWords) {
  const statsElem = document.getElementById('stats');
  var entropyPerWord = Math.log2(WORDS.length);
  var totalEntropy = numberOfWords * entropyPerWord;
  var equivalentPasswordLen = Math.round(totalEntropy / Math.log2(equivalentPasswordCharsetSize))
  statsElem.innerHTML =
    `Using a ${WORDS.length}-word list, this passphrase has ${Math.round(totalEntropy)} bits of entropy. That's as strong as a  ${equivalentPasswordLen}-character random password, containing uppercase and lowercase letters, numbers, and symbols.`;
}
