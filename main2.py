variables = {"x": 10, "y": 2, "z": 3.5}

aux = 'x'

print(variables)
#print(variables['xx'])
print(list(variables.values()).index(3.5))
print(variables.__contains__('xx'))

my_dict = {"m": 1, "k": 2}
new_keyzx = list(my_dict)
new_variables = list(variables)

index = new_variables.index(aux)
print(f"Index: {index}")

index_key = new_key.index('k')
print(index_key)

print("""
Testando o print.
Com varias linhas.
Será que presta?
Só testando
""")
