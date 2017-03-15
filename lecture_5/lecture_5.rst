
Beginning Python Class -- Lecture 5
===================================

Expected Understanding
----------------------

At this point in the class it is very important that you have a good
understanding of the topics in Lecture\_1 and Lecture\_2. The topics
today will build directly on the previous topics such as:

::

    - Basic Data Types
    - Conditionals
    - Loops
    - Functions
    - User Defined Datatypes -- Classes

In this lecture I am going to go over a few common topics that you will
encounter when looking/writing python and I would like you to know what
is happening. These topics will feel more disjointed than in previous
lectures but I hope they will help you understand what is happening when
you encounter them outside of class. Some of these topics might be
difficult to replicate in the lab because of running the code in a web
browser (from my testing at home it seems that everything works in the
web browser).

Running Python in the Lab
~~~~~~~~~~~~~~~~~~~~~~~~~

Not everyone has a dedicated Windows machine that they can remote into,
and not everyone has their own Linux account. Therefore we are going to
use an online Python Interpreter to run our Python code for this class.
This way we can practice in the lab and students can practice at home
without having to install python on their PC. I will run python from my
machine during the lecture so that the process of running python from
the command line is understood.

Here is the link to the online Python Interpreter --
https://repl.it/languages/python3

PEP8 Style Guide
~~~~~~~~~~~~~~~~

PEP8 style guide should be used as a reference for styling decisions.
This document (http://legacy.python.org/dev/peps/pep-0008/) covers
topics like: - Indentation - Comments - Line Length These are a set of
standards that allow Python developers to easily work on each others
code and avoid nasty syntax bugs caused by white space inconsistencies.

Syntax
~~~~~~

Syntax in the context of computer code is the set of rules that defines
the combinations of symbols that are considered to be a correctly
structured document or fragment in that language.

Python was designed to have a very clean look to the code. The
compromise is that to correctly interpret the code Python elected to use
white space as a syntactical character. The last language to use
syntactical white space was Fortran which was created by IBM in 1957.

Languages such as Perl and C ignore white space and rely on other
special characters that often mean different things in different
contexts. This allowed the programmer to develop their own style
independent of the format of the code.

A quick example is shown below:

::

    foreach my $a (@list_of_numbers){
        print "value of a: $a\n";
    }

The exact same Perl code could be written like:

::

    foreach my $a (@list_of_numbers){ print "value of a: $a\n"; }

This is because one of the characters that Perl uses to group
instructions are "{}" (brackets).

Python avoids this type of problem by requiring white space syntax to
group sequences of instruction:

.. code:: python

    for a in list_of_numbers:
        print( "Value of a: " + str(a))

Since the 'print' statement is executed during the loop it is
nested/grouped inside the loop with 4 spaces. (More on loops later in
Lecture 2)

New Topics
==========

Ternary Operator
----------------

The Ternary Operator is an operator that takes 3 arguments. This
operator is often used during the assignment process. Assignment is what
it is called when we take a variable and set it ``=`` to some value. We
have done this many times without putting a name to it.

.. code:: ipython3

    name = 'Dallin' # Assignment
    print(name)
    
    is_big = True
    size = 'Big' if is_big else 'Small'
    print(size)
    
    is_big = False
    size = 'Big' if is_big else 'Small'
    print(size)


.. parsed-literal::

    Dallin
    Big
    Small


In the example above we assign ``name`` equal to the string ``'dallin'``
with regular assingment. A little lower in the code we use the Ternary
Operator to assign ``size`` to either the string ``'Big'`` or
``'Small'`` based on the condition ``is_big``. The Ternary Operator is
short-hand for the code below.

.. code:: ipython3

    is_big = True
    size = ''
    if is_big:
        size = 'Big'
    else:
        size = 'Small'
    print(size)
    
    is_big = False
    size = ''
    if is_big:
        size = 'Big'
    else:
        size = 'Small'
    print(size)


.. parsed-literal::

    Big
    Small


List Comprehension and Range Function
-------------------------------------

List Comprehension is a really handy tool when creating lists of data.
They are very quick and are used all over the place in python code.
Let's jump right in.

The range function is a function that was changed between python2 and
python3. In python2, the ``range`` function returned a ``list``, but in
python3 the ``range`` function returns an iterator. Iterators are
outside the scope of this class but you can read up on them here:
https://www.programiz.com/python-programming/iterator. Therefore, the
proper way to create a ``list`` from a ``range`` is using the ``list()``
function or using the ``list`` comprehension. See the first example
below.

.. code:: ipython3

    x = [y for y in range(100)]
    print(x)


.. parsed-literal::

    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99]


We can selectively add numbers to a ``list`` using the ``if`` in the
comprehension. If the conditional after the ``if`` is ``True`` then the
value is added to the list otherwise it is ignored. See the example
below where we are looking for prime numbers.

.. code:: ipython3

    def is_prime(x):
        if x <=1:
            return False
        for y in range(2,int(x/2)+1):
            if x % y == 0:
                return False
        return True
    
    list_of_primes = [y for y in range(100) if is_prime(y)]
    print(list_of_primes)


