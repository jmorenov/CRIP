# -*- coding: utf-8 -*-
"""
Criptografía. Práctica 2. Cifrado de Flujo

@author: Javier Moreno <jmorenov@correo.ugr.es>
"""

def tobits(s):
    """ Conversión a bits.
    
        Recibe una cadena de caracteres, una lista o un entero 
        y lo convierte a una lista binaria.

    """    
    if type(s) in (tuple, list): return s
    if type(s) is int: s = str(s)
    result = []
    for c in s:
        bit = int(c)
        result.append(bit)
    return result

def checkIsBinary(l):
    """ Comprueba si el argumento es binario.
    
    """    
    l = tobits(l)
    for i in l:
        if i != 0 and i != 1: return False
    return True

def testGolomb(b):
    """ Determina si una secuencia de bits cumple los postulados de Golomb.
    
    """
    b = tobits(b)

    n_1 = sum(1 for i in b if i == 1)    
    n_0 = sum(1 for i in b if i == 0)
    if abs(n_1-n_0) > 1:
        return False
    
    r = runs(b)
    for i in range(1, len(r)-1):
        if r[i+1] != 0 and r[i]/2 != r[i+1] and r[i] != r[i+1]:
            return False
    
    s1 = b[:]
    s2 = moveRight(b)
    h = hamming(s1, s2)
    while s2 != b:       
        s1 = s2[:]
        s2 = moveRight(s2)
        h1 = hamming(s1, s2)
        if(h != h1):
            return False
    
    return True
    
def runs(s):
    """ Calcula el número de rachas que hay en una secuencia.
        
        El resultado lo devuelve en un array donde sus índices son el tamaño de cada racha,
        y su valor el número de rachas de esa longitud.

    """    
    m = [0] * len(s)
    i = 0    
    if s[0] == s[-1]: # primer bit igual que el último.
        n = 2    
        i = -2       
        while s[i] == s[0]:
            s[i] = -1
            n = n + 1
            i = i - 1
        i = 1
        while s[i] == s [0]:
            s[i] = -1
            n = n + 1
            i = i + 1
        m[n] += 1 # Añado una racha más de longitud n.

    bit = s[i]
    n = 0
    while i < len(s) and s[i] != -1:
        if bit == s[i]:
            n += 1
        else:
            m[n] += 1
            n = 1
            bit = s[i]
        i += 1
    m[n] += 1
    return(m)
  
def moveRight(s):
    """ Desplaza un bit a la derecha en una secuencia. 

    """    
    tmp = s[:]
    tmp[0] = s[-1]
    for i in range(1, len(tmp)):
        tmp[i] = s[i-1]
    return tmp
    
def hamming(s1, s2):
    h = 0
    for i in range(len(s1)):
        h += s1[i] ^ s2[i]
    return h

def hamming_bool(s1, s2):
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            return False
    return True

def lfsr(coef, seed, size):    
    """ Implementación de un registro lineal de desplazamiento con retroalimentación LFSR.
    
        Parámetros:
        coef -- Coeficientes o exponentes del polinomio de conexión: [1,0,1] indica el polinomio: D^2 + 1,
                otra forma de definir el mismo polinomio sería: [2].
        seed -- Semilla para el primer estado.
        size -- Longitud de la secuencia.
        
        Devuelve: Una lista binaria con la secuencia.
    
    """
    coef = tobits(coef)
    seed = tobits(seed) # Semilla pasada como cadena de caracteres.
    if checkIsBinary(coef): # coef pasada como coeficientes binarios del polinomio de conexión.
       exp = []
       for i in range(len(coef)):
           if coef[i] == 1: exp.append(i)
       coef = exp 
       
    sec = [0] * size
    L = max(coef)
    for i in range(L):
        sec[i] = seed[i]
    for j in range(size-L):
        for e in coef:
           sec[j+L] = sec[j+L] ^ sec[j+L-e] # Uso el operador XOR al estar trabajando en Z2.
    return(sec)


def period(s):
    """ Devuelve el periodo de una secuencia si lo hay, si no devuelve vacio (None).

    """    
    for i in range(1,len(s)):
        if len(s)%i == 0 and s == s[:i] * int(len(s)/i):
            return s[:i]
   
def nlfsr(f, s, k):
    """ Implementación de un NLFSR.
    
        Parámetros:
        f -- Función de feed-back definida como un array de arrays binario: [[1,0,1],[1,1,1],[0,1,1]]
        s -- Semilla para el primer estado.
        k -- Longitud de la secuencia.
        
        Devuelve: Una lista binaria con la secuencia.
    
    """
    result = []
    c = s[:]

    for i in range(k):
        b = 0
        for j in range(len(f)):
            a = 1
            for t in range(len(f[j])):
                if f[j][t] == 1:
                    a *= c[t]
            b ^= a
        result.append(c[0])
        for x in range(len(c)-1):
            c[x] = c[x+1]
        c[-1] = b

    return result

def geffe(coef1, seed1, coef2, seed2, coef3, seed3, size):
    """ Implementación de el generador de secuencias Geffe.

    """    
    result = []    
    x1 = lfsr(coef1, seed1, size)
    x2 = lfsr(coef2, seed2, size)
    x3 = lfsr(coef3, seed3, size) 

    for i in range(size):
        f = (x1[i]*x2[i])^(x2[i]*x3[i])^x3[i]
        result.append(f)
    
    return result

def encrypt(text, coef1, seed1, coef2, seed2, coef3, seed3):
    """ Cifrado de flujo usando el generador de secuencias Geffe.
    
        Encripta y desencripta texto binario.
    """
    size = len(text)
    result = geffe(coef1, seed1, coef2, seed2, coef3, seed3, size)

    msg_e = []
    
    for i in range(size):
        msg_e.append(int(text[i])^result[i])
        
    return msg_e
    
def BerlekampMassey(s):
    """ Determina la complejidad lineal de una sucesión binaria.
    
        Hace uso del algoritmo de Berlekamp-Massey.
    
    """
    C = [1]
    L = 0
    m = -1
    B = [1]
    N = 0
    T = []
    l = 1
    while(N<len(s)):
        d = 0
        for i in range(0,L+1):
            d+=C[i]*s[N-i]
        d = d%2
        if d == 1:
            T=C
            D = [0]*(N-m)+B 
            if(len(D)>len(C)):
                C = C+([0]*(len(D)-len(C)))
            for i in range(0,len(D)): 
                C[i] = (C[i]+D[i])%2
            if(L<=N/2):
                L=N+1-L
                m=N
                B=T
                l=1
            else:
                l+=1
        else:
             l+=1
        N = N+1
    return L,C
