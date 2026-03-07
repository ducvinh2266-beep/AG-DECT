"""
Module 5: Đánh giá hài lòng thực
Chia sẻ trải nghiệm thật của bạn
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

def show_feedback_module():
    """Module 5: Hệ thống đánh giá và phản hồi"""
    
    st.title("⭐ MODULE 5: ĐÁNH GIÁ HÀI LÒNG THỰC")
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem;">
        <h3 style="color: #2c3e50; text-align: center;">CHIA SẺ TRẢI NGHIỆM THẬT CỦA BẠN</h3>
        <p style="color: #34495e; text-align: center;">"Mỗi đánh giá là một cơ hội để chúng tôi hoàn thiện dịch vụ"</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Phân theo tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Đánh giá mới", "📊 Thống kê", "🏆 Xếp hạng", "💡 Góp ý"])
    
    with tab1:
        st.markdown("### 📝 ĐÁNH GIÁ HÀNH TRÌNH CỦA BẠN")
        
        # Thông tin hành trình
        col_info1, col_info2 = st.columns(2)
        
        with col_info1:
            journey_type = st.selectbox(
                "Loại hành trình bạn vừa trải nghiệm",
                ["Văn hóa - Ẩm thực Gia đình", "Thiên nhiên - Phiêu lưu", 
                 "Tâm linh - Nghỉ dưỡng", "Biển đảo - Khám phá"]
            )
        
        with col_info2:
            journey_duration = st.selectbox(
                "Thời gian hành trình",
                ["1 ngày", "2 ngày 1 đêm", "3 ngày 2 đêm", "Trên 3 ngày"]
            )
        
        # Đánh giá hài lòng
        st.markdown("#### 🎯 ĐIỀU KHIẾN BẠN HÀI LÒNG NHẤT? (chọn tối đa 3)")
        
        satisfaction_options = [
            "Sự chân thành của người dân địa phương",
            "Ẩm thực đặc sắc, đúng vị truyền thống",
            "Hành trình phù hợp với gia đình có trẻ nhỏ",
            "Thông tin audio/video sống động",
            "Tính cá nhân hóa của lịch trình",
            "Dịch vụ hướng dẫn viên chuyên nghiệp",
            "Chất lượng phương tiện di chuyển",
            "Đa dạng trải nghiệm văn hóa"
        ]
        
        satisfaction_choices = st.multiselect(
            "Chọn những điểm bạn hài lòng",
            satisfaction_options,
            max_selections=3
        )
        
        # Điểm chưa hài lòng
        st.markdown("#### ⚠️ ĐIỀU BẠN CHƯA THOẢI MÃN? (chọn nếu có)")
        
        dissatisfaction_options = [
            "Phương tiện di chuyển giữa các điểm",
            "Chất lượng vệ sinh tại một số điểm",
            "Quá đông khách du lịch",
            "Thiếu hoạt động cho trẻ em tại một số điểm",
            "Thông tin thực tế khác website",
            "Giá cả không hợp lý",
            "Thiếu hướng dẫn viên địa phương",
            "Không gian nghỉ ngơi chưa tốt"
        ]
        
        dissatisfaction_choices = st.multiselect(
            "Chọn những điểm cần cải thiện",
            dissatisfaction_options
        )
        
        # Đánh giá chi tiết
        st.markdown("#### ⭐ ĐÁNH GIÁ CHI TIẾT")
        
        col_rating1, col_rating2, col_rating3, col_rating4, col_rating5 = st.columns(5)
        
        with col_rating1:
            service_rating = st.slider("Dịch vụ", 1, 5, 5, help="Đánh giá chất lượng dịch vụ")
            st.markdown(f"**{service_rating}/5**")
        
        with col_rating2:
            guide_rating = st.slider("Hướng dẫn", 1, 5, 4, help="Đánh giá hướng dẫn viên/audio guide")
            st.markdown(f"**{guide_rating}/5**")
        
        with col_rating3:
            food_rating = st.slider("Ẩm thực", 1, 5, 5, help="Đánh giá chất lượng ẩm thực")
            st.markdown(f"**{food_rating}/5**")
        
        with col_rating4:
            accommodation_rating = st.slider("Chỗ ở", 1, 5, 4, help="Đánh giá chất lượng chỗ ở")
            st.markdown(f"**{accommodation_rating}/5**")
        
        with col_rating5:
            value_rating = st.slider("Giá trị", 1, 5, 4, help="Đánh giá giá trị nhận được so với chi phí")
            st.markdown(f"**{value_rating}/5**")
        
        # Tính điểm trung bình
        avg_rating = (service_rating + guide_rating + food_rating + accommodation_rating + value_rating) / 5
        
        st.markdown(f"### 📊 ĐIỂM TRUNG BÌNH: **{avg_rating:.1f}/5.0**")
        
        # Góp ý chi tiết
        st.markdown("#### 💬 GÓP Ý CHI TIẾT")
        
        improvement_suggestions = st.text_area(
            "Ý kiến của bạn để chúng tôi cải thiện:",
            placeholder="Vui lòng chia sẻ chi tiết về trải nghiệm của bạn..."
        )
        
        # Góp ý cho địa phương
        st.markdown("#### 🏛️ GÓP Ý CHO ĐỊA PHƯƠNG (tùy chọn)")
        
        local_suggestions = st.text_area(
            "Thông điệp gửi đến chính quyền địa phương:",
            placeholder="Ví dụ: Cần thêm biển chỉ dẫn tại..., Cải thiện vệ sinh tại..., Tổ chức thêm hoạt động văn hóa..."
        )
        
        # Khảo sát cuối
        st.markdown("#### 🗳️ KHẢO SÁT CUỐI CÙNG")
        
        recommend = st.radio(
            "Bạn có giới thiệu An Giang - Kiên Giang cho người khác không?",
            ["Chắc chắn có - trải nghiệm tuyệt vời",
             "Có - với một số lưu ý nhỏ",
             "Chưa chắc - cần cải thiện vài điểm",
             "Không - trải nghiệm chưa tốt"],
            index=0
        )
        
        # Nút gửi đánh giá
        st.markdown("---")
        col_submit1, col_submit2, col_submit3 = st.columns([1, 2, 1])
        
        with col_submit2:
            if st.button("📤 GỬI ĐÁNH GIÁ", type="primary", use_container_width=True):
                # Lưu đánh giá
                feedback_data = {
                    "timestamp": datetime.now(),
                    "journey_type": journey_type,
                    "duration": journey_duration,
                    "satisfactions": satisfaction_choices,
                    "dissatisfactions": dissatisfaction_choices,
                    "ratings": {
                        "service": service_rating,
                        "guide": guide_rating,
                        "food": food_rating,
                        "accommodation": accommodation_rating,
                        "value": value_rating,
                        "average": avg_rating
                    },
                    "suggestions": improvement_suggestions,
                    "local_suggestions": local_suggestions,
                    "recommendation": recommend
                }
                
                # Hiển thị kết quả
                st.success("✅ Cảm ơn bạn đã gửi đánh giá!")
                st.balloons()
                
                # Hiển thị tóm tắt
                with st.expander("📋 XEM LẠI ĐÁNH GIÁ CỦA BẠN"):
                    st.json(feedback_data)
                
                # Khuyến mãi cảm ơn
                st.markdown("""
                <div style="background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%); padding: 1.5rem; border-radius: 10px; margin-top: 1rem;">
                    <h4 style="color: white; text-align: center;">🎁 ƯU ĐÃI CẢM ƠN!</h4>
                    <p style="color: white; text-align: center;">
                    Nhập mã <strong>FEEDBACK2024</strong> để được giảm 10% cho hành trình tiếp theo!
                    </p>
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 📊 THỐNG KÊ ĐÁNH GIÁ")
        
        # Tạo dữ liệu mẫu
        feedback_stats = {
            "Tổng số đánh giá": 2345,
            "Điểm trung bình": 4.7,
            "Tỉ lệ hài lòng (4-5 sao)": "92%",
            "Tỉ lệ giới thiệu": "94%",
            "Thời gian đánh giá TB": "3.2 phút"
        }
        
        # Hiển thị KPI
        col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
        
        with col_kpi1:
            st.metric("📊 Tổng đánh giá", f"{feedback_stats['Tổng số đánh giá']:,}")
        
        with col_kpi2:
            st.metric("⭐ Điểm TB", f"{feedback_stats['Điểm trung bình']}/5.0")
        
        with col_kpi3:
            st.metric("😊 Hài lòng", feedback_stats['Tỉ lệ hài lòng (4-5 sao)'])
        
        with col_kpi4:
            st.metric("📢 Giới thiệu", feedback_stats['Tỉ lệ giới thiệu'])
        
        # Biểu đồ phân phối đánh giá
        st.markdown("#### 📈 PHÂN PHỐI ĐÁNH GIÁ")
        
        rating_distribution = {
            "5 sao": 1450,
            "4 sao": 720,
            "3 sao": 125,
            "2 sao": 38,
            "1 sao": 12
        }
        
        rating_df = pd.DataFrame({
            "Sao": list(rating_distribution.keys()),
            "Số lượng": list(rating_distribution.values()),
            "Tỉ lệ": [f"{(v/sum(rating_distribution.values()))*100:.1f}%" 
                     for v in rating_distribution.values()]
        })
        
        fig = px.bar(rating_df, x="Sao", y="Số lượng", 
                    color="Sao", text="Tỉ lệ",
                    title="Phân phối đánh giá theo sao")
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
        
        # Biểu đồ theo thời gian
        st.markdown("#### 📅 XU HƯỚNG THEO THỜI GIAN")
        
        # Tạo dữ liệu mẫu theo tháng
        months = ["Tháng 1", "Tháng 2", "Tháng 3", "Tháng 4", "Tháng 5", "Tháng 6"]
        monthly_data = {
            "Số đánh giá": [320, 380, 420, 450, 480, 295],
            "Điểm TB": [4.6, 4.7, 4.8, 4.7, 4.8, 4.6]
        }
        
        monthly_df = pd.DataFrame({
            "Tháng": months * 2,
            "Giá trị": monthly_data["Số đánh giá"] + monthly_data["Điểm TB"],
            "Chỉ số": ["Số đánh giá"] * len(months) + ["Điểm TB"] * len(months)
        })
        
        fig = px.line(monthly_df, x="Tháng", y="Giá trị", color="Chỉ số",
                     markers=True, title="Xu hướng đánh giá 6 tháng gần nhất")
        
        # Thêm secondary y-axis cho điểm TB
        fig.update_layout(
            yaxis=dict(title="Số đánh giá"),
            yaxis2=dict(
                title="Điểm TB",
                overlaying="y",
                side="right",
                range=[4.0, 5.0]
            )
        )
        
        # Cập nhật trace thứ 2 (điểm TB) dùng yaxis2
        fig.data[1].update(yaxis="y2")
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Phân tích theo loại hành trình
        st.markdown("#### 🎯 PHÂN TÍCH THEO LOẠI HÀNH TRÌNH")
        
        journey_analysis = {
            "Văn hóa - Ẩm thực": {"count": 850, "rating": 4.8},
            "Thiên nhiên - Phiêu lưu": {"count": 720, "rating": 4.7},
            "Tâm linh - Nghỉ dưỡng": {"count": 450, "rating": 4.6},
            "Biển đảo - Khám phá": {"count": 325, "rating": 4.9}
        }
        
        journey_df = pd.DataFrame([
            {
                "Loại hành trình": key,
                "Số đánh giá": value["count"],
                "Điểm TB": value["rating"]
            }
            for key, value in journey_analysis.items()
        ])
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=journey_df["Loại hành trình"],
            y=journey_df["Số đánh giá"],
            name="Số đánh giá",
            marker_color='lightsalmon'
        ))
        
        fig.add_trace(go.Scatter(
            x=journey_df["Loại hành trình"],
            y=journey_df["Điểm TB"],
            name="Điểm TB",
            yaxis="y2",
            mode="lines+markers",
            line=dict(color='darkblue', width=3)
        ))
        
        fig.update_layout(
            title="Phân tích theo loại hành trình",
            xaxis_title="Loại hành trình",
            yaxis=dict(
                title="Số đánh giá",
                titlefont=dict(color="lightsalmon"),
                tickfont=dict(color="lightsalmon")
            ),
            yaxis2=dict(
                title="Điểm TB",
                titlefont=dict(color="darkblue"),
                tickfont=dict(color="darkblue"),
                anchor="x",
                overlaying="y",
                side="right",
                range=[4.0, 5.0]
            ),
            legend=dict(x=0.1, y=1.1, orientation="h")
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("### 🏆 XẾP HẠNG & ĐÁNH GIÁ TIÊU BIỂU")
        
        # Xếp hạng các điểm đến
        st.markdown("#### 📍 TOP 10 ĐIỂM ĐẾN ĐƯỢC ĐÁNH GIÁ CAO")
        
        top_locations = [
            {"name": "Núi Cấm", "rating": 4.9, "reviews": 345},
            {"name": "Phú Quốc", "rating": 4.9, "reviews": 420},
            {"name": "Rừng Tràm Trà Sư", "rating": 4.8, "reviews": 289},
            {"name": "Miếu Bà Chúa Xứ", "rating": 4.8, "reviews": 312},
            {"name": "Chùa Hang (Phước Điền Tự)", "rating": 4.7, "reviews": 256},
            {"name": "Làng Chăm Châu Giang", "rating": 4.7, "reviews": 198},
            {"name": "Thánh đường Jamiul Azhar", "rating": 4.6, "reviews": 167},
            {"name": "Di chỉ Óc Eo", "rating": 4.6, "reviews": 145},
            {"name": "Hòn Phụ Tử", "rating": 4.5, "reviews": 178},
            {"name": "U Minh Thượng", "rating": 4.5, "reviews": 156}
        ]
        
        top_df = pd.DataFrame(top_locations)
        
        # Hiển thị bảng xếp hạng
        st.dataframe(
            top_df.style
            .background_gradient(subset=['rating'], cmap='YlOrRd')
            .format({'rating': '{:.1f}', 'reviews': '{:,}'})
            .set_properties(**{'text-align': 'center'}),
            use_container_width=True
        )
        
        # Đánh giá tiêu biểu
        st.markdown("#### 🌟 ĐÁNH GIÁ TIÊU BIỂU")
        
        featured_reviews = [
            {
                "user": "Nguyễn Thị Mai",
                "rating": 5,
                "journey": "Văn hóa - Ẩm thực Gia đình",
                "comment": "Hành trình tuyệt vời! Con tôi rất thích được tự tay dệt thổ cẩm. Audio guide từ người dân rất chân thật và cảm động.",
                "date": "2 ngày trước",
                "helpful": 45
            },
            {
                "user": "Trần Văn Nam",
                "rating": 4,
                "journey": "Thiên nhiên - Phiêu lưu",
                "comment": "Trải nghiệm leo núi Cấm rất thú vị. Tuy nhiên cần cải thiện dịch vụ ăn uống trên núi. Hướng dẫn viên nhiệt tình.",
                "date": "1 tuần trước",
                "helpful": 32
            },
            {
                "user": "Lê Hoàng Anh",
                "rating": 5,
                "journey": "Biển đảo - Khám phá",
                "comment": "Phú Quốc quá đẹp! Hệ thống audio guide giúp tôi hiểu sâu về văn hóa địa phương. Sẽ quay lại vào mùa sau.",
                "date": "3 tuần trước",
                "helpful": 67
            }
        ]
        
        for review in featured_reviews:
            with st.container():
                st.markdown(f"""
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong>{review['user']}</strong> • {review['date']}
                        </div>
                        <div>
                            {'⭐' * review['rating']} ({review['rating']}/5)
                        </div>
                    </div>
                    <p style="color: #6c757d; font-size: 0.9rem; margin: 0.5rem 0;">
                        <em>Hành trình: {review['journey']}</em>
                    </p>
                    <p style="margin: 0.5rem 0;">
                        {review['comment']}
                    </p>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.5rem;">
                        <span>👍 {review['helpful']} người thấy hữu ích</span>
                        <button style="background: #007bff; color: white; border: none; padding: 0.25rem 0.75rem; border-radius: 5px;">
                            Hữu ích
                        </button>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Người đánh giá tích cực
        st.markdown("#### 🏅 TOP NGƯỜI ĐÁNH GIÁ TÍCH CỰC")
        
        top_reviewers = [
            {"name": "Phạm Văn Đạt", "reviews": 12, "helpful": 156},
            {"name": "Nguyễn Thị Hương", "reviews": 8, "helpful": 134},
            {"name": "Trần Quốc Bảo", "reviews": 7, "helpful": 98},
            {"name": "Lê Minh Châu", "reviews": 6, "helpful": 87},
            {"name": "Hoàng Văn Tú", "reviews": 5, "helpful": 76}
        ]
        
        reviewer_df = pd.DataFrame(top_reviewers)
        
        col_rev1, col_rev2 = st.columns([2, 1])
        
        with col_rev1:
            fig = px.bar(reviewer_df, x="name", y="reviews", 
                        color="helpful",
                        title="Top người đánh giá tích cực",
                        labels={"name": "Tên", "reviews": "Số đánh giá", "helpful": "Hữu ích"})
            st.plotly_chart(fig, use_container_width=True)
        
        with col_rev2:
            st.markdown("##### 🎁 QUÀ TẶNG TRI ÂN")
            st.markdown("""
            **Top 5 reviewer nhận được:**
            - 🏆 Giấy chứng nhận
            - 🎫 Voucher 500k
            - 🎁 Quà lưu niệm đặc biệt
            - 👑 Quyền lợi VIP
            """)
            
            if st.button("🏆 XEM CHI TIẾT CHƯƠNG TRÌNH"):
                st.info("""
                **Chương trình Reviewer Tích cực:**
                1. Đánh giá trên 5 hành trình
                2. Đánh giá chất lượng, chi tiết
                3. Tỷ lệ hữu ích cao
                4. Tích cực phản hồi
                """)
    
    with tab4:
        st.markdown("### 💡 HỆ THỐNG GÓP Ý & CẢI TIẾN")
        
        # Phân loại góp ý
        st.markdown("#### 📊 PHÂN LOẠI GÓP Ý")
        
        suggestion_categories = {
            "Cơ sở hạ tầng": 45,
            "Dịch vụ du lịch": 38,
            "Ẩm thực": 29,
            "Vệ sinh môi trường": 27,
            "Hướng dẫn viên": 23,
            "Phương tiện di chuyển": 19,
            "Giá cả": 16,
            "Hoạt động văn hóa": 12
        }
        
        category_df = pd.DataFrame({
            "Danh mục": list(suggestion_categories.keys()),
            "Số góp ý": list(suggestion_categories.values())
        })
        
        fig = px.pie(category_df, values="Số góp ý", names="Danh mục",
                    title="Phân bố góp ý theo danh mục",
                    hole=0.3)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
        
        # Góp ý gần đây
        st.markdown("#### 📝 GÓP Ý GẦN ĐÂY")
        
        recent_suggestions = [
            {
                "id": 1,
                "category": "Cơ sở hạ tầng",
                "suggestion": "Cần thêm nhà vệ sinh công cộng tại khu vực Núi Cấm",
                "status": "Đã tiếp nhận",
                "votes": 42,
                "date": "15/10/2024"
            },
            {
                "id": 2,
                "category": "Dịch vụ du lịch",
                "suggestion": "Nên có ứng dụng đặt tour với nhiều ngôn ngữ hơn",
                "status": "Đang xử lý",
                "votes": 38,
                "date": "12/10/2024"
            },
            {
                "id": 3,
                "category": "Ẩm thực",
                "suggestion": "Cần quy chuẩn giá cả tại các quán ăn địa phương",
                "status": "Đã tiếp nhận",
                "votes": 35,
                "date": "10/10/2024"
            },
            {
                "id": 4,
                "category": "Vệ sinh môi trường",
                "suggestion": "Tăng cường thùng rác tại các điểm du lịch",
                "status": "Hoàn thành",
                "votes": 29,
                "date": "05/10/2024"
            }
        ]
        
        for suggestion in recent_suggestions:
            status_color = {
                "Đã tiếp nhận": "blue",
                "Đang xử lý": "orange",
                "Hoàn thành": "green"
            }.get(suggestion["status"], "gray")
            
            col_sug1, col_sug2, col_sug3 = st.columns([3, 1, 1])
            
            with col_sug1:
                st.markdown(f"""
                **{suggestion['category']}**
                
                {suggestion['suggestion']}
                
                *{suggestion['date']}*
                """)
            
            with col_sug2:
                st.markdown(f"""
                **Trạng thái**
                
                <span style="color: {status_color}; font-weight: bold;">{suggestion['status']}</span>
                """, unsafe_allow_html=True)
            
            with col_sug3:
                st.metric("👍 Biểu quyết", suggestion['votes'])
                
                if st.button("👍 Ủng hộ", key=f"vote_{suggestion['id']}"):
                    st.success("Đã ghi nhận biểu quyết của bạn!")
        
        # Form góp ý chung
        st.markdown("---")
        st.markdown("#### ✍️ GÓP Ý CHUNG CHO HỆ THỐNG")
        
        with st.form("general_feedback_form"):
            feedback_type = st.selectbox(
                "Loại góp ý",
                ["Cải thiện dịch vụ", "Ý tưởng mới", "Báo lỗi hệ thống", "Đề xuất hợp tác", "Khác"]
            )
            
            feedback_title = st.text_input("Tiêu đề góp ý")
            
            feedback_content = st.text_area(
                "Nội dung chi tiết",
                placeholder="Vui lòng mô tả chi tiết góp ý của bạn..."
            )
            
            upload_files = st.file_uploader(
                "Tải lên hình ảnh minh họa (nếu có)",
                type=['jpg', 'png', 'pdf'],
                accept_multiple_files=True
            )
            
            contact_info = st.text_input(
                "Thông tin liên hệ (tùy chọn)",
                placeholder="Email hoặc số điện thoại nếu muốn nhận phản hồi"
            )
            
            submitted = st.form_submit_button("📤 GỬI GÓP Ý")
            
            if submitted and feedback_content:
                st.success("✅ Đã gửi góp ý thành công! Cảm ơn sự đóng góp của bạn.")
                
                if contact_info:
                    st.info(f"Chúng tôi sẽ liên hệ qua: {contact_info}")
        
        # Tiến độ xử lý góp ý
        st.markdown("---")
        st.markdown("#### 📈 TIẾN ĐỘ XỬ LÝ GÓP Ý")
        
        processing_stats = {
            "Tổng góp ý": 287,
            "Đã tiếp nhận": 156,
            "Đang xử lý": 78,
            "Hoàn thành": 53,
            "Tỉ lệ hoàn thành": "18.5%"
        }
        
        # Hiển thị tiến trình
        st.markdown("##### 🎯 TIẾN TRÌNH XỬ LÝ")
        
        progress_data = pd.DataFrame({
            "Giai đoạn": ["Đã tiếp nhận", "Đang xử lý", "Hoàn thành"],
            "Số lượng": [156, 78, 53],
            "Màu": ["#007bff", "#ffc107", "#28a745"]
        })
        
        fig = px.funnel(progress_data, x="Số lượng", y="Giai đoạn", color="Giai đoạn")
        st.plotly_chart(fig, use_container_width=True)
        
        # Thời gian xử lý trung bình
        st.metric("⏱️ Thời gian xử lý TB", "7.2 ngày", "-1.3 ngày")
    
    # Footer chung
    st.markdown("---")
    st.markdown("""
    <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px; text-align: center;">
        <p style="color: #6c757d; margin: 0;">
            ⭐ <strong>Hệ thống đánh giá</strong> - Nơi trải nghiệm của bạn tạo nên sự khác biệt
        </p>
        <p style="color: #6c757d; font-size: 0.9rem; margin: 0.5rem 0 0 0;">
            Mỗi đánh giá, mỗi góp ý đều quý giá và được chúng tôi trân trọng
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    # Test module
    show_feedback_module()