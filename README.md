# Đề tài 33: Phát hiện bất thường trong lưu lượng IoT
* **Học phần:** Bảo mật trong IoT (INT4410)
* **Sinh viên thực hiện:** Đào Văn Toàn
* **Mã số sinh viên:** 231A010610
* **Lớp:** INT4410 - Bảo mật trong IoT

---
## 1. Lý do chọn đề tài
Sự bùng nổ của các thiết bị IoT mang lại nhiều tiện ích nhưng cũng đối mặt với nhiều rủi ro bảo mật lớn. Do hạn chế về tài nguyên tính toán phần cứng, các thiết bị IoT không thể cài đặt các hệ thống diệt virus hay tường lửa nặng nề. Do đó, phương pháp tiếp cận giám sát và phân tích lưu lượng mạng từ xa để tự động phát hiện hành vi bất thường (DDoS, tấn công quét cổng, Botnet) là giải pháp tối ưu và khả thi nhất hiện nay.
## 2. Mục tiêu đề tài
* Tìm hiểu cấu trúc và các đặc trưng cơ bản của dữ liệu lưu lượng mạng (Network Traffic Log) trong môi trường IoT.
* Xây dựng và triển khai thực nghiệm mô hình Học máy (Machine Learning) baseline để tự động phân loại lưu lượng bình thường và bất thường.
* Đánh giá hiệu năng của mô hình dựa trên các chỉ số bảo mật tiêu chuẩn (Accuracy, Precision, Recall).
## 3. Phạm vi và Tập dữ liệu (Dataset)
* **Phạm vi:** Tập trung xử lý dữ liệu ở tầng mạng (Network/Transport Flow) dựa trên định dạng log kết nối của các thiết bị IoT.
* **Tập dữ liệu sử dụng:** Thực nghiệm trên tập dữ liệu **TON-IoT** (hoặc **CICIoT2023**). Đây là các bộ dữ liệu mới, mô phỏng chính xác các kịch bản tấn công mạng thực tế nhắm vào hệ thống IIoT/IoT thông minh, cung cấp đầy đủ các đặc trưng lưu lượng mạng hiện đại.

## 4. Công cụ và Môi trường thực hiện
* **Ngôn ngữ:** Python.
* **Môi trường:** Google Colab (Xử lý online trên trình duyệt).
* **Thuật toán baseline:** Isolation Forest (Rừng cô lập) - Thuật toán học máy không giám sát hiệu quả cho bài toán phát hiện phần tử dị biệt.
* **Trực quan hóa (Demo):** Sử dụng thư viện Seaborn/Matplotlib để vẽ biểu đồ phân phối mẫu (Normal vs Anomaly) và biểu đồ ma trận nhầm lẫn (Confusion Matrix) nhằm đánh giá trực quan hiệu năng hệ thống.
  ### 📊 Kết quả thực nghiệm Baseline (Cập nhật Tuần 02)
  * Mô hình Isolation Forest Baseline chạy tuyến tính ổn định trên cấu trúc dòng mạng mô phỏng ToN-IoT.
  * **Độ chính xác tổng thể (Accuracy):** Đạt **76%** trên tập dữ liệu kiểm thử độc lập. 
        
        Accuracy = 76.4%

        Precision = 24.8%

        Recall = 25.9%

        F1 = 25.3%
  * **Minh chứng đồ họa:** File ma trận nhầm lẫn tĩnh `confusion_matrix_ton_iot_final.png` đã được xuất và lưu trữ trực tiếp tại repo này.
## Cấu trúc Repository (Code & Output)
| Tệp tin | Mô tả chức năng |
| :--- | :--- |
| `dataset.csv` | Tập dữ liệu mạng giả lập (>100 dòng) đại diện lưu lượng IoT. |
| `detect_anomaly.py` | Script Python chạy tĩnh (Offline/Batch Mode) để phát hiện bất thường từ dữ liệu CSV. |
| `detect_anomaly_realtime.py` | Script Python mô phỏng phát hiện bất thường thời gian thực (Real-time Stream) có in log cảnh báo. |
| `anomaly_report.csv` | Tệp kết quả đầu ra chứa danh sách các gói tin/dòng lưu lượng bị gán nhãn `Anomaly`. |
| `confusion_matrix_ton_iot_final.png` | Đồ thị Ma trận nhầm lẫn (Confusion Matrix) đánh giá hiệu năng mô hình. |
## Hướng dẫn Tái hiện Thực nghiệm (Replication Guide)
### Môi trường yêu cầu
- Ngôn ngữ: Python 3.x
- Thư viện cần thiết: `pandas`, `scikit-learn`
- Thực thi trực tiếp trên moi trường online **Google Colab**.
### Các bước chạy kiểm thử
## Dạng tĩnh (Batch Processing)
    "!python detect_anomaly.py"
   
->Script sẽ đọc file dataset.csv, chạy mô hình Isolation Forest và tự động xuất kết quả ra file anomaly_report.csv.  
## Dạng động (Real-time Stream Monitoring)
    "!python detect_anomaly_realtime.py"
 
->Hệ thống sẽ mô phỏng luồng dữ liệu mạng chảy về liên tục từng giây, dự đoán và in trực tiếp nhãn cảnh báo ⚠️ ANOMALY hoặc ✅ Normal ra màn hình dòng lệnh. 
## Kiểm tra kết quả cập nhật trong tệp báo cáo (anomaly_report.csv) 
    "Import pandas as pd
    Xem nội dung báo cáo cảnh báo mới nhất
    df_report = pd.read_csv('anomaly_report.csv')
    print(df_report)"
  
->Kết quả mẫu hiển thị trên màn hình (Output) khớp với ⚠️ "detect_anomaly_realtime.py".
## 5. Danh sách tài liệu tham khảo ban đầu
1. OWASP Internet of Things - Top IoT Vulnerabilities.
2. Bộ dữ liệu huấn luyện mạng IoT thế hệ mới: "The TON_IoT Datasets" hoặc "CICIoT2023 Dataset".
3. Tài liệu hướng dẫn thuật toán Isolation Forest từ Scikit-Learn Documentation.
4. Repo GitHub tham khảo xử lý lưu lượng: https://github.com/scikit-learn/scikit-learn (Thư viện gốc hỗ trợ các mô hình Baseline).
5. Tài liệu môn học :'https://drive.google.com/drive/folders/1CgVfkRDFyF3NPUsf-ukFDtv-wkqoCx1x'
6. Bài báo khoa học: "CICIoT2023: A Real-Time Dataset and Benchmark for Large-Scale Attacks in IoT Environment" - Tạp chí MDPI Sensors (Nghiên cứu cấu trúc các lớp tấn công mạng IoT thực tế).
7. Repo GitHub thực nghiệm: https://github.com/syedissambukhari/Intrusion-detection-in-CICIoT2023-Using-ML-and-DL-Approach (Tham khảo mã nguồn Python tiền xử lý dữ liệu và vẽ Confusion Matrix trên bộ dữ liệu IoT).
8. Bài báo khoa học: "A Systematic Review of Data-Driven Attack Detection Trends in IoT" (Khảo sát các phương pháp học máy phát hiện bất thường dựa trên lưu lượng kết nối flow-based).
