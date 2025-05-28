# Thang Đo Đánh Giá Làm Thẳng Văn Bản (Dewarping Evaluation - DW)

Tài liệu này mô tả hệ thống đánh giá chất lượng của quá trình làm thẳng văn bản cong trong ứng dụng. Thang đo này giúp định lượng mức độ thành công của thuật toán trong việc chuyển đổi văn bản cong thành văn bản thẳng.

## 1. Tổng Quan Về Thang Đo DW

### 1.1. Mục Đích
Thang đo DW (Dewarping Evaluation) được thiết kế để:
- Đánh giá chất lượng đầu ra của quá trình làm thẳng văn bản
- So sánh hiệu quả của các tham số khác nhau
- Cung cấp phản hồi định lượng về kết quả xử lý
- Hỗ trợ tối ưu hóa thuật toán

### 1.2. Phạm Vi Đánh Giá
Thang đo bao gồm các khía cạnh chính:
- **Độ thẳng của dòng văn bản** (Line Straightness)
- **Chất lượng hình ảnh sau xử lý** (Image Quality)
- **Độ rõ nét của ký tự** (Character Clarity)
- **Tính nhất quán của khoảng cách** (Spacing Consistency)

## 2. Các Chỉ Số Đánh Giá Chi Tiết

### 2.1. Độ Thẳng Dòng Văn Bản (Line Straightness Score - LSS)

#### 2.1.1. Định Nghĩa
Đo lường mức độ thẳng của các dòng văn bản sau khi xử lý, so với một đường thẳng lý tưởng.

#### 2.1.2. Công Thức Tính
```
LSS = 1 - (Độ lệch trung bình / Chiều cao văn bản)

Trong đó:
- Độ lệch trung bình = Σ|yi - y_ref|/n
- yi: tọa độ y của pixel văn bản thứ i
- y_ref: tọa độ y của đường thẳng tham chiếu
- n: tổng số pixel văn bản
```

#### 2.1.3. Phân Loại Điểm
- **0.9 - 1.0**: Xuất sắc (văn bản rất thẳng)
- **0.8 - 0.9**: Tốt (văn bản khá thẳng)
- **0.7 - 0.8**: Trung bình (còn nhỏ uốn cong)
- **0.6 - 0.7**: Kém (nhiều uốn cong)
- **< 0.6**: Rất kém (không cải thiện được)

### 2.2. Chỉ Số Chất Lượng Hình Ảnh (Image Quality Index - IQI)

#### 2.2.1. Định Nghĩa
Đánh giá chất lượng tổng thể của hình ảnh sau xử lý, bao gồm độ tương phản và độ rõ nét.

#### 2.2.2. Các Thành Phần
- **Contrast Ratio (CR)**: Tỷ lệ tương phản giữa văn bản và nền
- **Edge Sharpness (ES)**: Độ sắc nét của biên ký tự
- **Noise Level (NL)**: Mức độ nhiễu trong ảnh

#### 2.2.3. Công Thức Tính
```
IQI = (CR × w1 + ES × w2 + (1-NL) × w3) / (w1 + w2 + w3)

Trong đó:
- w1, w2, w3: trọng số (thường w1=0.4, w2=0.4, w3=0.2)
- CR: Contrast Ratio ∈ [0,1]
- ES: Edge Sharpness ∈ [0,1]
- NL: Noise Level ∈ [0,1] (0 = không nhiễu)
```

### 2.3. Độ Rõ Nét Ký Tự (Character Clarity Score - CCS)

#### 2.3.1. Định Nghĩa
Đo lường mức độ rõ ràng và dễ đọc của từng ký tự sau khi làm thẳng.

#### 2.3.2. Phương Pháp Đánh Giá
- Phân tích histogram gradient của các vùng ký tự
- Tính toán độ sắc nét của biên ký tự
- Đánh giá tính toàn vẹn của cấu trúc ký tự

#### 2.3.3. Công Thức
```
CCS = (Số ký tự rõ nét / Tổng số ký tự) × Chất lượng trung bình

Chất lượng ký tự = (Gradient_strength × 0.6 + Completeness × 0.4)
```

### 2.4. Tính Nhất Quán Khoảng Cách (Spacing Consistency - SC)

#### 2.4.1. Định Nghĩa
Đánh giá tính đều đặn của khoảng cách giữa các từ và ký tự sau khi xử lý.

#### 2.4.2. Công Thức Tính
```
SC = 1 - (Độ lệch chuẩn khoảng cách / Khoảng cách trung bình)

Trong đó:
- Khoảng cách được đo giữa các centroid của ký tự liên tiếp
```

## 3. Thang Điểm Tổng Hợp

