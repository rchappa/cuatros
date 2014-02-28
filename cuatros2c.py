# Solucion usando memoization v.3
# Produce expresiones mas largas (comparada con las otras versiones)
# No considera el largo de las expresiones para insertar las siguientes
# Inserta siempre, incondicionalmente.
# Se generan incluso algunos parentesis superfluos
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
nums  = { 1: { 2: "r(4)", 4: "4", 24: "4!", 4.0/9.0: ".4'", .4: ".4", sqrt(4.0/9.0):"r(.4')" } }

# paren(x): escribe parentesis alrededor de la expresion x, intenta no hacerlo cuando es superfluo
#
# No hace el mejor esfuerzo, eso si, pero eso requiere mas logica
def paren(x,level):
    return "(" + x + ")" if level > 1 else x

# construye tabla de memoization usando los operadores que se pasan
# en parametro funcs, la tabla se usa en invocaciones posteriores
def populate_level(funcs,level):

   for i in range(1,level):
       # generar todas las combinaciones posibles
       # usar esas combinaciones para operarlas con todos los operadores
       ni  = nums[i]
       nli = nums[level-i]
       nums[level] = dict( [ (funcs[op](x,y), paren(ni[x],i) + op + paren(nli[y],level-i)) for op in funcs for x in ni for y in nli ] )
   nums[2][44] = "44"

## Para comprobar que los datos generados son correctos
def evalme(expr):
   expr = expr.replace("4!","24").replace(".4'","(4.0/9.0)").replace("r(","sqrt(").replace("^","**")
   expr = expr.replace("4.0","X").replace("44","Y").replace(".4","Z")
   expr = expr.replace("4","4.0").replace("Z",".4").replace("Y","44").replace("X","4.0")
   return eval(expr)

def populate(funcs):
    for l in range(2,5):
        populate_level(funcs, l)
        # print "nums", l, len(nums[l])

# Cuando no se estan generando todas las expresiones, descomentar para saber cuales son estos,
# los que se guardan en la lista missing
#
    missing = []
    n4 = nums[4]
    for n in range(0,101):
        if n in n4:
           print n, "=", n4[n]
## Descomentar para comprobar que las expresiones efectivamente generan el nro adecuado
           print "TST", n, n == int(evalme(n4[n])+0.000001)
           if n != int(evalme(n4[n])+0.000001):
              print n, int(evalme(n4[n])+0.000001)
              print n, evalme(n4[n])
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
