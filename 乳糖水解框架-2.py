# 依赖项安装指南：
# 请确保已安装以下库：
# pip install streamlit numpy scipy matplotlib pandas

import streamlit as st
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.font_manager as fm

# 检查 Streamlit 版本
try:
    import streamlit as st
    if st.__version__ < '1.0.0':
        st.warning("请升级 Streamlit 到最新版本以获得最佳体验。")
except ImportError:
    st.error("Streamlit 未安装，请使用 'pip install streamlit' 安装。")

# 尝试使用系统默认字体
try:
    zh_font = fm.FontProperties(family='SimSun')  # 尝试使用宋体
    en_font = fm.FontProperties(family='Times New Roman')
    plt.rcParams['axes.unicode_minus'] = False
except:
    st.warning("字体设置失败，图表可能无法正确显示")
    zh_font = None
    en_font = None

st.set_page_config(page_title="乳糖水解动力学模拟 - 教学版", layout="wide")

# 语言选择
language = st.sidebar.selectbox("选择语言 / Select Language", ["中文", "English"])
lang = "zh" if language == "中文" else "en"

# 翻译字典
translations = {
    "zh": {
        "title": "🍼 乳糖水解动力学模拟 - 教学版",
        "intro": """
        ### 欢迎体验乳糖水解模拟
        乳糖水解是乳糖在β-半乳糖苷酶作用下分解为半乳糖和葡萄糖的过程，广泛应用于食品工业（如乳糖不耐受产品的生产）。本工具通过动力学模型模拟这一过程，帮助你理解酶催化反应和产物抑制的影响。

        **学习目标：**
        - 掌握Michaelis-Menten动力学的基本原理。
        - 理解产物抑制（半乳糖抑制）如何影响反应速率。
        - 通过交互式模拟，探索参数对乳糖水解的影响。
        """,
        "model_desc": "该模型模拟乳糖在β-半乳糖苷酶作用下的水解过程，考虑产物抑制效应（半乳糖抑制）。",
        "equation": r"\frac{dL}{dt} = -\frac{V_{max} \cdot L}{K_m \cdot (1 + \frac{Gal}{K_i}) + L}",
        "gal_desc": "其中 $Gal = L_0 - L$ 表示生成的半乳糖浓度",
        "reaction_params": "反应参数",
        "initial_lactose": "初始乳糖浓度 (mM) - 反应开始时的乳糖量",
        "enzyme_conc": "酶浓度 (U/mL) - 决定反应速率的关键因素",
        "reaction_time": "反应时间 (小时) - 模拟的总时间",
        "kinetic_params": "动力学参数",
        "km": "Km (mM) - 米氏常数，表示酶对底物的亲和力",
        "ki": "Ki (mM) - 抑制常数，表示半乳糖的抑制强度",
        "steps": "模拟精度 - 数值计算的步数",
        "theory": "理论背景",
        "theory_content": """
        **动力学模型：**
        - $L$: 乳糖浓度 (mM)
        - $Gal$: 半乳糖浓度 (mM)
        - $V_{max}$: 最大反应速率，与酶浓度 ($E$) 成正比
        - $K_m$: 米氏常数，表示酶对底物的亲和力（$K_m$ 越小，亲和力越高）
        - $K_i$: 产物抑制常数，表示半乳糖对酶的抑制强度（$K_i$ 越小，抑制越强）

        **微分方程推导：**
        根据Michaelis-Menten动力学，反应速率 $v = \frac{V_{max} \cdot L}{K_m + L}$。加入产物抑制后，分母变为 $K_m \cdot (1 + \frac{Gal}{K_i}) + L$，反映半乳糖的竞争性抑制效应。
        """,
        "equation_desc": "该方程考虑了产物半乳糖对酶活的竞争性抑制。",
        "inhibition_toggle": "启用产物抑制",
        "compare_inhibition": "比较有无产物抑制的模拟结果",
        "final_lactose": "最终乳糖浓度",
        "final_galactose": "最终半乳糖浓度",
        "conversion_rate": "转化率",
        "download_data": "下载模拟数据 (CSV)",
        "rate_analysis": "反应速率分析",
        "max_rate": "最大反应速率: **{:.2f} mM/小时** (发生在 {:.1f} 小时)",
        "exercises": "练习题",
        "exercise_content": """
        1. 如果酶浓度加倍，乳糖水解速率会如何变化？尝试调整参数并观察结果。
        2. 在什么条件下，产物抑制对反应速率的影响最小？调整 $K_i$ 值并分析。
        3. 使用模拟工具，找到使转化率达到90%所需的最短反应时间。
        """,
        "error": "计算错误: {}",
        "copyright": "© 生物反应工程教学模拟器 | 基于Michaelis-Menten动力学与产物抑制模型"
    },
    "en": {
        "title": "🍼 Lactose Hydrolysis Kinetics Simulation - Educational Version",
        "intro": """
        ### Welcome to Lactose Hydrolysis Simulation
        Lactose hydrolysis is the process where lactose is broken down into galactose and glucose by β-galactosidase, widely used in the food industry (e.g., lactose-free products). This tool simulates this process using a kinetic model, helping you understand enzyme catalysis and product inhibition effects.

        **Learning Objectives:**
        - Understand the basics of Michaelis-Menten kinetics.
        - Explore how product inhibition (galactose) affects reaction rates.
        - Investigate parameter effects on lactose hydrolysis through interactive simulation.
        """,
        "model_desc": "This model simulates lactose hydrolysis by β-galactosidase, considering product inhibition (galactose inhibition).",
        "equation": r"\frac{dL}{dt} = -\frac{V_{max} \cdot L}{K_m \cdot (1 + \frac{Gal}{K_i}) + L}",
        "gal_desc": "where $Gal = L_0 - L$ represents the concentration of produced galactose",
        "reaction_params": "Reaction Parameters",
        "initial_lactose": "Initial Lactose Concentration (mM) - Amount of lactose at the start",
        "enzyme_conc": "Enzyme Concentration (U/mL) - Key factor determining reaction rate",
        "reaction_time": "Reaction Time (hours) - Total simulation duration",
        "kinetic_params": "Kinetic Parameters",
        "km": "Km (mM) - Michaelis Constant, indicating enzyme-substrate affinity",
        "ki": "Ki (mM) - Inhibition Constant, indicating galactose inhibition strength",
        "steps": "Simulation Precision - Number of calculation points",
        "theory": "Theoretical Background",
        "theory_content": """
        **Kinetic Model:**
        - $L$: Lactose concentration (mM)
        - $Gal$: Galactose concentration (mM)
        - $V_{max}$: Maximum reaction rate, proportional to enzyme concentration ($E$)
        - $K_m$: Michaelis constant, indicating enzyme-substrate affinity (lower $K_m$, higher affinity)
        - $K_i$: Product inhibition constant, indicating galactose inhibition strength (lower $K_i$, stronger inhibition)

        **Differential Equation Derivation:**
        Based on Michaelis-Menten kinetics, the reaction rate is $v = \frac{V_{max} \cdot L}{K_m + L}$。With product inhibition, the denominator becomes $K_m \cdot (1 + \frac{Gal}{K_i}) + L$, reflecting galactose’s competitive inhibition.
        """,
        "equation_desc": "This equation accounts for the competitive inhibition of the enzyme by the product galactose.",
        "inhibition_toggle": "Enable Product Inhibition",
        "compare_inhibition": "Compare Simulation with and without Product Inhibition",
        "final_lactose": "Final Lactose Concentration",
        "final_galactose": "Final Galactose Concentration",
        "conversion_rate": "Conversion Rate",
        "download_data": "Download Simulation Data (CSV)",
        "rate_analysis": "Reaction Rate Analysis",
        "max_rate": "Maximum Reaction Rate: **{:.2f} mM/hour** (occurs at {:.1f} hours)",
        "exercises": "Exercises",
        "exercise_content": """
        1. How does doubling the enzyme concentration affect the hydrolysis rate? Adjust the parameters and observe.
        2. Under what conditions is the effect of product inhibition minimal? Adjust $K_i$ and analyze.
        3. Use the tool to find the shortest reaction time needed for a 90% conversion rate.
        """,
        "error": "Calculation Error: {}",
        "copyright": "© Bioreaction Engineering Educational Simulator | Based on Michaelis-Menten Kinetics with Product Inhibition Model"
    }
}

