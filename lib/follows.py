#All the needed non-terminal's follows in a hash table

defList=dict.fromkeys(["$","if","while","for","pass","return","-","(","ID","None","True","False","INTEGER","STRING","["],True)
typedVarList=dict.fromkeys([")"],True)
typedVarListTail=dict.fromkeys([")"],True)
_return=dict.fromkeys([":"],True)        
stmtList=dict.fromkeys(["$","DEDENT"],True)    
elifList=dict.fromkeys(["$","if","while","for","pass","return","-","(","ID","None","True","False","INTEGER","STRING","[","def","DEDENT","else","elif"],True)
_else=dict.fromkeys(["$","if","while","for","pass","return","-","(","ID","None","True","False","INTEGER","STRING","[","def","DEDENT","elif","else"],True)
ssTail=dict.fromkeys(["NEWLINE"],True)
returnExpr=dict.fromkeys(["NEWLINE"],True)
exprPrime=dict.fromkeys([":","NEWLINE","=",")","]",","],True)
orExprPrime=dict.fromkeys(["if",":","NEWLINE","=",")","]",","],True)
andExprPrime=dict.fromkeys(["else","if",":","NEWLINE","=","or",")","]",","],True)
notExprPrime=dict.fromkeys(["and","else","if",":","NEWLINE","=","or",")","]",","],True)
compExprPrime=dict.fromkeys(["not","and","else","if",":","NEWLINE","=","or",")","]",","],True)
intExprPrime=dict.fromkeys(["not","and","else","if",":","NEWLINE","=","or","==","!=","<",">","<=",">=","is",")","]",","],True)
termPrime=dict.fromkeys(["+","-","not","and","else","if",":","NEWLINE","=","or","==","!=","<",">","<=",">=","is",")","]",","],True)
nameTail=dict.fromkeys(["*","//","%","+","-","not","and","else","if",":","NEWLINE","=","or","==","!=","<",">","<=",">=","is",")","]",","],True)
exprList=dict.fromkeys([")","]"],True)
exprListTail=dict.fromkeys([")","]"],True)

