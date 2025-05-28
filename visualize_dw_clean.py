import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
from evaluation_system import compute_dw
import pandas as pd

def detect_text_baselines(image_path, num_lines=3):
    """
    Phát hiện các baseline của văn bản từ ảnh
    """
    print(f"  Đang phát hiện baseline từ: {image_path}")
    
    # Đọc ảnh và chuyển sang grayscale
    image = cv2.imread(image_path)
    if image is None:
        print(f"    LỖI: Không thể đọc ảnh: {image_path}")
        return None
        
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    print(f"    Kích thước ảnh: {gray.shape}")
    
    # Áp dụng threshold để tách văn bản
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Tìm các pixel đen (văn bản)
    black_pixels = np.column_stack(np.where(thresh == 0))
    print(f"    Số pixel văn bản: {len(black_pixels)}")
    
    if len(black_pixels) == 0:
        print(f"    CẢNH BÁO: Không tìm thấy văn bản trong ảnh: {image_path}")
        return None
    
    # Chia ảnh thành các dải ngang để phát hiện các dòng
    height = gray.shape[0]
    width = gray.shape[1]
    
    # Chia thành num_lines dải
    strip_height = height // num_lines
    baselines = []
    
    for i in range(num_lines):
        y_start = i * strip_height
        y_end = (i + 1) * strip_height if i < num_lines - 1 else height
        
        # Lấy các pixel trong dải này
        strip_pixels = black_pixels[(black_pixels[:, 0] >= y_start) & 
                                  (black_pixels[:, 0] < y_end)]
        
        if len(strip_pixels) > 0:
            # Tạo baseline bằng cách lấy trung bình y cho mỗi x
            x_coords = []
            y_coords = []
            
            # Chia x thành các bin
            x_bins = np.linspace(0, width-1, min(width//10, 50))
            
            for j in range(len(x_bins)-1):
                x_min, x_max = x_bins[j], x_bins[j+1]
                pixels_in_bin = strip_pixels[(strip_pixels[:, 1] >= x_min) & 
                                           (strip_pixels[:, 1] < x_max)]
                
                if len(pixels_in_bin) > 0:
                    x_coords.append((x_min + x_max) / 2)
                    y_coords.append(np.mean(pixels_in_bin[:, 0]))
            
            if len(y_coords) > 5:  # Chỉ giữ baseline có đủ điểm
                baselines.append(np.array(y_coords))
                print(f"    Dòng {i+1}: {len(y_coords)} điểm")
    
    print(f"    Tổng cộng tìm thấy: {len(baselines)} dòng")
    return baselines if baselines else None

def load_image_pairs():
    """Tải các cặp ảnh gốc và kết quả từ thư mục"""
    print("Đang tìm kiếm các cặp ảnh...")
    image_pairs = []
    
    # Các cặp ảnh có sẵn
    pairs = [
        ("tv.png", "tv_finnal.png"),
        ("new1.png", "new1_finnal.png"), 
        ("gray.png", "gray_ouput.png"),
        ("viettay.png", "viettay_ouput.png"),
        ("HUS1.png", "HUS1_final.png")
    ]
    
    for original, result in pairs:
        original_path = f"images/{original}"
        result_path = f"result/{result}"
        
        print(f"  Kiểm tra: {original} -> {result}")
        if os.path.exists(original_path) and os.path.exists(result_path):
            image_pairs.append((original_path, result_path, original.split('.')[0]))
            print(f"    ✓ Tìm thấy cặp ảnh hợp lệ")
        else:
            print(f"    ✗ Thiếu file: {original_path if not os.path.exists(original_path) else result_path}")
    
    print(f"Tổng cộng tìm thấy {len(image_pairs)} cặp ảnh hợp lệ")
    return image_pairs

def visualize_real_dw_evaluation():
    """
    Visualize kết quả của hàm compute_dw với ảnh thực từ thư mục images và result
    """
    # Thiết lập matplotlib
    plt.rcParams['font.size'] = 10
    plt.rcParams['font.family'] = 'DejaVu Sans'
    
    try:
        plt.style.use('seaborn-v0_8')
    except:
        plt.style.use('default')
    
    # Tải các cặp ảnh
    image_pairs = load_image_pairs()
    
    if not image_pairs:
        print("Không tìm thấy cặp ảnh nào!")
        return
    
    # Tính DW score cho từng cặp ảnh
    results = []
    
    for original_path, result_path, name in image_pairs:
        print(f"Đang xử lý: {name}")
        
        # Phát hiện baseline từ ảnh gốc và ảnh kết quả
        original_baselines = detect_text_baselines(original_path)
        result_baselines = detect_text_baselines(result_path)
        
        if original_baselines and result_baselines:
            # Tính DW score cho ảnh gốc
            original_score = compute_dw(original_baselines)
            
            # Tính DW score cho ảnh kết quả  
            result_score = compute_dw(result_baselines)
            
            improvement = result_score - original_score
            
            results.append({
                'name': name,
                'original_score': original_score,
                'result_score': result_score,
                'improvement': improvement,
                'original_baselines': original_baselines,
                'result_baselines': result_baselines
            })
        else:
            print(f"Không thể phát hiện baseline cho {name}")
    
    if not results:
        print("Không có kết quả nào để hiển thị!")
        return
    
    # Tạo visualization
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Đánh Giá Kết Quả Dewarp Bằng Hàm compute_dw', fontsize=16, fontweight='bold')
    
    # 1. So sánh điểm số DW
    ax1 = axes[0, 0]
    names = [r['name'] for r in results]
    original_scores = [r['original_score'] for r in results]
    result_scores = [r['result_score'] for r in results]
    
    x = np.arange(len(names))
    width = 0.35
    
    bars1 = ax1.bar(x - width/2, original_scores, width, label='Anh goc', color='lightcoral', alpha=0.7)
    bars2 = ax1.bar(x + width/2, result_scores, width, label='Sau dewarp', color='lightblue', alpha=0.7)
    
    ax1.set_xlabel('Ten anh')
    ax1.set_ylabel('Diem DW Score')
    ax1.set_title('So sanh Diem DW Score Truoc va Sau Dewarp')
    ax1.set_xticks(x)
    ax1.set_xticklabels(names, rotation=45)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Thêm giá trị lên các cột
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{height:.1f}', ha='center', va='bottom', fontsize=9)
    
    for bar in bars2:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{height:.1f}', ha='center', va='bottom', fontsize=9)
    
    # 2. Mức độ cải thiện
    ax2 = axes[0, 1]
    improvements = [r['improvement'] for r in results]
    colors = ['green' if imp > 0 else 'red' for imp in improvements]
    
    bars = ax2.bar(names, improvements, color=colors, alpha=0.7)
    ax2.set_xlabel('Ten anh')
    ax2.set_ylabel('Muc cai thien (diem)')
    ax2.set_title('Muc Do Cai Thien Sau Dewarp')
    ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    ax2.grid(True, alpha=0.3)
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
    
    # Thêm giá trị lên các cột
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + (0.5 if height > 0 else -1),
                f'{height:.1f}', ha='center', va='bottom' if height > 0 else 'top', fontsize=9)
    
    # 3. Phân phối điểm số
    ax3 = axes[1, 0]
    ax3.boxplot([original_scores, result_scores], labels=['Anh goc', 'Sau dewarp'])
    ax3.set_ylabel('Diem DW Score')
    ax3.set_title('Phan Pho Diem DW Score')
    ax3.grid(True, alpha=0.3)
    
    # 4. Bảng tóm tắt kết quả
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    # Tạo bảng dữ liệu
    table_data = []
    for r in results:
        table_data.append([
            r['name'],
            f"{r['original_score']:.1f}",
            f"{r['result_score']:.1f}", 
            f"{r['improvement']:.1f}",
            "✓" if r['improvement'] > 0 else "✗"
        ])
    
    table = ax4.table(cellText=table_data,
                     colLabels=['Ten anh', 'Diem goc', 'Diem sau', 'Cai thien', 'Ket qua'],
                     cellLoc='center',
                     loc='center')
    
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 1.5)
    
    # Tô màu header
    for i in range(5):
        table[(0, i)].set_facecolor('#4CAF50')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    ax4.set_title('Tom Tat Ket Qua Danh Gia', fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.show()
    
    # In kết quả chi tiết
    print("\n" + "="*50)
    print("KET QUA DANH GIA DEWARP CHI TIET")
    print("="*50)
    
    for r in results:
        print(f"\n{r['name'].upper()}:")
        print(f"  - Diem goc: {r['original_score']:.2f}")
        print(f"  - Diem sau dewarp: {r['result_score']:.2f}")
        print(f"  - Cai thien: {r['improvement']:.2f} diem")
        print(f"  - Danh gia: {'Thanh cong' if r['improvement'] > 0 else 'Can cai thien'}")
    
    # Thống kê tổng quan
    avg_original = np.mean(original_scores)
    avg_result = np.mean(result_scores) 
    avg_improvement = np.mean(improvements)
    
    print(f"\nTHONG KE TONG QUAN:")
    print(f"  - Diem trung binh goc: {avg_original:.2f}")
    print(f"  - Diem trung binh sau dewarp: {avg_result:.2f}")
    print(f"  - Cai thien trung binh: {avg_improvement:.2f} diem")
    print(f"  - Ty le thanh cong: {sum(1 for imp in improvements if imp > 0)}/{len(improvements)} ({100*sum(1 for imp in improvements if imp > 0)/len(improvements):.1f}%)")

def show_baseline_comparison():
    """
    Hiển thị baseline của ảnh gốc và sau dewarp để so sánh trực quan
    """
    image_pairs = load_image_pairs()
    
    if not image_pairs:
        return
    
    fig, axes = plt.subplots(len(image_pairs), 2, figsize=(14, 4*len(image_pairs)))
    if len(image_pairs) == 1:
        axes = axes.reshape(1, -1)
    
    for idx, (original_path, result_path, name) in enumerate(image_pairs):
        print(f"Visualizing baselines for: {name}")
        
        # Phát hiện baseline
        original_baselines = detect_text_baselines(original_path)
        result_baselines = detect_text_baselines(result_path)
        
        if original_baselines and result_baselines:
            # Tính DW scores
            original_score = compute_dw(original_baselines)
            result_score = compute_dw(result_baselines)
            
            # Plot ảnh gốc với baseline
            original_img = cv2.imread(original_path)
            original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
            
            axes[idx, 0].imshow(original_img)
            axes[idx, 0].set_title(f'{name} - Goc (DW: {original_score:.1f})')
            
            # Vẽ baseline
            colors = ['red', 'green', 'blue', 'yellow', 'purple']
            for i, baseline in enumerate(original_baselines):
                x_coords = np.linspace(0, original_img.shape[1]-1, len(baseline))
                axes[idx, 0].plot(x_coords, baseline, color=colors[i % len(colors)], linewidth=2)
            
            axes[idx, 0].axis('off')
            
            # Plot ảnh kết quả với baseline
            result_img = cv2.imread(result_path)
            result_img = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
            
            axes[idx, 1].imshow(result_img)
            axes[idx, 1].set_title(f'{name} - Sau Dewarp (DW: {result_score:.1f})')
            
            # Vẽ baseline
            for i, baseline in enumerate(result_baselines):
                x_coords = np.linspace(0, result_img.shape[1]-1, len(baseline))
                axes[idx, 1].plot(x_coords, baseline, color=colors[i % len(colors)], linewidth=2)
            
            axes[idx, 1].axis('off')
    
    plt.tight_layout()
    plt.suptitle('So Sanh Baseline Truoc va Sau Dewarp', fontsize=16, fontweight='bold', y=1.02)
    plt.show()

if __name__ == "__main__":
    print("Bat dau danh gia ket qua dewarp voi anh thuc...")
    
    # Hiển thị kết quả đánh giá DW
    visualize_real_dw_evaluation()
    
    print("\n" + "="*50)
    print("Hien thi so sanh baseline...")
    
    # Hiển thị so sánh baseline
    show_baseline_comparison()
    
    print("\nVisualization hoan tat!")
