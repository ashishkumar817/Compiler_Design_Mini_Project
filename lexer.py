import re

def lexical_analysis(code):
    token_specification = [
        ('KEYWORD', r'\b(int|begin|for|to|do|if|endif|endfor|return|End)\b'),
        ('NUMBER', r'\d+'),
        ('IDENTIFIER', r'[A-Za-z_]\w*'),
        ('OPERATOR', r'==|>|=|-'),
        ('DELIMITER', r'[\[\]\(\);]'),
        ('SKIP', r'[ \t\n]+'),
        ('MISMATCH', r'.'),
    ]

    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)

    tokens = []
    symbol_table = {
        "IDENTIFIER": set(),
        "NUMBER": set()
    }

    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()

        if kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'Unexpected token: {value}')

        tokens.append((kind, value))

        if kind == "IDENTIFIER":
            symbol_table["IDENTIFIER"].add(value)
        elif kind == "NUMBER":
            symbol_table["NUMBER"].add(value)

    return tokens, symbol_table
