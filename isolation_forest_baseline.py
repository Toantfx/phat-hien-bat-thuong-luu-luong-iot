import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report, confusion_matrix

# ==========================================
# 1. ĐỌC DỮ LIỆU TỪ URL GITHUB (CÓ XỬ LÝ NGOẠI LỆ)
# ==========================================
url_ton_iot = "https://raw.githubusercontent.com/wongw9/TON_IoT_Dataset/main/Network_Dataset/NF-ToN-IoT-v2.csv"

print("--- Đang tải và cấu trúc dữ liệu từ GitHub ---")
try:
    # Đọc dữ liệu dạng bảng kết nối dòng mạng IoT
    df = pd.read_csv(url_ton_iot)
    print(drop_v2_info := f"Đã nạp thành công tập dữ liệu. Kích thước thô: {df.shape}")
except Exception as e:
    print(f"LỖI HỆ THỐNG: Không thể truy cập link GitHub kết nối dataset. Chi tiết lỗi: {e}")
    print("Vui lòng kiểm tra lại đường truyền mạng hoặc link URL dự phòng.")
    sys.exit(0) # Dừng chương trình chủ động để tránh lỗi tràn biến rác

# ==========================================
# 2. TIỀN XỬ LÝ DỮ LIỆU THÔ & CHỐNG DATA LEAKAGE
# ==========================================
# Loại bỏ các cột định danh hoặc nhãn text không tham gia tính toán toán học
features_to_drop = ['src_ip', 'dst_ip', 'proto', 'dns_query', 'http_method', 'type']
df_cleaned = df.drop(columns=[col for col in features_to_drop if col in df.columns])

# Tách biệt ma trận đặc trưng (X) và nhãn mục tiêu thực tế (y)
X = df_cleaned.drop(columns=['label'])
y = df_cleaned['label'] # Nhãn 0: Bình thường, Nhãn 1: Tấn công/Bất thường

# [BƯỚC QUAN TRỌNG]: Tách tập dữ liệu TRƯỚC khi chuẩn hóa để triệt tiêu Data Leakage
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

# Khởi tạo bộ chuẩn hóa dữ liệu dòng mạng toàn cục
scaler = StandardScaler()

# Chỉ fit và học phân phối toán học trên tập Train
X_train_scaled = scaler.fit_transform(X_train)

# Tập Test chỉ được transform thụ động dựa trên tham số của tập Train, giữ bí mật tuyệt đối
X_test_scaled = scaler.transform(X_test)

# ==========================================
# 3. HUẤN LUYỆN MÔ HÌNH HỌC KHÔNG GIÁM SÁT (UNSUPERVISED)
# ==========================================
# Tính toán tỷ lệ nhiễm độc (contamination) thực tế dựa trên y_train ngoài lề
contamination_rate = np.sum(y_train == 1) / len(y_train)
print(f"Tỷ lệ nhiễm độc (Luồng lưu lượng bất thường) ước tính: {contamination_rate:.4f}")

print("\n--- Đang huấn luyện mô hình Isolation Forest Baseline ---")
# Khởi tạo mô hình rừng cô lập phân hoạch ngẫu nhiên các phần tử dị biệt
model = IsolationForest(contamination=contamination_rate, random_state=42, n_jobs=-1)

# Học không giám sát: Tuyệt đối CHỈ ném X_train_scaled vào hàm fit, không đưa nhãn y_train
model.fit(X_train_scaled)

# ==========================================
# 4. DỰ ĐOÁN VÀ ĐÁNH GIÁ CHỈ SỐ HIỆU NĂNG BẢO MẬT
# ==========================================
print("\n--- Đang tiến hành thực nghiệm trên tập dữ liệu kiểm thử ---")
# Mô hình xuất ra kết quả mặc định: 1 (Bình thường), -1 (Bất thường/Dị biệt)
y_pred_raw = model.predict(X_test_scaled)

# Ánh xạ lại nhãn (-1 thành 1 cho Anomaly, 1 thành 0 cho Normal) để khớp với nhãn gốc của dataset
y_pred = np.where(y_pred_raw == -1, 1, 0)

# Xuất bảng báo cáo chỉ số an ninh mạng tiêu chuẩn (Xử lý lỗi chia cho 0 nếu có)
print("\nBÁO CÁO HIỆU NĂNG PHÁT HIỆN BẤT THƯỜNG:")
print(classification_report(y_test, y_pred, target_names=['Normal (0)', 'Anomaly (1)'], zero_division=0))

# ==========================================
# 5. TRỰC QUAN HÓA MA TRẬN NHẦM LẪN (CONFUSION MATRIX)
# ==========================================
cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['Dự đoán Bình thường', 'Dự đoán Tấn công'],
            yticklabels=['Thực tế Bình thường', 'Thực tế Tấn công'])

plt.title('Ma trận nhầm lẫn phát hiện lưu lượng IoT - Isolation Forest Baseline')
plt.ylabel('Giá trị thực tế')
plt.xlabel('Giá trị dự đoán')
plt.tight_layout()

# Lưu đồ họa trực tiếp vào thư mục tạm của hệ thống để làm minh chứng báo cáo
plt.savefig('confusion_matrix_ton_iot_final.png', dpi=300)
print("\n[THÀNH CÔNG]: Đã xuất file ảnh đồ họa minh chứng 'confusion_matrix_ton_iot_final.png'.")
plt.show()
