# Giải Thích Thuật Toán và Cách Hoạt Động Của Ứng Dụng

Tài liệu này mô tả chi tiết về các thuật toán cốt lõi được sử dụng trong ứng dụng làm thẳng văn bản cong, bao gồm thuật toán đường thẳng Bresenham, Mô hình Cộng Tổng quát (GAM), và cách chúng phối hợp hoạt động trong quy trình tổng thể của ứng dụng.

## 1. Thuật Toán Đường Thẳng Bresenham

### 1.1. Công Dụng

Thuật toán đường thẳng Bresenham là một thuật toán hiệu quả được sử dụng để vẽ (rasterize) một đoạn thẳng giữa hai điểm cho trước trên một lưới 2D, ví dụ như màn hình máy tính bao gồm các pixel. Mục tiêu chính của thuật toán là xác định tập hợp các pixel cần được chiếu sáng để tạo ra một hình ảnh gần đúng nhất với đoạn thẳng lý tưởng.

Ưu điểm lớn của thuật toán Bresenham là nó chỉ sử dụng các phép toán số nguyên (cộng, trừ, và dịch bit), giúp nó thực thi rất nhanh và phù hợp cho việc triển khai bằng phần cứng.

### 1.2. Cách Hoạt Động Chi Tiết

Giả sử chúng ta cần vẽ một đoạn thẳng giữa hai điểm `(x0, y0)` và `(x1, y1)`. Để đơn giản, xét trường hợp đoạn thẳng có độ dốc `m` nằm trong khoảng `0 <= m <= 1` và `x0 < x1`. Các trường hợp khác (ví dụ, độ dốc lớn hơn 1 hoặc độ dốc âm) có thể được xử lý bằng cách hoán đổi vai trò của x và y hoặc thay đổi hướng duyệt.

Ý tưởng cốt lõi của Bresenham là tại mỗi bước lặp theo trục x (từ `x0` đến `x1`), thuật toán quyết định xem tọa độ y của pixel tiếp theo nên giữ nguyên hay tăng lên 1 đơn vị. Quyết định này dựa trên một "tham số quyết định" (decision parameter), thường ký hiệu là `p`, đại diện cho sai số giữa đường thẳng thực tế và tâm của pixel hiện tại.

Các bước thực hiện:

1.  **Khởi tạo:**
    *   Tính `dx = x1 - x0` và `dy = y1 - y0`.
    *   Pixel đầu tiên được vẽ là `(x0, y0)`.
    *   Tham số quyết định ban đầu `p0 = 2*dy - dx`.

2.  **Lặp:**
    *   Với mỗi `x` từ `x0` đến `x1 - 1` (hoặc `x0 + 1` đến `x1` tùy cách triển khai):
        *   Nếu `p < 0`:
            *   Pixel tiếp theo là `(x_k+1, y_k)`. (y không đổi)
            *   Cập nhật tham số quyết định: `p_k+1 = p_k + 2*dy`.
        *   Nếu `p >= 0`:
            *   Pixel tiếp theo là `(x_k+1, y_k+1)`. (y tăng 1)
            *   Cập nhật tham số quyết định: `p_k+1 = p_k + 2*dy - 2*dx`.
        *   Vẽ pixel tiếp theo đã xác định.

Quá trình này đảm bảo rằng các pixel được chọn nằm gần nhất với đường thẳng lý tưởng.

### 1.3. Ứng Dụng Trong Ứng Dụng Này

Trong ứng dụng làm thẳng văn bản cong (`dewarp_rectify.py`), thuật toán Bresenham đóng vai trò quan trọng trong hàm `uncurve_text_tight`, cụ thể là sau khi:

1.  Mô hình GAM đã dự đoán được đường cong trung tâm của văn bản (`y_hat`).
2.  Nửa chiều cao của văn bản (`d`) đã được ước tính.

Quy trình như sau:

