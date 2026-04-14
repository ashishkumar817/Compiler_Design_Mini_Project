from lexer import lexical_analysis
from myparser import parse
from grammar import grammar, first_sets, follow_sets, parsing_table
from tabulate import tabulate

# Read input
with open("input.txt", "r") as file:
    code = file.read()

# =========================
# LEXICAL ANALYSIS
# =========================
tokens, symbol_table = lexical_analysis(code)

# =========================
# SOURCE CODE DISPLAY
# =========================
print("\n===== SOURCE CODE =====\n")

with open("input.txt", "r") as file:
    lines = file.readlines()

for i, line in enumerate(lines, start=1):
    print(f"{i:>2} {line.rstrip()}")

# TOKEN TABLE
print("\n===== TOKEN TABLE =====")

unique_tokens = []
seen = {}
token_id = 1

for t in tokens:
    key = (t[0], t[1])  # (Type, Lexeme)

    if key not in seen:
        seen[key] = token_id
        unique_tokens.append([t[0], t[1], token_id])
        token_id += 1

# Print table
print(tabulate(unique_tokens, headers=["Type", "Lexeme", "Token ID"], tablefmt="fancy_grid"))
# =========================
# SYMBOL TABLE
# =========================
print("\n===== SYMBOL TABLE =====")

id_table = [[i] for i in symbol_table["IDENTIFIER"]]
num_table = [[n] for n in symbol_table["NUMBER"]]

print("\nIdentifiers:")
print(tabulate(id_table, headers=["Identifier"], tablefmt="fancy_grid"))

print("\nNumbers:") 
print(tabulate(num_table, headers=["Number"], tablefmt="fancy_grid"))

# =========================
# GRAMMAR TABLE
# =========================
print("\n===== GRAMMAR =====")

grammar_table = []
for nt, rules in grammar.items():
    for r in rules:
        grammar_table.append([nt, r])

print(tabulate(grammar_table, headers=["Non-Terminal", "Production"], tablefmt="fancy_grid"))

# =========================
# FIRST SETS
# =========================
print("\n===== FIRST SET =====")

first_table = [[nt, ", ".join(fs)] for nt, fs in first_sets.items()]
print(tabulate(first_table, headers=["Non-Terminal", "First Set"], tablefmt="fancy_grid"))

# =========================
# FOLLOW SETS
# =========================
print("\n===== FOLLOW SET =====")

follow_table = [[nt, ", ".join(fs)] for nt, fs in follow_sets.items()]
print(tabulate(follow_table, headers=["Non-Terminal", "Follow Set"], tablefmt="fancy_grid"))

# =========================
# PARSING TABLE
# =========================
print("\n===== PARSING TABLE =====")

print(tabulate(parsing_table[1:], headers=parsing_table[0], tablefmt="fancy_grid"))

# =========================
# PARSER
# =========================
print("\n===== PARSING ACTIONS =====")

result, steps = parse(tokens)

from tabulate import tabulate
print(tabulate(steps, headers=["Step", "Stack", "Input Symbol", "Action"], tablefmt="fancy_grid"))

print("\n===== FINAL RESULT =====")
print(result)