# Solucion de fuerza bruta, considerando tambien que
# para generar las distintas expresiones no es necesario muchos
# niveles de recursion y que ellas seran faciles de regenerar
#
# Se toman varios nros mas sus versiones en string.
# Se generan 2 listas, la lista de los nros involucrados y las operaciones que 
# permitieron generar # el nro. en cuestion.
# Por ejemplo:
#       [ "4", "4", "4", "4" ] y ["+","+","+","+"]
#
# si se inicia con 0 genera el 16
#         0 + 4 + 4 + 4 + 4 = 16
#
# o tambien se puede generar asi:
#       [ "4", "4", "4", "r(4)" ] y [ "-", "-", "+", "^" ]
#
#         ( 0 - 4 - 4 + 4 ) ^ r(4) = (-4)^2 = 16
#
# y como se sabia que habia que parentizar?
#
# Se sabe pues el backtrack consulta todas las alternativas de izquierda a derecha
# y va calculando lo que ya lleva de izquierda a derecha, por tanto la reconstruccion 
# de las expresiones DEBE parentizar para imitar al backtrack y llegar al mismo resultado.
#
# Esta solucion no es generica. Solo resuelve el caso 1-100 con exito.
# Una alternativa generica podria constuir las expresiones al estilo de Dynamic Programming
# i.e. bottom up, para no morir en la recursion
#
# El usar este arreglo en vez de ir formando la expresion en medio del backtrack permite
# ser mas veloz, pues no hay operaciones de strings superfluas
#
# rodrigo.chappa@gmail.com
# http://goo.gl/SAaM48

FARAWAY = -9999     # Nro feo que hace ignorar resultados intermedios inutiles
FERROR  = 0.00001
LIMITE  = 100

import operator

# midiv(x,y) = x/y
def midiv(x,y): 
    if y == 0: return FARAWAY
    return float(x) / float(y)

# miexp(x,y) = x^y
# Numeros gigantescos eliminados, pues no se requieren para estos calculos
def miexp(x,y): 
    if type(x) != int or type(y) != int: return FARAWAY
    if x > 20 or y > 20: return FARAWAY
    return x**y

# mipegador("4","4") -> "44"
# El backtrack es ciego e intenta usar el operador de pegado con expresiones incluso
# asi que aqui detenemos algunos intentos inutiles
def mipegador(x,y): 
    if x != 4 or y != 4: return FARAWAY
    return int(str(int(x))+str(int(y)))

from math import sqrt

#               4  4!  0.44444  0.4 2  sqrt(0.4444)
values      = [ 4, 24, 4.0/9.0, .4, 2, sqrt(4.0/9.0) ] 
values_str1 = [ "4", "4!", ".4'", ".4", "r(4)", "r(.4')"  ]
op          = [ operator.sub, operator.add, operator.mul, midiv, miexp, mipegador ]
opstr       = [ "-", "+", "*", "/", "^", "_" ]

# Si reemplaza el uso de values_str por values_str2 mas abajo, se puede evaluar las expresiones
# descomentando el "eval" que aparece tambien mas abajo
values_str2 = [ "4", "24.0", "(4.0/9.0)", "0.4", "2.0", "sqrt(4.0/9.0)" ]

values_str = values_str1

def mytry( stack, operaciones, sofar, solution ):
   if len(solution) == LIMITE: return

#   print "DBG ", "stack", stack, "op", operaciones, "sofar", sofar, "stack currlen =", len(stack), "esta en cache", int(sofar) in solution
   if len(stack) == 4:
      dif = sofar - int(sofar+0.5)
      if dif < 0: dif = -dif
      if dif < FERROR:
         sofar = int(sofar+0.5)
         if sofar > 0 and sofar <= LIMITE and sofar not in solution:
            solution[sofar] = { "stack":list(stack), "op":list(operaciones) }
            # print "solution[",sofar,"] =", solution[sofar]
      return
   
   # El backtrack necesita recordar este valor
   prevsofar = sofar
   # Fuerza bruta, evaluar todas las posibilidades que se muestran en lista "values"
   for i in range(len(values)):
       stack.append(values_str[i])
       # .. aplicando todas las operaciones que se muestran en lista "op"
       for j in range(len(op)):
           if len(operaciones) == 0 and j >= 2: continue
           operaciones.append(opstr[j])
           sofar = op[j](prevsofar,values[i])
           # print " "*j, opstr[j], "(prev:",prevsofar,"val",values[i],") =", sofar
           mytry( stack, operaciones, sofar, solution )
           operaciones.pop()
       stack.pop()

def solve():
   solution = {}
   mytry( [], [], 0, solution )
   print "Solucion muestra", len(solution), "numeros y sus expresiones"
   # Si hay algun nro que no se ha calculado, se muestra aqui
   noestan = []
   for i in range(1,LIMITE+1):
       if i not in solution:
          noestan.append(i)
   if len(noestan) > 0: print "Problemas. No estan:", noestan
   return solution

# Parece mas dificil imprimir la solucion que obtenerla
def printsol(n,sol_n):
    print n,"=",

    exp = ""
    prev_op = ""
    for i in range(4):
       curr_op = sol_n['op'][i]
       # No se escribe el operador si es un + al inicio (por superfluo)
       # Siempre se escribe si no es al inicio
       if i > 0 or curr_op != "+": 
          parentizar = False
          if curr_op == "^": 
             parentizar = True
          # El backtrack se aplico de izq a derecha
          # Si se aplico un "*" o un "/" y antes habia un "+" o un "-", estos DEBEN parentizarse
          if (i>1 and (curr_op in ["*","/"] and prev_op in ["+","-"])): 
             parentizar = True
          if parentizar:
             exp = "(" + exp + ")"
          # Si se trata del operador de pegado, no hacemos nada y con eso se pega: 4_4 -> 44
          if curr_op != "_":
             exp += curr_op
       exp += sol_n['stack'][i] 
       prev_op = curr_op

    # Descomente aqui para evaluar las expresiones y comprobar que ellas efectivamente generan
    # el numero asociado. (Hay que hacer values_str = values_str2 mas arriba tambien
    #evalexp = int(eval(exp.replace("^","**"))+FERROR) 
    #print exp, "->", evalexp, evalexp == n
    for i in range(1,10):
        if i == 4: 
           assert( exp.count(str(i)) == 4 )    # Comprobar que hay 4 4s
        else:
           assert( exp.count(str(i)) == 0 )    # y no hay ningun otro numero
    print exp

def showsolution(solution):
   for s in sorted(solution.keys()):
       printsol( s, solution[s] )

if __name__ == '__main__':
   from time import time
   inicio = time()
   sol = solve()
   showsolution(sol)
   fin = time()
   print('Tiempo total %g' % (fin - inicio))

