#!/usr/bin/python

# "Fizzbuzz" Algorithms - Thanks to Tom Scott
# https://www.youtube.com/watch?v=QPZ0pIK_wsc
# for laying down the gauntlet and issuing the challenge.
#
# 200425 Karim Sultan - Created this module
# This module shows off Python 3.7's powerful OOP capabilities.
#
# Fizzbuzz rules:
# Output, from 1 to 100 (configurable via command line):
# if x divisible by 15: Fizzbuzz
# else if x divisible by 5: Buzz
# else if x divisible by 3: Fizz
# else: X
#
# This module explores a colletion of algorithmic approaches, times them,
# and ranks them.
# To increase the Fizzbuzz range from the default 100, alter "MAX_NUMBERS" global,
# or pass in a number on the command line:
#
# FizzBuzz.py --max=200
# FizzBuzz.py -m 200
#
# Example of using only Racers algorithm, quiet mode, range of 15000:
#
# FizzBuzz.py -a racers -v false -m 15000
# FizzBuzz.py --algo=racers --verbose=false --max=15000


from time import perf_counter
import sys
import getopt

# Global constants, can be modified by command line parameter
MAX_NUMBERS     = 100
VERBOSE         = True
ALGO_REQUESTED  = "*"
RECURSION_LIMIT = 10000

# Small timer class to handle performance timing
class Timer():
   timeStart = timeStop = timElapsed = 0
   running = False

   def __init__(self):
      self.timeStart=0
      self.timeStop=0
      self.timeElapsed=0
      self.running=False

   def start(self):
      self.running=True
      self.timeStart=perf_counter()

   def stop(self):
      self.timeStop=perf_counter()
      self.running=False

   def elapsed(self):
      if (self.timeStop<self.timeStart):
         self.timeElapsed = perf_counter() - self.timeStart
      else:
         self.timeElapsed = self.timeStop - self.timeStart
      return (self.timeElapsed)

   def isRunning(self):
      return(self.running)
#End of class
###########################################################################

# Base class, will be inherited by different algorithms
# As python doesn't formally  support interfaces, this class
# also has an algorithm implementation.  It is "Basic" and
# just implements the rules as per above, directly.
# This basic implementation is consistently middle of the rankings.
class FizzBuzz:
   # Class attributes
   Max = 100         # Number of items to FizzBuzz
   Name = ""         # Algorithm name
   results=[0]       # Results stored here
   timer = Timer()   # A timer object for high performance timing

   # The base constructor should be calle be all derived classes.
   # IE, "super().__init__("Name of Algorithm")
   def __init__(self, name="Approach 0. Basic - FizzBuzz"):
      # Start performance timer
      self.timer.start()
      self.Name = name
      self.results=[0]
      self.Max = MAX_NUMBERS

   # Returns the name of the class.
   # Used in automation / templating in main().
   # User self.name for the algorithm name.
   def myName(self):
      return (type(self).__name__)

   # Base class wasn't going to have a base implementation,
   # but since Python doesn't have formal support for interfaces,
   # it's best to show an implementation that derived classes
   # can override with their own.
   def doFizzBuzz(self):
      for i in range(1,self.Max+1):
         if (i%15==0):
            self.results.append("FizzBuzz")
         elif (i%5==0):
            self.results.append("Buzz")
         elif (i%3==0):
            self.results.append("Fizz")
         else:
            self.results.append(i)

   # Reports output, stops timing, and returns elapsed time
   # As some algorithms have different output requirements,
   # accepts a formatted output string, optionally.
   # We don't time the CRT output portion.
   def report(self, dataString=""):
      self.timer.stop()

      # If we are in quiet mode, abort report and return time
      if (VERBOSE==False):
         return(self.timer.elapsed())

      # We are in verbose mode.  Show output.
      print("--> " + self.Name)

      if (dataString == ""):
         for i in range (1, len(self.results)):
            print ("[{0}] {1}".format(i, self.results[i]))
      else:
         print (dataString)

      # Report timing...
      return(self.timer.elapsed())

