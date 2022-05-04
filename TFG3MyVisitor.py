from this import d
from tokenize import String
from antlr4 import *
from MyExceptions import *

from dist.TrabalhoFinalG3Parser import TrabalhoFinalG3Parser
from dist.TrabalhoFinalG3Visitor import TrabalhoFinalG3Visitor

global_variables = {}
flag_break = []
lines = []


def transform_var(declaration, var):
    operation = {
        'int': lambda: int(var),
        'float': lambda: float(var),
        'string': lambda: str(var),
        'boolean': lambda: bool(var) if var == 'True' else False
    }

    return operation.get(declaration, lambda: None)()


def parse_attrib(declaration_type, declaration):
    first_split = declaration.split(',')

    for aux in first_split:
        key = aux.split('=')[0]
        value = aux.split('=')[1]

        check_var(key)
        if('"' in value):
            global_variables.update({key: value.replace('"', "")})
        else:
            global_variables.update(
                {key: transform_var(declaration_type, value)})


def parse_var(declaration_type, declaration):
    first_split = declaration.split(',')

    for aux in first_split:
        check_var(aux)
        global_variables.update({aux: declaration_type})


def parse_number(value):
    if value.isdigit():
        number = int(value)
    else:
        number = float(value)

    return number


def update_var(var, new_value):
    global_variables.update({var: new_value})


def check_var(var):
    if(global_variables.__contains__(var)):
        raise DeclarationError(f"Variavel '{var}' ja declarada.")


