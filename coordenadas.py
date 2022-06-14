from math import sin, cos, tan
import math


def calcularNumABits(listaIndividuos):
    print("\nRecalculandor valor bits")
    for i in range(len(listaIndividuos)):
        listaIndividuos[i][2] = int( str(listaIndividuos[i][1]) , 2)
    return listaIndividuos

def calcularCoordenadas(listaIndividuos, rangoInicio, presicion, funcion):
    print("calculando coordenadas")
    
    coordenadasOrdenado = []
    for i in listaIndividuos:              
        xiFun = float( rangoInicio + (float(i[2]) * presicion) )            
        x = xiFun #se usa dentro de eval como expresion regular
        fxFun = eval(funcion)        
        coordenadasOrdenado.append( [ i[0], xiFun, fxFun, i[1] ] )

    listaIndividuos = sorted(coordenadasOrdenado, key=lambda individuo: individuo[2], reverse=True)

    print("\nCordenada calculada:")
    """ for x in listaIndividuos:
        print(x) """
    
    return listaIndividuos












def calcularCoordenadas2(self, listaIndividuos, tipoGrafico):

        coordenadasOrdenado = []

        rangoInicio = int(self.rangoInicioText.text())
        presicion = float(self.precisionText.text())
        funcion = self.FuncionText.text()                

        for i in listaIndividuos:              
            xiFun = float( rangoInicio + (float(i[2]) * presicion) )            
            x = xiFun #se usa dentro de eval como expresion regular
            fxFun = eval(funcion)
            
            coordenadasOrdenado.append( [xiFun, fxFun, i[1]] )

        listaIndividuos = sorted(coordenadasOrdenado, key=lambda individuo: individuo[1], reverse=True)

        if tipoGrafico == "historico":
            """ Limpio - historico"""            
            
            maximoCoord = float(listaIndividuos[0][1])
            minimoCoord = float( listaIndividuos[ len(listaIndividuos)-1 ][1] )

            promedio = 0.0
            for x in range( len(listaIndividuos) ):
                promedio += listaIndividuos[x][1]
            promedioCord = promedio / len(listaIndividuos)
            
            xiFun = maximoCoord
            x = xiFun #se usa dentro de eval como expresion regular
            fxFun = eval(funcion)
                        
            self.MEJORES_GENERACION.append([self.ITERACION_GENERACION, fxFun])        

            xiFun = minimoCoord
            x = xiFun #se usa dentro de eval como expresion regular
            fxFun = eval(funcion)
            self.PEORES_GENERACION.append([self.ITERACION_GENERACION, fxFun])

            xiFun = promedioCord
            x = xiFun #se usa dentro de eval como expresion regular
            fxFun = eval(funcion)
            self.PROMEDIO_GENERACION.append([self.ITERACION_GENERACION, fxFun])
            
            #coordenadasOrdenado = sorted(coordenadasOrdenado, key=lambda xCoord: xCoord[0], reverse=False) # menor -mayor en x

            xImax = []
            fXmax = []
            
            xImin = []
            fXmin = []

            fXprom = []
            xIprom = []

            if int(self.ITERACION_GENERACION) == int(self.numGeneracionText.text()) : #int( self.numGeneracionText()
                print("\nCoordenadas para graficar")
                print(" mejor")
                for coor in self.MEJORES_GENERACION:
                    print(str(coor))
                    xImax.append(coor[0])
                    fXmax.append(coor[1])            
                print(" peor")
                for coor in self.PEORES_GENERACION :
                    print(str(coor))
                    xImin.append(coor[0])
                    fXmin.append(coor[1])

                print(" prom: ")
                for coor in self.PROMEDIO_GENERACION:
                    print(coor)
                    promedio = coor[1]
                    xIprom.append( coor[0] )
                    fXprom.append(promedio)
                                
                self.graficarDatos(xImax, fXmax, xImin, fXmin, xIprom, fXprom, [], [])
                #self.graficarDatos(xImin, fXmin)
                self.ITERACION_GENERACION = 1

            else:
                #print("menor a iteracion")
                self.ITERACION_GENERACION +=1
            """ Fin historico """
        if (tipoGrafico == "podaMax" or tipoGrafico == "podaMin"):
            #print("Poda")
            if tipoGrafico == "podaMax":
                listaIndividuos = sorted(listaIndividuos, key=lambda individuo: individuo[1], reverse=True)                

            if tipoGrafico == "podaMin":                
                listaIndividuos = sorted(listaIndividuos, key=lambda individuo: individuo[1], reverse=False)

            listaPodTempMax = []
            xPoda = []
            yPoda = []
            
            print("Nueva generacion: \n")
            
            for index in range(len(listaIndividuos)):                                
                if index < int(self.poblacionMaximaText.text()):

                    #print( str(index) , str(listaIndividuos[index]))
                    listaPodTempMax.append(listaIndividuos[index])
                    xPoda.append(listaIndividuos[index][0])
                    yPoda.append(listaIndividuos[index][1])
                    self.NUEVA_GENERACION.append( [ index, listaIndividuos[index][2], int( listaIndividuos[index][2],2 ) ] )

                    print( str(index), str(listaIndividuos[index][2]), str( int( listaIndividuos[index][2],2 )) )

                    #print("bits: "+ str(listaIndividuos[index][2]))
                """ else:
                    print("fuera de limite de poblacion") """

            self.graficarDatos([], [], [], [], [], [], xPoda, yPoda)
