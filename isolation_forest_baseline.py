import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.datasets import make_classification

# ==========================================
# 1. KHỞI TẠO DỮ LIỆU MÔ PHỎNG LƯU LƯỢNG MẠNG IoT (CHỐNG LỖI MẠNG / 404)
# ==========================================
print("--- Đang khởi tạo cấu trúc tập dữ liệu dòng mạng IoT (ToN-IoT/CICIoT2023 Flow Base) ---")

# Tự động sinh tập dữ liệu dạng bảng mô phỏng luồng dữ liệu 
# Gồm 5,000 phiên kết nối với 10 thuộc tính dòng mạng đặc trưng (thời lượng, bytes, gói tin...)
X_raw, y_raw = make_classification(
    n_samples=5000, 
    n_features=10, 
    n_informative=8, 
    n_redundant=2,
    weights=[0.85, 0.15], # Tỷ lệ: 85% lưu lượng bình thường, 15% lưu lượng bất thường (Tấn công)
    random_state=42
)

# Chuyển đổi sang định dạng DataFrame dữ liệu bảng
feature_names = ['duration', 'src_bytes', 'dst_bytes', 'src_pkts', 'dst_pkts', 
                 'src_load', 'dst_load', 'loss', 'sttl', 'dttl']
df = pd.DataFrame(X_raw, columns=feature_names)
df['label'] = y_raw

print(f"✔ Khởi tạo thành công! Kích thước dữ liệu: {df.shape}")
print(f"Tổng số mẫu lưu lượng mạng IoT: {df.shape[0]}")
print(f"Số đặc trưng dòng mạng (Flow Features): {df.shape[1] - 1}")
print(f"Phân phối nhãn THẬT: {np.bincount(df['label'])} (0: Bình thường, 1: Tấn công)")

# Tách biệt ma trận đặc trưng X và nhãn y
X = df.drop(columns=['label'])
y_true = df['label'].values

# ==========================================
# 2. TIỀN XỬ LÝ DỮ LIỆU & CHỐNG DATA LEAKAGE
# ==========================================
# [BƯỚC QUAN TRỌNG]: Tách tập dữ liệu TRƯỚC khi chuẩn hóa để triệt tiêu Data Leakage
X_train, X_test, y_train, y_test = train_test_split(X, y_true, test_size=0.3, random_state=42, stratify=y_true)

# Khởi tạo bộ chuẩn hóa dữ liệu dòng mạng toàn cục
scaler = StandardScaler()

# Chỉ fit và học phân phối toán học trên tập Train
X_train_scaled = scaler.fit_transform(X_train)

# Tập Test chỉ được transform thụ động dựa trên tham số của tập Train, giữ bí mật tuyệt đối
X_test_scaled = scaler.transform(X_test)
print("✔ Quy trình chuẩn hóa StandardScaler hoàn tất (Đã bảo vệ tính toàn vẹn của tập Test).")

# ==========================================
# 3. HUÂN LUYỆN MÔ HÌNH HỌC KHÔNG GIÁM SÁT (UNSUPERVISED)
# ==========================================
# Tính toán tỷ lệ nhiễm độc (contamination) thực tế dựa trên y_train ngoài lề
contamination_rate = np.sum(y_train == 1) / len(y_train)
print(f"\nTỷ lệ nhiễm độc (Luồng lưu lượng bất thường) ước tính: {contamination_rate:.4f}")

print("--- Đang huấn luyện mô hình Isolation Forest Baseline ---")
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

# Ánh xạ lại nhãn (-1 thành 1 cho Anomaly, 1 thành 0 cho Normal) để khớp với nhãn gốc
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
