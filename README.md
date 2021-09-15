# Forecasting_and_Genetic_algorithms

 Primer diseño de un codigo para hacer prediccion en series de tiempo, haciendo uso de los algortimos geneticos en la parte de optimizacion

## Algortimos genéticos

Un algoritmo genético trata de replicar el modelo de selección natural que propuso Darwin. Este modelo básicamente dice que, dentro de una población, los individuos que sobreviven son aquellos que están más adaptados al medio.

Es por esto que los individuos que se reproducen dando lugar a descendencia con sus genes son los que están mejor adaptados. Por lo tanto, las generaciones están cada vez mejor adaptadas pues son combinación de los mejores genes de las generaciones anteriores.

Además, esta teoría de la evolución introduce un concepto muy interesante que son las mutaciones. Una mutación es un pequeño cambio que se produce de manera aleatoria en ciertos individuos e introduce de esta manera versatilidad en las poblaciones. Habrá mutaciones que den lugar a cambios favorables y otros desfavorables.

### Estructura de un algoritmo genético

Para poder explicar la estructura de los algoritmos genéticos primero es necesario explicar algunos términos que serán útiles:

- Genes: Son las caracteristicas de cada inviduo, que en nuestro caso se representan por los valores que hay dentro de un vector.
- Individuo:  los individuos de nuestra población son las posibles soluciones al problema que estamos tratando. Se representan como un vectoy unidimensional con un tamaño igual a que se definio para el numero de Genes de todos los individuos.
- Población: conjunto de individuos (soluciones). Se representa como una matrix de todos los vectores de los individuos
- Función fitness o de adaptación: función que evalúa a los individuos y les asigna una puntuación en función de lo buenas soluciones que sean para el problema.
- Función de cruce: función que, dados dos individuos, genera dos ‘descendientes’ a partir de la combinación de genes de sus ‘padres’. Esta función se diseña especialmente para el problema que se esté tratando y, por lo general, se encarga de que los hijos sean mejores soluciones que los padres. En nuestro ejemplo utilizamos una funcion de cruce que se denomina elitista en donde se les da mayor probabilidad de cruce a los padres con un mejor resultado de la funcion de fitness.

Entonces, la estructura de un algoritmo genético es la siguiente:

- Se genera una población inicial de individuos (soluciones), usualmente de manera aleatoria.
- Fase de evaluación: se evalúan los individuos de la población con la función fitness.
- Fase de selección: se seleccionan los mejores individuos.
- Fase de reproducción: se cruzan los individuos seleccionados mediante la función de cruce, dando lugar a una nueva generación que va a sustituir a la anterior. 
- Fase de mutación: se introducen mutaciones (pequeños cambios) en ciertos individuos de la nueva población de manera aleatoria.
- Tenemos una nueva generación, generalmente, con soluciones mejores que la anterior. Volvemos al punto 2.

Los algoritmos genéticos finalizan o bien cuando alcanzan un número de generaciones concreto o cuando cumplen una condición de parada.

## Metodo de prediccion (Holt-Winters)

El método Holt-Winters es una ampliación perfeccionada del enfoque de la suavización exponencial, mientras que el procedimiento de suavización proporciona una impresión general, movimientos a largo plazo en la información y permite la elaboración de pronósticos a corto plazo. Este método permite también el estudio de tendencia a futuro mediante la elaboración de pronósticos a mediano y largo plazo. Para mas informacion se puede revisar dar click en el siguiente [enlace](http://cienciauanl.uanl.mx/?p=7948)


