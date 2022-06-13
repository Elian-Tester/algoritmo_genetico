import random


def generarBinario(poblacion, precision, rangoinicio, rangofin):     
    print("Generando binarios")

    rangoPrecision = (rangofin - rangoinicio) / precision
        
    numDeBits = numBits(rangoPrecision)
    
    numeroBin=0
    arrayBits = []

    for x in range(int(poblacion)):
        numeroBin = random.randint(1, int(rangoPrecision))                        
        temp = format(numeroBin, "b")            
            
        binarioArrayTemp=[x, temp, numeroBin] #identificador A-B-C...w
        arrayBits.append(binarioArrayTemp)    #enviar "numeroBin" es el random para el binario

    return [arrayBits, numDeBits, rangoPrecision]


def numBits(rango):        
        bitsTemp = 0
        conta=0
        while (rango >= bitsTemp):
            conta+=1
            bitsTemp = 2**conta            
        #self.numBitsLabel.setText(str(conta))
        return conta

def completarNumBit( arrayBit, numDeBits):
        
        binariosGeneradosFinales = ""
        for dato in arrayBit:            
            faltaanCeros = numDeBits - len(dato[1])            

            datoAux = dato[1]
            dato[1]=""

            for x in range(0,faltaanCeros):
                dato[1] += "0"
            
            dato[1] += datoAux
            
            binariosGeneradosFinales += str(dato[0])+" : "+str(dato[1]) + " <-> " +str(dato[2])
            binariosGeneradosFinales += "\n"

        #self.binariosGeneradosLabel.setText(binariosGeneradosFinales)
        return arrayBit