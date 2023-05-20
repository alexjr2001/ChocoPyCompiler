import chocoToken
import pyfiglet
import sys
sys.path.append('../')
from lib import dictionary as dic

class Scanner:
    def __init__(self) -> None:
        self.cur_char = ""
        self.cur_word = ""
        self.idx_line = 0
        self.idx_char = 0
        self.total_lines = 0
        self.spaces = 0
        self.errors = 0
        self.end_doc = False
        self.tokens=[]
        print(pyfiglet.figlet_format("SCANNER", font = "slant"))

    def open_file(self, file_name):     #Open the file and counts how many lines has
        self.file=open("../test/"+file_name,"r")
        self.lines = self.file.readlines()
        self.total_lines = len(self.lines)
    
    def getTokens(self):                #Getting all the tokens in the file .txt
        print("INFO SCAN - Start scanning...")
        self.token_in_line = False
        self.update_cur_char()
        
        while not self.end_doc:
            acumulate = ''
            if self.peek_char() != False: 
                acumulate = self.cur_char + self.peek_char()
            cur_token=chocoToken.Token()  # We create token in every iteration

            next_char = self.peek_char()
            if self.cur_char.isalpha():     #Identify if is a keyword or ID
                self.cur_word+=self.cur_char
                while next_char!=False and (next_char.isalpha() or next_char.isdecimal() or next_char == '_'):  #We acumulate the word until there's no alpha character
                    next_char = self.step_up()
                self.token_in_line = True
                if dic.keywords.get(self.cur_word) != None:     #Verify if it's a Keyword, else ID
                    cur_token.set_info(self.cur_word,"KEYWORD",self.idx_line,self.idx_char)
                else:
                    cur_token.set_info(self.cur_word,"ID",self.idx_line,self.idx_char)
                cur_token.print_token()
                self.tokens.append(cur_token)

            elif self.cur_char.isdecimal():
                self.cur_word+=self.cur_char
                while next_char!=False and next_char.isdecimal():  #We acumulate the word until there's no alpha character
                    next_char = self.step_up()
                if not next_char.isalpha() and 2147483647>=int(self.cur_word):
                    cur_token.set_info(self.cur_word,"INTEGER",self.idx_line,self.idx_char)
                    self.token_in_line = True
                    cur_token.print_token()
                    self.tokens.append(cur_token)
                else:
                    while next_char!= False and (next_char.isalpha() or next_char.isdecimal()):
                        next_char = self.step_up()
                    self.print_error()
            
            #We create these functions to detect operators that can be useful with binary or other chars
            #We used dic to make easier the search 
            #Then we create tockens and identify them
            elif dic.operators.get(acumulate) or dic.bin_op.get(acumulate):
                self.cur_word = acumulate
                self.operator_token(cur_token)
                self.get_char()
            
            elif dic.operators.get(self.cur_char) or dic.bin_op.get(self.cur_char):
                self.cur_word = self.cur_char
                self.operator_token(cur_token)
            
            elif self.cur_char == "\"" or self.cur_char == "\'":
                self.cur_word += self.cur_char
                error = False
                while not error and (next_char!="\"" and next_char!="\'" or self.cur_char == "\\"):
                    next_char=self.step_up()
                    if next_char == False or (self.cur_char == "\\" and (next_char !="\"" and next_char != "\'")) or next_char == "\n":
                        error = True
                if next_char != False:
                    self.get_char()
                    self.cur_word+=self.cur_char
                if not error: 
                    next_char = self.peek_char()
                    cur_token.set_info(self.cur_word,"STRING",self.idx_line,self.idx_char)
                    self.token_in_line = True
                    cur_token.print_token()
                    self.tokens.append(cur_token)
                if error:
                    while next_char!= False and next_char!=" " and next_char!="\n":
                        next_char = self.step_up()
                    self.print_error()
            elif (self.cur_char != '#' and self.cur_char != '\n' and self.cur_char != ' '):
                self.cur_word = self.cur_char
                self.print_error()

            self.cur_word = ''
            

            if next_char == False:          #If nextchar is False means it's the end of the txt
                self.end_doc = True
            elif self.cur_char == '#' or next_char == '#':
                self.get_char()
                self.jump_line()
            else:
                self.get_char()           #We get the next char for the following iterations
    
    def update_cur_char(self):
        self.cur_char = self.lines[self.idx_line][self.idx_char]

    def get_char(self):    #Moves the current char to the next char if it exists, otherwise return False
        if self.cur_char != '\n':
            self.idx_char += 1
            self.update_cur_char()
            return True
        else:
            return self.jump_line()
        
    def peek_char(self): #Returns the next char if it exists, otherwise return False
        if self.cur_char != '\n' and self.idx_char+1<len(self.lines[self.idx_line]):
            return self.lines[self.idx_line][self.idx_char+1]
        elif self.total_lines-1 > self.idx_line:
            return self.lines[self.idx_line+1][0]
        else:
            return False
    def step_up(self):  #Pass to the next character
        self.get_char()
        self.cur_word+=self.cur_char 
        return self.peek_char()

    def jump_line(self): #We jump to the next line, if there was a token in the previous line we create a literal
        jump = False
        if self.token_in_line:
            literal = chocoToken.Token()
            literal.set_info("NEWLINE","LITERAL",self.idx_line,self.idx_char)
            literal.print_token()
            self.tokens.append(literal)
            self.token_in_line = False

        if self.total_lines-1 > self.idx_line:
            self.idx_line+=1
            self.idx_char = 0

            self.indent_dedent()    #Here we identify if there was indens or dedents because we are starting a new line

            self.update_cur_char()
            jump=True
        else: 
            self.end_doc = True
        return jump
    
    def operator_token(self,cur_token):
        if dic.operators.get(self.cur_word) != None:
            cur_token.set_info(self.cur_word,"OPERATOR",self.idx_line,self.idx_char)
        elif dic.bin_op.get(self.cur_word) != None:
            cur_token.set_info(self.cur_word,"BIN OPERATOR",self.idx_line,self.idx_char)
        self.token_in_line = True
        cur_token.print_token()
        self.tokens.append(cur_token)

    def indent_dedent(self):
        space_test = 0              #We'll save the amount of spaces the new line have until it reach a char
        while self.lines[self.idx_line][self.idx_char] == ' ':
                space_test += 1
                self.idx_char += 1
        if self.lines[self.idx_line][self.idx_char] != ' ' and self.lines[self.idx_line][self.idx_char] != '\n':    #If the line has no char, we just jump
            space_test = space_test/4                                                                               #to the next line
            if (space_test - self.spaces) != 0:                                                                     #We know that a dent is made up                                   
                for i in range(int(abs(space_test-self.spaces))):                                                   #of 4 spaces, that's why we devided  
                    cur_token=chocoToken.Token()                                                                    #the spaces in line by that number
                    if space_test > self.spaces:                                                                    #It's possible that we found out that
                        cur_token.set_info("","INDENT",self.idx_line,self.idx_char)                                 #more than one functions is closed  
                    else:                                                                                           #that's the reason why we need to 
                        cur_token.set_info("","DEDENT",self.idx_line,self.idx_char)                                 #make it a loop
                    cur_token.print_token()    
                    self.tokens.append(cur_token)                                                                 
                self.spaces = space_test

    def print_error(self):   #We print errors aligned
        self.errors +=1
        if self.cur_word[-1]=='\n': 
            self.cur_word = self.cur_word[:-1]
        space_occupied = len(self.cur_word)
        spaces_to_align = " "*max(0,16-space_occupied)
        print("ERROR",self.cur_word,"is not recognized",spaces_to_align,"FOUND AT (",self.idx_line + 1,":",self.idx_char,")")

    def __del__(self):
        if self.file != None:
            self.file.close()
        print("INFO SCAN COMPLETED WITH", self.errors, "ERRORS")