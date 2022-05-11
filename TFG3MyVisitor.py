from this import d
from tokenize import String
from antlr4 import *
from MyExceptions import *

from dist.TrabalhoFinalG3Parser import TrabalhoFinalG3Parser
from dist.TrabalhoFinalG3Visitor import TrabalhoFinalG3Visitor

global_variables = {}
global_funct = {}
flags = {'break': 0, 'for': 0, 'while': 0,
         'read': 0, 'read_print': 0, 'enter_while': -1, 'exit_while': 0, 'read_if': 0, 'enter_func': 0, 'exit_func': 0}
lines = []
label = 0


def transform_var(declaration, var):
    operation = {
        'int': lambda: int(var),
        'float': lambda: float(var),
        'string': lambda: str(var),
        'boolean': lambda: True if var == 'True' else False,
        'void': lambda: 'void'
    }

    return operation.get(declaration, lambda: None)()


def parse_var(declaration_type, declaration):
    first_split = declaration.split(',')

    if(first_split[0].find('=') != -1):
        for aux in first_split:
            key = aux.split('=')[0]
            value = aux.split('=')[1]

            check_var(key)
            if('"' in value):
                global_variables.update(
                    {key: value.replace('"', "")})
                jasmin_var_declaration(key)
            else:
                global_variables.update(
                    {key: transform_var(declaration_type, value)})
                jasmin_var_declaration(key)
    else:
        for aux in first_split:
            check_var(aux)
            global_variables.update({aux: declaration_type})


def parse_id(parse):
    check = parse.isdigit()
    if(check):
        result = int(parse)
    else:
        try:
            result = float(parse)
        except ValueError:
            if(parse == 'True'):
                result = True
            elif(parse == 'False'):
                result = False
            else:
                result = parse

    return result


def parse_func_name(name):
    i = name.find('(')
    return name[:i]


def update_var(var, new_value):
    if(not global_variables.__contains__(var)):
        raise DeclarationError(f"ID '{var}' nao declarado.")

    global_variables.update({var: new_value})


def check_var(var):
    if(global_variables.__contains__(var)):
        raise DeclarationError(f"ID '{var}' ja declarado.")


def jasmin_var_declaration(key):
    var_list = list(global_variables)
    value = global_variables.get(key)

    if(type(value) == int):
        lines.append(f"ldc {value}\nistore {var_list.index(key)}\n")
    elif(type(value) == float):
        lines.append(f"ldc {value}\nfstore {var_list.index(key)}\n")
    elif(type(value) == str):
        lines.append(f'ldc "{value}"\nastore {var_list.index(key)}\n')


def jasmin_print(result):
    lines.append("getstatic java/lang/System/out Ljava/io/PrintStream;\n")

    if(type(result) == int):
        try:
            lines.append(f"iload {list(global_variables.values()).index(result)}\n")
        except ValueError:
            lines.append(f'ldc "{result}"\n')
        lines.append("invokevirtual java/io/PrintStream/println(I)V\n")
    elif(type(result) == float):
        try:
            lines.append(f"fload {list(global_variables.values()).index(result)}\n")
        except ValueError:
            lines.append(f'ldc "{result}"\n')
        lines.append("invokevirtual java/io/PrintStream/println(F)V\n")
    elif(type(result) == str):
        try:
            lines.append(f'aload {list(global_variables.values()).index(result)}\n')
        except ValueError:
            lines.append(f'ldc "{result}"\n')
        lines.append(
            "invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V\n")


def jasmin_var_operations(left, right, l, r):
    var_list = list(global_variables)
    left_key = left.getText()
    right_key = right.getText()

    if(str(type(left)).find('Id') != -1 and str(type(right)).find('Id') != -1):
        if(type(l) == int and type(r) == int):
            lines.append(f"iload {var_list.index(left_key)}\n")
            lines.append(f"iload {var_list.index(right_key)}\n")
        elif(type(l) == float and type(r) == float):
            lines.append(f"fload {var_list.index(left_key)}\n")
            lines.append(f"fload {var_list.index(right_key)}\n")
    elif(str(type(left)).find('Id') != -1):
        if(type(l) == int):
            lines.append(f"iload {var_list.index(left_key)}\n")
        elif(type(l) == float):
            lines.append(f"fload {var_list.index(left_key)}\n")
        lines.append(f"ldc {r}\n")
    elif(str(type(right)).find('Id') != -1):
        if(type(r) == int):
            lines.append(f"iload {var_list.index(right_key)}\n")
        elif(type(r) == float):
            lines.append(f"fload {var_list.index(right_key)}\n")
        lines.append(f"ldc {l}\n")
    else:
        lines.append(f"ldc {l}\n")
        lines.append(f"ldc {r}\n")


