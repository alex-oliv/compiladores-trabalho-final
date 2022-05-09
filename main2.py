def jasmin_infix_operations(op, l, r):
    if(op == '+'):
        lines.append("iadd\n") if (type(l) == int and type(r) == int) else lines.append("fadd\n")
    elif(op == '-'):
        lines.append("isub\n") if (type(l) == int and type(r) == int) else lines.append("fsub\n")
    elif(op == '*'):
        lines.append("imul\n") if (type(l) == int and type(r) == int) else lines.append("fmul\n")
    elif(op)