t = translations[lang]

st.title(t["title"])
st.markdown(t["intro"])

# 主界面
st.markdown(t["model_desc"])
st.latex(t["equation"])
st.markdown(t["gal_desc"])

# 创建两列布局
col1, col2 = st.columns(2)

with col1:
    st.header(t["reaction_params"])
    L0 = st.slider(
        label=t["initial_lactose"],
        min_value=0.1,
        max_value=500.0,
        value=200.0,
        step=0.1,
        help="反应开始时的乳糖浓度 (mM)"
    )
    E = st.slider(
        label=t["enzyme_conc"],
        min_value=0.001,
        max_value=10.0,
        value=1.0,
        step=0.001,
        help="酶浓度 (U/mL)，影响反应速率"
    )
    t_max = st.slider(
        label=t["reaction_time"],
        min_value=0.0,
        max_value=12.0,
        value=1.0,
        step=0.01,
        help="模拟的反应时间 (小时)"
    )

with col2:
    st.header(t["kinetic_params"])
    Km = st.slider(
        label=t["km"],
        min_value=0.1,
        max_value=50.0,
        value=30.0,
        step=0.1,
        help="米氏常数 (mM)，表示酶对底物的亲和力"
    )
    inhibition_enabled = st.checkbox(t["inhibition_toggle"], value=True)
    Ki = st.slider(
        label=t["ki"],
        min_value=0.1,
        max_value=50.0,
        value=10.0,
        step=0.1,
        disabled=not inhibition_enabled,
        help="抑制常数 (mM)，表示半乳糖的抑制强度"
    )
    steps = st.slider(
        label=t["steps"],
        min_value=50,
        max_value=500,
        value=200,
        step=1,
        help="数值计算的步数，影响模拟精度"
    )