def jasmin_infix_operations(op, l, r):
    if(op == '+'):
        lines.append("iadd\n") if (type(l) == int and type(r)
                                   == int) else lines.append("fadd\n")
    elif(op == '-'):
        lines.append("isub\n") if (type(l) == int and type(r)
                                   == int) else lines.append("fsub\n")
    elif(op == '*'):
        lines.append("imul\n") if (type(l) == int and type(r)
                                   == int) else lines.append("fmul\n")
    elif(op == '/'):
        lines.append("idiv\n") if (type(l) == int and type(r)
                                   == int) else lines.append("fdiv\n")


def jasmin_logic_operations(op, l, r):
    global label

    if(op == '>'):
        if(flags['enter_while'] != -1):
            if(type(l) == int and type(r) == int):
                lines.append(f"if_icmpgt L{flags['enter_while']}\n")
            elif(type(l) == float and type(r) == float):
                lines.append(f"fcmpl\nifgt L{flags['enter_while']}\n")
        else:
            if(type(l) == int and type(r) == int):
                lines.append(f"if_icmpgt L{label}\n")
            elif(type(l) == float and type(r) == float):
                lines.append(f"fcmpl\nifgt L{label}\n")
    elif(op == '>='):
        if(flags['enter_while'] != -1):
            if(type(l) == int and type(r) == int):
                lines.append(f"if_icmpge L{flags['enter_while']}\n")
            elif(type(l) == float and type(r) == float):
                lines.append(f"fcmpl\nifge L{flags['enter_while']}\n")
        else:
            if(type(l) == int and type(r) == int):
                lines.append(f"if_icmpge L{label}\n")
            elif(type(l) == float and type(r) == float):
                lines.append(f"fcmpl\nifge L{label}\n")
    elif(op == '<'):
        if(flags['enter_while'] != -1 and flags['read_if'] == 0):
            if(type(l) == int and type(r) == int):
                lines.append(f"if_icmplt L{flags['enter_while']}\n")
            elif(type(l) == float and type(r) == float):
                lines.append(f"fcmpl\niflt L{flags['enter_while']}\n")
        else:
            if(type(l) == int and type(r) == int):
                lines.append(f"if_icmplt L{label}\n")
            elif(type(l) == float and type(r) == float):
                lines.append(f"fcmpl\niflt L{label}\n")
    elif(op == '<='):
        if(flags['enter_while'] != -1 and flags['read_if'] == 0):
            if(type(l) == int and type(r) == int):
                lines.append(f"if_icmple L{flags['enter_while']}\n")
            elif(type(l) == float and type(r) == float):
                lines.append(f"fcmpl\nifle L{flags['enter_while']}\n")
        else:
            if(type(l) == int and type(r) == int):
                lines.append(f"if_icmple L{label}\n")
            elif(type(l) == float and type(r) == float):
                lines.append(f"fcmpl\nifle L{label}\n")
    elif(op == '=='):
        if(flags['enter_while'] != -1 and flags['read_if'] == 0):
            if(type(l) == int and type(r) == int):
                lines.append(f"if_icmpeq L{flags['enter_while']}\n")
            elif(type(l) == float and type(r) == float):
                lines.append(f"fcmpl\nifeq L{flags['enter_while']}\n")
        else:
            if(type(l) == int and type(r) == int):
                lines.append(f"if_icmpeq L{label}\n")
            elif(type(l) == float and type(r) == float):
                lines.append(f"fcmpl\nifeq L{label}\n")
    elif(op == '!='):
        if(flags['enter_while'] != -1 and flags['read_if'] == 0):
            if(type(l) == int and type(r) == int):
                lines.append(f"if_icmpne L{flags['enter_while']}\n")
            elif(type(l) == float and type(r) == float):
                lines.append(f"fcmpl\nifne L{flags['enter_while']}\n")
        else:
            if(type(l) == int and type(r) == int):
                lines.append(f"if_icmpne L{label}\n")
            elif(type(l) == float and type(r) == float):
                lines.append(f"fcmpl\nifne L{label}\n")

    label += 1
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


def jasmin_if_command(evaluated, stmt):
    aux = label
    if(stmt == None):
        lines.append(f"goto L{aux}\n")
    else:
        lines.append(f"goto ELSE{label-1}\n")

    if(evaluated):
        lines.append(f"L{label-1}:\n")

    if(not evaluated and stmt == None):
        lines.append(f"L{label-1}:\n")
    elif(evaluated and stmt != None):
        lines.append(f"ELSE{label-1}:\n")


