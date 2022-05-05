variables = {"x": [10, 'int'], "y": [2, 'int'], "z": [3.5, 'float']}

print(variables['x'][1])



for key, value in variables.items():
    if(value[1] == 'int'):
        print(f"Var {key} eh int")
