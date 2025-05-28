import cv2
import numpy as np
from pygam import LinearGAM
from scipy.integrate import trapz
import os

def get_curve_integral(image_path, n_splines=8):
    """
    Ước tính đường cong trung tâm của văn bản trong ảnh và tính tích phân
    của độ lệch tuyệt đối của đường cong so với đường trung bình của nó.

    Args:
        image_path (str): Đường dẫn đến tệp ảnh.
        n_splines (int): Số lượng spline để sử dụng cho GAM.

    Returns:
        float: Giá trị tích phân đã tính. Trả về 0.0 nếu không tìm thấy văn bản
               hoặc nếu đường cong là một đường thẳng đứng. Trả về -1.0 nếu lỗi đọc ảnh.
    """
    image = cv2.imread(image_path)
    if image is None:
        print(f"Lỗi: Không thể đọc ảnh từ {image_path}")
        return -1.0 # Sử dụng giá trị đặc biệt để báo lỗi

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    kernel = np.ones((3, 3), np.uint8)
    eroded = cv2.erode(thresh, kernel, iterations=1)
    dilated = cv2.dilate(eroded, kernel, iterations=1)

    processed_thresh = dilated

    black_pixels = np.column_stack(np.where(processed_thresh == 0))

    if len(black_pixels) == 0:
        # print(f"Không tìm thấy pixel đen nào trong {image_path}. Giả sử là đường thẳng.")
        return 0.0

    X_coords = black_pixels[:, 1].reshape(-1, 1)
    y_coords = black_pixels[:, 0]

    if X_coords.shape[0] < n_splines + 2: # Cần đủ điểm cho GAM
        # print(f"Không đủ điểm dữ liệu trong {image_path} cho {n_splines} splines. Giả sử là đường thẳng.")
        return 0.0

    leftmost_x_data = np.min(X_coords)
    rightmost_x_data = np.max(X_coords)

    width_data = rightmost_x_data - leftmost_x_data
    if width_data == 0: # Trường hợp văn bản thẳng đứng
        # print(f"Văn bản trong {image_path} có vẻ thẳng đứng. Giả sử độ cong bằng 0.")
        return 0.0

    padding_x = int(0.05 * width_data)
    leftmost_x = max(0, leftmost_x_data - padding_x)
    rightmost_x = min(image.shape[1] - 1, rightmost_x_data + padding_x)


    try:
        gam = LinearGAM(n_splines=n_splines).fit(X_coords, y_coords)
    except Exception as e:
        print(f"Lỗi khi khớp GAM cho {image_path}: {e}. Giả sử là đường thẳng.")
        return 0.0

    num_pred_points = max(2, int(rightmost_x - leftmost_x + 1))
    X_pred = np.linspace(leftmost_x, rightmost_x, num=num_pred_points)

    if len(X_pred) < 2: # Không đủ điểm để tính tích phân
        return 0.0

    y_pred = gam.predict(X_pred)
    y_baseline = np.mean(y_pred)
    deviations = np.abs(y_pred - y_baseline)
    area = trapz(deviations, X_pred)

    return area

def calculate_dw_for_defined_pair(original_image_path, result_image_path, num_splines=8):
    """
    Tính điểm DW cho một cặp ảnh (gốc và kết quả) đã được định nghĩa đường dẫn.

    Args:
        original_image_path (str): Đường dẫn đến ảnh gốc.
        result_image_path (str): Đường dẫn đến ảnh kết quả.
        num_splines (int): Số lượng spline để sử dụng cho GAM.

    Returns:
        float: Điểm DW, hoặc None nếu có lỗi.
    """
    if not os.path.exists(original_image_path):
        print(f"Lỗi: Tệp ảnh gốc không tồn tại tại '{original_image_path}'.")
        return None
    if not os.path.exists(result_image_path):
        print(f"Lỗi: Tệp ảnh kết quả không tồn tại tại '{result_image_path}'.")
        return None

    print(f"\nĐang xử lý: '{os.path.basename(original_image_path)}' -> '{os.path.basename(result_image_path)}'")
    area_original = get_curve_integral(original_image_path, num_splines)
    area_dewarped = get_curve_integral(result_image_path, num_splines)

    if area_original == -1.0 or area_dewarped == -1.0: # Lỗi đọc ảnh từ get_curve_integral
        print("  Lỗi khi đọc một trong các tệp ảnh. Không thể tính DW.")
        return None

    print(f"  Diện tích gốc (Ar'): {area_original:.4f}")
    print(f"  Diện tích đã làm thẳng (Ar): {area_dewarped:.4f}")

    dw_j = 0.0
    if area_original == 0:
        if area_dewarped == 0:
            dw_j = 100.0
        else:
            dw_j = 0.0
    else:
        ratio = area_dewarped / area_original
        if ratio < 1.0:
            dw_j = (1.0 - ratio) * 100.0
        else:
            dw_j = 0.0

    print(f"  Điểm Dewarping (DW) cho cặp ảnh này: {dw_j:.2f}%")
    return dw_j

if __name__ == "__main__":
    # --- THAY ĐỔI ĐƯỜNG DẪN TỆP TẠI ĐÂY ---
    # Ví dụ sử dụng đường dẫn tuyệt đối (khuyến nghị để tránh nhầm lẫn)
    # original_image_file = r"D:\Git\curved-text-alignment\images\new1.png"
    # result_image_file = r"D:\Git\curved-text-alignment\result\new1_finnal.png"

    # Hoặc sử dụng đường dẫn tương đối nếu script này nằm trong cùng thư mục cha
    # của thư mục 'images' và 'result'
    # current_script_dir = os.path.dirname(os.path.abspath(__file__))
    # original_image_file = os.path.join(current_script_dir, "images", "new1.png")
    # result_image_file = os.path.join(current_script_dir, "result", "new1_finnal.png")

    # Hãy đảm bảo thay thế các đường dẫn ví dụ dưới đây bằng đường dẫn thực tế của bạn
    original_image_file = r"D:\curved-text-alignment\curved-text-alignment\images\HUS1.png" # << THAY THẾ ĐƯỜNG DẪN NÀY
    result_image_file = r"D:\curved-text-alignment\curved-text-alignment\result\HUS1_final.png"   # << THAY THẾ ĐƯỜNG DẪN NÀY
    # ------------------------------------

    num_splines_for_dw = 8 # Bạn có thể thay đổi giá trị này nếu cần

    print(f"Công cụ tính Điểm Dewarping (DW) cho một cặp ảnh được định nghĩa trong mã.")
    print(f"Số splines cho GAM (tính DW): {num_splines_for_dw}")
    print(f"Ảnh gốc: {original_image_file}")
    print(f"Ảnh kết quả: {result_image_file}")


    dw_score = calculate_dw_for_defined_pair(original_image_file, result_image_file, num_splines=num_splines_for_dw)

    if dw_score is not None:
        print(f"\nKết quả cuối cùng - Điểm DW: {dw_score:.2f}%")
    else:
        print("\nKhông thể tính toán điểm DW do lỗi (ví dụ: tệp không tồn tại hoặc không thể đọc).")

    # Hướng dẫn kiểm tra:
    # 1. Đảm bảo bạn đã cài đặt các thư viện cần thiết: opencv-python, numpy, pygam, scipy.
    #    pip install opencv-python numpy pygam scipy
    # 2. Sửa đổi các biến `original_image_file` và `result_image_file` trong khối
    #    `if __name__ == "__main__":` để trỏ đến các tệp ảnh của bạn.
    # 3. Chạy script: python ten_file_script.py