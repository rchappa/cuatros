# Solucion usando memoization
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

nums1 = {
    2: "r(4)", 4: "4", 24: "4!", 4.0/9.0: ".4'", .4: ".4", sqrt(4.0/9.0):"r(.4')"
}
nums = {}

# reduce el nro de parentesis usados
def paren(x,force=False):
    if not force:
       cnt = x.count("4")
       if cnt == 1 or x == "44": return x
       if cnt == 2 and any( op in x for op in ["*","/"] ): return x
    return "(" + x + ")"

# acerca al entero mas cercano
def roundme(x):
    dif = x- int(x+0.5)
    if dif < 0: dif = -dif 
    if dif < 0.00001:
       return int(x+0.5)
    return x

# construye tabla de memoization usando los operadores que se pasan
# en parametro funcs
def populate_level(funcs,level):
   nums[level] = {}
   if level == 1:
      nums[1] = {x:nums1[x] for x in nums1}
      return

   for i in range(1,level):
       # generar todas las combinaciones posibles
       pairs = [[x,y] for x in nums[i] for y in nums[level-i]]
       # usar esas combinaciones para operarlas con todos los operadores
       newelements = [ (roundme(funcs[op](x[0],x[1])), paren(nums[i][x[0]],op=="^") + op + paren(nums[level-i][x[1]])) for op in funcs for x in pairs ]
       # se tienen varios resultados, tomemos lo mejor
       for k,v in newelements:
           # se intenta generar la expresion mas corta
           if k not in nums[level]:
              nums[level][k] = v
           else:
              lnew = len(v)
              lold = len(nums[level][k])
              # y tambien se favorece a quienes usan mas "+"
              if lnew < lold or (lnew == lold and v.count("+") > nums[level][k].count("+")):
                 nums[level][k] = v
   # Agrego caso especial de 2 digitos
   # Puede hacerse tambien usando operador de pegado (no implementado aqui)
   if level == 2:
       nums[2][44] = "44"

# Para comprobar que los datos generados son correctos
#def evalme(expr):
#   expr = expr.replace("4!","24").replace(".4'","(4.0/9.0)").replace("r(","sqrt(").replace("^","**")
#   return eval(expr)

def populate(funcs):
    for l in range(1,4+1):
        populate_level(funcs, l)
        # print "nums", l, len(nums[l])

    missing = []
    for n in range(0,100+1):
        if n in nums[4]:
           print n, "=", nums[4][n]
#           print "TST", n, n == int(evalme(nums[4][n])+0.000001)
        else:
           missing.append(n)

    if len(missing) > 0:
       print "Aun falta generar:", missing
        
def midiv(x,y):
    if y == 0: return -9999
    return float(x)/float(y)
      
def mipow(x,y):
    if x >= 0 and y >= 0 and x <= 10 and y <= 10: return x**y
    return -9999

ops = {
    "+": operator.add, "-": operator.sub, "*": operator.mul, "/": midiv, "^": mipow,
}
 
if __name__ == '__main__':
    from time import time
    t1 = time()
    populate(ops)
    t2 = time()
    print "Tiempo: %g" % (t2-t1)
