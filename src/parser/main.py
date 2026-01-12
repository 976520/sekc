import sys
import json


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        statements = []
        while not self.is_at_end():
            while self.match("Newline"): pass
            if self.is_at_end(): break
            statements.append(self.statement())
            while self.match("Newline"): pass
        return {"statements": statements}

    def statement(self):
        if self.match("Keyword", "set"): return self.set_stmt()
        if self.match("Keyword", "define"): return self.func_def()
        if self.match("Keyword", "if"): return self.if_stmt()
        if self.match("Keyword", "repeat"): return self.repeat_stmt()
        if self.match("Keyword", "break"): 
            self.consume("Newline", "Expect newline after break")
            return {"class": "FlowStmt", "type": "break", "value": None}
        if self.match("Keyword", "continue"): 
             self.consume("Newline", "Expect newline after continue")
             return {"class": "FlowStmt", "type": "continue", "value": None}
        
        if self.match("Keyword", "print"):
            expr = self.expression()
            return {"class": "PrintStmt", "expr": expr}
        
        if self.match("Keyword", "read"):
            self.consume("Keyword", "input")
            self.consume("Keyword", "into")
            target = self.consume("Identifier", "Expect variable for read")
            return {"class": "ReadStmt", "target": target['value']}

        if self.match("Keyword", "return"):
            expr = None
            if not self.check("Newline"): expr = self.expression()
            return {"class": "FlowStmt", "type": "return", "value": expr}

        if self.check("Identifier") and self.peek_next() and self.peek_next()['value'] == "=>":
            return self.bind_stmt()

        raise Exception(f"Unexpected token {self.peek()}")

    def set_stmt(self):
        expr = self.expression()
        self.consume("Keyword", "in")
        target = self.consume("Identifier", "Expect target")
        return {"class": "SetStmt", "expr": expr, "target": target['value']}

    def bind_stmt(self):
        name = self.consume("Identifier")
        self.consume("Symbol", "=>")
        expr = self.expression()
        return {"class": "BindStmt", "name": name['value'], "expr": expr}
    
    def if_stmt(self):
        cond = self.expression()
        self.match("Newline")
        self.consume("Indent", "Expect indent")
        then_block = self.block()
        return {"class": "IfStmt", "condition": cond, "thenBlock": then_block, "elseBlock": None}

    def repeat_stmt(self):
        if self.match("Keyword", "while"):
            cond = self.expression()
            self.match("Newline")
            self.consume("Indent", "Expect indent")
            body = self.block()
            return {"class": "LoopStmt", "type": "while", "condition": cond, "block": body}
        raise Exception("Unknown repeat type")

    def func_def(self):
        name = self.consume("Identifier")
        self.consume("Symbol", "(")
        params = []
        if not self.check("Symbol", ")"):
            while True:
                p = self.consume("Identifier")
                params.append(p['value'])
                if not self.match("Symbol", ","): break
        self.consume("Symbol", ")")
        
        if self.match("Symbol", "=>"):
            expr = self.expression()
            body = [{"class": "FlowStmt", "type": "return", "value": expr}]
            return {"class": "FuncDef", "name": name['value'], "params": params, "body": body}
        
        self.match("Newline")
        self.consume("Indent", "Expect indent")
        body = self.block()
        return {"class": "FuncDef", "name": name['value'], "params": params, "body": body}

    def block(self):
        stmts = []
        while not self.check("Dedent") and not self.is_at_end():
            if self.match("Newline"): continue
            stmts.append(self.statement())
        self.consume("Dedent", "Expect dedent")
        return stmts

    def expression(self):
        return self.logic_or()

    def logic_or(self):
        expr = self.logic_and()
        while self.match("Keyword", "or"):
            right = self.logic_and()
            expr = {"class": "BinaryExpr", "left": expr, "op": "or", "right": right}
        return expr

    def logic_and(self):
        expr = self.equality()
        while self.match("Keyword", "and"):
            right = self.equality()
            expr = {"class": "BinaryExpr", "left": expr, "op": "and", "right": right}
        return expr

    def equality(self):
        expr = self.comparison()
        if self.match("Keyword", "is"):
            op = "is"
            if self.match("Keyword", "not"): op = "is_not"
            right = self.comparison()
            expr = {"class": "BinaryExpr", "left": expr, "op": op, "right": right}
        return expr

    def comparison(self):
        return self.term()

    def term(self):
        expr = self.factor()
        while self.check("Symbol", "+") or self.check("Symbol", "-"):
            op = self.advance()['value']
            right = self.factor()
            expr = {"class": "BinaryExpr", "left": expr, "op": op, "right": right}
        return expr

    def factor(self):
        expr = self.primary()
        while self.match("Symbol", "->"):
             right = self.primary()
             expr = {"class": "PipeExpr", "start": expr, "pipe": right}
        return expr

    def primary(self):
        if self.match("Number"): return {"class": "Literal", "value": self.previous()['value']}
        if self.match("String"): return {"class": "Literal", "value": self.previous()['value']}
        if self.match("Keyword", "true"): return {"class": "Literal", "value": True}
        if self.match("Keyword", "false"): return {"class": "Literal", "value": False}
        if self.match("Keyword", "null"): return {"class": "Literal", "value": None}
        
        if self.match("Identifier"):
            name = self.previous()['value']
            if self.match("Symbol", "("):
                args = []
                if not self.check("Symbol", ")"):
                    while True:
                        args.append(self.expression())
                        if not self.match("Symbol", ","): break
                self.consume("Symbol", ")")
                return {"class": "FuncCall", "name": name, "args": args}
            return {"class": "Identifier", "name": name}

        raise Exception(f"Unknown primary {self.peek()}")

    def match(self, type_name, value=None):
        if self.check(type_name, value):
            self.advance()
            return True
        return False

    def check(self, type_name, value=None):
        if self.is_at_end(): return False
        t = self.peek()
        if t['type'] != type_name: return False
        if value is not None and t['value'] != value: return False
        return True

    def consume(self, type_name, msg="Error"):
        if self.check(type_name): return self.advance()
        raise Exception(f"{msg}: Found {self.peek()}")

    def advance(self):
        if not self.is_at_end(): self.current += 1
        return self.previous()

    def is_at_end(self):
        return self.peek()['type'] == 'EOF'

    def peek(self):
        return self.tokens[self.current]

    def peek_next(self):
        if self.current + 1 < len(self.tokens): return self.tokens[self.current + 1]
        return None

    def previous(self):
        return self.tokens[self.current - 1]

def main():
    try:
        data = sys.stdin.read()
        if not data: return
        tokens = json.loads(data)
        parser = Parser(tokens)
        ast = parser.parse()
        print(json.dumps(ast))
    except Exception as e:
        sys.stderr.write(f"Parser Error: {str(e)}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
