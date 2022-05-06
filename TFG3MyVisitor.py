from this import d
from tokenize import String
from antlr4 import *
from MyExceptions import *

from dist.TrabalhoFinalG3Parser import TrabalhoFinalG3Parser
from dist.TrabalhoFinalG3Visitor import TrabalhoFinalG3Visitor

global_variables = {}
global_funct = {}
flag_break = []
lines = []
label = 0


def transform_var(declaration, var):
    operation = {
        'int': lambda: int(var),
        'float': lambda: float(var),
        'string': lambda: str(var),
        'boolean': lambda: bool(var) if var == 'True' else False
    }

    return operation.get(declaration, lambda: None)()


def parse_var(declaration_type, declaration):
    first_split = declaration.split(',')

    if(len(first_split[0]) != 1):
        for aux in first_split:
            key = aux.split('=')[0]
            value = aux.split('=')[1]

            check_var(key)
            if('"' in value):
                global_variables.update({key: value.replace('"', "")})
            else:
                global_variables.update(
                    {key: transform_var(declaration_type, value)})

                jasmin_var_declaration(key)
    else:
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


def jasmin_var_declaration(key):
    aux = list(global_variables)
    value = global_variables.get(key)

    if(type(value) == int):
        lines.append(f"ldc {value}\nistore {aux.index(key)}\n")
    elif(type(value) == float):
        lines.append(f"ldc {value}\nfstore {aux.index(key)}\n")


def jasmin_var_attribution(key):
    aux = list(global_variables)
    value = global_variables.get(key)

    if(type(value) == int):
        lines.append(f"istore {aux.index(key)}\n")
    elif(type(value) == float):
        lines.append(f"fstore {aux.index(key)}\n")


def jasmin_var_operations(left, right, l, r):
    aux = list(global_variables)

    if(str(type(left)).find('Id') != -1 and str(type(right)).find('Id') != -1):
        if(type(l) == int and type(r) == int):
            lines.append(f"iload {aux.index(left.getText())}\n")
            lines.append(f"iload {aux.index(right.getText())}\n")
        elif(type(l) == float and type(r) == float):
            lines.append(f"fload {aux.index(left.getText())}\n")
            lines.append(f"fload {aux.index(right.getText())}\n")
    elif(str(type(left)).find('Id') != -1):
        if(type(l) == int):
            lines.append(f"iload {aux.index(left.getText())}\n")
        elif(type(l) == float):
            lines.append(f"fload {aux.index(left.getText())}\n")
        lines.append(f"ldc {r}\n")
    elif(str(type(right)).find('Id') != -1):
        if(type(r) == int):
            lines.append(f"iload {aux.index(right.getText())}\n")
        elif(type(r) == float):
            lines.append(f"fload {aux.index(right.getText())}\n")
        lines.append(f"ldc {l}\n")
    else:
        lines.append(f"ldc {l}\n")
        lines.append(f"ldc {r}\n")


def jasmin_print(result):
    lines.append("getstatic java/lang/System/out Ljava/io/PrintStream;\n")

    if(type(result) == int):
        lines.append(
            f"iload {list(global_variables.values()).index(result)}\n")
        lines.append("invokevirtual java/io/PrintStream/println(I)V\n")
    elif(type(result) == float):
        lines.append(
            f"fload {list(global_variables.values()).index(result)}\n")
        lines.append("invokevirtual java/io/PrintStream/println(F)V\n")
    elif(type(result) == str):
        lines.append(f'ldc "{result}"\n')
        lines.append(
            "invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V\n")


def jasmin_logic_operations(op, l, r):
    global label
    label += 1

    if(op == '>'):
        if(type(l) == int and type(r) == int):
            lines.append(f"if_icmpgt L{label}\n")
        elif(type(l) == float and type(r) == float):
            lines.append(f"fcmpl\nifgt L{label}\n")
    elif(op == '>='):
        if(type(l) == int and type(r) == int):
            lines.append(f"if_icmpge L{label}\n")
        elif(type(l) == float and type(r) == float):
            lines.append(f"fcmpl\nifge L{label}\n")
    elif(op == '<'):
        if(type(l) == int and type(r) == int):
            lines.append(f"if_icmplt L{label}\n")
        elif(type(l) == float and type(r) == float):
            lines.append(f"fcmpl\niflt L{label}\n")
    elif(op == '<='):
        if(type(l) == int and type(r) == int):
            lines.append(f"if_icmple L{label}\n")
        elif(type(l) == float and type(r) == float):
            lines.append(f"fcmpl\nifle L{label}\n")
    elif(op == '=='):
        if(type(l) == int and type(r) == int):
            lines.append(f"if_icmpeq L{label}\n")
        elif(type(l) == float and type(r) == float):
            lines.append(f"fcmpl\nifeq L{label}\n")
    elif(op == '!='):
        if(type(l) == int and type(r) == int):
            lines.append(f"if_icmpne L{label}\n")
        elif(type(l) == float and type(r) == float):
            lines.append(f"fcmpl\nifne L{label}\n")
    
    # elif(op == 'and'):
    #     if(type(l) == int and type(r) == int):
    #         lines.append(f"if_icmpgt L{label}\n")
    #     elif(type(l) == float and type(r) == float):
    #         lines.append(f"fcmpl\nifgt L{label}\n")
    # elif(op == 'or'):
    #     if(type(l) == int and type(r) == int):
    #         lines.append(f"if_icmpgt L{label}\n")
    #     elif(type(l) == float and type(r) == float):
    #         lines.append(f"fcmpl\nifgt L{label}\n")


