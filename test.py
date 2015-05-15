# -*- coding: utf-8 -*-
"""
Criptografía. Práctica 2. Cifrado de Flujo

@author: Javier Moreno <jmorenov@correo.ugr.es>

Archivo de prueba de los ejercicios mostrando ejemplos y comprobaciones.

"""

import cifrado_flujo as cf

####################
#
# Ejercicio 1
#
####################
print("Ejercicio 1")
if cf.testGolomb("01110100"):
    print("Cumple los postulados de Golomb.")
else:
    print("No cumple los postulados de Golomb.")


####################
#
# Ejercicio 2
#
####################
print("Ejercicio 2")
# Polinomio reducible D^4 + D^2 + 1 --> Periodo máximo: <7 --> Periodo: 110011
print(len(cf.period(cf.lfsr([4,2],1100,24))))
# Polinomio irreducible D^4+D^3+D^2+D+1 --> Periodo máximo: divisor de 15 = 2^4 - 1 --> Periodo: 11000
print(len(cf.period(cf.lfsr([4,3,2,1],1100,30))))
# Polinomio irreducible y primitivo D^18 + D^3 --> Periodo: 2^5 - 1 = 31
print(len(cf.period(cf.lfsr([5,2],10101,62))))

# Cambiando las semillas:
print(len(cf.period(cf.lfsr([4,2],1101,24))))
print(len(cf.period(cf.lfsr([4,3,2,1],1100,30))))
print(len(cf.period(cf.lfsr([5,2],10110,62))))

# Probando postulados de Golomb con un polinomio primitivo.
if cf.testGolomb(cf.period(cf.lfsr([5,2],10110,62))):
    print("Cumple los postulados de Golomb.")
else:
    print("No cumple los postulados de Golomb.")

####################
#
# Ejercicio 3
#
####################
print("Ejercicio 3")
# Convierto la función f pedida a una en que solo use and y xor como operadores.
# Para ello uso las leyes de Demorgan y las propiedad distributiva y asociativa.
# f(x,y,z,t) = ((x*y) + !z) ^ t = ((!(xy) * z) ^ 1) ^ t = ((x*y ^ 1) * z) ^ 1 ^ t = (x*y*z ^ z) ^ 1 ^ t 
#            = x*y*z ^ z ^ t ^ 1 = [[1,1,1,0],[0,0,1,0],[0,0,0,1],[0,0,0,0]]
# Semilla = 1011
b = cf.nlfsr([[1,1,1,0],[0,0,1,0],[0,0,0,1],[0,0,0,0]],[1,0,1,1], 12)
print(b)


####################
#
# Ejercicio 4
#
####################
print("Ejercicio 4")
e = cf.encrypt("10111", "1001", "1000", "1110", "1010", "1010", "1101")
print(e)
d = cf.encrypt(e, "1001", "1000", "1110", "1010", "1010", "1101")
print(d)


####################
#
# Ejercicio 5
#
####################
print("Ejercicio 5")

C1 = cf.lfsr([2,1],"11", 3)
C2 = cf.lfsr([3,1],"111", 7)

L1,C = cf.BerlekampMassey(C1)
print(L1)

L2,C = cf.BerlekampMassey(C2)
print(L2)

# Se observa como la complejidad es la suma de la complejidad de cada secuencia por separado.
L3,C = cf.BerlekampMassey(C1+C2)
print(L3)

C3 = C1[:]
for i in range(len(C2)):
    C3[i] = C1[i] ^ C2[i]

L4,C = cf.BerlekampMassey(C3)
print(L4)
