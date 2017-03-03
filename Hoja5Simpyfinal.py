#Universidad del Valle de Guatemala
#Algoritmos y estructura de datos
#Ricardo Miranda 14027
#Emilio Diaz 15316
import simpy
import random
#Definicion de parametros y variables
mRam = 100
time_Total = 0.0
time = []
nProcess = 2
vel = 5.0     
numInt = 1
random.seed(10) 
env = simpy.Environment()
ram = simpy.Container(env, capacity=mRam, init=mRam)
cpu = simpy.Resource(env, capacity = 2)
wait = simpy.Resource(env, capacity =2)
def RAM(env, tiempo, nproceso, ram, Memoria, nInstrucciones, vel):
    global time
    global time_Total 
    yield env.timeout(tiempo)
    print ('%s Solicitando %d de RAM ' % ( nproceso, Memoria)) 
    tiempoReal = env.now
    yield ram.get(Memoria) 
    finished = 0
    #Cantidad de instrucciones
    while finished < nInstrucciones:
        with cpu.request() as ola_ke_ase:
            yield ola_ke_ase
            if (nInstrucciones - finished)>= vel:
                real=vel
            else:
                real=(nInstrucciones - finished)
            print ('%s Se realizaran  %d procesos' % (nproceso ,real))
            yield env.timeout(real/vel)

            finished = finished + real
            print ('%s en paquetes de %d se han completado %d instrucciones' % (nproceso, finished, nInstrucciones))

        cola = random.randint(1,2)

        if (cola == 1) and (finished<nInstrucciones):  
            
            with wait.request() as waiting:
                yield waiting
                yield env.timeout(1)
                print ('%s se han echo operaciones de entrada y salida' % ( nproceso))

    
    yield ram.put(Memoria)
    print ('%s se ha liberado la RAM con total de %d' % (nproceso, Memoria))
    time_Total += (env.now - tiempoReal)
    time.append(env.now - tiempoReal)
  
for i in range(nProcess):
    tiempo = random.expovariate(1.0 /numInt)
    nInstrucciones = random.randint(1,10)
    Memoria = random.randint(1,10) 
    env.process(RAM(env, tiempo, 'Proceso %d' %(i+1), ram, Memoria, nInstrucciones, vel))
env.run()
suma =0
promedio = 0
promedio = (time_Total/nProcess)
print ('El promedio de los tiempos de todos los procesos es de: %f segundos'%(promedio))
for cont in time:
    suma = suma +((cont-promedio)**2)
desv = (suma/(nProcess))**5
print('La desviacion estandar de los tiempos de todos los procesos es de: %f segundos' %(desv))
