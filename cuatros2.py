# Solucion usando memoization v.1
#
# Construye soluciones usando 1 nro 4, luego 2 nros 4, luego 3 y finalmente 4,
# al estilo usado por Dynamic Programming
# (Ver funcion populate_level, la que se invoca sucesivamente de nivel 1 a 4)
#
# Esta solucion generica permitiria usar el mismo codigo para formar soluciones
# de 5 usos del nro 4, 6 usos, etc.
#
# rodrigo.chappa@gmail.com
# http://goo.gl/SAaM48

import operator
 
from math import sqrt

# Construccion bottom up de nums, partiendo por el diccionario de tamano 1
# (ver populate_level() mas abajo tb)
nums  = { 1: { 2: "r(4)", 4: "4", 24: "4!", 4.0/9.0: ".4'", .4: ".4", sqrt(4.0/9.0):"r(.4')" },
          2: { 44: "44" }, 3: {}, 4: {} }

# paren(x): escribe parentesis alrededor de la expresion x, intenta no hacerlo cuando es superfluo
#
# reduce el nro de parentesis usados
# e.g. algunos parentesis superfluos (a*b)+c -> a*b+c
def paren(x,level,force=False):
    if not force:
       if level == 1 or x == "44": return x
       if level == 2 and any( op in x for op in ["*","/"] ): return x
    return "(" + x + ")"

# acerca al entero mas cercano, cuando esta cerca de este
ferror = 0.00001
def roundme(x):
    if abs(x- int(x+ferror)) < ferror: return int(x+ferror)
    return x

# construye tabla de memoization usando los operadores que se pasan
# en parametro funcs, la tabla se usa en invocaciones posteriores
def populate_level(funcs,level):

   ll = {}  # el largo de cada expresion en este nivel, la idea es usar esto para generar expresiones cortas
   nl = nums[level]
   for i in range(1,level):
       # generar todas las combinaciones posibles
       # usar esas combinaciones para operarlas con todos los operadores
       ni  = nums[i]
       nli = nums[level-i]
       newelements = [ (roundme(funcs[op](x,y)), paren(ni[x],i,op=="^") + op + paren(nli[y],level-i)) for op in funcs for x in ni for y in nli ]
       # se tienen varios resultados, tomemos lo mejor
       for k,v in newelements:
           # se usa una expresion mas corta cada vez que se puede
           lv = len(v)
           if k not in nl or lv < ll[k]:
              nl[k] = v
              ll[k] = lv

# Para comprobar que los datos generados son correctos
def evalme(expr):
   expr = expr.replace("4!","24").replace(".4'","(4.0/9.0)").replace("r(","sqrt(").replace("^","**")
   return eval(expr)

def populate(funcs):
    for l in range(2,5):
        populate_level(funcs, l)
        # print "nums", l, len(nums[l])

    missing = []
    for n in range(0,101):
        if n in nums[4]:
           print n, "=", nums[4][n]
           print "TST", n, n == int(evalme(nums[4][n])+0.000001)
        else:
           missing.append(n)

    if len(missing) > 0:
       print "Aun falta generar:", missing
        
faraway = -9999
def midiv(x,y): return float(x)/float(y) if y != 0 else faraway
      
def mipow(x,y): return x**y if x >= 0 and x <= 10 and y >= 0 and y <= 5 else faraway

ops = { "+": operator.add, "-": operator.sub, "*": operator.mul, "/": midiv, "^": mipow }
 
if __name__ == '__main__':
    from time import time
    t1 = time()
    populate(ops)
    t2 = time()
    print "Tiempo: %g" % (t2-t1)
