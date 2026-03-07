@echo off
echo 🔧 CÀI ĐẶT THƯ VIỆN CHO DỰ ÁN STEM DU LỊCH SỐ
echo ==============================================

echo 🐍 Kiểm tra Python...
python --version
if errorlevel 1 (
    echo ❌ Python chưa được cài đặt! Vui lòng cài Python 3.8+
    pause
    exit /b 1
)

echo 📦 Cài đặt thư viện từ requirements.txt...
pip install --upgrade pip
pip install -r requirements.txt

if errorlevel 1 (
    echo ⚠️ Có lỗi khi cài đặt. Thử cài từng thư viện...
    
    echo 📦 Cài đặt Streamlit...
    pip install streamlit==1.29.0
    
    echo 📦 Cài đặt Pandas...
    pip install pandas==2.1.4
    
    echo 📦 Cài đặt Plotly...
    pip install plotly==5.18.0
    
    echo 📦 Cài đặt Folium...
    pip install folium==0.14.0
    
    echo 📦 Cài đặt scikit-learn...
    pip install scikit-learn==1.3.2
    
    echo 📦 Cài đặt Pillow...
    pip install Pillow==10.1.0
    
    echo 📦 Cài đặt geopy...
    pip install geopy==2.4.1
)

echo ✅ Hoàn thành cài đặt thư viện!
echo.
echo 🚀 Để chạy ứng dụng: streamlit run app.py
pause