#functia f(x)=(a^x)%15
from qiskit import *
from math import pi
from qiskit.circuit.library import QFT
import numpy as np

a=7

circuit=QuantumCircuit(12,12)
circuit.append(QFT(8,True),circuit.qubits[:8])

def modulo15(a, power):
    U = QuantumCircuit(4)        
    for iteration in range(power):
        if a in [2,13]:
            U.swap(0,1)
            U.swap(1,2)
            U.swap(2,3)
        if a in [7,8]:
            U.swap(2,3)
            U.swap(1,2)
            U.swap(0,1)
        if a == 11:
            U.swap(1,3)
            U.swap(0,2)
        if a in [7,11,13]:
            for q in range(4):
                U.x(q)
    U = U.to_gate()
    U.name = "%i^%i mod 15" % (a, power)
    c_U = U.control()
    return c_U

for i in range(8):
    circuit.append(modulo15(a, 2**i), 
             [i] + [x+8 for x in range(4)])

circuit.append(QFT(8,True),circuit.qubits[:8])

for i in range(8):
	circuit.measure(i,i)

print(circuit.draw())

#pentru a vedea rezultatul
simulator=Aer.get_backend('qasm_simulator')
job=execute(circuit,simulator)
result=job.result()
counts=result.get_counts()
print(counts)