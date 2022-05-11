a = [2, 4, 8]

try:
    print(a.index(5))
except ValueError:
    print("NUMBER NOT IN LIST")