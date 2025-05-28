import numpy as np

def compute_dw(y_coords, normalize_height=None):
    """
    Tính Dewarping Evaluation Measure (DW) từ các dòng y (baseline) sau khi nắn thẳng.

    Parameters:
    - y_coords: 2D numpy array, mỗi hàng là 1 dòng baseline gồm các tọa độ y.
    - normalize_height: (tùy chọn) chiều cao chuẩn H để chuẩn hóa DW. Nếu None, sẽ dùng chiều cao dòng tối đa.

    Returns:
    - dw_score: Điểm DW trong khoảng [0, 100], càng gần 100 nghĩa là nắn càng thẳng.
    """
    if not isinstance(y_coords, np.ndarray):
        y_coords = np.array(y_coords)

    # Bước 1: Tính độ lệch chuẩn của từng dòng
    stds = np.std(y_coords, axis=1)  # Độ lệch chuẩn theo từng dòng

    # Bước 2: Tính trung bình độ lệch chuẩn
    mean_std = np.mean(stds)

    # Bước 3: Chuẩn hóa theo chiều cao dòng
    if normalize_height is None:
        normalize_height = np.ptp(y_coords)  # peak-to-peak: max - min

    # Tránh chia cho 0
    if normalize_height == 0:
        return 100.0

    # Bước 4: Tính điểm DW (lý tưởng = 100%)
    dw_score = 100 * (1 - mean_std / normalize_height)
    return round(dw_score, 2)

if __name__ == "__main__":
    # Test với dữ liệu mẫu
    y_coords = np.array([[10, 12, 11], [20, 22, 21], [30, 32, 31]])
    normalize_height = 50
    score = compute_dw(y_coords, normalize_height)
    print(f"Dewarping Score: {score}/100")
    print(f"Điểm đánh giá độ thẳng của baseline: {score:.2f}")
    
    # Test với dữ liệu khác
    print("\n--- Test với dữ liệu khác ---")
    y_coords_curved = np.array([[10, 15, 20, 18, 12], [30, 35, 40, 38, 32], [50, 55, 60, 58, 52]])
    score_curved = compute_dw(y_coords_curved, normalize_height)
    print(f"Dewarping Score (văn bản cong): {score_curved:.2f}/100")
    
    y_coords_straight = np.array([[10, 10, 10, 10, 10], [30, 30, 30, 30, 30], [50, 50, 50, 50, 50]])
    score_straight = compute_dw(y_coords_straight, normalize_height)
    print(f"Dewarping Score (văn bản thẳng): {score_straight:.2f}/100")