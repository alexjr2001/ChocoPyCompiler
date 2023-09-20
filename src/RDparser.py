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
        self.cur_parent=Node("Constructor")
        self.cur_children=[]
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
        if(self.idx_token>-1):
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
        if self.cur_token.name != "$": 
            self.print_error()
            while self.idx_token<len(self.tokens)-1 and self.tokens[self.idx_token+1].name != "NEWLINE":  #Verify if we're in newline to continue to parse or is the last line to finish de parse
                self.idx_token+=1
                self.cur_token=self.tokens[self.idx_token]
            if self.idx_token<len(self.tokens)-1 and self.tokens[self.idx_token+1].name == "NEWLINE":
                self.idx_token+=front
                self.cur_token=self.tokens[self.idx_token]
            return syncFunction()
       
    def print_error(self):
        self.n_errors +=1
        space_occupied = len(self.cur_token.name)
        spaces_to_align = " "*max(0,16-space_occupied)
        print("ERROR",self.cur_token.name,"is unexpected term that does not follow the grammar",spaces_to_align,"FOUND AT (",self.cur_token.line + 1,":",self.cur_token.column,")")
    
    ##Grammar functions
    def program(self):
        Root= Node("Program")
        if self.defList(Root):
            if self.stmtList(Root): 
                pass;
        if self.n_errors == 0 and self.scanner.errors == 0: 
            print("Grammar Accepted")
            with self.treeFile as f:
                print(RenderTree(Root).by_attr(),file=f)
            UniqueDotExporter(Root).to_picture("../visual/TreeImg.png")
        else:
            print("Grammar Not-Accepted")
        

        return True
    
    def defList(self,parent=None):          ##It could be empty, so it has a FOLLOW list
        if self._def(parent):
            if self.defList(parent):
                return True
        ###FOLLLOWS
        elif self.verifyFollows(flws.defList):
            return True
    
    def _def(self,parent=None):
        if self.check_term("def"):
            newNode=Node("def",parent)
            parent=newNode   
            if self.check_term("ID"):
                newNode=Node(self.cur_token.name,parent)
                if self.check_term("("):
                    if self.typedVarList(parent):
                        if self.check_term(")"):
                            if self._return(parent):
                                if self.check_term(":"):
                                    if self.block(parent):
                                        return True
            return self.errorManage(self.block)
        if self.peekToken().type=="ID":         ##Error al inicio de def
            if self.idx_token+2<len(self.tokens):
                if self.tokens[self.idx_token+2].type=="ID":
                    return self.errorManage(self.block)
        return False
    def typedVar(self,parent=None):
        if self.check_term("ID"):
            newNode=Node(":",parent)
            parent=newNode
            newNode=Node(self.cur_token.name,parent)
            if  self.check_term(":"):
                if self._type(parent):
                    return True
    
    def _type(self,parent=None):
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
    
    def typedVarList(self,parent=None):   ##It could be empty, so it has a FOLLOW list
        if self.typedVar(parent):
            if self.typedVarListTail(parent):
                return True
        ###FOLLLOWS
        elif self.verifyFollows(flws.typedVarList):
            return True
        #########
    
    def typedVarListTail(self,parent=None): ##It could be empty, so it has a FOLLOW list
        if self.check_term(","):
            if self.typedVar(parent):
                if self.typedVarListTail(parent):
                    return True
                
        elif self.verifyFollows(flws.typedVarListTail):
            return True
    
    def _return(self,parent=None):  ##It could be empty, so it has a FOLLOW list
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
        if self.check_term("NEWLINE"):
            newNode=Node("BLOCK",parent)
            parent=newNode
            if self.check_term("INDENT"):
                if self.stmt(parent):
                    if self.stmtList(parent):
                        if self.check_term("DEDENT"):
                            return True
            return self.errorManage(self.stmtList,1)                   
    
    def stmtList(self,parent=None):   ##It could be empty, so it has a FOLLOW list
        if self.stmt(parent):
            if self.stmtList(parent):
                return True
            
        elif self.verifyFollows(flws.stmtList):
            return True
    
    def stmt(self,parent=None):
        if self.simpleStmt(parent):
            if self.check_term("NEWLINE"):
                return True
        elif self.check_term("if"):
            newNode=Node("if",parent)
            parent=newNode
            if self.expr(parent):
                if self.check_term(":"):
                    if self.block(parent):
                        if self.elifList(parent):
                            if self._else(parent):
                                return True
            if self.errorManage(self.block) and self.elifList():
                if self._else():
                    return True
    
        elif self.check_term("while"):
            newNode=Node("while",parent)
            parent=newNode
            if self.expr(parent):
                if self.check_term(":"):
                    if self.block(parent):
                        return True
            return self.errorManage(self.block)		##El unico errorMessage no funciona
                                        
        elif self.check_term("for"):
            newNode=Node("for",parent)
            parent=newNode
            if self.check_term("ID"):
                newNode=Node(self.cur_token.name,parent)
                if self.check_term("in"):
                    newNode=Node("in",parent)
                    if self.expr(parent):
                        if self.check_term(":"):
                            if self.block(parent):
                                return True
            return self.errorManage(self.block)		##El unico errorMessage no funciona
    
    def elifList(self,parent=None):   ##It could be empty, so it has a FOLLOW list
        if self._elif(parent):
            if self.elifList(parent):
                return True
        elif self.verifyFollows(flws.elifList):  #ID 
            return True
        if self.errorManage(self.block):		##El unico errorMessage no funciona aun
            if self.elifList(parent):
                return True
    
    def _elif(self,parent=None):
        if self.check_term("elif"):
            newNode=Node("elif",parent)
            parent=newNode
            if self.expr(parent):
                if self.check_term(":"):
                    if self.block(parent):
                        return True
            return self.errorManage(self.block)	#Da error No porque puede ser un follow	##El unico errorMessage no funciona aun
    
    def _else(self,parent=None):    ##It could be empty, so it has a FOLLOW list
        if self.check_term("else"):
            newNode=Node("else",parent)
            parent=newNode
            if self.check_term(":"):
                if self.block(parent):
                    return True
        
        elif self.verifyFollows(flws._else):
            return True

        return self.errorManage(self.block)		##El unico errorMessage no funciona aun
    
    def simpleStmt(self,parent=None):
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
            
    
    def ssTail(self,parent=None):       ##It could be empty, so it has a FOLLOW list
        if self.check_term("="):
            newNode=Node("=")
            if(parent!=None and parent.children.__len__()>0):
                newNode.children=[parent.children[parent.children.__len__()-1]]
            newNode.parent=parent
            parent=newNode
            if self.expr(parent):
                return True
        
        elif self.verifyFollows(flws.ssTail):
            return True

    def returnExpr(self,parent=None):      ##It could be empty, so it has a FOLLOW list
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
                         newTree.children[0].parent=parent
                    else:
                        newTree.parent = parent
                return True
    
    def exprPrime(self,parent=None):      ##It could be empty, so it has a FOLLOW list
        if self.check_term("if"):
            p=parent
            newNode=Node("if",parent)
            parent=newNode
            if self.andExpr(parent):
                if self.check_term("else"):
                    newNode=Node("else",parent)
                    tempParent=newNode
                    if self.andExpr(tempParent):
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
            
    def orExprPrime(self,parent=None):    ##It could be empty, so it has a FOLLOW list
        if self.check_term("or"):
            newNode=Node("or")
            if(parent!=None and parent.children.__len__()>0):
                newNode.children=[parent.children[parent.children.__len__()-1]]
            newNode.parent=parent
            parent=newNode
            if self.andExpr(parent):
                if self.orExprPrime(parent):
                    return True
                
        elif self.verifyFollows(flws.orExprPrime):
            return True
    
    def andExpr(self,parent=None):
        if self.notExpr(parent):
            if self.andExprPrime(parent):
                return True
            
    def andExprPrime(self,parent=None):            ##It could be empty, so it has a FOLLOW list
        if self.check_term("and"):
            newNode=Node("and")
            if(parent!=None and parent.children.__len__()>0):
                newNode.children=[parent.children[parent.children.__len__()-1]]
            newNode.parent=parent
            parent=newNode
            if self.notExpr(parent):
                if self.andExprPrime(parent):
                    return True
        
        elif self.verifyFollows(flws.andExprPrime):
            return True
                
    def notExpr(self,parent=None):
        if self.compExpr(parent):
            if self.notExprPrime(parent):
                return True
            
    def notExprPrime(self,parent=None):       ##It could be empty, so it has a FOLLOW list
        if self.check_term("not"):
            newNode=Node("not",parent)  
            parentTemp=newNode          
            if self.compExpr(parentTemp):
                if self.notExprPrime(parent):
                    return True
        
        elif self.verifyFollows(flws.notExprPrime):
            return True
        
    def compExpr(self,parent=None):
        if self.intExpr(parent):
            if self.compExprPrime(parent):
                return True
            
    def compExprPrime(self,parent=None):         ##It could be empty, so it has a FOLLOW list
        if self.compOp():
            newNode=Node(self.cur_token.name)
            if(parent!=None and parent.children.__len__()>0):
                newNode.children=[parent.children[parent.children.__len__()-1]]
            newNode.parent=parent
            parentTemp=newNode
            if self.intExpr(parentTemp):
                if self.compExprPrime(parent):
                    return True
                
        elif self.verifyFollows(flws.compExprPrime):
            return True

    def intExpr(self,parent=None):
        if self.term(parent):
            if self.intExprPrime(parent):
                return True

    def intExprPrime(self,parent=None):     ##It could be empty, so it has a FOLLOW list
        if self.check_term("+") or self.check_term("-"):
            if(parent!=None):
                newNode=Node(self.cur_token.name)
                newNode.children=parent.children
                newNode.parent=parent
                parent=newNode
            if self.term(parent):
                if self.intExprPrime(parent):
                    return True
                
        elif self.verifyFollows(flws.intExprPrime):
            return True
                
    def term(self,parent=None):
        if self.factor(parent):
            if self.termPrime(parent):
                return True
    
    def termPrime(self,parent=None):        ##It could be empty, so it has a FOLLOW list
        if self.check_term("*") or self.check_term("//") or self.check_term("%"):
            if(parent!=None):
                newNode=Node(self.cur_token.name)
                newNode.children=parent.children
                newNode.parent=parent
                parent=newNode
            if self.factor(parent):
                if self.termPrime(parent):
                    return True
            
        elif self.verifyFollows(flws.termPrime):
            return True
    
    def factor(self,parent=None):
        if self.name(parent) or self.literal(parent) or self._list(parent):
            return True
        if self.check_term("-"):
            newNode=Node("-",parent)
            if self.factor(parent):
                return True
        if self.check_term("("):
            if self.expr(parent):
                if self.check_term(")"):
                    return True
    
    def name(self,parent=None):
        if self.check_term("ID"):
            newNode=Node(self.cur_token.name,parent)
            if self.nameTail(parent):   
                return True
    
    def nameTail(self,parent=None):         ##It could be empty, so it has a FOLLOW list
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
        if self.check_term("["):
            newNode=Node("[",parent)
            if self.exprList(parent):
                if self.check_term("]"):
                    newNode=Node("]",parent)
                    return True
    def exprList(self,parent=None):     ##It could be empty, so it has a FOLLOW list
        if self.expr(parent):
            if self.exprListTail(parent):
                return True
        
        elif self.verifyFollows(flws.exprList):
            return True
    
    def exprListTail(self,parent=None):     ##It could be empty, so it has a FOLLOW list
        if self.check_term(","):
            if self.expr(parent):
                if self.exprListTail(parent):
                    return True
        
        elif self.verifyFollows(flws.exprListTail):
            return True
                
    def compOp(self,parent=None):
        if self.check_term("==") or self.check_term("!=") or self.check_term("<") or self.check_term(">") or self.check_term("<=") or self.check_term(">=") or self.check_term("is"):
            return True
        
    def __del__(self):
        self.treeFile.close()
        print("PARSING COMPLETED WITH", self.n_errors, "ERRORS")
    
    
    

    
                   