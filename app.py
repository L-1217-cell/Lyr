import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time
import streamlit.components.v1 as components

# ==========================================
# 1. 页面基础设置
# ==========================================
st.set_page_config(page_title="西安财经专属财税大脑", page_icon="🏦", layout="wide")

# ==========================================
# 2. 注入全局高级 CSS 美化
# ==========================================
st.markdown("""
<style>
    /* 全局背景淡雅渐变 */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
    }
    
    /* 左侧侧边栏深色质感 */
    [data-testid="stSidebar"] {
        background-color: #1e293b !important;
    }
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    
    /* 按钮渐变色和阴影 */
    .stButton>button {
        background: linear-gradient(to right, #4facfe 0%, #00f2fe 100%);
        color: white;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border-radius: 8px;
        font-weight: bold;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
    }
    
    /* Tabs样式 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #ffffff;
        border-radius: 8px 8px 0px 0px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    /* 自定义彩色数据卡片 */
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        text-align: center;
        border-top: 5px solid #4facfe;
        margin-bottom: 15px;
    }
    .metric-title { font-size: 14px; color: #64748b; margin-bottom: 10px; font-weight: bold;}
    .metric-value { font-size: 24px; color: #1e293b; font-weight: 800; }
    .metric-delta { font-size: 12px; margin-top: 5px; }
    .card-green { border-top-color: #10b981; }
    .card-orange { border-top-color: #f59e0b; }
    .card-purple { border-top-color: #8b5cf6; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 初始化全局状态
# ==========================================
if 'company_info' not in st.session_state:
    st.session_state.company_info = {
        "name": "西安财经有限公司", "industry": "信息技术", "scale": "小型微利"
    }
if 'uploaded_data' not in st.session_state:
    st.session_state.uploaded_data = None

# ==========================================
# 4. 左侧侧边栏：导航与署名
# ==========================================
with st.sidebar:
    st.title("🧭 功能导航")
    st.markdown("---")
    
    menu = st.radio("请选择模块", [
        "🏢 企业中心", 
        "📤 数据上传", 
        "🧮 计税申报", 
        "📜 政策中心", 
        "⚠️ 风险看板", 
        "🤖 智能问答",
        "🔔 消息提醒"
    ])
    
    st.markdown("---")
    st.success("✅ 系统运行正常\n\n📩 您有 1 条未读政策提醒")
    
    # 你的专属署名
    st.info("👨‍💻 开发者：李垚如\n\n🏫 西安财经大学")

# ==========================================
# 5. 主页面数据看板（彩色卡片）
# ==========================================
st.title("📊 智慧财税管理智能体")
st.caption(f"当前计税主体：**{st.session_state.company_info['name']}** | 行业：**{st.session_state.company_info['industry']}** | 规模：**{st.session_state.company_info['scale']}**")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown("""<div class="metric-card">
        <div class="metric-title">💰 本期预估应纳税额</div>
        <div class="metric-value">¥ 114,910.00</div>
        <div class="metric-delta" style="color: #10b981;">↑ 环比 +1.9%</div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown("""<div class="metric-card card-green">
        <div class="metric-title">📤 本期销项税额</div>
        <div class="metric-value">¥ 1,500,000.00</div>
        <div class="metric-delta" style="color: #10b981;">↑ 环比 +0.8%</div>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown("""<div class="metric-card card-orange">
        <div class="metric-title">📥 本期进项税额</div>
        <div class="metric-value">¥ 360,000.00</div>
        <div class="metric-delta" style="color: #ef4444;">↓ 环比 -0.3%</div>
    </div>""", unsafe_allow_html=True)
with c4:
    st.markdown("""<div class="metric-card card-purple">
        <div class="metric-title">📊 当前适用增值税率</div>
        <div class="metric-value">13.0%</div>
        <div class="metric-delta" style="color: #64748b;">一般纳税人</div>
    </div>""", unsafe_allow_html=True)

st.divider()

# ==========================================
# 6. 各功能模块开发
# ==========================================

# 模块一：企业中心
if menu == "🏢 企业中心":
    st.header("🏢 企业基础信息中心")
    st.info("请完善企业画像，系统将基于此构建知识图谱并匹配政策。")
    
    col1, col2 = st.columns(2)
    with col1:
        c_name = st.text_input("企业名称", value=st.session_state.company_info["name"])
        c_ind = st.selectbox("所属行业", ["信息技术", "制造业", "批发零售", "服务业"], index=0)
    with col2:
        c_scale = st.radio("企业规模", ["小型微利", "一般企业"], horizontal=True)
        c_region = st.selectbox("注册地", ["陕西省西安市", "北京市", "广东省"])
        
    if st.button("保存企业画像"):
        st.session_state.company_info = {"name": c_name, "industry": c_ind, "scale": c_scale}
        st.success("企业画像已更新！知识图谱库已刷新。")

# 模块二：数据上传
if menu == "📤 数据上传":
    st.header("📤 多源数据接入与清洗")
    st.markdown("支持接入财务系统报表、发票系统、银行流水等。")
    
    uploaded_file = st.file_uploader("请上传财务报表 (CSV 或 Excel)", type=["csv", "xlsx"])
    
    if uploaded_file is not None:
        with st.spinner("AI 正在执行数据去重、异常值过滤与标准化..."):
            time.sleep(1.5)
            data = pd.DataFrame({
                "凭证号": ["记-001", "记-002", "记-003"],
                "摘要": ["销售软件产品", "采购办公用品", "支付员工工资"],
                "金额": [100000, 5000, 30000],
                "税额": [13000, 650, 0]
            })
            st.session_state.uploaded_data = data
            st.success("✅ 数据清洗完成！业务-会计科目-税种勾稽关系校验通过。")
            st.dataframe(data, use_container_width=True)

# 模块三：计税申报（含语音播报）
if menu == "🧮 计税申报":
    st.header("🧮 智能自动计税引擎")
    st.caption(f"当前计税主体：{st.session_state.company_info['name']} | 适用规则库：2026版")
    
    with st.form("tax_form"):
        st.subheader("1. 增值税计算")
        col1, col2, col3 = st.columns(3)
        sales = col1.number_input("本期不含税销售额 (元)", value=1000000.0)
        purchase = col2.number_input("本期进项税额 (元)", value=50000.0)
        vat_rate = col3.selectbox("适用税率", [0.13, 0.09, 0.06], format_func=lambda x: f"{int(x*100)}%")
        
        st.subheader("2. 企业所得税计算 (税会差异自动调整)")
        profit = st.number_input("本期会计利润总额 (元)", value=500000.0)
        
        submit = st.form_submit_button("一键计算并生成申报表")
        
    if submit:
        with st.spinner("AI 推理计算中..."):
            time.sleep(1)
            out_tax = sales * vat_rate
            vat_pay = max(out_tax - purchase, 0)
            
            if st.session_state.company_info["scale"] == "小型微利":
                cit_rate = 0.05
                msg = "✨ 触发小微优惠政策：实际税负 5%"
            else:
                cit_rate = 0.25
                msg = "适用一般企业所得税率 25%"
                
            cit_pay = profit * cit_rate
            
            st.success("计算完成！")
            st.info(msg)
            
            r1, r2 = st.columns(2)
            r1.metric("本期应纳增值税", f"¥ {vat_pay:,.2f}")
            r2.metric("本期应纳企业所得税", f"¥ {cit_pay:,.2f}")
            
            st.download_button("📥 下载标准纳税申报表 (Excel)", data="模拟Excel数据", file_name="申报表.xlsx")

            # --- 语音播报功能 ---
            st.markdown("### 🔊 智能语音播报")
            report_text = f"西安财经有限公司，本期计税已完成。本期应缴纳增值税{int(vat_pay)}元，企业所得税{int(cit_pay)}元。请及时进行申报。"
            
            audio_html = f"""
                <button onclick="speakText()" style="background-color: #ff4b4b; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 16px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    🔊 点击听取语音通报
                </button>
                <script>
                function speakText() {{
                    window.speechSynthesis.cancel(); 
                    var msg = new SpeechSynthesisUtterance();
                    msg.text = "{report_text}";
                    msg.lang = 'zh-CN'; 
                    msg.rate = 0.9; 
                    msg.pitch = 1.0; 
                    window.speechSynthesis.speak(msg);
                }}
                </script>
            """
            components.html(audio_html, height=60)

# 模块四：政策中心
if menu == "📜 政策中心":
    st.header("📜 税收政策智能匹配")
    st.markdown("### 🔍 基于企业画像的自动匹配结果")
    
    if st.session_state.company_info["scale"] == "小型微利":
        st.success("✅ 已享受：《财政部 税务总局关于进一步支持小微企业和个体工商户发展有关税费政策的公告》\n\n👉 减免金额测算：约 ¥ 120,000")
    else:
        st.warning("暂不满足小微企业减免条件。")
        
    st.markdown("### 📚 政策变动实时更新库")
    with st.expander("2026年10月 最新政策变动"):
        st.write("- 研发费用加计扣除比例调整通知")
        st.write("- 先进制造业企业增值税加计抵减政策")
        
    with st.expander("🏛️ 陕西省/西安市 特色惠企政策"):
        st.write("- 对新落户西咸新区秦创原总窗口的科技型企业，给予前三年企业所得税区级留成部分全额补贴。")
        st.write("- 高新技术企业研发费用加计扣除比例提升。")

# 模块五：风险看板
if menu == "⚠️ 风险看板":
    st.header("⚠️ 涉税风险动态看板")
    st.error("🚨 机器学习模型预警：发现 2 项高风险指标！")
    
    col1, col2 = st.columns(2)
    with col1:
        df_radar = pd.DataFrame(dict(
            r=[80, 60, 90, 40, 70],
            theta=['税负率异常', '进销项匹配度', '发票作废率', '利润波动', '存货周转']
        ))
        fig = px.line_polar(df_radar, r='r', theta='theta', line_close=True, title="企业健康度雷达图")
        fig.update_traces(fill='toself', line_color='#ef4444')
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.warning("**风险点 1**：本期增值税税负率 1.2%，低于行业均值 3%，触发异常预警。\n\n**风险点 2**：业务招待费占比偏高，存在汇算清缴调增风险。")
        st.button("生成合规整改建议书")

# 模块六：智能问答
if menu == "🤖 智能问答":
    st.header("🤖 财税 AI 助手")
    st.info("💡 基于大语言模型 (LLM) 与税收知识图谱构建，已学习最新财税法规。")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "您好！我是您的专属财税顾问，请问有什么可以帮您？"}]
        
    # 这里就是那个 for 循环，注意下一行必须缩进
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
        
    if prompt := st.chat_input("例如：小微企业的企业所得税怎么算？"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("AI 正在查阅税法知识库..."):
                time.sleep(1)
                if "小微" in prompt and "所得税" in prompt:
                    response = "根据最新政策，小型微利企业年应纳税所得额不超过300万元的部分，减按25%计入应纳税所得额，按20%的税率缴纳企业所得税（实际税负5%）。"
                elif "增值税" in prompt:
                    response = "一般纳税人增值税计算公式为：应纳税额 = 当期销项税额 - 当期进项税额。"
                else:
                    response = "收到您的问题。根据税收知识图谱分析，建议您前往【政策中心】查看具体匹配的法规，或完善企业信息以便我给出更精准的答复。"
                
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})