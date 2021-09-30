#modications of https://github.com/SJTU-IPADS/ServerlessBench/tree/master/Testcase1-Resource-efficiency
from random import randint
import time
import os
from multiprocessing import Process, Pipe

minLoopTime = 1000000
maxLoopTime = 3000000

minParallelIndex = 60
maxParallelIndex = 120

def function_handler(event, context):

    loopTime = randint(minLoopTime, maxLoopTime)
    return alu_handler(loopTime)



def alu_handler(loopTime):
    parallelIndex = randint(minParallelIndex, maxParallelIndex)
    temp = alu(loopTime, parallelIndex)
    return {'statusCode':200, 'body':'AWS'}

def doAlu(times, childConn, clientId):
    a = randint(10, 100)
    b = randint(10, 100)
    temp = 0
    for i in range(times):
        if i % 4 == 0:
            temp = a + b
        elif i % 4 == 1:
            temp = a - b
        elif i % 4 == 2:
            temp = a * b
        else:
            temp = a / b
    print('my time: ',times)
    childConn.send(temp)
    childConn.close()
    return temp

def alu(times, parallelIndex):
    per_times = int(times / parallelIndex)
    threads = []
    childConns = []
    parentConns = []
    for i in range(parallelIndex):
        parentConn, childConn = Pipe()
        parentConns.append(parentConn)
        childConns.append(childConn)
        t = Process(target=doAlu, args=(per_times, childConn, i))
        threads.append(t)
    for i in range(parallelIndex):
        threads[i].start()
    for i in range(parallelIndex):
        threads[i].join()

    results = []
    for i in range(parallelIndex):
        results.append(parentConns[i].recv())
    return str(results)
if __name__ == '__main__':
    function_handler(None, None)