*   Với mỗi điểm `(X_new[i], y_hat[i])` trên đường cong trung tâm đã dự đoán, ứng dụng cần lấy một cột các pixel từ ảnh gốc. Cột pixel này phải **vuông góc** với đường cong `y_hat` tại điểm đó và kéo dài `d` pixel lên trên và `d` pixel xuống dưới so với `y_hat[i]`.
*   Hàm `find_perpendicular_points` tính toán tọa độ hai điểm đầu cuối của mỗi đoạn thẳng ngắn vuông góc này.
*   Sau đó, hàm `bresenham(x1, y1, x2, y2)` (từ thư viện `bresenham`) được gọi để tạo ra một danh sách (`bresenham_list`) chứa tất cả các tọa độ pixel nguyên nằm trên đoạn thẳng vuông góc đó.
*   Các giá trị pixel từ ảnh nhị phân đã qua tiền xử lý (`thresh`) tại các tọa độ trong `bresenham_list` được trích xuất.
*   Tập hợp các giá trị pixel này (đại diện cho một lát cắt vuông góc qua văn bản gốc) sau đó được nội suy để có chiều dài cố định `2*d+1` và trở thành một cột trong ảnh đã làm thẳng (`dewarp_image`).

Như vậy, Bresenham giúp "quét" ảnh gốc một cách chính xác dọc theo các đường vuông góc với đường cong văn bản, thu thập thông tin pixel cần thiết để "trải phẳng" văn bản.

## 2. Mô Hình Cộng Tổng Quát (Generalized Additive Models - GAMs)

### 2.1. Công Dụng

Mô hình Cộng Tổng quát (GAM) là một lớp các mô hình thống kê mở rộng từ Mô hình Tuyến tính Tổng quát (Generalized Linear Models - GLMs). Thay vì giả định một mối quan hệ tuyến tính giữa các biến độc lập và biến đổi của giá trị kỳ vọng của biến phụ thuộc, GAM cho phép các mối quan hệ phi tuyến phức tạp hơn.

Một mô hình GAM biểu diễn biến phụ thuộc (hay một hàm liên kết của nó) dưới dạng tổng của các hàm trơn (smooth functions) của các biến độc lập:

`g(E[Y]) = β₀ + f₁(x₁) + f₂(x₂) + ... + fₚ(xₚ)`

Trong đó:

*   `Y` là biến phụ thuộc.
*   `E[Y]` là giá trị kỳ vọng của `Y`.
*   `g(.)` là một hàm liên kết (link function), ví dụ: hàm logit cho dữ liệu nhị phân, hàm log cho dữ liệu đếm.
*   `β₀` là hệ số chặn (intercept).
*   `x₁, x₂, ..., xₚ` là các biến độc lập (predictors).
*   `f₁, f₂, ..., fₚ` là các hàm trơn phi tham số. Các hàm này thường được ước lượng bằng các kỹ thuật như splines (ví dụ: B-splines, cubic splines, thin plate splines).

Ưu điểm của GAM là khả năng mô hình hóa các mối quan hệ phi tuyến một cách linh hoạt mà vẫn giữ được tính cộng (additivity), giúp mô hình dễ diễn giải hơn so với các mô hình "hộp đen" phức tạp khác.

### 2.2. Cách Hoạt Động Trong Ứng Dụng Này

Trong ứng dụng này, GAM (cụ thể là `LinearGAM` từ thư viện `pygam`) được sử dụng trong cả hai hàm chính là `uncurve_text_tight` và `uncurve_text` để mô hình hóa đường cong của dòng văn bản.

1.  **Đầu vào:**
    *   `X`: Một mảng chứa các tọa độ x của các pixel được xác định là thuộc về văn bản (thường là các pixel đen sau khi ảnh đã được nhị phân hóa).
    *   `y`: Một mảng chứa các tọa độ y tương ứng của các pixel văn bản đó.

2.  **Quá trình:**
    *   Một đối tượng `LinearGAM` được khởi tạo, ví dụ: `gam = LinearGAM(n_splines=n_splines)`.
        *   Tham số `n_splines` kiểm soát độ "mềm dẻo" của đường cong mà GAM có thể học. Số lượng splines nhiều hơn cho phép đường cong uốn lượn phức tạp hơn để khớp với dữ liệu, nhưng cũng có nguy cơ overfitting nếu quá nhiều.
    *   Mô hình GAM sau đó được "huấn luyện" (fit) với dữ liệu pixel văn bản: `gam.fit(X, y)`.
        *   Trong quá trình này, GAM tìm ra các hàm spline tối ưu để mô tả mối quan hệ giữa tọa độ x và y của các pixel văn bản. Về cơ bản, nó "học" được hình dạng đường cong của dòng văn bản.

