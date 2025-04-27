import tkinter as tk
from tkinter import messagebox, scrolledtext
import sys
import os
import matplotlib.pyplot as plt
from quantum_descriptions import QUANTUM_GAME_DESCRIPTIONS
import tkinter.messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# 将项目根目录添加到 Python 路径
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

try:
    from quantum_logic.games import QuantumGames
except ImportError as e:
    messagebox.showerror("导入错误", f"无法导入 QuantumGames 类: {e}\n请确保 quantum_logic 模块在 Python 路径中。")
    sys.exit(1)

def clear_frame(frame):
    """Removes all widgets from a Tkinter frame."""
    for widget in frame.winfo_children():
        widget.destroy()

class QuantumGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("量子游戏与演示")
        self.root.configure(bg="#f5f7fa")  # 主窗口背景色
        # 设置全局字体
        self.root.option_add("*Font", "微软雅黑 11")
        # 增加顶部标题栏
        title_label = tk.Label(self.root, text="量子游戏集合 Quantum Games", font=("微软雅黑", 18, "bold"), fg="#2d3a4b", bg="#f5f7fa", pady=12)
        title_label.pack(side=tk.TOP, fill=tk.X)
        # 主frame下移，避免与标题重叠
        # self.root.geometry("800x700") # Optional: Increase height for multiple plots

        # --- Game Logic Instance ---
        # Pass the new display_plots_list method during initialization
        self.game_logic = QuantumGames(
            gui_output_func=self.display_output,
            request_input_func=None,  # 不再需要输入
            end_game_func=self.end_game_ui,
            gui_display_plots_func=self.display_plots_list
        )
        # self.plot_canvas_widget = None # OLD: single plot
        self.plot_canvas_widgets = [] # NEW: List to hold multiple plot canvases

        # --- Main Frame using grid layout ---
        main_frame = tk.Frame(self.root, bg="#f5f7fa")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0,15))
        main_frame.columnconfigure(0, weight=0) 
        main_frame.columnconfigure(1, weight=1)  # 右侧整体

        # 新增右侧大frame（只含输出和可视化）
        right_frame = tk.Frame(main_frame)
        right_frame.grid(row=0, column=1, rowspan=2, sticky="nsew")
        right_frame.rowconfigure(0, weight=1)   # 输出区
        right_frame.rowconfigure(1, weight=3)   # 可视化区
        right_frame.columnconfigure(0, weight=1)

        # 主frame底部说明区权重
        main_frame.rowconfigure(2, weight=0)

        # --- Control frame (Left - Column 0) ---
        control_frame = tk.LabelFrame(main_frame, text="控制面板", padx=10, pady=10)
        control_frame.grid(row=0, column=0, rowspan=3, padx=(0, 5), pady=0, sticky="nsew") 

        # Demo Buttons (Using standardized names)
        demo_buttons = {
            "量子叠加态演示": ("superposition", self.game_logic.run_superposition_demo),
            "量子纠缠态演示 (Bell 态)": ("bell", self.game_logic.run_entanglement_game),
            "量子隐形传态演示": ("teleportation", self.game_logic.run_teleportation_game),
            "量子干涉实验 (HZH)": ("interference", self.game_logic.run_interference_game),
            "Deutsch-Jozsa 演示": ("deutsch_jozsa", self.game_logic.run_deutsch_jozsa_demo),
            "Grover 搜索演示": ("grover", self.game_logic.run_grover_search_demo),
            "QFT 演示": ("qft", self.game_logic.run_qft_demo),
        }
        for text, (desc_key, command) in demo_buttons.items():
            # 点击按钮时，右侧说明框自动更新
            def make_callback(cmd=command, key=desc_key):
                def callback():
                    desc = QUANTUM_GAME_DESCRIPTIONS.get(key)
                    if desc:
                        info = f"{desc['title']}\n\n【算法原理】\n{desc['principle']}\n\n【电路结构】\n{desc['circuit']}\n\n【直方图解释】\n{desc['histogram']}"
                        self.description_var.set(info)
                    self.run_game(cmd)
                return callback
            button = tk.Button(control_frame, text=text, command=make_callback(), width=25,
                              bg="#4f8cff", fg="white", activebackground="#2d3a4b", activeforeground="white", relief=tk.FLAT, bd=2, highlightthickness=0)
            button.pack(pady=6, fill=tk.X, ipadx=2, ipady=2)

        # Game Buttons (Using standardized names)
        game_buttons = {
            "量子猜硬币游戏": self.game_logic.run_coin_game # Corrected name
        }
        tk.Label(control_frame, text="---").pack(pady=5) # Separator
        for text, command in game_buttons.items():
            # 猜硬币按钮集成说明
            def make_coin_callback(cmd=command):
                def callback():
                    from quantum_descriptions import QUANTUM_GAME_DESCRIPTIONS
                    desc = QUANTUM_GAME_DESCRIPTIONS.get("coin")
                    if desc:
                        info = f"{desc['title']}\n\n【算法原理】\n{desc['principle']}\n\n【电路结构】\n{desc['circuit']}\n\n【直方图解释】\n{desc['histogram']}"
                        self.description_var.set(info)
                    self.run_game(cmd)
                return callback
            button = tk.Button(control_frame, text=text, command=make_coin_callback(), width=25,
                              bg="#00bfae", fg="white", activebackground="#2d3a4b", activeforeground="white", relief=tk.FLAT, bd=2, highlightthickness=0)
            button.pack(pady=8, fill=tk.X, ipadx=2, ipady=2)

        # --- Output Area (Right-Top - Column 1, Row 0) ---
        output_frame = tk.LabelFrame(right_frame, text="输出信息", padx=8, pady=8, bg="#f9fafc", fg="#2d3a4b", font=("微软雅黑", 11, "bold"), bd=2, relief=tk.GROOVE)
        output_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=(0,8))
        output_frame.rowconfigure(0, weight=1)
        output_frame.columnconfigure(0, weight=1)

        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, height=10, width=60, state='disabled', bg="#f9fafc", fg="#2d3a4b", bd=1, relief=tk.FLAT)
        self.output_text.grid(row=0, column=0, sticky="nsew")

        # --- Description Area (底部横跨) ---
        description_frame = tk.LabelFrame(main_frame, text="算法说明", padx=8, pady=8, bg="#f9fafc", fg="#2d3a4b", font=("微软雅黑", 11, "bold"), bd=2, relief=tk.GROOVE)
        description_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=8, pady=(0,8))
        description_frame.rowconfigure(0, weight=1)
        description_frame.columnconfigure(0, weight=1)
        self.description_var = tk.StringVar()
        self.description_label = tk.Label(description_frame, textvariable=self.description_var, justify="left", anchor="nw", wraplength=700, bg="#f9fafc", fg="#2d3a4b")
        self.description_label.grid(row=0, column=0, sticky="ew")

        # --- Visualization Area (Right-Bottom - Column 1, Row 2) ---
        self.plot_frame = tk.LabelFrame(right_frame, text="可视化区域", padx=8, pady=8, bg="#f9fafc", fg="#2d3a4b", font=("微软雅黑", 11, "bold"), bd=2, relief=tk.GROOVE)
        self.plot_frame.grid(row=2, column=0, padx=(8, 0), pady=(0, 8), sticky="nsew")
        self.plot_frame.grid_rowconfigure(0, weight=1)
        self.plot_frame.grid_columnconfigure(0, weight=1)

        # Create a Canvas widget within the plot_frame
        self.plot_canvas = tk.Canvas(self.plot_frame)
        # Create a Scrollbar linked to the canvas
        self.plot_scrollbar = tk.Scrollbar(self.plot_frame, orient="vertical", command=self.plot_canvas.yview)
        # Create the frame INSIDE the canvas that will hold the plots
        self.inner_plot_frame = tk.Frame(self.plot_canvas)

        # Configure the canvas scrolling
        self.plot_canvas.configure(yscrollcommand=self.plot_scrollbar.set)

        # Grid the canvas and scrollbar within plot_frame
        self.plot_canvas.grid(row=0, column=0, sticky='nsew')
        self.plot_scrollbar.grid(row=0, column=1, sticky='ns')

        # Put the inner_plot_frame inside the canvas window
        self.canvas_window = self.plot_canvas.create_window((0, 0), window=self.inner_plot_frame, anchor="nw")

        # Update scrollregion when the inner frame size changes
        self.inner_plot_frame.bind("<Configure>", self.on_inner_frame_configure)
        # Update canvas window width when the canvas size changes
        self.plot_canvas.bind('<Configure>', self.on_canvas_configure)

        # Keep track of plot widgets placed in the inner frame
        self.plot_canvas_widgets = [] 

        
        # --- Exit Button (Bottom - Spanning Columns, Row 3) ---
        self.exit_button = tk.Button(main_frame, text="退出", command=self.root.quit, bg="#e74c3c", fg="white", font=("微软雅黑", 12, "bold"), relief=tk.FLAT, bd=2, highlightthickness=0, activebackground="#c0392b")
        self.exit_button.grid(row=3, column=0, columnspan=2, pady=(10, 0), sticky="ew")

        # --- Game Logic Initialization Callbacks (Update this if method names changed in QuantumGames) ---
        # Pass the new display_plots_list method
        # self.game_logic.set_gui_callbacks(self.display_output, self.prompt_input, self.display_plot, self.end_game_ui, self.display_plots_list) 
        # Note: QuantumGames __init__ already sets callbacks if passed
        self.display_output("欢迎来到量子游戏应用程序! 请选择一个演示或游戏。\n")

    def on_inner_frame_configure(self, event):
        """Update scroll region when inner frame size changes."""
        self.plot_canvas.configure(scrollregion=self.plot_canvas.bbox("all"))

    def on_canvas_configure(self, event):
        """Update the width of the inner frame to match the canvas width."""
        canvas_width = event.width
        self.plot_canvas.itemconfig(self.canvas_window, width=canvas_width)

    def run_game(self, game_function):
        """Wrapper to clear output and run selected game/demo."""
        # Clear previous plots
        self.clear_plot_area() 
        # Clear output text
        self.display_output("", clear=True)
        # 已无输入区，无需禁用输入控件
        # Run the game function
        try:
            game_function() 
        except Exception as e:
            self.display_output(f"\n运行游戏时发生错误: {e}\n")
            import traceback
            self.display_output(traceback.format_exc() + "\n") # Show full traceback
            self.end_game_ui() # Ensure UI is reset even on error

    def end_game_ui(self):
        """Resets UI elements after a game ends (e.g., disable input)."""
        # 已无输入区，无需禁用输入控件
        # DO NOT clear the plot here

    def display_output(self, message, clear=False):
        self.output_text.configure(state='normal')
        if clear:
            self.output_text.delete('1.0', tk.END)
        self.output_text.insert(tk.END, str(message))
        self.output_text.see(tk.END) # Scroll to end
        self.output_text.configure(state='disabled')


    def display_plots_list(self, figures):
        """Displays a LIST of matplotlib figures vertically in the **scrollable** plot area."""
        self.clear_plot_area() # Clear previous plots first
        if not figures:
            self.display_output("没有可显示的绘图。")
            return
        
        self.display_output(f"准备显示 {len(figures)} 个图表...")
        try:
            for i, fig in enumerate(figures):
                if fig is None:
                    self.display_output(f"警告：图表 {i+1} 为空，跳过。")
                    continue
                
                # Embed the plot in the INNER frame
                canvas = FigureCanvasTkAgg(fig, master=self.inner_plot_frame)
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.pack(side=tk.TOP, fill=tk.X, expand=False, pady=5) # Pack vertically
                self.plot_canvas_widgets.append(canvas_widget) # Store reference for clearing
                canvas.draw()
                plt.close(fig) # Close the mpl figure to save memory
                self.display_output(f"图表 {i+1} 已绘制。")
            
            self.root.update_idletasks() # Ensure layout updates
            # Reset scroll region after adding all plots
            self.plot_canvas.configure(scrollregion=self.plot_canvas.bbox("all")) 
            self.plot_canvas.yview_moveto(0) # Scroll to top
            self.display_output("所有图表显示完成。")

        except Exception as e:
            self.display_output(f"\n显示绘图列表时出错: {e}\n")
            self.clear_plot_area()

    def clear_plot_area(self):
        """Destroys all plot canvases currently in the **inner** plot frame."""
        for widget in self.plot_canvas_widgets:
            widget.destroy()
        self.plot_canvas_widgets = []
        # Reset scroll region
        # self.plot_canvas.configure(scrollregion=self.plot_canvas.bbox("all")) 
        # Seems better to not reset scrollregion here, let it update naturally
        self.root.update_idletasks()


# --- Main Application Execution ---
if __name__ == "__main__":
    root = tk.Tk()
    app = QuantumGameApp(root)
    root.mainloop()