### 3.1. Điểm Số DW Tổng Hợp
```
DW_Score = LSS × 0.35 + IQI × 0.25 + CCS × 0.25 + SC × 0.15

Trong đó:
- LSS: Line Straightness Score (35%)
- IQI: Image Quality Index (25%)
- CCS: Character Clarity Score (25%)
- SC: Spacing Consistency (15%)
```

### 3.2. Phân Cấp Chất Lượng
- **A (9.0 - 10.0)**: Xuất sắc - Kết quả hoàn hảo
- **B (8.0 - 8.9)**: Tốt - Kết quả chấp nhận được cho hầu hết ứng dụng
- **C (7.0 - 7.9)**: Trung bình - Cần cải thiện một số khía cạnh
- **D (6.0 - 6.9)**: Kém - Nhiều vấn đề cần khắc phục
- **F (< 6.0)**: Không đạt - Không sử dụng được

## 4. Phương Pháp Đo Lường Thực Tế

### 4.1. Chuẩn Bị Dữ Liệu
1. **Ảnh Gốc**: Ảnh văn bản cong đầu vào
2. **Ảnh Kết Quả**: Ảnh văn bản đã làm thẳng
3. **Ground Truth**: Ảnh tham chiếu (nếu có)

### 4.2. Quy Trình Đánh Giá

#### Bước 1: Tiền Xử Lý
- Chuyển đổi ảnh sang thang độ xám
- Áp dụng ngưỡng để tách văn bản và nền
- Loại bỏ nhiễu nhỏ

#### Bước 2: Phân Tích Cấu Trúc
- Phát hiện các dòng văn bản
- Xác định vị trí các ký tự
- Tính toán các đặc trưng hình học

#### Bước 3: Tính Toán Điểm Số
- Áp dụng các công thức cho từng chỉ số
- Tính điểm tổng hợp DW_Score
- Phân loại kết quả theo thang điểm

### 4.3. Công Cụ Đánh Giá Tự Động

#### 4.3.1. Input Parameters
```python
def evaluate_dewarping(original_image, dewarped_image, reference_image=None):
    """
    Đánh giá chất lượng kết quả làm thẳng văn bản
    
    Args:
        original_image: Ảnh gốc (numpy array)
        dewarped_image: Ảnh đã làm thẳng (numpy array)
        reference_image: Ảnh tham chiếu (optional)
    
    Returns:
        dict: Điểm số chi tiết và tổng hợp
    """
```

#### 4.3.2. Output Format
```python
{
    'line_straightness_score': 0.85,
    'image_quality_index': 0.78,
    'character_clarity_score': 0.82,
    'spacing_consistency': 0.75,
    'overall_dw_score': 8.1,
    'grade': 'B',
    'detailed_analysis': {
        'contrast_ratio': 0.76,
        'edge_sharpness': 0.81,
        'noise_level': 0.15,
        'character_count': 156,
        'clear_characters': 142
    }
}
```

## 5. Ứng Dụng Thang Đo

### 5.1. Tối Ưu Hóa Tham Số
- Thử nghiệm với các giá trị `n_splines` khác nhau
- Đánh giá hiệu quả của `arc_equal` parameter
- So sánh kết quả giữa hai giai đoạn xử lý

### 5.2. Báo Cáo Chất Lượng
- Tạo báo cáo tự động cho từng ảnh xử lý
- Thống kê hiệu suất trên tập dữ liệu lớn
- Theo dõi xu hướng cải thiện theo thời gian

### 5.3. Benchmark và So Sánh
- So sánh với các thuật toán làm thẳng khác
- Đánh giá trên các loại văn bản khác nhau
- Xác định điểm mạnh và yếu của thuật toán

## 6. Hạn Chế và Cải Tiến

### 6.1. Hạn Chế Hiện Tại
- Phụ thuộc vào chất lượng ảnh đầu vào
- Khó đánh giá với văn bản có font chữ phức tạp
- Chưa xử lý được trường hợp văn bản đa ngôn ngữ

### 6.2. Hướng Cải Tiến
- Tích hợp OCR để đánh giá độ chính xác nhận dạng
- Sử dụng machine learning để học các pattern đánh giá
- Phát triển GUI để đánh giá thủ công và so sánh

## 7. Kết Luận

Thang đo DW cung cấp một framework toàn diện để đánh giá chất lượng của quá trình làm thẳng văn bản. Bằng cách kết hợp nhiều chỉ số khác nhau, thang đo này giúp:

- Đưa ra đánh giá khách quan về kết quả xử lý
- Hỗ trợ cải tiến thuật toán một cách có hệ thống
- Tạo cơ sở so sánh với các phương pháp khác
- Đảm bảo chất lượng sản phẩm cuối cùng

Việc áp dụng thang đo này sẽ giúp nâng cao chất lượng và độ tin cậy của ứng dụng làm thẳng văn bản cong.