def jasmin_for_command(var, range_values):
    var_list = list(global_variables)
    i = global_variables.get(var)

    lines.append(f"Lfor{var}:\n")
    if(type(i) == int and type(range_values[1]) == int):
        lines.append(f"iload {var_list.index(var)}\n")
        lines.append(f"ldc {range_values[1]}\n")
    elif(type(i) == float and type(range_values[1]) == float):
        lines.append(f"iload {var_list.index(var)}\n")
        lines.append(f"ldc {range_values[1]}\n")

    jasmin_logic_operations('>=', global_variables.get(var), range_values[1])


def jasmin_break():
    lines.append("return\n")


def jasmin_input_command(ctx, var=None):
    if(ctx == 2):
        var_list = list(global_variables)

        lines.append(f"invokestatic TrabalhoFinal.read()I\n")
        lines.append(f"istore {var_list.index(var)}\n")
    elif(ctx == 1):
        lines.append(""".method public static read()I

        .limit stack 5   ; up to five items can be pushed
        .limit locals 100

        ; the input function starts at this point
            ldc 0
            istore 50     ; storage for a dummy integer for reading it by input()
            ldc 0
            istore 49     ; preparacao para negativo
        Label1:
            getstatic java/lang/System/in Ljava/io/InputStream;
            invokevirtual java/io/InputStream/read()I
            istore 51
            iload 51
            ldc 10 ; uso no mac (valor ASCII da tecla ENTER)
        ;    ldc 13 ; uso no windows (valor ASCII da tecla ENTER)
            isub
            ifeq Label2
            iload 51
            ldc 32 ; space 
            isub
            ifeq Label2
            iload 51
            ldc 43 ; plus sign
            isub
            ifeq Label1
            iload 51
            ldc 45 ; minus sign
            isub
            ifeq Label3
            iload 51
            ldc 48
            isub
            ldc 10
            iload 50
            imul
            iadd
            istore 50
            goto Label1

        Label3:
            ldc 1
            istore 49
            goto Label1
            
        Label2:     ; now our dummy integer contains the integer read from the keyboard
            ldc 1
            iload 49
            isub
            ifeq Label4
            iload 50       ; input function ends here
            ireturn
        Label4:
            ldc 0
            iload 50
            isub
            ireturn
        .end method""")
    

def jasmin_func(func_name):
    func_type = global_variables.get(func_name)
    var_list = list(global_variables)

    op = {
        'int': lambda: 'I',
        'float': lambda: 'F',
        'string': lambda: 'Ljava/lang/String;',
        'void': lambda: 'V',
    }
    result = op.get(func_type, lambda: None)()

    lines.append(f"invokestatic TrabalhoFinal.{func_name}(){result}\n")
    if(func_type == 'int'):
        lines.append(f"istore {var_list.index(func_name)}\n")
    elif(func_type == 'float'):
        lines.append(f"fstore {var_list.index(func_name)}\n")
    elif(func_type == 'string'):
        lines.append(f"astore {var_list.index(func_name)}\n")