#End of class
###########################################################################
# Approach 1: Sieve of Eratosthenes
# A play on the famous prime number algorithm.  We start with all the
# numbers up to Max, and remove multiples of 3 (Fizz), 5 (Buzz) and
# 15 (FizzBuzz).  A very fast and simple algorithm
class Sieve(FizzBuzz):
   def __init__(self):
      super().__init__("Approach 1: Sieve of Eratosthenes")

   def doFizzBuzz(self):
      self.results = [i for i in range(self.Max+1)]

      # For each multiple, step and tag
      for i in range(0, len(self.results), 3):
         self.results[i]="Fizz"

      for i in range(0, len(self.results), 5):
         self.results[i]="Buzz"

      for i in range(0, len(self.results), 15):
         self.results[i]="FizzBuzz"

#End of class
###########################################################################
# Approach 2: Minefield
# A fun way of looking at the problem, not optimal but surprisingly fast
# for large sets.  Creates a "minefield" of special characters ("*") at
# values of multiple of 3, 5, 15. Does not distinguish between multiples.
# Post mining, uses a reduction function to swap out * values with Fizz,
# Buzz, or FizzBuzz.
class Minefield(FizzBuzz):
   def __init__(self):
      super().__init__("Approach 2: Minefield")

   def doFizzBuzz(self):
      self.results = [i for i in range(self.Max+1)]
      for i in range (1, self.Max+1):
         if (i%15==0 or i%5==0 or i%3==0):
            self.results[i]="*"
      self.reduction()

   # Reduction function
   def reduction(self):
      for i in range(1,len(self.results)):
         if self.results[i]=="*":
            if i%15==0: self.results[i]="Fizzbuzz"
            elif i%5==0: self.results[i]="Buzz"
            elif i%3==0: self.results[i]="Fizz"

#End of class
###########################################################################
# Approach #3: Dictionary
# A solid performer which indexes the numbers up to Max. Then it replaces
# values of multiples with the Fizzbuzz words, as values for their numeric key.
class Dictionary(FizzBuzz):
   dic = {}

   def __init__(self):
      super().__init__("Approach #3: Dictionary")

   def doFizzBuzz(self):
      self.dic = {0:0}

      # Init / Build dictionary
      for i in range (1, self.Max+1):
         self.dic[i]=i

      # Note: must build upwards by factor
      for i in range(0, len(self.dic), 3):
         self.dic[i]="Fizz"
      for i in range(0, len(self.dic), 5):
         self.dic[i]="Buzz"
      for i in range(0, len(self.dic), 15):
         self.dic[i]="FizzBuzz"
      self.reduction()

   # Reduction function
   def reduction(self):
      for i in range(1, len(self.dic)):
         self.results.append(self.dic[i])

#End of class
###########################################################################
# Approach #4: Lambda
# Uses lambda expressions to determine an index (3, 5, or -1). That needs
# some clarification.  A) Lambdas can't have logic / conditions in them.
# So, I use a trick to do ternary operations in Python:
# (Tuple 0, 1)[index]
# Where a calculation reduces to a valid index and returns a tuple member
# value. This value is a 3(Fizz), 5(Buzz), or -1 (FizzBuzz) pulled from a
# dictionary.  Note that we must use -1 instead of 15 for unique recognition.
# This is an intellectually challenging algorithm; unfortunately,it is a
# regular bottom-of-the-pack performer.
# Lambda: Not just complex obfuscation, but poor performance as well.
class Lambda(FizzBuzz):
   def __init__(self):
      super().__init__("Approach #4: Lambdas")

   # Note we use -1 for 15 as it doesn't share factors 3,5 and is numeric
   def doFizzBuzz(self):
      mod3 = lambda x:  (x, 3)[min(x%3==0,1)]
      mod5 = lambda x:  (x, 5)[min(x%5==0,1)]
      mod15 = lambda x: (x, -1)[min(x%15==0,1)]

      for i in range (1, self.Max+1):
         self.results.append(mod3(mod5(mod15(i))))
      self.reduction()

   # Reduction function
   def reduction(self):
      flip = {3: "Fizz",
              5: "Buzz",
             -1: "FizzBuzz"}
      for i in range (1, len(self.results)):
         if (self.results[i] in (3, 5, -1)):
            self.results[i] = flip[self.results[i]]
         else:
            self.results[i] = i

