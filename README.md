# ChocoPyCompiler
Python implementation of a two-pass Compiler which receive a source code in order to process it and recognize if a language is a legal or illegal one accordingly to ChocoPy's gramnmar.

<img src="https://user-images.githubusercontent.com/63054183/231643361-4fe1ec27-292c-4ff3-88ba-a863f26eb03b.png" width=20/>

First of all, we are going to understand the structure of our projects, starting with the directories. In our [/lib](https://github.com/alexjr2001/ChocoPyCompiler/tree/main/lib) directory we have all the dictionaries ([dictionary.py](https://github.com/alexjr2001/ChocoPyCompiler/blob/main/lib/dictionary.py)) and the grammar of the ChocoPy Language, [/src](https://github.com/alexjr2001/ChocoPyCompiler/tree/main/src) contains all the source code of the project divided for the components of a typical compiler and finally, we have [/test](https://github.com/alexjr2001/ChocoPyCompiler/tree/main/test) where we stored all the quirkies programs to identify some errors and verify if the program can accept even the most unlikely situations. Furthermore, we see two loose documents the known [README.md](https://github.com/alexjr2001/ChocoPyCompiler/blob/main/README.md) (I mean, here I am!) and the [setup.py](https://github.com/alexjr2001/ChocoPyCompiler/blob/main/setup.py) with the main information.


### Install libraries 

Install it like this if you haven't before. The library "sys" is usually a built-in library in python.

```
$ pip install pyfiglet
```

## Compiler Structure

### - Scanner or Tokenizer
Our scanner is going to receive help from a class called [chocoToken](https://github.com/alexjr2001/ChocoPyCompiler/blob/main/src/chocoToken.py) in order to get an organize and comprehensible code. This simple class will store the information of a token and it will print it out when it will be required. In the other hand, our class Scanner will open foremost a file and then it's going to start the scanning applying the 'getTokens' function. Therefore, it'll grab token (or word) by token and a process of conditionals sentences will start to find if it belongs to any type and if so will print it out with its respective name and type, otherwise, it is going to be an error with a simple specification.

<p align="center"><img width="421" alt="image" src="https://user-images.githubusercontent.com/63054183/231651433-087784c7-e2ab-4751-9193-f9b840c055d6.png"></p>

Everything is achieved largely by two useful functions such as get_char() and peek_char(), the first one is going to move 'the pointer' to the next char and the second one is going to say what is in the next char without moving 'the pointer'. Besides we have jump_line().


### Running the project

After being in the right location [/src](https://github.com/alexjr2001/ChocoPyCompiler/tree/main/src) in cmd and enter the program we want to compile in the [main.py](https://github.com/alexjr2001/ChocoPyCompiler/blob/main/src/main.py), we run it with this command:

```
$ python main.py
```