class TFG3MyVisitor(TrabalhoFinalG3Visitor):
    def visitProg(self, ctx):
        lines.append(".class TrabalhoFinal\n.super java/lang/Object\n")
        lines.append(
            ".method public static main([Ljava/lang/String;)V\n.limit stack 50\n.limit locals 10\n")

        for declaration in ctx.var_declaration():
            self.visit(declaration)

        for func_declaration in ctx.func_declaration():
            self.visit(func_declaration)

        self.visit(ctx.main_block())

    def visitDeclarations(self, ctx: TrabalhoFinalG3Parser.DeclarationsContext):
        declaration_type = ctx.type_decl.getText()

        if(ctx.var):
            parse_var(declaration_type, ctx.var.getText())
        if(ctx.attrib):
            parse_var(declaration_type, ctx.attrib.getText())

    def visitFuncDeclaration(self, ctx: TrabalhoFinalG3Parser.FuncDeclarationContext):
        print(ctx.func_type.getText())
        print(ctx.func_name.text)
        print(ctx.parameter_list().getText())
        #print(ctx.stats().getText())

    def visitMain_block(self, ctx):
        for stats in ctx.stats():
            self.visit(stats)

        lines.append("Fim:\nreturn\n.end method")
        with open('jasmin/TrabalhoFinal.j', 'w+') as writer:
            writer.writelines(lines)
            writer.close()

    def visitAttribCommand(self, ctx: TrabalhoFinalG3Parser.AttribCommandContext):
        v = ctx.var.text

        result = self.visit(ctx.op)
        update_var(v, result)

        jasmin_var_attribution(v)

        print(global_variables)

    def visitIfCommand(self, ctx: TrabalhoFinalG3Parser.IfCommandContext):
        condition = ctx.condition_block()
        evaluated_block = False

        if(str(type(condition.op)).find('Logic') != -1):
            evaluated = self.visit(condition.op)
            if(evaluated):
                evaluated_block = True
                lines.append(f"L{label}:\n")
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
            jasmin_print(result1)
            jasmin_print(result2)
        else:
            print(result1)
            jasmin_print(result1)

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
            if(op == '+'):
                jasmin_var_operations(ctx.left, ctx.right, l, r)
                lines.append("iadd\n") if (type(l) == int and type(
                    r) == int) else lines.append("fadd\n")
                return l + r
            elif(op == '-'):
                jasmin_var_operations(ctx.left, ctx.right, l, r)
                lines.append("isub\n") if (type(l) == int and type(
                    r) == int) else lines.append("fsub\n")
                return l - r
            elif(op == '*'):
                jasmin_var_operations(ctx.left, ctx.right, l, r)
                lines.append("imul\n") if (type(l) == int and type(
                    r) == int) else lines.append("fmul\n")
                return l * r
            elif(op == '/'):
                jasmin_var_operations(ctx.left, ctx.right, l, r)
                lines.append("idiv\n") if (type(l) == int and type(
                    r) == int) else lines.append("fdiv\n")
                return l / r
        elif(type(l) == str and type(r) == str and op == '+'):
            return l + r
        else:
            raise TypeError(
                f"Erro - tentando operar {str(type(l)).split()[1].replace('>', '')} com {str(type(r)).split()[1].replace('>', '')}")

    def visitLogicExp(self, ctx: TrabalhoFinalG3Parser.LogicExpContext):
        l = self.visit(ctx.left)
        r = self.visit(ctx.right)
        op = ctx.op.text

        jasmin_var_operations(ctx.left, ctx.right, l, r)
        jasmin_logic_operations(op, l, r)

        if(op == 'and'):
            if(type(l) == bool and type(r) == bool):
                return l and r
            else:
                raise TypeError(f"Operacao {str(type(l)).split()[1].replace('>', '')} and {str(type(r)).split()[1].replace('>', '')} invalida")
                    
        elif(op == 'or'):
            if(type(l) == bool and type(r) == bool):
                return l or r
            else:
                raise TypeError(f"Operacao {str(type(l)).split()[1].replace('>', '')} and {str(type(r)).split()[1].replace('>', '')} invalida")

        operation = {
            '>': lambda: l > r,
            '>=': lambda: l >= r,
            '<': lambda: l < r,
            '<=': lambda: l <= r,
            '==': lambda: l == r,
            '!=': lambda: l != r,
        }
        result = operation.get(op, lambda: None)()

        return result

    def visitParenExp(self, ctx: TrabalhoFinalG3Parser.ParenExpContext):
        return self.visit(ctx.op)

    def visitIdExp(self, ctx: TrabalhoFinalG3Parser.IdExpContext):
        if(not global_variables.__contains__(ctx.atom.text)):
            raise DeclarationError(
                f"Variavel '{ctx.atom.text}' nao declarada.")

        for key, val in global_variables.items():
            if ctx.atom.text == key:
                return val

    def visitNumberExp(self, ctx: TrabalhoFinalG3Parser.NumberExpContext):
        return parse_number(ctx.atom.text)

    def visitStringExp(self, ctx: TrabalhoFinalG3Parser.StringExpContext):
        return ctx.atom.text.replace('"', "")

    def visitBooleanExp(self, ctx: TrabalhoFinalG3Parser.BooleanExpContext):
        return True if (ctx.atom.text == 'True') else False