#End of class
###########################################################################
# Approach #5: Recursive
# Recursively builds the list.  Since Python has a recursion limit, we
# need to set it to Max + a small safety margin, but only set it if we need
# to so we don't uneccessarily reduce it.
# However in testing I noted that there was a limit of 11387 for the value.
# This is dependent on the machine it is executed on, probably a memory issue.
# I have blanket restricted it to 10,000; if higher, it returns a bogus high time.
class Recursive(FizzBuzz):
   def __init__(self):
      # Adjust recursion limit or it will go poof (+10 is safety margin)
      # (but must be under recusion max limit).
      # Also, must use MAX_NUMBERS instead of self.max as it isn't set until
      # the super is called.
      if (MAX_NUMBERS >= sys.getrecursionlimit()):
         if (MAX_NUMBERS<=RECURSION_LIMIT):
            sys.setrecursionlimit(MAX_NUMBERS+10)
      super().__init__("Approach #5: Recursion")

   def doFizzBuzz(self):
      if (MAX_NUMBERS<=RECURSION_LIMIT):
         self.doRecursion(1)

   def doRecursion(self, i=0):
      if (i>=self.Max+1):
         return
      if (i%15==0):
         self.results.append("FizzBuzz")
      elif (i%5==0):
         self.results.append("Buzz")
      elif (i%3==0):
         self.results.append("Fizz")
      else:
         self.results.append(i)
      self.doRecursion(i+1)

   def report(self, dataString=""):
      if (MAX_NUMBERS>RECURSION_LIMIT):
         print ("Recursion limit of 10,000 exceeded for Recursive algorithm.")
         print ("Test run aborted, and bogus high-time returned.")
         return(999.999999);
      else:
         super().report("")
         return (self.timer.elapsed())

#End of class
###########################################################################
# Approach #6: Nested
# This approach is the anti-thesis to recursion, using nested method calls.
# Surprisingly slow compared to the others.  Often fails to outrank
# Recursion algorithm.
class Nested(FizzBuzz):
   def __init__(self):
      super().__init__("Approach #6: Nested")

   def nested_mod(self, x, mod, label):
      if not type(x) == str:
         if (x%mod==0):
            return(label)
      return(x)

   def doFizzBuzz(self):
      for i in range (1, self.Max+1):
         self.results.append(self.nested_mod(
            self.nested_mod(
               self.nested_mod(i, 15, "FizzBuzz"), 5, "Buzz"), 3, "Fizz"))