class TFG3MyVisitor(TrabalhoFinalG3Visitor):
    def visitProg(self, ctx):
        lines.append(".class TrabalhoFinal\n.super java/lang/Object\n")
        lines.append(
            ".method public static main([Ljava/lang/String;)V\n.limit stack 50\n.limit locals 10\n")

        for declaration in ctx.var_declaration():
            self.visit(declaration)

        for func_declaration in ctx.func_declaration():
            global_funct[func_declaration.func_name.text] = self.visit(
                func_declaration)

        self.visit(ctx.main_block())

    def visitDeclarations(self, ctx: TrabalhoFinalG3Parser.DeclarationsContext):
        declaration_type = ctx.type_decl.getText()

        if(ctx.var):
            parse_var(declaration_type, ctx.var.getText())
        if(ctx.attrib):
            parse_var(declaration_type, ctx.attrib.getText())

    def visitFuncDeclaration(self, ctx: TrabalhoFinalG3Parser.FuncDeclarationContext):
        flags[ctx.func_name.text] = []
        parse_var(ctx.func_type.getText(), ctx.func_name.text)

        op = {
            'int': lambda: 'I',
            'float': lambda: 'F',
            'string': lambda: 'Ljava/lang/String;',
            'void': lambda: 'V',
        }
        result = op.get(ctx.func_type.getText(), lambda: None)()

        lines.append(f".method public static {ctx.func_name.text}(){result}\n.limit stack 50\n.limit locals 10\n")

        for parameter in ctx.parameter_list():
            parse_var(parameter.t_type().getText(), parameter.ID().getText())
            flags[ctx.func_name.text].append(parameter.ID().getText())

        flags['enter_func'] = 1
        for stats in ctx.stats():
            self.visit(stats)
        flags['enter_func'] = 0
        flags['exit_func'] = 1

        return ctx.stats()

    def visitMain_block(self, ctx):
        input_command = 0
        for stats in ctx.stats():
            if(stats.input_command()):
                input_command = 1
            self.visit(stats)
        func_names = list(global_funct)
        for func in func_names:
            jasmin_func(func)

        lines.append("Fim:\nreturn\n.end method\n\n")
        if(input_command == 1):
            jasmin_input_command(1)

        with open('jasmin/TrabalhoFinal.j', 'w+') as writer:
            writer.writelines(lines)
            writer.close()

    def visitAttribCommand(self, ctx: TrabalhoFinalG3Parser.AttribCommandContext):
        var = ctx.var.text

        if(str(type(ctx.op)).find('Func') != -1):
            func_name = parse_func_name(ctx.op.getText())
            if(global_variables[func_name] == 'void'):
                raise TypeError("Erro - Funcao declarada do tipo sem retorno.")

        control = 0
        if(flags['for'] == 0 and flags['while'] == 0):
            if(str(type(ctx.op)).find('Number') != -1 or str(type(ctx.op)).find('String') != -1) or str(type(ctx.op)).find('Infix') != -1:
                control = 1

        result = self.visit(ctx.op)

        var_list = list(global_variables)
        values_list = list(global_variables.values())

        if(flags['for'] == 0 and flags['while'] == 0):
            if(control == 0):
                if(type(result) == int):
                    lines.append(
                        f"iload {values_list.index(result)}\nistore {var_list.index(var)}\n")
                elif(type(result) == float):
                    lines.append(
                        f"fload {values_list.index(result)}\nfstore {var_list.index(var)}\n")
                elif(type(result) == str):
                    lines.append(
                        f"aload {values_list.index(result)}\nastore {var_list.index(var)}\n")

        update_var(var, result)

        if(flags['for'] == 0 and flags['while'] == 0):
            if(control == 1):
                if(type(result) == int):
                    lines.append(f"istore {var_list.index(var)}\n")
                elif(type(result) == float):
                    lines.append(f"fstore {var_list.index(var)}\n")
                elif(type(result) == str):
                    lines.append(
                        f'"ldc {result}"\nastore {var_list.index(var)}\n')

    def visitIfCommand(self, ctx: TrabalhoFinalG3Parser.IfCommandContext):
        condition = ctx.condition_block()
        evaluated_block = False

        if(str(type(condition.op)).find('Logic') != -1):
            flags['read_if'] = 1
            evaluated = self.visit(condition.op)
            if(flags['for'] == 0 and flags['while'] == 0):
                jasmin_if_command(evaluated, ctx.stmt)

            if(evaluated):
                evaluated_block = True
                self.visit(condition.stmt)

            if(flags['read'] == 0):
                lines.append(f"L{label-1}:\n")
                self.visit(condition.stmt)
                if(ctx.stmt != None):
                    lines.append(f"ELSE{label-1}:\n")
                flags['read'] = 1
            else:
                flags['read'] = 0
                if(flags['exit_while'] == 0):
                    lines.append(f"L{label-1}:\n")
                    self.visit(condition.stmt)
                    if(ctx.stmt != None):
                        lines.append(f"goto L{label}\nELSE{label-1}:\n")
                flags['read'] = 1

            if(not evaluated_block and ctx.stmt != None):
                self.visit(ctx.stmt)

            if(flags['for'] == 0 and flags['while'] == 0):
                lines.append(f"L{label}:\n")

            flags['read_if'] = 0
            return evaluated
        else:
            raise OperationError(
                f"Operacao '{condition.op.getText()}' invalida para um condicional")

    def visitForCommand(self, ctx: TrabalhoFinalG3Parser.ForCommandContext):
        range_values = self.visit(ctx.rang)
        var = ctx.var.text
        var_list = list(global_variables)

        jasmin_for_command(var, range_values)
        aux = label-1
        for i in range(range_values[0], range_values[1], range_values[2]):
            update_var(var, i)
            self.visit(ctx.stmt)

            if(flags['for'] == 0):
                lines.append(f"goto Lfor{var}_inc\nLfor{var}_inc:\n")
                lines.append(
                    f"iinc {var_list.index(var)} {range_values[2]}\ngoto Lfor{var}\n")
                lines.append(f"L{aux}:\nreturn\n")
                flags['for'] = 1
                flags['read'] = 1

            if(flags['break'] == 1):
                flags['break'] = 0
                lines.append("return\n")
                flags['for'] = 0
                break

        flags['for'] = 0

    def visitRangeCommand(self, ctx: TrabalhoFinalG3Parser.RangeCommandContext):
        aux = []
        range_values = []

        if(ctx.ID()):
            for x in ctx.ID():
                aux.append(global_variables.get(x.getText()))
        else:
            for x in ctx.NUMBER():
                aux.append(parse_id(x.getText()))

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

            flags['read'] = 1
            lines.append(f"L{label-1}:\n")
            flags['enter_while'] = label-1

            while(op):
                self.visit(ctx.stmt)
                op = self.visit(ctx.op)

                if(flags['break'] == 1):
                    flags['break'] = 0
                    break

                if(flags['while'] == 0):
                    flags['while'] = 1
                    flags['exit_while'] = 1

        else:
            raise OperationError(
                f"Operacao '{ctx.op.getText()}' invalida para um condicional")

    def visitPrintCommand(self, ctx: TrabalhoFinalG3Parser.PrintCommandContext):
        if(str(type(ctx.op1)).find('Func') != -1):
            func_name1 = parse_func_name(str(ctx.op1.getText()))
            self.visit(ctx.op1)
            result1 = global_variables[func_name1]

            if(ctx.op2):
                if(str(type(ctx.op2)).find('Func') != -1):
                    func_name2 = parse_func_name(str(ctx.op2.getText()))
                    self.visit(ctx.op2)
                    result2 = global_variables[func_name2]
                    print(result1, result2)
                else:
                    result2 = self.visit(ctx.op2)
                    if(flags['read'] == 1):
                        print(result1, result2)
                    if(flags['for'] == 0 and flags['while'] == 0):
                        jasmin_print(result1)
                        jasmin_print(result2)
            else:
                if(flags['read_print'] == 0 and flags['read'] == 1):
                    print(result1)
                if(flags['for'] == 0 and flags['while'] == 0):
                    jasmin_print(result1)
        else:
            result1 = self.visit(ctx.op1)
            if(ctx.op2):
                if(str(type(ctx.op2)).find('Func') != -1):
                    func_name = parse_func_name(str(ctx.op2.getText()))
                    self.visit(ctx.op2)
                    result2 = global_variables[func_name]
                    print(result1, result2)
                else:
                    result2 = self.visit(ctx.op2)
                    if(flags['read'] == 1):
                        print(result1, result2)
                    if(flags['for'] == 0 and flags['while'] == 0):
                        jasmin_print(result1)
                        jasmin_print(result2)
            else:
                if(flags['read_print'] == 0 and flags['read'] == 1):
                    print(result1)
                if(flags['for'] == 0 and flags['while'] == 0):
                    jasmin_print(result1)

    def visitInputCommand(self, ctx: TrabalhoFinalG3Parser.InputCommandContext):
        var = ctx.var.text
        parse = input()

        jasmin_input_command(2, var)

        result = parse_id(parse)
        update_var(var, result)

    def visitFunct_return(self, ctx: TrabalhoFinalG3Parser.Funct_returnContext):
        raise FunctionReturnResultException(self.visit(ctx.op))

    def visitExpr_list(self, ctx: TrabalhoFinalG3Parser.Expr_listContext):
        return self.visit(ctx.op)

    def visitBreakCommand(self, ctx: TrabalhoFinalG3Parser.BreakCommandContext):
        flags['break'] = 1

    def visitNotExp(self, ctx: TrabalhoFinalG3Parser.NotExpContext):
        op = self.visit(ctx.op)
        result = not op

        return result

    def visitUnaryExp(self, ctx: TrabalhoFinalG3Parser.UnaryExpContext):
        op = self.visit(ctx.op)
        result = -op

        return result

    def visitInfixExp(self, ctx: TrabalhoFinalG3Parser.InfixExpContext):
        if(str(type(ctx.left)).find('Func') != -1):
            func_name = parse_func_name(str(ctx.left.getText()))
            self.visit(ctx.left)
            l = global_variables[func_name]
        else:
            l = self.visit(ctx.left)

        if(str(type(ctx.right)).find('Func') != -1):
            func_name = parse_func_name(str(ctx.right.getText()))
            self.visit(ctx.right)
            r = global_variables[func_name]
        else:
            r = self.visit(ctx.right)

        op = ctx.op.text

        if((type(l) != str and type(r) != str) and (type(l) != bool and type(r) != bool)):
            if(flags['for'] == 0 and flags['while'] == 0):
                jasmin_var_operations(ctx.left, ctx.right, l, r)

            if(op == '+'):
                if(flags['for'] == 0 and flags['while'] == 0):
                    jasmin_infix_operations(op, l, r)
                return l + r
            elif(op == '-'):
                if(flags['for'] == 0 and flags['while'] == 0):
                    jasmin_infix_operations(op, l, r)
                return l - r
            elif(op == '*'):
                if(flags['for'] == 0 and flags['while'] == 0):
                    jasmin_infix_operations(op, l, r)
                return l * r
            elif(op == '/'):
                if(flags['for'] == 0 and flags['while'] == 0):
                    jasmin_infix_operations(op, l, r)
                return l / r
        elif(type(l) == str and type(r) == str and op == '+'):
            return l + r
        else:
            raise TypeError(
                f"Erro - tentando operar {str(type(l)).split()[1].replace('>', '')} com {str(type(r)).split()[1].replace('>', '')}")

    def visitLogicExp(self, ctx: TrabalhoFinalG3Parser.LogicExpContext):
        if(str(type(ctx.left)).find('Func') != -1):
            func_name = parse_func_name(str(ctx.left.getText()))
            self.visit(ctx.left)
            l = global_variables[func_name]
        else:
            l = self.visit(ctx.left)

        if(str(type(ctx.right)).find('Func') != -1):
            func_name = parse_func_name(str(ctx.right.getText()))
            self.visit(ctx.right)
            r = global_variables[func_name]
        else:
            r = self.visit(ctx.right)

        op = ctx.op.text

        if(flags['for'] == 0 and flags['while'] == 0):
            jasmin_var_operations(ctx.left, ctx.right, l, r)
            jasmin_logic_operations(op, l, r)

        left_operation_type = str(type(l)).split()[1].replace('>', '')
        rigth_operation_type = str(type(r)).split()[1].replace('>', '')

        if(op == 'and'):
            if(type(l) == bool and type(r) == bool):
                return l and r
            else:
                raise TypeError(
                    f"Operacao {left_operation_type} and {rigth_operation_type} invalida.")
        elif(op == 'or'):
            if(type(l) == bool and type(r) == bool):
                return l or r
            else:
                raise TypeError(
                    f"Operacao {left_operation_type} and {rigth_operation_type} invalida.")

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

    def visitFuncExp(self, ctx: TrabalhoFinalG3Parser.FuncExpContext):
        func_name = ctx.ID().getText()

        if(not global_variables.__contains__(func_name)):
            raise DeclarationError(f"ID '{func_name}' nao declarado.")

        parameters = flags[func_name]
        count = 0

        jasmin_func(func_name)

        if(ctx.expr_list()):
            for expr in ctx.expr_list().expr():
                e = expr.getText()
                if(e.find('(') != -1):
                    self.visit(expr)
                    update_var(
                        parameters[count], global_variables[parse_func_name(e)])
                else:
                    value = self.visit(expr)
                    update_var(parameters[count], value)

                count += 1

        for expr in global_funct[func_name]:
            try:
                self.visit(expr)
            except FunctionReturnResultException as e:
                result = parse_id(str(e))
                update_var(func_name, result)

    def visitParenExp(self, ctx: TrabalhoFinalG3Parser.ParenExpContext):
        return self.visit(ctx.op)

    def visitIdExp(self, ctx: TrabalhoFinalG3Parser.IdExpContext):
        if(not global_variables.__contains__(ctx.atom.text)):
            raise DeclarationError(
                f"ID '{ctx.atom.text}' nao declarado.")

        for key, val in global_variables.items():
            if ctx.atom.text == key:
                return val

    def visitNumberExp(self, ctx: TrabalhoFinalG3Parser.NumberExpContext):
        return parse_id(ctx.atom.text)

    def visitStringExp(self, ctx: TrabalhoFinalG3Parser.StringExpContext):
        return ctx.atom.text.replace('"', "")

    def visitBooleanExp(self, ctx: TrabalhoFinalG3Parser.BooleanExpContext):
        return True if (ctx.atom.text == 'True') else False
