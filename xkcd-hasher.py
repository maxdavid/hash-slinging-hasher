#!/usr/bin/env python3

# xkcd-hasher.py
# for the motherland!! http://almamater.xkcd.com/
# forked from arthurdent's 1193.py. thx buddy
# 
# usage:  ./xkcd-hasher.py <num hashes> <randword length> <goal number>

from skein import skein1024
from datetime import *
import timeit
import string
import random
import sys

numtries = 10000000  # 10 million
randlength = 24      # length of random word to hash
goalnum = 411        # current evergreen.edu score
target_hash = '5b4da95f5fa08280fc9879df44f418c8f9f12ba424b7757de02bbdfbae0d4c4fdf9317c80cc5fe04c6429073466cf29706b8c25999ddd2f6540d4475cc977b87f4757be023f19b8f4035d7722886b78869826de916a79cf9c94cc79cd4347d24b567aa3e2390a573a373a48a5e676640c79cc70197e1c5e7f902fb53ca1858b6'

# sloppy args
# [1] = number of hashes to compute
# [2] = length of the random word to hash
# [3] = record number to beat on http://almamater.xkcd.com/best.csv for evergreen
if (len(sys.argv) > 1):
  numtries = int(sys.argv[1])
if (len(sys.argv) == 3):
  randlength = int(sys.argv[2])
if (len(sys.argv) == 4):
  goalnum = int(sys.argv[3])

# get xor of our hash and the target hash
def hash_distance(s1, s2):
  return bin(int(s1,16)^int(s2,16)).zfill(512).count("1")

# get a random string from the pool of printable characters
def random_string(length=24):
  return ''.join(random.choice(string.printable) for i in range(length))


# skein it up! 
# not the most optimized hash brute-forcer (it makes a new random word *each time*) 
# but hey whatever
def hashify(target=goalnum,wordlength=randlength):
  h = skein1024(digest_bits=1024)
  h.update((random_string(wordlength).encode('utf-8')))
  dig = h.hexdigest()
  hash_score = hash_distance(dig, target_hash)
  if (hash_score <= target):
    print("************************   WHOA DOGGY   ****************************")
    print()
    print("Score {0} found! '{1}' yields a beautiful hash of:\n{2}"
        .format(hash_score, randstr, dig))
    print()
    print("********************************************************************")
  return hash_score

# loops hashify, using the timeit module to benchmark the execution time
def bench_hash(tries=numtries, target=goalnum):
  start_time = datetime.now()
  print("Started {}".format(start_time))

  total_time = timeit.timeit("hashify()", setup="from __main__ import hashify", number=tries)
  
  end_time = datetime.now() # voila!
  print("Finished {}".format(end_time))

  print("\nStarted {0}, Finished at {1}.".format(start_time, end_time))
  print("Computed {0} hashes in {1} seconds.".format(numtries, total_time))


"""
# This works fine, but abandoned for hashify and bench_hash instead. 
# Kept for posterity (and lack of using git)

def hash_loop(tries=numtries, target=goalnum):
  lowest_found = 0
  start_time = datetime.now() # ready, set

  for x in range(tries):
    h = skein1024(digest_bits=1024)
    h.update((randstr + str(x)).encode('utf-8'))
    dig = h.hexdigest()
    print(dig)
    hash_score = hash_distance(dig, target_hash)
    if (lowest_found == 0):
      lowest_found = hash_score
    else:
      if (hash_score < lowest_found):
        lowest_found = hash_score

    if (hash_score <= target):
      print("************************   WHOA DOGGY   ***************************")
      print()
      print("Score {0} found! '{1}' yields a beautiful hash of:\n{2}"
          .format(hash_score, randstr + str(x), dig))
      print()
      print("***********************************************************************")

  end_time = datetime.now() # voila!
  total_time = end_time - start_time
  print("\nComputed {0} hashes in {1}. Lowest score achieved was {2}.".format(numtries, total_time, lowest_found))
"""

if __name__ == "__main__":
  bench_hash()
