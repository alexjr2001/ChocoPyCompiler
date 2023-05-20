import scanner
import chocoToken
import pyfiglet
import sys
sys.path.append("../")
from lib import dictionary as dic
from lib import follows as flws

#Recursive descent parser class
class Parser:
    def __init__(self,_scanner) -> None:
        self.errors=[]
        self.scanner = _scanner
        self.idx_token = -1
        self.tokens = self.scanner.tokens   #Lista de objetos token
        eof = chocoToken.Token('$','EOF')
        self.tokens.append(eof)
        for i in self.tokens: 
            print(i.name,"->",i.type)
        self.cur_token = None
        self.n_errors = 0
        print(pyfiglet.figlet_format("PARSER", font = "slant"))
    
    def getToken(self):
        if(self.idx_token+1<len(self.tokens)):
            self.cur_token = self.tokens[self.idx_token+1]
        else:
            self.__del__()
    
    def peekToken(self):
        if(self.idx_token+1<len(self.tokens)):
            return self.tokens[self.idx_token+1]
        return False

    def verifyFollows(self,nonterm):    ###FOLLLOWS
        if self.peekToken() != False:
            if nonterm.get(self.peekToken().name):
                return True
            elif nonterm.get(self.peekToken().type):
                return True
        return False

            
    def errorManage(self,syncFunction):   ##We pass a function which have to be called after the newline
        self.print_error()
        self.idx_token+=1
        self.cur_token=self.tokens[self.idx_token]
        while self.idx_token<len(self.tokens)-1 and self.tokens[self.idx_token+1] != "NEWLINE":  #Verify if we're in newline to continue to parse or is the last line to finish de parse
            self.idx_token+=1
            self.cur_token=self.tokens[self.idx_token]
        return syncFunction()
    
    def print_error(self):
        self.n_errors +=1
        space_occupied = len(self.cur_token.name)
        spaces_to_align = " "*max(0,16-space_occupied)
        print("ERROR",self.cur_token.name,"does not follow the grammar",spaces_to_align,"FOUND AT (",self.cur_token.line + 1,":",self.cur_token.column,")")
    
    ##Grammar functions
    def program(self):
        if self.defList():
            if self.stmtList(): 
                if self.n_errors == 0: 
                    print("Grammar Accepted")
                else:
                    print("Grammar Not-Accepted")
                return True
         
    
    def defList(self):          ##Puede ser vacío FOLLOW
        if self._def():
            if self.defList():
                return True
        ###FOLLLOWS
        elif self.verifyFollows(flws.defList):
            return True
        
        else: 
            return self.errorManage(self.block())		##El unico errorMessage no funciona aun
    
    def _def(self):
        self.getToken()   
        if self.cur_token.name == "def":
            self.getToken()   
            if self.cur_token.type == "ID":
                self.getToken()
                if self.cur_token.name == "(":
                    if self.typedVarList():
                        self.getToken()
                        if self.cur_token.name == ")":
                            if self._return():
                                self.getToken()
                                if self.cur_token.name == ":":
                                    if self.block():
                                        return True     
    
    def typedVar(self):
        self.getToken()
        if self.cur_token.type == "ID":
            self.getToken()
            if  self.cur_token.name ==":":
                if self._type():
                    return True
    
    def _type(self):
        self.getToken()
        if self.cur_token.name == "int":
            return True
        if self.cur_token.name == "str":
            return True
        if self.cur_token.name == "[":
            if self._type():
                self.getToken()
                if self.cur_token.name == "]":
                    return True
    
    def typedVarList(self):   ##Puede ser vacío FOLLOW
        if self.typedVar():
            if self.typedVarListTail():
                return True
        ###FOLLLOWS
        elif self.verifyFollows(flws.typedVarList):
            return True
        #########
    
    def typedVarListTail(self): ##Puede ser vacío FOLLOW
        self.getToken()
        if self.cur_token.name == ",":
            if self.typedVar():
                if self.typedVarListTail():
                    return True
                
        elif self.verifyFollows(flws.typedVarListTail):
            return True
    
    def _return(self):  ##Puede ser vacío FOLLOW
        self.getToken()
        if self.cur_token.name == "->":
            if self._type():
                return True

        elif self.verifyFollows(flws._return):
            return True
    
    def block(self):
        self.getToken()
        if self.cur_token.name == "NEWLINE":
            self.getToken()
            if self.cur_token.type == "INDENT":
                if self.stmt():
                    if self.stmtList():
                        self.getToken()
                        if self.cur_token.type == "DEDENT":
                            return True                   
    
    def stmtList(self):   ##Puede ser vacío FOLLOW
        if self.stmt():
            if self.stmtList():
                return True
            
        elif self.verifyFollows(flws.stmtList):
            return True
    
    def stmt(self):
        self.getToken()
        if self.simpleStmt():
            if self.cur_token.name == "NEWLINE":
                return True
        elif self.cur_token.name == "if":
            if self.expr():
                self.getToken()
                if self.cur_token.name == ":":
                    if self.block():
                        if self.elifList():
                            if self._else():
                                return True
        elif self.cur_token.name == "while":
            if self.expr():
                self.getToken()
                if self.cur_token.name == ":":
                    if self.block():
                        return True
        elif self.cur_token.name =="for":
            self.getToken()
            if self.cur_token.type =="ID":
                self.getToken()
                if self.cur_token.name =="in":
                    if self.expr():
                        self.getToken()
                        if self.cur_token.name == ":":
                            if self.block():
                                return True
    
    def elifList(self):   ##Puede ser vacío FOLLOW
        if self._elif():
            if self._elifList():
                return True
            
        elif self.verifyFollows(flws.elifList):
            return True
    
    def _elif(self):
        self.getToken()
        if self.cur_token.name =="elif":
            if self.expr():
                self.getToken()
                if self.cur_token.name ==":":
                    if self.block():
                        return True
    
    def _else(self):    ##Puede ser vacío FOLLOW
        self.getToken()
        if self.cur_token.name == "else":
            self.getToken()
            if self.cur_token.name == ":":
                if self.block():
                    return True
        
        elif self.verifyFollows(flws._else):
            return True
    
    def simpleStmt(self):
            if self.expr():
               if self.ssTail():
                   return True
            self.getToken()
            if self.cur_token.name == "pass":
                return True
            if self.cur_token.name == "return":
                if self.returnExpr():
                    return True
    
    def ssTail(self):       ##Puede ser vacío FOLLOW
        self.getToken()
        if self.cur_token.name == "=":
            if self.expr():
                return True
        
        elif self.verifyFollows(flws.ssTail):
            return True

    def returnExpr(self):      ##Puede ser vacío FOLLOW
        if self.expr():
            return True       
        
        elif self.verifyFollows(flws.returnExpr):
            return True
    
    def expr(self):
        if self.orExpr():
            if self.exprPrime():
                return True
    
    def exprPrime(self):      ##Puede ser vacío FOLLOW
        self.getToken()
        if self.cur_token.name =="if":
            if self.andExpr():
                self.getToken()
                if self.cur_token.name =="else":
                    if self.andExpr():
                        if self.exprPrime():
                            return True
        
        elif self.verifyFollows(flws.exprPrime):
            return True
    
    def orExpr(self):
        if self.andExpr():
            if self.orExprPrime():
                return True
            
    def orExprPrime(self):    ##Puede ser vacío FOLLOW
        self.getToken()
        if self.cur_token.name == "or":
            if self.andExpr():
                if self.orExprPrime():
                    return True
                
        elif self.verifyFollows(flws.orExprPrime):
            return True
    
    def andExpr(self):
        if self.notExpr():
            if self.andExprPrime():
                return True
            
    def andExprPrime(self):            ##Puede ser vacío FOLLOW
        self.getToken()
        if self.cur_token.name == "and":
            if self.notExpr():
                if self.andExprPrime():
                    return True
        
        elif self.verifyFollows(flws.andExprPrime):
            return True
                
    def notExpr(self):
        if self.compExpr():
            if self.notExprPrime():
                return True
    def notExprPrime(self):       ##Puede ser vacío FOLLOW
        self.getToken()
        if self.cur_token.name == "not":
            if self.compExpr():
                if self.notExprPrime():
                    return True
        
        elif self.verifyFollows(flws.notExprPrime):
            return True
        
    def compExpr(self):
        if self.intExpr():
            if self.compExprPrime():
                return True
            
    def compExprPrime(self):         ##Puede ser vacío FOLLOW
        if self.compOp():
            if self.intExpr():
                if self.compExprPrime():
                    return True
                
        elif self.verifyFollows(flws.compExprPrime):
            return True

    def intExpr(self):
        if self.term():
            if self.intExprPrime():
                return True

    def intExprPrime(self):     ##Puede ser vacío FOLLOW
        self.getToken()
        if self.cur_token.name == "+" or self.cur_token.name == "-":
            if self.term():
                if self.intExprPrime():
                    return True
                
        elif self.verifyFollows(flws.intExprPrime):
            return True
                
    def term(self):
        if self.factor():
            if self.termPrime():
                return True
    
    def termPrime(self):        ##Puede ser vacío FOLLOW
        self.getToken()
        if self.cur_token.name == "*" or self.cur_token.name == "//" or self.cur_token.name =="%":
            if self.factor():
                if self.termExprPrime():
                    return True
            
        elif self.verifyFollows(flws.termPrime):
            return True
    
    def factor(self):
        if self.name() or self.literal() or self._list():
            return True
        self.getToken()
        if self.cur_token.name == "-":
            if self.factor():
                return True
        self.getToken()
        if self.cur_token.name == "(":
            if self.expr():
                self.getToken()
                if self.cur_token.name == ")":
                    return True
    
    def name(self):
        self.getToken()
        if self.cur_token.type == "ID":
            if self.nameTail():
                return True
    
    def nameTail(self):         ##Puede ser vacío FOLLOW
        if self._list():
            return True
        self.getToken()
        if self.cur_token.name == "(":
            if self.exprList():
                self.getToken()
                if self.cur_token.name == ")":
                    return True
        
        elif self.verifyFollows(flws.nameTail):     #Está bien posicionado?
            return True
                
    def literal(self):
        self.getToken()
        if self.cur_token.name == "None" or self.cur_token.name == "True" or self.cur_token.name == "False" or self.cur_token.type == "INTEGER" or self.cur_token.type == "STRING":
            return True
    
    def _list(self):
        self.getToken()
        if self.cur_token.name == "[":
            if self.exprList():
                self.getToken()
                if self.cur_token.name == "]":
                    return True
    
    def exprList(self):     ##Puede ser vacío FOLLOW
        if self.expr():
            if self.exprListTail():
                return True
        
        elif self.verifyFollows(flws.exprList):
            return True
    
    def exprListTail(self):     ##Puede ser vacío FOLLOW
        self.getToken()
        if self.cur_token.name == ",":
            if self.expr():
                if self.exprListTail():
                    return True
        
        elif self.verifyFollows(flws.exprListTail):
            return True
                
    def compOp(self):
        self.getToken()
        if self.cur_token.name == "==" or self.cur_token.name == "!=" or self.cur_token.name == "<" or self.cur_token.name == ">" or self.cur_token.name == "<=" or self.cur_token.name == ">=" or self.cur_token.name == "is":
            return True
        
    def __del__(self):
        print("PARSING COMPLETED WITH", self.n_errors, "ERRORS")
    
    
    

    
                   