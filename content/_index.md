---
title: Passphraser
---
## Why should I use a random passphrase?

The passwords that most people come up with are hard to remember _and_ easy for computers to guess. Randomness is the source of strength in a password, and humans are terrible at coming up with randomness.

We use common words, easily-typed sequences on a keyboard, or our own personal information, which a motivated attacker can learn.

Strong, random passwords like `pQ[!:WQblzY2` are hard to remember.

Random passphrases can be equally as strong but are easier to remember. For example, `sarcasm towel mimosas smallest censoring` is a passphrase of approximately equal strength to `pQ[!:WQblzY2`. If you find the passphrase easier to remember, you are not alone. Passphrases are easier for most humans to remember, but no easier for computers to guess.

For a longer discussion about how passwords are cracked, check out [useapassphrase.com][uap]. It's the site this one is based on!

[uap]: https://www.useapassphrase.com/

## How do you determine password strength? How do you compare the strength of a password and a passphrase?

The most principled way of determining password complexity is to assume your attacker knows your password generation scheme. So if you're using a 10-character random password with a specific set of special characters, assume they know that. Now, trick to remaining secure is to make them search as many passwords as possible.

For instance, a 5-character random password made up of only lowercase letters (26 options), has `26 * 26 * 26 * 26 * 26` combinations, because you can use any of 26 different letters in each of 5 places. That's 11,881,376 combinations. That sounds like a lot, but hackers can guess passwords at a very high rate that's always increasing.

Since these numbers of combinations get huge, we usually talk about the log-base-2 (log2) of these numbers. `log2(11,881,376) = 23.5`. We call this number _bits of entropy_, so a 5-character random password made up of only lowercase letters has 23.5 bits of entropy. Remember, we're talking about log-base-2, so for every added bit of entropy in a password, an attacker must guess twice as many combinations.

This gives us a way to compare passphrases and passwords. Passphrases are just like passwords, but each word in the passphrase is taken from a word list. If your word list has 5,000 words, and you have a 4-word random passphrase, you have `5,000 * 5,000 * 5,000 * 5,000 = 625,000,000,000,000` combinations. `log2(625,000,000,000,000) = 49.1`, so a random passphrase generated this way has 49.1 bits of entropy.

If you use uppercase and lowercase letters, numbers, and all special symbols, you're choosing from 89 characters. A 8-character random password chosen from those 89 characters has 51.8 bits of entropy, so it's just a little stronger than the passphrase above.