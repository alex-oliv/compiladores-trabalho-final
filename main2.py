""" variables = {"x": ['int'], "y": ['int', 2], "z": ['float', 3.5]}
print(variables)

def update_var(var, new_value):
    aux = variables.get(var)
    
    if(len(aux) > 1):
        aux.pop()
    
    aux.append(new_value)
    variables.update({var: aux})


update_var('y', 50)
update_var('x', 10)

print(variables.get('x')[1]) """


v1 = 10.5
v2 = 10.4

if(type(v1) == int and type(v2) == int):
    print("V1 e V2")
elif(type(v1) == float and type(v2) == float):
    print("HM")
else:
    print("HM-2")


""" def jasmin_var_operations(left, right, l, r):
    aux = list(global_variables)

    if(str(type(left)).find('Id') != -1 and str(type(right)).find('Id') != -1):
        if(type(l) == int and type(r) == int):
            lines.append(f"iload {aux.index(left.getText())}\n")
            lines.append(f"iload {aux.index(right.getText())}\n")
    elif(str(type(left)).find('Id') != -1):
        lines.append(f"iload {aux.index(left.getText())}\n")
        lines.append(f"ldc {r}\n")
    elif(str(type(right)).find('Id') != -1):
        lines.append(f"iload {aux.index(right.getText())}\n")
        lines.append(f"ldc {l}\n")
    else:
        lines.append(f"ldc {l}\n")
        lines.append(f"ldc {r}\n") """
