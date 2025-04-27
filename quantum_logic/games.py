#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
量子游戏集合
这个程序包含多种基于量子计算原理的游戏和演示
展示了量子叠加、量子纠缠、量子干涉等量子力学特性
"""

from qiskit_aer import Aer
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram, plot_bloch_multivector, plot_state_city
from qiskit.quantum_info import Statevector
from qiskit.circuit.library import MCPhaseGate
import matplotlib.pyplot as plt
import numpy as np
import random
import time
import os
import math

class QuantumGames:
    # Modify init to accept GUI interaction functions
    def __init__(self, gui_output_func=None, request_input_func=None, end_game_func=None, gui_display_plots_func=None):
        """Initialize with optional callbacks for GUI interaction."""
        self.gui_output = gui_output_func
        self.request_input = request_input_func # Expects a function that takes a callback
        self.end_game = end_game_func # Callback to signal game end to GUI
        self.gui_display_plots = gui_display_plots_func # NEW: Callback for list of plots
        self.simulator = Aer.get_backend('qasm_simulator')
        self.statevector_sim = Aer.get_backend('statevector_simulator')
        # Store GUI interaction functions
        self.current_game_state = {} # Optional: For more complex state between inputs
    
    # Remove clear_screen as it's GUI's responsibility or done via gui_output
    # def clear_screen(self):
    #     """清屏函数"""
    #     os.system('cls' if os.name == 'nt' else 'clear')

    def save_circuit_image(self, qc, filename="quantum_circuit.png"):
        """保存量子电路图像"""
        try:
            qc.draw(output='mpl', filename=filename)
            # Use gui_output instead of print
            self.gui_output(f"电路图已保存为 {filename}\n")
            return True
        except Exception as e:
            # Use gui_output instead of print
            self.gui_output(f"无法保存电路图: {e}\n")
            return False
    
    # Remove pause as GUI flow handles pauses
    # def pause(self):
    #     """暂停并等待用户按键继续"""
    #     input("\n按回车键继续...")

    # ---------- 基础量子操作 (Keep these as internal logic) ----------
    
    def flip_quantum_coin(self, draw_only=False):
        """创建量子电路来模拟硬币翻转 (Internal Logic)"""
        # ... (keep internal logic as is) ...
        qc = QuantumCircuit(1, 1)
        qc.h(0)
        qc.measure(0, 0)
        if draw_only:
            return qc
        compiled_circuit = transpile(qc, self.simulator)
        job = self.simulator.run(compiled_circuit, shots=1)
        result = job.result()
        counts = result.get_counts(compiled_circuit)
        return list(counts.keys())[0]
    
    # ... (other internal logic methods like flip_quantum_biased_coin, create_entangled_pair etc. remain unchanged) ...
    # Make sure they don't use print/input directly if called from game flows
    def create_entangled_pair(self, draw_only=False):
        """创建一对纠缠的量子比特（贝尔态）(Internal Logic)"""
        qc = QuantumCircuit(2, 2)
        qc.h(0)
        qc.cx(0, 1)
        qc.measure([0, 1], [0, 1])
        if draw_only:
            return qc
        compiled_circuit = transpile(qc, self.simulator)
        job = self.simulator.run(compiled_circuit, shots=1)
        result = job.result()
        counts = result.get_counts(compiled_circuit)
        return list(counts.keys())[0]

    def create_superposition(self, num_qubits=3, shots=1000):
        """创建多量子比特叠加态 (Internal Logic, but might need GUI output for counts/statevector)"""
        # ... (Internal logic for circuit creation) ...
        qc = QuantumCircuit(num_qubits, num_qubits)
        for q in range(num_qubits):
            qc.h(q)
        
        # Statevector part (no direct print)
        statevector_circuit = qc.copy()
        statevector_circuit.remove_final_measurements(inplace=True)
        statevector_job = self.statevector_sim.run(transpile(statevector_circuit, self.statevector_sim))
        statevector_result = statevector_job.result()
        statevector = statevector_result.get_statevector(statevector_circuit)
        
        # Measurement part (no direct print)
        qc.measure(range(num_qubits), range(num_qubits))
        compiled_circuit = transpile(qc, self.simulator)
        job = self.simulator.run(compiled_circuit, shots=shots)
        result = job.result()
        counts = result.get_counts(compiled_circuit)
        
        # Return results; calling function decides how to display
        return qc, counts, statevector

    def create_interference_circuit(self, circuit_type='standard', draw_only=False, shots=1000):
         """创建量子干涉电路 (Internal Logic)"""
         # ... (Internal logic as before) ...
         qc = QuantumCircuit(1, 1)
         if circuit_type == 'standard':
             qc.h(0); qc.z(0); qc.h(0)
         elif circuit_type == 'no_z':
             qc.h(0); qc.h(0)
         elif circuit_type == 's_gate':
             qc.h(0); qc.s(0); qc.h(0)
         qc.measure(0, 0)
         if draw_only:
             return qc
         compiled_circuit = transpile(qc, self.simulator)
         job = self.simulator.run(compiled_circuit, shots=shots)
         result = job.result()
         counts = result.get_counts(compiled_circuit)
         return counts

    def quantum_teleportation_demo(self, state_to_teleport=None, draw_only=False):
        """量子隐形传态演示 (Internal Logic)"""
        # ... (Internal logic as before) ...
        # This one likely needs significant refactoring if it had print/input.
        # For now, assume it just returns the circuit or results.
        qc = QuantumCircuit(3, 2) 
        # ... rest of teleportation logic ...
        # Ensure no print/input inside this core logic function
        # It should return results (e.g., circuit, final state, counts) 
        # The calling GUI function will display them.
        pass # Placeholder - requires detailed check

    def create_coin_circuit(self):
        """
        创建一个量子猜硬币实验的电路：
        对一个量子比特应用H门（Hadamard门），使其进入|0⟩和|1⟩的叠加态，然后测量。
        返回QuantumCircuit对象。
        """
        from qiskit import QuantumCircuit
        qc = QuantumCircuit(1, 1)
        qc.h(0)  # Hadamard门：叠加
        qc.measure(0, 0)  # 测量
        return qc

    # ---------- Game Flows (Refactored for GUI) ----------

    # --- Coin Game --- 
    def run_coin_game(self):
        """Entry point for the GUI to start the coin game."""
        if not self.gui_output:
            return
        self.gui_output("--- 量子猜硬币游戏 ---\n")
        self.gui_output("我们将抛掷1000次量子硬币 (Hadamard门+测量)，统计0/1出现次数。\n")
        from qiskit import transpile
        from qiskit.visualization import plot_histogram
        qc = self.create_coin_circuit()
        compiled_circuit = transpile(qc, self.simulator)
        job = self.simulator.run(compiled_circuit, shots=1000)
        counts = job.result().get_counts(compiled_circuit)
        count_0 = counts.get('0', 0)
        count_1 = counts.get('1', 0)
        self.gui_output(f"实验统计结果：\n  0（正面）：{count_0} 次\n  1（反面）：{count_1} 次\n")
        from matplotlib.figure import Figure
        figs = []
        if self.gui_display_plots:
            # 直方图
            hist_fig = plot_histogram(counts, title='1000次量子硬币实验结果分布')
            figs.append(hist_fig)
            # 电路图
            fig_circuit = Figure(figsize=(4,2))
            ax = fig_circuit.add_subplot(111)
            qc.draw(output='mpl', ax=ax)
            ax.set_title('量子猜硬币实验电路')
            figs.append(fig_circuit)
            self.gui_display_plots(figs)
        self.gui_output("--------------------\n")
        self.end_game()

    # --- Entanglement Game --- 
    def run_entanglement_game(self):
        """Entry point for GUI - Demonstrates Bell state entanglement."""
        self.gui_output("--- 量子纠缠演示 ---\n")
        self.gui_output("创建一个纠缠贝尔对 (|00> + |11>)/sqrt(2)。\n")
        self.gui_output("测量两个量子比特会显示出相关性：它们总是相同的 (00 或 11)。\n")
        
        try:
            # Create a 2-qubit quantum circuit
            qc = QuantumCircuit(2, 2) # 2 qubits, 2 classical bits
            
            # Create Bell state |Φ+>
            qc.h(0)    # Apply Hadamard gate to qubit 0
            qc.cx(0, 1) # Apply CNOT gate with control qubit 0 and target qubit 1
            
            # Measure both qubits
            qc.measure([0, 1], [0, 1])
            
            self.gui_output("\n贝尔态 |Φ+> 的量子电路已创建。\n")
            # Plot circuit diagram using GUI callback
            if self.gui_display_plots:
                try:
                    circuit_fig = qc.draw('mpl', style='iqx')
                    figures_to_display = [circuit_fig]
                    self.gui_display_plots(figures_to_display)
                    self.gui_output("电路图已在 GUI 区域绘制。\n")
                except ImportError:
                    self.gui_output("绘制电路图需要 'pylatexenc' 包。请运行 'pip install pylatexenc'。\n")
                except Exception as plot_error:
                    self.gui_output(f"绘制电路图时出错: {plot_error}\n")
            
            # Optional: Display circuit (might be too complex for text output)
            # self.gui_output(str(qc))
            # Optional: Save circuit image
            # self.save_circuit_image(qc, "entanglement_circuit.png")

            self.gui_output("模拟电路运行 100 次...\n")
            # Execute the circuit on the qasm simulator
            job = self.simulator.run(qc, shots=100)
            result = job.result()
            counts = result.get_counts(qc)
            
            self.gui_output("\n测量结果:\n")
            # Nicely format counts dictionary
            for state, count in sorted(counts.items()):
                self.gui_output(f"  状态 |{state}>: {count} 次\n")
            
            self.gui_output("\n注意结果只包含 '00' 或 '11'，显示了完美的关联性。\n")
            
        except Exception as e:
            self.gui_output(f"\n纠缠演示过程中出错: {e}\n")
            
        # TODO: Refactor this game flow using gui_output and request_input
        # Possible extension: Measure only one qubit, ask user to predict the other.
        # self.gui_output("This game is not yet fully adapted for GUI.\n")
        # Simulate immediate end for now
        self.gui_output("--------------------\n")
        self.end_game()

    # --- Interference Game --- 
    def run_interference_game(self):
        """Entry point for GUI - Demonstrates Quantum Interference (Mach-Zehnder)."""
        self.gui_output("--- 量子干涉演示 ---\n")
        self.gui_output("比较两个单量子比特电路:\n")
        self.gui_output("1. H门后测量: 产生叠加态 (约50%为0, 50%为1)。\n")
        self.gui_output("2. H门, Z门, H门后测量 (HZH): 展示干涉现象。\n")
        self.gui_output("   理想情况下，HZH 作用于 |0> 等效于 X 门, 结果应为 100% '1'。\n")
        
        shots = 1024
        figures_to_display = [] # Initialize list to collect figures
        try:
            # Circuit 1: H-Measure
            qc_h = QuantumCircuit(1, 1)
            qc_h.h(0)
            qc_h.measure(0, 0)
            self.gui_output("\n电路 H 已创建.")
            # Try plotting circuit H
            try:
                circuit_fig_h = qc_h.draw('mpl', style='iqx')
                figures_to_display.append(circuit_fig_h)
                self.gui_output("电路 H 图已生成.")
            except ImportError:
                 self.gui_output("绘制电路图需要 'pylatexenc' 包。请运行 'pip install pylatexenc'。\n")
            except Exception as plot_error:
                 self.gui_output(f"绘制电路 H 图时出错: {plot_error}\n")

            job_h = self.simulator.run(qc_h, shots=shots)
            result_h = job_h.result()
            counts_h = result_h.get_counts(qc_h)
            self.gui_output(f"结果 (H): {counts_h}\n")
            # Generate histogram for H circuit
            try:
                hist_h_fig = plot_histogram(counts_h, title='电路 H 的结果')
                figures_to_display.append(hist_h_fig) # Append figure
                self.gui_output("直方图 H 已生成.")
            except Exception as plot_error:
                self.gui_output(f"绘制直方图 H 时出错: {plot_error}\n")
            
            # Circuit 2: H-Z-H-Measure
            qc_hzh = QuantumCircuit(1, 1)
            qc_hzh.h(0)
            qc_hzh.z(0)
            qc_hzh.h(0)
            qc_hzh.measure(0, 0)
            self.gui_output("\n电路 HZH 已创建.")
            # Try plotting circuit HZH
            try:
                circuit_fig_hzh = qc_hzh.draw('mpl', style='iqx')
                figures_to_display.append(circuit_fig_hzh)
                self.gui_output("电路 HZH 图已生成.")
            except ImportError:
                 self.gui_output("绘制电路图需要 'pylatexenc' 包。\n")
            except Exception as plot_error:
                 self.gui_output(f"绘制电路 HZH 图时出错: {plot_error}\n")
            
            job_hzh = self.simulator.run(qc_hzh, shots=shots)
            result_hzh = job_hzh.result()
            counts_hzh = result_hzh.get_counts(qc_hzh)
            self.gui_output(f"结果 (HZH): {counts_hzh}\n")
            # Generate histogram for HZH circuit
            try:
                hist_hzh_fig = plot_histogram(counts_hzh, title='电路 HZH 的结果')
                figures_to_display.append(hist_hzh_fig) # Append figure
                self.gui_output("直方图 HZH 已生成.")
            except Exception as plot_error:
                self.gui_output(f"绘制直方图 HZH 时出错: {plot_error}\n")

            # Display all collected plots together at the end
            if self.gui_display_plots and figures_to_display:
                self.gui_display_plots(figures_to_display)
                self.gui_output("\n所有图表已在 GUI 区域绘制。\n")
            else:
                self.gui_output("\n未生成或无法显示图表。\n")

            self.gui_output("\n比较: 注意HZH主要产生'1'的结果, 不同于单独H门的50/50分布。\n") # Corrected newline and string termination
            
        except Exception as e:
            self.gui_output(f"\n干涉演示过程中出错: {e}\n")
            
        # TODO: Refactor this game flow
        # Example: Ask user which circuit type, display results/histogram
        # self.gui_output("This game is not yet fully adapted for GUI.\n")
        # Simulate immediate end for now
        self.gui_output("--------------------\n")
        self.end_game()

    # --- Teleportation Game --- 
    def run_teleportation_game(self):
        """Entry point for GUI - Demonstrates Quantum Teleportation."""
        self.gui_output("--- 量子隐形传态演示 ---\n")
        self.gui_output("将量子态 |+> = (|0> + |1>)/sqrt(2) 从 Alice (q0) 传输到 Bob (q2)。\n")
        self.gui_output("使用一个纠缠对 (q1, q2) 和 2 个经典比特进行通信。\n")

        try:
            # Create a 3-qubit, 3-classical bit circuit
            qc = QuantumCircuit(3, 3)
            
            # 1. Prepare Alice's state |ψ> on q0 (let's use |+>)
            qc.h(0)
            qc.barrier() # Visually separate steps
            
            # 2. Create Bell pair between q1 (Alice) and q2 (Bob)
            qc.h(1)
            qc.cx(1, 2)
            qc.barrier()
            
            # 3. Alice performs Bell measurement on her qubits (q0, q1)
            qc.cx(0, 1)
            qc.h(0)
            qc.barrier()
            
            # 4. Alice measures q0 and q1 into classical bits c0 and c1
            qc.measure([0, 1], [0, 1]) # Measure q0 to c0, q1 to c1
            qc.barrier()
            
            # 5. Bob applies corrections to q2 based on Alice's classical bits (c0, c1)
            # Get the classical register (assuming only one is named 'c' or is the default)
            creg = qc.cregs[0]
            
            # Apply X gate to q2 if c1 (creg[1]) is 1
            with qc.if_test((creg[1], 1)):
                qc.x(2)
                
            # Apply Z gate to q2 if c0 (creg[0]) is 1
            with qc.if_test((creg[0], 1)):
                qc.z(2)
                
            qc.barrier()

            # 6. Measure Bob's qubit (q2) to see the teleported state
            # Note: For a |+> input state, the output should ideally be |+> again.
            qc.measure(2, 2) # Measure q2 into classical bit c2
            
            self.gui_output("\n量子隐形传态电路已创建。\n")

            shots = 1024
            self.gui_output(f"模拟电路运行 {shots} 次...\n")
            # Execute the circuit
            job = self.simulator.run(qc, shots=shots)
            result = job.result()
            counts = result.get_counts(qc)
            
            self.gui_output("\n完整测量结果 (c2 c1 c0):\n")
            # Display raw counts (c2 is the leftmost bit)
            for state, count in sorted(counts.items()):
                self.gui_output(f"  状态 |{state}>: {count} 次\n")

            # Analyze the results for Bob's qubit (c2) specifically
            bob_counts = {'0': 0, '1': 0}
            for state, count in counts.items():
                bob_measure = state[0] # c2 is the first char in the string 'c2c1c0'
                bob_counts[bob_measure] += count
                
            self.gui_output("\nBob 的量子比特 (q2) 测量结果分析:\n")
            self.gui_output(f"  状态 |0>: {bob_counts.get('0', 0)} 次\n")
            self.gui_output(f"  状态 |1>: {bob_counts.get('1', 0)} 次\n")
            self.gui_output("由于原始状态是 |+>, 我们期望 Bob 的量子比特测量结果中 0 和 1 大约各占 50%。\n")

            # Plot Bob's qubit results using GUI callback
            if self.gui_display_plots:
                try:
                    # Use bob_counts for the histogram
                    hist_bob_fig = plot_histogram(bob_counts, title='Bob 量子比特 (q2) 的测量结果')
                    figures_to_display = [hist_bob_fig]
                    self.gui_display_plots(figures_to_display)
                    self.gui_output("\nBob 量子比特的直方图已在 GUI 区域绘制。\n")
                except Exception as plot_error:
                    self.gui_output(f"绘制 Bob 量子比特直方图时出错: {plot_error}\n")

        except Exception as e:
            self.gui_output(f"\n隐形传态演示过程中出错: {e}\n")
            
        # TODO: Refactor this game flow
        # self.gui_output("This game is not yet fully adapted for GUI.\n")
        self.gui_output("--------------------\n")
        self.end_game()
        
    # --- Superposition Demo ---
    def run_superposition_demo(self, num_qubits=2):
        """Demonstrates superposition for multiple qubits with GUI output and plots."""
        if not self.gui_output or not self.gui_display_plots:
            self.gui_output("错误: GUI 回调函数未设置!")
            return
        self.gui_output("--- 量子叠加态演示 ---\n")
        try:
            self.gui_output(f"为 {num_qubits} 个量子比特创建叠加态 (应用H门)...\n")
            qc, counts, statevector = self.create_superposition(num_qubits=num_qubits, shots=1024)
            
            self.gui_output(f"\n模拟运行 {1024} 次的测量结果:\n") # Use actual shots number if needed

            # Nicely format counts dictionary
            for state, count in sorted(counts.items()):
                self.gui_output(f"  状态 |{state}>: {count} 次\n")
            
            self.gui_output("\n理论状态向量 (部分):\n")
            # Display statevector nicely (can be long)
            max_display = 2**num_qubits if 2**num_qubits <= 8 else 8 # Limit display
            for i, amp in enumerate(statevector):
                if i >= max_display:
                    self.gui_output(f"  ... (仅显示前 {max_display} 个分量)\n")
                    break
                basis_state = format(i, f'0{num_qubits}b')
                self.gui_output(f"  |{basis_state}>: {amp:.3f}\n")
            # Add a pass statement here just in case it helps parser with line 268 error
            pass 
                
            # Show plots? Now use the callback if available.
            if self.gui_display_plots:
                try:
                    # Generate histogram figure
                    hist_fig = plot_histogram(counts)
                    # Send figure to GUI for display (this will replace the circuit diagram)
                    figures_to_display = [hist_fig]
                    self.gui_display_plots(figures_to_display)
                    self.gui_output("\n结果直方图已绘制。\n")
                    
                    # Could also plot bloch sphere, but one plot at a time is usually best for GUI
                    # bloch_fig = plot_bloch_multivector(statevector)
                    # self.gui_plot(bloch_fig) 
                except Exception as plot_error:
                    self.gui_output(f"\n生成/绘制可视化时出错: {plot_error}\n")
            else:
                self.gui_output("\n(绘图功能未提供给 GUI)\n")
                # Fallback or just skip? Maybe show counts again.
                # plot_histogram(counts).show() # Original behavior: pops up window
            
            # Simplified string for lint check
            # self.gui_output("(Histograms/Bloch spheres usually show in separate windows)\n")
                
        except Exception as e:
            self.gui_output(f"\n叠加态演示过程中出错: {e}\n")
            
        self.gui_output("--------------------\n")
        self.end_game()
        
    # --- Deutsch-Jozsa Demo --- NEW
    def run_deutsch_jozsa_demo(self):
        """Demonstrates the Deutsch-Jozsa algorithm.

        Distinguishes between a constant function (f(x) = c for all x)
        and a balanced function (f(x) = 0 for half of inputs, 1 for the other half)
        with a single query to the oracle.
        """
        self.gui_output("--- Deutsch-Jozsa 算法演示 ---\n")
        self.gui_output("目标: 判断一个未知函数 f(x) 是常数函数还是平衡函数。\n")
        self.gui_output("方法: 使用量子预言机（Oracle）查询一次即可区分。\n")
        
        n = 2 # Number of input qubits for the function f:{0,1}^n -> {0,1}
        self.gui_output(f"示例: n = {n} 个输入比特。\n")

        # Create the circuit with n input qubits + 1 output qubit + n classical bits
        dj_circuit = QuantumCircuit(n + 1, n)
        figures_to_display = []

        try:
            # Step 1: Initialize output qubit to |->
            self.gui_output("步骤 1: 将输出量子比特初始化为 |-> 状态 (应用 X 和 H 门)。\n")
            dj_circuit.x(n) # Apply X gate to the last qubit (index n)
            dj_circuit.h(n) # Apply H gate to the last qubit

            # Step 2: Apply Hadamard to all input qubits
            self.gui_output(f"步骤 2: 对所有 {n} 个输入量子比特应用 Hadamard (H) 门。\n")
            for i in range(n):
                dj_circuit.h(i)
            dj_circuit.barrier() # Separator for clarity

            # Step 3: Define and Apply the Oracle U_f
            # Example: Balanced oracle f(x_1, x_0) = x_1 XOR x_0
            # Implemented using CNOTs targeting the output qubit
            self.gui_output("步骤 3: 应用代表平衡函数 f(x1, x0) = x1 XOR x0 的预言机。\n")
            self.gui_output("        (通过 CNOT 门实现)\n")
            for i in range(n):
                dj_circuit.cx(i, n) # CNOT from input qubit i to output qubit n
            dj_circuit.barrier()

            # Step 4: Apply Hadamard to input qubits again
            self.gui_output(f"步骤 4: 再次对所有 {n} 个输入量子比特应用 Hadamard 门。\n")
            for i in range(n):
                dj_circuit.h(i)
            dj_circuit.barrier()

            # Step 5: Measure the input qubits
            self.gui_output(f"步骤 5: 测量前 {n} 个输入量子比特。\n")
            dj_circuit.measure_all()

            # --- Simulation and Results ---
            self.gui_output("\n电路构建完成，准备模拟...\n")
            # Draw the circuit
            try:
                circuit_fig = dj_circuit.draw('mpl', style='iqx')
                figures_to_display.append(circuit_fig)
                self.gui_output("电路图已生成。\n")
            except ImportError:
                self.gui_output("绘制电路图需要 'pylatexenc' 包。\n")
            except Exception as plot_error:
                self.gui_output(f"绘制电路图时出错: {plot_error}\n")

            # Simulate
            shots = 100 # Only need a few shots, ideally 1 is enough theoretically
            job = self.simulator.run(dj_circuit, shots=shots)
            result = job.result()
            counts = result.get_counts(dj_circuit)
            self.gui_output(f"模拟结果 (测量前 {n} 个比特): {counts}\n")

            # Interpretation
            # For Deutsch-Jozsa, if the result is |00...0>, the function is constant.
            # If the result is anything else, the function is balanced.
            all_zeros = '0' * n
            if all_zeros in counts and len(counts) == 1: # Check if only the all-zero state is measured
                 self.gui_output("解释: 测量结果全部为 '0...0'，表明函数是常数函数。\n")
            else:
                 # Check if the all-zero state is absent or has zero probability
                 measurement_keys = counts.keys()
                 if all_zeros not in measurement_keys or counts.get(all_zeros, 0) == 0:
                     self.gui_output("解释: 测量结果不是 '0...0'，表明函数是平衡函数。\n")
                 else:
                     # This case (mixing 0s and non-0s) shouldn't happen for a valid DJ oracle/circuit
                     self.gui_output("解释: 测量结果包含 '0...0' 和其他状态，这不符合Deutsch-Jozsa算法的预期。可能预言机或电路有问题。\n")

            # Display plots
            if self.gui_display_plots and figures_to_display:
                self.gui_display_plots(figures_to_display)
                self.gui_output("图表已在 GUI 区域绘制。\n")
            else:
                 self.gui_output("未生成或无法显示图表。\n")

        except Exception as e:
            self.gui_output(f"\nDeutsch-Jozsa 演示过程中出错: {e}\n")
        finally:
            # End the game/demo process
            self.gui_output("--------------------\n")
            self.end_game()


    # --- Grover Search Demo --- NEW
    def run_grover_search_demo(self):
        """Demonstrates Grover's search algorithm.

        Finds a marked item in an unstructured database quadratically faster
        than classical algorithms.
        """
        self.gui_output("--- Grover 搜索算法演示 ---\n")
        self.gui_output("目标: 在未排序的数据库中高效查找一个标记项。\n")
        self.gui_output("方法: 通过量子叠加和幅度放大实现平方级加速。\n")
        
        n = 3 # Number of qubits
        num_states = 2**n
        marked_item_bin = '101' # The item we want to find (example)
        self.gui_output(f"示例: n = {n} 个量子比特 (数据库大小 N = {num_states}).\n")
        self.gui_output(f"        标记项 (二进制): {marked_item_bin}\n")

        figures_to_display = []

        try:
            # --- Oracle Definition --- 
            # Marks the state |101> by flipping its phase
            def create_oracle(qc, n, marked_state_binary):
                # Flip bits corresponding to 0s in the marked state
                for qubit, bit in enumerate(reversed(marked_state_binary)):
                    if bit == '0':
                        qc.x(qubit)
                # Apply multi-controlled Z gate
                control_qubits = list(range(n-1))
                target_qubit = n-1
                qc.append(MCPhaseGate(np.pi, len(control_qubits)), control_qubits + [target_qubit]) # Corrected: positional arg
                # Flip bits back
                for qubit, bit in enumerate(reversed(marked_state_binary)):
                    if bit == '0':
                        qc.x(qubit)
                qc.barrier()

            # --- Diffuser Definition ---
            def create_diffuser(qc, n):
                qc.h(range(n))
                qc.x(range(n))
                control_qubits = list(range(n-1))
                target_qubit = n-1
                qc.append(MCPhaseGate(np.pi, len(control_qubits)), control_qubits + [target_qubit]) # Corrected: positional arg
                qc.x(range(n))
                qc.h(range(n))
                qc.barrier()

            # --- Circuit Construction ---
            self.gui_output("步骤 1: 初始化所有量子比特到 |+> 状态 (应用 H 门).\n")
            grover_circuit = QuantumCircuit(n, name="Grover Search Demo")
            grover_circuit.h(range(n))
            grover_circuit.barrier()

            # Calculate optimal number of iterations
            # optimal_iterations = int(np.round((np.pi / 4) * np.sqrt(num_states)))
            # For n=3, N=8, sqrt(8) is approx 2.82, pi/4 * 2.82 is approx 2.2. Let's use 2 iterations.
            optimal_iterations = 2 
            self.gui_output(f"步骤 2: 重复应用 Oracle 和 Diffuser {optimal_iterations} 次.\n")

            for iteration in range(optimal_iterations):
                self.gui_output(f"  迭代 {iteration + 1}:")
                self.gui_output("    应用 Oracle (标记状态 '{marked_item_bin}')")
                create_oracle(grover_circuit, n, marked_item_bin)
                self.gui_output("    应用 Diffuser (放大标记态幅度)")
                create_diffuser(grover_circuit, n)
            
            # Step 3: Measure all qubits
            self.gui_output(f"步骤 3: 测量所有 {n} 个量子比特.\n")
            grover_circuit.measure_all()

            # --- Simulation and Results ---
            self.gui_output("\n电路构建完成，准备模拟...\n")
            
            # Draw the circuit
            try:
                circuit_fig = grover_circuit.draw('mpl', style='iqx', fold=-1)
                figures_to_display.append(circuit_fig)
                self.gui_output("电路图已生成.\n")
            except ImportError:
                self.gui_output("绘制电路图需要 'pylatexenc' 包.\n")
            except Exception as plot_error:
                self.gui_output(f"绘制电路图时出错: {plot_error}\n")

            # Simulate
            shots = 1024 # Use more shots for better statistics
            job = self.simulator.run(grover_circuit, shots=shots)
            result = job.result()
            counts = result.get_counts(grover_circuit)
            self.gui_output(f"模拟结果 (测量 {n} 个比特 {shots} 次): {counts}\n")

            # Interpretation
            # The state with the highest probability should be the marked item
            most_frequent = max(counts, key=counts.get)
            self.gui_output(f"解释: 测量结果中概率最高的态是 '{most_frequent}'.\n")
            if most_frequent == marked_item_bin:
                self.gui_output(f"        这与我们标记的项 '{marked_item_bin}' 相符，搜索成功！\n")
            else:
                # This case (not finding the marked item) could happen due to insufficient iterations or noise
                self.gui_output(f"        这与我们标记的项 '{marked_item_bin}' 不符，搜索可能未完全收敛或存在错误.\n")

            # Generate and add histogram
            try:
                hist_fig = plot_histogram(counts, title="Grover 搜索结果")
                figures_to_display.append(hist_fig)
                self.gui_output("直方图已生成.\n")
            except Exception as plot_error:
                 self.gui_output(f"绘制直方图时出错: {plot_error}\n")

            # Display plots
            if self.gui_display_plots and figures_to_display:
                self.gui_display_plots(figures_to_display)
                self.gui_output("图表已在 GUI 区域绘制.\n")
            else:
                 self.gui_output("未生成或无法显示图表.\n")

        except Exception as e:
             self.gui_output(f"\nGrover 搜索演示过程中出错: {e}\n")
             import traceback
             traceback.print_exc() # Print detailed traceback to console for debugging
        finally:
            # End the game/demo process
            self.gui_output("--------------------\n")
            self.end_game()

    # --- Quantum Fourier Transform (QFT) Demo --- NEW
    def run_qft_demo(self):
        """Demonstrates the Quantum Fourier Transform (QFT)."""
        self.gui_output("--- 量子傅里叶变换 (QFT) 演示 ---\n")
        self.gui_output("目标: 演示 QFT 如何将计算基态转换为傅里叶基态.\n")
        self.gui_output("应用: QFT 是许多量子算法的关键组成部分，如 Shor 算法.\n")
        
        n = 3 # Number of qubits
        input_state_decimal = 5
        input_state_binary = format(input_state_decimal, f'0{n}b') # '101' for n=3

        self.gui_output(f"示例: n = {n} 个量子比特.\n")
        self.gui_output(f"        输入态: |{input_state_binary}> (十进制 {input_state_decimal})\n")

        figures_to_display = []

        try:
            # --- Helper Functions for Manual QFT ---
            def qft_rotations(circuit, n):
                """Applies the rotation part of the QFT circuit."""
                if n == 0:
                    return circuit
                # Apply H gate to the most significant qubit
                circuit.h(n-1)
                # Apply controlled rotations
                for qubit in range(n-1):
                    # control=qubit, target=n-1
                    circuit.cp(np.pi/2**(n-1-qubit), qubit, n-1)
                # Recursively apply to the rest
                qft_rotations(circuit, n-1)

            def swap_registers(circuit, n):
                """Applies SWAP gates to reverse qubit order after QFT rotations."""
                for qubit in range(n//2):
                    circuit.swap(qubit, n-qubit-1)
                return circuit

            # --- Circuit Construction ---
            # 1. Prepare initial state |101>
            qc = QuantumCircuit(n, name="Manual QFT Demo")
            self.gui_output("步骤 1: 准备初始态 |101>.\n") # Corrected single line
            # Initialize to |101> (Qiskit order is qn-1...q0, so |101> means q2=1, q1=0, q0=1)
            if input_state_binary[0] == '1': qc.x(n-1) # q2
            if input_state_binary[1] == '1': qc.x(n-2) # q1
            if input_state_binary[2] == '1': qc.x(n-3) # q0
            qc.barrier()

            # 2. Apply QFT manually
            self.gui_output("步骤 2: 手动应用 QFT 旋转门.\n") # Corrected single line
            qft_rotations(qc, n)
            qc.barrier()
            self.gui_output("步骤 3: 应用 SWAP 门来反转量子比特顺序.\n") # Corrected single line
            swap_registers(qc, n)
            qc.barrier()

            self.gui_output("手动 QFT 电路构建完成.\n") # Corrected single line

            # Draw the circuit (no need to decompose now)
            self.gui_output("绘制电路图...\n") # Added closing parenthesis and newline
            try:
                circuit_fig = qc.draw('mpl', style='iqx', fold=-1)
                figures_to_display.append(circuit_fig)
                self.gui_output("电路图已生成.\n") # Corrected previous message
            except ImportError:
                self.gui_output("绘制电路图需要 'pylatexenc' 包.\n") # Corrected quotes
            except Exception as plot_error:
                self.gui_output(f"绘制电路图时出错: {plot_error}\n")

            # --- Simulation (Statevector) ---
            self.gui_output("\n准备使用状态向量模拟器模拟...\n") # Corrected newline/string termination
            try:
                sv_simulator = Aer.get_backend('statevector_simulator')

                # Run the circuit directly (should contain only basic gates now)
                job = sv_simulator.run(qc)
                result = job.result()
                output_statevector = result.get_statevector(qc)
                
                self.gui_output("模拟完成。输出状态向量:\n")
                # Format output for better readability
                for i, amp in enumerate(output_statevector):
                    # Only show non-negligible amplitudes
                    if not np.isclose(amp, 0):
                         self.gui_output(f"  |{format(i, f'0{n}b')}> : {amp:.3f}")
                self.gui_output("\n(注意: 幅度是复数，这里显示了实部和虚部)\n")

                # Visualize the statevector
                state_fig = plot_state_city(output_statevector, title="QFT 输出状态向量")
                figures_to_display.append(state_fig)
                self.gui_output("状态向量图已生成.\n")

            except Exception as sim_error: # Restored missing except block for simulation try
                self.gui_output(f"状态向量模拟或绘图时出错: {sim_error}\n")
                import traceback
                traceback.print_exc()

            # Display plots
            if self.gui_display_plots and figures_to_display:
                self.gui_display_plots(figures_to_display)
                self.gui_output("图表已在 GUI 区域绘制.\n")
            else:
                 self.gui_output("未生成或无法显示图表.\n")

        except Exception as e:
            self.gui_output(f"\nQFT 演示过程中出错: {e}\n")
            
        # End the game/demo process
        self.gui_output("--------------------\n")
        self.end_game()

    # Remove the console entry point