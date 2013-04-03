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
import urllib.request

numtries = 10000000             # default 10 million attempts
randlength = 24                 # length of random word to hash
high_score = 411                # hamdist to beat
target_hash = '5b4da95f5fa08280fc9879df44f418c8f9f12ba424b7757de02bbdfbae0d4c4fdf9317c80cc5fe04c6429073466cf29706b8c25999ddd2f6540d4475cc977b87f4757be023f19b8f4035d7722886b78869826de916a79cf9c94cc79cd4347d24b567aa3e2390a573a373a48a5e676640c79cc70197e1c5e7f902fb53ca1858b6'

# scrape the leaderboard and grab the current highscore for evergreen.edu
def get_target_goal():
  leaderboard = urllib.request.urlopen('http://almamater.xkcd.com/').readlines()
  for line in leaderboard:
    line = line.decode().strip()
    place = line.replace("\"", "").split(",")
    if place[0] == "evergreen.edu":
      return int(place[1])
high_score = get_target_goal()

# sloppy args
# [1] = number of hashes to compute
# [2] = length of the random word to hash
# [3] = record number to beat on http://almamater.xkcd.com/best.csv for evergreen
if (len(sys.argv) > 1):
  numtries = int(sys.argv[1])
if (len(sys.argv) == 3):
  randlength = int(sys.argv[2])
if (len(sys.argv) == 4):
  high_score = int(sys.argv[3])

# get xor of our hash and the target hash
def hash_distance(s1, s2):
  return bin(int(s1,16)^int(s2,16)).zfill(512).count("1")

# get a random string from the pool of ascii letters
def get_random_string(length=24):
  return ''.join(random.choice(string.ascii_letters) for i in range(length))

def get_skein_hash(input_string):
  h = skein1024(digest_bits=1024)
  h.update(input_string.encode('utf-8'))
  return h.hexdigest()

# skein it up! 
def hashify(inputstr=get_random_string()):
  dig = get_skein_hash(inputstr)
  hash_score = hash_distance(dig, target_hash)
  return hash_score

def hash_loop(tries=numtries, target=high_score):
  lowest_found = 0
  randstr = get_random_string(randlength)
  start_time = datetime.now() # ready, set
  print("Started {}".format(start_time))

  for x in range(tries):
    inputstr = randstr + str(x)
    hash_score = hashify(inputstr)
    if (lowest_found == 0):
      lowest_found = hash_score
    else:
      if (hash_score < lowest_found):
        lowest_found = hash_score

    if (hash_score <= target):
      woot(hash_score, inputstr)
  end_time = datetime.now() # voila!
  print("Finished {}".format(end_time))

  total_time = end_time - start_time
  print("\nStarted {0}, Finished at {1}.".format(start_time, end_time))
  print("Computed {0} hashes in {1}. Lowest score achieved was {2}.".format(numtries, total_time, lowest_found))

def woot(hash_score, inputstr):
  print("\n************************   WHOA DOGGY   ****************************")
  print()
  print("{0}".format(datetime.now().strftime("%m/%d/%Y %H:%M")))
  print("Score {0} found! '{1}' yields a beautiful hash of:\n{2}"
      .format(hash_score, inputstr, get_skein_hash(inputstr)))
  print("(input encoded in utf-8: {})".format(inputstr.encode('utf-8')))
  print()
  print("********************************************************************\n")

if __name__ == "__main__":
  hash_loop()
