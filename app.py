# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 17:17:48 2026

@author: 32404
"""
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import base64
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from io import BytesIO, StringIO
from scipy import stats
import json
import time
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import networkx as nx
import re
import matplotlib.patches as patches
from matplotlib.patches import Rectangle, Polygon
import seaborn as sns
from PIL import Image
import warnings
warnings.filterwarnings('ignore')

# 设置matplotlib中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# ========== 页面配置 ==========
st.set_page_config(
    layout="wide",
    page_title="中国古代建筑数学建模交互式平台",
    initial_sidebar_state="collapsed",
    page_icon="🏯"
)

# ========== 自定义CSS：极致视觉体验 ==========
st.markdown("""
<style>
    /* 基础样式 - 添加渐变色背景 */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main > div {
        padding: 0 2rem;
    }
    
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4, #45B7D1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient 3s ease infinite;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .sub-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: #333;
        border-left: 5px solid #8B4513;
        padding-left: 12px;
        margin: 2rem 0 1rem 0;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 0 10px 10px 0;
    }
    
    .card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 16px;
        padding: 1.8rem;
        box-shadow: 0 8px 24px rgba(0,0,0,0.12);
        margin: 0.5rem 0 1.5rem 0;
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        height: 100%;
        min-height: 220px;
    }
    
    .card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    .card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 32px rgba(0,0,0,0.2);
    }
    
    .circle-btn {
        width: 200px;
        height: 200px;
        border-radius: 50%;
        background: linear-gradient(135deg, #FF6B6B, #4ECDC4, #45B7D1);
        color: white;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        cursor: pointer;
        transition: all 0.4s ease;
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
        margin: 0 auto;
        font-weight: 600;
        font-size: 1.2rem;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    .circle-btn:hover {
        transform: scale(1.08) rotate(5deg);
        background: linear-gradient(135deg, #45B7D1, #4ECDC4, #FF6B6B);
        box-shadow: 0 15px 30px rgba(0,0,0,0.4);
    }
    
    .circle-icon {
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    
    .architecture-card {
        border-radius: 16px;
        overflow: hidden;
        transition: all 0.5s ease;
        border: 3px solid transparent;
        background: linear-gradient(135deg, #fff, #f8f9fa);
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        margin-bottom: 20px;
        cursor: pointer;
        position: relative;
        animation: fadeInUp 0.8s ease;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .architecture-card:hover {
        transform: translateY(-10px) rotate(1deg);
        border-color: #FF6B6B;
        box-shadow: 0 20px 30px rgba(0,0,0,0.25);
    }
    
    .architecture-card:active {
        transform: scale(0.98);
    }
    
    .architecture-img {
        width: 100%;
        height: 220px;
        object-fit: cover;
        transition: transform 0.6s ease;
    }
    
    .architecture-card:hover .architecture-img {
        transform: scale(1.1);
    }
    
    .architecture-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #2c3e50;
        padding: 15px 20px 10px;
        text-align: center;
        background: linear-gradient(135deg, #f8f9fa, #fff);
        position: relative;
    }
    
    .architecture-title::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 20%;
        width: 60%;
        height: 2px;
        background: linear-gradient(90deg, transparent, #FF6B6B, transparent);
    }
    
    .timeline-card {
        background: linear-gradient(135deg, #ffffff, #f8f9fa);
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        border-left: 8px solid;
        transition: all 0.4s ease;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .timeline-card::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 100px;
        height: 100px;
        background: linear-gradient(135deg, transparent, rgba(255,107,107,0.1));
        border-radius: 50%;
        transform: translate(50px, -50px);
    }
    
    .timeline-card:hover {
        transform: translateX(10px) scale(1.02);
        box-shadow: 0 15px 40px rgba(0,0,0,0.2);
    }
    
    .timeline-year {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    
    .timeline-title {
        font-size: 1.8rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 10px;
    }
    
    .timeline-desc {
        color: #666;
        line-height: 1.6;
        font-size: 1rem;
    }
    
    .timeline-badge {
        display: inline-block;
        padding: 5px 15px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border-radius: 20px;
        font-size: 0.9rem;
        margin-top: 10px;
    }
    
    .system-card {
        background: linear-gradient(135deg, #ffffff, #f8f9fa);
        border-radius: 20px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border: 2px solid transparent;
        transition: all 0.4s ease;
        cursor: pointer;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .system-card:hover {
        transform: translateY(-8px);
        border-color: #FF6B6B;
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
    }
    
    .system-icon {
        font-size: 3rem;
        margin-bottom: 15px;
    }
    
    .system-name {
        font-size: 1.4rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 10px;
    }
    
    .system-period {
        color: #FF6B6B;
        font-weight: 500;
        margin-bottom: 10px;
    }
    
    .system-desc {
        color: #666;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    .ancient-text {
        background: linear-gradient(135deg, #2c3e50, #34495e);
        color: #f1c40f;
        padding: 25px;
        border-radius: 15px;
        font-family: 'KaiTi', '楷体', serif;
        font-size: 1.2rem;
        line-height: 2;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        position: relative;
    }
    
    .ancient-text::before {
        content: '「';
        position: absolute;
        top: -10px;
        left: 10px;
        font-size: 4rem;
        color: rgba(241,196,15,0.2);
    }
    
    .ancient-text::after {
        content: '」';
        position: absolute;
        bottom: -30px;
        right: 10px;
        font-size: 4rem;
        color: rgba(241,196,15,0.2);
    }
    
    .modern-text {
        background: linear-gradient(135deg, #e3f2fd, #bbdefb);
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #2980b9;
        margin: 20px 0;
    }
    
    .graph-container {
        background: white;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: 20px 0;
    }
    
    .compare-table {
        background: white;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: 20px 0;
    }
    
    .compare-table th {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 15px;
        font-weight: 600;
    }
    
    .compare-table td {
        padding: 12px 15px;
        border-bottom: 1px solid #e0e0e0;
    }
    
    .compare-table tr:hover {
        background: #f8f9fa;
    }
    
    .detail-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 30px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        backdrop-filter: blur(10px);
        animation: slideIn 0.6s ease;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .detail-title {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 30px;
        background: linear-gradient(135deg, #8B4513, #FF6B6B);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: glow 2s ease-in-out infinite;
    }
    
    @keyframes glow {
        0%, 100% { text-shadow: 0 0 10px rgba(255,107,107,0.3); }
        50% { text-shadow: 0 0 20px rgba(255,107,107,0.6); }
    }
    
    .detail-section {
        background: linear-gradient(135deg, #f8f9fa, #ffffff);
        border-radius: 20px;
        padding: 20px;
        margin: 20px 0;
        border-left: 5px solid #4ECDC4;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    }
    
    .detail-section h3 {
        color: #2c3e50;
        margin-bottom: 15px;
        font-size: 1.5rem;
    }
    
    .detail-section p {
        color: #555;
        line-height: 1.8;
        font-size: 1.1rem;
    }
    
    .math-formula {
        background: linear-gradient(135deg, #1a2a6c, #2c3e50);
        color: white;
        padding: 20px;
        border-radius: 15px;
        font-family: 'Courier New', monospace;
        font-size: 1.2rem;
        text-align: center;
        margin: 15px 0;
    }
    
    .back-button-container {
        display: flex;
        justify-content: center;
        margin: 30px 0;
    }
    
    .custom-back-btn {
        background: linear-gradient(135deg, #8B4513, #A0522D);
        color: white;
        padding: 12px 40px;
        border-radius: 30px;
        text-align: center;
        display: inline-block;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 600;
        font-size: 1.1rem;
        border: none;
        box-shadow: 0 4px 15px rgba(139,69,19,0.3);
    }
    
    .custom-back-btn:hover {
        transform: translateX(-5px);
        box-shadow: 0 8px 25px rgba(139,69,19,0.5);
    }
    
    .intro-text {
        text-align: center;
        font-size: 1.2rem;
        color: #fff;
        margin: 2rem 0;
        padding: 2rem;
        background: linear-gradient(135deg, rgba(102,126,234,0.2), rgba(118,75,162,0.2));
        border-radius: 20px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .button-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 10px;
    }
    
    .btn-caption {
        text-align: center;
        color: #fff;
        margin-top: 10px;
        margin-bottom: 20px;
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    .decor-circle {
        position: fixed;
        width: 300px;
        height: 300px;
        border-radius: 50%;
        background: linear-gradient(135deg, rgba(102,126,234,0.1), rgba(118,75,162,0.1));
        top: -150px;
        right: -150px;
        z-index: -1;
    }
    
    .decor-square {
        position: fixed;
        width: 200px;
        height: 200px;
        background: linear-gradient(135deg, rgba(255,107,107,0.1), rgba(78,205,196,0.1));
        bottom: -100px;
        left: -100px;
        transform: rotate(45deg);
        z-index: -1;
    }
    
    .footer-text {
        text-align: center;
        margin: 3rem 0;
        color: rgba(255,255,255,0.5);
        font-size: 1rem;
    }
    
    .module-tab {
        display: flex;
        justify-content: center;
        margin: 30px 0;
        gap: 15px;
        flex-wrap: wrap;
    }
    
    .module-tab-btn {
        background: rgba(255,255,255,0.1);
        color: white;
        padding: 12px 30px;
        border-radius: 40px;
        margin: 0;
        cursor: pointer;
        transition: all 0.3s ease;
        border: 1px solid rgba(255,255,255,0.2);
        font-weight: 500;
        text-align: center;
        backdrop-filter: blur(5px);
    }
    
    .module-tab-btn:hover {
        background: rgba(255,255,255,0.2);
        transform: translateY(-3px);
        border-color: rgba(255,255,255,0.4);
    }
    
    .module-tab-btn.active {
        background: linear-gradient(135deg, #FF6B6B, #4ECDC4);
        border-color: white;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        margin-bottom: 1rem;
        border: 1px solid #e0e0e0;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #2980b9;
    }
    
    .metric-label {
        font-size: 1rem;
        color: #7f8c8d;
        margin-top: 0.5rem;
    }
    
    /* 简化版面板 - 一个白卡片即可 */
    .simple-panel {
        background: #ffffff;
        border-radius: 20px;
        padding: 20px 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        margin-bottom: 20px;
        height: fit-content;
    }
    
    .panel-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 15px;
        padding-bottom: 8px;
        border-bottom: 2px solid #4ECDC4;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .recommend-card {
        background: linear-gradient(135deg, #FF6B6B20, #4ECDC420);
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #FF6B6B;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .recommend-card strong {
        display: block;
        margin-bottom: 8px;
        font-size: 1.1rem;
    }
    
    .recommend-card p {
        margin: 0;
        line-height: 1.5;
        font-size: 0.95rem;
        color: #555;
    }
    
    .live-card {
        background: linear-gradient(135deg, #667eea20, #764ba220);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        border: 1px solid rgba(255,255,255,0.2);
        backdrop-filter: blur(5px);
    }
    
    .live-value {
        font-size: 2rem;
        font-weight: 700;
        color: #FF6B6B;
        text-align: center;
    }
    
    .live-label {
        font-size: 0.95rem;
        color: #666;
        text-align: center;
        margin-top: 5px;
        font-weight: 500;
    }
    
    .compliance-badge {
        display: inline-block;
        padding: 6px 15px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 4px 4px;
    }
    
    .compliance-pass {
        background: #d4edda;
        color: #155724;
    }
    
    .compliance-warn {
        background: #fff3cd;
        color: #856404;
    }
    
    .compliance-fail {
        background: #f8d7da;
        color: #721c24;
    }
    
    .dashboard-card {
        background: linear-gradient(135deg, #ffffff, #f8f9fa);
        border-radius: 16px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .dashboard-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #FF6B6B;
    }
    
    .dashboard-label {
        font-size: 0.9rem;
        color: #7f8c8d;
    }
    
    .insight-box {
        background: linear-gradient(135deg, #e8f4f8, #d1ecf1);
        border-radius: 12px;
        padding: 15px;
        border-left: 4px solid #17a2b8;
        margin: 10px 0;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102,126,234,0.4);
    }
</style>

<div class="decor-circle"></div>
<div class="decor-square"></div>
""", unsafe_allow_html=True)

# ========== 状态管理 ==========
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'detail' not in st.session_state:
    st.session_state.detail = None
if 'module2_system' not in st.session_state:
    st.session_state.module2_system = None
if 'module2_subpage' not in st.session_state:
    st.session_state.module2_subpage = 'timeline'
if 'module4_params' not in st.session_state:
    st.session_state.module4_params = {
        'system': '宋制·材分制',
        'grade': '三等材(廊屋)',
        'jian_shu': 3,
        'bu_jia_shu': 4,
        'ming_jian_width': 250,
        'ci_jian_width': 200,
        'bu_jia_depth': 120,
        'ju_zhe_ratio': 0.333,
        'wood_strength': 30,
        'load_factor': 5.0
    }
if 'module4_compare' not in st.session_state:
    st.session_state.module4_compare = []
if 'module4_recommendations' not in st.session_state:
    st.session_state.module4_recommendations = []
# 模块三状态
if 'module3_architecture' not in st.session_state:
    st.session_state.module3_architecture = '亭'
if 'image_analysis_result' not in st.session_state:
    st.session_state.image_analysis_result = None
# 模块二经典案例标签状态
if 'gallery_tab' not in st.session_state:
    st.session_state.gallery_tab = "殿堂建筑"

# ========== 本地图片路径配置 ==========
IMAGE_FOLDER = r"C:\Users\32404\OneDrive\桌面\计算机设计"

# 模块一图片路径映射
ARCHITECTURE_IMAGES = {
    "亭": os.path.join(IMAGE_FOLDER, "亭.png"),
    "台": os.path.join(IMAGE_FOLDER, "台.png"),
    "楼": os.path.join(IMAGE_FOLDER, "楼.png"),
    "阁": os.path.join(IMAGE_FOLDER, "阁.png"),
    "榭": os.path.join(IMAGE_FOLDER, "榭.png"),
    "舫": os.path.join(IMAGE_FOLDER, "舫.png"),
    "轩": os.path.join(IMAGE_FOLDER, "轩.png"),
    "云南民族": os.path.join(IMAGE_FOLDER, "云南民族.png"),
    # 云南民族子分类图片（6个）
    "傣族竹楼": os.path.join(IMAGE_FOLDER, "傣族竹楼.png"),
    "白族三坊一照壁": os.path.join(IMAGE_FOLDER, "白族三坊一照壁.png"),
    "彝族土掌房": os.path.join(IMAGE_FOLDER, "彝族土掌房.png"),
    "哈尼族蘑菇房": os.path.join(IMAGE_FOLDER, "哈尼族蘑菇房.png"),
    "纳西族四合院": os.path.join(IMAGE_FOLDER, "纳西族四合院.png"),
    "独龙族木楞房": os.path.join(IMAGE_FOLDER, "独龙族木楞房.png")
}

# 模块二经典案例图片映射
CASE_IMAGES = {
    "大明宫含元殿遗址": os.path.join(IMAGE_FOLDER, "大明宫含元殿遗址.png"),
    "麟德殿遗址": os.path.join(IMAGE_FOLDER, "麟德殿遗址.png"),
    "隆兴寺摩尼殿": os.path.join(IMAGE_FOLDER, "隆兴寺摩尼殿.png"),
    "玄妙观三清殿": os.path.join(IMAGE_FOLDER, "玄妙观三清殿.png"),
    "乔家大院": os.path.join(IMAGE_FOLDER, "乔家大院.png"),
    "王家大院": os.path.join(IMAGE_FOLDER, "王家大院.png"),
    "崇福寺弥陀殿": os.path.join(IMAGE_FOLDER, "崇福寺弥陀殿.png"),
    "永乐宫三清殿": os.path.join(IMAGE_FOLDER, "永乐宫三清殿.png"),
    "太庙戟门": os.path.join(IMAGE_FOLDER, "太庙戟门.png"),
    "长陵祾恩殿": os.path.join(IMAGE_FOLDER, "长陵祾恩殿.png"),
    "故宫太和殿": os.path.join(IMAGE_FOLDER, "故宫太和殿.png"),
    "颐和园": os.path.join(IMAGE_FOLDER, "颐和园.png"),
    "赵州桥": os.path.join(IMAGE_FOLDER, "赵州桥.png"),
    "布达拉宫": os.path.join(IMAGE_FOLDER, "布达拉宫.png"),
    "徽州民居": os.path.join(IMAGE_FOLDER, "徽州民居.png"),
    "北京四合院": os.path.join(IMAGE_FOLDER, "北京四合院.png"),
    "将军坟": os.path.join(IMAGE_FOLDER, "将军坟.png")
}

# ========== 云南民族民居详细数据（扩展为6个，上3下3布局）==========
YUNNAN_ETHNIC_HOUSES = {
    "傣族竹楼": {
        "img_key": "傣族竹楼",
        "full_name": "傣族·干栏式竹楼",
        "struct": "干栏式建筑，竹木结构，底层架空，上层住人。屋顶多为歇山式，坡度陡峭，利于排水。",
        "math": "柱间距2-3m，底层架空高度1.5-2m，屋顶坡度35-40°，楼面荷载2.0kN/m²",
        "history": "傣族竹楼起源于百越文化，已有数千年历史。适应西双版纳炎热潮湿的气候，底层架空防潮通风，上层居住。",
        "features": ["底层架空", "竹木结构", "歇山屋顶", "金水漏印装饰"],
        "famous": "西双版纳曼飞龙白塔周边傣寨、橄榄坝傣族园",
        "structure": "采用穿斗式木构架，柱间距2-3米。主柱6-8根，中柱承托屋脊。墙体用竹篾编织，外涂泥灰。屋顶覆盖挂瓦。",
        "culture": "竹楼体现傣族'水'文化，房屋朝向通常面向江河。金水漏印、孔雀图案装饰象征吉祥。",
        "math_detail": "数学模型：\n- 柱网：L=2-3m，柱径d=150-200mm\n- 楼面荷载：q=2.0kN/m²\n- 悬挑长度：l=0.5-0.8m\n- 屋顶坡度：i=tanθ=0.7-0.8",
        "construction": "营造要点：\n1. 木桩入土深度≥1.2m\n2. 主柱间距≤3m\n3. 竹篾墙厚30-50mm\n4. 屋面挂瓦搭接≥100mm"
    },
    "白族三坊一照壁": {
        "img_key": "白族三坊一照壁",
        "full_name": "白族·三坊一照壁",
        "struct": "四合院式布局，正房+两厢房+照壁，白墙青瓦，木雕精美。",
        "math": "正房面阔3-5间，厢房进深4-5m，庭院宽深比1:1，照壁高4-5m",
        "history": "白族建筑融合中原汉文化与大理本土文化，三坊一照壁布局始于明代，体现儒家礼制思想。",
        "features": ["三合院布局", "白墙青瓦", "水墨彩绘", "木雕精美"],
        "famous": "大理喜洲白族民居建筑群、周城",
        "structure": "抬梁式木构架，正房三间或五间，厢房两层。照壁设于正对正房处，用于遮挡和装饰。",
        "culture": "照壁彩绘'清白传家'等家训，体现白族重视教育、清白做人的价值观。",
        "math_detail": "数学模型：\n- 正房面阔B=3-5间，每间3-4m\n- 庭院S=2B×2D\n- 照壁高H=4-5m，宽W=B×0.8\n- 屋顶坡度i=0.25-0.3",
        "construction": "营造要点：\n1. 木柱径250-300mm\n2. 斗拱出踩3-5踩\n3. 瓦屋面坡度25°\n4. 木雕装饰面积≥15%"
    },
    "彝族土掌房": {
        "img_key": "彝族土掌房",
        "full_name": "彝族·土掌房",
        "struct": "平顶厚墙土坯房，层层叠落，晒台相连。墙体收分明显，隔热蓄水。",
        "math": "墙体收分比1:20，墙厚400-600mm，平顶坡度1:15，蓄水层厚度100mm",
        "history": "彝族土掌房源于古羌人建筑传统，适应山区气候。平顶可用于晾晒粮食，墙体厚实保温隔热。",
        "features": ["平顶晒台", "厚墙收分", "土坯砌筑", "层层叠落"],
        "famous": "楚雄彝族自治州彝族村落、城子古村",
        "structure": "夯土墙或土坯砌筑，墙体下宽上窄收分明显。木梁檩条承托平顶屋面，上铺松木、树枝、泥土。",
        "culture": "土掌房层层叠落的形态如同梯田，体现彝族与山地共生的智慧。",
        "math_detail": "数学模型：\n- 墙体收分k=1/20\n- 土坯尺寸：400×200×100mm\n- 平顶荷载：q=3.0kN/m²\n- 蓄水层厚度t=0.1m",
        "construction": "营造要点：\n1. 基础深500mm\n2. 墙体分层夯实\n3. 梁檩间距500-600mm\n4. 屋面铺土厚度200mm"
    },
    "哈尼族蘑菇房": {
        "img_key": "哈尼族蘑菇房",
        "full_name": "哈尼族·蘑菇房",
        "struct": "土墙茅草顶，形似蘑菇。二层架空，下层关牲畜，上层住人。",
        "math": "土墙厚400mm，草顶悬挑0.5-0.8m，屋顶坡度45-50°",
        "history": "哈尼族蘑菇房是哀牢山区最具特色的民居形式，与梯田文化共同构成哈尼族的文化符号。",
        "features": ["蘑菇形草顶", "土坯墙", "二层居住", "冬暖夏凉"],
        "famous": "元阳哈尼梯田景区、阿者科村",
        "structure": "土坯墙承重，木构架支撑屋顶。草顶用山草覆盖，厚200-300mm。二层设火塘，是家庭活动中心。",
        "culture": "蘑菇房与梯田相映成趣，是哈尼族'森林-村寨-梯田-水系'四素同构文化的载体。",
        "math_detail": "数学模型：\n- 草顶悬挑l=0.5-0.8m\n- 火塘位置居中\n- 通风口面积=0.5-1m²\n- 室内热环境：夏季降温3-5℃，冬季保温",
        "construction": "营造要点：\n1. 土墙收分1/15\n2. 山草铺设厚度≥200mm\n3. 火塘设于二层中心\n4. 预留排烟口"
    },
    "纳西族四合院": {
        "img_key": "纳西族四合院",
        "full_name": "纳西族·四合院",
        "struct": "四合五天井，走马转角楼。木雕精美，融合汉藏白建筑风格。",
        "math": "院落宽深比3:2，天井面积15-25m²，木雕覆盖率20%",
        "history": "纳西族四合院是丽江古城的主体建筑形式，融合了中原、藏族、白族的建筑精华。",
        "features": ["四合五天井", "走马楼", "悬鱼博风", "木雕精美"],
        "famous": "丽江古城、束河古镇",
        "structure": "抬梁式木构架，二层设回廊连通。门窗雕刻精美，悬鱼博风装饰丰富。",
        "culture": "纳西族建筑体现'天人合一'理念，庭院中常种植花草、设水景，营造宜居环境。",
        "math_detail": "数学模型：\n- 院落面积S=L×W=200-300m²\n- 天井占比15-20%\n- 回廊宽度1.2-1.5m\n- 木雕构件强度折减系数0.85",
        "construction": "营造要点：\n1. 柱网间距3-4m\n2. 二层回廊连通\n3. 悬鱼长度0.8-1.2m\n4. 木雕采用透雕工艺"
    },
    "独龙族木楞房": {
        "img_key": "独龙族木楞房",
        "full_name": "独龙族·木楞房",
        "struct": "井干式木楞房，圆木叠垒，结构稳固，保暖防潮。屋顶为双坡悬山顶。",
        "math": "圆木直径200-250mm，墙体收分1:30，屋顶坡度35°，抗震性能优良",
        "history": "独龙族是中国人口最少的民族之一，主要聚居在独龙江峡谷。木楞房是独龙族传统民居，适应高寒山区气候。",
        "features": ["井干结构", "圆木叠垒", "双坡屋顶", "古朴自然"],
        "famous": "贡山独龙族怒族自治县独龙江乡",
        "structure": "井干式木构架，圆木两端开槽咬合，层层叠垒形成墙体。屋顶覆盖木板或瓦片，室内设火塘。",
        "culture": "木楞房体现独龙族与自然和谐共生的智慧，是独龙族文化的物质载体。",
        "math_detail": "数学模型：\n- 圆木直径d=200-250mm\n- 墙体收分k=1/30\n- 屋顶坡度i=0.7\n- 抗震验算：榫卯节点刚度K=EI/L\n- 保温性能：墙体传热系数U=0.8W/(m²·K)",
        "construction": "营造要点：\n1. 圆木去皮干燥\n2. 两端开燕尾槽\n3. 墙体咬合严密\n4. 火塘居中设排烟口"
    }
}

# ========== 传统民居数据库 ==========
TRADITIONAL_HOUSES = {
    "北京四合院": {
        "dynasty": "元-清",
        "region": "北京",
        "desc": "北方合院式民居的代表，布局严谨，中轴对称，体现了封建社会的等级制度和家族观念。",
        "features": ["中轴对称", "内外有别", "青砖灰瓦", "影壁垂花门"],
        "image": CASE_IMAGES["北京四合院"]
    },
    "徽州民居": {
        "dynasty": "明-清",
        "region": "安徽徽州",
        "desc": "粉墙黛瓦马头墙，天井采光四水归堂。木雕、砖雕、石雕并称'徽州三雕'。",
        "features": ["粉墙黛瓦", "马头墙", "天井采光", "徽州三雕"],
        "image": CASE_IMAGES["徽州民居"]
    },
    "乔家大院": {
        "dynasty": "清",
        "region": "山西祁县",
        "desc": "晋商大院的杰出代表，城堡式建筑群，'在中堂'是乔家大院的核心建筑。",
        "features": ["城堡式布局", "晋商风格", "砖雕精美", "规模宏大"],
        "image": CASE_IMAGES["乔家大院"]
    },
    "王家大院": {
        "dynasty": "明-清",
        "region": "山西灵石",
        "desc": "'王家归来不看院'，五巷六堡一条街，总面积25万平方米，是中国最大的民居建筑群。",
        "features": ["规模最大", "依山而建", "三雕俱全", "官宅特色"],
        "image": CASE_IMAGES["王家大院"]
    }
}

# ========== 中国桥梁数据库 ==========
CHINESE_BRIDGES = {
    "赵州桥": {
        "dynasty": "隋代",
        "location": "河北赵县",
        "desc": "世界上现存最古老的石拱桥，由李春设计建造。采用敞肩拱结构，开创了桥梁建筑的新纪元。",
        "features": ["敞肩拱", "单孔石桥", "雕刻精美", "1400年历史"],
        "image": CASE_IMAGES["赵州桥"]
    },
    "卢沟桥": {
        "dynasty": "金代",
        "location": "北京",
        "desc": "北京现存最古老的石造联拱桥，桥上501只石狮形态各异，'卢沟晓月'为燕京八景之一。",
        "features": ["联拱石桥", "石狮雕刻", "历史见证", "交通要道"],
        "image": "https://images.unsplash.com/photo-1590845947674-f6e8b9f8a4e8?w=800"
    },
    "洛阳桥": {
        "dynasty": "北宋",
        "location": "福建泉州",
        "desc": "中国现存最早的跨海石桥，首创'筏形基础'和'种蛎固基'的造桥技术。",
        "features": ["跨海石桥", "筏形基础", "种蛎固基", "北宋遗构"],
        "image": "https://images.unsplash.com/photo-1590845947674-f6e8b9f8a4e8?w=800"
    },
    "广济桥": {
        "dynasty": "南宋",
        "location": "广东潮州",
        "desc": "中国四大古桥之一，集梁桥、浮桥、拱桥于一体，'十八梭船廿四洲'的独特格局。",
        "features": ["梁浮结合", "启闭式", "潮州八景", "独特格局"],
        "image": "https://images.unsplash.com/photo-1590845947674-f6e8b9f8a4e8?w=800"
    }
}

# ========== 官府与皇宫建筑数据库 ==========
IMPERIAL_PALACES = {
    "故宫太和殿": {
        "dynasty": "清代",
        "location": "北京",
        "desc": "明清两代皇帝举行大典的场所，是中国现存最大的木构殿宇，面阔十一间，重檐庑殿顶。",
        "features": ["最高等级", "十一开间", "重檐庑殿", "金砖墁地"],
        "image": CASE_IMAGES["故宫太和殿"]
    },
    "大明宫含元殿": {
        "dynasty": "唐代",
        "location": "陕西西安",
        "desc": "唐代大明宫正殿，龙尾道、翔鸾阁、栖凤阁组成'凹'字形平面，体现大唐威仪。",
        "features": ["唐代最高规制", "凹字形平面", "龙尾道", "气势恢宏"],
        "image": CASE_IMAGES["大明宫含元殿遗址"]
    },
    "长陵祾恩殿": {
        "dynasty": "明代",
        "location": "北京",
        "desc": "明十三陵中朱棣的陵寝大殿，殿内60根金丝楠木巨柱，是中国现存最大的楠木殿。",
        "features": ["楠木巨柱", "明代官式", "陵寝建筑", "保存完好"],
        "image": CASE_IMAGES["长陵祾恩殿"]
    },
    "太庙戟门": {
        "dynasty": "明代",
        "location": "北京",
        "desc": "明清两代皇帝祭祀祖先的场所，建筑规制严谨，是研究明代官式建筑的典范。",
        "features": ["规制严谨", "官式典范", "祭祀建筑", "明代遗构"],
        "image": CASE_IMAGES["太庙戟门"]
    }
}

# ========== 模数体系数据 ==========
SYSTEMS = {
    "宋制·材分制": {
        "scale": {
            "一等材(大殿)": 6 * 31.2,
            "二等材(厅堂)": 5.5 * 31.2,
            "三等材(廊屋)": 5 * 31.2,
            "四等材(小殿)": 4.8 * 31.2,
            "五等材(小厅堂)": 4.4 * 31.2,
            "六等材(亭榭)": 4 * 31.2,
            "七等材(小亭)": 3.6 * 31.2,
            "八等材(井亭)": 3 * 31.2,
        },
        "unit": "分°",
        "base_unit": lambda grade: SYSTEMS["宋制·材分制"]["scale"][grade] / 15,
        "color": "#8B4513",
        "rules": {
            "min_jian_shu": 1,
            "max_jian_shu": 11,
            "min_bu_jia": 2,
            "max_bu_jia": 8,
            "ming_jian_range": [200, 350],
            "ci_jian_range": [150, 300],
            "bu_jia_range": [100, 200],
            "ju_zhe_range": [0.25, 0.4]
        }
    },
    "清制·斗口制": {
        "scale": {
            "一寸斗口(大殿)": 1 * 32,
            "0.9寸斗口(次殿)": 0.9 * 32,
            "0.8寸斗口(厅堂)": 0.8 * 32,
            "0.7寸斗口(配殿)": 0.7 * 32,
            "0.6寸斗口(亭台)": 0.6 * 32,
            "0.5寸斗口(廊屋)": 0.5 * 32,
            "0.4寸斗口(杂屋)": 0.4 * 32,
        },
        "unit": "斗口",
        "base_unit": lambda grade: SYSTEMS["清制·斗口制"]["scale"][grade],
        "color": "#2980b9",
        "rules": {
            "min_jian_shu": 1,
            "max_jian_shu": 11,
            "min_bu_jia": 2,
            "max_bu_jia": 8,
            "ming_jian_range": [200, 400],
            "ci_jian_range": [150, 350],
            "bu_jia_range": [100, 200],
            "ju_zhe_range": [0.25, 0.4]
        }
    },
    "唐制·大木作": {
        "scale": {
            "殿身材(一等)": 9.0 * 30.0,
            "殿身材(二等)": 8.5 * 30.0,
            "厅堂材(一等)": 7.5 * 30.0,
            "厅堂材(二等)": 7.0 * 30.0,
            "余屋材(一等)": 6.0 * 30.0,
            "余屋材(二等)": 5.5 * 30.0,
        },
        "unit": "分",
        "base_unit": lambda grade: SYSTEMS["唐制·大木作"]["scale"][grade] / 15,
        "color": "#e74c3c",
        "rules": {
            "min_jian_shu": 1,
            "max_jian_shu": 11,
            "min_bu_jia": 2,
            "max_bu_jia": 8,
            "ming_jian_range": [250, 400],
            "ci_jian_range": [200, 350],
            "bu_jia_range": [120, 220],
            "ju_zhe_range": [0.25, 0.4]
        }
    },
    "明制·官式": {
        "scale": {
            "一等(大殿)": 8.0 * 31.8,
            "二等(次殿)": 7.0 * 31.8,
            "三等(厅堂)": 6.0 * 31.8,
            "四等(配殿)": 5.0 * 31.8,
            "五等(廊屋)": 4.0 * 31.8,
        },
        "unit": "寸",
        "base_unit": lambda grade: SYSTEMS["明制·官式"]["scale"][grade] / 10,
        "color": "#f39c12",
        "rules": {
            "min_jian_shu": 1,
            "max_jian_shu": 11,
            "min_bu_jia": 2,
            "max_bu_jia": 8,
            "ming_jian_range": [220, 380],
            "ci_jian_range": [180, 320],
            "bu_jia_range": [110, 210],
            "ju_zhe_range": [0.25, 0.4]
        }
    }
}

# ========== 亭台楼阁榭舫轩详细数据 ==========
ARCHITECTURES = {
    "亭": {
        "img_path": ARCHITECTURE_IMAGES["亭"],
        "struct": "开敞式结构，攒尖顶，无墙体，柱网对称，多采用六角或八角形平面",
        "math": "正多边形对称，屋顶斜率 1:2.5，柱高与柱径比 10:1",
        "history": "历史渊源：亭最早出现于商周时期，最初为驿站建筑，供行人休息。发展于秦汉，鼎盛于明清。既是休憩之所，也是园林点景的重要元素。",
        "types": "主要类型：有圆亭、方亭、六角亭、八角亭、重檐亭、流杯亭等多种形式。",
        "famous": "著名实例：醉翁亭（安徽滁州）、陶然亭（北京）、爱晚亭（湖南长沙）、湖心亭（浙江杭州）并称中国四大名亭。",
        "structure": "结构特点：由台基、柱身、屋顶三部分组成。柱网对称布置，屋顶多为攒尖顶，有单檐、重檐之分。亭的梁架常采用抹角梁或井字梁，形成独特的结构体系。",
        "culture": "文化内涵：亭不仅是建筑，更是文人雅集、诗词唱和的文化载体。王羲之《兰亭集序》、欧阳修《醉翁亭记》等千古名篇皆以亭为题。",
        "math_detail": "数学模型：\n- 圆亭：C=2πr，S=πr²\n- 方亭：S=a²\n- 六角亭：内切圆半径r，边长a=r/√3，面积S=2.598a²\n- 八角亭：内切圆半径r，边长a=0.828r，面积S=4.828a²",
        "construction": "营造要点：\n1. 柱高不超过3米，柱径200-300mm\n2. 举高为步架总深的1/3\n3. 攒尖顶坡度30-35度\n4. 翼角起翘高度为檐口高度的1/10"
    },
    "台": {
        "img_path": ARCHITECTURE_IMAGES["台"],
        "struct": "高台建筑，逐层收分，台上建屋，设有台阶和栏杆，兼具观演与祭祀功能",
        "math": "收分率 1/10，台阶坡度 30度，台基高宽比 1:2，每层设须弥座",
        "history": "历史渊源：台起源于商周时期，早期用于观天象、祭祀。春秋战国时期，各国竞相筑台，如楚灵王章华台、吴王夫差姑苏台。汉代以后发展为礼制建筑，用于祭天、观演。",
        "types": "主要类型：有观景台、点将台、祭台、舞台、钓鱼台等，以戏台最为常见。",
        "famous": "著名实例：铜雀台（河北临漳）、古琴台（湖北武汉）、钓鱼台（北京）、越王台（浙江绍兴）。",
        "structure": "结构特点：台基分层收分，一般每层收分1/10，呈梯形断面。台基内部可夯土或砌筑，表面包砌砖石。台上建筑多为木构殿堂，设台阶和栏杆。戏台则设前后台、屏风、出将入相门等。",
        "culture": "文化内涵：台是权力与地位的象征。曹操筑铜雀台以彰显武功，李白有“东风不与周郎便，铜雀春深锁二乔”的咏叹。戏台则是民间文化的中心。",
        "math_detail": "数学模型：\n- 收分率k=1/10，第n层宽度Wn=W0*(1-k)^n\n- 台阶高度h=150mm，水平投影l=300mm，坡度角θ=arctan(h/l)=26.6°\n- 台基稳定系数：K = (B/2) / (H * tan(φ))，其中B为基底宽，H为台高，φ为土体内摩擦角\n- 须弥座比例：上枋:束腰:下枋 = 1:2:1",
        "construction": "营造要点：\n1. 台基高度3-9米，分层夯实\n2. 每层收分100-200mm\n3. 台阶每级高150mm，宽300mm，设垂带石\n4. 台面设排水坡度3-5%，周围设栏杆望柱\n5. 戏台设前后台分隔，屏风彩绘，出将入相门"
    },
    "楼": {
        "img_path": ARCHITECTURE_IMAGES["楼"],
        "struct": "多层木结构建筑，矩形平面，内置楼梯，各层设回廊",
        "math": "层高 3.3~3.6m，面阔进深比 3:2，柱径与柱高比 1:10",
        "history": "历史渊源：楼的出现晚于阁，汉代开始流行，唐代达到鼎盛。初为军事瞭望之用，后多用于居住、观景、藏书。",
        "types": "主要类型：有城楼、钟鼓楼、藏书楼、酒楼、观景楼、戏楼等。",
        "famous": "著名实例：黄鹤楼（湖北武汉）、岳阳楼（湖南岳阳）、滕王阁（江西南昌）、鹳雀楼（山西永济）并称中国四大名楼。",
        "structure": "结构特点：多为二层以上，采用抬梁式木构架。楼层间有楼梯相连，檐口出挑深远。各层设平座栏杆，可供登临观景。",
        "culture": "文化内涵：楼是文人登高望远、赋诗抒怀的场所。王之涣“欲穷千里目，更上一层楼”、崔颢“昔人已乘黄鹤去”等名句流传千古。",
        "math_detail": "数学模型：\n- 层高h=3.3-3.6m，面阔B，进深D，比例B:D=3:2\n- 斗拱出挑L=0.3-0.5D\n- 结构周期T=0.05H^(3/4)（H为总高）\n- 风荷载W=0.5ρv²CdA，其中ρ空气密度，v风速，Cd体型系数",
        "construction": "营造要点：\n1. 底层柱径300-400mm，上层柱径递减\n2. 每层设暗层加强整体性\n3. 楼梯坡度45度，每步高180mm\n4. 檐口出挑1.2-1.5m"
    },
    "阁": {
        "img_path": ARCHITECTURE_IMAGES["阁"],
        "struct": "重檐建筑，斗拱繁复，多用于藏书、供佛、观景",
        "math": "斗口制模数，举折1/3进深，暗层与明层高比2:3",
        "history": "历史渊源：阁最初指架空的栈道，后演变为多层建筑。汉代已有藏书阁，魏晋时期出现佛阁，唐宋时期阁成为重要建筑类型。",
        "types": "主要类型：有藏书阁、佛阁、文昌阁、观音阁、魁星阁等。",
        "famous": "著名实例：天一阁（浙江宁波）、文渊阁（北京故宫）、佛香阁（北京颐和园）、大悲阁（河北正定）。",
        "structure": "结构特点：平面多为方形或六角形，采用平座暗层结构，外观多为二层，实有三层。暗层结构加强整体刚度，明层用于使用功能。",
        "culture": "文化内涵：阁是文化传承的象征。宁波天一阁是中国现存最早的私家藏书楼，范钦“代不分书”的祖训使古籍得以保存。",
        "math_detail": "数学模型：\n- 暗层高h1，明层高h2，h1:h2=2:3\n- 出檐深度E=0.3-0.4H，H为层高\n- 屋顶举高Hr=1/3D，D为进深\n- 斗拱承载力P=n×A×σ，n斗拱朵数，A受力面积，σ木材强度",
        "construction": "营造要点：\n1. 暗层高2.2-2.5m，明层高3.3-3.6m\n2. 斗拱出踩3-5踩\n3. 平座挑出1.2-1.8m\n4. 屋顶采用歇山或攒尖形式"
    },
    "榭": {
        "img_path": ARCHITECTURE_IMAGES["榭"],
        "struct": "临水建筑，一半在岸一半在水，四面通透开敞",
        "math": "悬挑比1:2，桩基入土深度≥2倍悬挑长度，三角形稳定结构",
        "history": "历史渊源：榭最早指高台上的木构建筑，《尔雅》有“阁谓之台，有木者谓之榭”的记载。宋代以后特指临水建筑，成为园林标配。",
        "types": "主要类型：有水榭、花榭、舞榭等，以水榭最为常见。水榭又分单面水榭和双面水榭。",
        "famous": "著名实例：苏州拙政园远香堂、北京颐和园鱼藻轩、上海豫园水榭。",
        "structure": "结构特点：一半建在岸上，一半伸入水中。采用悬挑结构或桩基础，平台临水一面设美人靠，便于凭栏观鱼。屋顶多为卷棚歇山。",
        "culture": "文化内涵：榭是园林中观鱼赏荷的最佳处所，体现“天人合一”的造园理念。庄子与惠子“濠梁观鱼”的典故，赋予水榭哲学意味。",
        "math_detail": "数学模型：\n- 悬挑L1，岸上L2，L1:L2=1:2\n- 桩基深度H≥2L1，桩径d≥L1/15\n- 悬挑梁弯矩M=qL1²/2，q为均布荷载\n- 平台面积S=(L1+L2)×W，W为面宽\n- 稳定验算：抗倾覆系数K=G×L2/(q×L1²/2)≥1.5",
        "construction": "营造要点：\n1. 悬挑不超过3m\n2. 木桩直径150-200mm，间距1.2-1.5m\n3. 平台铺设厚40-50mm防腐木\n4. 设美人靠高450mm，倾角15度"
    },
    "舫": {
        "img_path": ARCHITECTURE_IMAGES["舫"],
        "struct": "仿船形建筑，石砌船身，木构舱楼，固定不系舟",
        "math": "长宽比5:1，头舱:中舱:尾舱=1:2:1，视觉浮力平衡",
        "history": "历史渊源：舫源于江南水乡的船形建筑，又称“不系舟”。明清园林中大量出现，象征自由超脱的人生境界。",
        "types": "主要类型：有石舫、木舫、画舫。石舫以北京颐和园清晏舫最为著名，木舫多见于江南私家园林。",
        "famous": "著名实例：北京颐和园清晏舫、苏州狮子林石舫、南京瞻园石舫。",
        "structure": "结构特点：分为头舱、中舱、尾舱三段。船头有跳板，船尾有舵楼。船身多用青石砌筑，舱楼为木构，设轩棚式屋顶。",
        "culture": "文化内涵：舫象征“人生在世不称意，明朝散发弄扁舟”的隐逸思想。乾隆皇帝诗云：“临水常看不系舟，舟人已自识归休。”",
        "math_detail": "数学模型：\n- 总长L，宽W，L:W=5:1\n- 头舱长L1=0.25L，中舱L2=0.5L，尾舱L3=0.25L\n- 船身排水体积V=W×H×L×0.6（H为吃水深度）\n- 浮力F=ρgV，需等于总重量G\n- 稳心高度GM=KB+BM-KG，要求GM>0.5m",
        "construction": "营造要点：\n1. 船身石砌厚300-400mm\n2. 舱高2.8-3.2m\n3. 船头翘起高度300-500mm\n4. 设石栏板高900-1100mm"
    },
    "轩": {
        "img_path": ARCHITECTURE_IMAGES["轩"],
        "struct": "小巧高敞的建筑，前檐完全敞开，设轩梁和美人靠",
        "math": "檐高与进深比2:3，轩梁圆弧半径R，矢高f=R-√(R²-(D/2)²)",
        "history": "历史渊源：轩原指有窗的长廊，后演变为小巧雅致的建筑。明代江南文人园林中大量出现，多用于书房、茶室、琴室。",
        "types": "主要类型：有敞轩、半轩、曲尺轩、船篷轩、鹤胫轩等，以敞轩最为常见。",
        "famous": "著名实例：苏州留园五峰仙馆、北京恭王府邀月轩、扬州个园宜雨轩。",
        "structure": "结构特点：前檐完全敞开，不设门窗。梁架常做成轩梁形式，形成优美的弧形天花板。设美人靠供休憩，轩内可置琴棋书画。",
        "culture": "文化内涵：轩是文人雅集的私密空间，追求“轩窗敞启，听松涛鸟语”的清雅意境。郑板桥曾在轩中画竹题诗：“衙斋卧听萧萧竹，疑是民间疾苦声。”",
        "math_detail": "数学模型：\n- 檐高H，进深D，H:D=2:3\n- 轩梁半径R，矢高f，满足f=R-√(R²-(D/2)²)\n- 轩梁弯矩M=qD²/8，q为均布荷载\n- 梁截面应力σ=M/W≤[σ]，W为截面模量\n- 轩梁挠度δ=5qD⁴/(384EI)≤D/250",
        "construction": "营造要点：\n1. 檐高3-3.6m，进深4.5-5.4m\n2. 轩梁截面高300-400mm\n3. 轩椽间距400-500mm\n4. 美人靠高450mm，倾角20度"
    },
    "云南民族": {
        "img_path": ARCHITECTURE_IMAGES["云南民族"],
        "struct": "融合汉、藏、傣、白等民族特色，干栏式、土掌房、三坊一照壁等多种形式并存",
        "math": "干栏式柱网间距2-3m，土掌房收分比1:20，三坊一照壁面阔进深比3:2",
        "history": "历史渊源：云南地处中国西南，多民族聚居，建筑形态多样。傣族干栏式建筑源自百越文化，彝族土掌房体现山地智慧，白族三坊一照壁融合中原礼制。",
        "types": "主要类型：傣族干栏式竹楼、彝族土掌房、白族三坊一照壁、哈尼族蘑菇房、纳西族四合院、独龙族木楞房等。",
        "famous": "著名实例：西双版纳曼飞龙白塔、大理喜洲白族民居、丽江古城纳西民居、元阳哈尼族蘑菇房。",
        "structure": "结构特点：干栏式建筑以木柱架空，防潮通风；土掌房平顶厚墙，隔热蓄水；三坊一照壁采用木构架，庭院布局严谨，白墙青瓦。",
        "culture": "文化内涵：云南民族建筑是人与自然和谐共生的典范。傣族竹楼“宁可食无肉，不可居无竹”；白族照壁“清白传家”；彝族土掌房层层叠叠，展现山地聚落之美。",
        "math_detail": "数学模型：\n- 干栏式：柱高H=2.2-2.8m，柱间距L=2-3m，楼面荷载q=2.0kN/m²\n- 土掌房：墙体收分k=1/20，屋顶坡度i=1:15，蓄水层厚度t=0.1m\n- 三坊一照壁：正房面阔B，厢房进深D，B:D=3:2，庭院面积S=2B×2D\n- 结构抗震：木构架榫卯节点刚度K=EI/L，阻尼比ξ=0.05",
        "construction": "营造要点：\n1. 干栏式：木桩入土深度≥1.2m，穿斗式构架，竹篾墙\n2. 土掌房：土坯墙厚400-600mm，松木梁檩，草泥屋面\n3. 三坊一照壁：木雕精美，照壁高4-5m，瓦屋面坡度25°\n4. 装饰：彩绘、木雕、石雕，融合佛教、道教、本主信仰图案"
    }
}

# ========== 12种营造体系详细数据 ==========
BUILDING_SYSTEMS = {
    "唐制·大木作": {
        "year": "618-907年",
        "dynasty": "唐代",
        "color": "#e74c3c",
        "icon": "🏯",
        "source": "《唐六典》《营缮令》",
        "author": "李林甫等",
        "ancient": "凡构屋之制，皆以材为祖。材分三等，殿用九分，堂用七分，余屋用六分。柱高以材为率，殿柱高十五材，堂柱高十二材。",
        "modern": "唐代建筑以“材”为基本模数，材分为三个等级。殿身用一等材（9分°），厅堂用二等材（7分°），余屋用三等材（6分°）。柱高为材高的倍数，殿柱高15材，堂柱高12材。这种模数体系体现了唐代建筑的恢宏气势和严谨规制。",
        "features": ["用材硕大", "斗拱雄健", "出檐深远", "气势恢宏"],
        "example": "大明宫含元殿遗址、麟德殿遗址",
        "image": CASE_IMAGES["大明宫含元殿遗址"],
        "modules": {
            "材等": {"一等": 270, "二等": 225, "三等": 180},
            "比例": "1材=15分°",
            "柱高": "殿柱15材，堂柱12材"
        }
    },
    "宋制·材分制": {
        "year": "1103年",
        "dynasty": "北宋",
        "color": "#8B4513",
        "icon": "📜",
        "source": "《营造法式》",
        "author": "李诫",
        "ancient": "凡构屋之制，皆以材为祖。材分八等，度屋之大小，因而用之。各以其材之广，分为十五分，以十分为其厚。凡屋宇之高深，名物之短长，曲直举折之势，皆以所用材之分，以为制度焉。",
        "modern": "宋代《营造法式》确立了完整的材分制体系。以“材”为基本模数，将材分为八个等级，适应不同规模的建筑。每材的高度分为15分°，厚度为10分°。所有构件尺寸、屋顶举折等都以分°为单位计算，形成了中国最早的建筑模数化标准。",
        "features": ["材分八等", "比例严谨", "模数化强", "体系完整"],
        "example": "隆兴寺摩尼殿、玄妙观三清殿",
        "image": CASE_IMAGES["隆兴寺摩尼殿"],
        "modules": {
            "材等": {"一等": 187.2, "二等": 171.6, "三等": 156.0, "四等": 149.8},
            "比例": "1材=15分°，1栔=6分°",
            "柱高": "檐柱高=6材，柱径=2材"
        }
    },
    "辽制·大木作": {
        "year": "907-1125年",
        "dynasty": "辽代",
        "color": "#d35400",
        "icon": "🏛️",
        "source": "《辽史·营卫志》",
        "author": "脱脱等",
        "ancient": "辽承唐制，材分五等，殿身用大材，柱高十五材。斗拱雄大，出檐深远，多用斜拱。",
        "modern": "辽代建筑继承唐代风格，用材更为硕大，结构雄健。斗拱尺度宏大，常采用斜拱等特殊形式。柱高一般为15材，体现了辽代建筑的豪放风格。",
        "features": ["用材硕大", "斗拱雄健", "斜拱特色", "结构稳定"],
        "example": "奉国寺大殿",
        "image": "https://images.unsplash.com/photo-1590845947674-f6e8b9f8a4e8?w=800",
        "modules": {
            "材等": {"殿身一等": 280, "殿身二等": 250, "厅堂": 220},
            "比例": "1材=15分°",
            "柱高": "殿柱15材，斜拱角度30°"
        }
    },
    "金制·大木作": {
        "year": "1115-1234年",
        "dynasty": "金代",
        "color": "#c0392b",
        "icon": "🏰",
        "source": "《金史·礼志》",
        "author": "脱脱等",
        "ancient": "金承宋辽，材分五等，用材精炼。减柱造、移柱造盛行，室内空间开阔。",
        "modern": "金代建筑融合宋辽特点，结构精巧，装饰华丽。首创减柱造和移柱造，通过减少或移动柱子，获得更开阔的室内空间。",
        "features": ["减柱移柱", "空间开阔", "装饰华丽", "结构创新"],
        "example": "崇福寺弥陀殿、善化寺大殿",
        "image": CASE_IMAGES["崇福寺弥陀殿"],
        "modules": {
            "材等": {"殿身一等": 260, "殿身二等": 235, "厅堂": 210},
            "比例": "减柱率30-50%",
            "柱高": "殿柱12材，跨度增大"
        }
    },
    "元制·官式大木": {
        "year": "1271-1368年",
        "dynasty": "元代",
        "color": "#27ae60",
        "icon": "⛩️",
        "source": "《元内府营造法式》",
        "author": "官修",
        "ancient": "大木之制，材分三等，殿用大材，堂用中材，余屋用小材。柱高以材高为率，殿柱高六材，堂柱高五材。",
        "modern": "元代简化材等，用材等级减少，施工效率提高。柱高相对降低，建筑风格趋向简洁。永乐宫三清殿是元代官式建筑的典范。",
        "features": ["材等简化", "施工高效", "风格简洁", "实用性强"],
        "example": "永乐宫三清殿、北岳庙德宁殿",
        "image": CASE_IMAGES["永乐宫三清殿"],
        "modules": {
            "材等": {"大材": 226.8, "中材": 189, "小材": 151.2},
            "比例": "殿柱高6材",
            "柱高": "较宋代降低20%"
        }
    },
    "明制·官式": {
        "year": "1368-1644年",
        "dynasty": "明代",
        "color": "#f39c12",
        "icon": "🏯",
        "source": "《明宫史》《工部厂库须知》",
        "author": "刘若愚等",
        "ancient": "凡宫殿之制，皆以斗口为度，斗口一寸，柱高十丈。梁枋之制，皆以斗口倍数定之，额枋高六斗口，平板枋高二斗口。",
        "modern": "明代建筑承上启下，既保留材分制的比例美学，又发展出斗口制。模数体系更加标准化，施工精度提高。太庙、长陵等明代建筑体现了严谨的规制和雄伟的气魄。",
        "features": ["承上启下", "规制严谨", "标准化高", "气势雄伟"],
        "example": "太庙戟门、长陵祾恩殿",
        "image": CASE_IMAGES["太庙戟门"],
        "modules": {
            "斗口": {"一等": 31.8, "二等": 31.8, "三等": 31.8},
            "比例": "1斗口=1寸",
            "柱高": "檐柱高=10斗口"
        }
    },
    "清制·斗口制": {
        "year": "1734年",
        "dynasty": "清代",
        "color": "#2980b9",
        "icon": "🏰",
        "source": "《工程做法则例》",
        "author": "允禄等",
        "ancient": "凡斗口有头等料，自一寸至二寸五分，每等五分递加，共分十一等。凡檐柱，以斗口定高，每斗口高一丈，径一尺。",
        "modern": "清代《工程做法则例》确立斗口制为官式建筑标准。斗口分为十一等，所有构件尺寸均为斗口的倍数。这种高度标准化的模数体系，实现了构件的预制化生产，大大提高了施工效率。",
        "features": ["十一等斗口", "高度标准化", "预制化强", "施工高效"],
        "example": "故宫太和殿、颐和园",
        "image": CASE_IMAGES["故宫太和殿"],
        "modules": {
            "斗口": {"一寸": 32, "0.8寸": 25.6, "0.6寸": 19.2},
            "比例": "檐柱径=6斗口",
            "柱高": "檐柱高=10斗口"
        }
    },
    "西夏·官式": {
        "year": "1038-1227年",
        "dynasty": "西夏",
        "color": "#9b59b6",
        "icon": "🛕",
        "source": "《天盛改旧新定律令》",
        "author": "官修",
        "ancient": "凡营造之制，材分二等，殿用大材，堂用小材。柱高以材高为率，殿柱高八材，堂柱高六材。",
        "modern": "西夏建筑融合汉藏文化，用材简练，结构雄健。建筑风格独特，体现了西夏建筑独特的艺术风格。",
        "features": ["汉藏融合", "用材简练", "建筑独特", "地域特色"],
        "example": "西夏王陵",
        "image": "https://images.unsplash.com/photo-1590845947674-f6e8b9f8a4e8?w=800",
        "modules": {
            "材等": {"殿材": 152.5, "堂材": 122},
            "比例": "殿柱高8材"
        }
    },
    "藏式·大木": {
        "year": "唐-清",
        "dynasty": "西藏",
        "color": "#34495e",
        "icon": "⛰️",
        "source": "《西藏营造法式》",
        "author": "藏族工匠",
        "ancient": "凡殿堂之制，以柱径为度，柱径一尺，梁高八尺。梁枋之制，皆以柱径倍数定之，额枋高四柱径，平板枋高一柱径。",
        "modern": "藏式建筑以柱径为基本模数，梁枋尺寸均为柱径的倍数。建筑依山而建，色彩艳丽，融合了藏、汉等多种建筑风格。布达拉宫是藏式建筑的杰出代表。",
        "features": ["柱径模数", "依山而建", "色彩艳丽", "多元融合"],
        "example": "布达拉宫、大昭寺",
        "image": CASE_IMAGES["布达拉宫"],
        "modules": {
            "柱径": {"大经堂": 260, "小经堂": 195},
            "比例": "梁高=8柱径",
            "墙厚": "收分明显"
        }
    },
    "高句丽制": {
        "year": "前37-668年",
        "dynasty": "高句丽",
        "color": "#16a085",
        "icon": "🏯",
        "source": "《三国史记》",
        "author": "金富轼",
        "ancient": "高句丽建筑依山而建，用材粗犷，柱础雄大。城垣以石垒砌，宫殿以木构为主。",
        "modern": "高句丽建筑采用独特的叠涩顶和柱心支撑结构。墓葬建筑尤为发达，将军坟等巨型石室墓体现了高句丽高超的石构技术。",
        "features": ["依山而建", "石构为主", "叠涩技术", "柱心支撑"],
        "example": "将军坟、五盔坟",
        "image": CASE_IMAGES["将军坟"],
        "modules": {
            "石材": "巨型条石",
            "叠涩": "逐层收进",
            "墓室": "石室结构"
        }
    },
    "渤海国制": {
        "year": "698-926年",
        "dynasty": "渤海国",
        "color": "#2c3e50",
        "icon": "🏯",
        "source": "《渤海国志长编》",
        "author": "金毓黻",
        "ancient": "渤海建筑效法唐制，融合靺鞨民族特色。宫殿用材硕大，厅堂布局严谨。",
        "modern": "渤海国建筑以石木混合结构为主，既采用唐代的材分制，又融入地方民族特色。上京龙泉府遗址展现了渤海建筑的宏伟规模。",
        "features": ["石木混合", "效法唐制", "民族融合", "布局严谨"],
        "example": "上京龙泉府遗址、贞孝公主墓",
        "image": "https://images.unsplash.com/photo-1590845947674-f6e8b9f8a4e8?w=800",
        "modules": {
            "材等": {"殿材": 235, "堂材": 195},
            "结构": "石基木构",
            "瓦作": "琉璃瓦"
        }
    },
    "南诏大理制": {
        "year": "738-1254年",
        "dynasty": "南诏大理",
        "color": "#8e44ad",
        "icon": "🛕",
        "source": "《蛮书》《南诏野史》",
        "author": "樊绰等",
        "ancient": "南诏大理建筑融合中原与南亚风格，宫殿干栏式，民居白族风格。",
        "modern": "南诏大理建筑以干栏式建筑和白族民居为代表，融合了中原、南亚和本地特色。大理古城、喜洲白族民居是典型代表。",
        "features": ["干栏建筑", "白族民居", "南亚风格", "地域特色"],
        "example": "大理古城、太和城遗址",
        "image": "https://images.unsplash.com/photo-1590845947674-f6e8b9f8a4e8?w=800",
        "modules": {
            "民居": "三坊一照壁",
            "布局": "四合院式",
            "装饰": "木雕彩绘"
        }
    }
}

# ========== 经典案例库 ==========
CLASSIC_CASES = {
    "唐制·大木作": [
        {
            "name": "大明宫含元殿遗址",
            "location": "陕西西安",
            "year": "663年",
            "desc": "唐代大明宫正殿，是唐代举行重大国事活动的场所。殿基高15米，面阔十一间，进深四间，体现了唐代建筑的恢宏气势。",
            "features": ["十一开间大殿", "高台基", "唐代最高规格"],
            "image": CASE_IMAGES["大明宫含元殿遗址"]
        },
        {
            "name": "麟德殿遗址",
            "location": "陕西西安",
            "year": "唐",
            "desc": "唐代大明宫内规模最大的殿堂，由前、中、后三殿组成，面阔十一间，进深十七间，是唐代皇帝举行宴会、接见使节的重要场所。",
            "features": ["三殿相连", "规模宏大", "功能多样"],
            "image": CASE_IMAGES["麟德殿遗址"]
        }
    ],
    "宋制·材分制": [
        {
            "name": "隆兴寺摩尼殿",
            "location": "河北正定",
            "year": "1052年",
            "desc": "宋代建筑的杰出代表，采用“材分制”营造。殿身面阔七间，进深七间，重檐九脊顶，四面出抱厦，形成十字形平面，建筑造型独特。",
            "features": ["十字平面", "四面抱厦", "斗拱雄大"],
            "image": CASE_IMAGES["隆兴寺摩尼殿"]
        },
        {
            "name": "玄妙观三清殿",
            "location": "江苏苏州",
            "year": "南宋",
            "desc": "江南现存最大的宋代木构建筑，面阔九间，进深六间，用材宏大，斗拱繁复。殿内采用减柱造，空间开阔，体现了南宋高超的建筑技艺。",
            "features": ["九开间大殿", "减柱造", "江南特色"],
            "image": CASE_IMAGES["玄妙观三清殿"]
        }
    ],
    "清制·斗口制": [
        {
            "name": "故宫太和殿",
            "location": "北京",
            "year": "1695年",
            "desc": "清代等级最高的建筑，采用斗口制营造。面阔十一间，进深五间，重檐庑殿顶。殿高35.05米，是中国现存最大的木构殿宇，体现了清代官式建筑的最高成就。",
            "features": ["十一开间", "重檐庑殿", "最高等级"],
            "image": CASE_IMAGES["故宫太和殿"]
        },
        {
            "name": "颐和园",
            "location": "北京",
            "year": "1894年",
            "desc": "清代皇家园林的代表，集传统造园艺术之大成。万寿山、昆明湖构成山水画卷，佛香阁、长廊等建筑精美绝伦。",
            "features": ["皇家园林", "山水画卷", "建筑精美"],
            "image": CASE_IMAGES["颐和园"]
        }
    ],
    "明制·官式": [
        {
            "name": "太庙戟门",
            "location": "北京",
            "year": "明",
            "desc": "明代官式建筑的代表，采用斗口制。面阔五间，进深两间，单檐庑殿顶。建筑规制严谨，斗拱规范，体现了明代建筑的标准化水平。",
            "features": ["规制严谨", "斗口规范", "官式典范"],
            "image": CASE_IMAGES["太庙戟门"]
        },
        {
            "name": "长陵祾恩殿",
            "location": "北京",
            "year": "明",
            "desc": "明代陵寝建筑的杰作，面阔九间，进深五间，重檐庑殿顶。殿内使用60根金丝楠木巨柱，气势宏伟，体现了明代皇家建筑的至高规格。",
            "features": ["楠木巨柱", "九开间大殿", "皇家气派"],
            "image": CASE_IMAGES["长陵祾恩殿"]
        }
    ],
    "民居大观": [
        {
            "name": "乔家大院",
            "location": "山西祁县",
            "year": "清",
            "desc": "晋商大院的杰出代表，城堡式建筑群，'在中堂'是乔家大院的核心建筑。砖雕、木雕、石雕精美绝伦。",
            "features": ["城堡式布局", "晋商风格", "三雕精美"],
            "image": CASE_IMAGES["乔家大院"]
        },
        {
            "name": "王家大院",
            "location": "山西灵石",
            "year": "明-清",
            "desc": "'王家归来不看院'，五巷六堡一条街，总面积25万平方米，是中国最大的民居建筑群。",
            "features": ["规模最大", "依山而建", "官宅特色"],
            "image": CASE_IMAGES["王家大院"]
        },
        {
            "name": "徽州民居",
            "location": "安徽徽州",
            "year": "明-清",
            "desc": "粉墙黛瓦马头墙，天井采光四水归堂。木雕、砖雕、石雕并称'徽州三雕'，是中国传统民居的瑰宝。",
            "features": ["粉墙黛瓦", "马头墙", "徽州三雕"],
            "image": CASE_IMAGES["徽州民居"]
        },
        {
            "name": "北京四合院",
            "location": "北京",
            "year": "元-清",
            "desc": "北方合院式民居的代表，布局严谨，中轴对称，体现了封建社会的等级制度和家族观念。",
            "features": ["中轴对称", "内外有别", "青砖灰瓦"],
            "image": CASE_IMAGES["北京四合院"]
        }
    ],
    "桥梁工程": [
        {
            "name": "赵州桥",
            "location": "河北赵县",
            "year": "隋代",
            "desc": "世界上现存最古老的石拱桥，由李春设计建造。采用敞肩拱结构，开创了桥梁建筑的新纪元。",
            "features": ["敞肩拱", "单孔石桥", "1400年历史"],
            "image": CASE_IMAGES["赵州桥"]
        }
    ]
}

# ========== 工具函数 ==========
def get_image_base64(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

def display_image_from_file(image_path, caption=None, height=None):
    img_base64 = get_image_base64(image_path)
    if img_base64:
        height_style = f"height: {height};" if height else "width: 100%;"
        st.markdown(f"""
        <div style="text-align: center;">
            <img src="data:image/png;base64,{img_base64}" style="{height_style} border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); object-fit: cover;">
            {f'<p style="color: #666; margin-top: 5px;">{caption}</p>' if caption else ''}
        </div>
        """, unsafe_allow_html=True)
        return True
    else:
        st.markdown(f"""
        <div style="text-align: center;">
            <div style="height: 220px; background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; font-size: 2rem;">🏯</div>
            {f'<p style="color: #666; margin-top: 5px;">{caption}</p>' if caption else ''}
        </div>
        """, unsafe_allow_html=True)
        return False

def back_btn():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔙 返回上一级", key="back_button_main", use_container_width=True):
            if st.session_state.detail is not None:
                st.session_state.detail = None
            elif st.session_state.module2_system is not None:
                st.session_state.module2_system = None
            else:
                st.session_state.page = 'home'
            st.markdown('<script>window.scrollTo(0, 0);</script>', unsafe_allow_html=True)
            st.rerun()

def parse_year(year_str):
    try:
        year_str = year_str.replace('年', '')
        if '-' in year_str and not year_str.startswith('前'):
            parts = year_str.split('-')
            return int(parts[0])
        elif year_str.startswith('前'):
            match = re.search(r'前(\d+)', year_str)
            if match:
                return -int(match.group(1))
            else:
                return 0
        else:
            return int(year_str)
    except:
        return 1000

def create_knowledge_graph():
    G = nx.Graph()
    systems = list(BUILDING_SYSTEMS.keys())
    for system in systems:
        G.add_node(system, size=20)
    
    edges = [
        ("唐制·大木作", "宋制·材分制"),
        ("唐制·大木作", "辽制·大木作"),
        ("宋制·材分制", "金制·大木作"),
        ("宋制·材分制", "元制·官式大木"),
        ("元制·官式大木", "明制·官式"),
        ("明制·官式", "清制·斗口制"),
        ("唐制·大木作", "渤海国制"),
        ("宋制·材分制", "西夏·官式"),
        ("唐制·大木作", "藏式·大木"),
        ("南诏大理制", "藏式·大木"),
        ("高句丽制", "渤海国制")
    ]
    
    for edge in edges:
        if edge[0] in systems and edge[1] in systems:
            G.add_edge(edge[0], edge[1])
    
    pos = nx.spring_layout(G, k=2, iterations=50)
    
    edge_trace = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace.append(go.Scatter(
            x=[x0, x1, None],
            y=[y0, y1, None],
            mode='lines',
            line=dict(width=2, color='#888'),
            hoverinfo='none',
            showlegend=False
        ))
    
    node_x = []
    node_y = []
    node_text = []
    node_color = []
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)
        node_color.append(BUILDING_SYSTEMS[node]["color"] if node in BUILDING_SYSTEMS else "#888")
    
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_text,
        textposition="top center",
        hoverinfo='text',
        marker=dict(
            size=30,
            color=node_color,
            line=dict(width=2, color='white')
        ),
        showlegend=False
    )
    
    fig = go.Figure(data=edge_trace + [node_trace])
    fig.update_layout(
        title="营造制度知识图谱 - 传承与影响关系",
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20,l=5,r=5,t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=500,
        plot_bgcolor='rgba(255,255,255,0.9)'
    )
    return fig

def create_comparison_chart():
    systems = list(BUILDING_SYSTEMS.keys())
    dynasties = [BUILDING_SYSTEMS[s]["dynasty"] for s in systems]
    years = [BUILDING_SYSTEMS[s]["year"] for s in systems]
    
    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{'type': 'bar'}, {'type': 'scatter'}],
               [{'type': 'table', 'colspan': 2}, None]],
        subplot_titles=("材等数量对比", "时间轴分布", "制度参数对比"),
        row_heights=[0.4, 0.3]
    )
    
    module_counts = []
    for s in systems:
        if "材等" in BUILDING_SYSTEMS[s]["modules"]:
            count = len(BUILDING_SYSTEMS[s]["modules"]["材等"])
        else:
            count = 0
        module_counts.append(count)
    
    fig.add_trace(
        go.Bar(
            x=systems,
            y=module_counts,
            marker_color=[BUILDING_SYSTEMS[s]["color"] for s in systems],
            text=module_counts,
            textposition='auto',
            name='材等数量'
        ),
        row=1, col=1
    )
    
    year_numeric = [parse_year(y) for y in years]
    
    fig.add_trace(
        go.Scatter(
            x=systems,
            y=year_numeric,
            mode='markers+lines',
            marker=dict(size=15, color=[BUILDING_SYSTEMS[s]["color"] for s in systems]),
            line=dict(color='#888', width=2),
            text=years,
            name='年代'
        ),
        row=1, col=2
    )
    
    table_data = []
    for system in systems[:6]:
        data = BUILDING_SYSTEMS[system]
        table_data.append([
            system,
            data["dynasty"],
            data["features"][0] if data["features"] else "",
            data["example"].split('、')[0] if data["example"] else ""
        ])
    
    fig.add_trace(
        go.Table(
            header=dict(
                values=["体系名称", "朝代", "主要特征", "代表建筑"],
                fill_color='#667eea',
                font=dict(color='white', size=12),
                align='center'
            ),
            cells=dict(
                values=list(zip(*table_data)),
                fill_color='#f8f9fa',
                align='left',
                font_size=11
            )
        ),
        row=2, col=1
    )
    
    fig.update_layout(height=800, showlegend=False)
    return fig

# ========== 模块四专用函数 ==========
def calculate_dimensions(system_name, grade, jian_shu, ming_jian_fen, ci_jian_fen, bu_jia_shu, bu_shen_fen, ju_zhe_ratio):
    system = SYSTEMS[system_name]
    base_unit = system["base_unit"](grade)
    unit_name = system["unit"]
    
    if system_name == "宋制·材分制":
        data = {
            "构件": ["材(高)", "材(厚)", "栔(高)", "足材(高)", "檐柱径", "明间面阔", "次间面阔", "步架深", "檐柱高"],
            f"尺寸({unit_name})": [15, 10, 6, 21, 30, ming_jian_fen, ci_jian_fen, bu_shen_fen, 6*15],
            "尺寸(mm)": [f"{15 * base_unit:.1f}", f"{10 * base_unit:.1f}",
                        f"{6 * base_unit:.1f}", f"{21 * base_unit:.1f}",
                        f"{30 * base_unit:.1f}", f"{ming_jian_fen * base_unit:.1f}",
                        f"{ci_jian_fen * base_unit:.1f}", f"{bu_shen_fen * base_unit:.1f}",
                        f"{6*15 * base_unit:.1f}"]
        }
    elif system_name == "清制·斗口制":
        data = {
            "构件": ["斗口尺寸", "檐柱径", "明间面阔", "次间面阔", "步架深", "额枋高", "平板枋高", "檐柱高"],
            f"尺寸({unit_name})": [1, 6, 11, 9, 4, 6, 2, 10],
            "尺寸(mm)": [f"{base_unit:.1f}", f"{6 * base_unit:.1f}", f"{11 * base_unit:.1f}",
                        f"{9 * base_unit:.1f}", f"{4 * base_unit:.1f}", f"{6 * base_unit:.1f}", 
                        f"{2 * base_unit:.1f}", f"{10 * base_unit:.1f}"]
        }
    else:
        data = {
            "构件": ["基准材", "檐柱径", "明间面阔", "次间面阔", "步架深", "檐柱高"],
            f"尺寸({unit_name})": [1, 2, 25, 20, 12, 6],
            "尺寸(mm)": [f"{base_unit * 10:.1f}", f"{2 * base_unit * 10:.1f}",
                        f"{25 * base_unit * 10:.1f}", f"{20 * base_unit * 10:.1f}",
                        f"{12 * base_unit * 10:.1f}", f"{6 * base_unit * 10:.1f}"]
        }
    
    df = pd.DataFrame(data)
    jian_width = ming_jian_fen * base_unit
    bu_jia_depth = bu_shen_fen * base_unit
    total_width = jian_shu * jian_width
    total_depth = bu_jia_shu * bu_jia_depth
    ju_gao = total_depth * ju_zhe_ratio
    
    mechanics = calculate_mechanics(system_name, grade, jian_shu, base_unit, jian_width, bu_jia_depth, ju_zhe_ratio)
    compliance = check_compliance(system_name, grade, jian_shu, ming_jian_fen, ci_jian_fen, bu_jia_shu, bu_shen_fen, ju_zhe_ratio)
    
    return df, base_unit, total_width, total_depth, ju_gao, mechanics, compliance

def calculate_mechanics(system_name, grade, jian_shu, base_unit, jian_width, bu_jia_depth, ju_zhe_ratio):
    if system_name == "宋制·材分制":
        zhu_jing = 2 * 15 * base_unit
        zhu_gao = 6 * 15 * base_unit
    elif system_name == "清制·斗口制":
        zhu_jing = 6 * base_unit
        zhu_gao = 10 * base_unit
    else:
        zhu_jing = 2 * base_unit * 10
        zhu_gao = 6 * base_unit * 10
    
    wood_strength = st.session_state.module4_params.get('wood_strength', 30)
    elastic_modulus = 10000
    
    area = np.pi * (zhu_jing / 2)**2
    inertia = np.pi * (zhu_jing)**4 / 64
    
    dead_load = 3.0
    live_load = st.session_state.module4_params.get('load_factor', 5.0)
    snow_load = 0.5
    wind_load = 0.8
    
    total_load_per_area = dead_load + live_load + snow_load + wind_load
    building_area = (jian_shu * jian_width) * (4 * bu_jia_depth) / 1000000
    total_load = total_load_per_area * building_area
    
    bearing_capacity = area * wood_strength / 1000
    column_count = (jian_shu + 1) * 5
    load_per_column = total_load / column_count
    safety_factor = bearing_capacity / load_per_column
    
    slenderness_ratio = zhu_gao / (zhu_jing / 4)
    stability_factor = min(1.0, 3000 / (slenderness_ratio**2)) if slenderness_ratio > 0 else 1.0
    
    deflection = (5 * total_load * 1000 * (zhu_gao**3)) / (384 * elastic_modulus * inertia)
    
    stress = load_per_column * 1000 / area
    
    return {
        "柱径": f"{zhu_jing:.1f} mm",
        "柱高": f"{zhu_gao:.1f} mm",
        "长细比": f"{slenderness_ratio:.1f}",
        "单柱承载力": f"{bearing_capacity:.1f} kN",
        "单柱荷载": f"{load_per_column:.1f} kN",
        "安全系数": f"{safety_factor:.2f}",
        "稳定性系数": f"{stability_factor:.3f}",
        "柱顶挠度": f"{deflection:.2f} mm",
        "柱应力": f"{stress:.2f} MPa",
        "承载力利用率": f"{(load_per_column/bearing_capacity*100):.1f}%"
    }

def check_compliance(system_name, grade, jian_shu, ming_jian_fen, ci_jian_fen, bu_jia_shu, bu_shen_fen, ju_zhe_ratio):
    system = SYSTEMS[system_name]
    rules = system["rules"]
    
    compliance_results = []
    
    if jian_shu < rules["min_jian_shu"] or jian_shu > rules["max_jian_shu"]:
        compliance_results.append(("开间数", f"应在{rules['min_jian_shu']}-{rules['max_jian_shu']}之间", "fail"))
    else:
        compliance_results.append(("开间数", f"{jian_shu}间 (合规)", "pass"))
    
    if bu_jia_shu < rules["min_bu_jia"] or bu_jia_shu > rules["max_bu_jia"]:
        compliance_results.append(("步架数", f"应在{rules['min_bu_jia']}-{rules['max_bu_jia']}之间", "fail"))
    else:
        compliance_results.append(("步架数", f"{bu_jia_shu}架 (合规)", "pass"))
    
    if ming_jian_fen < rules["ming_jian_range"][0] or ming_jian_fen > rules["ming_jian_range"][1]:
        compliance_results.append(("明间宽度", f"应在{rules['ming_jian_range'][0]}-{rules['ming_jian_range'][1]}分°之间", "warn" if abs(ming_jian_fen - rules["ming_jian_range"][0]) < 50 else "fail"))
    else:
        compliance_results.append(("明间宽度", f"{ming_jian_fen}分° (合规)", "pass"))
    
    if ci_jian_fen < rules["ci_jian_range"][0] or ci_jian_fen > rules["ci_jian_range"][1]:
        compliance_results.append(("次间宽度", f"应在{rules['ci_jian_range'][0]}-{rules['ci_jian_range'][1]}分°之间", "warn"))
    else:
        compliance_results.append(("次间宽度", f"{ci_jian_fen}分° (合规)", "pass"))
    
    if bu_shen_fen < rules["bu_jia_range"][0] or bu_shen_fen > rules["bu_jia_range"][1]:
        compliance_results.append(("步架深度", f"应在{rules['bu_jia_range'][0]}-{rules['bu_jia_range'][1]}分°之间", "warn"))
    else:
        compliance_results.append(("步架深度", f"{bu_shen_fen}分° (合规)", "pass"))
    
    if ju_zhe_ratio < rules["ju_zhe_range"][0] or ju_zhe_ratio > rules["ju_zhe_range"][1]:
        compliance_results.append(("举折系数", f"应在{rules['ju_zhe_range'][0]:.2f}-{rules['ju_zhe_range'][1]:.2f}之间", "warn"))
    else:
        compliance_results.append(("举折系数", f"{ju_zhe_ratio:.3f} (合规)", "pass"))
    
    return compliance_results

def draw_structure_diagram(jian_shu, bu_jia_shu, jian_width, bu_jia_depth, zhu_jing, zhu_gao, ju_gao, system_color):
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    total_width = jian_shu * jian_width
    total_depth = bu_jia_shu * bu_jia_depth
    
    for i in range(jian_shu + 1):
        x = i * jian_width
        for j in range(bu_jia_shu + 1):
            y = j * bu_jia_depth
            circle = plt.Circle((x, y), zhu_jing/2000, color=system_color, alpha=0.7)
            ax1.add_patch(circle)
    
    for i in range(jian_shu):
        for j in range(bu_jia_shu):
            rect = patches.Rectangle((i*jian_width, j*bu_jia_depth), jian_width, bu_jia_depth, 
                                   fill=False, edgecolor='#95a5a6', linestyle='--', linewidth=1)
            ax1.add_patch(rect)
    
    ax1.set_xlim(-500, total_width + 500)
    ax1.set_ylim(-500, total_depth + 500)
    ax1.set_aspect('equal')
    ax1.set_xlabel('面阔方向 (mm)')
    ax1.set_ylabel('进深方向 (mm)')
    ax1.set_title('柱网平面图')
    ax1.grid(True, alpha=0.3)
    
    x = np.linspace(0, total_width, 100)
    roof_line = ju_gao * (1 - (x/total_width)**1.5) + zhu_gao
    
    ax2.plot([0, total_width], [zhu_gao, zhu_gao], 'b-', linewidth=2, label='檐口')
    ax2.plot(x, roof_line, 'r-', linewidth=2, label='屋顶轮廓')
    
    for i in range(jian_shu + 1):
        x_pos = i * jian_width
        ax2.plot([x_pos, x_pos], [0, zhu_gao], 'k-', linewidth=1.5, alpha=0.5)
    
    ax2.set_xlim(-500, total_width + 500)
    ax2.set_ylim(0, ju_gao + zhu_gao + 500)
    ax2.set_xlabel('面阔方向 (mm)')
    ax2.set_ylabel('高度 (mm)')
    ax2.set_title('正立面图')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='#f8f9fa')
    buf.seek(0)
    plt.close(fig)
    return buf

def create_heatmap(jian_shu, bu_jia_shu, stress_values, system_color):
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    
    stress_matrix = np.array(stress_values).reshape(bu_jia_shu + 1, jian_shu + 1)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    im = ax.imshow(stress_matrix, cmap='YlOrRd', aspect='auto', interpolation='bilinear')
    
    ax.set_xticks(np.arange(jian_shu + 1))
    ax.set_yticks(np.arange(bu_jia_shu + 1))
    ax.set_xticklabels([f'开间{i+1}' for i in range(jian_shu + 1)])
    ax.set_yticklabels([f'步架{j+1}' for j in range(bu_jia_shu + 1)])
    
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    
    for i in range(bu_jia_shu + 1):
        for j in range(jian_shu + 1):
            text = ax.text(j, i, f'{stress_matrix[i, j]:.1f}',
                         ha="center", va="center", color="white" if stress_matrix[i, j] > 0.5 else "black", fontsize=8)
    
    ax.set_title('构件受力热力图 (MPa)')
    fig.colorbar(im, ax=ax, label='应力 (MPa)')
    
    plt.tight_layout()
    
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    return buf

def generate_recommendations(system_name, grade, jian_shu, bu_jia_shu, ming_jian_fen, ci_jian_fen, bu_shen_fen, ju_zhe_ratio, safety_factor):
    recommendations = []
    
    if safety_factor is not None:
        try:
            sf = float(str(safety_factor).replace(' ', '').replace('倍', ''))
            if sf < 1.5:
                recommendations.append({
                    "type": "warning",
                    "title": "⚠️ 安全系数偏低",
                    "desc": f"当前安全系数为 {sf:.2f}，建议增大构件截面尺寸"
                })
            elif sf > 3.0:
                recommendations.append({
                    "type": "info",
                    "title": "ℹ️ 安全系数偏高",
                    "desc": f"安全系数为 {sf:.2f}，可考虑优化用材以节约成本"
                })
        except:
            pass
    
    if ju_zhe_ratio < 0.28:
        recommendations.append({
            "type": "info",
            "title": "📐 举折系数偏小",
            "desc": "建议增加举折系数至0.3左右，改善屋面排水"
        })
    elif ju_zhe_ratio > 0.38:
        recommendations.append({
            "type": "warning",
            "title": "⚠️ 举折系数偏大",
            "desc": "建议减小举折系数，避免屋面过陡"
        })
    
    if jian_shu < 3:
        recommendations.append({
            "type": "info",
            "title": "🏛️ 建筑规模较小",
            "desc": "可考虑增加开间数至3-5间，提升建筑气势"
        })
    elif jian_shu > 7:
        recommendations.append({
            "type": "warning",
            "title": "⚠️ 建筑规模较大",
            "desc": "注意结构整体稳定性，建议增设抗震措施"
        })
    
    if ci_jian_fen > 0:
        ratio = ming_jian_fen / ci_jian_fen
        if ratio < 1.1 or ratio > 1.3:
            recommendations.append({
                "type": "info",
                "title": "📏 开间比例优化",
                "desc": "建议明次间比例保持在1.2左右，符合传统审美"
            })
    
    if bu_jia_shu < 3:
        recommendations.append({
            "type": "info",
            "title": "📐 进深较小",
            "desc": "建议增加步架数以获得更合理的进深比例"
        })
    
    return recommendations

def save_to_excel(df, filename="古建尺寸表.xlsx"):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='古建尺寸表', index=False)
    output.seek(0)
    return output

def generate_text_report(system_name, grade, df, mechanics, compliance, recommendations):
    report = f"""中国古代建筑数字化设计报告
生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

体系：{system_name}
等级：{grade}

一、构件尺寸表
{df.to_string(index=False)}

二、力学分析结果
"""
    for key, value in mechanics.items():
        report += f"{key}：{value}\n"
    
    report += "\n三、规制合规性检测\n"
    for item, msg, status in compliance:
        status_text = "✓ 通过" if status == "pass" else "⚠ 警告" if status == "warn" else "✗ 不通过"
        report += f"{item}：{msg} [{status_text}]\n"
    
    report += "\n四、智能优化建议\n"
    for rec in recommendations:
        report += f"{rec['title']}：{rec['desc']}\n"
    
    return BytesIO(report.encode('utf-8'))

def save_svg_diagram(fig):
    buf = BytesIO()
    fig.savefig(buf, format='svg', dpi=150, bbox_inches='tight')
    buf.seek(0)
    return buf

# ========== 模块三：数学建模动画函数 ==========
def create_caifen_animation(system_name, grade, jian_shu, bu_jia_shu, ming_jian_fen, bu_shen_fen, ju_zhe_ratio, system_color, base_unit):
    """材分制建筑动画 - 比例优化版 + 控件分离"""
    
    jian_width = ming_jian_fen * base_unit / 1000
    bu_depth = bu_shen_fen * base_unit / 1000
    total_width = jian_shu * jian_width
    total_depth = bu_jia_shu * bu_depth
    
    if system_name == "宋制·材分制":
        column_height = 6 * 15 * base_unit / 1000
        column_radius = column_height / 12
    else:
        column_height = 6 * base_unit * 10 / 1000
        column_radius = column_height / 12
    
    roof_height = total_depth * ju_zhe_ratio
    
    beam_height = column_radius * 0.8
    dougong_width = column_radius * 1.2
    dougong_height = column_radius * 0.6
    
    steps_desc = {
        1: {"name": "奠基·台基", "desc": "平整土地，夯筑台基。古代建筑先筑台基，防潮防水，奠定建筑基础。台基高度决定建筑等级。", "icon": "⛰️"},
        2: {"name": "立柱·柱网", "desc": "竖立檐柱，形成柱网。柱径与柱高遵循材分制比例，柱网决定建筑开间与进深。", "icon": "🌲"},
        3: {"name": "架梁·大木", "desc": "安装梁架，形成屋架结构。抬梁式构架，层层叠叠，承托屋顶。", "icon": "🏗️"},
        4: {"name": "铺作·斗拱", "desc": "铺设斗拱层。斗拱是古建筑精华，层层出挑，传递荷载，兼具装饰功能。", "icon": "⚙️"},
        5: {"name": "举折·屋顶", "desc": "架设檩条，铺设望板。举折之制，屋顶曲线优美，排水顺畅。", "icon": "🏔️"},
        6: {"name": "瓦作·装饰", "desc": "铺设琉璃瓦，安装脊兽。屋面装饰体现建筑等级，龙吻、走兽各具寓意。", "icon": "✨"},
        7: {"name": "落成·全貌", "desc": "建筑落成！完整呈现中国古建筑的恢宏气势与精妙构造。", "icon": "🏯"}
    }
    
    animation_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ 
                background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
                overflow: hidden;
                font-family: 'Microsoft YaHei', monospace;
            }}
            #canvas-container {{ width: 100%; height: 100vh; }}
            .controls-container {{
                position: fixed;
                bottom: 20px;
                left: 20px;
                right: 20px;
                background: rgba(0,0,0,0.85);
                backdrop-filter: blur(15px);
                border-radius: 20px;
                padding: 15px;
                z-index: 100;
                border: 1px solid rgba(255,215,150,0.3);
                box-shadow: 0 10px 30px rgba(0,0,0,0.4);
                display: flex;
                flex-direction: column;
                gap: 10px;
            }}
            .step-buttons {{
                display: flex;
                justify-content: center;
                gap: 10px;
                flex-wrap: wrap;
            }}
            .step-btn {{
                background: linear-gradient(135deg, #2c3e50, #34495e);
                border: none;
                color: white;
                padding: 8px 16px;
                border-radius: 30px;
                cursor: pointer;
                font-size: 12px;
                font-weight: bold;
                transition: all 0.3s ease;
                min-width: 70px;
            }}
            .step-btn:hover, .step-btn.active {{
                background: linear-gradient(135deg, #{system_color[1:] if system_color.startswith('#') else '8B4513'}, #{system_color[1:] if system_color.startswith('#') else 'A0522D'});
                transform: translateY(-2px);
            }}
            .action-buttons {{
                display: flex;
                justify-content: center;
                gap: 15px;
            }}
            .action-btn {{
                background: rgba(255,255,255,0.2);
                border: 1px solid rgba(255,215,150,0.5);
                color: #ffd796;
                padding: 6px 16px;
                border-radius: 25px;
                cursor: pointer;
                font-size: 12px;
                transition: all 0.3s ease;
            }}
            .action-btn:hover {{
                background: rgba(255,215,150,0.3);
                transform: scale(1.05);
            }}
            .step-desc {{
                text-align: center;
                color: #ffd796;
                font-size: 13px;
                padding: 8px;
                background: rgba(0,0,0,0.5);
                border-radius: 10px;
            }}
            .progress-bar {{
                height: 3px;
                background: rgba(255,255,255,0.2);
                border-radius: 2px;
                overflow: hidden;
            }}
            .progress-fill {{
                height: 100%;
                background: linear-gradient(90deg, #{system_color[1:] if system_color.startswith('#') else 'FF6B6B'}, #{system_color[1:] if system_color.startswith('#') else '4ECDC4'});
                width: 0%;
                transition: width 0.3s ease;
            }}
            .stats {{
                position: fixed;
                top: 20px;
                right: 20px;
                color: rgba(255,255,255,0.6);
                background: rgba(0,0,0,0.5);
                padding: 6px 12px;
                border-radius: 20px;
                font-size: 11px;
                font-family: monospace;
                z-index: 100;
            }}
        </style>
    </head>
    <body>
        <div id="canvas-container"></div>
        <div class="stats">进度: <span id="progress-text">0</span>% | 构件: <span id="component-count">0</span></div>
        <div class="controls-container">
            <div class="step-buttons" id="step-buttons"></div>
            <div class="action-buttons">
                <button class="action-btn" onclick="playAll()">▶ 一键成形动画</button>
                <button class="action-btn" onclick="resetView()">🎥 重置视角</button>
                <button class="action-btn" onclick="toggleWireframe()">🔲 线框模式</button>
            </div>
            <div class="progress-bar"><div class="progress-fill" id="progress-fill"></div></div>
            <div class="step-desc" id="step-desc">点击步骤按钮，观看分步建造过程</div>
        </div>
        
        <script type="importmap">
            {{
                "imports": {{
                    "three": "https://unpkg.com/three@0.128.0/build/three.module.js",
                    "three/addons/": "https://unpkg.com/three@0.128.0/examples/jsm/"
                }}
            }}
        </script>
        
        <script type="module">
            import * as THREE from 'three';
            import {{ OrbitControls }} from 'three/addons/controls/OrbitControls.js';
            
            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0x0f0c29);
            scene.fog = new THREE.FogExp2(0x0f0c29, 0.008);
            
            const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
            camera.position.set(8, 5, 12);
            
            const renderer = new THREE.WebGLRenderer({{ antialias: true }});
            renderer.setSize(window.innerWidth, window.innerHeight);
            renderer.shadowMap.enabled = true;
            document.getElementById('canvas-container').appendChild(renderer.domElement);
            
            const controls = new OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;
            controls.target.set(0, 2, 0);
            
            const ambientLight = new THREE.AmbientLight(0x404040);
            scene.add(ambientLight);
            const mainLight = new THREE.DirectionalLight(0xfff5e6, 1.2);
            mainLight.position.set(5, 10, 7);
            mainLight.castShadow = true;
            scene.add(mainLight);
            const fillLight = new THREE.PointLight(0x88aaff, 0.5);
            fillLight.position.set(3, 4, 4);
            scene.add(fillLight);
            const backLight = new THREE.PointLight(0xffaa66, 0.4);
            backLight.position.set(-3, 5, -5);
            scene.add(backLight);
            
            const gridHelper = new THREE.GridHelper(20, 20, 0x88aaff, 0x335588);
            gridHelper.position.y = -0.1;
            gridHelper.material.transparent = true;
            gridHelper.material.opacity = 0.3;
            scene.add(gridHelper);
            
            const buildingGroup = new THREE.Group();
            scene.add(buildingGroup);
            
            const jianShu = {jian_shu};
            const buJiaShu = {bu_jia_shu};
            const jianWidth = {jian_width};
            const buDepth = {bu_depth};
            const totalWidth = {total_width};
            const totalDepth = {total_depth};
            const columnHeight = {column_height};
            const columnRadius = {column_radius};
            const roofHeight = {roof_height};
            const beamHeight = {beam_height};
            const dougongWidth = {dougong_width};
            const dougongHeight = {dougong_height};
            
            const woodMat = new THREE.MeshStandardMaterial({{ color: 0xCD853F, roughness: 0.5, metalness: 0.1 }});
            const darkWoodMat = new THREE.MeshStandardMaterial({{ color: 0x8B5A2B, roughness: 0.5 }});
            const roofMat = new THREE.MeshStandardMaterial({{ color: 0x4a3a2a, roughness: 0.8, metalness: 0.05 }});
            const dougongMat = new THREE.MeshStandardMaterial({{ color: 0xD2691E, roughness: 0.4 }});
            const platformMat = new THREE.MeshStandardMaterial({{ color: 0xBC9A6C, roughness: 0.7 }});
            const stoneMat = new THREE.MeshStandardMaterial({{ color: 0x9B7B5C, roughness: 0.7 }});
            const goldMat = new THREE.MeshStandardMaterial({{ color: 0xffaa66, metalness: 0.6, roughness: 0.3 }});
            
            let components = [];
            let currentStep = 0;
            let animating = false;
            const stepsDesc = {steps_desc};
            
            function generatePlatform(progress) {{
                if (progress <= 0) return;
                const platformGeo = new THREE.BoxGeometry(totalWidth + 0.8, 0.25 * progress, totalDepth + 0.8);
                const platform = new THREE.Mesh(platformGeo, platformMat);
                platform.position.set(0, -0.125 * progress, 0);
                platform.castShadow = true;
                buildingGroup.add(platform);
                components.push(platform);
                const edgeGeo = new THREE.BoxGeometry(totalWidth + 1.0, 0.08, 0.2);
                const frontEdge = new THREE.Mesh(edgeGeo, stoneMat);
                frontEdge.position.set(0, -0.125 * progress + 0.2, totalDepth/2 + 0.4);
                buildingGroup.add(frontEdge);
                components.push(frontEdge);
                const backEdge = new THREE.Mesh(edgeGeo, stoneMat);
                backEdge.position.set(0, -0.125 * progress + 0.2, -totalDepth/2 - 0.4);
                buildingGroup.add(backEdge);
                components.push(backEdge);
            }}
            
            function generateColumns(progress) {{
                const startX = -totalWidth / 2;
                const startZ = -totalDepth / 2;
                const stepX = jianWidth;
                const stepZ = buDepth;
                const totalCols = (jianShu + 1) * (buJiaShu + 1);
                const targetCount = Math.floor(totalCols * progress);
                let built = 0;
                for (let i = 0; i <= jianShu && built < targetCount; i++) {{
                    for (let j = 0; j <= buJiaShu && built < targetCount; j++) {{
                        const x = startX + i * stepX;
                        const z = startZ + j * stepZ;
                        const colGeo = new THREE.CylinderGeometry(columnRadius, columnRadius * 1.05, columnHeight, 24);
                        const column = new THREE.Mesh(colGeo, woodMat);
                        column.position.set(x, columnHeight/2, z);
                        column.castShadow = true;
                        buildingGroup.add(column);
                        components.push(column);
                        const baseGeo = new THREE.CylinderGeometry(columnRadius + 0.04, columnRadius + 0.08, 0.1, 12);
                        const base = new THREE.Mesh(baseGeo, stoneMat);
                        base.position.set(x, 0.05, z);
                        buildingGroup.add(base);
                        components.push(base);
                        built++;
                    }}
                }}
            }}
            
            function generateBeams(progress) {{
                if (progress <= 0) return;
                const startX = -totalWidth / 2;
                const beamCount = jianShu * buJiaShu;
                const target = Math.floor(beamCount * progress);
                let built = 0;
                for (let i = 0; i < jianShu && built < target; i++) {{
                    for (let j = 0; j < buJiaShu && built < target; j++) {{
                        const x = startX + i * jianWidth + jianWidth/2;
                        const z = -totalDepth/2 + j * buDepth + buDepth/2;
                        const beamGeo = new THREE.BoxGeometry(jianWidth * 0.85, beamHeight, buDepth * 0.85);
                        const beam = new THREE.Mesh(beamGeo, darkWoodMat);
                        beam.position.set(x, columnHeight - beamHeight/2, z);
                        beam.castShadow = true;
                        buildingGroup.add(beam);
                        components.push(beam);
                        built++;
                    }}
                }}
            }}
            
            function generateDougong(progress) {{
                if (progress <= 0) return;
                const startX = -totalWidth / 2;
                const startZ = -totalDepth / 2;
                const stepX = jianWidth;
                const stepZ = buDepth;
                const totalDougong = (jianShu + 1) * (buJiaShu + 1);
                const target = Math.floor(totalDougong * progress);
                let built = 0;
                for (let i = 0; i <= jianShu && built < target; i++) {{
                    for (let j = 0; j <= buJiaShu && built < target; j++) {{
                        const x = startX + i * stepX;
                        const z = startZ + j * stepZ;
                        const dgGroup = new THREE.Group();
                        const baseGeo = new THREE.BoxGeometry(dougongWidth, dougongHeight*0.4, dougongWidth);
                        const base = new THREE.Mesh(baseGeo, dougongMat);
                        base.position.set(0, 0, 0);
                        dgGroup.add(base);
                        const armGeo = new THREE.BoxGeometry(dougongWidth*0.8, dougongHeight*0.3, dougongWidth*1.2);
                        const arm = new THREE.Mesh(armGeo, dougongMat);
                        arm.position.set(0, dougongHeight*0.3, dougongWidth*0.4);
                        dgGroup.add(arm);
                        const topGeo = new THREE.BoxGeometry(dougongWidth*0.7, dougongHeight*0.3, dougongWidth*0.7);
                        const top = new THREE.Mesh(topGeo, dougongMat);
                        top.position.set(0, dougongHeight*0.7, 0);
                        dgGroup.add(top);
                        dgGroup.position.set(x, columnHeight - 0.02, z);
                        buildingGroup.add(dgGroup);
                        components.push(dgGroup);
                        built++;
                    }}
                }}
            }}
            
            function generateRoof(progress) {{
                if (progress <= 0) return;
                const roofWidth = totalWidth + 0.6;
                const roofDepth = totalDepth + 0.6;
                const roofGeo = new THREE.BoxGeometry(roofWidth * progress, roofHeight * progress, roofDepth * progress);
                const roof = new THREE.Mesh(roofGeo, roofMat);
                roof.position.set(0, columnHeight + roofHeight/2 * progress, 0);
                roof.castShadow = true;
                buildingGroup.add(roof);
                components.push(roof);
                if (progress >= 0.9) {{
                    const ridgeGeo = new THREE.BoxGeometry(roofWidth * 0.9, 0.1, 0.25);
                    const ridge = new THREE.Mesh(ridgeGeo, goldMat);
                    ridge.position.set(0, columnHeight + roofHeight - 0.05, 0);
                    buildingGroup.add(ridge);
                    components.push(ridge);
                    const beastGeo = new THREE.SphereGeometry(0.08, 8, 8);
                    [-roofWidth/3, roofWidth/3].forEach(x => {{
                        const beast = new THREE.Mesh(beastGeo, goldMat);
                        beast.position.set(x, columnHeight + roofHeight - 0.02, roofDepth/2 + 0.1);
                        buildingGroup.add(beast);
                        components.push(beast);
                    }});
                }}
            }}
            
            function addDecorations() {{
                const roofWidth = totalWidth + 0.6;
                const ornamentGeo = new THREE.SphereGeometry(0.12, 16, 16);
                const ornamentMat = new THREE.MeshStandardMaterial({{ color: 0xffaa66, metalness: 0.7 }});
                [-roofWidth/2, roofWidth/2].forEach(x => {{
                    const ornament = new THREE.Mesh(ornamentGeo, ornamentMat);
                    ornament.position.set(x, columnHeight + roofHeight - 0.05, 0);
                    buildingGroup.add(ornament);
                    components.push(ornament);
                }});
            }}
            
            function updateBuilding(step) {{
                components.forEach(comp => buildingGroup.remove(comp));
                components = [];
                if (step >= 1) generatePlatform(1);
                if (step >= 2) generateColumns(1);
                if (step >= 3) generateBeams(1);
                if (step >= 4) generateDougong(1);
                if (step >= 5) generateRoof(0.7);
                if (step >= 6) generateRoof(1);
                if (step >= 7) addDecorations();
                
                const progressPercent = (step / 7) * 100;
                document.getElementById('progress-fill').style.width = progressPercent + '%';
                document.getElementById('progress-text').textContent = Math.floor(progressPercent);
                document.getElementById('component-count').textContent = components.length;
                
                if (stepsDesc[step]) {{
                    document.getElementById('step-desc').innerHTML = `<strong>${{stepsDesc[step].icon}} ${{stepsDesc[step].name}}</strong><br>${{stepsDesc[step].desc}}`;
                }}
            }}
            
            function setStep(step) {{
                currentStep = step;
                updateBuilding(step);
                document.querySelectorAll('.step-btn').forEach((btn, idx) => {{
                    if (idx + 1 === step) btn.classList.add('active');
                    else btn.classList.remove('active');
                }});
            }}
            
            function playAll() {{
                if (animating) return;
                animating = true;
                let step = 1;
                function animateStep() {{
                    if (step <= 7) {{
                        setStep(step);
                        step++;
                        setTimeout(animateStep, 500);
                    }} else {{
                        animating = false;
                    }}
                }}
                animateStep();
            }}
            
            function resetView() {{
                camera.position.set(8, 5, 12);
                controls.target.set(0, 2, 0);
                controls.update();
            }}
            
            function toggleWireframe() {{
                components.forEach(comp => {{
                    if (comp.isMesh && comp.material) {{
                        if (Array.isArray(comp.material)) comp.material.forEach(m => m.wireframe = !m.wireframe);
                        else comp.material.wireframe = !comp.material.wireframe;
                    }}
                }});
            }}
            
            const btnContainer = document.getElementById('step-buttons');
            for (let i = 1; i <= 7; i++) {{
                const btn = document.createElement('button');
                btn.className = 'step-btn';
                btn.innerHTML = `<span style="font-size:1rem;">${{stepsDesc[i].icon}}</span><br>${{stepsDesc[i].name}}`;
                btn.onclick = () => setStep(i);
                btnContainer.appendChild(btn);
            }}
            
            setStep(1);
            
            function render() {{
                requestAnimationFrame(render);
                controls.update();
                renderer.render(scene, camera);
            }}
            render();
            
            window.addEventListener('resize', () => {{
                camera.aspect = window.innerWidth / window.innerHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(window.innerWidth, window.innerHeight);
            }});
            
            window.playAll = playAll;
            window.resetView = resetView;
            window.toggleWireframe = toggleWireframe;
        </script>
    </body>
    </html>
    """
    return animation_html

def create_architecture_animation(arch_name):
    """亭台楼阁榭舫轩建筑动画 - 根据建筑类型生成专属3D模型"""
    
    arch_data = ARCHITECTURES[arch_name]
    
    if arch_name == "亭":
        steps_desc = {
            1: {"name": "台基", "desc": "筑造八角形台基，奠定建筑基础。", "icon": "⛰️"},
            2: {"name": "立柱", "desc": "竖立八根檐柱，形成柱网。柱高与柱径遵循古典比例。", "icon": "🌲"},
            3: {"name": "搭顶", "desc": "搭建攒尖顶木架，形成六角/八角形屋顶骨架。", "icon": "🏗️"},
            4: {"name": "铺瓦", "desc": "铺设青瓦，安装宝顶。亭顶优雅舒展。", "icon": "🏔️"},
            5: {"name": "落成", "desc": "亭子落成！四面临风，八面玲珑，是园林点景之精髓。", "icon": "🏯"}
        }
        model_params = {"type": "pavilion", "sides": 6, "height": 2.5, "radius": 1.8}
        
    elif arch_name == "台":
        steps_desc = {
            1: {"name": "筑基", "desc": "夯筑高台基础，层层夯实。台基高度决定建筑等级，一般为3-9米。", "icon": "⛰️"},
            2: {"name": "砌台", "desc": "包砌砖石，形成台壁。每层收分1/10，呈梯形断面，设须弥座装饰。", "icon": "🏗️"},
            3: {"name": "台阶", "desc": "铺设踏道，设垂带石。台阶每级高150mm，宽300mm，坡度30度。", "icon": "🚶"},
            4: {"name": "栏杆", "desc": "安装望柱栏杆，设寻杖、云拱。栏杆高900-1100mm，雕刻精美纹饰。", "icon": "🏛️"},
            5: {"name": "台面", "desc": "铺设台面石板，设排水坡度3-5%。台面宽阔平整，可容纳百人观演。", "icon": "🏔️"},
            6: {"name": "戏台", "desc": "搭建戏台木构，设前后台分隔。前台表演，后台化妆准备。", "icon": "🎭"},
            7: {"name": "屏风", "desc": "安装屏风，彩绘吉祥图案。屏风后设出将入相门，演员进出。", "icon": "🖼️"},
            8: {"name": "屋顶", "desc": "架设歇山式屋顶，飞檐翘角。屋顶铺设琉璃瓦，设脊兽装饰。", "icon": "🏔️"},
            9: {"name": "落成", "desc": "戏台落成！可上演戏曲，民间文化活动中心。", "icon": "🏯"}
        }
        model_params = {"type": "stage", "height": 3.0, "width": 8.0, "depth": 6.0}
        
    elif arch_name == "楼":
        steps_desc = {
            1: {"name": "台基", "desc": "筑造高台基，彰显建筑气势。", "icon": "⛰️"},
            2: {"name": "立柱", "desc": "竖立两层柱网，形成楼阁骨架。", "icon": "🌲"},
            3: {"name": "架梁", "desc": "搭建抬梁式木构架，形成二层楼阁。", "icon": "🏗️"},
            4: {"name": "铺作", "desc": "铺设斗拱层，出挑深远。", "icon": "⚙️"},
            5: {"name": "屋顶", "desc": "架设歇山式屋顶，飞檐翘角。", "icon": "🏔️"},
            6: {"name": "落成", "desc": "楼阁落成！可登高望远，极目楚天舒。", "icon": "🏯"}
        }
        model_params = {"type": "tower", "floors": 2, "height": 5.0, "width": 3.0, "depth": 2.5}
        
    elif arch_name == "阁":
        steps_desc = {
            1: {"name": "台基", "desc": "筑造石砌台基，防潮稳固。", "icon": "⛰️"},
            2: {"name": "立柱", "desc": "竖立内外两圈柱网。", "icon": "🌲"},
            3: {"name": "架梁", "desc": "搭建暗层结构，形成平座。", "icon": "🏗️"},
            4: {"name": "斗拱", "desc": "铺设繁复斗拱层，层层出跳。", "icon": "⚙️"},
            5: {"name": "屋顶", "desc": "架设重檐屋顶，气势恢宏。", "icon": "🏔️"},
            6: {"name": "落成", "desc": "楼阁落成！藏书万卷，传承文脉。", "icon": "🏯"}
        }
        model_params = {"type": "pavilion", "sides": 4, "height": 4.0, "radius": 2.0}
        
    elif arch_name == "榭":
        steps_desc = {
            1: {"name": "桩基", "desc": "打入木桩，深入水中。", "icon": "⛰️"},
            2: {"name": "平台", "desc": "搭建临水平台，悬挑出岸。", "icon": "🏗️"},
            3: {"name": "立柱", "desc": "竖立檐柱，形成开敞空间。", "icon": "🌲"},
            4: {"name": "屋顶", "desc": "架设卷棚歇山屋顶。", "icon": "🏔️"},
            5: {"name": "落成", "desc": "水榭落成！临水观鱼，赏荷听雨。", "icon": "🏯"}
        }
        model_params = {"type": "pavilion", "sides": 4, "height": 2.5, "radius": 2.0}
        
    elif arch_name == "舫":
        steps_desc = {
            1: {"name": "船身", "desc": "砌筑石砌船身，仿船形。", "icon": "⛰️"},
            2: {"name": "头舱", "desc": "搭建船头舱楼，设跳板。", "icon": "🏗️"},
            3: {"name": "中舱", "desc": "搭建中舱，为主要活动空间。", "icon": "🏔️"},
            4: {"name": "尾舱", "desc": "搭建尾舱，设舵楼。", "icon": "⚙️"},
            5: {"name": "落成", "desc": "石舫落成！不系之舟，象征自由超脱。", "icon": "🏯"}
        }
        model_params = {"type": "boat", "length": 5.0, "width": 1.5, "height": 2.0}
        
    elif arch_name == "轩":
        steps_desc = {
            1: {"name": "台基", "desc": "筑造低矮台基，亲近自然。", "icon": "⛰️"},
            2: {"name": "立柱", "desc": "竖立前檐柱，完全敞开。", "icon": "🌲"},
            3: {"name": "轩梁", "desc": "安装轩梁，形成弧形天花。", "icon": "🏗️"},
            4: {"name": "屋顶", "desc": "架设卷棚顶，轻盈舒展。", "icon": "🏔️"},
            5: {"name": "落成", "desc": "轩斋落成！幽静雅致，文人雅集之所。", "icon": "🏯"}
        }
        model_params = {"type": "pavilion", "sides": 4, "height": 2.8, "radius": 2.2}
        
    elif arch_name == "云南民族":
        steps_desc = {
            1: {"name": "选址", "desc": "依山傍水，因地制宜。傣族临水而居，彝族依山筑台，白族择平地建院。", "icon": "⛰️"},
            2: {"name": "筑基", "desc": "傣族打木桩、架空层；彝族夯土筑台；白族铺石垫层。基础形式因民族而异。", "icon": "🏗️"},
            3: {"name": "立柱", "desc": "傣族穿斗式木构架，柱间距2-3米；白族抬梁式构架，柱网规整。", "icon": "🌲"},
            4: {"name": "架梁", "desc": "安装梁枋、檩条。傣族竹篾绑扎，白族榫卯连接，彝族土坯墙承重。", "icon": "🏔️"},
            5: {"name": "围护", "desc": "傣族竹篾墙、木雕；白族白墙青瓦、照壁彩绘；彝族土坯墙、木雕窗。", "icon": "🎨"},
            6: {"name": "屋顶", "desc": "傣族歇山式、坡度陡；白族硬山顶、瓦屋面；彝族平顶、土掌房。", "icon": "🏔️"},
            7: {"name": "装饰", "desc": "傣族金水漏印、孔雀图案；白族水墨彩绘、木雕；彝族太阳历图腾、牛头装饰。", "icon": "✨"},
            8: {"name": "落成", "desc": "民族建筑落成！傣家竹楼、白族三坊一照壁、彝族土掌房，展现多元建筑智慧。", "icon": "🏯"}
        }
        model_params = {"type": "ethnic", "style": "dai"}

    else:
        steps_desc = {
            1: {"name": "奠基", "desc": "筑造台基，奠定基础。", "icon": "⛰️"},
            2: {"name": "立柱", "desc": "竖立柱网，形成框架。", "icon": "🌲"},
            3: {"name": "架梁", "desc": "搭建梁架，形成屋架。", "icon": "🏗️"},
            4: {"name": "屋顶", "desc": "架设屋顶，铺设瓦片。", "icon": "🏔️"},
            5: {"name": "落成", "desc": f"{arch_name}落成！{arch_data['struct']}", "icon": "🏯"}
        }
        model_params = {"type": "pavilion", "sides": 4, "height": 3.0, "radius": 2.0}
    
    animation_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ 
                background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
                overflow: hidden;
                font-family: 'Microsoft YaHei', monospace;
            }}
            #canvas-container {{ width: 100%; height: 100vh; }}
            #controls-panel {{
                position: absolute;
                bottom: 20px;
                left: 20px;
                right: 20px;
                background: rgba(0,0,0,0.85);
                backdrop-filter: blur(15px);
                border-radius: 20px;
                padding: 15px;
                z-index: 100;
                border: 1px solid rgba(255,215,150,0.3);
            }}
            .step-buttons {{ display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; margin-bottom: 10px; }}
            .step-btn {{
                background: linear-gradient(135deg, #2c3e50, #34495e);
                border: none; color: white; padding: 8px 16px; border-radius: 30px;
                cursor: pointer; font-size: 12px; font-weight: bold; transition: all 0.3s ease;
                min-width: 70px;
            }}
            .step-btn:hover, .step-btn.active {{
                background: linear-gradient(135deg, #8B4513, #A0522D);
                transform: translateY(-2px);
            }}
            .action-buttons {{ display: flex; justify-content: center; gap: 15px; margin-bottom: 10px; }}
            .action-btn {{
                background: rgba(255,255,255,0.2); border: 1px solid rgba(255,215,150,0.5);
                color: #ffd796; padding: 6px 16px; border-radius: 25px;
                cursor: pointer; font-size: 12px; transition: all 0.3s ease;
            }}
            .action-btn:hover {{ background: rgba(255,215,150,0.3); transform: scale(1.05); }}
            .step-desc {{ text-align: center; color: #ffd796; font-size: 13px; padding: 8px; background: rgba(0,0,0,0.5); border-radius: 10px; margin-top: 5px; }}
            .progress-bar {{ height: 3px; background: rgba(255,255,255,0.2); border-radius: 2px; overflow: hidden; margin: 8px 0; }}
            .progress-fill {{ height: 100%; background: linear-gradient(90deg, #FF6B6B, #4ECDC4); width: 0%; transition: width 0.3s ease; }}
            .stats {{ position: absolute; top: 20px; right: 20px; color: rgba(255,255,255,0.6); background: rgba(0,0,0,0.5); padding: 6px 12px; border-radius: 20px; font-size: 11px; pointer-events: none; z-index: 100; }}
            .title-info {{ position: absolute; top: 20px; left: 20px; color: #ffd796; background: rgba(0,0,0,0.5); padding: 8px 16px; border-radius: 20px; font-size: 14px; font-weight: bold; pointer-events: none; z-index: 100; }}
        </style>
    </head>
    <body>
        <div id="canvas-container"></div>
        <div class="title-info">🏯 {arch_name} · {arch_data['struct'][:40]}...</div>
        <div class="stats">进度: <span id="progress-text">0</span>%</div>
        <div id="controls-panel">
            <div class="step-buttons" id="step-buttons"></div>
            <div class="action-buttons">
                <button class="action-btn" onclick="playAll()">▶ 一键成形动画</button>
                <button class="action-btn" onclick="resetView()">🎥 重置视角</button>
                <button class="action-btn" onclick="toggleWireframe()">🔲 线框模式</button>
            </div>
            <div class="progress-bar"><div class="progress-fill" id="progress-fill"></div></div>
            <div class="step-desc" id="step-desc">点击步骤按钮，观看{arch_name}分步建造过程</div>
        </div>
        
        <script type="importmap">
            {{
                "imports": {{
                    "three": "https://unpkg.com/three@0.128.0/build/three.module.js",
                    "three/addons/": "https://unpkg.com/three@0.128.0/examples/jsm/"
                }}
            }}
        </script>
        
        <script type="module">
            import * as THREE from 'three';
            import {{ OrbitControls }} from 'three/addons/controls/OrbitControls.js';
            
            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0x0f0c29);
            scene.fog = new THREE.FogExp2(0x0f0c29, 0.008);
            
            const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
            camera.position.set(8, 5, 12);
            
            const renderer = new THREE.WebGLRenderer({{ antialias: true }});
            renderer.setSize(window.innerWidth, window.innerHeight);
            renderer.shadowMap.enabled = true;
            document.getElementById('canvas-container').appendChild(renderer.domElement);
            
            const controls = new OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;
            controls.target.set(0, 2, 0);
            
            const ambientLight = new THREE.AmbientLight(0x404040);
            scene.add(ambientLight);
            const mainLight = new THREE.DirectionalLight(0xfff5e6, 1.2);
            mainLight.position.set(5, 10, 7);
            mainLight.castShadow = true;
            scene.add(mainLight);
            const fillLight = new THREE.PointLight(0x88aaff, 0.5);
            fillLight.position.set(3, 4, 4);
            scene.add(fillLight);
            
            const gridHelper = new THREE.GridHelper(20, 20, 0x88aaff, 0x335588);
            gridHelper.position.y = -0.1;
            gridHelper.material.transparent = true;
            gridHelper.material.opacity = 0.3;
            scene.add(gridHelper);
            
            const buildingGroup = new THREE.Group();
            scene.add(buildingGroup);
            
            const woodMat = new THREE.MeshStandardMaterial({{ color: 0xCD853F, roughness: 0.5 }});
            const roofMat = new THREE.MeshStandardMaterial({{ color: 0x4a3a2a, roughness: 0.8 }});
            const stoneMat = new THREE.MeshStandardMaterial({{ color: 0x9B7B5C, roughness: 0.7 }});
            const platformMat = new THREE.MeshStandardMaterial({{ color: 0xBC9A6C, roughness: 0.7 }});
            const railingMat = new THREE.MeshStandardMaterial({{ color: 0xCD853F, roughness: 0.5 }});
            const screenMat = new THREE.MeshStandardMaterial({{ color: 0xB87333, roughness: 0.4, metalness: 0.2 }});
            const bambooMat = new THREE.MeshStandardMaterial({{ color: 0x9C7A4A, roughness: 0.8 }});
            const earthMat = new THREE.MeshStandardMaterial({{ color: 0xBC9A6C, roughness: 0.9 }});
            const whiteMat = new THREE.MeshStandardMaterial({{ color: 0xF5F5DC, roughness: 0.6 }});
            
            let components = [];
            let currentStep = 0;
            let animating = false;
            
            const stepsCount = {len(steps_desc)};
            const stepsDesc = {steps_desc};
            
            const modelParams = {json.dumps(model_params)};
            
            if (modelParams.type === 'stage') {{
                const stageHeight = modelParams.height || 2.5;
                const stageWidth = modelParams.width || 6.0;
                const stageDepth = modelParams.depth || 5.0;
                
                function generatePlatform(progress) {{
                    const layers = 3;
                    for (let l = 0; l < layers && l < progress * layers; l++) {{
                        const layerWidth = stageWidth * (1 - l * 0.1);
                        const layerDepth = stageDepth * (1 - l * 0.1);
                        const layerHeight = 0.35;
                        const platformGeo = new THREE.BoxGeometry(layerWidth, layerHeight, layerDepth);
                        const platform = new THREE.Mesh(platformGeo, stoneMat);
                        platform.position.set(0, l * layerHeight, 0);
                        platform.castShadow = true;
                        buildingGroup.add(platform);
                        components.push(platform);
                        
                        if (l === layers - 1) {{
                            const waistGeo = new THREE.BoxGeometry(layerWidth * 0.8, 0.15, layerDepth * 0.8);
                            const waist = new THREE.Mesh(waistGeo, new THREE.MeshStandardMaterial({{ color: 0xCD853F }}));
                            waist.position.set(0, l * layerHeight + layerHeight - 0.08, 0);
                            buildingGroup.add(waist);
                            components.push(waist);
                        }}
                    }}
                }}
                
                function generateSteps(progress) {{
                    if (progress <= 0) return;
                    const stepCount = 6;
                    const stepHeight = 0.15;
                    const stepWidth = 1.2;
                    const stepDepth = 0.3;
                    for (let i = 0; i < stepCount && i < progress * stepCount; i++) {{
                        const stepGeo = new THREE.BoxGeometry(stepWidth, stepHeight, stepDepth);
                        const step = new THREE.Mesh(stepGeo, stoneMat);
                        step.position.set(-stageWidth/3, i * stepHeight, stageDepth/2 + i * stepDepth);
                        step.castShadow = true;
                        buildingGroup.add(step);
                        components.push(step);
                    }}
                }}
                
                function generateRailings(progress) {{
                    if (progress <= 0) return;
                    const railingHeight = 0.9;
                    const railingThick = 0.12;
                    const startY = 3 * 0.35;
                    
                    const frontRailingGeo = new THREE.BoxGeometry(stageWidth, railingHeight * progress, railingThick);
                    const frontRailing = new THREE.Mesh(frontRailingGeo, railingMat);
                    frontRailing.position.set(0, startY + railingHeight/2, stageDepth/2);
                    buildingGroup.add(frontRailing);
                    components.push(frontRailing);
                    
                    const sideRailingGeo = new THREE.BoxGeometry(railingThick, railingHeight * progress, stageDepth);
                    const leftRailing = new THREE.Mesh(sideRailingGeo, railingMat);
                    leftRailing.position.set(-stageWidth/2, startY + railingHeight/2, 0);
                    buildingGroup.add(leftRailing);
                    components.push(leftRailing);
                    
                    const rightRailing = new THREE.Mesh(sideRailingGeo, railingMat);
                    rightRailing.position.set(stageWidth/2, startY + railingHeight/2, 0);
                    buildingGroup.add(rightRailing);
                    components.push(rightRailing);
                    
                    const pillarGeo = new THREE.BoxGeometry(0.15, 0.25, 0.15);
                    const pillarMat = new THREE.MeshStandardMaterial({{ color: 0xffaa66 }});
                    for (let i = -3; i <= 3; i++) {{
                        const pillar = new THREE.Mesh(pillarGeo, pillarMat);
                        pillar.position.set(i * 0.8, startY + railingHeight, stageDepth/2);
                        buildingGroup.add(pillar);
                        components.push(pillar);
                    }}
                }}
                
                function generateStageFrame(progress) {{
                    if (progress <= 0) return;
                    const startY = 3 * 0.35 + 0.9;
                    const columns = 4;
                    for (let i = 0; i < columns && i < progress * columns; i++) {{
                        const colGeo = new THREE.CylinderGeometry(0.2, 0.25, 2.5, 8);
                        const column = new THREE.Mesh(colGeo, woodMat);
                        const x = -stageWidth/2 + i * stageWidth/(columns-1);
                        column.position.set(x, startY + 1.25, 0);
                        column.castShadow = true;
                        buildingGroup.add(column);
                        components.push(column);
                    }}
                }}
                
                function generateScreen(progress) {{
                    if (progress <= 0) return;
                    const screenWidth = stageWidth * 0.7;
                    const screenHeight = 2.0;
                    const screenGeo = new THREE.BoxGeometry(screenWidth * progress, screenHeight * progress, 0.1);
                    const screen = new THREE.Mesh(screenGeo, screenMat);
                    screen.position.set(0, 3 * 0.35 + 0.9 + 1.0, -stageDepth/3);
                    buildingGroup.add(screen);
                    components.push(screen);
                    
                    if (progress >= 0.8) {{
                        const doorGeo = new THREE.BoxGeometry(0.8, 1.2, 0.05);
                        const leftDoor = new THREE.Mesh(doorGeo, new THREE.MeshStandardMaterial({{ color: 0xffaa66 }}));
                        leftDoor.position.set(-1.2, 3 * 0.35 + 0.9 + 0.8, -stageDepth/3 + 0.06);
                        buildingGroup.add(leftDoor);
                        components.push(leftDoor);
                        
                        const rightDoor = new THREE.Mesh(doorGeo, new THREE.MeshStandardMaterial({{ color: 0xffaa66 }}));
                        rightDoor.position.set(1.2, 3 * 0.35 + 0.9 + 0.8, -stageDepth/3 + 0.06);
                        buildingGroup.add(rightDoor);
                        components.push(rightDoor);
                    }}
                }}
                
                function generateRoof(progress) {{
                    if (progress <= 0) return;
                    const roofWidth = stageWidth + 0.8;
                    const roofDepth = stageDepth + 0.8;
                    const roofHeightVal = 1.2 * progress;
                    const roofGeo = new THREE.ConeGeometry(roofWidth/2, roofHeightVal, 4);
                    const roof = new THREE.Mesh(roofGeo, roofMat);
                    roof.position.set(0, 3 * 0.35 + 0.9 + 2.5, 0);
                    roof.castShadow = true;
                    buildingGroup.add(roof);
                    components.push(roof);
                    
                    if (progress >= 0.9) {{
                        const ridgeGeo = new THREE.BoxGeometry(roofWidth, 0.08, 0.2);
                        const ridge = new THREE.Mesh(ridgeGeo, new THREE.MeshStandardMaterial({{ color: 0xffaa66 }}));
                        ridge.position.set(0, 3 * 0.35 + 0.9 + 2.5 + roofHeightVal, 0);
                        buildingGroup.add(ridge);
                        components.push(ridge);
                    }}
                }}
                
                function addDecorations() {{
                    const lanternGeo = new THREE.SphereGeometry(0.2, 16, 16);
                    const lanternMat = new THREE.MeshStandardMaterial({{ color: 0xff6666, emissive: 0x442222 }});
                    for (let i = -2; i <= 2; i++) {{
                        const lantern = new THREE.Mesh(lanternGeo, lanternMat);
                        lantern.position.set(i * 1.2, 3 * 0.35 + 1.5, stageDepth/2 + 0.3);
                        buildingGroup.add(lantern);
                        components.push(lantern);
                    }}
                }}
                
                function updateBuilding(step) {{
                    components.forEach(comp => buildingGroup.remove(comp));
                    components = [];
                    if (step >= 1) generatePlatform(1);
                    if (step >= 2) generatePlatform(1);
                    if (step >= 3) generateSteps(step === 3 ? 1 : 1);
                    if (step >= 4) generateRailings(step === 4 ? 1 : 1);
                    if (step >= 5) generateStageFrame(step === 5 ? 1 : 1);
                    if (step >= 6) generateScreen(step === 6 ? 1 : 1);
                    if (step >= 7) generateRoof(step === 7 ? 0.7 : (step >= 8 ? 1 : 0.7));
                    if (step >= 8) generateRoof(1);
                    if (step >= 9) addDecorations();
                    
                    const progressPercent = (step / stepsCount) * 100;
                    document.getElementById('progress-fill').style.width = progressPercent + '%';
                    document.getElementById('progress-text').textContent = Math.floor(progressPercent);
                    
                    if (stepsDesc[step]) {{
                        document.getElementById('step-desc').innerHTML = `<strong>${{stepsDesc[step].icon}} ${{stepsDesc[step].name}}</strong><br>${{stepsDesc[step].desc}}`;
                    }}
                }}
                
                window.updateBuilding = updateBuilding;
                window.setStep = function(step) {{
                    currentStep = step;
                    updateBuilding(step);
                    document.querySelectorAll('.step-btn').forEach((btn, idx) => {{
                        if (idx + 1 === step) btn.classList.add('active');
                        else btn.classList.remove('active');
                    }});
                }};
                
                window.playAll = function() {{
                    if (animating) return;
                    animating = true;
                    let step = 1;
                    function animateStep() {{
                        if (step <= stepsCount) {{
                            window.setStep(step);
                            step++;
                            setTimeout(animateStep, 500);
                        }} else {{
                            animating = false;
                        }}
                    }}
                    animateStep();
                }};
                
                window.resetView = function() {{
                    camera.position.set(10, 6, 12);
                    controls.target.set(0, 2, 0);
                    controls.update();
                }};
                
                window.toggleWireframe = function() {{
                    components.forEach(comp => {{
                        if (comp.isMesh && comp.material) {{
                            if (Array.isArray(comp.material)) comp.material.forEach(m => m.wireframe = !m.wireframe);
                            else comp.material.wireframe = !comp.material.wireframe;
                        }}
                    }});
                }};
                
                const btnContainer = document.getElementById('step-buttons');
                for (let i = 1; i <= stepsCount; i++) {{
                    const btn = document.createElement('button');
                    btn.className = 'step-btn';
                    btn.innerHTML = `<span style="font-size:1rem;">${{stepsDesc[i].icon}}</span><br>${{stepsDesc[i].name}}`;
                    btn.onclick = () => window.setStep(i);
                    btnContainer.appendChild(btn);
                }}
                
                window.setStep(1);
                
            }} else if (modelParams.type === 'ethnic') {{
                const width = 4.0;
                const depth = 4.0;
                const columnHeight = 2.2;
                const roofHeight = 1.2;
                
                function generatePlatform(progress) {{
                    const platformGeo = new THREE.BoxGeometry(width + 0.5, 0.2 * progress, depth + 0.5);
                    const platform = new THREE.Mesh(platformGeo, stoneMat);
                    platform.position.set(0, -0.1 * progress, 0);
                    buildingGroup.add(platform);
                    components.push(platform);
                }}
                
                function generateColumns(progress) {{
                    const positions = [
                        [-1.2, -1.2], [1.2, -1.2], [1.2, 1.2], [-1.2, 1.2],
                        [-0.6, -0.6], [0.6, -0.6], [0.6, 0.6], [-0.6, 0.6]
                    ];
                    const totalCols = positions.length;
                    const target = Math.floor(totalCols * progress);
                    for (let i = 0; i < target && i < totalCols; i++) {{
                        const [x, z] = positions[i];
                        const colGeo = new THREE.CylinderGeometry(0.15, 0.18, columnHeight, 6);
                        const column = new THREE.Mesh(colGeo, woodMat);
                        column.position.set(x, columnHeight/2, z);
                        column.castShadow = true;
                        buildingGroup.add(column);
                        components.push(column);
                    }}
                }}
                
                function generateBeams(progress) {{
                    if (progress <= 0) return;
                    const beamCount = 4;
                    const target = Math.floor(beamCount * progress);
                    const beamPositions = [[-1.5, 1.0], [1.5, 1.0], [0, -1.5], [0, 1.5]];
                    for (let i = 0; i < target && i < beamCount; i++) {{
                        const [x, z] = beamPositions[i];
                        const beamGeo = new THREE.BoxGeometry(3.0, 0.15, 0.3);
                        const beam = new THREE.Mesh(beamGeo, woodMat);
                        beam.position.set(x, columnHeight - 0.1, z);
                        buildingGroup.add(beam);
                        components.push(beam);
                    }}
                }}
                
                function generateWalls(progress) {{
                    if (progress <= 0) return;
                    const wallMat = modelParams.style === 'dai' ? bambooMat : (modelParams.style === 'yi' ? earthMat : whiteMat);
                    const wallHeight = 1.8;
                    const wallGeo = new THREE.BoxGeometry(width - 0.4, wallHeight * progress, 0.15);
                    const backWall = new THREE.Mesh(wallGeo, wallMat);
                    backWall.position.set(0, wallHeight/2, -depth/2 + 0.1);
                    buildingGroup.add(backWall);
                    components.push(backWall);
                    
                    const leftWallGeo = new THREE.BoxGeometry(0.15, wallHeight * progress, depth - 0.4);
                    const leftWall = new THREE.Mesh(leftWallGeo, wallMat);
                    leftWall.position.set(-width/2 + 0.1, wallHeight/2, 0);
                    buildingGroup.add(leftWall);
                    components.push(leftWall);
                    
                    const rightWall = new THREE.Mesh(leftWallGeo, wallMat);
                    rightWall.position.set(width/2 - 0.1, wallHeight/2, 0);
                    buildingGroup.add(rightWall);
                    components.push(rightWall);
                }}
                
                function generateRoof(progress) {{
                    const roofWidth = width + 0.8;
                    const roofDepth = depth + 0.8;
                    const roofGeo = new THREE.ConeGeometry(roofWidth/2, roofHeight * progress, 4);
                    const roof = new THREE.Mesh(roofGeo, roofMat);
                    roof.position.set(0, columnHeight, 0);
                    roof.castShadow = true;
                    buildingGroup.add(roof);
                    components.push(roof);
                    
                    if (progress >= 0.8 && modelParams.style === 'bai') {{
                        const screenGeo = new THREE.BoxGeometry(2.5, 1.8, 0.1);
                        const screen = new THREE.Mesh(screenGeo, new THREE.MeshStandardMaterial({{ color: 0xFFFFFF }}));
                        screen.position.set(0, 1.0, depth/2 + 0.2);
                        buildingGroup.add(screen);
                        components.push(screen);
                    }}
                }}
                
                function addDecorations() {{
                    const decoMat = new THREE.MeshStandardMaterial({{ color: 0xffaa66 }});
                    const decoGeo = new THREE.SphereGeometry(0.12, 8, 8);
                    for (let i = -2; i <= 2; i++) {{
                        const deco = new THREE.Mesh(decoGeo, decoMat);
                        deco.position.set(i * 0.8, columnHeight - 0.2, depth/2 - 0.1);
                        buildingGroup.add(deco);
                        components.push(deco);
                    }}
                }}
                
                function updateBuilding(step) {{
                    components.forEach(comp => buildingGroup.remove(comp));
                    components = [];
                    if (step >= 1) generatePlatform(1);
                    if (step >= 2) generateColumns(1);
                    if (step >= 3) generateBeams(step === 3 ? 0.5 : 1);
                    if (step >= 4) generateBeams(1);
                    if (step >= 5) generateWalls(step === 5 ? 0.7 : 1);
                    if (step >= 6) generateRoof(step === 6 ? 0.6 : (step >= 7 ? 1 : 0.6));
                    if (step >= 7) generateRoof(1);
                    if (step >= 8) addDecorations();
                    
                    const progressPercent = (step / stepsCount) * 100;
                    document.getElementById('progress-fill').style.width = progressPercent + '%';
                    document.getElementById('progress-text').textContent = Math.floor(progressPercent);
                    
                    if (stepsDesc[step]) {{
                        document.getElementById('step-desc').innerHTML = `<strong>${{stepsDesc[step].icon}} ${{stepsDesc[step].name}}</strong><br>${{stepsDesc[step].desc}}`;
                    }}
                }}
                
                window.updateBuilding = updateBuilding;
                window.setStep = function(step) {{
                    currentStep = step;
                    updateBuilding(step);
                    document.querySelectorAll('.step-btn').forEach((btn, idx) => {{
                        if (idx + 1 === step) btn.classList.add('active');
                        else btn.classList.remove('active');
                    }});
                }};
                
                window.playAll = function() {{
                    if (animating) return;
                    animating = true;
                    let step = 1;
                    function animateStep() {{
                        if (step <= stepsCount) {{
                            window.setStep(step);
                            step++;
                            setTimeout(animateStep, 500);
                        }} else {{
                            animating = false;
                        }}
                    }}
                    animateStep();
                }};
                
                window.resetView = function() {{
                    camera.position.set(8, 5, 12);
                    controls.target.set(0, 2, 0);
                    controls.update();
                }};
                
                window.toggleWireframe = function() {{
                    components.forEach(comp => {{
                        if (comp.isMesh && comp.material) {{
                            if (Array.isArray(comp.material)) comp.material.forEach(m => m.wireframe = !m.wireframe);
                            else comp.material.wireframe = !comp.material.wireframe;
                        }}
                    }});
                }};
                
                const btnContainer = document.getElementById('step-buttons');
                for (let i = 1; i <= stepsCount; i++) {{
                    const btn = document.createElement('button');
                    btn.className = 'step-btn';
                    btn.innerHTML = `<span style="font-size:1rem;">${{stepsDesc[i].icon}}</span><br>${{stepsDesc[i].name}}`;
                    btn.onclick = () => window.setStep(i);
                    btnContainer.appendChild(btn);
                }}
                
                window.setStep(1);
                
            }} else {{
                function generatePlatform(progress) {{
                    const baseW = modelParams.type === 'boat' ? 1.5 : 2.5;
                    const baseD = modelParams.type === 'boat' ? 5.0 : 2.5;
                    const platformGeo = new THREE.BoxGeometry(baseW * progress, 0.2 * progress, baseD * progress);
                    const platform = new THREE.Mesh(platformGeo, platformMat);
                    platform.position.set(0, -0.1 * progress, 0);
                    platform.castShadow = true;
                    buildingGroup.add(platform);
                    components.push(platform);
                }}
                
                function generateColumns(progress) {{
                    const radius = modelParams.radius || 0.25;
                    const height = modelParams.height || 2.5;
                    const sides = modelParams.sides || 4;
                    const angleStep = (Math.PI * 2) / sides;
                    for (let i = 0; i < sides && i < progress * sides; i++) {{
                        const angle = i * angleStep;
                        const x = Math.cos(angle) * radius;
                        const z = Math.sin(angle) * radius;
                        const colGeo = new THREE.CylinderGeometry(0.12, 0.15, height, 8);
                        const column = new THREE.Mesh(colGeo, woodMat);
                        column.position.set(x, height/2, z);
                        column.castShadow = true;
                        buildingGroup.add(column);
                        components.push(column);
                    }}
                }}
                
                function generateRoof(progress) {{
                    const radius = (modelParams.radius || 1.8) + 0.3;
                    const roofHeight = 1.2 * progress;
                    const coneGeo = new THREE.ConeGeometry(radius, roofHeight, 16);
                    const roof = new THREE.Mesh(coneGeo, roofMat);
                    roof.position.set(0, (modelParams.height || 2.5), 0);
                    roof.castShadow = true;
                    buildingGroup.add(roof);
                    components.push(roof);
                    
                    if (progress >= 0.9) {{
                        const topGeo = new THREE.SphereGeometry(0.12, 8, 8);
                        const topMat = new THREE.MeshStandardMaterial({{ color: 0xffaa66 }});
                        const top = new THREE.Mesh(topGeo, topMat);
                        top.position.set(0, (modelParams.height || 2.5) + roofHeight, 0);
                        buildingGroup.add(top);
                        components.push(top);
                    }}
                }}
                
                function generateFloors(progress) {{
                    if (modelParams.type !== 'tower') return;
                    const width = modelParams.width || 2.5;
                    const depth = modelParams.depth || 2.0;
                    const floorHeight = 1.5;
                    for (let f = 0; f < 2 && f < progress * 2; f++) {{
                        const floorGeo = new THREE.BoxGeometry(width * (1 - f*0.1), 0.1, depth * (1 - f*0.1));
                        const floor = new THREE.Mesh(floorGeo, woodMat);
                        floor.position.set(0, 1.0 + f * floorHeight, 0);
                        floor.castShadow = true;
                        buildingGroup.add(floor);
                        components.push(floor);
                        
                        const columnGeo = new THREE.CylinderGeometry(0.1, 0.12, 1.2, 6);
                        for (let i = 0; i < 4; i++) {{
                            const x = (i % 2 === 0 ? 1 : -1) * width * 0.4;
                            const z = (i < 2 ? 1 : -1) * depth * 0.4;
                            const column = new THREE.Mesh(columnGeo, woodMat);
                            column.position.set(x, 0.6 + f * floorHeight, z);
                            column.castShadow = true;
                            buildingGroup.add(column);
                            components.push(column);
                        }}
                    }}
                }}
                
                function addDecorations() {{
                    const radius = (modelParams.radius || 1.8) + 0.3;
                    const ornamentGeo = new THREE.SphereGeometry(0.08, 6, 6);
                    const ornamentMat = new THREE.MeshStandardMaterial({{ color: 0xffaa66 }});
                    for (let i = 0; i < 4; i++) {{
                        const angle = i * Math.PI / 2;
                        const x = Math.cos(angle) * radius;
                        const z = Math.sin(angle) * radius;
                        const ornament = new THREE.Mesh(ornamentGeo, ornamentMat);
                        ornament.position.set(x, (modelParams.height || 2.5) + 0.8, z);
                        buildingGroup.add(ornament);
                        components.push(ornament);
                    }}
                }}
                
                function updateBuilding(step) {{
                    components.forEach(comp => buildingGroup.remove(comp));
                    components = [];
                    if (step >= 1) generatePlatform(1);
                    if (step >= 2) generateColumns(1);
                    if (step >= 3) {{
                        if (modelParams.type === 'tower') generateFloors(1);
                        else generateRoof(0.6);
                    }}
                    if (step >= 4) generateRoof(1);
                    if (step >= 5) addDecorations();
                    
                    const progressPercent = (step / stepsCount) * 100;
                    document.getElementById('progress-fill').style.width = progressPercent + '%';
                    document.getElementById('progress-text').textContent = Math.floor(progressPercent);
                    
                    if (stepsDesc[step]) {{
                        document.getElementById('step-desc').innerHTML = `<strong>${{stepsDesc[step].icon}} ${{stepsDesc[step].name}}</strong><br>${{stepsDesc[step].desc}}`;
                    }}
                }}
                
                window.updateBuilding = updateBuilding;
                window.setStep = function(step) {{
                    currentStep = step;
                    updateBuilding(step);
                    document.querySelectorAll('.step-btn').forEach((btn, idx) => {{
                        if (idx + 1 === step) btn.classList.add('active');
                        else btn.classList.remove('active');
                    }});
                }};
                
                window.playAll = function() {{
                    if (animating) return;
                    animating = true;
                    let step = 1;
                    function animateStep() {{
                        if (step <= stepsCount) {{
                            window.setStep(step);
                            step++;
                            setTimeout(animateStep, 500);
                        }} else {{
                            animating = false;
                        }}
                    }}
                    animateStep();
                }};
                
                window.resetView = function() {{
                    camera.position.set(6, 4, 8);
                    controls.target.set(0, 2, 0);
                    controls.update();
                }};
                
                window.toggleWireframe = function() {{
                    components.forEach(comp => {{
                        if (comp.isMesh && comp.material) {{
                            if (Array.isArray(comp.material)) comp.material.forEach(m => m.wireframe = !m.wireframe);
                            else comp.material.wireframe = !comp.material.wireframe;
                        }}
                    }});
                }};
                
                const btnContainer = document.getElementById('step-buttons');
                for (let i = 1; i <= stepsCount; i++) {{
                    const btn = document.createElement('button');
                    btn.className = 'step-btn';
                    btn.innerHTML = `<span style="font-size:1rem;">${{stepsDesc[i].icon}}</span><br>${{stepsDesc[i].name}}`;
                    btn.onclick = () => window.setStep(i);
                    btnContainer.appendChild(btn);
                }}
                
                window.setStep(1);
            }}
            
            function render() {{
                requestAnimationFrame(render);
                controls.update();
                renderer.render(scene, camera);
            }}
            render();
            
            window.addEventListener('resize', () => {{
                camera.aspect = window.innerWidth / window.innerHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(window.innerWidth, window.innerHeight);
            }});
        </script>
    </body>
    </html>
    """
    return animation_html

def analyze_architecture_image(image_bytes):
    """AI图片识别分析"""
    try:
        img = Image.open(BytesIO(image_bytes))
        img_array = np.array(img.convert('L'))
        height, width = img_array.shape
        aspect_ratio = width / height
        
        grad_x = np.gradient(img_array, axis=1)
        grad_y = np.gradient(img_array, axis=0)
        edge_density = np.mean(np.abs(grad_x) + np.abs(grad_y)) / 255
        
        top_half = img_array[:height//3, :]
        roof_intensity = np.mean(top_half)
        
        if aspect_ratio > 1.5:
            building_type = "楼阁"
            confidence = 0.75
            description = "图像呈现高耸的竖向构图，可能为多层楼阁建筑，如黄鹤楼、滕王阁等。"
        elif edge_density > 0.25:
            building_type = "殿堂"
            confidence = 0.7
            description = "图像中屋顶线条明显，轮廓清晰，可能为殿堂建筑，如太和殿、隆兴寺等。"
        elif roof_intensity < 100:
            building_type = "亭榭"
            confidence = 0.65
            description = "屋顶较暗且轮廓分明，可能为开敞式亭榭建筑，常见于园林之中。"
        else:
            building_type = "民居"
            confidence = 0.6
            description = "建筑形态朴素，可能为传统民居建筑，如四合院、徽派民居等。"
        
        if edge_density > 0.3:
            roof_style = "庑殿顶/歇山顶"
        elif edge_density > 0.2:
            roof_style = "悬山顶/硬山顶"
        else:
            roof_style = "攒尖顶/卷棚顶"
        
        return {
            "type": building_type,
            "confidence": confidence,
            "description": description,
            "aspect_ratio": f"{aspect_ratio:.2f}",
            "edge_density": f"{edge_density:.2f}",
            "roof_style": roof_style,
            "features": [
                f"图像尺寸: {width}x{height}",
                f"长宽比: {aspect_ratio:.2f}",
                f"纹理复杂度: {'高' if edge_density > 0.25 else '中' if edge_density > 0.15 else '低'}",
                f"推测屋顶: {roof_style}"
            ]
        }
    except Exception as e:
        return {
            "type": "未知",
            "confidence": 0.3,
            "description": f"分析失败: {str(e)}",
            "aspect_ratio": "N/A",
            "edge_density": "N/A",
            "roof_style": "未知",
            "features": ["无法识别"]
        }

# ========== 页面路由 ==========
# 1. 首页
if st.session_state.page == 'home':
    st.markdown('<div class="main-header">🏯 中国古代建筑数学建模交互式平台</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="intro-text">
        中国古建筑是世界建筑史上的瑰宝，融合了精湛的工艺、深厚的文化和严谨的数学逻辑。<br>
        本平台基于《营造法式》《工程做法则例》等12部古代建筑典籍，结合现代数学建模方法，<br>
        实现了中国古代建筑的数字化设计、3D建造模拟与智能分析。
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align:center; color:#fff; margin:3rem 0 2rem 0;'>平台核心模块</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="button-container">
            <div class="circle-btn">
                <div class="circle-icon">🏯</div>
                <div>古典建筑</div>
                <div style="font-size:0.9rem; margin-top:5px;">亭台楼阁</div>
            </div>
        </div>
        <div class="btn-caption">探索中国传统建筑类型</div>
        """, unsafe_allow_html=True)
        
        if st.button("进入古典建筑模块", key="m1_home", use_container_width=True):
            st.session_state.page = 'module1'
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="button-container">
            <div class="circle-btn">
                <div class="circle-icon">📜</div>
                <div>营造制度</div>
                <div style="font-size:0.9rem; margin-top:5px;">12种体系</div>
            </div>
        </div>
        <div class="btn-caption">历代建筑模数制度</div>
        """, unsafe_allow_html=True)
        
        if st.button("进入营造制度模块", key="m2_home", use_container_width=True):
            st.session_state.page = 'module2'
            st.session_state.module2_subpage = 'timeline'
            st.session_state.module2_system = None
            st.rerun()
    
    with col3:
        st.markdown("""
        <div class="button-container">
            <div class="circle-btn">
                <div class="circle-icon">📐</div>
                <div>数学建模</div>
                <div style="font-size:0.9rem; margin-top:5px;">3D模拟</div>
            </div>
        </div>
        <div class="btn-caption">AI数字孪生建造模拟</div>
        """, unsafe_allow_html=True)
        
        if st.button("进入数学建模模块", key="m3_home", use_container_width=True):
            st.session_state.page = 'module3'
            st.rerun()
    
    with col4:
        st.markdown("""
        <div class="button-container">
            <div class="circle-btn">
                <div class="circle-icon">🔬</div>
                <div>智能设计</div>
                <div style="font-size:0.9rem; margin-top:5px;">AI分析</div>
            </div>
        </div>
        <div class="btn-caption">智能参数化设计</div>
        """, unsafe_allow_html=True)
        
        if st.button("进入智能设计模块", key="m4_home", use_container_width=True):
            st.session_state.page = 'module4'
            st.rerun()
    
    st.markdown('<div class="sub-header">✨ 平台特色</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3>📚 12大营造体系</h3>
            <p>涵盖唐、宋、辽、金、元、明、清、西夏、藏、高句丽、渤海、南诏大理等12种古代建筑模数体系</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3>🎬 AI数学建模建造</h3>
            <p>分步动画 + 一键成形，电影级3D可视化，从台基到屋脊完整展现古建筑建造过程</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card">
            <h3>🔧 AI图片识别</h3>
            <p>上传古建筑图片，AI自动识别建筑类型、屋顶样式、结构特征，生成分析报告</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="footer-text">
        ⚡ 点击上方圆形按钮进入各功能模块 ⚡
    </div>
    """, unsafe_allow_html=True)

# 2. 模块一：古典建筑
elif st.session_state.page == 'module1':
    back_btn()
    st.markdown('<script>window.scrollTo(0, 0);</script>', unsafe_allow_html=True)
    st.markdown('<div class="main-header">🏯 中国古典建筑 · 亭台楼阁榭舫轩 + 云南民族建筑</div>', unsafe_allow_html=True)
    
    # 第一层：8个卡片
    if st.session_state.detail is None:
        st.markdown("""
        <div class="intro-text">
            中国传统建筑类型丰富多样，亭之玲珑、台之雄壮、楼之巍峨、阁之玲珑、榭之清雅、舫之飘逸、轩之幽静，<br>
            云南民族建筑更是融合了傣族、白族、彝族等多元民族的建筑智慧，各具特色，共同构成了中国古典园林建筑的完美画卷。<br>
            点击下方图片，深入了解每一种建筑类型。
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<h2 style='text-align:center; color:#fff; margin:2rem 0;'>八种经典建筑形式</h2>", unsafe_allow_html=True)
        
        # 第一行：亭、台、楼、阁
        col1, col2, col3, col4 = st.columns(4)
        
        names = list(ARCHITECTURES.keys())
        
        with col1:
            n = names[0]  # 亭
            img_base64 = get_image_base64(ARCHITECTURES[n]["img_path"])
            if img_base64:
                st.markdown(f"""
                <div class="architecture-card">
                    <img src="data:image/png;base64,{img_base64}" class="architecture-img">
                    <div class="architecture-title">{n}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="architecture-card">
                    <div style="height:220px; background: linear-gradient(135deg, #667eea, #764ba2); display:flex; align-items:center; justify-content:center; color:white; font-size:3rem;">{n}</div>
                    <div class="architecture-title">{n}</div>
                </div>
                """, unsafe_allow_html=True)
            if st.button(f"查看{n}详情", key=f"card_{n}_1", use_container_width=True):
                st.session_state.detail = n
                st.rerun()
        
        with col2:
            n = names[1]  # 台
            img_base64 = get_image_base64(ARCHITECTURES[n]["img_path"])
            if img_base64:
                st.markdown(f"""
                <div class="architecture-card">
                    <img src="data:image/png;base64,{img_base64}" class="architecture-img">
                    <div class="architecture-title">{n}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="architecture-card">
                    <div style="height:220px; background: linear-gradient(135deg, #667eea, #764ba2); display:flex; align-items:center; justify-content:center; color:white; font-size:3rem;">{n}</div>
                    <div class="architecture-title">{n}</div>
                </div>
                """, unsafe_allow_html=True)
            if st.button(f"查看{n}详情", key=f"card_{n}_2", use_container_width=True):
                st.session_state.detail = n
                st.rerun()
        
        with col3:
            n = names[2]  # 楼
            img_base64 = get_image_base64(ARCHITECTURES[n]["img_path"])
            if img_base64:
                st.markdown(f"""
                <div class="architecture-card">
                    <img src="data:image/png;base64,{img_base64}" class="architecture-img">
                    <div class="architecture-title">{n}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="architecture-card">
                    <div style="height:220px; background: linear-gradient(135deg, #667eea, #764ba2); display:flex; align-items:center; justify-content:center; color:white; font-size:3rem;">{n}</div>
                    <div class="architecture-title">{n}</div>
                </div>
                """, unsafe_allow_html=True)
            if st.button(f"查看{n}详情", key=f"card_{n}_3", use_container_width=True):
                st.session_state.detail = n
                st.rerun()
        
        with col4:
            n = names[3]  # 阁
            img_base64 = get_image_base64(ARCHITECTURES[n]["img_path"])
            if img_base64:
                st.markdown(f"""
                <div class="architecture-card">
                    <img src="data:image/png;base64,{img_base64}" class="architecture-img">
                    <div class="architecture-title">{n}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="architecture-card">
                    <div style="height:220px; background: linear-gradient(135deg, #667eea, #764ba2); display:flex; align-items:center; justify-content:center; color:white; font-size:3rem;">{n}</div>
                    <div class="architecture-title">{n}</div>
                </div>
                """, unsafe_allow_html=True)
            if st.button(f"查看{n}详情", key=f"card_{n}_4", use_container_width=True):
                st.session_state.detail = n
                st.rerun()
        
        # 第二行：榭、舫、轩、云南民族
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            n = names[4]  # 榭
            img_base64 = get_image_base64(ARCHITECTURES[n]["img_path"])
            if img_base64:
                st.markdown(f"""
                <div class="architecture-card">
                    <img src="data:image/png;base64,{img_base64}" class="architecture-img">
                    <div class="architecture-title">{n}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="architecture-card">
                    <div style="height:220px; background: linear-gradient(135deg, #667eea, #764ba2); display:flex; align-items:center; justify-content:center; color:white; font-size:3rem;">{n}</div>
                    <div class="architecture-title">{n}</div>
                </div>
                """, unsafe_allow_html=True)
            if st.button(f"查看{n}详情", key=f"card_{n}_5", use_container_width=True):
                st.session_state.detail = n
                st.rerun()
        
        with col2:
            n = names[5]  # 舫
            img_base64 = get_image_base64(ARCHITECTURES[n]["img_path"])
            if img_base64:
                st.markdown(f"""
                <div class="architecture-card">
                    <img src="data:image/png;base64,{img_base64}" class="architecture-img">
                    <div class="architecture-title">{n}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="architecture-card">
                    <div style="height:220px; background: linear-gradient(135deg, #667eea, #764ba2); display:flex; align-items:center; justify-content:center; color:white; font-size:3rem;">{n}</div>
                    <div class="architecture-title">{n}</div>
                </div>
                """, unsafe_allow_html=True)
            if st.button(f"查看{n}详情", key=f"card_{n}_6", use_container_width=True):
                st.session_state.detail = n
                st.rerun()
        
        with col3:
            n = names[6]  # 轩
            img_base64 = get_image_base64(ARCHITECTURES[n]["img_path"])
            if img_base64:
                st.markdown(f"""
                <div class="architecture-card">
                    <img src="data:image/png;base64,{img_base64}" class="architecture-img">
                    <div class="architecture-title">{n}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="architecture-card">
                    <div style="height:220px; background: linear-gradient(135deg, #667eea, #764ba2); display:flex; align-items:center; justify-content:center; color:white; font-size:3rem;">{n}</div>
                    <div class="architecture-title">{n}</div>
                </div>
                """, unsafe_allow_html=True)
            if st.button(f"查看{n}详情", key=f"card_{n}_7", use_container_width=True):
                st.session_state.detail = n
                st.rerun()
        
        with col4:
            n = names[7]  # 云南民族
            img_base64 = get_image_base64(ARCHITECTURES[n]["img_path"])
            if img_base64:
                st.markdown(f"""
                <div class="architecture-card">
                    <img src="data:image/png;base64,{img_base64}" class="architecture-img">
                    <div class="architecture-title">{n}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="architecture-card">
                    <div style="height:220px; background: linear-gradient(135deg, #667eea, #764ba2); display:flex; align-items:center; justify-content:center; color:white; font-size:3rem;">{n}</div>
                    <div class="architecture-title">{n}</div>
                </div>
                """, unsafe_allow_html=True)
            if st.button(f"查看{n}详情", key=f"card_{n}_8", use_container_width=True):
                st.session_state.detail = n
                st.rerun()
    
    # 第二层：云南民族总览（展示6个民族卡片，上3下3布局）
    elif st.session_state.detail == "云南民族":
        st.markdown(f'<div class="detail-title">🏘️ 云南民族建筑大观</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="intro-text">
            云南是中国民族最多的省份，各民族在长期的生产生活中创造了丰富多彩的建筑形式。<br>
            傣家竹楼、白族三坊一照壁、彝族土掌房、哈尼族蘑菇房、纳西族四合院、独龙族木楞房，各具特色，异彩纷呈。<br>
            点击下方卡片，深入了解每一种民族建筑。
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<h2 style='text-align:center; color:#fff; margin:2rem 0;'>六大民族建筑形式</h2>", unsafe_allow_html=True)
        
        # 显示6个民族建筑卡片（上3下3）
        ethnic_names = list(YUNNAN_ETHNIC_HOUSES.keys())
        
        # 第一行：3个
        col1, col2, col3 = st.columns(3)
        
        with col1:
            name = ethnic_names[0]  # 傣族竹楼
            data = YUNNAN_ETHNIC_HOUSES[name]
            img_path = ARCHITECTURE_IMAGES.get(data["img_key"], ARCHITECTURE_IMAGES["云南民族"])
            img_base64 = get_image_base64(img_path)
            if img_base64:
                st.markdown(f"""
                <div class="architecture-card">
                    <img src="data:image/png;base64,{img_base64}" class="architecture-img">
                    <div class="architecture-title">{data['full_name']}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="architecture-card">
                    <div style="height:220px; background: linear-gradient(135deg, #667eea, #764ba2); display:flex; align-items:center; justify-content:center; color:white; font-size:3rem;">🏘️</div>
                    <div class="architecture-title">{data['full_name']}</div>
                </div>
                """, unsafe_allow_html=True)
            if st.button(f"查看{data['full_name']}", key=f"ethnic_{name}", use_container_width=True):
                st.session_state.detail = name
                st.rerun()
        
        with col2:
            name = ethnic_names[1]  # 白族三坊一照壁
            data = YUNNAN_ETHNIC_HOUSES[name]
            img_path = ARCHITECTURE_IMAGES.get(data["img_key"], ARCHITECTURE_IMAGES["云南民族"])
            img_base64 = get_image_base64(img_path)
            if img_base64:
                st.markdown(f"""
                <div class="architecture-card">
                    <img src="data:image/png;base64,{img_base64}" class="architecture-img">
                    <div class="architecture-title">{data['full_name']}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="architecture-card">
                    <div style="height:220px; background: linear-gradient(135deg, #667eea, #764ba2); display:flex; align-items:center; justify-content:center; color:white; font-size:3rem;">🏘️</div>
                    <div class="architecture-title">{data['full_name']}</div>
                </div>
                """, unsafe_allow_html=True)
            if st.button(f"查看{data['full_name']}", key=f"ethnic_{name}", use_container_width=True):
                st.session_state.detail = name
                st.rerun()
        
        with col3:
            name = ethnic_names[2]  # 彝族土掌房
            data = YUNNAN_ETHNIC_HOUSES[name]
            img_path = ARCHITECTURE_IMAGES.get(data["img_key"], ARCHITECTURE_IMAGES["云南民族"])
            img_base64 = get_image_base64(img_path)
            if img_base64:
                st.markdown(f"""
                <div class="architecture-card">
                    <img src="data:image/png;base64,{img_base64}" class="architecture-img">
                    <div class="architecture-title">{data['full_name']}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="architecture-card">
                    <div style="height:220px; background: linear-gradient(135deg, #667eea, #764ba2); display:flex; align-items:center; justify-content:center; color:white; font-size:3rem;">🏘️</div>
                    <div class="architecture-title">{data['full_name']}</div>
                </div>
                """, unsafe_allow_html=True)
            if st.button(f"查看{data['full_name']}", key=f"ethnic_{name}", use_container_width=True):
                st.session_state.detail = name
                st.rerun()
        
        # 第二行：3个
        col1, col2, col3 = st.columns(3)
        
        with col1:
            name = ethnic_names[3]  # 哈尼族蘑菇房
            data = YUNNAN_ETHNIC_HOUSES[name]
            img_path = ARCHITECTURE_IMAGES.get(data["img_key"], ARCHITECTURE_IMAGES["云南民族"])
            img_base64 = get_image_base64(img_path)
            if img_base64:
                st.markdown(f"""
                <div class="architecture-card">
                    <img src="data:image/png;base64,{img_base64}" class="architecture-img">
                    <div class="architecture-title">{data['full_name']}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="architecture-card">
                    <div style="height:220px; background: linear-gradient(135deg, #667eea, #764ba2); display:flex; align-items:center; justify-content:center; color:white; font-size:3rem;">🏘️</div>
                    <div class="architecture-title">{data['full_name']}</div>
                </div>
                """, unsafe_allow_html=True)
            if st.button(f"查看{data['full_name']}", key=f"ethnic_{name}", use_container_width=True):
                st.session_state.detail = name
                st.rerun()
        
        with col2:
            name = ethnic_names[4]  # 纳西族四合院
            data = YUNNAN_ETHNIC_HOUSES[name]
            img_path = ARCHITECTURE_IMAGES.get(data["img_key"], ARCHITECTURE_IMAGES["云南民族"])
            img_base64 = get_image_base64(img_path)
            if img_base64:
                st.markdown(f"""
                <div class="architecture-card">
                    <img src="data:image/png;base64,{img_base64}" class="architecture-img">
                    <div class="architecture-title">{data['full_name']}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="architecture-card">
                    <div style="height:220px; background: linear-gradient(135deg, #667eea, #764ba2); display:flex; align-items:center; justify-content:center; color:white; font-size:3rem;">🏘️</div>
                    <div class="architecture-title">{data['full_name']}</div>
                </div>
                """, unsafe_allow_html=True)
            if st.button(f"查看{data['full_name']}", key=f"ethnic_{name}", use_container_width=True):
                st.session_state.detail = name
                st.rerun()
        
        with col3:
            name = ethnic_names[5]  # 独龙族木楞房
            data = YUNNAN_ETHNIC_HOUSES[name]
            img_path = ARCHITECTURE_IMAGES.get(data["img_key"], ARCHITECTURE_IMAGES["云南民族"])
            img_base64 = get_image_base64(img_path)
            if img_base64:
                st.markdown(f"""
                <div class="architecture-card">
                    <img src="data:image/png;base64,{img_base64}" class="architecture-img">
                    <div class="architecture-title">{data['full_name']}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="architecture-card">
                    <div style="height:220px; background: linear-gradient(135deg, #667eea, #764ba2); display:flex; align-items:center; justify-content:center; color:white; font-size:3rem;">🏘️</div>
                    <div class="architecture-title">{data['full_name']}</div>
                </div>
                """, unsafe_allow_html=True)
            if st.button(f"查看{data['full_name']}", key=f"ethnic_{name}", use_container_width=True):
                st.session_state.detail = name
                st.rerun()
        
        # 返回按钮
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔙 返回建筑列表", key="back_to_module1", use_container_width=True):
                st.session_state.detail = None
                st.rerun()
    
    # 第三层：具体民族建筑详情
    elif st.session_state.detail in YUNNAN_ETHNIC_HOUSES:
        data = YUNNAN_ETHNIC_HOUSES[st.session_state.detail]
        img_path = ARCHITECTURE_IMAGES.get(data["img_key"], ARCHITECTURE_IMAGES["云南民族"])
        
        st.markdown(f'<div class="detail-title">🏘️ {data["full_name"]}</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea20, #764ba220); border-radius: 20px; padding: 20px;">
            """, unsafe_allow_html=True)
            
            display_image_from_file(img_path, f"{data['full_name']} - 云南民族建筑")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="detail-section">
                <h3>📐 结构特点</h3>
                <p>{data['struct']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="detail-section">
                <h3>📊 数学模型</h3>
                <p>{data['math']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="detail-section">
                <h3>📜 历史渊源</h3>
                <p>{data['history']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="detail-section">
                <h3>🏗️ 营造结构</h3>
                <p>{data['structure']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="detail-section">
                <h3>🎨 文化内涵</h3>
                <p>{data['culture']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="detail-section">
            <h3>🔢 详细数学建模</h3>
            <div class="math-formula">
                {data['math_detail'].replace(chr(10), '<br>')}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="detail-section">
                <h3>🏛️ 著名实例</h3>
                <p>{data['famous']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="detail-section">
                <h3>🔨 营造要点</h3>
                <p>{data['construction'].replace(chr(10), '<br>')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="detail-section">
            <h3>📋 主要特征</h3>
            <p>{' · '.join(data['features'])}</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔙 返回云南民族总览", key="back_to_yunnan_overview", use_container_width=True):
                st.session_state.detail = "云南民族"
                st.rerun()
    
    # 其他建筑详情（亭、台、楼、阁、榭、舫、轩）
    else:
        data = ARCHITECTURES[st.session_state.detail]
        
        st.markdown(f'<div class="detail-title">🏯 {st.session_state.detail}</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea20, #764ba220); border-radius: 20px; padding: 20px;">
            """, unsafe_allow_html=True)
            
            display_image_from_file(data["img_path"], f"{st.session_state.detail} - 中国传统建筑")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="detail-section">
                <h3>📐 结构特点</h3>
                <p>{data['struct']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="detail-section">
                <h3>📊 数学模型</h3>
                <p>{data['math']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="detail-section">
                <h3>📜 历史渊源</h3>
                <p>{data['history']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="detail-section">
                <h3>🏗️ 营造结构</h3>
                <p>{data['structure']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="detail-section">
                <h3>🎨 文化内涵</h3>
                <p>{data['culture']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="detail-section">
            <h3>🔢 详细数学建模</h3>
            <div class="math-formula">
                {data['math_detail'].replace(chr(10), '<br>')}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="detail-section">
                <h3>🏛️ 著名实例</h3>
                <p>{data['famous']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="detail-section">
                <h3>🔨 营造要点</h3>
                <p>{data['construction'].replace(chr(10), '<br>')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="detail-section">
            <h3>📋 类型细分</h3>
            <p>{data['types']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔙 返回建筑列表", key="back_button_detail", use_container_width=True):
                st.session_state.detail = None
                st.rerun()

# 3. 模块二：营造制度（经典案例标签改为左中右居中对齐）
elif st.session_state.page == 'module2':
    back_btn()
    st.markdown('<script>window.scrollTo(0, 0);</script>', unsafe_allow_html=True)
    st.markdown('<div class="main-header">📜 中国古代建筑营造制度</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="module-tab">', unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("📅 时间轴", key="tab_timeline", use_container_width=True):
            st.session_state.module2_subpage = 'timeline'
            st.session_state.module2_system = None
            st.rerun()
    with col2:
        if st.button("📚 体系总览", key="tab_systems", use_container_width=True):
            st.session_state.module2_subpage = 'systems'
            st.session_state.module2_system = None
            st.rerun()
    with col3:
        if st.button("⚖️ 制度对比", key="tab_compare", use_container_width=True):
            st.session_state.module2_subpage = 'compare'
            st.session_state.module2_system = None
            st.rerun()
    with col4:
        if st.button("🏛️ 经典案例", key="tab_gallery", use_container_width=True):
            st.session_state.module2_subpage = 'gallery'
            st.session_state.module2_system = None
            st.rerun()
    with col5:
        if st.button("🕸️ 知识图谱", key="tab_knowledge", use_container_width=True):
            st.session_state.module2_subpage = 'knowledge'
            st.session_state.module2_system = None
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.session_state.module2_subpage == 'timeline' and st.session_state.module2_system is None:
        st.markdown("""
        <div class="intro-text">
            中国古代建筑营造制度历经数千年的发展演变，从唐代的材分制到清代的斗口制，<br>
            形成了完整而严密的模数体系。点击下方时间轴卡片，深入了解每一种营造制度。
        </div>
        """, unsafe_allow_html=True)
        
        sorted_systems = sorted(BUILDING_SYSTEMS.items(), 
                               key=lambda x: parse_year(x[1]['year']))
        
        for system_name, system_data in sorted_systems:
            col1, col2, col3 = st.columns([1, 10, 1])
            with col2:
                st.markdown(f"""
                <div class="timeline-card" style="border-left-color: {system_data['color']};">
                    <div class="timeline-year">{system_data['year']}</div>
                    <div class="timeline-title">{system_name}</div>
                    <div class="timeline-desc">{system_data['modern'][:150]}...</div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"查看{system_name}详情", key=f"timeline_{system_name}", use_container_width=True):
                    st.session_state.module2_system = system_name
                    st.rerun()
    
    elif st.session_state.module2_subpage == 'systems' and st.session_state.module2_system is None:
        st.markdown("""
        <div class="intro-text">
            中国历代营造制度共12种，每种制度都有其独特的模数体系和营造规则。<br>
            点击下方卡片，深入了解每一种制度的详细内容。
        </div>
        """, unsafe_allow_html=True)
        
        cols = st.columns(3)
        for i, (system_name, system_data) in enumerate(BUILDING_SYSTEMS.items()):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="system-card">
                    <div class="system-icon">{system_data['icon']}</div>
                    <div class="system-name">{system_name}</div>
                    <div class="system-period">{system_data['year']}</div>
                    <div class="system-desc">{system_data['modern'][:80]}...</div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"查看{system_name}详情", key=f"system_{system_name}", use_container_width=True):
                    st.session_state.module2_system = system_name
                    st.rerun()
    
    elif st.session_state.module2_system is not None:
        system_name = st.session_state.module2_system
        data = BUILDING_SYSTEMS[system_name]
        
        st.markdown(f'<div class="detail-title">{data["icon"]} {system_name}</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{data['year']}</div>
                <div class="metric-label">年代</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{data['dynasty']}</div>
                <div class="metric-label">朝代</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{data['source']}</div>
                <div class="metric-label">典籍来源</div>
            </div>
            """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📜 古籍原文")
            st.markdown(f'<div class="ancient-text">{data["ancient"]}</div>', unsafe_allow_html=True)
            st.markdown(f"**出处**：{data['source']} · {data['author']}")
        
        with col2:
            st.markdown("### 📖 白话文解读")
            st.markdown(f'<div class="modern-text">{data["modern"]}</div>', unsafe_allow_html=True)
            
            st.markdown("### ✨ 主要特征")
            features_html = ""
            for feature in data['features']:
                features_html += f'<span style="background: {data["color"]}20; color: {data["color"]}; padding: 5px 10px; border-radius: 15px; margin-right: 10px;">{feature}</span>'
            st.markdown(f'<div style="margin: 15px 0;">{features_html}</div>', unsafe_allow_html=True)
        
        if data["image"]:
            st.markdown("### 🖼️ 代表建筑")
            display_image_from_file(data["image"], f"{system_name}代表建筑", "300px")
        
        st.markdown("### 📊 模数体系参数")
        
        if "材等" in data["modules"]:
            modules_df = pd.DataFrame({
                "等级": list(data["modules"]["材等"].keys()),
                "尺寸(mm)": list(data["modules"]["材等"].values())
            })
            
            col1, col2 = st.columns([1, 1])
            with col1:
                fig = go.Figure(data=[
                    go.Bar(
                        x=list(data["modules"]["材等"].keys()),
                        y=list(data["modules"]["材等"].values()),
                        marker_color=data['color']
                    )
                ])
                fig.update_layout(
                    title="材等尺寸对比",
                    xaxis_title="材等",
                    yaxis_title="尺寸 (mm)",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.dataframe(modules_df, use_container_width=True, hide_index=True)
        
        st.markdown("### 🏛️ 代表建筑")
        st.markdown(f"**{data['example']}**")
        
        if system_name in CLASSIC_CASES:
            st.markdown("### 📸 经典案例详情")
            cases = CLASSIC_CASES[system_name]
            
            for case in cases:
                with st.container():
                    st.markdown(f"""
                    <div class="detail-section">
                        <h4>🏯 {case['name']}（{case['location']} · {case['year']}）</h4>
                        <p>{case['desc']}</p>
                        <p><strong>主要特点</strong>：{', '.join(case['features'])}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    if case['image']:
                        display_image_from_file(case['image'], case['name'], "250px")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔙 返回制度列表", key="back_to_systems", use_container_width=True):
                st.session_state.module2_system = None
                st.rerun()
    
    elif st.session_state.module2_subpage == 'compare':
        st.markdown("""
        <div class="intro-text">
            对比分析12种营造制度的异同，直观展示历代模数体系的演变规律。<br>
            从材分制到斗口制，制度的演变反映了中国古代建筑技术的进步。
        </div>
        """, unsafe_allow_html=True)
        
        fig = create_comparison_chart()
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### 📋 详细参数对比")
        
        compare_data = []
        for system_name, data in BUILDING_SYSTEMS.items():
            compare_data.append({
                "体系名称": system_name,
                "朝代": data["dynasty"],
                "年代": data["year"],
                "典籍来源": data["source"],
                "主要特征": "、".join(data["features"][:2]),
                "代表建筑": data["example"]
            })
        
        df_compare = pd.DataFrame(compare_data)
        st.dataframe(df_compare, use_container_width=True, hide_index=True)
    
    elif st.session_state.module2_subpage == 'gallery':
        st.markdown("""
        <div class="intro-text">
            经典案例库收录了各时期最具代表性的建筑实例，每一座建筑都是营造制度的完美体现。<br>
            点击下方按钮，浏览不同类别的建筑瑰宝。
        </div>
        """, unsafe_allow_html=True)
        
        # 左中右居中对齐的标签按钮
        col_left, col_center1, col_center2, col_center3, col_right = st.columns([1, 1, 1, 1, 1])
        
        with col_center1:
            if st.button("🏛️ 殿堂建筑", key="tab_hall", use_container_width=True):
                st.session_state.gallery_tab = "殿堂建筑"
        with col_center2:
            if st.button("🏘️ 民居大观", key="tab_house", use_container_width=True):
                st.session_state.gallery_tab = "民居大观"
        with col_center3:
            if st.button("🌉 桥梁工程", key="tab_bridge", use_container_width=True):
                st.session_state.gallery_tab = "桥梁工程"
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 殿堂建筑
        if st.session_state.gallery_tab == "殿堂建筑":
            for system_name, cases in CLASSIC_CASES.items():
                if system_name in ["唐制·大木作", "宋制·材分制", "明制·官式", "清制·斗口制"]:
                    if system_name in BUILDING_SYSTEMS:
                        st.markdown(f"### {BUILDING_SYSTEMS[system_name]['icon']} {system_name}")
                        
                        cols = st.columns(2)
                        for i, case in enumerate(cases):
                            with cols[i % 2]:
                                img_base64 = get_image_base64(case['image']) if case['image'] else None
                                if img_base64:
                                    st.markdown(f"""
                                    <div class="architecture-card">
                                        <img src="data:image/png;base64,{img_base64}" class="architecture-img">
                                        <div class="architecture-title">{case['name']}</div>
                                        <div style="padding: 10px 15px 15px;">
                                            <p style="color: #666;"><strong>{case['location']} · {case['year']}</strong></p>
                                            <p style="color: #555; font-size: 0.95rem;">{case['desc'][:100]}...</p>
                                            <p style="color: #FF6B6B; font-size: 0.9rem;">{' · '.join(case['features'])}</p>
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                else:
                                    st.markdown(f"""
                                    <div class="architecture-card">
                                        <div style="height:220px; background: linear-gradient(135deg, #667eea, #764ba2); display:flex; align-items:center; justify-content:center; color:white; font-size:3rem;">🏯</div>
                                        <div class="architecture-title">{case['name']}</div>
                                        <div style="padding: 10px 15px 15px;">
                                            <p style="color: #666;"><strong>{case['location']} · {case['year']}</strong></p>
                                            <p style="color: #555; font-size: 0.95rem;">{case['desc'][:100]}...</p>
                                            <p style="color: #FF6B6B; font-size: 0.9rem;">{' · '.join(case['features'])}</p>
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
        
        # 民居大观
        elif st.session_state.gallery_tab == "民居大观":
            if "民居大观" in CLASSIC_CASES:
                st.markdown("### 🏘️ 中国传统民居精华")
                
                cols = st.columns(2)
                for i, case in enumerate(CLASSIC_CASES["民居大观"]):
                    with cols[i % 2]:
                        img_base64 = get_image_base64(case['image']) if case['image'] else None
                        if img_base64:
                            st.markdown(f"""
                            <div class="architecture-card">
                                <img src="data:image/png;base64,{img_base64}" class="architecture-img">
                                <div class="architecture-title">{case['name']}</div>
                                <div style="padding: 10px 15px 15px;">
                                    <p style="color: #666;"><strong>{case['location']} · {case['year']}</strong></p>
                                    <p style="color: #555; font-size: 0.95rem;">{case['desc'][:100]}...</p>
                                    <p style="color: #FF6B6B; font-size: 0.9rem;">{' · '.join(case['features'])}</p>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div class="architecture-card">
                                <div style="height:220px; background: linear-gradient(135deg, #667eea, #764ba2); display:flex; align-items:center; justify-content:center; color:white; font-size:3rem;">🏘️</div>
                                <div class="architecture-title">{case['name']}</div>
                                <div style="padding: 10px 15px 15px;">
                                    <p style="color: #666;"><strong>{case['location']} · {case['year']}</strong></p>
                                    <p style="color: #555; font-size: 0.95rem;">{case['desc'][:100]}...</p>
                                    <p style="color: #FF6B6B; font-size: 0.9rem;">{' · '.join(case['features'])}</p>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
        
        # 桥梁工程
        elif st.session_state.gallery_tab == "桥梁工程":
            if "桥梁工程" in CLASSIC_CASES:
                st.markdown("### 🌉 中国古代桥梁工程")
                
                cols = st.columns(2)
                for i, case in enumerate(CLASSIC_CASES["桥梁工程"]):
                    with cols[i % 2]:
                        img_base64 = get_image_base64(case['image']) if case['image'] else None
                        if img_base64:
                            st.markdown(f"""
                            <div class="architecture-card">
                                <img src="data:image/png;base64,{img_base64}" class="architecture-img">
                                <div class="architecture-title">{case['name']}</div>
                                <div style="padding: 10px 15px 15px;">
                                    <p style="color: #666;"><strong>{case['location']} · {case['year']}</strong></p>
                                    <p style="color: #555; font-size: 0.95rem;">{case['desc'][:100]}...</p>
                                    <p style="color: #FF6B6B; font-size: 0.9rem;">{' · '.join(case['features'])}</p>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div class="architecture-card">
                                <div style="height:220px; background: linear-gradient(135deg, #667eea, #764ba2); display:flex; align-items:center; justify-content:center; color:white; font-size:3rem;">🌉</div>
                                <div class="architecture-title">{case['name']}</div>
                                <div style="padding: 10px 15px 15px;">
                                    <p style="color: #666;"><strong>{case['location']} · {case['year']}</strong></p>
                                    <p style="color: #555; font-size: 0.95rem;">{case['desc'][:100]}...</p>
                                    <p style="color: #FF6B6B; font-size: 0.9rem;">{' · '.join(case['features'])}</p>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
    
    elif st.session_state.module2_subpage == 'knowledge':
        st.markdown("""
        <div class="intro-text">
            营造制度知识图谱展示了12种建筑模数体系之间的传承与影响关系。<br>
            从唐代到清代，制度的演变形成了一条清晰的发展脉络。
        </div>
        """, unsafe_allow_html=True)
        
        fig = create_knowledge_graph()
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### 📖 制度演变脉络")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="detail-section">
                <h4>📜 主要传承关系</h4>
                <ul style="line-height: 2;">
                    <li><strong>唐制</strong> → 宋制、辽制、渤海国制</li>
                    <li><strong>宋制</strong> → 金制、元制</li>
                    <li><strong>元制</strong> → 明制</li>
                    <li><strong>明制</strong> → 清制</li>
                    <li><strong>唐制</strong> → 藏式（融合）</li>
                    <li><strong>南诏大理制</strong> → 藏式（融合）</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="detail-section">
                <h4>⚙️ 模数演变</h4>
                <ul style="line-height: 2;">
                    <li><strong>唐</strong>：材分三等，殿柱15材</li>
                    <li><strong>宋</strong>：材分八等，柱高6材</li>
                    <li><strong>元</strong>：材分三等，柱高6材</li>
                    <li><strong>明</strong>：斗口制雏形</li>
                    <li><strong>清</strong>：斗口十一等，高度标准化</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)


# 3. 模块三：数学建模平台
elif st.session_state.page == 'module3':
    back_btn()
    st.markdown('<script>window.scrollTo(0, 0);</script>', unsafe_allow_html=True)
    st.markdown('<div class="main-header">📐 数学建模·古建筑建造模拟</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="intro-text">
        AI驱动的电影级数学建模引擎 | 分步建造动画 + 一键成形 | 完整展现从台基到落成的建造全过程
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="module-tab">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏛️ 材分制·殿堂建筑", key="mode_tab1_btn", use_container_width=True):
            st.session_state.module3_mode = 'caifen'
            st.rerun()
    with col2:
        if st.button("🏯 亭台楼阁·古典建筑", key="mode_tab2_btn", use_container_width=True):
            st.session_state.module3_mode = 'gudian'
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    if 'module3_mode' not in st.session_state:
        st.session_state.module3_mode = 'caifen'
    
    if st.session_state.module3_mode == 'caifen':
        st.markdown("### 🎛️ 材分制建筑参数配置")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            system_name = st.selectbox("营造体系", list(SYSTEMS.keys()), key="m3_system")
        with col2:
            system = SYSTEMS[system_name]
            grade = st.selectbox(f"{system['unit']}等级", list(system["scale"].keys()), key="m3_grade")
        with col3:
            jian_shu = st.slider("开间数", 1, 9, 3, step=2, key="m3_jian")
        with col4:
            bu_jia_shu = st.slider("步架数", 2, 8, 4, step=1, key="m3_bu")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            ming_jian_fen = st.number_input(f"明间宽 ({system['unit']})", 150, 400, 250, step=10, key="m3_ming")
        with col2:
            bu_shen_fen = st.number_input(f"步架深 ({system['unit']})", 80, 250, 120, step=10, key="m3_bushen")
        with col3:
            ju_zhe_ratio = st.slider("举折系数", 0.25, 0.45, 0.333, 0.001, key="m3_juzhe")
        
        base_unit = system["base_unit"](grade)
        
        st.markdown("---")
        st.markdown("### 🏗️ 材分制建筑数学建模建造动画")
        
        animation_html = create_caifen_animation(
            system_name, grade, jian_shu, bu_jia_shu,
            ming_jian_fen, bu_shen_fen, ju_zhe_ratio,
            system['color'], base_unit
        )
        components.html(animation_html, height=650)
    
    else:
        st.markdown("### 🎛️ 古典建筑类型选择")
        
        arch_names = list(ARCHITECTURES.keys())
        arch_cols = st.columns(8)
        for i, name in enumerate(arch_names):
            with arch_cols[i]:
                display_image_from_file(ARCHITECTURES[name]["img_path"], name, "80px")
                if st.button(f"选择{name}", key=f"select_{name}"):
                    st.session_state.module3_architecture = name
                    st.rerun()
        
        if 'module3_architecture' not in st.session_state:
            st.session_state.module3_architecture = '亭'
        
        st.markdown("---")
        st.markdown(f"### 🏗️ {st.session_state.module3_architecture} 数学建模建造动画")
        
        arch_animation_html = create_architecture_animation(st.session_state.module3_architecture)
        components.html(arch_animation_html, height=650)
    
    st.markdown("---")
    st.markdown("### 🤖 AI智能图片识别")
    st.markdown("上传古建筑图片，AI将自动识别建筑类型、结构特征并生成分析报告")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        uploaded_file = st.file_uploader("选择古建筑图片", type=['jpg', 'jpeg', 'png'], key="m3_upload")
        if uploaded_file is not None:
            st.image(uploaded_file, caption="上传的图片", use_container_width=True)
            if st.button("🔍 AI分析图片", key="m3_analyze"):
                with st.spinner("AI正在分析中..."):
                    img_bytes = uploaded_file.getvalue()
                    result = analyze_architecture_image(img_bytes)
                    st.session_state.image_analysis_result = result
                st.success("分析完成！")
    
    with col2:
        if st.session_state.image_analysis_result is not None:
            result = st.session_state.image_analysis_result
            st.markdown(f"""
            <div class="param-panel" style="background: rgba(255,255,255,0.9);">
                <div class="param-title">📊 AI分析报告</div>
                <div class="param-content">
                    <p><strong>🏛️ 推测建筑类型：</strong> {result['type']}</p>
                    <p><strong>🎯 置信度：</strong> {result['confidence']*100:.0f}%</p>
                    <p><strong>🏔️ 屋顶样式：</strong> {result['roof_style']}</p>
                    <p><strong>📐 图像特征：</strong></p>
                    <ul>
                        {"".join([f"<li>{f}</li>" for f in result['features']])}
                    </ul>
                    <p><strong>📝 分析描述：</strong><br>{result['description']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("👈 请先上传古建筑图片，然后点击「AI分析图片」按钮")
    
    st.markdown("""
    <div style="background: rgba(0,0,0,0.5); border-radius: 12px; padding: 15px; margin-top: 20px;">
        <p style="color: #ffd796; margin: 0; text-align: center;">
            🎬 动画说明 | 点击步骤按钮观看分步建造 | 「一键成形」观看完整建造过程 | 支持鼠标拖拽旋转视角
        </p>
    </div>
    """, unsafe_allow_html=True)
# 4. 模块四：数字化分析（重构版 - 新布局：顶部仪表盘 + 第一行三列 + 第二行三列）
elif st.session_state.page == 'module4':
    back_btn()
    st.markdown('<script>window.scrollTo(0, 0);</script>', unsafe_allow_html=True)
    st.markdown('<div class="main-header">🔬 古建数字化分析中心</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="intro-text">
        ⚡ 智能参数化设计 · 实时力学分析 · 规制合规检测 · 多方案对比 · 设计成果导出 ⚡
    </div>
    """, unsafe_allow_html=True)
    
    # 先计算当前数据用于所有面板
    system_name = st.session_state.module4_params['system']
    system = SYSTEMS[system_name]
    grade = st.session_state.module4_params['grade']
    base_unit = system["base_unit"](grade)
    jian_shu = st.session_state.module4_params['jian_shu']
    bu_jia_shu = st.session_state.module4_params['bu_jia_shu']
    ming_jian_fen = st.session_state.module4_params['ming_jian_width']
    ci_jian_fen = st.session_state.module4_params['ci_jian_width']
    bu_shen_fen = st.session_state.module4_params['bu_jia_depth']
    ju_zhe_ratio = st.session_state.module4_params['ju_zhe_ratio']
    wood_strength = st.session_state.module4_params['wood_strength']
    load_factor = st.session_state.module4_params['load_factor']
    
    jian_width = ming_jian_fen * base_unit
    bu_depth = bu_shen_fen * base_unit
    total_width_m = jian_shu * jian_width / 1000
    total_depth_m = bu_jia_shu * bu_depth / 1000
    
    # 计算尺寸数据
    df, base_unit, total_width, total_depth, ju_gao, mechanics, compliance = calculate_dimensions(
        system_name, grade, jian_shu, ming_jian_fen, ci_jian_fen, bu_jia_shu, bu_shen_fen, ju_zhe_ratio
    )
    
    # ========== 顶部仪表盘 ==========
    st.markdown("### 📊 实时设计仪表盘")
    dash_col1, dash_col2, dash_col3, dash_col4 = st.columns(4)
    
    with dash_col1:
        st.markdown(f"""
        <div class="dashboard-card" style="text-align:center;">
            <div class="dashboard-value">{total_width_m:.1f}m</div>
            <div class="dashboard-label">总面阔</div>
        </div>
        """, unsafe_allow_html=True)
    
    with dash_col2:
        st.markdown(f"""
        <div class="dashboard-card" style="text-align:center;">
            <div class="dashboard-value">{total_depth_m:.1f}m</div>
            <div class="dashboard-label">总进深</div>
        </div>
        """, unsafe_allow_html=True)
    
    with dash_col3:
        area_m2 = total_width_m * total_depth_m
        st.markdown(f"""
        <div class="dashboard-card" style="text-align:center;">
            <div class="dashboard-value">{area_m2:.1f}㎡</div>
            <div class="dashboard-label">占地面积</div>
        </div>
        """, unsafe_allow_html=True)
    
    with dash_col4:
        st.markdown(f"""
        <div class="dashboard-card" style="text-align:center;">
            <div class="dashboard-value">{grade.split('(')[0] if '(' in grade else grade}</div>
            <div class="dashboard-label">当前等级</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ========== 第一行：三列布局 ==========
    # 左列：核心参数调节（简洁白卡片）
    # 中列：2D结构简图 + 构件尺寸表
    # 右列：力学分析 + 规制合规性检测
    col1, col2, col3 = st.columns([1.2, 1.5, 1.2])
    
    # ===== 左列：核心参数调节 =====
    with col1:
        st.markdown('<div class="simple-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">🎛️ 核心参数调节</div>', unsafe_allow_html=True)
        
        system_options = list(SYSTEMS.keys())
        new_system_name = st.selectbox("选择营造体系", system_options, 
                                  index=system_options.index(st.session_state.module4_params['system']),
                                  key="param_system")
        
        new_system = SYSTEMS[new_system_name]
        grade_options = list(new_system["scale"].keys())
        new_grade = st.selectbox(f"选择{new_system['unit']}等级", grade_options,
                            index=min(2, len(grade_options)-1),
                            key="param_grade")
        
        new_jian_shu = st.slider("开间数", 1, 11, st.session_state.module4_params['jian_shu'], step=2, key="param_jian")
        new_bu_jia_shu = st.slider("步架数", 2, 8, st.session_state.module4_params['bu_jia_shu'], step=1, key="param_bu")
        
        col_a, col_b = st.columns(2)
        with col_a:
            new_ming_jian_fen = st.number_input(f"明间宽 ({new_system['unit']})", 
                                            min_value=100, max_value=500, 
                                            value=st.session_state.module4_params['ming_jian_width'],
                                            step=10, key="param_ming")
        with col_b:
            new_ci_jian_fen = st.number_input(f"次间宽 ({new_system['unit']})",
                                          min_value=80, max_value=400,
                                          value=st.session_state.module4_params['ci_jian_width'],
                                          step=10, key="param_ci")
        
        new_bu_shen_fen = st.number_input(f"步架深 ({new_system['unit']})",
                                      min_value=50, max_value=300,
                                      value=st.session_state.module4_params['bu_jia_depth'],
                                      step=10, key="param_bushen")
        
        new_ju_zhe_ratio = st.slider("举折系数", 0.2, 0.5, 
                                 st.session_state.module4_params['ju_zhe_ratio'], 0.001, key="param_juzhe")
        
        st.markdown("### 🪵 材料参数")
        col_a, col_b = st.columns(2)
        with col_a:
            new_wood_strength = st.number_input("木材强度 (MPa)", 20, 50, 
                                            st.session_state.module4_params['wood_strength'], 1, key="param_wood")
        with col_b:
            new_load_factor = st.number_input("设计荷载 (kN/m²)", 3.0, 8.0,
                                         st.session_state.module4_params['load_factor'], 0.1, key="param_load")
        
        # 更新session state
        st.session_state.module4_params.update({
            'system': new_system_name,
            'grade': new_grade,
            'jian_shu': new_jian_shu,
            'bu_jia_shu': new_bu_jia_shu,
            'ming_jian_width': new_ming_jian_fen,
            'ci_jian_width': new_ci_jian_fen,
            'bu_jia_depth': new_bu_shen_fen,
            'ju_zhe_ratio': new_ju_zhe_ratio,
            'wood_strength': new_wood_strength,
            'load_factor': new_load_factor
        })
        
        # 实时数据显示
        st.markdown('<div class="live-card">', unsafe_allow_html=True)
        st.markdown("### 📊 实时数据")
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f'<div class="live-value">{total_width/1000:.2f}m</div><div class="live-label">总面阔</div>', unsafe_allow_html=True)
        with col_b:
            st.markdown(f'<div class="live-value">{total_depth/1000:.2f}m</div><div class="live-label">总进深</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="live-value">{ju_gao/1000:.2f}m</div><div class="live-label">屋顶举高</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("➕ 添加当前方案到对比", use_container_width=True, key="add_compare"):
            st.session_state.module4_compare.append({
                'name': f"方案{len(st.session_state.module4_compare)+1}",
                'system': new_system_name,
                'grade': new_grade,
                'jian_shu': new_jian_shu,
                '总面阔(m)': f"{total_width/1000:.2f}",
                '总进深(m)': f"{total_depth/1000:.2f}",
                '安全系数': mechanics['安全系数'],
                '柱应力(MPa)': mechanics['柱应力']
            })
            st.success("已添加到对比列表")
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ===== 中列：2D结构简图 + 构件尺寸表 =====
    with col2:
        st.markdown('<div class="simple-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">📐 2D结构简图</div>', unsafe_allow_html=True)
        
        try:
            zhu_jing = float(mechanics['柱径'].replace(' mm', ''))
            zhu_gao_val = float(mechanics['柱高'].replace(' mm', ''))
            fig_buf = draw_structure_diagram(jian_shu, bu_jia_shu, total_width/jian_shu, total_depth/bu_jia_shu, 
                                            zhu_jing, zhu_gao_val, ju_gao, system['color'])
            st.image(fig_buf, use_container_width=True)
        except Exception as e:
            st.warning(f"绘图出错：{str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="simple-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">📋 构件尺寸表</div>', unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ===== 右列：力学分析 + 规制合规性检测 =====
    with col3:
        st.markdown('<div class="simple-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">⚖️ 力学分析</div>', unsafe_allow_html=True)
        
        metrics = ['安全系数', '长细比', '稳定性系数', '柱应力', '承载力利用率']
        for metric in metrics:
            if metric in mechanics:
                value = mechanics[metric]
                try:
                    if metric == '安全系数':
                        num_value = float(value.replace(' ', '').replace('倍', ''))
                        color = "#27ae60" if num_value > 2.0 else "#e74c3c"
                    else:
                        color = "#2980b9"
                except:
                    color = "#2980b9"
                
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value" style="color: {color};">{value}</div>
                    <div class="metric-label">{metric}</div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="simple-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">✅ 规制合规性检测</div>', unsafe_allow_html=True)
        
        for item, msg, status in compliance:
            badge_class = "compliance-pass" if status == "pass" else "compliance-warn" if status == "warn" else "compliance-fail"
            st.markdown(f'<span class="compliance-badge {badge_class}">{item}: {msg}</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ========== 第二行：三列布局 ==========
    # 左列：受力热力图（移至中下方）
    # 中列：智能推荐 + 多方案对比
    # 右列：设计成果导出 + 设计洞察
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1.2, 1.5, 1.2])
    
    # ===== 左列：受力热力图 =====
    with col1:
        st.markdown('<div class="simple-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">🔥 受力热力图</div>', unsafe_allow_html=True)
        
        try:
            stress_values = []
            base_stress = float(mechanics['柱应力'].replace(' MPa', ''))
            for i in range(bu_jia_shu + 1):
                for j in range(jian_shu + 1):
                    factor = 1.0 + 0.2 * np.sin(i * np.pi / max(bu_jia_shu, 1)) * np.cos(j * np.pi / max(jian_shu, 1))
                    stress_values.append(base_stress * factor)
            
            heatmap_buf = create_heatmap(jian_shu, bu_jia_shu, stress_values, system['color'])
            st.image(heatmap_buf, use_container_width=True)
        except Exception as e:
            st.warning(f"热力图生成出错：{str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ===== 中列：智能推荐 + 多方案对比 =====
    with col2:
        st.markdown('<div class="simple-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">🤖 智能推荐</div>', unsafe_allow_html=True)
        
        recommendations = generate_recommendations(
            system_name, grade, jian_shu, bu_jia_shu, 
            ming_jian_fen, ci_jian_fen, bu_shen_fen, ju_zhe_ratio,
            mechanics.get('安全系数', '2.0')
        )
        
        for rec in recommendations:
            st.markdown(f"""
            <div class="recommend-card">
                <strong style="color: {'#e74c3c' if rec['type'] == 'warning' else '#f39c12'};">{rec['title']}</strong>
                <p style="margin:5px 0 0 0; font-size:0.9rem;">{rec['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        if not recommendations:
            st.info("当前参数配置合理，暂无优化建议")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 多方案对比
        if st.session_state.module4_compare:
            st.markdown('<div class="simple-panel">', unsafe_allow_html=True)
            st.markdown('<div class="panel-title">📊 多方案对比</div>', unsafe_allow_html=True)
            
            compare_df = pd.DataFrame(st.session_state.module4_compare)
            st.dataframe(compare_df, use_container_width=True, hide_index=True)
            
            if st.button("清空对比列表", use_container_width=True, key="clear_compare"):
                st.session_state.module4_compare = []
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # ===== 右列：设计成果导出 + 设计洞察 =====
    with col3:
        st.markdown('<div class="simple-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">📥 设计成果导出</div>', unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("📊 Excel尺寸表", use_container_width=True, key="export_excel"):
                excel_buf = save_to_excel(df)
                b64 = base64.b64encode(excel_buf.getvalue()).decode()
                href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="古建尺寸表.xlsx">点击下载Excel</a>'
                st.markdown(href, unsafe_allow_html=True)
        
        with col_b:
            if st.button("📄 报告TXT", use_container_width=True, key="export_txt"):
                report_buf = generate_text_report(system_name, grade, df, mechanics, compliance, recommendations)
                b64 = base64.b64encode(report_buf.getvalue()).decode()
                href = f'<a href="data:text/plain;base64,{b64}" download="古建设计报告.txt">点击下载报告</a>'
                st.markdown(href, unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("📐 SVG简图", use_container_width=True, key="export_svg"):
                fig, _ = plt.subplots(figsize=(10, 4))
                try:
                    svg_buf = save_svg_diagram(plt.gcf())
                    b64 = base64.b64encode(svg_buf.getvalue()).decode()
                    href = f'<a href="data:image/svg+xml;base64,{b64}" download="结构简图.svg">点击下载SVG</a>'
                    st.markdown(href, unsafe_allow_html=True)
                except:
                    st.warning("SVG导出失败")
        
        with col_b:
            if st.button("📋 复制参数", use_container_width=True, key="copy_params"):
                params_str = f"""营造体系：{system_name}
材等：{grade}
开间数：{jian_shu}
步架数：{bu_jia_shu}
明间宽：{ming_jian_fen} {system['unit']}
次间宽：{ci_jian_fen} {system['unit']}
步架深：{bu_shen_fen} {system['unit']}
举折系数：{ju_zhe_ratio:.3f}
安全系数：{mechanics.get('安全系数', 'N/A')}"""
                st.code(params_str)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 设计洞察
        st.markdown('<div class="simple-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">💡 设计洞察</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        try:
            sf = float(mechanics.get('安全系数', '2.0').replace(' ', '').replace('倍', ''))
            if sf > 2.5:
                insight = "✅ 当前结构安全储备充足，可考虑优化用材以降低成本"
            elif sf > 1.8:
                insight = "📊 安全系数处于合理区间，结构设计经济适用"
            else:
                insight = "⚠️ 安全系数偏低，建议增大主要构件截面或提高材料等级"
        except:
            insight = "请完成参数配置后查看设计洞察"
        
        st.markdown(f'<p style="margin:0; color:#17a2b8;">{insight}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)