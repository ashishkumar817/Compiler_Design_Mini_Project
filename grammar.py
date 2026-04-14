# Grammar Rules
grammar = {
    "program": ["int main ( ) begin stmt_list End"],
    "stmt_list": ["stmt stmt_list", "ε"],
    "stmt": ["declaration", "assignment", "for_loop", "if_stmt", "return_stmt"],
    "declaration": ["int IDENTIFIER [ NUMBER ] ;", "int IDENTIFIER = expr ;"],
    "assignment": ["IDENTIFIER = expr ;"],
    "for_loop": ["for IDENTIFIER = expr to expr do stmt_list endfor"],
    "if_stmt": ["if condition stmt_list endif"],
    "return_stmt": ["return ( expr )"],
    "condition": ["expr > expr"],
    "expr": ["IDENTIFIER", "NUMBER", "IDENTIFIER [ expr ]", "expr - expr"]
}

# FIRST sets
first_sets = {
    "program": {"int"},
    "stmt_list": {"int", "IDENTIFIER", "for", "if", "return", "ε"},
    "stmt": {"int", "IDENTIFIER", "for", "if", "return"},
    "declaration": {"int"},
    "assignment": {"IDENTIFIER"},
    "for_loop": {"for"},
    "if_stmt": {"if"},
    "return_stmt": {"return"},
    "condition": {"IDENTIFIER", "NUMBER"},
    "expr": {"IDENTIFIER", "NUMBER"}
}

# FOLLOW sets
follow_sets = {
    "program": {"$"},
    "stmt_list": {"End", "endfor", "endif"},
    "stmt": {"int", "IDENTIFIER", "for", "if", "return", "End", "endfor", "endif"},
    "declaration": {"int", "IDENTIFIER", "for", "if", "return", "End", "endfor", "endif"},
    "assignment": {"int", "IDENTIFIER", "for", "if", "return", "End", "endfor", "endif"},
    "for_loop": {"int", "IDENTIFIER", "for", "if", "return", "End", "endfor", "endif"},
    "if_stmt": {"int", "IDENTIFIER", "for", "if", "return", "End", "endfor", "endif"},
    "return_stmt": {"int", "IDENTIFIER", "for", "if", "return", "End", "endfor", "endif"},
    "condition": {"int", "IDENTIFIER", "for", "if", "return", "endif"},
    "expr": {";", ")", ">", "to", "do", "]", "-", "int", "IDENTIFIER", "for", "if", "return", "endif"}
}

# Parsing Table (Comprehensive)
parsing_table = [
    ["Non-Terminal", "int", "IDENTIFIER", "for", "if", "return", "NUMBER", "End", "endif", "endfor"],
    ["program", "int main( )...", "-", "-", "-", "-", "-", "-", "-", "-"],
    ["stmt_list", "stmt stmt_list", "stmt stmt_list", "stmt stmt_list", "stmt stmt_list", "stmt stmt_list", "-", "ε", "ε", "ε"],
    ["stmt", "declaration", "assignment", "for_loop", "if_stmt", "return_stmt", "-", "-", "-", "-"],
    ["declaration", "int ID...", "-", "-", "-", "-", "-", "-", "-", "-"],
    ["assignment", "-", "ID = expr ;", "-", "-", "-", "-", "-", "-", "-"],
    ["for_loop", "-", "-", "for ID...", "-", "-", "-", "-", "-", "-"],
    ["if_stmt", "-", "-", "-", "if cond...", "-", "-", "-", "-", "-"],
    ["return_stmt", "-", "-", "-", "-", "return...", "-", "-", "-", "-"],
    ["condition", "-", "expr > expr", "-", "-", "-", "expr > expr", "-", "-", "-"],
    ["expr", "-", "ID / ID[expr]", "-", "-", "-", "NUMBER", "-", "-", "-"]
]
