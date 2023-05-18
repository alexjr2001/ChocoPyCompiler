import chocoToken
import sys
sys.path.append("../")
from lib import dictionary as dic

#Recursive descent parser class
class Parser:
    def __init__(self,_scanner) -> None:
        self.errors=[]
        self.scanner=_scanner
        #self.tokens=scanner.tokens
        self.cur_token=""

    def program(self):
        if self.defList():
            if self.stmtList(): 
                return True
        return False
    
    def defList(self):
        if self._def():
            if self.defList():
                return True		
    
    def _def(self):
		#####getToken   
        if self.cur_token == "def":
			#####getToken
            if self.cur_token == "ID":
				#####getToken
                if self.cur_token == "(":
					#####getToken
                    if self.typedVarList():
                        if self.cur_token == ")":
                            if self._return():
                                if self.cur_token == ":":
                                    if self.block():
                                        return True
    
    def typedVar(self):
        if self.cur_token == "ID":
            if  self.cur_token==":":
                if self._type():
                    return True
    
    def _type(self):
        if self.cur_token == "int":
            return True
        if self.cur_token == "str":
            return True
        if self.cur_token == "[":
            if self._type():
                if self.cur_token == "]":
                    return True
    
    def typedVarList(self):
        if self.typedVar():
            if self.typedVarListTail():
                return True
    
    def typedVarListTail(self):
        if self.cur_token == ",":
            if self.typedVar():
                if self.typedVarListTail():
                    return True
    
    def _return(self):
        if self.cur_token == "->":
            if self._type():
                return True
    
    def block(self):
        if self.cur_token == "NEWLINE":
            if self.cur_token == "INDENT":
                if self.stmt():
                    if self.stmtList():
                        if self.cur_token == "DEDENT":
                            return True                   
    
    def stmtList(self):
        if self.stmt():
            if self.stmtList():
                return True
    
    def stmt(self):
        if self.simpleStmt():
            if self.cur_token == "NEWLINE":
                return True
        elif self.cur_token == "if":
            if self.expr():
                if self.cur_token == ":":
                    if self.block():
                        if self.elifList():
                            if self._else():
                                return True
        elif self.cur_token == "while":
            if self.expr():
                if self.cur_token == ":":
                    if self.block():
                        return True
        elif self.cur_token=="for":
            if self.cur_token=="ID":
                if self.cur_token=="in":
                    if self.expr():
                        if self.cur_token == ":":
                            if self.block():
                                return True
    
    def elifList(self):
        if self._elif():
            if self._elifList():
                return True
    
    def _elif(self):
        if self.cur_token=="elif":
            if self.expr():
                if self.cur_token==":":
                    if self.block():
                        return True
    
    def _else(self):
        if self.cur_token == "else":
            if self.cur_token == ":":
                if self.block():
                    return True
    
    def simpleStmt(self):
           if self.expr():
               if self.ssTail():
                   return True
           if self.cur_token == "pass":
                return True
           if self.cur_token == "return":
               if self.returnExpr():
                    return True
    
    def ssTail(self):
        if self.cur_token=="=":
            if self.expr():
                return True

    def returnExpr(self):
        if self.expr():
            return True       
    
    def expr(self):
        if self.orExpr():
            if self.exprPrime():
                return True
    
    def exprPrime(self):
        if self.cur_token=="if":
            if self.andExpr():
                if self.cur_token=="else":
                    if self.andExpr():
                        if self.exprPrime():
                            return True
    
    def orExpr(self):
        if self.andExpr():
            if self.orExprPrime():
                return True
            
    def orExprPrime(self):
        if self.cur_token == "or":
            if self.andExpr():
                if self.orExprPrime():
                    return True
    
    def andExpr(self):
        if self.notExpr():
            if self.andExprPrime():
                return True
            
    def andExprPrime(self):
        if self.cur_token == "and":
            if self.notExpr():
                if self.andExprPrime():
                    return True
                
    def notExpr(self):
        if self.compExpr():
            if self.notExprPrime():
                return True
    def notExprPrime(self):
        if self.cur_token == "not":
            if self.compExpr():
                if self.notExprPrime():
                    return True
    def compExpr(self):
        if self.intExpr():
            if self.compExprPrime():
                return True
            
    def compExprPrime(self):
        if self.compOp():
            if self.intExpr():
                if self.compExprPrime():
                    return True

    def intExpr(self):
        if self.term():
            if self.intExprPrime():
                return True

    def intExprPrime(self):
        if self.cur_token == "+" or self.cur_token == "-":
            if self.term():
                if self.intExprPrime():
                    return True
                
    def term(self):
        if self.factor():
            if self.termPrime():
                return True
    
    def termPrime(self):
        if self.cur_token=="*" or self.cur_token=="//" or self.cur_token=="%":
            if self.factor():
                if self.termExprPrime():
                    return True
    
    def factor(self):
        if self.name() or self.literal() or self._list():
            return True
        if self.cur_token == "-":
            if self.factor():
                return True
        if self.cur_token == "(":
            if self.expr():
                if self.cur_token==")":
                    return True
    
    def name(self):
        if self.cur_token == "ID":
            if self.nameTail():
                return True
    
    def nameTail(self):
        if self._list():
            return True
        if self.cur_token == "(":
            if self.exprList():
                if self.cur_token == ")":
                    return True
                
    def literal(self):
        if self.cur_token == "None" or self.cur_token == "True" or self.cur_token == "False" or self.cur_token == "INTEGER" or self.cur_token == "STRING":
            return True
    
    def _list(self):
        if self.cur_token == "[":
            if self.exprList():
                if self.cur_token == "]":
                    return True
    
    def exprList(self):
        if self.expr():
            if self.exprListTail():
                return True
    
    def exprListTail(self):
        if self.cur_token == ",":
            if self.expr():
                if self.exprListTail():
                    return True
                
    def compOp(self):
        if self.cur_token == "==" or self.cur_token == "!=" or self.cur_token == "<" or self.cur_token == ">" or self.cur_token == "<=" or self.cur_token == ">=" or self.cur_token == "is":
            return True
    
    
    

    
                   