# Công Cụ Chỉnh Sửa Văn Bản Cong

Công cụ này giúp bạn làm thẳng và căn chỉnh văn bản cong trong hình ảnh. Nó sử dụng quy trình hai giai đoạn để phát hiện và chỉnh sửa các dòng văn bản cong.

## Tính Năng

- Tải lên hình ảnh của bạn hoặc sử dụng hình ảnh mẫu
- Điều chỉnh các thông số thuật toán để có kết quả tối ưu
- Quy trình làm thẳng văn bản hai giai đoạn
- Hiển thị tương tác của quá trình căn chỉnh
- Tải xuống hình ảnh đã xử lý

## Cài Đặt

1. Clone repository này:
```
git clone https://github.com/yourusername/curved-text-alignment.git
cd curved-text-alignment
```

2. Cài đặt các thư viện cần thiết:
```
pip install -r requirements.txt
```

## Cách Sử Dụng

1. Khởi động ứng dụng Streamlit:
```
streamlit run app.py
```

2. Mở trình duyệt web của bạn và truy cập http://localhost:8501

3. Tải lên một hình ảnh hoặc chọn một hình ảnh mẫu

4. Điều chỉnh các thông số khi cần:
   - Số đường cong spline: Điều khiển mức độ thuật toán bám sát đường cong
   - Chuẩn hóa chiều dài cung: Làm cho việc lấy mẫu dọc theo đường cong đồng đều hơn

5. Nhấp "Xử Lý Hình Ảnh" để bắt đầu căn chỉnh

6. Xem kết quả và tải xuống hình ảnh đã xử lý

## Cách Hoạt Động

Quá trình căn chỉnh văn bản gồm hai giai đoạn chính:

1. **Giai Đoạn 1 (Dewarp Chặt)**:
   - Phát hiện các điểm ảnh đen trong hình
   - Khớp đường cong với các điểm ảnh này
   - Lấy mẫu vuông góc với đường cong này để tạo ra dòng văn bản thẳng

2. **Giai Đoạn 2 (Căn Chỉnh Cuối Cùng)**:
   - Lấy đầu ra từ giai đoạn đầu tiên
   - Thực hiện các điều chỉnh bổ sung bằng cách cuộn các cột hình ảnh
   - Tạo ra văn bản đã căn chỉnh cuối cùng

## Thông Số

- **Thông Số Giai Đoạn 1**:
  - Số đường cong spline: Giá trị cao hơn sẽ bám sát đường cong hơn nhưng có thể ít mượt mà
  - Chuẩn hóa chiều dài cung: Đảm bảo lấy mẫu đồng đều dọc theo đường cong

- **Thông Số Giai Đoạn 2**:
  - Số đường cong spline: Tinh chỉnh căn chỉnh cuối cùng
  - Chuẩn hóa chiều dài cung: Điều chỉnh việc lấy mẫu cho căn chỉnh cuối cùng
