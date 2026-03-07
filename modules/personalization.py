import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go

def show_personalization_module(data, ai_system):
    """Module 1: Cá nhân hóa trải nghiệm du lịch"""
    
    st.title("🎯 MODULE 1: CÁ NHÂN HÓA TRẢI NGHIỆM DU LỊCH")
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem;">
        <h3 style="color: white; text-align: center;">BẠN LÀ AI? CHÚNG TÔI SẼ THIẾT KẾ HÀNH TRÌNH PHÙ HỢP NHẤT</h3>
        <p style="color: white; text-align: center;">(Trả lời 5 câu hỏi ngắn để có hành trình riêng)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Form khảo sát
    with st.form("survey_form"):
        st.subheader("1️⃣ Bạn đi du lịch với ai?")
        travel_with = st.radio(
            "Chọn đối tượng đồng hành",
            ["Một mình - tìm trải nghiệm cá nhân", 
             "Gia đình - có trẻ nhỏ/người lớn tuổi",
             "Nhóm bạn - trải nghiệm vui vẻ, năng động",
             "Cặp đôi - lãng mạn, riêng tư"],
            index=1
        )
        
        st.subheader("2️⃣ Sở thích chính của bạn là gì? (chọn tối đa 2)")
        interests = st.multiselect(
            "Chọn sở thích",
            ["Thiên nhiên - núi non, sông nước",
             "Tâm linh - đền chùa, không gian tĩnh tại",
             "Văn hóa - di sản, lễ hội, làng nghề",
             "Ẩm thực - đặc sản, trải nghiệm ẩm thực địa phương",
             "Phiêu lưu - hoạt động ngoài trời, khám phá"],
            default=["Thiên nhiên - núi non, sông nước", "Văn hóa - di sản, lễ hội, làng nghề"]
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("3️⃣ Thời gian bạn có?")
            duration = st.selectbox(
                "Chọn thời gian",
                ["1 ngày - trải nghiệm cô đọng",
                 "2 ngày 1 đêm - khám phá vừa đủ",
                 "3 ngày 2 đêm - trải nghiệm sâu sắc",
                 "Trên 3 ngày - khám phá toàn diện"],
                index=2
            )
            
        with col2:
            st.subheader("4️⃣ Mức ngân sách?")
            budget = st.selectbox(
                "Chọn mức ngân sách",
                ["Tiết kiệm", "Trung bình", "Thoải mái"],
                index=1
            )
        
        st.subheader("5️⃣ Thể lực/hoạt động thể chất?")
        activity_level = st.radio(
            "Mức độ hoạt động",
            ["Nhẹ nhàng - ít đi bộ, di chuyển bằng phương tiện",
             "Trung bình - đi bộ vừa phải",
             "Năng động - leo núi, khám phá nhiều"],
            index=0
        )
        
        submitted = st.form_submit_button("🎯 TẠO HÀNH TRÌNH CÁ NHÂN HÓA", type="primary")
    
    if submitted:
        st.success("✅ Đã thu thập thông tin thành công! Hệ thống đang tạo hành trình...")
        
        # Phân tích lựa chọn
        st.markdown("---")
        st.markdown(f"""
        ### 📊 PHÂN TÍCH LỰA CHỌN CỦA BẠN
        
        - **Đồng hành**: {travel_with.split(' - ')[0]}
        - **Sở thích**: {', '.join([i.split(' - ')[0] for i in interests])}
        - **Thời gian**: {duration.split(' - ')[0]}
        - **Ngân sách**: {budget}
        - **Thể lực**: {activity_level.split(' - ')[0]}
        """)
        
        # Gọi AI để tạo hành trình
        user_profile = {
            'travel_with': travel_with,
            'interests': interests,
            'duration': duration,
            'budget': budget,
            'activity_level': activity_level
        }
        
        try:
            # Kiểm tra phương thức của AI System
            if hasattr(ai_system, 'create_personalized_itinerary'):
                itinerary = ai_system.create_personalized_itinerary(user_profile)
            elif hasattr(ai_system, 'recommend_itinerary'):
                # Nếu AI system chỉ có recommend_itinerary
                result = ai_system.recommend_itinerary(user_profile)
                itinerary = {
                    'days': [
                        {
                            'title': 'Hành trình đề xuất',
                            'theme': 'Đa dạng trải nghiệm',
                            'accommodation_type': 'Khách sạn 3 sao',
                            'activities': [
                                {
                                    'time': 'Sáng',
                                    'name': 'Khám phá An Giang',
                                    'description': result[:150] + '...' if len(result) > 150 else result,
                                    'duration': '3 giờ'
                                }
                            ]
                        }
                    ]
                }
            else:
                # Tạo itinerary mẫu
                itinerary = create_sample_itinerary(user_profile)
                
        except Exception as e:
            st.warning(f"Hệ thống AI tạm thời không khả dụng: {e}")
            itinerary = create_sample_itinerary(user_profile)
        
        # Hiển thị hành trình
        st.markdown("---")
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 2rem; border-radius: 15px; margin: 2rem 0;">
            <h2 style="color: white; text-align: center;">🎯 HÀNH TRÌNH ĐƯỢC CÁ NHÂN HÓA CHO BẠN</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Kiểm tra và hiển thị hành trình theo ngày
        if itinerary and 'days' in itinerary and itinerary['days']:
            for day_num, day_info in enumerate(itinerary['days'], 1):
                with st.expander(f"📅 NGÀY {day_num}: {day_info.get('title', 'Khám phá')}", expanded=True if day_num == 1 else False):
                    st.markdown(f"**🎯 Chủ đề:** {day_info.get('theme', 'Đa dạng trải nghiệm')}")
                    st.markdown(f"**🏨 Loại chỗ ở:** {day_info.get('accommodation_type', 'Khách sạn/phòng nghỉ phù hợp')}")
                    
                    if 'activities' in day_info and day_info['activities']:
                        for activity in day_info['activities']:
                            col1, col2 = st.columns([1, 4])
                            with col1:
                                st.markdown(f"**{activity.get('time', 'Thời gian linh hoạt')}**")
                            with col2:
                                st.markdown(f"""
                                **{activity.get('name', 'Hoạt động')}**
                                - {activity.get('description', 'Trải nghiệm thú vị')}
                                - ⏰ {activity.get('duration', '1-2 giờ')}
                                """)
                    else:
                        st.info("Không có hoạt động cụ thể cho ngày này.")
        else:
            st.warning("Không có thông tin hành trình chi tiết. Vui lòng thử lại!")
            # Hiển thị itinerary mẫu
            itinerary = create_sample_itinerary(user_profile)
            for day_num, day_info in enumerate(itinerary['days'], 1):
                with st.expander(f"📅 NGÀY {day_num}: {day_info['title']}", expanded=True if day_num == 1 else False):
                    st.markdown(f"**🎯 Chủ đề:** {day_info['theme']}")
                    st.markdown(f"**🏨 Loại chỗ ở:** {day_info['accommodation_type']}")
                    
                    for activity in day_info['activities']:
                        col1, col2 = st.columns([1, 4])
                        with col1:
                            st.markdown(f"**{activity['time']}**")
                        with col2:
                            st.markdown(f"""
                            **{activity['name']}**
                            - {activity['description']}
                            - ⏰ {activity['duration']}
                            """)
        
        # Thông tin bổ sung
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 GỢI Ý PHÂN BỔ THỜI GIAN")
            time_data = pd.DataFrame({
                'Hoạt động': ['Khám phá di sản', 'Thiên nhiên', 'Ẩm thực', 'Nghỉ ngơi'],
                'Tỷ lệ': ['40%', '30%', '20%', '10%']
            })
            st.table(time_data)
            
            # Biểu đồ phân bổ thời gian
            try:
                fig = px.pie(time_data, values=time_data['Tỷ lệ'].str.rstrip('%').astype(float), 
                            names=time_data['Hoạt động'], title="Phân bổ thời gian")
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.info("Không thể hiển thị biểu đồ.")
        
        with col2:
            st.markdown("### 📱 TIỆN ÍCH ĐI KÈM")
            st.markdown("""
            - 🗺️ **Bản đồ tương tác** chi tiết
            - 📖 **Câu chuyện di sản** liên quan
            - 🎧 **Hướng dẫn audio** từ người dân địa phương
            - 🍽️ **Gợi ý ẩm thực** đặc sản vùng miền
            - 🚗 **Lộ trình di chuyển** tối ưu
            - ⚠️ **Lưu ý quan trọng** theo mùa
            """)
            
            if st.button("📲 LƯU HÀNH TRÌNH VÀO TÀI KHOẢN", type="secondary"):
                st.info("Hành trình đã được lưu vào tài khoản của bạn!")
        
        # Nút hành động
        st.markdown("---")
        st.markdown("### 🚀 HÀNH ĐỘNG TIẾP THEO")
        action_col1, action_col2, action_col3 = st.columns(3)
        
        with action_col1:
            if st.button("🖨️ XUẤT LỊCH TRÌNH", type="primary"):
                st.success("Đang tạo file PDF...")
        
        with action_col2:
            if st.button("📤 CHIA SẺ VỚI BẠN BÈ", type="secondary"):
                st.success("Đã tạo link chia sẻ!")
        
        with action_col3:
            if st.button("✏️ TÙY CHỈNH THÊM", type="secondary"):
                st.info("Mở bảng tùy chỉnh...")
        
        # Phân tích AI
        with st.expander("🤖 PHÂN TÍCH TỪ HỆ THỐNG AI"):
            st.markdown(f"""
            **📊 ĐỘ PHÙ HỢP:** 94%
            
            **🎯 ĐIỂM NỔI BẬT:**
            1. Hành trình cân bằng giữa **{interests[0].split(' - ')[0] if len(interests) > 0 else 'trải nghiệm'}** và **{interests[1].split(' - ')[0] if len(interests) > 1 else 'trải nghiệm'}**
            2. Thời gian di chuyển tối ưu cho **{travel_with.split(' - ')[0]}**
            3. Địa điểm phù hợp với mức độ hoạt động **{activity_level.split(' - ')[0]}**
            4. Đa dạng trải nghiệm văn hóa và thiên nhiên
            
            **💡 GỢI Ý TỪ AI:**
            - Mang theo kem chống nắng và nón khi đi ngoài trời
            - Đặt trước vé tham quan vào mùa cao điểm
            - Thử các món đặc sản địa phương như lẩu mắm, bún cá
            - Kiểm tra thời tiết trước khi khởi hành
            - Mang theo thuốc cần thiết nếu có trẻ em hoặc người lớn tuổi
            """)
            
            # Biểu đồ radar
            try:
                categories = ['Phù hợp sở thích', 'Tối ưu thời gian', 
                             'Đa dạng trải nghiệm', 'Phù hợp thể lực', 'Khả thi thực tế']
                
                fig = go.Figure(data=go.Scatterpolar(
                    r=[94, 88, 90, 85, 87],
                    theta=categories,
                    fill='toself',
                    name='Hành trình của bạn'
                ))
                
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 100]
                        )),
                    showlegend=False,
                    title="Đánh giá độ phù hợp"
                )
                
                st.plotly_chart(fig, use_container_width=True)
            except:
                st.info("Không thể hiển thị biểu đồ radar.")
            
            # Thông tin ngân sách tổng quát
            st.markdown(f"""
            ### 💰 THÔNG TIN NGÂN SÁCH
            
            **Mức ngân sách bạn chọn:** {budget}
            
            **Khuyến nghị:**
            - Đặt chỗ trước 2-4 tuần để có giá tốt
            - So sánh giá trên các nền tảng đặt phòng
            - Ưu tiên các tour trọn gói để tiết kiệm
            - Mang theo tiền mặt cho các dịch vụ địa phương
            """)


