---
title: Passphraser
---
## Why should I use a random passphrase?

The passwords that most people come up with are hard for humans to remember _and_ easy for computers to guess. Randomness is the source of strength in a password, and humans are terrible at coming up with randomness.

We use common words, easily-typed sequences on a keyboard, or our own personal information, which a motivated attacker can learn.

Strong, random passwords like `pQ[!:WQblzY2` are hard to remember.

Random passphrases, on the other hand, consist of a series of words. They must be longer (in terms of characters) to be as strong as passwords, but they're easier to remember for most people. For example, `sarcasm towel mimosas smallest censoring` is a passphrase approximately as strong as `pQ[!:WQblzY2`. If you find the passphrase easier to remember, you are not alone.That's the advantage of passphrases.

## How strong of a passphrase do I need?

The default setting on this page (a 5-word passphrase) create a strong
password, designed to be suitable for high-value accounts like your email.

Estimates on different websites say a password like `pQ[!:WQblzY2` or a
passphrase like `sarcasm towel mimosas smallest censoring` take between 34,000
years and 400,000 years to crack as of 2022. The time it takes an attacker to
crack a given password is always decreasing, as computers get faster and
faster.

Here are some references:

- [CNBC](https://www.cnbc.com/2022/03/20/study-if-your-passwords-are-less-than-8-characters-long-change-them.html)
- [security.org](https://www.security.org/how-secure-is-my-password/)

All the passwords generated on this site, regardless of settings, exceed the
complexity of the recommended password length from NIST's [Digital Identity
Guidelines](https://pages.nist.gov/800-63-3/sp800-63b.html), updated in 2020.
(See "5.1.1.1 Memorized Secret Authenticators". NIST's guidelines are in terms
of passwords, not passphrases.)

## How do I know I can trust this page?

Getting your password from a website feels a little sketchy. Here are some precautions you can take:

- Save this web page to your own computer then open it up in a browser, and it'll work just as well. This page loads no external resources.
- Load up your local copy of this page in your browser while you're not connected to the internet.

All the javascript that powers this page is inlined into the page, and is not minified -- you can open the page up and audit it yourself. The source materials for this page are [on sourcehut](https://git.sr.ht/~mkelly/passphraser) (and [mirrored to GitHub](https://github.com/mjkelly/passphraser)). You can clone that repository and re-generate the page yourself!

## What else can I do to increase my security online?

The most important thing you can do is **not reuse passwords**. This means use
a unique password for each site, ideally, by using a password
manager.

Here two recommended password managers:
- [1Password](https://1password.com/) (paid)
- [BitWarden](https://bitwarden.com/) (free and paid plans)

References for password manager recommendations:
- [Wirecutter (New York Times), 2023](https://www.nytimes.com/wirecutter/reviews/best-password-managers/)
- [Wired, 2023](https://www.wired.com/story/best-password-managers/)
- [Consumer Reports, 2021](https://www.consumerreports.org/electronics-computers/password-managers/best-password-managers-review-digital-security-privacy-ease-of-use-a7337649384/)

## How do you determine password strength? How do you compare the strength of a password and a passphrase?

_Math alert! You don't need to know this to make use of the rest of this page.
This is here in case you're curious!_

The most principled way of determining password complexity is to assume your attacker knows your password generation scheme. So if you're using a 10-character random password with a specific set of special characters, assume they know that. Now, trick to remaining secure is to make them search as many passwords as possible.

For instance, a 5-character random password made up of only lowercase letters (26 options), has `26 * 26 * 26 * 26 * 26` combinations, because you can use any of 26 different letters in each of 5 places. That's 11,881,376 combinations. That sounds like a lot, but hackers can guess passwords at a very high rate that's always increasing.

Since these numbers of combinations get huge, we usually talk about the log-base-2 (log2) of these numbers. `log2(11,881,376) = 23.5`. (Which means, `2^23.5 = 11,881,376`.) . We call this number _bits of entropy_, so a 5-character random password made up of only lowercase letters has 23.5 bits of entropy. Remember, we're talking about log-base-2, so for every added bit of entropy in a password, an attacker must guess twice as many combinations.

This gives us a way to compare passphrases and passwords. Passphrases are just like passwords, but each word in the passphrase is taken from a word list. If your word list has 5,000 words, and you have a 4-word random passphrase, you have `5,000 * 5,000 * 5,000 * 5,000 = 625,000,000,000,000` combinations. `log2(625,000,000,000,000) = 49.1`, so a random passphrase generated this way has 49.1 bits of entropy.

If you use uppercase and lowercase letters, numbers, and all special symbols, you're choosing from 89 characters. A 8-character random password chosen from those 89 characters has 51.8 bits of entropy, so it's just a little stronger than the passphrase above.
