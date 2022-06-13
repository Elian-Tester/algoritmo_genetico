#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ast import arg
import sys
from turtle import color

#Importar aquí las librerías a utilizar
import matplotlib.pyplot as plt
import random
from math import sin, cos, tan
import math
import cv2

from PyQt5 import uic, QtWidgets
import numpy
from pymysql import NULL

import bits
import mutar_gen
import coordenadas

qtCreatorFile = "vista.ui" #Aquí va el nombre de tu archivo


Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    ID_IMAGES=0
    MEJORES_GENERACION = []
    PEORES_GENERACION = []
    PROMEDIO_GENERACION = []
    
    NUEVA_GENERACION = []
    ITERACION_GENERACION = 1
    BANDERA_MAX = True
    BANDERA_FIN_HISTORICO = False
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        #self.boton1.clicked.connect(self.setPlot)
        self.boton2.clicked.connect(self.setTexto)
        #self.enviar.clicked.connect(self.getTexto)
        self.CalcularBoton.clicked.connect(self.generaciones)


    def setPlot(self):
        print("mat plot lib")
        x=[3.6  ,3.6  ,5      ,5.4   ,6,6.1  ,6.2  ,6.2 ]
        y=[-5.74,-5.74, -23.97,-22.53,-10.06,-6.78,-3.19,-3.19]

        plt.plot(x,y, label='linear')        
        plt.legend()
        plt.show()

    def setTexto(self):
        print("texto en caja")        
        self.poblacionInicialText.setText("4")
        self.precisionText.setText("0.001")
        self.rangoInicioText.setText("-4")
        self.rangoFinText.setText("4")
        self.poblacionMaximaText.setText("8")
        self.decendenciaText.setText("0.90")
        self.mutacionIndividuoText.setText("0.2")
        self.mutacionGenText.setText("0.2")
        self.numGeneracionText.setText("2")
        self.FuncionText.setText("0.75*cos(1.50*x)*sin(1.50*x)-0.25*cos(0.25*x) ")
        

    def generaciones(self):        

        print("Generaciones")
        generaciones = int(self.numGeneracionText.text())
        for num in range(generaciones):
            #print("\nGeneracion: "+ str( num ))
            arrayBits = self.NUEVA_GENERACION

            if ( len(self.NUEVA_GENERACION) == 0):
                datos = self.Calcular()
                
                binario_completar = bits.generarBinario(datos[0], datos[1], datos[2], datos[3])
                self.CantidadSolucionesLabel.setText(str(binario_completar[2]+1))

                arrayBits = bits.completarNumBit(binario_completar[0], binario_completar[1])

            seleccion_data = self.seleccionTcT(arrayBits)            

            cruza_result = self.cruza(seleccion_data[0], seleccion_data[1])

            muta_result = self.mutacion(cruza_result[0], cruza_result[1])

            
            limpiado = self.limpieza( muta_result[0], muta_result[1] )
            
            limpiado = self.tipo_grafica(limpiado, self.maximoRadio.isChecked(), self.minimoRadio.isChecked())

            self.guardarHistoricio( limpiado[1] )
                

            if limpiado[0]:
                print("Hay poda")
            else:
                print("No hay poda")


    def Calcular(self):
        print("Datos obtenidos")

        poblacionInicial = self.poblacionInicialText.text()
        precision = self.precisionText.text()        
        rangoInicio = self.rangoInicioText.text()
        rangoFin = self.rangoFinText.text()

        return [poblacionInicial, float(precision), int(rangoInicio),int(rangoFin)]



    def seleccionTcT(self, arrayBits):
        print("\nTodos con Todos : ____________________________________________________")
        for x in arrayBits:
            print(x)
        #print( self.NUEVA_GENERACION)
        if ( len(self.NUEVA_GENERACION) > 0 ):
            arrayBits = self.NUEVA_GENERACION
            self.NUEVA_GENERACION = []

        seleccion=[]        

        auxDisminuir=1
        for x in range(0,len(arrayBits)):

            for j in range(auxDisminuir, len(arrayBits)):
                probabilidadDesendencia = (random.randint(1, 100)) / 100
                corteCruza = random.randint(1, len(arrayBits[x][1]) - 1 )
                combinacion=[x, j, probabilidadDesendencia, corteCruza]                
                seleccion.append(combinacion)        
            auxDisminuir+=1
        print("\nSeleccion TcT:")
        for x in seleccion:
            print(x)        

        probabDecendencia = self.decendenciaText.text()        

        for x in seleccion:
            if x[2] >= float(probabDecendencia):
                seleccion.remove(x)
        
        return [seleccion, arrayBits]

    def cruza(self, seleccion, arrayBits):
        print("Cruza")
        hijosCruza = []

        for datoBin in seleccion:
            # Identificadores

            idA = str(arrayBits[datoBin[0]][0]) #id del binario original
            idB = str(arrayBits[datoBin[1]][0]) #id del binario original

            # binario a arreglo
            hijo1 = list(arrayBits[datoBin[0]][1])
            hijo2 = list(arrayBits[datoBin[1]][1])

            rang1 = int(datoBin[3]) #punto corte
            rang2 = len(str(arrayBits[datoBin[0]][1]))
            #print(rang2)

            corteA = ""
            corteA1 = ""
            for corte1 in range( 0, rang2):
                if corte1 >= rang1:
                    corteA+=hijo1[corte1]
                else:
                    corteA1+=hijo1[corte1]


            corteB = ""
            corteB1 = ""
            for corte2 in range( 0, rang2):
                if corte2 >= rang1:
                    corteB+=hijo2[corte2]
                else:
                    corteB1+=hijo2[corte2]
                                        
            hijoA = corteA1 + corteB
            hijoB = corteB1 + corteA
            
            
            hijosCruza.append([idA+idB+"-1" , hijoA])
            hijosCruza.append([idA+idB+"-2" , hijoB])

        return [hijosCruza, arrayBits]

    def mutacion(self, listHijosCruza, arrayBits):
        print("Mutacion: ")
        mutacionIndividuo = self.mutacionIndividuoText.text()

        #print("mutacion individuo: "+mutacionIndividuo)        

        for individuo in listHijosCruza:
            probabilidadMutacionIndividuo = (random.randint(1, 100)) / 100
            individuo.append(probabilidadMutacionIndividuo)

        hijosMutacion = []

        for indiv in listHijosCruza:            
            if indiv[2] <= float(mutacionIndividuo):
                hijosMutacion.append(indiv)

        hijosMutados = mutar_gen.mutarGen(hijosMutacion, float(self.mutacionGenText.text()) )

        #print("regresar hijos mutados a lista principal de seleccion")
        for indice in range( len(listHijosCruza) ):
            for indiceMut in hijosMutados:                
                if listHijosCruza[indice][0] == indiceMut[0]:                    
                    listHijosCruza[indice][1] = indiceMut[1]
                
        
        for indiv in range(0, len(listHijosCruza)):            
            binario = listHijosCruza[indiv][1]
            valor = int(binario, 2)            

            listHijosCruza[indiv].append(valor)        
        
        return [listHijosCruza, arrayBits]

    def limpieza(self, listHijos, arrayBits):
        print("\nlimpieza: ")
        for x in listHijos:
            print(x)        

        rango = float(self.CantidadSolucionesLabel.text()) - 1        

        for hijo in listHijos:
            if hijo[3] <= rango:                
                arrayBits.append([ hijo[0] , hijo[1], hijo[3]])  #arrayBits (contiene a los padres) y se está agregando los hijos dentro del rango a los padres
        
        print("\narray bits (dentro de rango)")
        for x in arrayBits:
            print(x)

        poblacionMaxima = self.poblacionMaximaText.text()
        
        return self.verificarPODA(arrayBits, poblacionMaxima )

    def verificarPODA(self, arrayBits, poblacionMaxima ):
        print("\nVerificando PODA: ")        
        arrayBits = coordenadas.calcularNumABits(arrayBits)
        
        print("\nnum bit recalculado:")
        for x in arrayBits:
            print(x)

        rangoInicio = int(self.rangoInicioText.text())
        presicion = float(self.precisionText.text())
        funcion = self.FuncionText.text()
        arrayBits = coordenadas.calcularCoordenadas(arrayBits, rangoInicio, presicion, funcion)
            
        if len(arrayBits) > int(poblacionMaxima) :
            #print("\nNos vamos a PODA")            
            return [True, arrayBits]
        else:            
            #print("\nNo ocupa PODA ")            
            return [False, arrayBits]
    
    def guardarHistoricio(self, individuos_totales ):
        print("\nGuarda para historico:")
        for x in individuos_totales:
            print(x)

        maximo = individuos_totales[0][2]
        minimo = individuos_totales[-1][2]
        promedio = numpy.mean([x[2] for x in individuos_totales])

        self.MEJORES_GENERACION.append(maximo)
        self.PEORES_GENERACION.append(minimo)
        self.PROMEDIO_GENERACION.append(promedio)

        print( "\nMax: ", str(maximo) )
        print( "Min: ", str(minimo) )
        print( "Prom: ", str(promedio) )

    def tipo_grafica(self, limpiado, RadioMax, RadioMin):
        if ( RadioMax==False and RadioMin==False ):
            self.BANDERA_MAX = True                
            limpiado[1] = sorted( limpiado[1], key=lambda individuo: individuo[2], reverse=True)

        else:
            if RadioMax:                    
                self.BANDERA_MAX = True                    
                limpiado[1] = sorted( limpiado[1], key=lambda individuo: individuo[2], reverse=True)

            if RadioMin :
                self.BANDERA_MAX = False                    
                limpiado[1] = sorted( limpiado[1], key=lambda individuo: individuo[2], reverse=False)                    
        
        return limpiado


if __name__ == "__main__":
    app =  QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    app.exec_() #evita cerrar la ventana