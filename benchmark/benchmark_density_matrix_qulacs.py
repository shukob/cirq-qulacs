import os
import re
import time
import random
import matplotlib.pyplot as plt
import numpy as np

from qulacs import DensityMatrix, QuantumCircuit

def parse_qasm_to_QulacsCircuit(input_filename, qulacs_circuit):

   with open(input_filename, "r") as ifile:
       lines = ifile.readlines()

       for line in lines:
           s = re.search(r"qreg|cx|u3|u1", line)

           if s is None:
               continue

           elif s.group() == 'qreg':
               match = re.search(r"\d\d*", line)
               continue

           elif s.group() == 'cx':
               match = re.findall(r'\[\d\d*\]', line)
               c_qbit = int(match[0].strip('[]'))
               t_qbit = int(match[1].strip('[]'))
               qulacs_circuit.add_CNOT_gate(c_qbit, t_qbit)
               continue

           elif s.group() == 'u3':
               m_r = re.findall(r'[-]?\d\.\d\d*', line)
               m_i = re.findall(r'\[\d\d*\]', line)
               t_qbit = int(m_i[0].strip('[]'))
               qulacs_circuit.add_U3_gate(t_qbit, float(m_r[0]),float(m_r[1]),float(m_r[2]))
               continue

           elif s.group() == 'u1':
               m_r = re.findall(r'[-]?\d\.\d\d*', line)
               m_i = re.findall(r'\[\d\d*\]', line) 
               t_qbit = int(m_i[0].strip('[]'))
               qulacs_circuit.add_U1_gate(t_qbit, float(m_r[0]))
               continue


def main():

    folder_path = "./result_qulacs"
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    with open(folder_path+'/benchmark_density_matrix_qulacs_cpu.csv', 'w') as f:
        f.write('n_qubits,n_iter,elapsed_time\n')
        for niter in range(10):
            for nqubits in range(5, 12+1):
                circuit = QuantumCircuit(nqubits)
                parse_qasm_to_QulacsCircuit('quantum_volume/quantum_volume_n{}_d8_0_{}.qasm'.format(nqubits, niter) ,circuit)

                state = DensityMatrix(nqubits)
                start = time.time()
                rep = 0
                while time.time()-start < 1.0:
                    circuit.update_quantum_state(state)
                    rep+=1
                elapsed_time = (time.time() - start)/rep
                f.write('{},{},{}\n'.format(nqubits, niter, elapsed_time))
                print('cpu  {},{},{}'.format(nqubits, niter, elapsed_time))
                
                del state

if __name__ == '__main__':
   main()