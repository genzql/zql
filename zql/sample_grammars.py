from zql.grammar import parse_grammar


FORMULA_GRAMMAR_CONTENT = r"""
    root     : formula
             ;
    formula  : expr operator expr
             | expr
             ;
    expr     : open formula close
             | word
             | number
             ;
    open     : "("
             > "(\n"
             ;
    close    : ")"
             > "\n)"
             ;
    word     : r[a-zA-Z][\w$]*
             ;
    number   : r[0-9]+
             ;
    operator : "+"
             | "-"
             | "*"
             | "/"
             ;
"""
FORMULA_GRAMMAR = parse_grammar(FORMULA_GRAMMAR_CONTENT)


LIST_GRAMMAR_CONTENT = r"""
root     : list
         ;
list     : num_list end
         ;
num_list : num comma num_list
         | num
         ;
num      : r[0-9]+
         ;
comma    : ","
         ;
end      : r[0-9]+
         ;
"""
LIST_GRAMMAR = parse_grammar(LIST_GRAMMAR_CONTENT)


FUNCTION_GRAMMAR_CONTENT = r"""
    root     : function
             ;
    function : arg1 divide arg2
             > "{arg1}\n---------------------\n{arg2}"
             | arg1 operator arg2
             > "{operator}({arg1}, {arg2})"
             | expr
             ;
    arg1     : expr
             ;
    arg2     : expr
             ;
    expr     : open function close
             > "{function}"
             | word
             | number
             ;
    open     : "("
             ;
    close    : ")"
             ;
    word     : r[a-zA-Z][\w$]*
             ;
    number   : r[0-9]+
             ;
    operator : add
             | subtract
             | multiply
             | divide
             ;
    add      : "+"
             > "add"
             ;
    subtract : "-"
             > "subtract"
             ;
    multiply : "*"
             > "multiply"
             ;
    divide   : "/"
             > "divide"
             ;
"""
FUNCTION_GRAMMAR = parse_grammar(FUNCTION_GRAMMAR_CONTENT)