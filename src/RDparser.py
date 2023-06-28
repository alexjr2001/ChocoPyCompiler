import scanner
import chocoToken
import pyfiglet
import sys
sys.path.append("../")
from lib import dictionary as dic
from lib import follows as flws
from anytree import Node, RenderTree
from anytree.exporter import UniqueDotExporter

#Recursive descent parser class
class Parser:
    def __init__(self,_scanner) -> None:
        self.errors=[]
        self.scanner = _scanner
        self.idx_token = -1
        self.tokens = self.scanner.tokens   #Lista de objetos token
        eof = chocoToken.Token('$','EOF')
        self.tokens.append(eof)
        #for i in self.tokens: 
        #    print(i.name,"->",i.type)
        self.cur_token = None
        self.n_errors = 0
        self.treeFile = open("../visual/Tree.txt","w",encoding="utf-8")
        print(pyfiglet.figlet_format("PARSER", font = "slant"))
    
    

    def render_tree(root: object) -> None:
        for pre, fill, node in RenderTree(root):
            print("%s%s" % (pre, node.name))


    def getToken(self):
        if self.cur_token != None and self.cur_token.name=='$':
            self.__del__()
        elif (self.idx_token+1<len(self.tokens)):
            self.idx_token+=1
            self.cur_token = self.tokens[self.idx_token]
        else:
            self.__del__()
    
    def peekToken(self):
        if(self.idx_token+1<len(self.tokens)):
            return self.tokens[self.idx_token+1]
        return False
    
    def check_term(self,terminal):
        nextToken=self.peekToken()
        if nextToken != False:
            if terminal in ["STRING","INTEGER","ID","DEDENT","INDENT"]:
                if nextToken.type== terminal:
                    self.getToken()
                    return True
            else:
                if nextToken.name == terminal:
                    self.getToken()
                    return True
        return False
    def verifyFollows(self,nonterm):    ###FOLLLOWS
        self.cur_token=self.tokens[self.idx_token]
        if self.peekToken() != False:
            if nonterm.get(self.peekToken().name):
                return True
            elif nonterm.get(self.peekToken().type):
                return True
        return False

    def reTrue(self):
        return True

    def errorManage(self,syncFunction,front=0):   ##We pass a function which have to be called after the newline
        if self.idx_token<len(self.tokens)-1 and self.tokens[self.idx_token+1].name!="NEWLINE":
            self.idx_token+=1
            self.cur_token=self.tokens[self.idx_token]
        #print("1 ",self.cur_token.print_token())
        #print("name: ", self.cur_token.name)
        if self.cur_token.name != "$": 
            self.print_error()
            while self.idx_token<len(self.tokens)-1 and self.tokens[self.idx_token+1].name != "NEWLINE":  #Verify if we're in newline to continue to parse or is the last line to finish de parse
                self.idx_token+=1
                self.cur_token=self.tokens[self.idx_token]
            if self.idx_token<len(self.tokens)-1 and self.tokens[self.idx_token+1].name == "NEWLINE":
                self.idx_token+=front
                self.cur_token=self.tokens[self.idx_token]
            #print("2 ",self.cur_token.print_token())
            return syncFunction()
       # print("3 ",self.cur_token.print_token())
       
    def print_error(self):
        self.n_errors +=1
        space_occupied = len(self.cur_token.name)
        spaces_to_align = " "*max(0,16-space_occupied)
        print("ERROR",self.cur_token.name,"does not follow the grammar",spaces_to_align,"FOUND AT (",self.cur_token.line + 1,":",self.cur_token.column,")")
    
    ##Grammar functions
    def program(self):
        Root= Node("Root")
        if self.defList(Root):
            if self.stmtList(Root): 
                pass;
        if self.n_errors == 0: 
            print("Grammar Accepted")
        else:
            print("Grammar Not-Accepted")
        
        with self.treeFile as f:
            print(RenderTree(Root).by_attr(),file=f)
        UniqueDotExporter(Root).to_picture("../visual/TreeImg.png")
        #self.treeFile.write()
        #DotExporter(Root).to_dotfile("tree.dot")

        return True
    
    def defList(self,parent=None):          ##Puede ser vacío FOLLOW
        #newNode=Node("defList",parent)
        #parent=newNode
        if self._def(parent):
            if self.defList(parent):
                return True
        ###FOLLLOWS
        elif self.verifyFollows(flws.defList):
            return True
        
        
        #return self.errorManage(self.block)		##El unico errorMessage no funciona aun
    
    def _def(self,parent=None):
        if self.check_term("def"):
            newNode=Node("DEF",parent)
            parent=newNode   
            newNode=Node("def",parent)
            if self.check_term("ID"):
                newNode=Node(self.cur_token.name,parent)
                if self.check_term("("):
                    newNode=Node("(",parent)
                    if self.typedVarList(parent):
                        if self.check_term(")"):
                            newNode=Node(")",parent)
                            if self._return(parent):
                                if self.check_term(":"):
                                    newNode=Node(":",parent)
                                    if self.block(parent):
                                        return True
        if flws.defList.get(self.peekToken().name)==None:
            if self.idx_token!=0:
                return self.errorManage(self.block)		##El unico errorMessage no funciona aun
            else:
                return self.errorManage(self.defList)
    def typedVar(self,parent=None):
        newNode=Node("TYPEDVAR",parent)
        parent=newNode
        if self.check_term("ID"):
            newNode=Node(self.cur_token.name,parent)
            if  self.check_term(":"):
                newNode=Node(":",parent)
                if self._type(parent):
                    return True
    
    def _type(self,parent=None):
        #newNode=Node("TYPE",parent)
        #parent=newNode
        if self.check_term("int"):
            newNode=Node("int",parent)
            return True
        if self.check_term("str"):
            newNode=Node("str",parent)
            return True
        if self.check_term("["):
            newNode=Node("[",parent)
            if self._type(parent):
                if self.check_term("]"):
                    newNode=Node("]",parent)
                    return True
    
    def typedVarList(self,parent=None):   ##Puede ser vacío FOLLOW
        #newNode=Node("typedVarList",parent)
        #parent=newNode
        if self.typedVar(parent):
            if self.typedVarListTail(parent):
                return True
        ###FOLLLOWS
        elif self.verifyFollows(flws.typedVarList):
            return True
        #########
    
    def typedVarListTail(self,parent=None): ##Puede ser vacío FOLLOW
        #newNode=Node("typedVarListTail",parent)
        #parent=newNode
        if self.check_term(","):
            newNode=Node(",",parent)
            if self.typedVar(parent):
                if self.typedVarListTail(parent):
                    return True
                
        elif self.verifyFollows(flws.typedVarListTail):
            return True
    
    def _return(self,parent=None):  ##Puede ser vacío FOLLOW
        #newNode=Node("RETURN",parent)
        #parent=newNode
        if self.check_term("->"):
            newNode=Node("RETURN",parent)
            parent=newNode
            newNode=Node("->",parent)
            if self._type(parent):
                return True

        elif self.verifyFollows(flws._return):
            return True
    
    def block(self,parent=None):
        #print("Llama")
        #newNode=Node("BLOCK",parent)
        #parent=newNode
        if self.check_term("NEWLINE"):
            newNode=Node("BLOCK",parent)
            parent=newNode
            #newNode=Node("NEWLINE",parent)
            if self.check_term("INDENT"):
                #newNode=Node("INDENT",parent)
                if self.stmt(parent):
                    if self.stmtList(parent):
                        if self.check_term("DEDENT"):
                            #newNode=Node("DEDENT",parent)
                            return True                   
    
    def stmtList(self,parent=None):   ##Puede ser vacío FOLLOW
        #newNode=Node("stmtList",parent)
        #parent=newNode
        if self.stmt(parent):
            if self.stmtList(parent):
                return True
            
        elif self.verifyFollows(flws.stmtList):
            return True
    
    def stmt(self,parent=None):
        #newNode=Node("stmt",parent)
        #parent=newNode
        if self.simpleStmt(parent):
            if self.check_term("NEWLINE"):
                #newNode=Node("NEWLINE",parent)
                return True
        elif self.check_term("if"):
            newNode=Node("STMT",parent)
            parent=newNode
            newNode=Node("if",parent)
            if self.expr(parent):
                if self.check_term(":"):
                    newNode=Node(":",parent)
                    if self.block(parent):
                        if self.elifList(parent):
                            if self._else(parent):
                                return True
                        #if self.errorManage(self.block) and self.elifList():		##El unico errorMessage no funciona aun
                        #    if self._else():
                        #        return True
            if self.errorManage(self.block) and self.elifList():
                if self._else():
                    return True
    
        elif self.check_term("while"):
            newNode=Node("STMT",parent)
            parent=newNode
            newNode=Node("while",parent)
            if self.expr(parent):
                if self.check_term(":"):
                    newNode=Node(":",parent)
                    if self.block(parent):
                        return True
            return self.errorManage(self.block)		##El unico errorMessage no funciona
                                        
        elif self.check_term("for"):
            newNode=Node("STMT",parent)
            parent=newNode
            newNode=Node("for",parent)
            if self.check_term("ID"):
                newNode=Node(self.cur_token.name,parent)
                if self.check_term("in"):
                    newNode=Node("in",parent)
                    if self.expr(parent):
                        if self.check_term(":"):
                            newNode=Node(":",parent)
                            if self.block(parent):
                                return True
            return self.errorManage(self.block)		##El unico errorMessage no funciona
    
    def elifList(self,parent=None):   ##Puede ser vacío FOLLOW
        #newNode=Node("elifList",parent)
        #parent=newNode
        if self._elif(parent):
            if self.elifList(parent):
                return True
            #return self.errorManage(self.stmtList,1)
        elif self.verifyFollows(flws.elifList):  #ID 
            return True
        if self.errorManage(self.block):		##El unico errorMessage no funciona aun
            if self.elifList(parent):
                return True
    
    def _elif(self,parent=None):
        #newNode=Node("elif",parent)
        #parent=newNode
        if self.check_term("elif"):
            newNode=Node("elif",parent)
            if self.expr(parent):
                if self.check_term(":"):
                    newNode=Node(":",parent)
                    if self.block(parent):
                        return True
            return self.errorManage(self.block)	#Da error No porque puede ser un follow	##El unico errorMessage no funciona aun
    
    def _else(self,parent=None):    ##Puede ser vacío FOLLOW
        #newNode=Node("else",parent)
        #parent=newNode
        if self.check_term("else"):
            newNode=Node("else",parent)
            if self.check_term(":"):
                newNode=Node(":",parent)
                if self.block(parent):
                    return True
        
        elif self.verifyFollows(flws._else):
            return True

        return self.errorManage(self.block)		##El unico errorMessage no funciona aun
    
    def simpleStmt(self,parent=None):
        #newNode=Node("simpleStmt",parent)
        #parent=newNode
        if self.expr(parent):
            if self.ssTail(parent):
                return True
            else:
                return self.errorManage(self.reTrue)
        elif self.check_term("pass"):
            newNode=Node("pass",parent)
            return True
        elif self.check_term("return"):
            newNode=Node("return",parent)
            if self.returnExpr(parent):
                return True
            else:
                return self.errorManage(self.reTrue)
            
    
    def ssTail(self,parent=None):       ##Puede ser vacío FOLLOW
        #newNode=Node("ssTail",parent)
        #parent=newNode
        if self.check_term("="):
            newNode=Node("=",parent)
            if self.expr(parent):
                return True
        
        elif self.verifyFollows(flws.ssTail):
            return True

    def returnExpr(self,parent=None):      ##Puede ser vacío FOLLOW
        #newNode=Node("returnExpr",parent)
        #parent=newNode
        if self.expr(parent):
            return True       
        
        elif self.verifyFollows(flws.returnExpr):
            return True
    
    def expr(self,parent=None):
        newTree=Node("EXPR")
        parentTemp=newTree
        if self.orExpr(parentTemp):
            if self.exprPrime(parentTemp):
                if(newTree.height>0):
                    if(newTree.children.__len__()==1):
                        newTree.name="FACTOR"
                    newTree.parent = parent
                return True
    
    def exprPrime(self,parent=None):      ##Puede ser vacío FOLLOW
        #newNode=Node("exprPrime",parent)
        #parent=newNode
        if self.check_term("if"):
            newNode=Node("if",parent)
            if self.andExpr(parent):
                if self.check_term("else"):
                    newNode=Node("else",parent)
                    if self.andExpr(parent):
                        if self.exprPrime(parent):
                            return True
        
        elif self.verifyFollows(flws.exprPrime):
            return True
    
    def orExpr(self,parent=None):
        #newNode=Node("orExpr",parent)
        #parent=newNode
        if self.andExpr(parent):
            if self.orExprPrime(parent):
                return True
            
    def orExprPrime(self,parent=None):    ##Puede ser vacío FOLLOW
        #newNode=Node("orExprPrime",parent)
        #parent=newNode
        if self.check_term("or"):
            newNode=Node("or",parent)
            if self.andExpr(parent):
                if self.orExprPrime(parent):
                    return True
                
        elif self.verifyFollows(flws.orExprPrime):
            return True
    
    def andExpr(self,parent=None):
        #newNode=Node("andExpr",parent)
        #parent=newNode
        if self.notExpr(parent):
            if self.andExprPrime(parent):
                return True
            
    def andExprPrime(self,parent=None):            ##Puede ser vacío FOLLOW
        #newNode=Node("andExprPrime",parent)
        #parent=newNode
        if self.check_term("and"):
            newNode=Node("and",parent)
            if self.notExpr(parent):
                if self.andExprPrime(parent):
                    return True
        
        elif self.verifyFollows(flws.andExprPrime):
            return True
                
    def notExpr(self,parent=None):
        #newNode=Node("notExpr",parent)
        #parent=newNode
        if self.compExpr(parent):
            if self.notExprPrime(parent):
                return True
            
    def notExprPrime(self,parent=None):       ##Puede ser vacío FOLLOW
        #newNode=Node("notExprPrime",parent)
        #parent=newNode
        if self.check_term("not"):
            newNode=Node("not",parent)
            if self.compExpr(parent):
                if self.notExprPrime(parent):
                    return True
        
        elif self.verifyFollows(flws.notExprPrime):
            return True
        
    def compExpr(self,parent=None):
        #newNode=Node("compExpr",parent)
        #parent=newNode
        if self.intExpr(parent):
            if self.compExprPrime(parent):
                return True
            
    def compExprPrime(self,parent=None):         ##Puede ser vacío FOLLOW
        #newNode=Node("compExprPrime",parent)
        #parent=newNode
        if self.compOp(parent):
            if self.intExpr(parent):
                if self.compExprPrime(parent):
                    return True
                
        elif self.verifyFollows(flws.compExprPrime):
            return True

    def intExpr(self,parent=None):
        #newNode=Node("intExpr",parent)
        #parent=newNode
        if self.term(parent):
            if self.intExprPrime(parent):
                return True

    def intExprPrime(self,parent=None):     ##Puede ser vacío FOLLOW
        #newNode=Node("intExprPrime",parent)
        #parent=newNode
        if self.check_term("+") or self.check_term("-"):
            newNode=Node(self.cur_token.name,parent)
            if self.term(parent):
                if self.intExprPrime(parent):
                    return True
                
        elif self.verifyFollows(flws.intExprPrime):
            return True
                
    def term(self,parent=None):
        #newNode=Node("term",parent)
        #parent=newNode
        if self.factor(parent):
            if self.termPrime(parent):
                return True
    
    def termPrime(self,parent=None):        ##Puede ser vacío FOLLOW
        #newNode=Node("termPrime",parent)
        #parent=newNode
        if self.check_term("*") or self.check_term("//") or self.check_term("%"):
            newNode=Node(self.cur_token.name,parent)
            if self.factor(parent):
                if self.termPrime(parent):
                    return True
            
        elif self.verifyFollows(flws.termPrime):
            return True
    
    def factor(self,parent=None):
        #newNode=Node("factor",parent)
        #parent=newNode
        if self.name(parent) or self.literal(parent) or self._list(parent):
            return True
        if self.check_term("-"):
            newNode=Node("-",parent)
            if self.factor(parent):
                return True
        if self.check_term("("):
            newNode=Node("(",parent)
            if self.expr(parent):
                if self.check_term(")"):
                    newNode=Node(")",parent)
                    return True
    
    def name(self,parent=None):
        #newNode=Node("name",parent)
        #parent=newNode
        if self.check_term("ID"):
            newNode=Node(self.cur_token.name,parent)
            if self.nameTail(parent):
                return True
    
    def nameTail(self,parent=None):         ##Puede ser vacío FOLLOW
        #newNode=Node("nameTail",parent)
        #parent=newNode
        if self._list(parent):
            return True
        if self.check_term("("):
            newNode=Node("(",parent)
            if self.exprList(parent):
                if self.check_term(")"):
                    newNode=Node(")",parent)
                    return True
        
        elif self.verifyFollows(flws.nameTail):     #Está bien posicionado?
            return True
                
    def literal(self,parent=None):
        if self.check_term("None") or self.check_term("True") or self.check_term("False") or self.check_term("INTEGER") or self.check_term("STRING"):
            newNode=Node(self.cur_token.name,parent)
            return True
    
    def _list(self,parent=None):
        #newNode=Node("list",parent)
        #parent=newNode
        if self.check_term("["):
            newNode=Node("[",parent)
            if self.exprList(parent):
                if self.check_term("]"):
                    newNode=Node("]",parent)
                    return True
        #Retrocedo
    def exprList(self,parent=None):     ##Puede ser vacío FOLLOW
        #newNode=Node("exprList",parent)
        #parent=newNode
        if self.expr(parent):
            if self.exprListTail(parent):
                return True
        
        elif self.verifyFollows(flws.exprList):
            return True
    
    def exprListTail(self,parent=None):     ##Puede ser vacío FOLLOW
        #newNode=Node("exprListTail",parent)
        #parent=newNode
        if self.check_term(","):
            newNode=Node(",",parent)
            if self.expr(parent):
                if self.exprListTail(parent):
                    return True
        
        elif self.verifyFollows(flws.exprListTail):
            return True
                
    def compOp(self,parent=None):
        #newNode=Node("compOp",parent)
        #parent=newNode
        if self.check_term("==") or self.check_term("!=") or self.check_term("<") or self.check_term(">") or self.check_term("<=") or self.check_term(">=") or self.check_term("is"):
            newNode=Node(self.cur_token.name,parent)
            return True
        
    def __del__(self):
        self.treeFile.close()
        print("PARSING COMPLETED WITH", self.n_errors, "ERRORS")
    
    
    

    
                   