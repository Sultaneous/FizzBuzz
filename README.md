## FizzBuzz Python Script
This tool is a simple FizzBuzz algorithm tester, by Karim Sultan (May 2020). 
Wait, what is FizzBuzz you ask?  It's simple:

### Fizzbuzz rules:
Output, from 1 to 100 (configurable via command line): 
<br>
<br>if x divisible by 15: Fizzbuzz
<br>else if x divisible by 5: Buzz
<br>else if x divisible by 3: Fizz
<br>else: output X

The purpose is to spur critical thought and to try to resolve a problem with simple rules in
the most efficient manner.  I came across this interesting challenge thanks to Tom Scott's
Youtube video:

 https://www.youtube.com/watch?v=QPZ0pIK_wsc (Well worth watching).

## Command Line Syntax
You can execute the script (Python 3.7+) from any command line with:
<br>`Python FizzBuzz.py`

This will run it in verbose mode for a range of 1-100, for each algorithm and then compare
and rank their times.

The value of 100 is in line with Tom's video, but this can be changed (see below).
Note if running under Linux, you can issue:
<br>`chmod 644 FizzBuzz.py`
and then execute it directly as:
<br>`./FizzBuzz.py`

To get a list of the possible command line arguments, use **--help**

To run an exhaustive test with range 1..100,000, without results cluttering
the output, use:
<br>`Python FizzBuzz.py -m 100000 -v false` OR
<br>`Python FizzBuzz.py --max=100000 --verbose=false`

You can test just a single algorithm with **--algo** or **-a**
<br>`Python FizzBuzz.py -m 150000 -a Racers -v false`

Please note that the Recursive algorithm has a maximum recursion limit after which it will not run and will return a bogus high-time to go 
to the bottom of the rankings.

## Code Structure
Ok, so I'm watching Tom's video, and my mind starts racing with different approaches.  But I
wanted it to be elegant, not just a bunch of repeated code in a massive file.  Fortunately,
Python now has some great object oriented features, and they are leveraged here.

There is a base class `FizzBuzz` which implements the standard, basic algorithm.  It provides core code 
(register algorithm name, start the timer, report the output, return the elapsed time).

Now the fun begins; subsequent algorithms just inherit from this base class, and only
re-implement the algorithm execution. The timing and reporting comes for free. Next, to make
testing easier, a list of class names (matching the algorithms) is maintained in `main()`.
Using a nifty feature of Python, each string in this list is used to invoke the class it
represents, and the algorithm is executed.  This makes adding new algorithms a plug'n'play
approach (and also allows for specifying a specific algorithm from the command line.

## Algorithms
There are 10 that I implemented:
1. **FizzBuzz** (default / base class)
2. **Sieve**  (modeled after the famous Sieve of Eratosthenes for primes)
3. **Minefield** (A character search and replace)
4. **Dictionary**
5. **Lambda** (Uses nested Lambda expressions / similar to inline macros)
6. **Recursion** (Limited by Python's recursion limit)
7.  **Nested** (An anti-recursion approach)
8. **Unrolled** (An old-school approach to loop  optimization)
9. **Pattern** (FizzBuzz has a repeating pattern every 15 numbers)
10.**Racers** (my favourite; two "cars" racing on a number line)

I did not implement any *threaded* approaches, as Python does not offer a true multi-core
threading model that is easily accessed.

Which is fastest?  It depends on the iterations.
Try running with 1,000,000:
<br>`Pyton FizzBuzz.py -m 1000000 -v false` 
<br>(be sure to set `-v false`) and you'll get a fair distribution of results.

## Extending the Algorithms
The sky is the limit!  Why not try your own approach and see how it stacks up against the stock ones?  Extending `FizzBuzz.py` is simple:
1. Create a new class with the algorithm as the name, inheriting from FizzBuzz.  This example, we will use "NewAlgo" as the name:
<br>`class NewAlgo(FizzBuzz):`
2. Next, override `__init__` and register the name, as follows (arrow indicates indent):
<br> `def __init__(self):`
<br>`-->super().__init__("Approach #10: New Algorithm")`
3. Override `doFizzBuzz(self)` with your implementation
4. Finally, in `main()`, find the `algos`array and add `"NewAlgo"`as a member to it.

## Why did I do this?
For the love of  the game.  For which Tom's video re-sparked.  I'm a middle-aged programmer who wrote code as a kid on Commodore 64s - and it was *fun*.   Then you make it your career and it becomes anything but.  So, thank you Tom Scott for re-igniting the spark.
