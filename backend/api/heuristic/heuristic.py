import numpy as np
from pandas import DataFrame
import pandas as pd
from datetime import datetime,date
import sklearn
import random
import warnings
import copy
import time

mejor_pos_e=[]


class Particula:
    
    def __init__(self, n_variables, vector_variables, limites_inf=None, limites_sup=None,
                 verbose=False):

        
        self.n_variables = n_variables # Número de variables de la partícula
        self.limites_inf = limites_inf # Límite inferior de cada variable
        self.limites_sup = limites_sup # Límite superior de cada variable
        self.posicion = np.repeat(None, n_variables)  # Posición de la partícula
        self.velocidad = np.repeat(None, n_variables) # Velocidad de la parícula
        self.valor = np.repeat(None, 1) # Valor de la partícula
        self.mejor_valor = None  # Mejor valor que ha tenido la partícula hasta el momento
        self.mejor_posicion = None  # Mejor posición en la que ha estado la partícula hasta el momento
        
        # Si limites_inf o limites_sup no son un array numpy, se convierten en
        # ello.
        if self.limites_inf is not None         and not isinstance(self.limites_inf,np.ndarray):
            self.limites_inf = np.array(self.limites_inf)

        if self.limites_sup is not None         and not isinstance(self.limites_sup,np.ndarray):
            self.limites_sup = np.array(self.limites_sup)
        
        # ----------------------------------------------------------------------
        if self.limites_inf is not None         and len(self.limites_inf) != self.n_variables:
            raise Exception(
                
                )
        elif self.limites_sup is not None         and len(self.limites_sup) != self.n_variables:
            raise Exception(
                
                )
        elif (self.limites_inf is None) or (self.limites_sup is None):
            warnings.warn(
               
                )
        elif any(np.concatenate((self.limites_inf, self.limites_sup)) == None):
            warnings.warn(
                
            )

        
        # Si no se especifica limites_inf, el valor mínimo que pueden tomar las 
        # variables es -10^3.
        if self.limites_inf is None:
            self.limites_inf = np.repeat(-10**3, self.n_variables)

        # Si no se especifica limites_sup, el valor máximo que pueden tomar las 
        # variables es 10^3.
        if self.limites_sup is None:
             self.limites_sup = np.repeat(+10**3, self.n_variables)
            
        # Si los límites no son nulos, se reemplazan aquellas posiciones None por
        # el valor por defecto -10^3 y 10^3.
        if self.limites_inf is not None:
            self.limites_inf[self.limites_inf == None] = -10**3
           
        if self.limites_sup is not None:
            self.limites_sup[self.limites_sup == None] = +10**3
        
        # ----------------------------------------------------------------------
        if vector_variables==[]: 
            for i in np.arange(self.n_variables):
            # Para cada posición, se genera un valor aleatorio dentro del rango
            # permitido para esa variable.
                self.posicion[i] = random.uniform(
                                        self.limites_inf[i],
                                        self.limites_sup[i]
                                    )
        else: 
            for i in np.arange(self.n_variables):
            # Para cada posición, se genera un valor aleatorio dentro del rango
            # permitido para esa variable.
                self.posicion[i] = vector_variables[i]

        # LA VELOCIDAD INICIAL DE LA PARTÍCULA ES 0
        # ----------------------------------------------------------------------
        self.velocidad = np.repeat(0, self.n_variables)

        
    
    
    def __repr__(self):
        

        texto = "Partícula"                 + "\n"                 + "---------"                 + "\n"                 + "Posición: " + str(self.posicion)                 + "\n"                 + "Velocidad: " + str(self.velocidad)                 + "\n"                 + "Mejor posicion: " + str(self.mejor_posicion)                 + "\n"                 + "Mejor valor: " + str(self.mejor_valor)                 + "\n"                 + "Límites inferiores de cada variable: "                 + str(self.limites_inf)                 + "\n"                 + "Límites superiores de cada variable: "                 + str(self.limites_sup)                 + "\n"

        return(texto)

    def evaluar_particula(self, funcion_objetivo, optimizacion, verbose = False):
       

        # COMPROBACIONES INICIALES: EXCEPTIONS Y WARNINGS
        # ----------------------------------------------------------------------
        if not optimizacion in ["maximizar", "minimizar"]:
            raise Exception(
                "El argumento optimizacion debe ser: 'maximizar' o 'minimizar'"
                )

        # EVALUACIÓN DE LA FUNCIÓN OBJETIVO EN LA POSICIÓN ACTUAL
        # ----------------------------------------------------------------------
        self.valor = funcion_objetivo(*self.posicion)

        # MEJOR VALOR Y POSICIÓN
        # ----------------------------------------------------------------------
        # Se compara el valor actual con el mejor valor histórico. La comparación
        # es distinta dependiendo de si se desea maximizar o minimizar.
        # Si no existe ningún valor histórico, se almacena el actual. Si ya 
        # existe algún valor histórico se compara con el actual y, de ser mejor 
        # este último, se sobrescribe.
        
        if self.mejor_valor is None:
            self.mejor_valor    = np.copy(self.valor)
            self.mejor_posicion = np.copy(self.posicion)
        else:
            if optimizacion == "minimizar":
                if self.valor < self.mejor_valor:
                    self.mejor_valor    = np.copy(self.valor)
                    self.mejor_posicion = np.copy(self.posicion)
            else:
                if self.valor > self.mejor_valor:
                    self.mejor_valor    = np.copy(self.valor)
                    self.mejor_posicion = np.copy(self.posicion)

       

    def mover_particula(self, mejor_p_enjambre, inercia=0.8, peso_cognitivo=2,
                        peso_social=2, verbose=False):
        

        # ACTUALIZACIÓN DE LA VELOCIDAD
        # ----------------------------------------------------------------------
        componente_velocidad = inercia * self.velocidad
        r1 = np.random.uniform(low=0.0, high=1.0, size = len(self.velocidad))
        r2 = np.random.uniform(low=0.0, high=1.0, size = len(self.velocidad))
        componente_cognitivo = peso_cognitivo * r1 * (self.mejor_posicion                                                       - self.posicion)
        componente_social = peso_social * r2 * (mejor_p_enjambre                                                 - self.posicion)
        nueva_velocidad = componente_velocidad + componente_cognitivo                           + componente_social
        self.velocidad = np.copy(nueva_velocidad)
        
        # ACTUALIZACIÓN DE LA POSICIÓN
        # ----------------------------------------------------------------------
        self.posicion = self.posicion + self.velocidad

        
        # Se comprueba si algún valor de la nueva posición supera los límites
        # impuestos. En tal caso, se sobrescribe con el valor del límite
        # correspondiente y se reinicia a 0 la velocidad de la partícula en esa
        # componente.
        for i in np.arange(len(self.posicion)):
            if self.posicion[i] < self.limites_inf[i]:
                self.posicion[i] = self.limites_inf[i]
                self.velocidad[i] = 0

            if self.posicion[i] > self.limites_sup[i]:
                self.posicion[i] = self.limites_sup[i]
                self.velocidad[i] = 0


