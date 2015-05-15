# -*- coding: utf-8 -*-
"""
Created on Tue Feb 24 11:04:30 2015

Criptografía y Computación
Práctica 1: Aritmética Modular

@author: Francisco Javier Moreno Vega (jmorenov)
"""

# Ejercicio 1
def gcd(a, b):
    # list = [q, r, u, v]
    l_1 = [0, a, 1, 0]
    l_2 = [0, b, 0, 1]
    l_tmp = [a, 0, 0, 0]
    
    while l_2[1] > 0:
        while l_tmp[0] * l_2[1] > l_1[1]:
            l_tmp[0] = l_tmp[0] - 1
        for i in [1, 2, 3]:
            l_tmp[i] = l_1[i] - (l_tmp[0] * l_2[i])
        l_1 = l_2
        l_2 = l_tmp
        l_tmp = [l_1[1], 0, 0, 0]
        
    return l_1
    
# Ejercicio 2
# a^-1 mod b
def inv_mod(a, b):    
    l = gcd(b,a)
    if l[1] != 1:
        #print("false")
        return
    else:
        if l[2] < 0:
            l[2] = l[2]%b
        return l[3]

# Ejercicio 3
def binary(i):
    return "{0:b}".format(i)

# a^b mod n
def power_mod_int(a, b, n):
    B = 1
    if b != 0:
        A = a
        k = binary(b)
        k = k[::-1]
        if int(k[0]) == 1:
            B = a
        for i in range(len(k)):
            A = (A * A) % n
            if k[i] == 1:
                B = (A * B) % n
    return B
    

#Ejercicio 4
import random
test = 10

def is_prime(n):
    if n == 2:
        print("True")
        return
    if n % 2 == 0:
        print("False")
        return
    mod = 1%n
    mod1 = -1%n
    b = [None] * test
    for i in range(test):
        b[i] = random.randint(1, n-1)
    n1 = n-1
    l = 0
    if n1%2==0:
        while n1%2==0 and ((n-1)/2**(l+1))%2!=0:        
            n1 /= 2
            l += 1
    
    m = (n-1)/(2**l)
    for i in range(test):
        J = [None] * l
        j = 1
        while j<l:
            J[j] = pow(b[i], round(pow(2,j)*m))%n
            j+=1
        j = 2
        while j<l-1:
            if (J[j-1] != mod or J[j-1] != mod1) and J[j] == mod:
                print("False")
                return
            j+=1
        aux = pow(b[i],n-1)
        if aux%n != mod:
            print("False")
            return
    print("True")
    return

#Ejercicio 5
#y = a**x mod n
#Logaritmo de y base a modulo n
import math
def baby_giant_step(y, a, n):
    s = math.floor(math.sqrt(n))
     
    A = []
    B = []
     
    for r in range(0,s):
        value = y*(a^r) % n
        A.append(value)
     
    for t in range(1,s+1):
        value = a^(t*s) % n
        B.append(value)
     
    x1,x2 =0,0
      
    for r in A:
        for t in B:
            if r == t:
                x1 = A.index(r)            
                x2 = B.index(t)
                break
            
    print ("El valor de x es ", ((x2+1)*s - x1) % n)
    return


#Ejercicio 6
def congruente(a, b, m):
    if a%m == b%m:
        return True
    return False

def k_congruente(a, b, m): #Calcula un valor k de la congruencia.
    if congruente(a, b, m) == False:
        return
    return (a-b)/m

def jacobi(a, n):
    if n<3 or n%2 == 0 or a<0 or a>=n:
        print("Error en los valores.")
        return
    if a==0:
        return 0
    if a==1:
        return 1
        
    a1 = a
    e = 0    
    if a%2==0:
        while a1%2==0:        
            a1 /= 2
            e += 1
    
    if e%2==0 or (congruente(n, 1, 8) or congruente(n, 7, 8)):
        s = 1
    if congruente(n, 3, 8) or congruente(n, 5, 8):
        s = -1
    if congruente(n, 3, 4) and congruente(a1, 3, 4):
        s = -s
    
    n1 = n%a1
    
    if a1==1:
        return s
    else:
        return s*jacobi(n1, a1)

def ejercicio6a(a, p):
    if jacobi(a, p) != 1:
        print("Error en los valores.")
        return
    if congruente(p, 3, 4) == True:
        k = k_congruente(p, 3, 4)        
        return pow(a, k+1)
    if congruente(p, 1, 4) == True:
        k = k_congruente(p, 1, 4)
        b = random.randint(0, k-1)
        while jacobi(b, p) != -1:
            b = random.randint(0, k-1)
        i = 2*k
        j = 0
        while i%2==0:
            i = i/2
            j = j/2
            if pow(a, i)*pow(b, j) == -1:
                j = j + 2*k
        return pow(a, (i+1)/2)*pow(b, j/2)
    
    
#Ejercicio 7
def fermat_factor(n):
    if n<=0:
        print("Error en los valores.")
        return
    a = math.ceil(math.sqrt(n))
    b = math.sqrt((a*a)-n)
    while abs(b) - abs(int(b)) > 0.0:
        a += 1
        b = math.sqrt((a*a)-n)
    print (a-b)
    print (a+b)
    return

import fractions
def pollard(n):
    x = 2
    y = 2
    c = random.randint(1, n-1) 
    d = 1
    while d==1:
        x = (x*x+c)%n
        y = (y*y+c)%n
        y = (y*y+c)%n
        d = fractions.gcd(abs(x-y), n)
    return d

"""
Ejecución de los algoritmos y toma de tiempos.
"""
import time
inicio=time.time()
i=0
MAX = 1000

while i<MAX:
    gcd(393, 267)
    i=i+1
fin=time.time()
tiempo=fin - inicio
print("Ejercicio 1: ",tiempo)

inicio=time.time()
i=0
while i<MAX:
    inv_mod(391, 1542)
    i=i+1
fin=time.time()
tiempo=fin - inicio
print("Ejercicio 2: ",tiempo)

inicio=time.time()
i=0
while i<MAX:
    power_mod_int(86, 72, 145)
    i=i+1
fin=time.time()
tiempo=fin - inicio
print("Ejercicio 3: ",tiempo)

inicio=time.time()
i=0
while i<MAX:
    is_prime(46381)    
    i=i+1
fin=time.time()
tiempo=fin - inicio
print("Ejercicio 4: ",tiempo)

inicio=time.time()
i=0
while i<MAX:
    baby_giant_step(9, 11, 19)
    i=i+1
fin=time.time()
tiempo=fin - inicio
print("Ejercicio 5: ",tiempo)

inicio=time.time()
i=0
while i<MAX:
    ejercicio6a(5, 299)
    i=i+1
fin=time.time()
tiempo=fin - inicio
print("Ejercicio 6a: ",tiempo)

inicio=time.time()
i=0
while i<MAX:
    fermat_factor(132)
    i=i+1
fin=time.time()
tiempo=fin - inicio
print("Ejercicio 7a: ",tiempo)

inicio=time.time()
i=0
while i<MAX:
    pollard(40259)
    i=i+1
fin=time.time()
tiempo=fin - inicio
print("Ejercicio 7b: ",tiempo)