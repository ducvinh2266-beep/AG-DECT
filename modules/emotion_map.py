"""
Module 2: Bản đồ cảm xúc du lịch - Phiên bản nâng cấp
Khi bấm vào địa điểm sẽ hiện thông tin chi tiết + hình ảnh + đặc sản + quán ăn
"""

import streamlit as st
import folium
from folium import plugins
import pandas as pd
import json
import os
import random
from streamlit_folium import folium_static
import plotly.express as px

def show_emotion_map_module(data):
    """Module 2: Bản đồ cảm xúc du lịch với popup thông tin nâng cấp"""
    
    st.title("🗺️ BẢN ĐỒ CẢM XÚC DU LỊCH NÂNG CAO")
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem;">
        <h3 style="color: white; text-align: center;">BẢN ĐỒ CẢM XÚC AN GIANG - KIÊN GIANG</h3>
        <p style="color: white; text-align: center;">(Click vào địa điểm để xem hình ảnh, đặc sản và quán ăn gần đó)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ======================== DỮ LIỆU MẪU CHO HÌNH ẢNH, ĐẶC SẢN, QUÁN ĂN ========================
    
    # Dữ liệu mẫu cho hình ảnh (3 ảnh mỗi địa điểm)
    sample_images = {
        "KHU LƯU NIỆM CHỦ TỊCH TÔN ĐỨC THẮNG": [
            "https://images.unsplash.com/photo-1589802829985-817e51171b92?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1551632811-561732d1e306?w=400&h=300&fit=crop"
        ],
        "CHÙA HANG (PHƯỚC ĐIỀN TỰ)": [
            "https://images.unsplash.com/photo-1548013146-72479768bada?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1559526324-4b87b5e36e44?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=400&h=300&fit=crop"
        ],
        "ĐỒI TỨC DỤP": [
            "https://images.unsplash.com/photo-1505142468610-359e7d316be0?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=400&h=300&fit=crop"
        ],
        "NÚI CÔ TÔ": [
            "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1505142468610-359e7d316be0?w=400&h=300&fit=crop"
        ],
        "QUẦN ĐẢO NAM DU": [
            "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1519046904884-53103b34b206?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=400&h=300&fit=crop"
        ]
    }
    
    # Thêm hình ảnh cho các địa điểm khác
    for i in range(6, 46):
        sample_images[f"ĐỊA ĐIỂM {i}"] = [
            "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1519046904884-53103b34b206?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=400&h=300&fit=crop"
        ]
    
    # Dữ liệu mẫu cho đặc sản theo vùng
    specialties_data = {
        "An Giang": [
            "Lẩu mắm", "Bún cá", "Cá lóc nướng trui", "Bánh xèo", 
            "Chuột đồng nướng", "Khô cá lóc", "Mắm cá linh", "Bánh canh Vĩnh Trung",
            "Bánh phồng tôm Sa Giang", "Xôi bảy màu", "Mắm thái Châu Đốc"
        ],
        "Kiên Giang": [
            "Hủ tiếu", "Bún kèn", "Gỏi cá trích", "Cua huỳnh đế", 
            "Nhum biển", "Sò huyết", "Rượu mỏ quạ", "Bánh bèo",
            "Bánh canh chả cá", "Chả mực Hà Tiên", "Khô mực một nắng"
        ]
    }
    
    # Dữ liệu mẫu cho quán ăn gần đó (4.5-5 sao)
    restaurants_data = {
        "Long Xuyên": [
            {"name": "Nhà Hàng Lẩu Mắm Cô Ba", "address": "123 Đường Nguyễn Trãi, Long Xuyên", "rating": 4.8, "reviews": 1280, "specialties": ["Lẩu mắm", "Cá lóc nướng trui"]},
            {"name": "Quán Bún Cá Chú Tư", "address": "45 Đường Bình Khánh, Long Xuyên", "rating": 4.6, "reviews": 856, "specialties": ["Bún cá", "Cá kho tộ"]},
            {"name": "Nhà Hàng Ẩm Thực Miền Tây", "address": "78 Đường 30/4, Long Xuyen", "rating": 4.7, "reviews": 942, "specialties": ["Lẩu cá kèo", "Bánh xèo"]}
        ],
        "Châu Đốc": [
            {"name": "Nhà Hàng Mắm Thái", "address": "12 Đường Nguyễn Văn Thoại, Châu Đốc", "rating": 4.9, "reviews": 1567, "specialties": ["Mắm thái", "Cá linh kho mắm"]},
            {"name": "Quán Cơm Gia Truyền Bà Năm", "address": "34 Đường Trần Hưng Đạo, Châu Đốc", "rating": 4.5, "reviews": 723, "specialties": ["Cơm gà xối mỡ", "Canh chua cá lóc"]},
            {"name": "Lẩu Cá Kèo Sông Nước", "address": "56 Đường Bạch Đằng, Châu Đốc", "rating": 4.7, "reviews": 891, "specialties": ["Lẩu cá kèo", "Cá lóc nướng"]}
        ],
        "Tịnh Biên": [
            {"name": "Quán Cơm Núi Cấm", "address": "Đường lên Núi Cấm, Tịnh Biên", "rating": 4.6, "reviews": 645, "specialties": ["Cơm chay", "Đậu hủ núi"]},
            {"name": "Nhà Hàng Rừng Tràm", "address": "Gần Rừng Tràm Trà Sư, Tịnh Biên", "rating": 4.4, "reviews": 532, "specialties": ["Cá lóc nướng", "Lẩu mắm"]}
        ],
        "Tri Tôn": [
            {"name": "Quán Ăn Đồi Tức Dụp", "address": "Chân đồi Tức Dụp, Tri Tôn", "rating": 4.5, "reviews": 478, "specialties": ["Gà nướng", "Cơm lam"]},
            {"name": "Nhà Hàng Núi Cô Tô", "address": "Đường vào Núi Cô Tô, Tri Tôn", "rating": 4.3, "reviews": 389, "specialties": ["Cá suối nướng", "Rau rừng"]}
        ],
        "Hà Tiên": [
            {"name": "Nhà Hàng Hải Sản Hà Tiên", "address": "Bãi biển Mũi Nai, Hà Tiên", "rating": 4.8, "reviews": 1345, "specialties": ["Hải sản tươi sống", "Cua huỳnh đế"]},
            {"name": "Quán Ăn Gia Truyền Hà Tiên", "address": "22 Đường Đống Đa, Hà Tiên", "rating": 4.7, "reviews": 987, "specialties": ["Bún kèn", "Hủ tiếu"]},
            {"name": "Lẩu Hải Sản Biển Tây", "address": "45 Đường Phương Thành, Hà Tiên", "rating": 4.6, "reviews": 765, "specialties": ["Lẩu hải sản", "Sò huyết nướng"]}
        ],
        "Rạch Giá": [
            {"name": "Nhà Hàng Hải Sản Rạch Giá", "address": "Khu đô thị Phú Cường, Rạch Giá", "rating": 4.9, "reviews": 1876, "specialties": ["Cua gạch", "Tôm hùm"]},
            {"name": "Quán Ốc Nổi Tiếng", "address": "78 Đường Nguyễn Trung Trực, Rạch Giá", "rating": 4.7, "reviews": 1123, "specialties": ["Ốc mỡ", "Nghêu hấp"]},
            {"name": "Lẩu Cua Đồng", "address": "34 Đường Lê Lợi, Rạch Giá", "rating": 4.5, "reviews": 876, "specialties": ["Lẩu cua đồng", "Bánh canh cua"]}
        ],
        "Phú Quốc": [
            {"name": "Nhà Hàng Sang Trọng Phú Quốc", "address": "Bãi Trường, Phú Quốc", "rating": 4.9, "reviews": 2345, "specialties": ["Sim rừng nướng", "Gỏi cá trích"]},
            {"name": "Quán Hải Sản Dinh Cậu", "address": "Khu Dinh Cậu, Phú Quốc", "rating": 4.8, "reviews": 1876, "specialties": ["Cá mao ếch", "Nhum biển"]},
            {"name": "Nhà Hàng Ngon Rẻ", "address": "Chợ đêm Phú Quốc", "rating": 4.6, "reviews": 1543, "specialties": ["Bún quậy", "Chả mực"]}
        ],
        # Thêm các quận/huyện khác
        "Châu Phú": [
            {"name": "Quán Ăn Châu Phú", "address": "Đường Nguyễn Huệ, Châu Phú", "rating": 4.4, "reviews": 432, "specialties": ["Cá lóc nướng", "Lẩu mắm"]}
        ],
        "Thoại Sơn": [
            {"name": "Nhà Hàng Thoại Sơn", "address": "Đường 30/4, Thoại Sơn", "rating": 4.3, "reviews": 398, "specialties": ["Cá kho tộ", "Canh chua"]}
        ],
        "Chợ Mới": [
            {"name": "Quán Ăn Chợ Mới", "address": "Khu chợ Chợ Mới", "rating": 4.2, "reviews": 367, "specialties": ["Bún riêu", "Bánh canh"]}
        ],
        "Châu Thành": [
            {"name": "Nhà Hàng Châu Thành", "address": "Đường Lê Lợi, Châu Thành", "rating": 4.4, "reviews": 421, "specialties": ["Cơm tấm", "Hủ tiếu"]}
        ],
        "An Phú": [
            {"name": "Quán Ăn An Phú", "address": "Đường Biên giới, An Phú", "rating": 4.1, "reviews": 356, "specialties": ["Bánh xèo", "Bún mắm"]}
        ]
    }
    
    # Lấy dữ liệu địa điểm từ cấu trúc data
    if isinstance(data, dict):
        if 'locations' in data:
            if isinstance(data['locations'], dict) and 'locations' in data['locations']:
                # Cấu trúc: {'locations': {'locations': [...]}}
                locations = data['locations']['locations']
            elif isinstance(data['locations'], list):
                # Cấu trúc: {'locations': [...]}
                locations = data['locations']
            else:
                st.error("Cấu trúc dữ liệu không đúng")
                locations = []
        else:
            # Có thể data là list trực tiếp
            locations = data.get('locations', []) if isinstance(data.get('locations'), list) else []
    else:
        locations = []
    
    if not locations:
        st.warning("Không có dữ liệu địa điểm. Đang sử dụng dữ liệu mẫu...")
        # Tạo dữ liệu mẫu từ file locations.json
        sample_locations = [
            {
                "id": 1,
                "name": "KHU LƯU NIỆM CHỦ TỊCH TÔN ĐỨC THẮNG",
                "province": "An Giang",
                "district": "Long Xuyên",
                "ward": "Mỹ Bình",
                "coordinates": {"lat": 10.3804, "lng": 105.4352},
                "emotions": ["🗳️ Tôn kính", "📜 Lịch sử", "🇻🇳 Tự hào"],
                "best_time": "8:00-11:00, 14:00-17:00",
                "description": "Nơi lưu giữ kỷ vật về Chủ tịch Tôn Đức Thắng - người con ưu tú của An Giang",
                "category": "di_tich_lich_su",
                "image": "ton_duc_thang.jpg",
                "audio_story": "ky_uc_ton_duc_thang.mp3"
            },
            {
                "id": 2,
                "name": "CHÙA HANG (PHƯỚC ĐIỀN TỰ)",
                "province": "An Giang",
                "district": "Tịnh Biên",
                "ward": "An Phú",
                "coordinates": {"lat": 10.5623, "lng": 105.0123},
                "emotions": ["🕉️ Tĩnh tại", "🙏 Tâm linh", "🏔️ Huyền bí"],
                "best_time": "5:00-9:00, 15:00-18:00",
                "description": "Ngôi chùa trong hang động độc đáo, không khí mát lạnh quanh năm",
                "category": "tam_linh",
                "image": "chua_hang_phuoc_dien.jpg",
                "audio_story": "am_thanh_chua_hang.mp3"
            },
            {
                "id": 3,
                "name": "ĐỒI TỨC DỤP",
                "province": "An Giang",
                "district": "Tri Tôn",
                "ward": "Núi Tô",
                "coordinates": {"lat": 10.4123, "lng": 104.9567},
                "emotions": ["🌄 Hoàng hôn", "📸 Sống ảo", "💑 Lãng mạn"],
                "best_time": "16:00-18:30 (hoàng hôn)",
                "description": "Đồi cỏ xanh mướt, view toàn cảnh đồng bằng, điểm check-in tuyệt đẹp",
                "category": "thien_nhien",
                "image": "doi_tuc_dup.jpg",
                "audio_story": "hoang_hon_tuc_dup.mp3"
            }
        ]
        locations = sample_locations
    
    # ======================== BỘ LỌC ========================
    st.markdown("### 🔍 LỌC ĐỊA ĐIỂM")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Lấy danh sách tỉnh từ dữ liệu
        all_provinces = []
        for loc in locations:
            province = loc.get('province', '')
            if province and province not in all_provinces:
                all_provinces.append(province)
        
        province_filter = st.selectbox(
            "Tỉnh",
            ["Tất cả"] + sorted(all_provinces)
        )
    
    with col2:
        # Lấy tất cả các cảm xúc từ dữ liệu
        all_emotions = []
        for loc in locations:
            for emotion in loc.get('emotions', []):
                if isinstance(emotion, str):
                    # Tách emoji và text
                    parts = emotion.split(' ', 1)
                    if len(parts) == 2:
                        all_emotions.append(parts[1].strip())
                    else:
                        all_emotions.append(emotion.strip())
        
        unique_emotions = ["Tất cả"] + sorted(list(set([e for e in all_emotions if e])))
        
        emotion_filter = st.selectbox(
            "Cảm xúc",
            unique_emotions
        )
    
    with col3:
        # Lấy tất cả các loại hình
        all_categories = []
        for loc in locations:
            category = loc.get('category', '')
            if category:
                # Chuyển từ snake_case sang title case
                formatted_category = category.replace('_', ' ').title()
                if formatted_category not in all_categories:
                    all_categories.append(formatted_category)
        
        all_categories = ["Tất cả"] + sorted(all_categories)
        
        category_filter = st.selectbox(
            "Loại hình",
            all_categories
        )
    
    # Lọc dữ liệu
    filtered_locations = []
    for loc in locations:
        # Lọc theo tỉnh
        if province_filter != "Tất cả" and loc.get('province') != province_filter:
            continue
        
        # Lọc theo cảm xúc
        if emotion_filter != "Tất cả":
            loc_emotions = []
            for emotion in loc.get('emotions', []):
                if isinstance(emotion, str):
                    parts = emotion.split(' ', 1)
                    if len(parts) == 2:
                        loc_emotions.append(parts[1].strip())
                    else:
                        loc_emotions.append(emotion.strip())
            
            if emotion_filter not in loc_emotions:
                continue
        
        # Lọc theo loại hình
        if category_filter != "Tất cả":
            loc_category = loc.get('category', '').replace('_', ' ').title()
            if loc_category != category_filter:
                continue
        
        filtered_locations.append(loc)
    
    # ======================== TẠO BẢN ĐỒ ========================
    st.markdown(f"### 📍 {len(filtered_locations)} ĐỊA ĐIỂM ĐÃ TÌM THẤY")
    
    # Tạo bản đồ với vị trí trung tâm
    m = folium.Map(
        location=[10.3755, 105.4339],  # Tọa độ trung tâm An Giang
        zoom_start=9,
        control_scale=True,
        tiles='CartoDB positron'  # Bản đồ sáng
    )
    
    # Thêm plugin
    plugins.Fullscreen().add_to(m)
    plugins.MeasureControl(position='topright').add_to(m)
    
    # Thêm lớp tile bản đồ khác - chỉ layer sáng
    folium.TileLayer('OpenStreetMap').add_to(m)
    folium.TileLayer('Stamen Terrain').add_to(m)
    
    # Dictionary ánh xạ biểu tượng cảm xúc
    emotion_icons = {
        "🏔️": {"color": "green", "icon": "mountain", "prefix": "fa"},
        "🗳️": {"color": "red", "icon": "landmark", "prefix": "fa"},
        "🕉️": {"color": "purple", "icon": "place-of-worship", "prefix": "fa"},
        "🌄": {"color": "orange", "icon": "sun", "prefix": "fa"},
        "🏝️": {"color": "blue", "icon": "umbrella-beach", "prefix": "fa"},
        "🛶": {"color": "cadetblue", "icon": "ship", "prefix": "fa"},
        "🪨": {"color": "gray", "icon": "mountain", "prefix": "fa"},
        "🌲": {"color": "darkgreen", "icon": "tree", "prefix": "fa"},
        "🏖️": {"color": "lightblue", "icon": "umbrella-beach", "prefix": "fa"},
        "🙏": {"color": "orange", "icon": "pray", "prefix": "fa"},
        "⛰️": {"color": "darkred", "icon": "mountain", "prefix": "fa"},
        "🎨": {"color": "pink", "icon": "palette", "prefix": "fa"},
        "🏞️": {"color": "lightgreen", "icon": "image", "prefix": "fa"},
        "🌿": {"color": "green", "icon": "leaf", "prefix": "fa"},
        "🏺": {"color": "beige", "icon": "history", "prefix": "fa"},
        "🏴‍☠️": {"color": "black", "icon": "skull-crossbones", "prefix": "fa"},
        "💧": {"color": "blue", "icon": "water", "prefix": "fa"},
        "🗼": {"color": "red", "icon": "tower", "prefix": "fa"},
        "🏛️": {"color": "lightgray", "icon": "landmark", "prefix": "fa"},
        "⚔️": {"color": "darkpurple", "icon": "sword", "prefix": "fa"},
        "🎎": {"color": "red", "icon": "torii-gate", "prefix": "fa"},
        "📜": {"color": "darkblue", "icon": "scroll", "prefix": "fa"},
        "🇻🇳": {"color": "red", "icon": "flag", "prefix": "fa"},
        "📸": {"color": "purple", "icon": "camera", "prefix": "fa"},
        "💑": {"color": "pink", "icon": "heart", "prefix": "fa"},
        "🌅": {"color": "orange", "icon": "sun", "prefix": "fa"},
        "🧘‍♀️": {"color": "green", "icon": "spa", "prefix": "fa"},
        "🐠": {"color": "lightblue", "icon": "fish", "prefix": "fa"},
        "🌅": {"color": "orange", "icon": "sun", "prefix": "fa"},
        "🐟": {"color": "blue", "icon": "fish", "prefix": "fa"},
        "📚": {"color": "brown", "icon": "book", "prefix": "fa"},
        "🌫️": {"color": "lightgray", "icon": "cloud", "prefix": "fa"},
        "🏄‍♂️": {"color": "blue", "icon": "water", "prefix": "fa"},
        "🐚": {"color": "pink", "icon": "shell", "prefix": "fa"},
        "🕊️": {"color": "white", "icon": "dove", "prefix": "fa"},
        "🏮": {"color": "red", "icon": "lightbulb", "prefix": "fa"},
        "🚶‍♂️": {"color": "gray", "icon": "walking", "prefix": "fa"},
        "🧗‍♂️": {"color": "orange", "icon": "hiking", "prefix": "fa"},
        "🚣": {"color": "blue", "icon": "water", "prefix": "fa"},
        "🔍": {"color": "black", "icon": "search", "prefix": "fa"},
        "🏄‍♂️": {"color": "blue", "icon": "swimmer", "prefix": "fa"},
        "🍽️": {"color": "darkred", "icon": "utensils", "prefix": "fa"},
        "💊": {"color": "green", "icon": "pills", "prefix": "fa"},
    }
    
    # Thêm từng địa điểm vào bản đồ
    for location in filtered_locations:
        # Lấy tọa độ
        coords = location.get('coordinates', {})
        lat = coords.get('lat', 10.3755) if isinstance(coords, dict) else 10.3755
        lng = coords.get('lng', 105.4339) if isinstance(coords, dict) else 105.4339
        
        # Lấy biểu tượng cảm xúc đầu tiên
        emotions = location.get('emotions', ['🏔️ Thiên nhiên'])
        if emotions and isinstance(emotions, list) and len(emotions) > 0:
            first_emotion = emotions[0]
            if isinstance(first_emotion, str) and ' ' in first_emotion:
                icon_char = first_emotion.split(' ')[0]
            else:
                icon_char = '🏔️'
        else:
            icon_char = '🏔️'
        
        # Lấy cấu hình icon
        icon_config = emotion_icons.get(icon_char, {"color": "blue", "icon": "info-circle", "prefix": "fa"})
        
        # Lấy hình ảnh cho địa điểm (3 ảnh)
        location_name = location.get('name', '')
        images = sample_images.get(location_name, [
            "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1519046904884-53103b34b206?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=400&h=300&fit=crop"
        ])
        
        # Lấy đặc sản theo tỉnh
        province = location.get('province', 'An Giang')
        specialties = specialties_data.get(province, specialties_data["An Giang"])
        selected_specialties = random.sample(specialties, min(3, len(specialties)))
        
        # Lấy quán ăn gần đó theo district
        district = location.get('district', 'Long Xuyên')
        district_restaurants = []
        
        # Tìm quận/huyện phù hợp
        for key in restaurants_data:
            if key in district or district in key:
                district_restaurants = restaurants_data[key]
                break
        
        # Nếu không tìm thấy, dùng mặc định
        if not district_restaurants:
            district_restaurants = restaurants_data.get("Long Xuyên", [])
        
        # Chọn 2-3 quán ăn tốt nhất
        top_restaurants = sorted(district_restaurants, key=lambda x: x['rating'], reverse=True)[:3]
        
        # Tạo popup HTML chi tiết với hình ảnh và ẩm thực
        popup_html = f"""
        <div style="width: 420px; font-family: Arial, sans-serif; max-height: 600px; overflow-y: auto;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 12px; border-radius: 5px 5px 0 0; color: white;">
                <h4 style="margin: 0; font-size: 18px; text-align: center;">{location.get('name', 'Địa điểm')}</h4>
            </div>
            
            <div style="padding: 15px;">
                <!-- HÌNH ẢNH -->
                <div style="margin-bottom: 15px;">
                    <h5 style="margin: 0 0 8px 0; color: #2c3e50;">🖼️ HÌNH ẢNH ĐỊA ĐIỂM (3 ảnh)</h5>
                    <div style="display: flex; gap: 8px; overflow-x: auto; padding-bottom: 5px;">
        """
        
        # Thêm 3 hình ảnh
        for img in images:
            popup_html += f'<img src="{img}" style="width: 120px; height: 90px; border-radius: 5px; object-fit: cover; border: 2px solid #ddd;">'
        
        popup_html += f"""
                    </div>
                </div>
                
                <!-- THÔNG TIN CƠ BẢN -->
                <div style="margin-bottom: 15px; background: #f8f9fa; padding: 10px; border-radius: 5px;">
                    <p style="margin: 5px 0;"><strong>📍 Địa chỉ:</strong> {location.get('ward', '')}, {location.get('district', '')}, {location.get('province', '')}</p>
                    <p style="margin: 5px 0;"><strong>⏰ Thời điểm đẹp:</strong> {location.get('best_time', 'N/A')}</p>
                    <p style="margin: 5px 0;"><strong>🎯 Cảm xúc:</strong> {', '.join(location.get('emotions', []))}</p>
                </div>
                
                <!-- ĐẶC SẢN -->
                <div style="margin-bottom: 15px;">
                    <h5 style="margin: 0 0 8px 0; color: #2c3e50;">🍜 ĐẶC SẢN ĐỊA PHƯƠNG</h5>
                    <div style="display: flex; flex-wrap: wrap; gap: 5px;">
        """
        
        # Thêm đặc sản
        for spec in selected_specialties:
            popup_html += f'<span style="background: #ffebee; color: #c62828; padding: 4px 10px; border-radius: 15px; font-size: 12px; border: 1px solid #ffcdd2;">{spec}</span>'
        
        popup_html += f"""
                    </div>
                </div>
                
                <!-- QUÁN ĂN GẦN ĐÓ -->
                <div style="margin-bottom: 15px;">
                    <h5 style="margin: 0 0 8px 0; color: #2c3e50;">🍽️ QUÁN ĂN NGON GẦN ĐÂY (4.5-5★)</h5>
        """
        
        # Thêm quán ăn
        for i, restaurant in enumerate(top_restaurants):
            star_rating = "⭐" * int(restaurant['rating'])
            popup_html += f"""
                    <div style="background: #fff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 10px; margin-bottom: 8px;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <strong style="color: #e74c3c;">{restaurant['name']}</strong>
                            <span style="background: #27ae60; color: white; padding: 2px 8px; border-radius: 10px; font-size: 12px;">
                                {restaurant['rating']}★ ({restaurant['reviews']} đánh giá)
                            </span>
                        </div>
                        <p style="margin: 5px 0; font-size: 13px; color: #555;">📍 {restaurant['address']}</p>
                        <div style="font-size: 12px; color: #7f8c8d;">
                            <strong>Món ngon:</strong> {', '.join(restaurant['specialties'][:2])}
                        </div>
                    </div>
            """
        
        # Nếu không có quán ăn
        if not top_restaurants:
            popup_html += """
                    <div style="background: #fff3e0; border: 1px solid #ffb74d; border-radius: 8px; padding: 10px; margin-bottom: 8px;">
                        <p style="margin: 0; color: #ef6c00; text-align: center;">
                            Đang cập nhật thông tin quán ăn gần đây...
                        </p>
                    </div>
            """
        
        popup_html += f"""
                </div>
                
                <!-- MÔ TẢ -->
                <div style="margin-bottom: 15px;">
                    <h5 style="margin: 0 0 8px 0; color: #2c3e50;">📖 MÔ TẢ</h5>
                    <p style="margin: 0; font-size: 14px; line-height: 1.5; color: #555;">{location.get('description', '')}</p>
                </div>
                
                <!-- NÚT HÀNH ĐỘNG -->
                <div style="display: flex; gap: 10px; margin-top: 15px; padding-top: 10px; border-top: 1px solid #eee;">
                    <button onclick="alert('Đã thêm \\'{location_name}\\' vào hành trình!')" 
                            style="flex: 1; background: #4CAF50; color: white; border: none; padding: 10px; 
                                   border-radius: 5px; cursor: pointer; font-weight: bold;">
                        ➕ Thêm vào hành trình
                    </button>
                    <button onclick="alert('Đã lưu \\'{location_name}\\' vào yêu thích!')" 
                            style="flex: 1; background: #FF9800; color: white; border: none; padding: 10px; 
                                   border-radius: 5px; cursor: pointer; font-weight: bold;">
                        ⭐ Yêu thích
                    </button>
                </div>
            </div>
        </div>
        """
        
        # Tạo popup
        popup = folium.Popup(popup_html, max_width=450)
        
        # Tạo marker với popup
        folium.Marker(
            location=[lat, lng],
            popup=popup,
            tooltip=f"📌 {location.get('name', 'Địa điểm')}",
            icon=folium.Icon(
                color=icon_config['color'],
                icon=icon_config['icon'],
                prefix=icon_config['prefix'],
                icon_color='white'
            )
        ).add_to(m)
    
    # Thêm layer control
    folium.LayerControl().add_to(m)
    
    # Thêm plugin MousePosition
    plugins.MousePosition().add_to(m)
    
    # Thêm cluster marker để nhóm khi zoom nhỏ
    marker_cluster = plugins.MarkerCluster().add_to(m)
    
    # ======================== HIỂN THỊ BẢN ĐỒ ========================
    
    # Hiển thị bản đồ với kích thước lớn
    folium_static(m, width=1200, height=600)
    
    # ======================== THÔNG TIN CHI TIẾT ĐỊA ĐIỂM ========================
    
    if filtered_locations:
        st.markdown("---")
        st.markdown("### 📋 DANH SÁCH ĐỊA ĐIỂM CHI TIẾT")
        
        # Hiển thị danh sách địa điểm dưới dạng expander
        for i, location in enumerate(filtered_locations[:10]):  # Giới hạn hiển thị 10 địa điểm đầu
            with st.expander(f"📍 {location.get('name', 'Địa điểm')} - {location.get('province', '')} ⭐ {len(location.get('emotions', []))} cảm xúc"):
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    # Hiển thị hình ảnh mẫu
                    st.markdown("**🖼️ Hình ảnh:**")
                    
                    # Lấy hình ảnh cho địa điểm
                    location_name = location.get('name', '')
                    images = sample_images.get(location_name, [
                        "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=400&h=300&fit=crop",
                        "https://images.unsplash.com/photo-1519046904884-53103b34b206?w=400&h=300&fit=crop",
                        "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=400&h=300&fit=crop"
                    ])
                    
                    # Hiển thị carousel hình ảnh đơn giản
                    img_index = st.selectbox(
                        f"Chọn ảnh #{i}", 
                        list(range(1, 4)), 
                        format_func=lambda x: f"Ảnh {x}", 
                        key=f"img_{location.get('id', i)}_{i}"
                    )
                    st.image(images[img_index-1], use_column_width=True)
                    
                    # Thông tin cơ bản
                    st.markdown(f"""
                    **📍 Địa chỉ:**
                    {location.get('ward', '')}, {location.get('district', '')}
                    
                    **⏰ Thời điểm đẹp:**
                    {location.get('best_time', 'N/A')}
                    
                    **🎯 Cảm xúc:**
                    {', '.join(location.get('emotions', []))}
                    """)
                    
                    # Nút hành động
                    col_btn1, col_btn2 = st.columns(2)
                    with col_btn1:
                        if st.button("➕ Thêm vào hành trình", key=f"add_{location.get('id', i)}_{i}"):
                            st.success(f"Đã thêm '{location.get('name')}' vào hành trình!")
                    with col_btn2:
                        if st.button("⭐ Yêu thích", key=f"fav_{location.get('id', i)}_{i}"):
                            st.info(f"Đã thêm '{location.get('name')}' vào mục yêu thích!")
                
                with col2:
                    # Đặc sản
                    province = location.get('province', 'An Giang')
                    specialties = specialties_data.get(province, specialties_data["An Giang"])
                    selected_specialties = random.sample(specialties, min(5, len(specialties)))
                    
                    st.markdown("**🍜 Đặc sản địa phương:**")
                    cols_spec = st.columns(3)
                    for idx, spec in enumerate(selected_specialties[:3]):
                        with cols_spec[idx % 3]:
                            st.info(f"🍽️ {spec}")
                    
                    # Quán ăn gần đó
                    st.markdown("**🍽️ Quán ăn ngon gần đây (4.5-5★):**")
                    
                    # Lấy quán ăn theo district
                    district = location.get('district', 'Long Xuyên')
                    district_restaurants = []
                    
                    for key in restaurants_data:
                        if key in district or district in key:
                            district_restaurants = restaurants_data[key]
                            break
                    
                    if not district_restaurants:
                        district_restaurants = restaurants_data.get("Long Xuyên", [])
                    
                    top_restaurants = sorted(district_restaurants, key=lambda x: x['rating'], reverse=True)[:2]
                    
                    if top_restaurants:
                        for j, restaurant in enumerate(top_restaurants):
                            # SỬA LỖI Ở ĐÂY: Sử dụng st.container() hoặc st.columns() thay vì expander
                            restaurant_name = restaurant.get('name', 'Nhà hàng')
                            restaurant_rating = restaurant.get('rating', 4.5)
                            restaurant_reviews = restaurant.get('reviews', 100)
                            
                            # Sử dụng st.container với border
                            with st.container():
                                st.markdown(f"""
                                <div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 15px; margin-bottom: 10px;">
                                    <div style="display: flex; justify-content: space-between; align-items: center;">
                                        <h4 style="margin: 0; color: #e74c3c;">{restaurant_name} ⭐ {restaurant_rating} ({restaurant_reviews} đánh giá)</h4>
                                    </div>
                                    <p style="margin: 5px 0; color: #555;">📍 {restaurant.get('address', 'Đang cập nhật')}</p>
                                    <p style="margin: 5px 0; color: #7f8c8d;">🍽️ <strong>Món ngon:</strong> {', '.join(restaurant.get('specialties', ['Đặc sản địa phương']))}</p>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                if st.button(f"📞 Gọi đặt bàn", key=f"call_{location.get('id', i)}_{j}"):
                                    st.success(f"Đang kết nối đến {restaurant_name}...")
                    else:
                        st.info("Hiện chưa có thông tin quán ăn gần đây.")
                    
                    # Mô tả chi tiết
                    st.markdown(f"**📖 Mô tả:**")
                    st.write(location.get('description', 'Chưa có mô tả'))
    else:
        st.info("Không có địa điểm nào phù hợp với bộ lọc của bạn. Vui lòng thử lại với tiêu chí khác.")
    
    # ======================== THỐNG KÊ ========================
    
    st.markdown("---")
    st.markdown("### 📊 THỐNG KÊ & PHÂN TÍCH")
    
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    
    with col_stat1:
        st.metric("Tổng địa điểm", len(filtered_locations), f"{len(filtered_locations)}/45")
    
    with col_stat2:
        # Đếm theo tỉnh
        provinces_count = {}
        for loc in locations:
            province = loc.get('province', 'Khác')
            if province:
                provinces_count[province] = provinces_count.get(province, 0) + 1
        
        if provinces_count:
            most_province = max(provinces_count.items(), key=lambda x: x[1])
            st.metric("Tỉnh nhiều địa điểm nhất", most_province[0], f"{most_province[1]} điểm")
        else:
            st.metric("Tỉnh nhiều địa điểm nhất", "N/A", "0 điểm")
    
    with col_stat3:
        # Đếm theo loại hình
        categories_count = {}
        for loc in locations:
            category = loc.get('category', '').replace('_', ' ').title()
            if category:
                categories_count[category] = categories_count.get(category, 0) + 1
        
        if categories_count:
            most_category = max(categories_count.items(), key=lambda x: x[1])
            st.metric("Loại hình phổ biến", most_category[0], f"{most_category[1]} điểm")
        else:
            st.metric("Loại hình phổ biến", "N/A", "0 điểm")
    
    # Biểu đồ phân bố cảm xúc
    st.markdown("#### 📈 PHÂN BỐ CẢM XÚC")
    
    all_emotions_detail = []
    for loc in locations:
        for emotion in loc.get('emotions', []):
            if isinstance(emotion, str) and ' ' in emotion:
                parts = emotion.split(' ', 1)
                if len(parts) == 2:
                    all_emotions_detail.append({"icon": parts[0], "name": parts[1]})
            elif isinstance(emotion, str):
                all_emotions_detail.append({"icon": "", "name": emotion})
    
    if all_emotions_detail:
        try:
            emotion_df = pd.DataFrame(all_emotions_detail)
            emotion_counts = emotion_df['name'].value_counts().reset_index()
            emotion_counts.columns = ['Cảm xúc', 'Số địa điểm']
            
            # Hiển thị biểu đồ
            if not emotion_counts.empty:
                fig = px.bar(emotion_counts.head(10), x='Cảm xúc', y='Số địa điểm',
                             color='Cảm xúc', title="Top 10 cảm xúc phổ biến")
                st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.warning(f"Không thể tạo biểu đồ phân bố cảm xúc: {str(e)[:100]}...")
    
    # ======================== CHÚ THÍCH ========================
    
    st.markdown("---")
    st.markdown("### 🎨 CHÚ THÍCH & HƯỚNG DẪN")
    
    st.markdown("""
    <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px;">
        <h4 style="color: #2c3e50;">🎯 HƯỚNG DẪN SỬ DỤNG:</h4>
        <ol style="color: #34495e;">
            <li><strong>Click vào biểu tượng trên bản đồ</strong> để xem thông tin chi tiết, hình ảnh, đặc sản và quán ăn gần đó</li>
            <li><strong>Hình ảnh:</strong> Mỗi địa điểm có 3 hình ảnh minh họa</li>
            <li><strong>Đặc sản:</strong> Các món ăn đặc trưng của vùng</li>
            <li><strong>Quán ăn:</strong> Các nhà hàng được đánh giá 4.5-5 sao gần địa điểm</li>
            <li><strong>Bộ lọc:</strong> Sử dụng bộ lọc phía trên để tìm địa điểm theo tỉnh, cảm xúc, loại hình</li>
            <li><strong>Zoom:</strong> Sử dụng nút +/- hoặc scroll chuột để phóng to/thu nhỏ bản đồ</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

# ======================== HÀM PHỤ TRỢ ========================

if __name__ == "__main__":
    # Test module với dữ liệu mẫu
    sample_data = {
        "locations": [
            {
                "id": 1,
                "name": "NÚI CẤM",
                "province": "An Giang",
                "district": "Tịnh Biên",
                "ward": "An Hảo",
                "coordinates": {"lat": 10.4678, "lng": 104.9890},
                "emotions": ["🏔️ Tĩnh tại", "🧘‍♀️ Thanh tịnh", "🌫️ Mát mẻ"],
                "best_time": "5:00-7:00 (bình minh), 16:00-18:00 (hoàng hôn)",
                "description": "Ngọn núi cao nhất miền Tây Nam Bộ, khí hậu mát mẻ quanh năm",
                "category": "thien_nhien"
            }
        ]
    }
    
    show_emotion_map_module(sample_data)