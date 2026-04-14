def parse(tokens):
    # Create separate copies (VERY IMPORTANT)
    input_tokens = [t[1] for t in tokens] + ["$"]
    token_types = [t[0] for t in tokens] + ["$"]

    stack = ["$", "program"]
    steps = []
    step = 1

    def record(action):
        nonlocal step
        steps.append([
            step,
            " ".join(stack),
            input_tokens[0] if input_tokens else "",
            action
        ])
        step += 1

    record("Start parsing")

    while stack:
        top = stack[-1]
        current = input_tokens[0]
        current_type = token_types[0]

        # =====================
        # MATCH TERMINALS
        # =====================
        if top == current:
            stack.pop()
            input_tokens.pop(0)
            token_types.pop(0)
            record(f"Match '{current}'")

        elif top == "IDENTIFIER" and current_type == "IDENTIFIER":
            stack.pop()
            input_tokens.pop(0)
            token_types.pop(0)
            record("Match IDENTIFIER")

        elif top == "NUMBER" and current_type == "NUMBER":
            stack.pop()
            input_tokens.pop(0)
            token_types.pop(0)
            record("Match NUMBER")

        # =====================
        # NON-TERMINALS
        # =====================

        elif top == "program":
            stack.pop()
            stack.extend(["int", "main", "(", ")", "begin", "stmt_list", "End"][::-1])
            record("Apply: program → int main ( ) begin stmt_list End")

        elif top == "stmt_list":
            stack.pop()
            if current in ["int", "for", "if", "return"] or current_type == "IDENTIFIER":
                stack.extend(["stmt", "stmt_list"][::-1])
                record("Apply: stmt_list → stmt stmt_list")
            else:
                record("Apply: stmt_list → ε")

        elif top == "stmt":
            stack.pop()
            if current == "int":
                stack.append("declaration")
                record("Apply: stmt → declaration")
            elif current == "for":
                stack.append("for_loop")
                record("Apply: stmt → for_loop")
            elif current == "if":
                stack.append("if_stmt")
                record("Apply: stmt → if_stmt")
            elif current == "return":
                stack.append("return_stmt")
                record("Apply: stmt → return_stmt")
            else:
                stack.append("assignment")
                record("Apply: stmt → assignment")

        #  FIXED DECLARATION
        elif top == "declaration":
            stack.pop()

            # Check next symbol after IDENTIFIER
            if len(input_tokens) > 2 and input_tokens[2] == "[":
                stack.extend(["int", "IDENTIFIER", "[", "NUMBER", "]", ";"][::-1])
                record("Apply: declaration → int IDENTIFIER [ NUMBER ] ;")
            else:
                stack.extend(["int", "IDENTIFIER", "=", "expr", ";"][::-1])
                record("Apply: declaration → int IDENTIFIER = expr ;")

        elif top == "assignment":
            stack.pop()
            stack.extend(["IDENTIFIER", "=", "expr", ";"][::-1])
            record("Apply: assignment → IDENTIFIER = expr ;")

        elif top == "for_loop":
            stack.pop()
            stack.extend(["for", "IDENTIFIER", "=", "expr", "to", "expr", "do", "stmt_list", "endfor"][::-1])
            record("Apply: for_loop → for IDENTIFIER = expr to expr do stmt_list endfor")

        elif top == "if_stmt":
            stack.pop()
            stack.extend(["if", "condition", "stmt_list", "endif"][::-1])
            record("Apply: if_stmt → if condition stmt_list endif")

        elif top == "return_stmt":
            stack.pop()
            stack.extend(["return", "(", "expr", ")"][::-1])
            record("Apply: return_stmt → return ( expr )")

        elif top == "condition":
            stack.pop()
            stack.extend(["expr", ">", "expr"][::-1])
            record("Apply: condition → expr > expr")

        elif top == "expr":
            stack.pop()
            if current_type == "IDENTIFIER":
                if len(input_tokens) > 1 and input_tokens[1] == "[":
                    stack.extend(["IDENTIFIER", "[", "expr", "]"][::-1])
                    record("Apply: expr → IDENTIFIER [ expr ]")
                elif len(input_tokens) > 1 and input_tokens[1] == "-":
                    stack.extend(["IDENTIFIER", "-", "expr"][::-1])
                    record("Apply: expr → expr - expr")
                else:
                    stack.append("IDENTIFIER")
                    record("Apply: expr → IDENTIFIER")
            else:
                if len(input_tokens) > 1 and input_tokens[1] == "-":
                    stack.extend(["NUMBER", "-", "expr"][::-1])
                    record("Apply: expr → expr - expr")
                else:
                    stack.append("NUMBER")
                    record("Apply: expr → NUMBER")

        else:
            record("Error")
            return " Parsing Failed", steps

        if top == "$" and current == "$":
             record("Parsing completed successfully")
             break

    return " Parsing Successful", steps