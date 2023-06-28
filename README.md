# ChocoPyCompiler
Python implementation of a two-pass Compiler which receive a source code in order to process it and recognize if a language is a legal or illegal one accordingly to ChocoPy's gramnmar.

<img src="https://user-images.githubusercontent.com/63054183/231643361-4fe1ec27-292c-4ff3-88ba-a863f26eb03b.png" width=20/>

First of all, we are going to understand the structure of our projects, starting with the directories. In our [/lib](https://github.com/alexjr2001/ChocoPyCompiler/tree/main/lib) directory we have all the dictionaries ([dictionary.py](https://github.com/alexjr2001/ChocoPyCompiler/blob/main/lib/dictionary.py)), the grammar of the ChocoPy Language ([grammar.py](https://github.com/alexjr2001/ChocoPyCompiler/blob/feature/lib/grammar.py)) and the follows of every non-terminal ([follows.py](https://github.com/alexjr2001/ChocoPyCompiler/blob/feature/lib/follows.py)), [/src](https://github.com/alexjr2001/ChocoPyCompiler/tree/main/src) contains all the source code of the project divided for the components of a typical compiler and finally, we have [/test](https://github.com/alexjr2001/ChocoPyCompiler/tree/main/test) where we stored all the quirkies programs to identify some errors and verify if the program can accept even the most unlikely situations. Furthermore, we see two loose documents the known [README.md](https://github.com/alexjr2001/ChocoPyCompiler/blob/main/README.md) (I mean, here I am!) and the [setup.py](https://github.com/alexjr2001/ChocoPyCompiler/blob/main/setup.py) with the main information.


### Install libraries 

Install it like this if you haven't before. The library "sys" is usually a built-in library in python.

```
$ pip install pyfiglet
$ pip install anytree
```
We need graphviz as well, you can download it from [here](https://graphviz.org/download/). Don't forget to add it to the PATH.

## Compiler Structure

### - Scanner or Tokenizer
Our scanner is going to receive help from a class called [chocoToken](https://github.com/alexjr2001/ChocoPyCompiler/blob/main/src/chocoToken.py) in order to get an organize and comprehensible code. This simple class will store the information of a token and it will print it out when it will be required. In the other hand, our class Scanner will open foremost a file and then it's going to start the scanning applying the 'getTokens' function. Therefore, it'll grab token (or word) by token and a process of conditionals sentences will start to find if it belongs to any type and if so will print it out with its respective name and type, otherwise, it is going to be an error with a simple specification.

<p align="center"><img width="421" alt="image" src="https://user-images.githubusercontent.com/63054183/231651433-087784c7-e2ab-4751-9193-f9b840c055d6.png"></p>

Everything is achieved largely by two useful functions such as get_char() and peek_char(), the first one is going to move 'the pointer' to the next char and the second one is going to say what is in the next char without moving 'the pointer'. Besides we have jump_line().

### - Parser
This parser is recursive-descendent. After we pass our code through our scanner, we need to know if the code belongs to the grammar or not. That's why we have created the [Parser](https://github.com/alexjr2001/ChocoPyCompiler/blob/feature/src/RDparser.py). It is going to be link to the Scanner's output, where it says the line, type and name of the token found. It is possible because we pass in the Parser's constructor an argument which is a list of the identified object tokens. So to start, all the non-terminal terms in the grammar rules are going to be a function and the terminal ones will be an if statement to check whether it is correct or not. In case, we return to the first function "Program" without errors, the code is going to be accepted. Otherwise, during the path of calling functions we are going to make use of errorManage() function which will skip the characters till the next NEWLINE in order to continue our parsing.
Besides these functions, we got renderTree() that is for drawing the parsing tree and generate to files in the [/visual](https://github.com/alexjr2001/ChocoPyCompiler/tree/feature/visual) directory (an [image](https://github.com/alexjr2001/ChocoPyCompiler/blob/feature/visual/TreeImgExample.png) and a [dot file](https://github.com/alexjr2001/ChocoPyCompiler/blob/feature/visual/TreeDotExample.txt) converted to .txt), peekToken() to see the next token without jumping, getToken() to jump to the next token, check_term() before jumping verifies if it is the expected term and also verifyFollows() in case the current non-terminal token is empty and we got to verify if the next one is possible. 

In the following images, we see how the scanner is printed out with no errors and generates two files of visual representation of the parsing tree which is an abstract syntax tree (AST)
<p align="center"><img width="602" alt="image" src="https://github.com/alexjr2001/ChocoPyCompiler/assets/63054183/cd5e09b9-e85a-492f-96ec-bb4d8cd99b25"></p>
<p align="center"><img width="138" alt="image" src="https://github.com/alexjr2001/ChocoPyCompiler/assets/63054183/eef43fa5-7ace-49c4-962e-b37d4f1372c7"></p>
<p align="center"><img width="922" alt="image" src="https://github.com/alexjr2001/ChocoPyCompiler/assets/63054183/49aa9594-0270-4b49-810d-5aa2961043b2"></p>






### Running the project

After being in the right location [/src](https://github.com/alexjr2001/ChocoPyCompiler/tree/main/src) in cmd and enter the program we want to compile in the [main.py](https://github.com/alexjr2001/ChocoPyCompiler/blob/main/src/main.py), we run it with this command:

```
$ python main.py
```

