%%writefile detect_anomaly_realtime.py
import time
import random
import pandas as pd
from datetime import datetime
from sklearn.ensemble import IsolationForest

def generate_live_packet():
    """Mô phỏng 1 gói tin mạng chảy về thời gian thực"""
    # 85% cơ hội là lưu lượng bình thường, 15% cơ hội là bất thường (tấn công)
    is_anomaly = random.random() < 0.15 
    
    if is_anomaly:
        # Lưu lượng bất thường: số lượng packet và byte cực cao (ví dụ: DDoS, Scan)
        src_ip = f"192.168.1.{random.randint(100, 200)}"
        src_port = random.randint(10000, 65000)
        packet_count = random.randint(5000, 20000)
        byte_count = random.randint(1000000, 10000000)
    else:
        # Lưu lượng bình thường
        src_ip = f"192.168.1.{random.randint(2, 50)}"
        src_port = random.randint(1000, 9000)
        packet_count = random.randint(5, 50)
        byte_count = random.randint(500, 5000)

    return {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'src_ip': src_ip,
        'src_port': src_port,
        'dst_ip': '10.0.0.1',
        'dst_port': 80,
        'proto': 'TCP',
        'packet_count': packet_count,
        'byte_count': byte_count
    }

def main():
    print("==================================================")
    print("  HỆ THỐNG PHÁT HIỆN BẤT THƯỜNG THỜI GIAN THỰC   ")
    print("==================================================")
    
    # 1. Huấn luyện mô hình cơ sở (Pre-train Model)
    normal_data = pd.DataFrame({
        'packet_count': [random.randint(5, 50) for _ in range(200)],
        'byte_count': [random.randint(500, 5000) for _ in range(200)]
    })
    
    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(normal_data[['packet_count', 'byte_count']])
    print("[*] Mô hình Isolation Forest đã sẵn sàng giám sát luồng dữ liệu!\n")

    # 2. Bắt đầu luồng giám sát Real-time
    output_file = 'anomaly_report.csv'
    anomalies_list = []
    
    print(f"{'Thời gian':<20} | {'IP Nguồn':<15} | {'Packets':<8} | {'Bytes':<10} | {'Trạng thái'}")
    print("-" * 75)

    # Giả lập 20 gói tin chảy về, mỗi gói cách nhau 1 giây
    for i in range(20):
        packet = generate_live_packet()
        
        # Đưa vào mô hình để dự đoán ngay lập tức
        df_packet = pd.DataFrame([packet])
        features = df_packet[['packet_count', 'byte_count']]
        
        pred = model.predict(features)[0] # -1: Anomaly, 1: Normal
        
        if pred == -1:
            status = "⚠️ ANOMALY (CẢNH BÁO)"
            packet['status'] = 'Anomaly'
            anomalies_list.append(packet)
            
            # Cập nhật ngay lập tức vào file anomaly_report.csv
            pd.DataFrame(anomalies_list).to_csv(output_file, index=False)
        else:
            status = "✅ Normal"
            packet['status'] = 'Normal'

        # In kết quả ra màn hình dòng lệnh theo thời gian thực
        print(f"{packet['timestamp']:<20} | {packet['src_ip']:<15} | {packet['packet_count']:<8} | {packet['byte_count']:<10} | {status}")
        
        # Tạm dừng 1 giây để giả lập luồng dữ liệu thực tế
        time.sleep(1)

    print("\n--------------------------------------------------")
    print(f"[+] Giám sát hoàn tất! Tìm thấy {len(anomalies_list)} gói tin bất thường.")
    print(f"[+] Đã cập nhật kết quả tự động vào file: {output_file}")

if __name__ == "__main__":
    main()