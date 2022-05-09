var = {'x': 2, 'y': 105.5, 'z': 'ANTLR'}

aux = list(var)
value = var.get('z')

print(var.get('a'))

result = 'ANTL'
try:
    re = list(var.values()).index(result)
    print(f"Re: {re}")
except ValueError:
    print("EH uma string")