3.  **Đầu ra:**
    *   Sau khi huấn luyện, đối tượng `gam` có thể được sử dụng để dự đoán tọa độ y (`y_hat`) cho một tập hợp các tọa độ x mới (`X_new`): `y_hat = gam.predict(X_new)`.
    *   `X_new` thường là một dãy các giá trị x được tạo ra để cách đều nhau theo chiều ngang (hoặc cách đều theo chiều dài cung nếu `arc_equal=True`) và bao phủ toàn bộ chiều rộng của vùng văn bản.
    *   `y_hat` là một mảng các giá trị y dự đoán, đại diện cho đường cong trung tâm, đã được làm trơn của dòng văn bản. Đường cong này là nền tảng cho các bước làm thẳng tiếp theo.

## 3. Cách Hoạt Động Của Toàn Bộ Ứng Dụng

Ứng dụng làm thẳng văn bản cong hoạt động qua hai giai đoạn chính, được thực hiện bởi hai hàm `uncurve_text_tight` và `uncurve_text`.

### 3.1. Giai Đoạn 1: `uncurve_text_tight` (Làm thẳng văn bản - Tiếp cận chặt chẽ)

Mục tiêu của giai đoạn này là tạo ra một phiên bản "thô" của văn bản đã được làm thẳng bằng cách lấy mẫu các pixel dọc theo các đường vuông góc với đường cong văn bản ước lượng.

1.  **Tải và Tiền xử lý Ảnh:**
    *   Ảnh đầu vào được đọc (`cv2.imread`).
    *   Chuyển đổi sang ảnh thang độ xám (`cv2.cvtColor`).
    *   Áp dụng ngưỡng Otsu để tạo ảnh nhị phân (`cv2.threshold`), tách biệt văn bản (thường là pixel đen) khỏi nền (pixel trắng).
    *   Ảnh nhị phân được đệm thêm viền trắng (`pad_binary_image_with_ones`) để tránh các vấn đề xử lý ở biên ảnh.
    *   Thực hiện phép co ảnh (erosion) rồi đến giãn ảnh (dilation) (`cv2.erode`, `cv2.dilate`) để loại bỏ nhiễu nhỏ và lấp đầy các khoảng trống nhỏ bên trong các ký tự.

2.  **Phát hiện Pixel Văn bản:**
    *   Xác định vị trí của tất cả các pixel đen (`np.where(thresh == 0)`), coi đây là các pixel thuộc về văn bản.
    *   Tìm tọa độ x ngoài cùng bên trái (`leftmost_x`) và bên phải (`rightmost_x`) của vùng chứa văn bản.
    *   Chuẩn bị dữ liệu `X` (tọa độ x của các pixel đen) và `y` (tọa độ y của các pixel đen) để cung cấp cho mô hình GAM.

3.  **Khớp Mô hình GAM (Giai đoạn 1):**
    *   Khởi tạo một đối tượng `LinearGAM` với số lượng splines `n1_splines`.
    *   Huấn luyện mô hình GAM (`gam.fit(X, y)`) để học đường cong trung tâm của văn bản dựa trên các pixel đã phát hiện.

4.  **Tạo Dãy Tọa độ X Mới và Dự đoán Đường Cong:**
    *   Tạo một dãy các điểm `X_new` cách đều nhau theo chiều ngang (hoặc theo chiều dài cung nếu `arc_equal=True`) từ `leftmost_x` đến `rightmost_x`.
    *   Sử dụng GAM đã huấn luyện để dự đoán các giá trị `y_hat` tương ứng cho `X_new`. `y_hat` lúc này biểu diễn đường cong trung tâm ước lượng của văn bản.

5.  **Ước tính Chiều cao Văn bản:**
    *   Hàm `find_distance_d` được gọi. Hàm này tìm một khoảng cách `d` (nửa chiều cao của văn bản) sao cho nếu dịch chuyển đường cong `y_hat` lên trên `d` đơn vị và xuống dưới `d` đơn vị, thì hai đường cong mới này sẽ bao phủ tất cả các pixel văn bản gốc. Điều này giúp xác định "bề dày" của dòng văn bản.

