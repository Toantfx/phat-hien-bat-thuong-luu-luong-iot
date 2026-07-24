import pandas as pd
from sklearn.ensemble import IsolationForest

def main():
    print("=== BẮT ĐẦU QUÁ TRÌNH PHÁT HIỆN BẤT THƯỜNG ===")
    
    # 1. Nạp dữ liệu
    dataset_path = 'dataset.csv'
    print(f"[*] Đang đọc dữ liệu từ {dataset_path}...")
    df = pd.read_csv(dataset_path)
    
    # 2. Chọn đặc trưng để huấn luyện (Features)
    features = ['packet_count', 'byte_count']
    X = df[features]
    
    # 3. Chạy thuật toán Isolation Forest
    print("[*] Đang huấn luyện mô hình Isolation Forest...")
    model = IsolationForest(contamination=0.2, random_state=42)
    df['anomaly_score'] = model.fit_predict(X)
    
    # IsolationForest trả về -1 cho Anomaly (Bất thường) và 1 cho Normal (Bình thường)
    df['status'] = df['anomaly_score'].map({1: 'Normal', -1: 'Anomaly'})
    
    # 4. Lọc ra các dòng bất thường
    anomalies = df[df['status'] == 'Anomaly'].copy()
    
    # 5. Xuất kết quả ra file anomaly_report.csv
    output_path = 'anomaly_report.csv'
    anomalies.to_csv(output_path, index=False)
    
    print(f"[+] Hoàn tất! Tìm thấy {len(anomalies)} dòng bất thường.")
    print(f"[+] Kết quả đã được tự động lưu tại: {output_path}")

if __name__ == "__main__":
    main()
