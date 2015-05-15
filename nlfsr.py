# -*- coding: utf-8 -*-
"""
Created on Thu May 14 21:52:29 2015

@author: jmorenov
"""

import cifrado_flujo as cf
import datetime
# Busqueda del periodo de NLFSR con f = ((xy) + !z) ^ t
# Semilla 1011
# Tamaño de secuencia alcanzada sin encontrar periodo: 1176000
def nlfsrPeriod(f, s):
    #log = open('log', 'w')
    result = []
    c = s[:]
    h = False
    TAM = 1176000
    i = TAM
    size = 0
    b1 = 0
    b2 = 0
    while h == False:
        
        result.append(c[0])
        result.append(c[1])
        size += 2
        b1 = 1 ^ c[0]*c[1]*c[2] ^ c[2] ^ c[3]  
        b2 = 1 ^ c[1]*c[2]*c[3] ^ c[3] ^ b1   
        c[0] = c[2]
        c[1] = c[3]
        c[2] = b1
        c[3] = b2
        
        if size >= TAM:
            h = cf.hamming_bool(result[0:size/2], result[size/2:size])
            if size == i:
                print(str(datetime.datetime.now())+":  "+str(size))
                i += 500

    return result

r = nlfsrPeriod([[1,1,1,0],[0,0,1,0],[0,0,0,1],[0,0,0,0]],[1,0,1,1])
print(len(cf.period(r)))