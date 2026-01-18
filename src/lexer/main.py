import sys
import json
# import re

tokens = []
indent_stack = [0]
line_num = 1

KEYWORDS = {
    "set", "in", "is", "define", "if", "else", "repeat", "while", "until", 
    "break", "continue", "return", "and", "or", "not", "true", "false", "null",
    "print", "read", "input", "into"
}


def peek(s, i, offset=0):
    if i + offset < len(s): return s[i + offset]
    return None


def main():
    global line_num
    try:
        source = sys.stdin.read()
    except:
        return

    i = 0
    length = len(source)
    at_line_start = True

    while i < length:
        c = source[i]

        if at_line_start:
            if c == ' ' or c == '\t':
                indent = 0
                temp_i = i
                while temp_i < length:
                    if source[temp_i] == ' ': indent += 1
                    elif source[temp_i] == '\t': indent += 4
                    else: break
                    temp_i += 1

                next_char = peek(source, temp_i)
                if next_char == '\n':
                    i = temp_i + 1
                    line_num += 1
                    continue
                elif next_char is None:
                    i = temp_i
                    break
                
                current_indent = indent_stack[-1]
                if indent > current_indent:
                    indent_stack.append(indent)
                    tokens.append({"type": "Indent", "value": None, "line": line_num})
                elif indent < current_indent:
                    while indent < indent_stack[-1]:
                        indent_stack.pop()
                        tokens.append({"type": "Dedent", "value": None, "line": line_num})
                
                i = temp_i
                at_line_start = False
                continue

            elif c == '\n':
                i += 1
                line_num += 1
                continue
            else:
                while indent_stack[-1] > 0:
                    indent_stack.pop()
                    tokens.append({"type": "Dedent", "value": None, "line": line_num})
                at_line_start = False

        if c in ' \t\r':
            i += 1
        elif c == '\n':
            tokens.append({"type": "Newline", "value": None, "line": line_num})
            line_num += 1
            at_line_start = True
            i += 1
        
        elif c == '"':
            i += 1
            start = i
            while i < length and source[i] != '"':
                i += 1
            tokens.append({"type": "String", "value": source[start:i], "line": line_num})
            i += 1
            
        elif c.isdigit():
            start = i
            while i < length and (source[i].isdigit() or source[i] == '.'):
                i += 1
            tokens.append({"type": "Number", "value": float(source[start:i]), "line": line_num})
            
        elif c.isalpha() or c == '_':
            start = i
            while i < length and (source[i].isalnum() or source[i] == '_'):
                i += 1
            text = source[start:i]
            if text in KEYWORDS:
                 tokens.append({"type": "Keyword", "value": text, "line": line_num})
            else:
                 tokens.append({"type": "Identifier", "value": text, "line": line_num})
                 
        elif c == '-' and peek(source, i, 1) == '>':
            tokens.append({"type": "Symbol", "value": "->", "line": line_num})
            i += 2
        elif c == '=' and peek(source, i, 1) == '>':
            tokens.append({"type": "Symbol", "value": "=>", "line": line_num})
            i += 2
        else:
            tokens.append({"type": "Symbol", "value": c, "line": line_num})
            i += 1

    tokens.append({"type": "Newline", "value": None, "line": line_num})
    while indent_stack[-1] > 0:
        indent_stack.pop()
        tokens.append({"type": "Dedent", "value": None, "line": line_num})
    tokens.append({"type": "EOF", "value": None, "line": line_num})

    print(json.dumps(tokens))

if __name__ == "__main__":
    main()
