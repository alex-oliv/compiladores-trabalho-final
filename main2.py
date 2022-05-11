var = {'x': 'int', 'y': 5, 'z': 'ANTLR'}



x = 'int'
y = 5

x = y

x = 5

aux = list(var)
value = var.get('y')


print(aux)
print(value)

if(value == 'int' or value == 'float' or value == 'string'):
    print("SO DECLARADO")
else:
    print("NOPE")
    print

