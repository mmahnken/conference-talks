==========================
Cryptography for Engineers
==========================

Introduction
============

case study-- tale of war secret

public key encryption
- diffie hellman key exchange
- was classified information by british govt

goals of this talk
- learn the basics of one time pads and public key encrpyption


What is cryptography?
---------------------

secrets
hiding something in plainview
passing messages from one trusted party to another

Early Cryptography
==================

innovative methods of hiding messages
hide it javelin, on someone's head(shave to read)
message travels in the clear-- but someone has to know how to read

Keys
----

encrypted message travels-- if enemy finds it, it means nothing without the key
key could be a literal lock/key
or a means of translating the original message to the plaintext-- un-encrypted

Key Examples
------------

"Skip every 5th letter"

"Skip 5 letters [take letter] 
 4 letters [take letter]
 3 letters [take letter] 
 ... start over at 1"

Caesar Cypher
-------------

Key is BIRD

A B C D E F G H I J  K  L  M  N  O  P  Q  R  S  T  U  V  W  X  Y  Z
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26

B = 2
I = 9
R = 18
D = 4

Message to encrypt:
attack at dawn

   a  t  t  a  c  k  a  t  d  a  w  n
+  B  I  R  D  B  I  R  D  B  I  R  D 
-------------------------------------
   C  C  L  E  E  T  [Fill in the rest!]


One Time Pads
-------------

- Key is random, and as long as the message
- Difficult to crack, but eventually, cracked

Symetric Cryptography
---------------------

Sender (encrypter) and receiver MUST have the key

[insert pretty picture of symmtrical key relationship]

AES
---



Asymetric crypto
----------------

Key never travels in the clear
Murmurings about this in 1800s

Public Key Cryptography
=======================

The Beauty of Public Key Cryptography
-------------------------------------

- I can send a secret message that only one person can read.
- Someone can send me a message that only I can read.

- I can send a message that anyone could read, but is provably sent by me.
- Someone can send a message that anyone could read, but is provably sent by them.

[Key Never Needs to be Transferred or Communicated]

How?
----

Public and Private Keys

Something encrypted with a public key can ONLY be decrypted with the Private Key

Something encryted with a private key can ONLY be decrypted with Public Key



