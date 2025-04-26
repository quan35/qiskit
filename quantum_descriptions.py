# quantum_descriptions.py
# 量子演示/游戏项目说明结构化字典
QUANTUM_GAME_DESCRIPTIONS = {
    "superposition": {
        "title": "量子叠加态演示",
        "principle": "量子比特可以处于0和1的叠加态。通过Hadamard门（H门），|0⟩变为(|0⟩+|1⟩)/√2，体现量子并行性和概率性。",
        "circuit": "每个量子比特应用一次H门，将其变为叠加态。",
        "histogram": "理想情况下，每个测量结果出现的概率相等，体现量子叠加本质。"
    },
    "bell": {
        "title": "量子纠缠态演示（Bell 态）",
        "principle": "通过H门和CNOT门将两个比特纠缠，测量其中一个会影响另一个，体现量子非定域性。",
        "circuit": "第一个比特H门产生叠加，CNOT门与第二个比特纠缠。",
        "histogram": "只会出现“00”或“11”，概率各50%，体现纠缠特性。"
    },
    "teleportation": {
        "title": "量子隐形传态演示",
        "principle": "通过纠缠和经典通信，将一个未知量子态“传送”到远处，体现量子信息的独特传递方式。",
        "circuit": "H+CNOT生成纠缠对，CNOT、H门、测量实现隐形传送协议。",
        "histogram": "测量后接收者比特处于原始量子态，不同测量结果概率分布体现传送过程。"
    },
    "interference": {
        "title": "量子干涉实验（HZH）",
        "principle": "展示量子相位对测量结果的影响。H-Z-H结构可改变最终概率分布。",
        "circuit": "H门叠加，Z门引入相位，H门实现干涉。",
        "histogram": "有Z门时测得|1⟩，无Z门时测得|0⟩，直方图体现干涉现象。"
    },
    "deutsch_jozsa": {
        "title": "Deutsch-Jozsa 算法演示",
        "principle": "通过量子并行和干涉，一次查询判断函数是常值还是平衡，展示量子加速。",
        "circuit": "H门输入比特叠加，Oracle门查询函数，H门干涉消除错误解。",
        "histogram": "常值函数测得全0，平衡函数不会全为0，直方图一目了然。"
    },
    "grover": {
        "title": "Grover 搜索算法演示",
        "principle": "通过幅度放大，√N次找到目标项，远快于经典搜索。",
        "circuit": "H门叠加，Oracle门标记目标态，多组H、X、CNOT等扩散算符放大目标概率。",
        "histogram": "目标态概率远高于其他，直方图柱子明显突出。"
    },
    "qft": {
        "title": "量子傅里叶变换（QFT）演示", 
        "principle": "QFT将量子态从计算基变换到傅里叶基，是周期性问题求解的核心。",
        "circuit": "H门和受控相位门（CP）实现傅里叶变换，SWAP门调整比特顺序。",
        "histogram": "测量结果呈周期性分布，体现输入态的频谱特征。"
    },
    "coin": {
        "title": "量子猜硬币游戏",
        "principle": "通过量子叠加与测量，模拟硬币正反状态的随机性。",
        "circuit": "对一个量子比特应用H门（Hadamard门），使其进入|0⟩和|1⟩的叠加态，然后测量。",
        "histogram": "理想情况下，|0⟩和|1⟩各有50%概率，直方图显示两种结果概率均等。"
    }
}