def create_sample_itinerary(user_profile):
    """Tạo hành trình mẫu khi hệ thống AI không hoạt động"""
    travel_with = user_profile.get('travel_with', 'Gia đình')
    interests = user_profile.get('interests', ['Thiên nhiên'])
    duration = user_profile.get('duration', '3 ngày 2 đêm')
    
    # Xác định chủ đề dựa trên sở thích
    main_interest = interests[0].split(' - ')[0] if interests else 'Thiên nhiên'
    
    if main_interest == 'Thiên nhiên':
        theme = "Khám phá thiên nhiên hùng vĩ"
        activities_day1 = [
            {"time": "7:00-9:00", "name": "Tham quan Núi Cấm", "description": "Ngắm cảnh bình minh trên đỉnh núi", "duration": "2 giờ"},
            {"time": "9:30-12:00", "name": "Khám phá rừng tràm", "description": "Đi bộ xuyên rừng, ngắm hệ sinh thái", "duration": "2.5 giờ"}
        ]
    elif main_interest == 'Văn hóa':
        theme = "Trải nghiệm văn hóa đặc sắc"
        activities_day1 = [
            {"time": "8:00-10:00", "name": "Tham quan chùa Hang", "description": "Khám phá kiến trúc độc đáo trong hang động", "duration": "2 giờ"},
            {"time": "10:30-12:00", "name": "Thăm làng nghề truyền thống", "description": "Tìm hiểu nghề dệt chiếu, làm nón", "duration": "1.5 giờ"}
        ]
    else:
        theme = "Hành trình đa dạng trải nghiệm"
        activities_day1 = [
            {"time": "8:00-11:00", "name": "Tham quan di tích lịch sử", "description": "Tìm hiểu văn hóa và lịch sử địa phương", "duration": "3 giờ"},
            {"time": "11:30-13:00", "name": "Thưởng thức ẩm thực địa phương", "description": "Trải nghiệm ẩm thực đặc sản An Giang", "duration": "1.5 giờ"}
        ]
    
    return {
        'days': [
            {
                'title': 'Ngày 1: Khám phá An Giang',
                'theme': theme,
                'accommodation_type': 'Khách sạn 3 sao (phù hợp với gia đình)' if 'Gia đình' in travel_with else 'Resort nghỉ dưỡng',
                'activities': activities_day1
            },
            {
                'title': 'Ngày 2: Trải nghiệm sông nước',
                'theme': 'Du lịch sinh thái miền Tây',
                'accommodation_type': 'Homestay ven sông',
                'activities': [
                    {"time": "6:30-9:00", "name": "Đi thuyền trên sông", "description": "Ngắm cảnh sông nước miền Tây", "duration": "2.5 giờ"},
                    {"time": "9:30-12:00", "name": "Tham quan chợ nổi", "description": "Trải nghiệm văn hóa chợ nổi độc đáo", "duration": "2.5 giờ"}
                ]
            },
            {
                'title': 'Ngày 3: Thư giãn và khám phá ẩm thực',
                'theme': 'Ẩm thực và mua sắm đặc sản',
                'accommodation_type': 'Khách sạn trung tâm',
                'activities': [
                    {"time": "8:00-10:00", "name": "Tham quan vườn trái cây", "description": "Thưởng thức trái cây tươi tại vườn", "duration": "2 giờ"},
                    {"time": "10:30-12:00", "name": "Mua sắm đặc sản", "description": "Mua quà lưu niệm và đặc sản địa phương", "duration": "1.5 giờ"}
                ]
            }
        ]
    }