#End of class
###########################################################################
# Approach #7: Unrolled
# As an old 6502 programmer, I can attest to the value of unrolling code.
# Long, verbose, not truly dynamic but very fast. Regularly hits number 1
# in the rankings. To handle the Max value being altered, this is only
# unrolled to 100, and only handled in chunks of 100 up to Max. IE, 300 will
# be handled perfectly while 301 will be handled to 400.
# In a compiled language, the point of unrolling code is to ensure the CPU
# has enough instructions to process without stalling. So for example, a
# large loop might unroll 8 iterations at once, with the compiler knowing
# that the CPU would waste cycles if it looped after doing less than 8 ops.
# But Python isn't compiled. So why then does this algorithm perform so
# well?  To understand that, I'll have to peek under the hood of Python 3.
# But this is neither the time nor the place.
class Unrolled(FizzBuzz):
   def __init__(self):
      super().__init__("Approach #7: Unrolled")

   # Unrolled to 100.  BUT what if Max is changed?
   # We will assume Max is in multiples of 100.
   def doFizzBuzz(self):
      limit = max(self.Max, 100)
      base = 0;
      while (base<max(self.Max, 100)):
         self.results.append(base+1)
         self.results.append(base+2)
         self.results.append("Fizz")
         self.results.append(base+4)
         self.results.append("Buzz")
         self.results.append("Fizz")
         self.results.append(base+7)
         self.results.append(base+8)
         self.results.append("Fizz")
         self.results.append("Buzz")
         self.results.append(base+11)
         self.results.append("Fizz")
         self.results.append(base+13)
         self.results.append(base+14)
         self.results.append("FizzBuzz")
         self.results.append(base+16)
         self.results.append(base+17)
         self.results.append("Fizz")
         self.results.append(base+19)
         self.results.append("Buzz")
         self.results.append("Fizz")
         self.results.append(base+22)
         self.results.append(base+23)
         self.results.append("Fizz")
         self.results.append("Buzz")
         self.results.append(base+26)
         self.results.append("Fizz")
         self.results.append(base+28)
         self.results.append(base+29)
         self.results.append("FizzBuzz")
         self.results.append(base+31)
         self.results.append(base+32)
         self.results.append("Fizz")
         self.results.append(base+34)
         self.results.append("Buzz")
         self.results.append("Fizz")
         self.results.append(base+37)
         self.results.append(base+38)
         self.results.append("Fizz")
         self.results.append("Buzz")
         self.results.append(base+41)
         self.results.append("Fizz")
         self.results.append(base+43)
         self.results.append(base+44)
         self.results.append("FizzBuzz")
         self.results.append(base+46)
         self.results.append(base+47)
         self.results.append("Fizz")
         self.results.append(base+49)
         self.results.append("Buzz")
         self.results.append("Fizz")
         self.results.append(base+52)
         self.results.append(base+53)
         self.results.append("Fizz")
         self.results.append("Buzz")
         self.results.append(base+56)
         self.results.append("Fizz")
         self.results.append(base+58)
         self.results.append(base+59)
         self.results.append("FizzBuzz")
         self.results.append(base+61)
         self.results.append(base+62)
         self.results.append("Fizz")
         self.results.append(base+64)
         self.results.append("Buzz")
         self.results.append("Fizz")
         self.results.append(base+67)
         self.results.append(base+68)
         self.results.append("Fizz")
         self.results.append("Buzz")
         self.results.append(base+71)
         self.results.append("Fizz")
         self.results.append(base+73)
         self.results.append(base+74)
         self.results.append("FizzBuzz")
         self.results.append(base+76)
         self.results.append(base+77)
         self.results.append("Fizz")
         self.results.append(base+79)
         self.results.append("Buzz")
         self.results.append("Fizz")
         self.results.append(base+82)
         self.results.append(base+83)
         self.results.append("Fizz")
         self.results.append("Buzz")
         self.results.append(base+86)
         self.results.append("Fizz")
         self.results.append(base+88)
         self.results.append(base+89)
         self.results.append("FizzBuzz")
         self.results.append(base+91)
         self.results.append(base+92)
         self.results.append("Fizz")
         self.results.append(base+94)
         self.results.append("Buzz")
         self.results.append("Fizz")
         self.results.append(base+97)
         self.results.append(base+98)
         self.results.append("Fizz")
         self.results.append("Buzz")
         base+=100

#End of class
###########################################################################
# Approach #8: Racers
# This one is my favourite, and often near the top of the rankings.
# Two racers are on the numberline. One moves 3 spaces at a time, the other
# moves 5. BUT a racer can only move if its location is less than or equal
# to the other one.  Racer3 is Fizz, Racer5 is Buzz, and if there values
# are the same, then it is FizzBuzz.  This one excels for large Max values.
class Racers(FizzBuzz):
   def __init__(self):
      super().__init__("Approach #8: Racers")

   def doFizzBuzz(self):
      self.results = [i for i in range(self.Max+1)]

      racer3=3
      racer5=5
      while (racer3 <= self.Max) and (racer5 <= self.Max):
         if (racer3!=racer5):
            self.results[racer3]="Fizz"
            self.results[racer5]="Buzz"
         else:
            self.results[racer3]="FizzBuzz"

         if (racer3<racer5):
            racer3+=3
         elif (racer5<racer3):
            racer5+=5
         else:
            #They are equal, advance both
            racer3+=3
            racer5+=5

