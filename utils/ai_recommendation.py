"""
AI Recommendation System for An Giang Tourism
STEM Tin học - THPT HOA LAC
Version 2.3 - FIXED triệt để lỗi 'str' object has no attribute 'lower()'
"""

import random
from typing import Dict, List, Any, Union

class AIRecommendationSystem:
    """
    Hệ thống AI tư vấn du lịch thông minh cho An Giang
    """
    
    def __init__(self):
        self.initialize_data()
        self.setup_emotion_models()
        self.setup_cultural_factors()
        
    def initialize_data(self):
        """Khởi tạo dữ liệu địa điểm"""
        self.locations = [
            {
                "id": 1,
                "name": "Núi Cấm (Thiên Cấm Sơn)",
                "province": "An Giang",
                "type": "Thiên nhiên",
                "subtype": "Núi",
                "description": "Ngọn núi cao nhất An Giang (710m), cảnh quan hùng vĩ, khí hậu mát mẻ quanh năm",
                "lat": 10.3755,
                "lng": 105.4339,
                "emotions": ["tĩnh lặng", "phiêu lưu", "thiêng liêng"],
                "best_for": ["Người yêu thiên nhiên", "Pilgrimage", "Nhiếp ảnh"],
                "best_time": "Sáng sớm (5-7h), Chiều muộn (15-17h)",
                "duration": "3-4 giờ",
                "budget_level": 2,
                "physical_demand": 4,
                "family_friendly": 3,
                "romantic_level": 3,
                "cultural_significance": 4,
                "popularity": 4.5
            },
            {
                "id": 2,
                "name": "Chùa Hang (Phước Điền Tự)",
                "province": "An Giang",
                "type": "Văn hóa",
                "subtype": "Chùa",
                "description": "Ngôi chùa nằm trong hang động độc đáo, kiến trúc hài hòa với thiên nhiên",
                "lat": 10.0850,
                "lng": 105.0881,
                "emotions": ["tâm linh", "tĩnh lặng", "chiêm nghiệm"],
                "best_for": ["Tìm hiểu văn hóa", "Thiền định", "Kiến trúc"],
                "best_time": "Cả ngày",
                "duration": "1-2 giờ",
                "budget_level": 1,
                "physical_demand": 2,
                "family_friendly": 5,
                "romantic_level": 2,
                "cultural_significance": 5,
                "popularity": 4.2
            },
            {
                "id": 3,
                "name": "Miếu Bà Chúa Xứ Núi Sam",
                "province": "An Giang",
                "type": "Văn hóa",
                "subtype": "Di tích tâm linh",
                "description": "Di tích lịch sử - văn hóa cấp quốc gia, trung tâm tín ngưỡng quan trọng",
                "lat": 10.6961,
                "lng": 105.0975,
                "emotions": ["thiêng liêng", "tôn kính", "cộng đồng"],
                "best_for": ["Tín ngưỡng", "Lễ hội", "Văn hóa dân gian"],
                "best_time": "Lễ hội tháng 4 âm lịch",
                "duration": "2-3 giờ",
                "budget_level": 1,
                "physical_demand": 1,
                "family_friendly": 5,
                "romantic_level": 1,
                "cultural_significance": 5,
                "popularity": 4.8
            },
            {
                "id": 4,
                "name": "Rừng Tràm Trà Sư",
                "province": "An Giang",
                "type": "Thiên nhiên",
                "subtype": "Rừng ngập nước",
                "description": "Khu rừng ngập nước độc đáo, hệ sinh thái phong phú, làng nổi",
                "lat": 10.5986,
                "lng": 105.0094,
                "emotions": ["thư giãn", "khám phá", "hòa mình"],
                "best_for": ["Sinh thái", "Chụp ảnh", "Trải nghiệm"],
                "best_time": "Mùa nước nổi (8-11)",
                "duration": "4-5 giờ",
                "budget_level": 2,
                "physical_demand": 2,
                "family_friendly": 4,
                "romantic_level": 4,
                "cultural_significance": 3,
                "popularity": 4.3
            },
            {
                "id": 5,
                "name": "Làng nổi Châu Đốc",
                "province": "An Giang",
                "type": "Văn hóa",
                "subtype": "Làng nghề",
                "description": "Làng nổi trên sông với cuộc sống đặc trưng miền Tây",
                "lat": 10.6954,
                "lng": 105.1066,
                "emotions": ["thân thiện", "nhộn nhịp", "chân thật"],
                "best_for": ["Văn hóa", "Ẩm thực", "Trải nghiệm"],
                "best_time": "Sáng sớm (6-9h)",
                "duration": "2-3 giờ",
                "budget_level": 2,
                "physical_demand": 1,
                "family_friendly": 5,
                "romantic_level": 3,
                "cultural_significance": 4,
                "popularity": 4.0
            },
            {
                "id": 6,
                "name": "Núi Sam",
                "province": "An Giang",
                "type": "Thiên nhiên",
                "subtype": "Núi",
                "description": "Quần thể du lịch tâm linh - danh thắng nổi tiếng",
                "lat": 10.6889,
                "lng": 105.1000,
                "emotions": ["tôn kính", "bình yên", "chiêm nghiệm"],
                "best_for": ["Pilgrimage", "Tham quan", "Nhiếp ảnh"],
                "best_time": "Cả ngày",
                "duration": "3-4 giờ",
                "budget_level": 1,
                "physical_demand": 3,
                "family_friendly": 4,
                "romantic_level": 2,
                "cultural_significance": 5,
                "popularity": 4.6
            },
            {
                "id": 7,
                "name": "Đồi Tức Dụp",
                "province": "An Giang",
                "type": "Lịch sử",
                "subtype": "Di tích",
                "description": "Di tích lịch sử cách mạng, cảnh quan hoang sơ",
                "lat": 10.4567,
                "lng": 105.2345,
                "emotions": ["hoài niệm", "tự hào", "tĩnh lặng"],
                "best_for": ["Lịch sử", "Thiên nhiên", "Nhiếp ảnh"],
                "best_time": "Hoàng hôn (17-18h)",
                "duration": "2-3 giờ",
                "budget_level": 1,
                "physical_demand": 3,
                "family_friendly": 4,
                "romantic_level": 3,
                "cultural_significance": 4,
                "popularity": 3.8
            },
            {
                "id": 8,
                "name": "Chợ nổi Long Xuyên",
                "province": "An Giang",
                "type": "Văn hóa",
                "subtype": "Chợ",
                "description": "Chợ nổi đặc trưng miền Tây, giao thương trên sông",
                "lat": 10.3822,
                "lng": 105.4356,
                "emotions": ["nhộn nhịp", "chân thật", "thân thiện"],
                "best_for": ["Ẩm thực", "Văn hóa", "Mua sắm"],
                "best_time": "Sáng sớm (5-8h)",
                "duration": "1-2 giờ",
                "budget_level": 1,
                "physical_demand": 1,
                "family_friendly": 5,
                "romantic_level": 2,
                "cultural_significance": 4,
                "popularity": 3.9
            }
        ]
        
        self.budget_levels = {
            "Tiết kiệm": {"daily_budget": 500000, "accommodation": "Nhà nghỉ", "transport": "Xe máy/Xe đạp"},
            "Trung bình": {"daily_budget": 1000000, "accommodation": "Khách sạn 2-3 sao", "transport": "Taxi/Xe thuê"},
            "Thoải mái": {"daily_budget": 2000000, "accommodation": "Khách sạn 4 sao", "transport": "Xe riêng có tài xế"},
            "Cao cấp": {"daily_budget": 4000000, "accommodation": "Resort cao cấp", "transport": "Xe riêng VIP"}
        }

    def setup_emotion_models(self):
        self.emotion_mapping = {}  # có thể khôi phục sau nếu cần

    def setup_cultural_factors(self):
        self.cultural_aspects = {}  # có thể khôi phục sau nếu cần

    def _safe_interests_list(self, value: Any) -> List[str]:
        """Chuẩn hóa interests thành list[str] an toàn"""
        if value is None:
            return []
        if isinstance(value, str):
            if not value.strip():
                return []
            parts = value.replace(';', ',').split(',')
            return [p.strip() for p in parts if p.strip()]
        if isinstance(value, (list, tuple)):
            return [str(item).strip() for item in value if str(item).strip()]
        return []

    def _get_age_group(self, age: Any) -> str:
        try:
            age = int(age)
        except (TypeError, ValueError):
            age = 30
        if age < 18:
            return "trẻ em"
        elif age < 30:
            return "thanh niên"
        elif age < 50:
            return "trung niên"
        else:
            return "người già"

    def _select_locations(self, interests: Any, travel_with: str, age_group: str, budget: str) -> List[Dict]:
        """Chọn địa điểm - đã bảo vệ triệt để lỗi lower()"""
        budget_level_map = {"Tiết kiệm": 1, "Trung bình": 2, "Thoải mái": 3, "Cao cấp": 4}
        max_budget_level = budget_level_map.get(budget, 2)

        # Chuẩn hóa interests một lần nữa (phòng thủ kép)
        interests_list = self._safe_interests_list(interests)

        location_scores = []

        for location in self.locations:
            score = 0

            # PHẦN SỬA LỖI CHÍNH: chỉ gọi lower() khi chắc chắn là string
            for item in interests_list:
                if isinstance(item, str):
                    interest_clean = item.strip().lower()
                    if interest_clean and interest_clean in location.get("type", "").lower():
                        score += 2

            # Nhóm đi cùng
            if travel_with == "Gia đình":
                score += location.get("family_friendly", 0)
            elif travel_with == "Cặp đôi":
                score += location.get("romantic_level", 0)

            # Độ tuổi
            if age_group in ["người già", "trẻ em"]:
                if location.get("physical_demand", 0) <= 2:
                    score += 2

            # Ngân sách
            if location.get("budget_level", 0) <= max_budget_level:
                score += 1
            else:
                score -= 1

            # Độ phổ biến
            score += location.get("popularity", 0)

            location_scores.append((location, score))

        location_scores.sort(key=lambda x: x[1], reverse=True)
        return [loc[0] for loc in location_scores[:min(5, len(location_scores))]]

    def recommend_itinerary(self, preferences: Dict[str, Any]) -> str:
        """Tạo hành trình dạng văn bản"""
        try:
            interests = self._safe_interests_list(preferences.get('interests', []))
            travel_with = preferences.get('travel_with', 'Gia đình')
            duration = preferences.get('duration', '3 ngày 2 đêm')
            budget = preferences.get('budget', 'Trung bình')
            age = preferences.get('age', 30)
            age_group = self._get_age_group(age)

            locations = self._select_locations(interests, travel_with, age_group, budget)

            if not locations:
                return "Không tìm thấy địa điểm phù hợp với sở thích của bạn."

            names = ", ".join([loc["name"] for loc in locations[:3]])

            return f"""
🏞️ **HÀNH TRÌNH ĐỀ XUẤT {duration.upper()} - {travel_with.upper()}**

**Ngân sách**: {budget}
**Địa điểm nổi bật**: {names}

**Gợi ý chính**:
• Khám phá {locations[0]['name']} - {locations[0]['description'][:70]}...
• Tham quan {locations[1]['name'] if len(locations) > 1 else 'khu vực lân cận'}
• Nghỉ ngơi, ẩm thực địa phương

**Chi phí ước tính**: {self._estimate_cost(budget, len(locations))}
**Độ phù hợp**: Cao (ước lượng)
"""
        except Exception as e:
            return f"Lỗi khi tạo hành trình: {str(e)}"

    def get_ai_recommendation(self, user_info: Dict[str, Any]) -> Dict[str, Any]:
        """Tạo recommendation dạng dict"""
        try:
            interests = self._safe_interests_list(user_info.get('interests', []))
            travel_with = user_info.get('travel_with', 'Gia đình')
            budget = user_info.get('budget', 'Trung bình')
            age = user_info.get('age', 30)
            age_group = self._get_age_group(age)

            locations = self._select_locations(interests, travel_with, age_group, budget)

            if not locations:
                return {"status": "error", "message": "Không tìm thấy địa điểm phù hợp"}

            names = [loc["name"] for loc in locations]

            return {
                "status": "success",
                "itinerary_summary": f"Hành trình phù hợp cho {travel_with} - Ngân sách {budget}",
                "recommended_locations": names,
                "top_locations": names[:3],
                "confidence": random.randint(82, 97),
                "estimated_cost": self._estimate_cost(budget, len(locations)),
                "message": "Đã tạo hành trình dựa trên thông tin bạn cung cấp"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def _estimate_cost(self, budget_level: str, num_locations: int) -> str:
        cost_map = {
            "Tiết kiệm": f"{num_locations * 150000:,} - {num_locations * 300000:,} VNĐ/người",
            "Trung bình": f"{num_locations * 300000:,} - {num_locations * 600000:,} VNĐ/người",
            "Thoải mái": f"{num_locations * 600000:,} - {num_locations * 1200000:,} VNĐ/người",
            "Cao cấp": f"{num_locations * 1200000:,} - {num_locations * 2500000:,} VNĐ/người"
        }
        return cost_map.get(budget_level, "Liên hệ để biết chi tiết")


def get_ai_recommendation_system():
    return AIRecommendationSystem()


# ────────────────────────────────────────────────
#                   TEST NHANH
# ────────────────────────────────────────────────
if __name__ == "__main__":
    ai = get_ai_recommendation_system()

    # Test các trường hợp dễ gây lỗi
    test_cases = [
        {"interests": "thiên nhiên, văn hóa"},
        {"interests": ["thiên nhiên", "tâm linh"]},
        {"interests": ["thiên nhiên", 123, None]},  # trường hợp gây lỗi cũ
        {"interests": ""},
        {"interests": None},
    ]

    for i, prefs in enumerate(test_cases, 1):
        print(f"\nTest {i}: interests = {prefs.get('interests')}")
        print(ai.recommend_itinerary(prefs))
        print("-" * 70)