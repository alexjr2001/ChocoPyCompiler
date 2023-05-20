grammar = """
Program ->  DefList StatementList
DefList ->  Def DefList 
DefList ->  ''
Def ->  def ID ( TypedVarList ) Return : Block
TypedVar ->  ID : Type
Type ->  int
Type ->  str
Type ->  [ Type ]
TypedVarList ->  ''
TypedVarList ->  TypedVar TypedVarListTail
TypedVarListTail ->  , TypedVar TypedVarListTail
TypedVarListTail ->  ''
Return ->  ''
Return ->  -> Type
Block ->  NEWLINE INDENT Statement StatementList DEDENT
StatementList ->  Statement StatementList
StatementList ->  ''
Statement ->  SimpleStatement NEWLINE
Statement ->  if Expr : Block ElifList Else
Statement ->  while Expr : Block
Statement ->  for ID in Expr : Block
ElifList ->  Elif ElifList
ElifList ->  ''
Elif ->  elif Expr : Block
Else ->  ''
Else ->  else : Block
SimpleStatement ->  Expr SSTail
SSTail ->  ''
SSTail ->  = Expr
SimpleStatement ->  pass
SimpleStatement ->  return ReturnExpr
ReturnExpr ->  Expr
ReturnExpr -> ''
Expr ->  OrExpr ExprPrime
ExprPrime ->   if AndExpr else AndExpr ExprPrime
ExprPrime ->  ''
OrExpr ->  AndExpr OrExprPrime
OrExprPrime ->  or AndExpr OrExprPrime
OrExprPrime ->  ''
AndExpr -> NotExpr AndExprPrime
AndExprPrime ->   and NotExpr AndExprPrime
AndExprPrime ->  ''
NotExpr -> CompExpr NotExprPrime
NotExprPrime ->   not CompExpr NotExprPrime
NotExprPrime ->  ''
CompExpr ->  IntExpr CompExprPrime
CompExprPrime ->   CompOp IntExpr CompExprPrime
CompExprPrime ->  ''
IntExpr ->  Term IntExprPrime
IntExprPrime ->   + Term IntExprPrime
IntExprPrime ->   - Term IntExprPrime
IntExprPrime ->  ''
Term ->  Factor TermPrime
TermPrime ->   * Factor TermPrime
TermPrime ->   // Factor TermPrime
TermPrime ->   % Factor TermPrime
TermPrime ->  ''
Factor ->  - Factor
Factor ->  Name
Factor ->  Literal
Factor ->  List
Factor ->  ( Expr )
Name ->  ID NameTail
NameTail ->  ''
NameTail ->  ( ExprList )
NameTail ->  List
Literal ->  None
Literal ->  True
Literal ->  False
Literal ->  INTEGER
Literal ->  STRING
List ->  [ ExprList ]
ExprList ->  ''
ExprList ->  Expr ExprListTail
ExprListTail ->  ''
ExprListTail ->  , Expr ExprListTail
CompOp ->  == 
CompOp ->  != 
CompOp ->  < 
CompOp ->  > 
CompOp ->  <= 
CompOp ->  >= 
CompOp ->  is
"""