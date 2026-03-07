"""
AN GIANG - KIÊN GIANG: DU LỊCH SỐ LẤY NGƯỜI DÙNG LÀ TRUNG TÂM
Dự án STEM Tin học - THPT HOA LAC
Tích hợp AI thông minh, có thể sử dụng trong doanh nghiệp
"""

import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from datetime import datetime
import random
from PIL import Image
import time
import base64

# ============================================
# THIẾT LẬP TRANG - PHẢI ĐẶT ĐẦU TIÊN
# ============================================

st.set_page_config(
    page_title="An Giang - Du Lịch Số",
    page_icon="🌏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM CSS VÀ HÌNH NỀN NGHỆ THUẬT - MÀU XANH MIỀN TÂY
# ============================================

def set_background(image_file):
    """
    Thiết lập hình nền cho ứng dụng với màu xanh miền Tây
    """
    try:
        with open(image_file, "rb") as f:
            img_data = f.read()
        b64_encoded = base64.b64encode(img_data).decode()
        style = f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(255, 255, 255, 0.85), rgba(240, 248, 255, 0.85)), 
                              url("data:image/png;base64,{b64_encoded}");
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
        }}
        </style>
        """
        st.markdown(style, unsafe_allow_html=True)
    except:
        # Fallback với gradient xanh miền Tây
        st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #e0f7fa 0%, #b2ebf2 30%, #80deea 70%, #4dd0e1 100%);
        }
        </style>
        """, unsafe_allow_html=True)

# Thiết lập hình nền
set_background("assets/images/background.jpg")

# Thêm CSS tùy chỉnh với màu xanh miền Tây
st.markdown("""
<style>
/* Màu chủ đạo: Xanh nước biển và xanh núi rừng */
:root {
    --blue-water: #1e88e5;
    --blue-water-light: #4fc3f7;
    --blue-water-dark: #0d47a1;
    --green-mountain: #2e7d32;
    --green-mountain-light: #4caf50;
    --green-mountain-dark: #1b5e20;
    --yellow-rice: #ffd54f;
    --brown-earth: #8d6e63;
}

/* Card styling với hiệu ứng nổi - màu xanh nước */
.custom-card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 10px 30px rgba(30, 136, 229, 0.1);
    border: 1px solid rgba(30, 136, 229, 0.2);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    margin-bottom: 20px;
    border-left: 5px solid var(--blue-water);
}

.custom-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 35px rgba(30, 136, 229, 0.15);
    border-color: var(--green-mountain-light);
}

/* Gradient buttons - xanh nước biển */
.gradient-btn {
    background: linear-gradient(45deg, #1e88e5, #4fc3f7);
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 50px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
}

.gradient-btn:hover {
    background: linear-gradient(45deg, #0d47a1, #1e88e5);
    transform: scale(1.05);
}

/* Section headers - xanh núi rừng */
.section-header {
    background: linear-gradient(90deg, #2e7d32, #4caf50);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.5rem;
    font-weight: 800;
    margin-bottom: 30px;
    text-align: center;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
}

/* Feature icons */
.feature-icon {
    font-size: 3rem;
    margin-bottom: 15px;
    background: linear-gradient(45deg, #1e88e5, #2e7d32);
    webkit-text-fill-color: transparent;
}

/* Glass effect for sidebar */
[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-right: 2px solid #e0f7fa;
}

/* KPI Cards - màu xanh nước */
.kpi-card {
    background: white;
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0 5px 15px rgba(30, 136, 229, 0.1);
    text-align: center;
    border-top: 5px solid var(--blue-water);
    transition: all 0.3s ease;
}

.kpi-card:hover {
    border-top: 5px solid var(--green-mountain);
    box-shadow: 0 8px 20px rgba(46, 125, 50, 0.15);
}

/* Dashboard header - gradient xanh */
.dashboard-header {
    background: linear-gradient(90deg, #1e88e5, #2e7d32);
    padding: 2rem;
    border-radius: 20px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}

/* AI header */
.ai-header {
    background: linear-gradient(135deg, #1e88e5 0%, #2e7d32 100%);
    padding: 2.5rem;
    border-radius: 20px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 10px 25px rgba(0,0,0,0.15);
}

.ai-header::before {
    content: "🤖";
    position: absolute;
    font-size: 10rem;
    opacity: 0.1;
    right: -30px;
    top: -30px;
}

/* Custom tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 10px 10px 0 0;
    padding: 10px 20px;
    font-weight: 600;
    background: #e0f7fa;
    border: 1px solid #b2ebf2;
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(45deg, #1e88e5, #4fc3f7);
    color: white;
    border-color: #1e88e5;
}

/* Footer styling */
.footer-section {
    background: linear-gradient(135deg, #e0f7fa 0%, #b2ebf2 100%);
    border-radius: 15px;
    padding: 20px;
    margin-top: 30px;
    border: 1px solid #80deea;
}

/* Map styling */
.map-container {
    border-radius: 15px;
    overflow: hidden;
    border: 2px solid #1e88e5;
    box-shadow: 0 5px 15px rgba(30, 136, 229, 0.2);
}

/* Table styling */
.stDataFrame {
    border: 1px solid #b2ebf2;
    border-radius: 10px;
}

/* Button styling */
.stButton > button {
    background: linear-gradient(45deg, #1e88e5, #4fc3f7);
    color: white;
    border: none;
    border-radius: 50px;
    padding: 10px 20px;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    background: linear-gradient(45deg, #0d47a1, #1e88e5);
    transform: scale(1.05);
}

/* Metric cards */
[data-testid="stMetricValue"] {
    color: #1e88e5;
}

[data-testid="stMetricDelta"] {
    color: #2e7d32;
}

/* Sidebar styling */
[data-testid="stSidebarNav"] {
    background: linear-gradient(180deg, #e0f7fa 0%, #ffffff 100%);
}

/* Text color adjustments */
h1, h2, h3, h4 {
    color: #1a237e;
}

p {
    color: #37474f;
}

/* Success, info, warning boxes */
.stAlert {
    border-radius: 10px;
    border-left: 5px solid;
}

.stAlert.stSuccess {
    border-left-color: #2e7d32;
    background-color: rgba(46, 125, 50, 0.1);
}

.stAlert.stInfo {
    border-left-color: #1e88e5;
    background-color: rgba(30, 136, 229, 0.1);
}

.stAlert.stWarning {
    border-left-color: #ffd54f;
    background-color: rgba(255, 213, 79, 0.1);
}

/* Banner styling */
.banner-container {
    width: 100%;
    height: 180px;
    overflow: hidden;
    border-radius: 15px;
    margin-bottom: 20px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.banner-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
}
</style>
""", unsafe_allow_html=True)