6.  **Tạo Ảnh Đã Làm thẳng (Sử dụng Bresenham):**
    *   Khởi tạo một ảnh mới `dewarp_image` (ảnh kết quả của giai đoạn 1) với toàn pixel trắng. Kích thước của ảnh này là `(2*d + 1)` chiều cao và `len(X_new)` chiều rộng.
    *   Lặp qua từng điểm `(X_new[i], y_hat[i])` trên đường cong trung tâm:
        *   Sử dụng `find_perpendicular_points` để xác định hai điểm đầu cuối của một đoạn thẳng ngắn, vuông góc với `y_hat` tại `X_new[i]`, và có chiều dài `2d`.
        *   Sử dụng thuật toán **Bresenham** (`list(bresenham(x1, y1, x2, y2))`) để lấy danh sách tất cả các tọa độ pixel nguyên nằm trên đoạn thẳng vuông góc này.
        *   Trích xuất các giá trị pixel từ ảnh nhị phân `thresh` tại các tọa độ thu được từ Bresenham.
        *   Chuỗi giá trị pixel này (một cột dọc) được nội suy lại bằng `reshape_array_with_interpolation` để có đúng `2*d + 1` pixel.
        *   Gán cột pixel đã nội suy này vào cột thứ `i` của `dewarp_image`.
    *   Kết quả là `dewarp_image` chứa văn bản đã được "trải phẳng" một phần.

7.  **Lưu Kết quả Giai đoạn 1:**
    *   Ảnh `dewarp_image` được lưu lại. Ảnh này sẽ là đầu vào cho giai đoạn 2.

### 3.2. Giai Đoạn 2: `uncurve_text` (Làm thẳng văn bản - Tinh chỉnh)

Mục tiêu của giai đoạn này là tinh chỉnh kết quả từ giai đoạn 1, làm cho văn bản thẳng hơn nữa bằng cách dịch chuyển các cột pixel.

1.  **Tải và Tiền xử lý Ảnh:**
    *   Ảnh đầu vào là kết quả của hàm `uncurve_text_tight` (ảnh đã được làm thẳng một phần).
    *   Tương tự giai đoạn 1, ảnh được chuyển sang thang độ xám, áp dụng ngưỡng Otsu, và thực hiện co/giãn ảnh.

2.  **Phát hiện Pixel Văn bản và Khớp GAM (Giai đoạn 2):**
    *   Quá trình phát hiện pixel văn bản và chuẩn bị dữ liệu `X`, `y` tương tự giai đoạn 1.
    *   Lưu ý: Trong hàm này, tọa độ `y` của pixel đen có thể được tính là `thresh.shape[0] - black_pixels[:, 0]` (đảo ngược trục y) để phù hợp hơn với cách GAM thường xử lý các đường cong có xu hướng đi lên từ trái sang phải.
    *   Một mô hình GAM mới (`LinearGAM(n_splines=n2_splines)`) được huấn luyện với dữ liệu này để tinh chỉnh đường cong dựa trên ảnh đã qua giai đoạn 1.

3.  **Dự đoán Đường cong và Thực hiện Căn chỉnh Cuối cùng:**
    *   Tạo `X_new` và dự đoán `y_hat` mới từ GAM của giai đoạn 2.
    *   **Căn chỉnh bằng cách Dịch chuyển Cột (Column Shifting):**
        *   Lặp qua từng cột `j` của ảnh (từ `leftmost_x` đến `rightmost_x`):
            *   Tính toán lượng dịch chuyển dọc (`roll_amount`) cần thiết cho cột `j`. Lượng dịch chuyển này được tính dựa trên độ lệch của giá trị `y_hat` tại cột đó so với một đường tham chiếu ngang (thường là đường giữa ảnh: `thresh.shape[0]/2`). Cụ thể: `roll_amount = round(y_hat[index_corresponding_to_j] - thresh.shape[0]/2)`.
            *   Sử dụng hàm `np.roll` để dịch chuyển (cuộn) tất cả các pixel trong cột `j` của ảnh màu gốc (`image`) theo chiều dọc một lượng bằng `roll_amount`. Thao tác này được thực hiện cho cả ba kênh màu (R, G, B).
        *   Kỹ thuật này có tác dụng "kéo" các phần của văn bản nằm trên đường cong `y_hat` về một đường thẳng ngang.

4.  **Lưu Kết quả Cuối cùng:**
    *   Ảnh đã được căn chỉnh hoàn toàn sau giai đoạn 2 được lưu lại. Đây là kết quả cuối cùng của ứng dụng.

Tóm lại, ứng dụng sử dụng một cách tiếp cận hai giai đoạn. Giai đoạn đầu dùng GAM và Bresenham để "trải phẳng" văn bản một cách mạnh mẽ. Giai đoạn hai tiếp tục dùng GAM để tinh chỉnh đường cong và sau đó dịch chuyển các cột pixel để đạt được độ thẳng tối ưu cho văn bản.