class TFG3MyVisitor(TrabalhoFinalG3Visitor):
    def visitProg(self, ctx):
        lines.append(".class TrabalhoFinal\n.super java/lang/Object\n")

        for declaration in ctx.var_declaration():
            self.visit(declaration)

        for func_declaration in ctx.func_declaration():
            self.visit(ctx.func_declaration())

        self.visit(ctx.main_block())

    def visitDeclarations(self, ctx: TrabalhoFinalG3Parser.DeclarationsContext):
        declaration_type = ctx.type_decl.getText()

        if(ctx.var):
            parse_var(declaration_type, ctx.var.getText())
        if(ctx.attrib):
            parse_attrib(declaration_type, ctx.attrib.getText())

    def visitMain_block(self, ctx):
        lines.append(
            f".method public static main([Ljava/lang/String;)V\n.limit stack 10\n.limit locals {len(global_variables)}\n")

        for stats in ctx.stats():
            self.visit(stats)

        lines.append("return\n.end method")
        with open('TrabalhoFinal.j', 'w+') as writer:
            writer.writelines(lines)
            writer.close()

    def visitAttribCommand(self, ctx: TrabalhoFinalG3Parser.AttribCommandContext):
        v = ctx.var.text

        if(not global_variables.__contains__(v)):
            raise DeclarationError(f"Variavel '{v}' nao declarada.")

        result = self.visit(ctx.op)
        update_var(v, result)

        aux = list(global_variables)
        lines.append(f"istore {aux.index(v)}")  

    def visitIfCommand(self, ctx: TrabalhoFinalG3Parser.IfCommandContext):
        condition = ctx.condition_block()
        evaluated_block = False

        if(str(type(condition.op)).find('Logic') != -1):
            evaluated = self.visit(condition.op)
            if(evaluated):
                evaluated_block = True
                self.visit(condition.stmt)

            if(not evaluated_block and ctx.stmt != None):
                self.visit(ctx.stmt)

            return evaluated
        else:
            raise OperationError(
                f"Operacao '{condition.op.getText()}' invalida para um condicional")

    def visitForCommand(self, ctx: TrabalhoFinalG3Parser.ForCommandContext):
        range_values = self.visit(ctx.rang)
        var = ctx.var.text

        for i in range(range_values[0], range_values[1], range_values[2]):
            update_var(var, i)
            self.visit(ctx.stmt)

            if(len(flag_break) == 1):
                flag_break.pop()
                break

    def visitRangeCommand(self, ctx: TrabalhoFinalG3Parser.RangeCommandContext):
        aux = []
        range_values = []

        for x in ctx.NUMBER():
            aux.append(parse_number(x.getText()))

        if(len(aux) == 1):
            range_values.append(0)
            range_values.append(aux[0])
            range_values.append(1)
        elif(len(aux) == 2):
            range_values.append(aux[0])
            range_values.append(aux[1])
            range_values.append(1)
        elif(len(aux) == 3):
            range_values.append(aux[0])
            range_values.append(aux[1])
            range_values.append(aux[2])

        return range_values

    def visitWhileCommand(self, ctx: TrabalhoFinalG3Parser.WhileCommandContext):
        if(str(type(ctx.op)).find('Logic') != -1):
            op = self.visit(ctx.op)

            while(op):
                self.visit(ctx.stmt)
                op = self.visit(ctx.op)

                if(len(flag_break) == 1):
                    flag_break.pop()
                    break
        else:
            raise OperationError(
                f"Operacao '{ctx.op.getText()}' invalida para um condicional")

    def visitPrintCommand(self, ctx: TrabalhoFinalG3Parser.PrintCommandContext):
        result1 = self.visit(ctx.op1)

        if(ctx.op2):
            result2 = self.visit(ctx.op2)
            print(result1, result2)
        else:
            print(result1)

    def visitInputCommand(self, ctx: TrabalhoFinalG3Parser.InputCommandContext):
        var = ctx.var.text
        parse = input()

        check = parse.isdigit()
        result = parse_number(parse) if(check) else parse

        update_var(var, result)

    def visitBreakCommand(self, ctx: TrabalhoFinalG3Parser.BreakCommandContext):
        flag_break.append(1)

    def visitNotExp(self, ctx: TrabalhoFinalG3Parser.NotExpContext):
        op = self.visit(ctx.op)
        result = not op

        return result

    def visitUnaryExp(self, ctx: TrabalhoFinalG3Parser.UnaryExpContext):
        op = self.visit(ctx.op)
        result = -op

        return result

    def visitInfixExp(self, ctx: TrabalhoFinalG3Parser.InfixExpContext):
        l = self.visit(ctx.left)
        r = self.visit(ctx.right)
        op = ctx.op.text

        if((type(l) != str and type(r) != str) and (type(l) != bool and type(r) != bool)):
            if(op == '+' and (type(l) == int and type(r) == int)):
                lines.append(f"ldc {l}\nldc {r}\niadd")
                return l + r
            elif(op == '-'):
                return l - r
            elif(op == '*'):
                return l * r
            elif(op == '/'):
                return l / r

            """ operation = {
                '+': lambda: l + r,
                '-': lambda: l - r,
                '*': lambda: l * r,
                '/': lambda: l / r,
            }
            return operation.get(op, lambda: None)() """
        elif(type(l) == str and type(r) == str and op == '+'):
            return l + r
        else:
            raise TypeError(
                f"Erro - tentando operar {str(type(l)).split()[1].replace('>', '')} com {str(type(r)).split()[1].replace('>', '')}")

    def visitLogicExp(self, ctx: TrabalhoFinalG3Parser.LogicExpContext):
        l = self.visit(ctx.left)
        r = self.visit(ctx.right)
        op = ctx.op.text

        operation = {
            '>': lambda: l > r,
            '>=': lambda: l >= r,
            '<': lambda: l < r,
            '<=': lambda: l <= r,
            '==': lambda: l == r,
            '!=': lambda: l != r,
            'and': lambda: l and r,
            'or': lambda: l or r,
        }
        result = operation.get(op, lambda: None)()

        return result

    def visitParenExp(self, ctx: TrabalhoFinalG3Parser.ParenExpContext):
        return self.visit(ctx.op)

    def visitIdExp(self, ctx: TrabalhoFinalG3Parser.IdExpContext):
        for key, val in global_variables.items():
            if ctx.atom.text == key:
                return val

    def visitNumberExp(self, ctx: TrabalhoFinalG3Parser.NumberExpContext):
        return parse_number(ctx.atom.text)

    def visitStringExp(self, ctx: TrabalhoFinalG3Parser.StringExpContext):
        return ctx.atom.text.replace('"', "")

    def visitBooleanExp(self, ctx: TrabalhoFinalG3Parser.BooleanExpContext):
        return True if (ctx.atom.text == 'True') else False
