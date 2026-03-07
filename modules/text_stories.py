import streamlit as st
import json
import pandas as pd
import folium
from streamlit_folium import folium_static

def show_text_stories_module(data):
    """Hiển thị module kể chuyện bằng văn bản"""
    
    st.markdown("""
    <div class="ai-header">
        <h1 style="color: white; margin: 0; font-size: 2.8rem;">📖 TRUYỆN KỂ DI SẢN</h1>
        <p style="color: rgba(255,255,255,0.9); margin: 15px 0 0 0; font-size: 1.2rem;">
        Khám phá những câu chuyện hấp dẫn về vùng đất và con người An Giang - Kiên Giang
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Khởi tạo session state nếu chưa có
    if 'selected_story' not in st.session_state:
        st.session_state.selected_story = None
    if 'filtered_stories' not in st.session_state:
        st.session_state.filtered_stories = []
    
    # Lấy dữ liệu
    stories = []
    locations_list = []
    
    try:
        if 'text_stories' in data and isinstance(data['text_stories'], dict):
            stories = data['text_stories'].get('text_stories', [])
        elif 'text_stories' in data and isinstance(data['text_stories'], list):
            stories = data['text_stories']
        
        if 'locations' in data and isinstance(data['locations'], dict):
            locations_list = data['locations'].get('locations', [])
        elif 'locations' in data and isinstance(data['locations'], list):
            locations_list = data['locations']
    except Exception as e:
        st.error(f"Lỗi khi tải dữ liệu: {e}")
        stories = []
        locations_list = []
    
    # Tạo layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div class="custom-card">
            <h3 style="color: #1a237e; margin-bottom: 20px;">🔍 TÌM CÂU CHUYỆN</h3>
        """, unsafe_allow_html=True)
        
        # Bộ lọc
        search_term = st.text_input("Tìm kiếm câu chuyện:", placeholder="Nhập từ khóa...")
        
        # Lọc theo địa điểm
        location_options = ["Tất cả địa điểm"] + [loc["name"] for loc in locations_list]
        selected_location = st.selectbox("Lọc theo địa điểm:", location_options)
        
        # Lọc theo tác giả
        if stories:
            all_authors = ["Tất cả tác giả"] + list(set([story.get('author', 'Không rõ') for story in stories]))
            selected_author = st.selectbox("Lọc theo tác giả:", all_authors)
        
        st.markdown("### 📊 THỐNG KÊ")
        st.metric("Số câu chuyện", len(stories))
        st.metric("Địa điểm có truyện", len(set([s.get('location_id', 0) for s in stories])))
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Danh sách câu chuyện nổi bật
        st.markdown("""
        <div class="custom-card">
            <h3 style="color: #1a237e; margin-bottom: 15px;">🌟 NỔI BẬT</h3>
        """, unsafe_allow_html=True)
        
        if stories:
            for i, story in enumerate(stories[:5]):
                if st.button(f"{i+1}. {story.get('title', 'Không có tiêu đề')[:30]}...", 
                           key=f"featured_{i}",
                           use_container_width=True):
                    st.session_state.selected_story = story
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        # Áp dụng bộ lọc
        filtered_stories = stories.copy() if stories else []
        
        if search_term:
            filtered_stories = [s for s in filtered_stories 
                              if search_term.lower() in s.get('title', '').lower() 
                              or search_term.lower() in s.get('content', '').lower()]
        
        if selected_location != "Tất cả địa điểm":
            location_id = next((loc['id'] for loc in locations_list 
                              if loc['name'] == selected_location), None)
            if location_id:
                filtered_stories = [s for s in filtered_stories 
                                  if s.get('location_id') == location_id]
        
        if selected_author != "Tất cả tác giả":
            filtered_stories = [s for s in filtered_stories 
                              if s.get('author') == selected_author]
        
        # Lưu filtered_stories vào session state
        st.session_state.filtered_stories = filtered_stories
        
        # Hiển thị câu chuyện chi tiết
        if st.session_state.selected_story:
            selected_story = st.session_state.selected_story
            
            # Tạo card với HTML đơn giản
            st.markdown(f"""
            <div class="custom-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                    <h2 style="color: #1a237e; margin: 0;">{selected_story.get('title', '')}</h2>
                    <span style="background: #e0f7fa; padding: 5px 15px; border-radius: 20px; font-size: 0.9rem;">
                        ⏱️ {selected_story.get('reading_time', '')}
                    </span>
                </div>
            """, unsafe_allow_html=True)
            
            # Hiển thị nội dung bằng markdown thay vì HTML
            st.markdown("#### 📖 NỘI DUNG")
            st.markdown(f"""
            <div style="background: #f5f9ff; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 4px solid #1e88e5;">
                <p style="color: #37474f; line-height: 1.8; font-size: 1.1rem;">
                    {selected_story.get('content', '')}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Thông tin tác giả và nguồn
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; color: #666; font-size: 0.9rem;">
                <div>
                    <strong>✍️ Tác giả:</strong> {selected_story.get('author', 'Không rõ')}
                </div>
                <div>
                    <strong>📚 Nguồn:</strong> {selected_story.get('source', 'Sưu tầm')}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Kết thúc card
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Hiển thị thông tin địa điểm liên quan
            location_id = selected_story.get('location_id')
            if location_id and locations_list:
                related_location = next((loc for loc in locations_list if loc.get('id') == location_id), None)
                if related_location:
                    st.markdown("""
                    <div class="custom-card">
                        <h3 style="color: #1a237e; margin-bottom: 15px;">📍 ĐỊA ĐIỂM LIÊN QUAN</h3>
                    """, unsafe_allow_html=True)
                    
                    col_info, col_map = st.columns([2, 1])
                    
                    with col_info:
                        # Sử dụng try-except để tránh lỗi
                        try:
                            st.markdown(f"""
                            <h4 style="color: #1a237e;">{related_location.get('name', '')}</h4>
                            <p><strong>Tỉnh:</strong> {related_location.get('province', '')}</p>
                            <p><strong>Quận/Huyện:</strong> {related_location.get('district', '')}</p>
                            <p><strong>Thời điểm tốt nhất:</strong> {related_location.get('best_time', '')}</p>
                            <p><strong>Cảm xúc:</strong> {' '.join(related_location.get('emotions', []))}</p>
                            """, unsafe_allow_html=True)
                        except Exception as e:
                            st.error(f"Lỗi hiển thị thông tin địa điểm: {e}")
                    
                    with col_map:
                        try:
                            # Kiểm tra coordinates
                            if 'coordinates' in related_location:
                                lat = related_location['coordinates'].get('lat', 10.3755)
                                lng = related_location['coordinates'].get('lng', 105.4339)
                                m = folium.Map(location=[lat, lng], zoom_start=12)
                                folium.Marker(
                                    [lat, lng],
                                    popup=related_location.get('name', ''),
                                    icon=folium.Icon(color='blue', icon='info-sign')
                                ).add_to(m)
                                folium_static(m, width=200, height=200)
                            else:
                                st.info("Không có thông tin tọa độ")
                        except Exception as e:
                            st.info("Không thể hiển thị bản đồ")
                    
                    st.markdown("</div>", unsafe_allow_html=True)
        else:
            # Hiển thị hướng dẫn nếu chưa chọn câu chuyện
            st.info("👈 Vui lòng chọn một câu chuyện từ danh sách bên trái hoặc từ danh sách bên dưới để bắt đầu đọc.")
        
        # Danh sách tất cả câu chuyện (đã lọc)
        st.markdown(f"""
        <div class="custom-card">
            <h3 style="color: #1a237e; margin-bottom: 20px;">📚 TẤT CẢ CÂU CHUYỆN ({len(filtered_stories)})</h3>
        """, unsafe_allow_html=True)
        
        if filtered_stories:
            for i, story in enumerate(filtered_stories):
                # Tạo expander cho mỗi câu chuyện
                with st.expander(f"📖 {story.get('title')} - ⏱️ {story.get('reading_time', '')}", expanded=False):
                    # Hiển thị preview
                    st.markdown(f"**Tác giả:** {story.get('author', 'Không rõ')}")
                    st.markdown(f"**Nội dung:** {story.get('content', '')[:200]}...")
                    st.markdown(f"**Nguồn:** {story.get('source', 'Sưu tầm')}")
                    
                    # Nút "Đọc toàn bộ" - sửa lại để hoạt động đúng
                    if st.button("📖 Đọc toàn bộ", key=f"read_full_{i}"):
                        st.session_state.selected_story = story
                        st.rerun()
        
        else:
            st.info("Không tìm thấy câu chuyện nào phù hợp với bộ lọc.")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Phần chia sẻ và lưu trữ
    st.markdown("""
    <div class="custom-card">
        <h3 style="color: #1a237e; margin-bottom: 15px;">📤 CHIA SẺ & LƯU TRỮ</h3>
        <div style="display: flex; gap: 15px; justify-content: center;">
            <button onclick="alert('Tính năng đang phát triển')" style="padding: 10px 20px; background: #1e88e5; color: white; border: none; border-radius: 5px; cursor: pointer;">
                📥 Tải PDF
            </button>
            <button onclick="alert('Tính năng đang phát triển')" style="padding: 10px 20px; background: #2e7d32; color: white; border: none; border-radius: 5px; cursor: pointer;">
                📧 Gửi email
            </button>
            <button onclick="alert('Tính năng đang phát triển')" style="padding: 10px 20px; background: #ffd54f; color: #333; border: none; border-radius: 5px; cursor: pointer;">
                🔖 Lưu vào yêu thích
            </button>
        </div>
    </div>
    """, unsafe_allow_html=True)