
import simpy
import random
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