def funcion_objetivo(x_0):
    f= x_0
    return(f)


class Enjambre:
    

    def __init__(self, n_particulas, n_variables, vector_variables, limites_inf = None,
                 limites_sup = None, verbose = False):

        
        self.n_particulas = n_particulas # Número de partículas del enjambre
        self.n_variables = n_variables # Número de variables de cada partícula
        self.limites_inf = limites_inf # Límite inferior de cada variable
        self.limites_sup = limites_sup # Límite superior de cada variable
        self.particulas = [] # Lista de las partículas del enjambre
        self.optimizado = False # Etiqueta para saber si el enjambre ha sido optimizado
        self.iter_optimizacion = None  # Número de iteraciones de optimización llevadas a cabo
        self.mejor_particula = None  # Mejor partícula del enjambre
        self.mejor_valor = None # Mejor valor del enjambre
        self.mejor_posicion = None # Posición del mejor valor del enjambre
        self.historico_particulas = [] # Estado de todas las partículas del enjambre en cada iteración
        self.historico_mejor_posicion = []  # Mejor posición en cada iteración
        self.historico_mejor_valor = [] # Mejor valor en cada iteración.
        self.diferencia_abs = [] # Diferencia absoluta entre el mejor valor de iteraciones consecutivas.
        self.resultados_df = None # data.frame con la información del mejor valor y posición encontrado en
                                  # cada iteración, así como la mejora respecto a la iteración anterior.
        self.valor_optimo = None # Mejor valor de todas las iteraciones
        self.posicion_optima = None # Mejor posición de todas las iteraciones

        
        # Si limites_inf o limites_sup no son un array numpy, se convierten en
        # ello.
        if self.limites_inf is not None         and not isinstance(self.limites_inf,np.ndarray):
            self.limites_inf = np.array(self.limites_inf)

        if self.limites_sup is not None         and not isinstance(self.limites_sup,np.ndarray):
            self.limites_sup = np.array(self.limites_sup)

        # SE CREAN LAS PARTÍCULAS DEL ENJAMBRE Y SE ALMACENAN
        # ----------------------------------------------------------------------
        for i in np.arange(n_particulas):
            if vector_variables!=[]:
                particula_i = Particula(
                                n_variables = self.n_variables,
                                vector_variables=vector_variables,
                                limites_inf = self.limites_inf,
                                limites_sup = self.limites_sup,
                                verbose     = verbose
                              )
                self.particulas.append(particula_i)
                vector_variables=[]
            else:
                particula_i = Particula(
                            n_variables = self.n_variables,
                            vector_variables=[],
                            limites_inf = self.limites_inf,
                            limites_sup = self.limites_sup,
                            verbose     = verbose
                          )
                self.particulas.append(particula_i)

        

    def __repr__(self):
        

        texto = "============================"                 + "\n"                 + "         Enjambre"                 + "\n"                 + "============================"                 + "\n"                 + "Número de partículas: " + str(self.n_particulas)                 + "\n"                 + "Límites inferiores de cada variable: " + str(self.limites_inf)                 + "\n"                 + "Límites superiores de cada variable: " + str(self.limites_sup)                 + "\n"                 + "Optimizado: " + str(self.optimizado)                 + "\n"                 + "Iteraciones optimización: " + str(self.iter_optimizacion)                 + "\n"                 + "\n"                 + "Información mejor partícula:"                 + "\n"                 + "----------------------------"                 + "\n"                 + "Mejor posición actual: " + str(self.mejor_posicion)                 + "\n"                 + "Mejor valor actual: " + str(self.mejor_valor)                 + "\n"                 + "\n"                 + "Resultados tras optimizar:"                 + "\n"                 + "----------------------------"                 + "\n"                 + "Posición óptima: " + str(self.posicion_optima)                 + "\n"                 + "Valor óptimo: " + str(self.valor_optimo)
                
        return(texto)

    def mostrar_particulas(self, n=None):
        
        if n is None:
            n = self.n_particulas
        elif n > self.n_particulas:
            n = self.n_particulas

        for i in np.arange(n):
            print(self.particulas[i])
        return(None)

    def evaluar_enjambre(self, funcion_objetivo, optimizacion, verbose = False):
        
        global mejor_pos_e############################################################################################
        
        # SE EVALÚA CADA PARTÍCULA DEL ENJAMBRE
        # ----------------------------------------------------------------------
        for i in np.arange(self.n_particulas):
            self.particulas[i].evaluar_particula(
                funcion_objetivo = funcion_objetivo,
                optimizacion     = optimizacion,
                verbose          = verbose
                )

        
        self.mejor_particula =  copy.deepcopy(self.particulas[0])
        # Se comparan todas las partículas del enjambre.
        for i in np.arange(self.n_particulas):
            if optimizacion == "minimizar":
                if self.particulas[i].valor < self.mejor_particula.valor:
                    self.mejor_particula = copy.deepcopy(self.particulas[i])
            else:
                if self.particulas[i].valor > self.mejor_particula.valor:
                    self.mejor_particula = copy.deepcopy(self.particulas[i])

        # Se extrae la posición y valor de la mejor partícula y se almacenan
        # como mejor valor y posición del enjambre.
        self.mejor_valor    = self.mejor_particula.valor
        self.mejor_posicion = self.mejor_particula.posicion

        # INFORMACIÓN DEL PROCESO (VERBOSE)
        # ----------------------------------------------------------------------
        if verbose:
            #print("-----------------")
            #print("Enjambre evaluado")
            #print("-----------------")
            #print("Mejor posición encontrada : " + str(self.mejor_posicion))
            a=self.mejor_posicion
            #print("MEjor posición en lista:", a.tolist())
            mejor_pos_e=a.tolist()
            # np.savetxt("Mejor_pos_E.csv", self.mejor_posicion, delimiter=",")#############################
            #print("Mejor valor encontrado : " + str(self.mejor_valor))
            #print("")

    def mover_enjambre(self, inercia, peso_cognitivo, peso_social,
                       verbose = False):
        

        # Se actualiza la posición de cada una de las partículas que forman el
        # enjambre.
        for i in np.arange(self.n_particulas):
            self.particulas[i].mover_particula(
                mejor_p_enjambre = self.mejor_posicion,
                inercia          = inercia,
                peso_cognitivo   = peso_cognitivo,
                peso_social      = peso_social,
                verbose          = verbose
            )

        # Información del proceso (VERBOSE)
        # ----------------------------------------------------------------------
        #if verbose:
            #print("---------------------------------------------------------" \
                  #"------------")
            #print("La posición de todas las partículas del enjambre ha sido " \
                  #"actualizada.")
            #print("---------------------------------------------------------" \
            #"------------")
            #print("")


    def optimizar(self, funcion_objetivo, optimizacion, n_iteraciones = 50,
                  inercia = 0.8, reduc_inercia = True, inercia_max = 0.9,
                  inercia_min = 0.4, peso_cognitivo = 2, peso_social = 2,
                  parada_temprana = False, rondas_parada = None,
                  tolerancia_parada  = None, verbose = False):
        
        global mejor_pos_e############################################################################################
        
        # COMPROBACIONES INICIALES: EXCEPTIONS Y WARNINGS
        # ----------------------------------------------------------------------
        # Si se activa la parada temprana, hay que especificar los argumentos
        # rondas_parada y tolerancia_parada.
        if parada_temprana         and (rondas_parada is None or tolerancia_parada is None):
            raise Exception(
                "Para activar la parada temprana es necesario indicar un " \
                + " valor de rondas_parada y de tolerancia_parada."
                )
        
        # Si se activa la reducción de inercia, hay que especificar los argumentos
        # inercia_max y inercia_min.
        if reduc_inercia         and (inercia_max is None or inercia_min is None):
            raise Exception(
            "Para activar la reducción de inercia es necesario indicar un " \
            + "valor de inercia_max y de inercia_min."
            )

        # ITERACIONES
        # ----------------------------------------------------------------------
        start = time.time()

        for i in np.arange(n_iteraciones):
           
            # EVALUAR PARTÍCULAS DEL ENJAMBRE
            # ------------------------------------------------------------------
            self.evaluar_enjambre(
                funcion_objetivo = funcion_objetivo,
                optimizacion     = optimizacion,
                verbose          = verbose
                )

            # SE ALMACENA LA INFORMACIÓN DE LA ITERACIÓN EN LOS HISTÓRICOS
            # ------------------------------------------------------------------
            self.historico_particulas.append(copy.deepcopy(self.particulas))
            self.historico_mejor_posicion.append(copy.deepcopy(self.mejor_posicion))
            self.historico_mejor_valor.append(copy.deepcopy(self.mejor_valor))

            # SE CALCULA LA DIFERENCIA ABSOLUTA RESPECTO A LA ITERACIÓN ANTERIOR
            # ------------------------------------------------------------------
            # La diferencia solo puede calcularse a partir de la segunda
            # iteración.
            if i == 0:
                self.diferencia_abs.append(None)
            else:
                diferencia = abs(self.historico_mejor_valor[i]                                  - self.historico_mejor_valor[i-1])
                self.diferencia_abs.append(diferencia)

            
            if parada_temprana and i > rondas_parada:
                ultimos_n = np.array(self.diferencia_abs[-(rondas_parada): ])
                if all(ultimos_n < tolerancia_parada):
                    #print("Algoritmo detenido en la iteracion " 
                          #+ str(i) \
                          #+ " por falta cambio absoluto mínimo de " \
                          #+ str(tolerancia_parada) \
                          #+ " durante " \
                          #+ str(rondas_parada) \
                          #+ " iteraciones consecutivas.")
                    break
            
            
            if reduc_inercia:
                inercia = ((inercia_max - inercia_min)                           * (n_iteraciones-i)/n_iteraciones)                           + inercia_min
           
            self.mover_enjambre(
               inercia        = inercia,
               peso_cognitivo = peso_cognitivo,
               peso_social    = peso_social,
               verbose        = False
            )

        end = time.time()
        self.optimizado = True
        self.iter_optimizacion = i
        
        # IDENTIFICACIÓN DEL MEJOR PARTÍCULA DE TODO EL PROCESO
        # ----------------------------------------------------------------------
        if optimizacion == "minimizar":
            indice_valor_optimo=np.argmin(np.array(self.historico_mejor_valor))
        else:
            indice_valor_optimo=np.argmax(np.array(self.historico_mejor_valor))

        self.valor_optimo    = self.historico_mejor_valor[indice_valor_optimo]
        self.posicion_optima = self.historico_mejor_posicion[indice_valor_optimo]
        
        # CREACIÓN DE UN DATAFRAME CON LOS RESULTADOS
        # ----------------------------------------------------------------------
        self.resultados_df = pd.DataFrame(
            {
            "mejor_valor_enjambre"   : self.historico_mejor_valor,
            "mejor_posicion_enjambre": self.historico_mejor_posicion,
            "diferencia_abs"         : self.diferencia_abs
            }
        )
        self.resultados_df["iteracion"] = self.resultados_df.index
        
        
        a=self.posicion_optima  ##############################################################            
        mejor_pos_e=a.tolist()  ##############################################################
        #print("Valor óptimo: " + str(self.valor_optimo))
        #print("")


