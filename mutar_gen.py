import random

def mutarGen(hijosMutar, mutGen):        
        print("Mutacion gen: ")
        for i in hijosMutar:
            bitsMutar = list(i[1])
            
            mutarBitAux = ""
            for index in range(len(bitsMutar)):
                probabilidadMutacionGen = (random.randint(1, 100)) / 100

                if probabilidadMutacionGen <= mutGen:
                    if bitsMutar[index] == "0":
                        bitsMutar[index] = "1"
                        mutarBitAux+=bitsMutar[index]
                    else:
                        bitsMutar[index] = "0"
                        mutarBitAux+=bitsMutar[index]
                else:
                    mutarBitAux+=bitsMutar[index]

            i[1] = mutarBitAux        
        
        return hijosMutar