.. parsed-literal::

    [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]


We can also pass each value to a function and then add it to the list.
In the example below we are going to find 2 to the ``n``\ th power and
pair it in a tuple with ``n``.

.. code:: ipython3

    z = [(n, 2**n) for n in range(64)]
    print(z)


.. parsed-literal::

    [(0, 1), (1, 2), (2, 4), (3, 8), (4, 16), (5, 32), (6, 64), (7, 128), (8, 256), (9, 512), (10, 1024), (11, 2048), (12, 4096), (13, 8192), (14, 16384), (15, 32768), (16, 65536), (17, 131072), (18, 262144), (19, 524288), (20, 1048576), (21, 2097152), (22, 4194304), (23, 8388608), (24, 16777216), (25, 33554432), (26, 67108864), (27, 134217728), (28, 268435456), (29, 536870912), (30, 1073741824), (31, 2147483648), (32, 4294967296), (33, 8589934592), (34, 17179869184), (35, 34359738368), (36, 68719476736), (37, 137438953472), (38, 274877906944), (39, 549755813888), (40, 1099511627776), (41, 2199023255552), (42, 4398046511104), (43, 8796093022208), (44, 17592186044416), (45, 35184372088832), (46, 70368744177664), (47, 140737488355328), (48, 281474976710656), (49, 562949953421312), (50, 1125899906842624), (51, 2251799813685248), (52, 4503599627370496), (53, 9007199254740992), (54, 18014398509481984), (55, 36028797018963968), (56, 72057594037927936), (57, 144115188075855872), (58, 288230376151711744), (59, 576460752303423488), (60, 1152921504606846976), (61, 2305843009213693952), (62, 4611686018427387904), (63, 9223372036854775808)]


For more information on List Comprehension please see the following
links: -
https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
-
http://python-3-patterns-idioms-test.readthedocs.io/en/latest/Comprehensions.html
- http://www.python-course.eu/python3_list_comprehension.php

Modules
-------

Modules are a collection of Python code that work together. We can
``import`` modules in order to get extra functionality for free. There
are two standard ways of importing libraries. One only uses the
``import`` keywork and the other way also uses the ``from`` keyword.

.. code:: ipython3

    import math
    from random import *
    
    print( math.pi )
    print( randint(1,100) )


.. parsed-literal::

    3.141592653589793
    3


Notice that since we only used the ``import`` command we have to tell
python exactly which library the ``pi`` variable is in by typing
``math.pi``. The ``from`` keyword is used to tell python to ``import``
everything (``*``) in the ``random`` library directly into the current
scope. That is why we can access ``randint`` without typing
``random.randint(1,100)``. We can also ``import`` a specific attribute
from a library so that we only get what we need.

.. code:: ipython3

    from math import pi
    print( pi )


.. parsed-literal::

    3.141592653589793


The last thing that I want to bring up about modules is that you can
write your own. As long as they are files with the ``.py`` extention
then they can be imported.

Files
-----

Often we need to read data from files or store data in files for later.
It is possible to read and write from the same file but in most cases we
do either one or the other. There are many styles for working with files
so I will show a standard method of working with fils. For extra info
about file manipulation use the following link:
https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files.

.. code:: ipython3

    with open( 'temp.txt', 'w' ) as fout:
        fout.write( "Test Output " )
    
    with open( 'temp.txt', 'r' ) as fin:
        print( fin.read() )


.. parsed-literal::

    Test Output 


The ``with`` keyword is used to give us a little extra error handling
protection if the file doesn't open or if the file doesn't exist.

Executing External Shell Commands
---------------------------------

Often we like to use other scripts and other built-in Linux commands in
our scripts. Running external commands can be a little different
depending on the version of Python you are using. The easiest way to
access external commands is to use the ``subprocess`` module.

.. code:: ipython3

    import subprocess
    
    response = subprocess.check_output('pwd', shell=True)
    print( response )
    
    response = subprocess.check_output('ls', shell=True)
    print( response )
    
    response = subprocess.check_output('whoami', shell=True)
    print( response )


.. parsed-literal::

    b'/Users/dallin/projects/python_class/lecture_5\n'
    b'lecture_5.ipynb\ntemp.txt\n'
    b'dallin\n'


Practice Problems
=================

There are a lot of things in Python to practice and many things that I
did not try to show/teach in these 5 lectures. Python/Programming is
something that you will continue to master for years to come. I find
that often the best was to learn a new language is to pick a problem and
start trying to solve it with that language. Along the way you will
learn a lot of the ins and outs of the new language.

Another option is something like CodeWars. CodeWars is a site that has
many practice problems that are posted by other users. After you come up
with a solution your code is tested to see if it gives the correct
output. The really cool thing about CodeWars is that after you complete
a problem you can look at how other people solved the same problem and
learn new little pieces of Python from the other solutions.
https://www.codewars.com

This week for practice please practice anything you would like. Try to
solve a problem that you think up or try to solve some of the practice
problems on CodeWars. Good Luck