# ============================================
# IMPORT MODULES VÀ KHỞI TẠO
# ============================================

# Import các module
from modules.personalization import show_personalization_module
from modules.emotion_map import show_emotion_map_module
from modules.text_stories import show_text_stories_module
from modules.feedback import show_feedback_module
from utils.ai_recommendation import AIRecommendationSystem

# Tải dữ liệu
@st.cache_data
def load_data():
    """Tải tất cả dữ liệu cần thiết"""
    data = {}
    
    try:
        # Tải dữ liệu địa điểm
        with open('data/locations.json', 'r', encoding='utf-8') as f:
            data['locations'] = json.load(f)
        
        # Tải hành trình mẫu
        with open('data/itineraries.json', 'r', encoding='utf-8') as f:
            data['itineraries'] = json.load(f)
        
        # Tải câu chuyện văn bản
        with open('data/text_stories.json', 'r', encoding='utf-8') as f:
            data['text_stories'] = json.load(f)
    except Exception as e:
        st.warning(f"Không thể tải dữ liệu: {e}")
        data = {'locations': [], 'itineraries': [], 'text_stories': []}
    
    return data

# Khởi tạo AI Recommendation System
ai_system = AIRecommendationSystem()

# ============================================
# SIDEBAR NÂNG CẤP VỚI HÌNH ẢNH - MÀU XANH MIỀN TÂY
# ============================================