#End of class
###########################################################################
# Approach #9: Pattern
# FizzBuzz creates a repeating pattern every 15 numbers:
# .,.,F,.,B,F,.,.,F,B,.,F,.,.,FB
# This approach just stamps the pattern repeatedly.
# So far, this is usually the fastest algorithm.
class Pattern(FizzBuzz):
   def __init__(self):
      super().__init__("Approach #9: Pattern")

   def doFizzBuzz(self):
      pattern = {1: 1,
                 2: 2,
                 3: "Fizz",
                 4: 4,
                 5: "Buzz",
                 6: "Fizz",
                 7: 7,
                 8: 8,
                 9: "Fizz",
                 10: "Buzz",
                 11: 11,
                 12: "Fizz",
                 13: 13,
                 14: 14,
                 15: "FizzBuzz" }

      i=1
      count=0
      while (count<self.Max):
         temp=pattern[i]
         if (temp in [1, 2, 4, 7, 8, 11, 13, 14]):
            temp=count+1
         self.results.append(temp)
         i+=1
         if (i>15): i=1
         count+=1

#End of class
###########################################################################
def showHelp():
   print ("FizzBuzz v1.0 May 2020 Karim Sultan (karimsultan@hotmail.com)")
   print ()
   print ("Syntax: python3 fizzbuzz.py --max=number [--algo=name] [--verbose=[true|false]] [--help]")
   print ()
   print ("Where:")
   print ("-h,    --help: This help screen")
   print ("-m,     --max: # -> Amount of numbers to FizzBuzz, default is 100. IE, --max=200")
   print ("-a,    --algo: name -> The name of a specific algorithm to test.  IE, --algo=Racers")
   print ("-v, --verbose: true | false -> show output.  Default is true.  IE, --verbose=false")
   print ()
   exit(0)


def parseCommandLine():
   argc = len(sys.argv)
   try:
      opts, args = getopt.getopt(sys.argv[1:], "?hm:v:a:", ["max=","help","algo=","verbose="])
   except getopt.GetoptError as e:
      print("Arguments error:",e.msg,e.opt)
      showHelp()

   # Parse command line options
   for opt, arg in opts:
      if (opt in ("-?", "-h", "--help")):
         showHelp()

      if (opt in ("-m", "--max")):
         global MAX_NUMBERS
         x=int(arg)
         MAX_NUMBERS = max(x,100)

      if (opt in ("-v", "--verbose")):
         global VERBOSE
         if (arg.lower()=="false"):
            VERBOSE = False
         else:
            VERBOSE = True

      if (opt in ("-a", "--algo")):
         global ALGO_REQUESTED
         arg=arg.capitalize()
         ALGO_REQUESTED=arg




def displayTimings(timings):
   # Print ranked timings
   print()
   print ("Ranked Timings:")
   i=0
   for (k,v) in sorted(timings.items(), key=lambda kv:(kv[1],kv[0])):
      i+=1
      print("   {0:3}. {1:15}  @  {2:<10.6f} seconds".format(i, k, v))
   print()


def main():
   # Variables
   algos = ["FizzBuzz",
            "Sieve",    "Minefield",   "Dictionary",
            "Lambda",   "Recursive",   "Nested",
            "Unrolled", "Racers",      "Pattern"]
   timings=dict()

   parseCommandLine()

   # Test for selected algorithm from user
   if (ALGO_REQUESTED!="*"):
      if (ALGO_REQUESTED not in algos):
        print ("The requested algorithm,",ALGO_REQUESTED,", could not be found.")
        print ("Valid choices are:",algos)
        exit(0)

   print("Using a maximum number range of:", MAX_NUMBERS)

   # Use a cool trick to load class by name from list
   # Execute fizzbuzz, report, and track time taken.
   # The generic logic / method calls works well as
   # each algorithm is a sublass of the FizzBuzz class
   if (ALGO_REQUESTED=="*"):
      for algo in range(len(algos)):
         klass = globals()[algos[algo]]
         fizzy=klass()
         fizzy.doFizzBuzz()
         timings[fizzy.myName()]=fizzy.report()
   else:
      klass = globals()[ALGO_REQUESTED]
      fizzy=klass()
      fizzy.doFizzBuzz()
      timings[fizzy.myName()]=fizzy.report()

   # Report
   displayTimings(timings)

# end of Main

# Run the program
main()