# 理论背景
with st.expander(t["theory"]):
    st.markdown(t["theory_content"])
    st.latex(t["equation"])
    st.markdown(t["equation_desc"])

# 模拟函数
@st.cache_data
def solve_model(L0, Vmax, Km, Ki, t_max, steps, inhibition=True):
    if L0 <= 0 or Vmax <= 0 or Km <= 0 or (inhibition and Ki <= 0):
        raise ValueError("参数必须为正数")
    t_min = np.linspace(0, t_max * 60, steps)
    if not inhibition:
        Ki = 1e6  # 模拟无抑制情况
    sol = odeint(model, L0, t_min, args=(Vmax, Km, Ki, L0))
    L = sol[:, 0]
    Gal = np.maximum(L0 - L, 0)
    t_hour = t_min / 60
    rates = np.abs(np.gradient(L, t_hour))
    return t_hour, L, Gal, rates

def model(L, t, Vmax, Km, Ki, L0):
    L = max(L, 1e-6)
    Gal = L0 - L
    denominator = Km * (1 + Gal / Ki) + L
    dLdt = -Vmax * L / denominator
    return dLdt

try:
    Vmax = E
    t_hour, L, Gal, rates = solve_model(L0, Vmax, Km, Ki, t_max, steps, inhibition=inhibition_enabled)
    conversion = (1 - L[-1] / L0) * 100

    # 可视化
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(t_hour, L, color='#4E6691', linewidth=2.5, label=f"{t['final_lactose']}: {L[-1]:.1f} mM")
    ax.plot(t_hour, Gal, color='#B8474D', linewidth=2.5, label=f"{t['final_galactose']}: {Gal[-1]:.1f} mM")

    # 比较有无抑制
    if st.checkbox(t["compare_inhibition"]):
        t_hour_no_inh, L_no_inh, Gal_no_inh, rates_no_inh = solve_model(L0, Vmax, Km, Ki, t_max, steps, inhibition=False)
        ax.plot(t_hour_no_inh, L_no_inh, 'b--', label="Lactose (No Inhibition)")
        ax.plot(t_hour_no_inh, Gal_no_inh, 'r--', label="Galactose (No Inhibition)")

    ax.annotate(f'{conversion:.1f}% {t["conversion_rate"]}',
                xy=(t_hour[-1], Gal[-1]),
                xytext=(t_hour[-1] - 1, Gal[-1] + 0.05 * L0),
                arrowprops=dict(arrowstyle='->', color='green'),
                fontsize=12, color='green', fontproperties=zh_font if lang == "zh" else en_font)
    ax.set_xlabel("Time (hours)", fontsize=12, fontproperties=en_font)
    ax.set_ylabel("Concentration (mM)", fontsize=12, fontproperties=en_font)
    ax.set_title("Lactose Hydrolysis Kinetics", fontsize=14, fontproperties=en_font)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(loc='best', fontsize=12, prop=zh_font if lang == "zh" else en_font)
    ax.set_xlim([0, t_max])
    ax.set_ylim([0, L0 * 1.1])
    for spine in ax.spines.values():
        spine.set_linewidth(2.5)
    st.pyplot(fig)

    # 关键指标
    col1, col2, col3 = st.columns(3)
    col1.metric(t["final_lactose"], f"{L[-1]:.1f} mM")
    col2.metric(t["final_galactose"], f"{Gal[-1]:.1f} mM")
    col3.metric(t["conversion_rate"], f"{conversion:.1f}%")

    # 数据下载
    df = pd.DataFrame({'Time (hours)': t_hour, 'Lactose (mM)': L, 'Galactose (mM)': Gal, 'Reaction Rate (mM/hour)': rates})
    csv = df.to_csv(index=False).encode('utf-8-sig')  # 支持中文
    st.download_button(label=t["download_data"], data=csv, file_name='lactose_hydrolysis_data.csv', mime='text/csv')

    # 反应速率分析
    st.subheader(t["rate_analysis"])
    fig2, ax2 = plt.subplots(figsize=(10, 6))

    # 首先绘制有抑制曲线
    ax2.plot(L, rates, color='#4E6691', linewidth=2.5, label="With Inhibition")

    # 检查是否显示无抑制曲线
    show_inhibition_comparison = st.checkbox(t["compare_inhibition"], key="rate_compare")
    if show_inhibition_comparison:
        # 计算无抑制曲线数据
        t_hour_no_inh, L_no_inh, Gal_no_inh, rates_no_inh = solve_model(L0, Vmax, Km, Ki, t_max, steps, inhibition=False)

        # 绘制无抑制曲线
        ax2.plot(L_no_inh, rates_no_inh, 'b--', linewidth=2.5, label="No Inhibition")

        # 使用无抑制曲线数据进行标注
        substrate = L_no_inh
        rate_vals = rates_no_inh

        # 计算最大反应速率及其位置
        r_max = rate_vals.max()
        max_idx = np.argmax(rate_vals)
        max_substrate = substrate[max_idx]

        # 添加最大速率标注
        ax2.axhline(y=r_max, color='gray', linestyle='--', linewidth=1.5, alpha=0.7)
        ax2.text(0.02 * L0, r_max * 1.02, r'$r_{max} = k_2 \cdot C_{E0}$',
                 fontsize=12, color='gray', verticalalignment='bottom')

        # 找到速率等于最大速率一半的点
        half_max = r_max / 2
        half_idx = np.argmin(np.abs(rate_vals - half_max))
        half_substrate = substrate[half_idx]

        # 添加半速率点标注
        ax2.plot(half_substrate, half_max, 'go', markersize=8)
        ax2.text(half_substrate * 1.02, half_max * 1.05, r'$r = r_{max} / 2$',
                 fontsize=12, color='green')

        # 添加垂直线和Km标注
        ax2.plot([half_substrate, half_substrate], [0, half_max], 'g--', linewidth=1.5, alpha=0.7)
        ax2.text(half_substrate, -0.05 * r_max, r'$C_s = K_m$',
                 fontsize=12, color='green', horizontalalignment='center', verticalalignment='top')

        # 设置坐标轴范围
        ax2.set_ylim([0, r_max * 1.2])
        if half_substrate < 0.1 * L0:
            ax2.set_ylim(bottom=-0.1 * r_max)
    else:
        # 如果不显示无抑制曲线，只设置基础Y轴范围
        ax2.set_ylim([0, rates.max() * 1.2])

    ax2.set_xlabel("Substrate Concentration L (mM)", fontsize=12, fontproperties=en_font)
    ax2.set_ylabel("Reaction Rate (mM/hour)", fontsize=12, fontproperties=en_font)
    ax2.set_title("Reaction Rate vs. Substrate Concentration", fontsize=14, fontproperties=en_font)
    ax2.grid(True, linestyle='--', alpha=0.7)
    ax2.legend(loc='best', prop=zh_font if lang == "zh" else en_font)
    ax2.set_xlim([0, L0])

    for spine in ax2.spines.values():
        spine.set_linewidth(2.5)
    st.pyplot(fig2)

    # Lineweaver-Burk 图表
    st.subheader("Lineweaver-Burk 图表")
    Gal_fixed = st.slider("竞争性抑制中的固定半乳糖浓度 (mM)", 0.0, 200.0, 100.0)
    S_range = np.linspace(1, 500, 20)
    v_no_inh = Vmax * S_range / (Km + S_range)
    v_inh = Vmax * S_range / (Km * (1 + Gal_fixed / Ki) + S_range)

    # 计算1/[S]和1/v
    inv_S = 1 / S_range
    inv_v_no_inh = 1 / v_no_inh
    inv_v_inh = 1 / v_inh

    fig_lb, ax_lb = plt.subplots(figsize=(10, 6))
    p_no_inh = np.polyfit(inv_S, inv_v_no_inh, 1)
    x_fit_no_inh = np.linspace(-0.05, max(inv_S), 100)
    y_fit_no_inh = np.polyval(p_no_inh, x_fit_no_inh)
    ax_lb.plot(x_fit_no_inh, y_fit_no_inh, color='#4E6691', linewidth=2.5, label="无抑制剂")

    p_inh = np.polyfit(inv_S, inv_v_inh, 1)
    x_fit_inh = np.linspace(-0.05, max(inv_S), 100)
    y_fit_inh = np.polyval(p_inh, x_fit_inh)
    ax_lb.plot(x_fit_inh, y_fit_inh, color='#B8474D', linewidth=2.5, label="竞争性抑制")

    ax_lb.set_xlim(-0.05, 0.1)
    slope_no_inh = p_no_inh[0]
    x_range = 0.1 - (-0.05)
    y_max = x_range * slope_no_inh
    ax_lb.set_ylim(0, y_max * 1.2)

    y_intercept = p_no_inh[1]
    ax_lb.plot([0, 0], [0, y_intercept], 'g--', linewidth=2, alpha=0.7)
    ax_lb.plot(0, y_intercept, 'go', markersize=8)

    # 使用箭头标注 "1/r_{max}"，箭头指向绿色虚线中间
    ax_lb.annotate(r'$1 / r_{max}$', xy=(0, y_intercept / 2), xytext=(0.02, y_intercept / 2 + 0.02),
                   arrowprops=dict(arrowstyle='->', color='green'),
                   fontsize=12, fontproperties=en_font, ha='left', va='bottom')

    x_intercept_no_inh = -p_no_inh[1] / p_no_inh[0]
    ax_lb.plot(x_intercept_no_inh, 0, marker='*', color='#4E6691', markersize=10)

    # 使用箭头标注 "-1/K_m"，与x轴标签齐平，位于交点下方
    ax_lb.annotate(r'$-1 / K_m$', xy=(x_intercept_no_inh, 0), xytext=(x_intercept_no_inh, -0.115 * y_max),
                   arrowprops=dict(arrowstyle='->', color='green'),
                   fontsize=12, fontproperties=en_font, ha='center', va='top')

    x_intercept_inh = -p_inh[1] / p_inh[0]
    ax_lb.plot(x_intercept_inh, 0, marker='*', color='#B8474D', markersize=10)

    # 使用箭头标注 "-1/K_m(1+c_1/K_1)"，与x轴标签齐平，位于交点下方
    ax_lb.annotate(r'$-1 / K_m (1 + \frac{c_1}{K_1})$', xy=(x_intercept_inh, 0), xytext=(x_intercept_inh, -0.145 * y_max),
                   arrowprops=dict(arrowstyle='->', color='green'),
                   fontsize=12, fontproperties=en_font, ha='center', va='top')

    ax_lb.set_xlabel("1 / [S] (1/mM)", fontsize=12, fontproperties=en_font)
    ax_lb.set_ylabel("1 / v (hour/mM)", fontsize=12, fontproperties=en_font)
    ax_lb.set_title("Lineweaver-Burk", fontsize=14, fontproperties=en_font)
    ax_lb.legend(loc='best', prop=zh_font if lang == "zh" else en_font)
    ax_lb.grid(True, linestyle='--', alpha=0.7)
    for spine in ax_lb.spines.values():
        spine.set_linewidth(2.5)
    st.pyplot(fig_lb)

    st.markdown("""
    **说明：** 蓝色线条表示无抑制剂情况，遵循标准Michaelis-Menten动力学。红色线条表示固定半乳糖浓度下的竞争性抑制。
    注意两条线在y轴上的交点相同（绿色点），这表明竞争性抑制不影响 $V_{max}$，但改变了表观 $K_m$（与X轴负半轴的交点不同，蓝色和红色星号）。
    """)

    # 练习题
    with st.expander(t["exercises"]):
        st.markdown(t["exercise_content"])

except Exception as e:
    st.error(t["error"].format(str(e)))
    st.stop()

st.caption(t["copyright"])