def Pso(device, real_consumption):
    current_consumption = real_consumption.consumption_amount
    
    if current_consumption != 0:
        limites_inf_ = device.min_c
        limites_sup_ = device.max_c
    else:
        limites_inf_ = 0
        limites_sup_ = 0
    
    # Crear enjambre
    enjambre = Enjambre(
                   n_particulas = 1000,
                   n_variables = 1,
                   vector_variables = [current_consumption],
                   limites_inf = [limites_inf_],
                   limites_sup = [limites_sup_],
                   verbose = True
                )

    enjambre.evaluar_enjambre(
        funcion_objetivo = funcion_objetivo,
        optimizacion     = "minimizar",
        verbose          = True
        )
    
    enjambre.mover_enjambre(
        inercia          = 0.8,
        peso_cognitivo   = 2,
        peso_social      = 2,
        verbose          = True
    )

    enjambre.evaluar_enjambre(
        funcion_objetivo = funcion_objetivo,
        optimizacion     = "minimizar",
        verbose          = True
        )
    
    enjambre.optimizar(
        funcion_objetivo = funcion_objetivo,
        optimizacion     = "minimizar",
        n_iteraciones    = 25,
        inercia          = 0.8,
        reduc_inercia    = True,
        inercia_max      = 0.9,
        inercia_min      = 0.4,
        peso_cognitivo   = 1,
        peso_social      = 2,
        parada_temprana  = True,
        rondas_parada    = 5,
        tolerancia_parada = 10**-3,
        verbose          = False
    )
    return mejor_pos_e

def execute_heuristic(device, real_consumption):
    [pso_result] = Pso(device=device, real_consumption=real_consumption)

    optimized_consumption = {
        'consumption_datetime': real_consumption.consumption_datetime,
        'consumption_amount': pso_result
    }

    return optimized_consumption
