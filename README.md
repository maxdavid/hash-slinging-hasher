Hash Slinging Hasher
====================

### The Evergreen State College: Undefeated in brute-forcing since 1967

A program that brute-forces the [Skein hashing algorithm](http://www.skein-hash.info/) in an attempt to win xkcd's [hash-breaking competition](http://almamater.xkcd.com/) for The Evergreen State College. Made real quick and super sloppy. To be run on the [SLACR](http://github.com/slacr/) cluster, or really any other computer that runs python.

We've currently got evergreen.edu 411 bits off the target hash on the [leaderboards](http://almamater.xkcd.com/best.csv). While good, this is still unnacceptable

Make sure [pyskein](http://pythonhosted.org/pyskein/) is installed (pip install pyskein) and run:
    python3 xkcd-hasher.py <num of hash attempts> <length of input string> <score to beat>


***


#### TODO
* add execnet implementation
* scrape evergreen's current placement from the leaderboard automatically
* notify a successful input (< target score) in a more alertive way
 * (most likely by triggering /usr/local/sbin/epic_cuckoo.sh)
* do I *really* need a TODO? i mean seriously 
