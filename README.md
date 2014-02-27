cuatros
=======

Desafio programando.com

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

