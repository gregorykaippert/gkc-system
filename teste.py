string = 'python;php;java;.net;mysql'

for linguagem in string.split(';'):
    print(linguagem)

print('-'*20)

lista = ['php','python','java']

lista2 = ';'.join(lista)

print(lista2)