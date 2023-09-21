import numpy as np



lista = [ 10, 5, 5, 5, 11]

print('lista antes', lista)

cp = lista.copy()

lista.append(5)
lista.append(6)

print('lista alterada', lista)

for i in cp:
    lista.remove(i)

print('lista nova', lista)