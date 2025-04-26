from qiskit import QuantumCircuit
import matplotlib.pyplot as plt

def create_coin_circuit():
    """
    创建一个量子猜硬币实验的电路：
    对一个量子比特应用H门（Hadamard门），使其进入|0⟩和|1⟩的叠加态，然后测量。
    返回QuantumCircuit对象。
    """
    qc = QuantumCircuit(1, 1)
    qc.h(0)  # Hadamard门：叠加
    qc.measure(0, 0)  # 测量
    return qc

if __name__ == "__main__":
    qc = create_coin_circuit()
    qc.draw(output='mpl')
    plt.title("量子猜硬币实验电路")
    plt.show()