with st.sidebar:
    # Header với gradient xanh nước
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e88e5 0%, #2e7d32 100%); 
                padding: 1.5rem; 
                border-radius: 15px; 
                text-align: center;
                margin-bottom: 2rem;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);">
        <h1 style="color: white; margin: 0; font-size: 2.5rem;">🛕☪</h1>
        <h2 style="color: white; font-size: 1.2rem; margin: 10px 0 0 0;">AN GIANG</h2>
        <p style="color: rgba(255,255,255,0.9); font-size: 0.9rem; margin: 5px 0;">Miền Tây Sông Nước</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Logo với hiệu ứng
    try:
        logo_col1, logo_col2, logo_col3 = st.columns([1,2,1])
        with logo_col2:
            st.image("assets/images/logo.png", use_column_width=True)
    except:
        st.markdown("### 🏆 DỰ ÁN STEM")
    
    st.markdown("---")
    
    # Menu điều hướng đẹp hơn
    st.markdown("### 🧭 ĐIỀU HƯỚNG")
    
    menu_options = {
        "🏠 Trang chủ": "home",
        "🎯 Cá nhân hóa trải nghiệm": "module1",
        "🗺️ Bản đồ cảm xúc": "module2",
        "📖 Truyện kể di sản": "module3",
        "⭐ Đánh giá hài lòng": "module4",
        "📊 Dashboard tổng hợp": "dashboard",
        "🤖 AI Tư vấn thông minh": "ai_advisor"
    }
    
    selected_menu = st.selectbox("", list(menu_options.keys()))
    page = menu_options[selected_menu]
    
    # Hình ảnh đại diện
    st.markdown("---")
    st.markdown("### 📸 HÌNH ẢNH TIÊU BIỂU")
    
    # Tạo carousel đơn giản
    image_files = [
        "assets/images/gallery1.jpg",
        "assets/images/gallery2.jpg",
        "assets/images/gallery3.jpg"
    ]
    
    for img_file in image_files[:2]:  # Hiển thị 2 hình đầu
        try:
            st.image(img_file, use_column_width=True, caption="")
        except:
            pass
    
    # Thống kê với icon đẹp
    st.markdown("---")
    st.markdown("### 📈 THỐNG KÊ")
    
    stats_col1, stats_col2 = st.columns(2)
    with stats_col1:
        st.metric("📍 Địa điểm", "48", "+5")
    with stats_col2:
        st.metric("👤 Người dùng", "9,210", "15%")
    
    # Liên hệ với thiết kế đẹp
    st.markdown("---")
    st.markdown("### 📞 LIÊN HỆ")
    st.markdown("""
    <div style="background: rgba(30, 136, 229, 0.1); 
                padding: 15px; 
                border-radius: 10px;
                border-left: 4px solid #1e88e5;
                border-top: 1px solid #b2ebf2;">
        <p style="margin: 5px 0; color: #1a237e;">🏫 <b>Trường THPT HOA LAC</b></p>
        <p style="margin: 5px 0; color: #37474f;">📧 ducvinh2266@gmail.com</p>
        <p style="margin: 5px 0; color: #37474f;">📱 0343 561 847</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# LOAD DỮ LIỆU
# ============================================

data = load_data()

# ============================================
# MAIN CONTENT - TRANG CHỦ NÂNG CẤP
# ============================================

if page == "home":
    # Header mới - Thêm tiêu đề AG-DECT phía trên đầu
    st.markdown("""
    <div style="background: linear-gradient(90deg, #1e88e5 0%, #2e7d32 100%); 
                padding: 1rem; 
                border-radius: 15px; 
                text-align: center;
                margin-bottom: 1.5rem;
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
                border: 2px solid rgba(255,255,255,0.3);">
        <h1 style="color: white; margin: 0; font-size: 1.8rem; font-weight: bold;">
            🎯 AG-DECT: PHÁT TRIỂN DU LỊCH SỐ VÀ VĂN HOÁ AN GIANG
        </h1>
        <p style="color: rgba(255,255,255,0.9); margin: 5px 0 0 0; font-size: 0.9rem;">
            Sáng tạo - Kết nối - Phát triển bền vững
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Banner với kích thước hợp lý hơn
    st.markdown('<div class="banner-container">', unsafe_allow_html=True)
    try:
        st.image("assets/images/banner.jpg", use_column_width=True, caption="", 
                output_format="auto", clamp=False)
    except:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1e88e5 0%, #2e7d32 100%); 
                    height: 180px; 
                    border-radius: 15px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
                    color: white;
                    font-weight: bold;
                    font-size: 1.5rem;">
            🌊 Miền Tây An Giang - Vẻ Đẹp Sông Nước ⛰️
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Header chính với animation
    st.markdown("""
    <div class="custom-card" style="text-align: center; margin-top: 1rem; border-left: 5px solid #2e7d32;">
        <h1 style="font-size: 2.8rem; margin-bottom: 10px;">
            <span style="background: linear-gradient(45deg, #1e88e5, #2e7d32); 
                        -webkit-background-clip: text; 
                        -webkit-text-fill-color: transparent;
                        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">
                🌊 AN GIANG  ⛰️
            </span>
        </h1>
        <h2 style="color: #37474f; font-size: 1.6rem; margin-bottom: 15px;">
            Du Lịch Số - Lấy Người Dùng Là Trung Tâm
        </h2>
        <div style="display: inline-block; 
                    background: linear-gradient(45deg, #1e88e5, #2e7d32); 
                    padding: 6px 20px; 
                    border-radius: 50px;
                    color: white;
                    font-weight: bold;
                    margin-top: 10px;
                    box-shadow: 0 5px 15px rgba(30, 136, 229, 0.3);">
            🏆 STEM TIN HỌC - THPT HOÀ LẠC
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Tính năng nổi bật với hình ảnh
    st.markdown("<h2 class='section-header'>✨ TÍNH NĂNG NỔI BẬT</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="custom-card">
            <div style="text-align: center;">
                <div class="feature-icon">🎯</div>
                <h3 style="color: #1a237e; margin-bottom: 15px;">CÁ NHÂN HÓA</h3>
                <p style="color: #37474f; line-height: 1.6;">Hành trình được thiết kế riêng dựa trên sở thích, độ tuổi và ngân sách của bạn.</p>
            </div>
            <div style="text-align: center; margin-top: 20px;">
                <img src="https://images.unsplash.com/photo-1551632811-561732d1e306?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80" 
                     style="width: 100%; border-radius: 10px; height: 150px; object-fit: cover; border: 2px solid #b2ebf2;">
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="custom-card">
            <div style="text-align: center;">
                <div class="feature-icon">🗺️</div>
                <h3 style="color: #1a237e; margin-bottom: 15px;">BẢN ĐỒ CẢM XÚC</h3>
                <p style="color: #37474f; line-height: 1.6;">Khám phá địa điểm qua cảm xúc: vui vẻ, tĩnh lặng, phiêu lưu, lãng mạn.</p>
            </div>
            <div style="text-align: center; margin-top: 20px;">
                <img src="https://images.unsplash.com/photo-1526778548025-fa2f459cd5c1?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80" 
                     style="width: 100%; border-radius: 10px; height: 150px; object-fit: cover; border: 2px solid #b2ebf2;">
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="custom-card">
            <div style="text-align: center;">
                <div class="feature-icon">📖</div>
                <h3 style="color: #1a237e; margin-bottom: 15px;">TRUYỆN KỂ DI SẢN</h3>
                <p style="color: #37474f; line-height: 1.6;">45 câu chuyện hấp dẫn về văn hóa, lịch sử và con người An Giang - Kiên Giang.</p>
            </div>
            <div style="text-align: center; margin-top: 20px;">
                <img src="https://images.unsplash.com/photo-1481627834876-b7833e8f5570?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80" 
                     style="width: 100%; border-radius: 10px; height: 150px; object-fit: cover; border: 2px solid #b2ebf2;">
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Demo nhanh với hình ảnh
    st.markdown("<h2 class='section-header'>🚀 TRẢI NGHIỆM DEMO NHANH</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs([
        "🎯 **Cá nhân hóa**", 
        "🗺️ **Bản đồ**", 
        "📖 **Truyện kể**"
    ])
    
    with tab1:
        st.markdown("""
        <div class="custom-card">
            <h3 style="color: #1a237e; margin-bottom: 20px;">Khám phá hành trình riêng của bạn</h3>
        """, unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            travel_with = st.selectbox("Bạn đi du lịch với ai?", 
                                      ["Gia đình", "Bạn bè", "Cặp đôi", "Một mình"],
                                      key="home_travel")
            interests = st.multiselect("Sở thích của bạn", 
                                      ["Thiên nhiên", "Văn hóa", "Ẩm thực", "Phiêu lưu", "Tâm linh"],
                                      key="home_interests")
        
        with col_b:
            st.image("https://images.unsplash.com/photo-1518548419970-58e3b4079ab2?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80",
                    caption="Hành trình cá nhân hóa", use_column_width=True)
        
        if st.button("🎯 Tạo hành trình ngay", use_container_width=True, type="primary"):
            with st.spinner("Đang tạo hành trình độc đáo cho bạn..."):
                time.sleep(1.5)
                st.success("✅ Hành trình đã được tạo!")
                # Gọi AI recommendation
                try:
                    recommendation = ai_system.recommend_itinerary({
                        'travel_with': travel_with,
                        'interests': interests,
                        'duration': '3 ngày 2 đêm',
                        'budget': 'trung bình'
                    })
                    
                    st.markdown(f"""
                    <div style="background: #e0f7fa; padding: 20px; border-radius: 10px; margin-top: 20px; border: 1px solid #b2ebf2;">
                        <h4 style="color: #1a237e;">🎊 Gợi ý từ AI:</h4>
                        <p style="color: #37474f;">{recommendation[:250]}...</p>
                    </div>
                    """, unsafe_allow_html=True)
                except:
                    st.info("Hệ thống AI đang được cập nhật. Vui lòng thử lại sau.")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown("""
        <div class="custom-card">
            <h3 style="color: #1a237e; margin-bottom: 20px;">Bản đồ cảm xúc tương tác</h3>
        """, unsafe_allow_html=True)
        
        # Hiển thị bản đồ với nhiều marker màu sắc
        map_data = pd.DataFrame({
            'lat': [10.3755, 10.0850, 9.9522, 10.0123, 10.2000, 9.8000],
            'lon': [105.4339, 105.0881, 104.7758, 105.1234, 105.3000, 105.0000],
            'name': ['Núi Cấm', 'Châu Đốc', 'Rạch Giá', 'Hà Tiên', 'Long Xuyên', 'Phú Quốc'],
            'emotion': ['🏔️ Tĩnh tại', '🕌 Văn hóa', '🛶 Nhộn nhịp', '🌅 Lãng mạn', '🏙️ Đô thị', '🏝️ Thiên nhiên'],
            'color': ['#1e88e5', '#2e7d32', '#ffd54f', '#8d6e63', '#ab47bc', '#26a69a']
        })
        
        fig = px.scatter_mapbox(map_data, lat="lat", lon="lon", 
                               hover_name="name",
                               hover_data=["emotion"],
                               color="color",
                               color_discrete_map={c:c for c in map_data['color']},
                               zoom=8, height=400)
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab3:
        st.markdown("""
        <div class="custom-card">
            <h3 style="color: #1a237e; margin-bottom: 20px;">Khám phá câu chuyện di sản</h3>
            <div style="display: flex; gap: 20px; align-items: center;">
                <div style="flex: 1;">
        """, unsafe_allow_html=True)
        
        # Lấy danh sách câu chuyện
        if 'text_stories' in data and data['text_stories']:
            stories_list = data['text_stories'].get('text_stories', [])
            story_options = ["Chọn câu chuyện..."] + [f"{story.get('title', 'Không có tiêu đề')}" for story in stories_list[:5]]
        else:
            story_options = ["Chọn câu chuyện...", "Ký ức về Bác Tôn", "Huyền thoại Chùa Hang", "Hoàng hôn trên đồi Tức Dụp", "Chinh phục Núi Cô Tô", "Thiên đường biển đảo Nam Du"]
        
        story = st.selectbox("Chọn câu chuyện", story_options, key="home_story")
        
        if story != "Chọn câu chuyện...":
            if st.button("📖 Đọc ngay", use_container_width=True, type="primary"):
                col_story1, col_story2 = st.columns([1, 3])
                with col_story1:
                    st.image("https://images.unsplash.com/photo-1481627834876-b7833e8f5570?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80",
                            caption="", use_column_width=True)
                with col_story2:
                    st.markdown(f"""
                    <div style="background: linear-gradient(45deg, #1e88e5, #2e7d32); 
                                padding: 20px; 
                                border-radius: 10px;
                                color: white;
                                box-shadow: 0 5px 15px rgba(0,0,0,0.1);">
                        <h4>📚 {story}</h4>
                        <p>Mỗi câu chuyện là một hành trình khám phá văn hóa, lịch sử và con người An Giang - Kiên Giang. Truyện kể di sản cung cấp góc nhìn sâu sắc về 45 địa điểm du lịch nổi bật.</p>
                        <p><b>Thời gian đọc:</b> 2-3 phút | <b>Số chữ:</b> 100-200 chữ</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Hiển thị preview nội dung
                    st.markdown("""
                    <div style="background: #e0f7fa; padding: 15px; border-radius: 10px; margin-top: 15px; border: 1px solid #b2ebf2;">
                        <h5>📄 Nội dung mẫu:</h5>
                        <p>Khám phá những câu chuyện hấp dẫn về vùng đất và con người An Giang - Kiên Giang. Từ truyền thuyết dân gian đến những câu chuyện lịch sử, mỗi địa điểm đều ẩn chứa những câu chuyện thú vị đang chờ được khám phá...</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("""
                </div>
                <div style="flex: 1;">
                    <img src="https://images.unsplash.com/photo-1481627834876-b7833e8f5570?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80" 
                         style="width: 100%; border-radius: 10px; border: 2px solid #b2ebf2;">
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Gallery hình ảnh
    st.markdown("<h2 class='section-header'>📸 KHÁM PHÁ QUA HÌNH ẢNH</h2>", unsafe_allow_html=True)
    
    gallery_cols = st.columns(4)
    gallery_images = [
        "https://images.unsplash.com/photo-1552465011-b4e30bf7349d?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80",
        "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80",
        "https://images.unsplash.com/photo-1534008897995-27a23e859048?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80",
        "https://images.unsplash.com/photo-1518548419970-58e3b4079ab2?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80"
    ]
    
    for idx, col in enumerate(gallery_cols):
        with col:
            st.image(gallery_images[idx], use_column_width=True)

elif page == "module1":
    show_personalization_module(data, ai_system)

elif page == "module2":
    show_emotion_map_module(data)

elif page == "module3":
    show_text_stories_module(data)

elif page == "module4":
    show_feedback_module()

elif page == "dashboard":
    st.markdown("""
    <div class="dashboard-header">
        <h1 style="color: white; margin: 0;">📊 DASHBOARD TỔNG HỢP</h1>
        <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0;">Theo dõi và phân tích dữ liệu du lịch</p>
    </div>
    """, unsafe_allow_html=True)
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="kpi-card">
            <h3 style="color: #1a237e; margin: 0;">👥</h3>
            <h2 style="color: #1e88e5; margin: 10px 0;">87%</h2>
            <p style="color: #37474f; margin: 0;">Người dùng hoàn thành</p>
            <p style="color: #2e7d32; margin: 5px 0;">▲ 5%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="kpi-card">
            <h3 style="color: #1a237e; margin: 0;">⏱️</h3>
            <h2 style="color: #1e88e5; margin: 10px 0;">14m32s</h2>
            <p style="color: #37474f; margin: 0;">Thời gian trung bình</p>
            <p style="color: #2e7d32; margin: 5px 0;">▲ 2m18s</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="kpi-card">
            <h3 style="color: #1a237e; margin: 0;">📖</h3>
            <h2 style="color: #1e88e5; margin: 10px 0;">45</h2>
            <p style="color: #37474f; margin: 0;">Câu chuyện di sản</p>
            <p style="color: #2e7d32; margin: 5px 0;">▲ 5 câu chuyện</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="kpi-card">
            <h3 style="color: #1a237e; margin: 0;">⭐</h3>
            <h2 style="color: #1e88e5; margin: 10px 0;">92%</h2>
            <p style="color: #37474f; margin: 0;">Đánh giá hài lòng</p>
            <p style="color: #2e7d32; margin: 5px 0;">▲ 4%</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h3 style='text-align: center; color: #1a237e;'>📈 Phân bố đánh giá</h3>", unsafe_allow_html=True)
        ratings = pd.DataFrame({
            'Sao': ['⭐', '⭐⭐', '⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'],
            'Số lượng': [50, 150, 300, 850, 1200]
        })
        fig = px.bar(ratings, x='Sao', y='Số lượng', 
                     color='Số lượng',
                     color_continuous_scale=['#b2ebf2', '#4fc3f7', '#1e88e5', '#0d47a1'],
                     title="")
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("<h3 style='text-align: center; color: #1a237e;'>🎯 Loại hình du lịch</h3>", unsafe_allow_html=True)
        travel_types = pd.DataFrame({
            'Loại': ['Gia đình', 'Cặp đôi', 'Bạn bè', 'Một mình'],
            'Tỷ lệ': [45, 30, 20, 5],
            'Màu sắc': ['#1e88e5', '#2e7d32', '#ffd54f', '#8d6e63']
        })
        fig = px.pie(travel_types, values='Tỷ lệ', names='Loại',
                     color='Màu sắc',
                     title="",
                     hole=0.4)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    # Truyện kể nổi bật
    st.markdown("<h3 style='margin-top: 30px; color: #1a237e;'>📚 TRUYỆN KỂ NỔI BẬT</h3>", unsafe_allow_html=True)
    
    featured_stories = [
        {"title": "Ký ức về Bác Tôn", "views": 1250, "rating": 4.8, "emoji": "👴"},
        {"title": "Huyền thoại Chùa Hang", "views": 980, "rating": 4.7, "emoji": "🕉️"},
        {"title": "Hoàng hôn trên đồi Tức Dụp", "views": 1560, "rating": 4.9, "emoji": "🌅"},
    ]
    
    for story in featured_stories:
        stars = "⭐" * int(story['rating'])
        st.markdown(f"""
        <div style="background: white; 
                    padding: 20px; 
                    border-radius: 15px; 
                    margin-bottom: 15px;
                    box-shadow: 0 3px 10px rgba(30, 136, 229, 0.1);
                    border-left: 4px solid #1e88e5;">
            <div style="display: flex; align-items: center; gap: 15px;">
                <div style="font-size: 2rem;">{story['emoji']}</div>
                <div style="flex: 1;">
                    <h4 style="margin: 0; color: #1a237e;">{story['title']} {stars}</h4>
                    <p style="margin: 5px 0 0 0; color: #37474f;">👁️‍🗨️ {story['views']} lượt xem | ⭐ {story['rating']}/5</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Feedback với avatar
    st.markdown("<h3 style='margin-top: 30px; color: #1a237e;'>💬 Đánh giá gần đây</h3>", unsafe_allow_html=True)
    
    feedbacks = [
        {"user": "Nguyễn Văn A", "comment": "Hành trình gia đình tuyệt vời! Con tôi rất thích.", "rating": 5, "avatar": "👨‍👩‍👧"},
        {"user": "Trần Thị B", "comment": "Truyện kể di sản rất chân thật và cảm động.", "rating": 4, "avatar": "👩"},
        {"user": "Lê Văn C", "comment": "Bản đồ cảm xúc giúp tôi chọn đúng điểm đến mong muốn.", "rating": 5, "avatar": "🧑‍💼"},
    ]
    
    for fb in feedbacks:
        stars = "⭐" * fb['rating']
        st.markdown(f"""
        <div style="background: white; 
                    padding: 20px; 
                    border-radius: 15px; 
                    margin-bottom: 15px;
                    box-shadow: 0 3px 10px rgba(30, 136, 229, 0.1);
                    border-left: 4px solid #1e88e5;">
            <div style="display: flex; align-items: center; gap: 15px;">
                <div style="font-size: 2rem;">{fb['avatar']}</div>
                <div>
                    <h4 style="margin: 0; color: #1a237e;">{fb['user']} {stars}</h4>
                    <p style="margin: 5px 0 0 0; color: #37474f;">{fb['comment']}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

elif page == "ai_advisor":
    st.markdown("""
    <div class="ai-header">
        <h1 style="color: white; margin: 0; font-size: 2.8rem;">🤖 AI TƯ VẤN THÔNG MINH</h1>
        <p style="color: rgba(255,255,255,0.9); margin: 15px 0 0 0; font-size: 1.2rem;">
        Hệ thống AI phân tích và gợi ý hành trình tối ưu
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Input section với design đẹp
    st.markdown("""
    <div class="custom-card">
        <h3 style="color: #1a237e; margin-bottom: 25px; text-align: center;">
        📝 THÔNG TIN CỦA BẠN
        </h3>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.slider("🎂 Tuổi của bạn", 18, 70, 25, help="Tuổi ảnh hưởng đến loại hình du lịch phù hợp")
        budget = st.select_slider("💰 Mức ngân sách", 
                                 options=["Tiết kiệm", "Trung bình", "Thoải mái", "Cao cấp"],
                                 value="Trung bình")
        season = st.selectbox("🌤️ Mùa du lịch", 
                             ["Mùa khô (T11-T4)", "Mùa mưa (T5-T10)", "Mùa nước nổi (T8-T11)"])
    
    with col2:
        companions = st.multiselect("👥 Đi cùng", 
                                   ["Trẻ em", "Người lớn tuổi", "Bạn bè", "Người yêu", "Đồng nghiệp"])
        pace = st.select_slider("🚶‍♂️ Nhịp độ", 
                               options=["Nhẹ nhàng", "Vừa phải", "Nhanh", "Cực nhanh"],
                               value="Vừa phải")
        special_requests = st.text_area("💭 Yêu cầu đặc biệt", 
                                       placeholder="Ví dụ: Ăn chay, Xe lăn, Dị ứng...")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Nút tư vấn với hiệu ứng
    if st.button("🤖 NHẬN TƯ VẤN AI NGAY", 
                 use_container_width=True,
                 type="primary"):
        
        with st.spinner("AI đang phân tích và tạo hành trình tối ưu..."):
            time.sleep(2)
            
            # Tạo recommendation từ AI
            try:
                recommendation = ai_system.get_ai_recommendation({
                    'age': age,
                    'budget': budget,
                    'season': season,
                    'companions': companions,
                    'pace': pace,
                    'special_requests': special_requests
                })
                
                # Hiển thị kết quả với animation
                st.balloons()
                st.success("✅ Đã tạo xong hành trình tối ưu!")
                
                # Hiển thị kết quả trong tabs đẹp
                st.markdown("""
                <div style="background: linear-gradient(135deg, #1e88e5 0%, #2e7d32 100%); 
                            padding: 20px; 
                            border-radius: 15px;
                            color: white;
                            margin: 20px 0;
                            box-shadow: 0 10px 25px rgba(0,0,0,0.2);">
                    <h2 style="color: white; margin: 0;">🎯 HÀNH TRÌNH ĐƯỢC ĐỀ XUẤT</h2>
                    <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0;">
                    Dựa trên phân tích AI của {age} tuổi, ngân sách {budget.lower()}, đi {season.lower()}
                    </p>
                </div>
                """.format(age=age, budget=budget, season=season), unsafe_allow_html=True)
                
                tabs = st.tabs(["📅 Lịch trình", "🗺️ Bản đồ", "📊 Phân tích AI"])
                
                with tabs[0]:
                    st.markdown("""
                    <div class="custom-card">
                        <h3 style="color: #1a237e;">📋 CHI TIẾT HÀNH TRÌNH</h3>
                    """, unsafe_allow_html=True)
                    st.write(recommendation.get('itinerary', 'Thông tin hành trình đang được cập nhật...'))
                    st.image("https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80",
                            caption="Hành trình được AI đề xuất", use_column_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                
                with tabs[1]:
                    st.markdown("""
                    <div class="custom-card">
                        <h3 style="color: #1a237e;">🗺️ BẢN ĐỒ HÀNH TRÌNH</h3>
                    """, unsafe_allow_html=True)
                    # Hiển thị bản đồ
                    m = folium.Map(location=[10.3755, 105.4339], zoom_start=9)
                    
                    # Thêm markers
                    locations = [
                        {"name": "Núi Cấm", "lat": 10.3755, "lng": 105.4339},
                        {"name": "Châu Đốc", "lat": 10.0850, "lng": 105.0881},
                        {"name": "Rạch Giá", "lat": 9.9522, "lng": 104.7758},
                        {"name": "Hà Tiên", "lat": 10.0123, "lng": 105.1234}
                    ]
                    
                    colors = ['blue', 'green', 'orange', 'purple']
                    for idx, loc in enumerate(locations):
                        folium.Marker(
                            location=[loc['lat'], loc['lng']],
                            popup=loc['name'],
                            icon=folium.Icon(color=colors[idx], icon='info-sign')
                        ).add_to(m)
                    
                    # Vẽ đường đi
                    folium.PolyLine(
                        [[loc['lat'], loc['lng']] for loc in locations],
                        color="#1e88e5",
                        weight=2.5,
                        opacity=0.8
                    ).add_to(m)
                    
                    folium_static(m, width=800, height=500)
                    st.markdown("</div>", unsafe_allow_html=True)
                
                with tabs[2]:
                    st.markdown("""
                    <div class="custom-card">
                        <h3 style="color: #1a237e;">📊 PHÂN TÍCH AI</h3>
                    """, unsafe_allow_html=True)
                    
                    # Phân tích AI
                    col_anal1, col_anal2 = st.columns(2)
                    
                    with col_anal1:
                        st.markdown("#### 📈 Độ phù hợp:")
                        st.markdown("""
                        <div style="background: #e0f7fa; padding: 15px; border-radius: 10px; border: 1px solid #b2ebf2;">
                            <p style="color: #1a237e;">🎯 <b>Phù hợp sở thích:</b> 92%</p>
                            <p style="color: #1a237e;">⏱️ <b>Tối ưu thời gian:</b> 88%</p>
                            <p style="color: #1a237e;">🚶 <b>Phù hợp thể lực:</b> 85%</p>
                            <p style="color: #1a237e;">😊 <b>Độ hài lòng dự đoán:</b> 90%</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_anal2:
                        # Biểu đồ radar
                        categories = ['Sở thích', 'Thời gian', 'Thể lực', 'Văn hóa', 'Giải trí']
                        values = [92, 88, 85, 90, 87]
                        
                        fig = go.Figure(data=go.Scatterpolar(
                            r=values,
                            theta=categories,
                            fill='toself',
                            fillcolor='rgba(30, 136, 229, 0.3)',
                            line=dict(color='#1e88e5', width=3),
                            name='Độ phù hợp'
                        ))
                        
                        fig.update_layout(
                            polar=dict(
                                radialaxis=dict(
                                    visible=True,
                                    range=[0, 100],
                                    tickfont=dict(size=10)
                                ),
                                bgcolor='rgba(0,0,0,0)'
                            ),
                            showlegend=False,
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)'
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Recommendation từ AI
                    st.markdown("#### 💡 GỢI Ý TỪ AI:")
                    st.info("""
                    - 🏨 **Chỗ ở**: Nên đặt trước 2-4 tuần để có nhiều lựa chọn
                    - 🚗 **Di chuyển**: Thuê xe máy để linh hoạt khám phá
                    - 🍽️ **Ẩm thực**: Thử lẩu mắm và bánh xèo đặc sản
                    - ⚠️ **Lưu ý**: Mang theo thuốc chống muỗi vào mùa mưa
                    - 📅 **Thời điểm**: Sáng sớm và chiều tối là thời điểm đẹp nhất để tham quan
                    """)
                    
                    # Phân bổ ngân sách không số tiền
                    st.markdown("#### 💰 GỢI Ý PHÂN BỔ NGÂN SÁCH:")
                    st.markdown("""
                    - **Chỗ ở**: 35-45% ngân sách
                    - **Ăn uống**: 25-30% ngân sách  
                    - **Di chuyển**: 15-20% ngân sách
                    - **Vé tham quan**: 10-15% ngân sách
                    - **Chi phí khác**: 5-10% ngân sách
                    """)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
            
            except Exception as e:
                st.error(f"Không thể tạo hành trình: {e}")
                st.info("Vui lòng thử lại với thông tin khác hoặc liên hệ hỗ trợ.")
                
# ============================================
# FOOTER NÂNG CẤP - MÀU XANH MIỀN TÂY
# ============================================

st.markdown("---")

footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.markdown("""
    <div style="text-align: center; background: #e0f7fa; padding: 20px; border-radius: 15px; border: 1px solid #b2ebf2;">
        <h4 style="color: #1a237e;">🏆 GIẢI THƯỞNG</h4>
        <p style="color: #37474f;">STEM TIN – 12C1 </p>
        <p style="color: #37474f;">THPT HOA LAC </p>
        <img src="https://img.icons8.com/color/96/000000/trophy.png" width="60" style="filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.2));">
    </div>
    """, unsafe_allow_html=True)

with footer_col2:
    st.markdown("""
    <div style="text-align: center; background: #e0f7fa; padding: 20px; border-radius: 15px; border: 1px solid #b2ebf2;">
        <h4 style="color: #1a237e;">🤝 ĐỐI TÁC</h4>
        <p style="color: #37474f;">Sở Du Lịch An Giang</p>
        <p style="color: #37474f;">Sở GD&ĐT An Giang</p>
        <p style="color: #37474f;">Doanh nghiệp du lịch</p>
    </div>
    """, unsafe_allow_html=True)

with footer_col3:
    st.markdown("""
    <div style="text-align: center; background: #e0f7fa; padding: 20px; border-radius: 15px; border: 1px solid #b2ebf2;">
        <h4 style="color: #1a237e;">📞 LIÊN HỆ</h4>
        <p style="color: #37474f;">📧 dv1122@gmail.com</p>
        <p style="color: #37474f;">🌐 www.angiangstem.edu.vn</p>
        <p style="color: #37474f;">📱 0296 123 4567</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #1e88e5 0%, #2e7d32 100%); 
            border-radius: 15px; margin-top: 3rem; color: white; box-shadow: 0 10px 25px rgba(0,0,0,0.2);">
    <p style="font-size: 1.1rem; margin: 0; font-weight: bold;">© 2026 Dự án STEM Tin Học - An Giang</p>
    <p style="font-size: 0.9rem; margin: 10px 0 0 0; opacity: 0.9;">
    "Miền Tây hôm nay - Hành trình của bạn"
    </p>
    <div style="margin-top: 15px;">
        <span style="margin: 0 10px; font-size: 1.5rem;">🌊</span>
        <span style="margin: 0 10px; font-size: 1.5rem;">⛰️</span>
        <span style="margin: 0 10px; font-size: 1.5rem;">🚣</span>
        <span style="margin: 0 10px; font-size: 1.5rem;">🌾</span>
        <span style="margin: 0 10px; font-size: 1.5rem;">🐟</span>
    </div>
</div>
""", unsafe_allow_html=True)