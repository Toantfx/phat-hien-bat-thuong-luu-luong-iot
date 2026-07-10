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
* **Phạm vi:** Tập trung xử lý dữ liệu ở tầng mạng (Network/Transport Flow) dựa trên định dạng log kết nối.
* **Tập dữ liệu sử dụng:** Thực nghiệm trên tập dữ liệu công khai **KDD Cup 99** (Bộ dữ liệu kinh điển, cấu trúc đơn giản, tệp tin nhỏ gọn, cực kỳ phù hợp để huấn luyện mô hình baseline chạy thử nghiệm nhanh chóng).

## 4. Công cụ và Môi trường thực hiện (Phương pháp đơn giản nhất)
* **Ngôn ngữ:** Python.
* **Môi trường:** Google Colab (Xử lý online trên trình duyệt, không cần cài đặt phần mềm phức tạp vào máy tính).
* **Thuật toán baseline:** Isolation Forest (Rừng cô lập) - Thuật toán học máy không giám sát hiệu quả nhất cho bài toán phát hiện phần tử dị biệt.

## 5. Danh sách tài liệu tham khảo ban đầu
1. OWASP Internet of Things - Top IoT Vulnerabilities.
2. Bộ dữ liệu huấn luyện mạng: "KDD Cup 1999 Data" - UCI Machine Learning Repository.
3. Tài liệu hướng dẫn thuật toán Isolation Forest từ Scikit-Learn Documentation.
4. Repo GitHub tham khảo xử lý lưu lượng: `https://github.com/scikit-learn/scikit-learn` (Thư viện gốc hỗ trợ các mô hình Baseline).
5. Giáo trình/Bài giảng học phần Bảo mật IoT - Đại học Văn Hiến (VHU).
