import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import os
from PIL import Image
import tempfile
from dewarp_rectify import uncurve_text_tight, uncurve_text

# Set page configuration
st.set_page_config(
    page_title="Công Cụ Chỉnh Sửa Văn Bản Cong",
    page_icon="📝",
    layout="wide"
)

# App title and description
st.title("Công Cụ Chỉnh Sửa Văn Bản Cong")
st.markdown("Công cụ này giúp bạn làm thẳng và căn chỉnh văn bản cong trong hình ảnh.")
# Sidebar for parameters
st.sidebar.header("Thông Số")

# Image selection
st.sidebar.subheader("Chọn Hình Ảnh")
image_source = st.sidebar.radio(
    "Chọn nguồn hình ảnh:",
    ["Tải Hình Ảnh Lên", "Sử Dụng Hình Ảnh Mẫu"]
)

if image_source == "Tải Hình Ảnh Lên":
    uploaded_file = st.sidebar.file_uploader("Tải lên một hình ảnh", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        # Create images directory if it doesn't exist
        image_dir = "images"
        os.makedirs(image_dir, exist_ok=True)
        
        # Save the uploaded file to the images directory
        uploaded_filename = uploaded_file.name
        input_path = os.path.join(image_dir, uploaded_filename)
        
        # Write the uploaded file to the images directory
        with open(input_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        
        # Display the uploaded image
        st.sidebar.image(uploaded_file, caption="Hình Ảnh Đã Tải Lên", use_column_width=True)
        st.sidebar.success(f"📁 Đã lưu vào: `{input_path}`")
    else:
        st.warning("Vui lòng tải lên một hình ảnh để bắt đầu.")
        st.stop()
else:
    # List available sample images
    image_dir = "images"
    sample_images = [f for f in os.listdir(image_dir) if f.endswith((".png", ".jpg", ".jpeg"))]
    selected_image = st.sidebar.selectbox("Chọn một hình ảnh mẫu:", sample_images)
    input_path = os.path.join(image_dir, selected_image)
    
    # Display the selected sample image
    st.sidebar.image(input_path, caption=f"Hình Ảnh Mẫu: {selected_image}", use_column_width=True)

# Algorithm parameters
st.sidebar.subheader("Thông Số Thuật Toán")

# Parameters for the first stage (uncurve_text_tight)
st.sidebar.markdown("#### Thông Số Giai Đoạn 1")
n1_splines = st.sidebar.slider("Số đường cong spline cho phát hiện đường văn bản:", 3, 20, 6)
arc_equal_tight = st.sidebar.checkbox("Sử dụng chuẩn hóa chiều dài cung cho giai đoạn 1", True)

# Parameters for the second stage (uncurve_text)
st.sidebar.markdown("#### Thông Số Giai Đoạn 2")
n2_splines = st.sidebar.slider("Số đường cong spline cho điều chỉnh cuối cùng:", 3, 20, 9)
arc_equal_final = st.sidebar.checkbox("Sử dụng chuẩn hóa chiều dài cung cho giai đoạn 2", False)

# Process button
process_button = st.sidebar.button("Xử Lý Hình Ảnh", type="primary")

# Create a placeholder for displaying results
result_container = st.container()

def plot_to_image(fig):
    """Convert a matplotlib figure to an image for Streamlit."""
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight', pad_inches=0)
    buf.seek(0)
    return Image.open(buf)

# Process the image when the button is clicked
if process_button:
    with st.spinner("Đang xử lý hình ảnh..."):
        try:
            # Create temporary file paths for outputs
            with tempfile.NamedTemporaryFile(delete=False, suffix='_intermediate.png') as tmp_file1:
                intermediate_path = tmp_file1.name
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='_final.png') as tmp_file2:
                final_path = tmp_file2.name

            # Disable matplotlib's interactive mode to avoid showing the plots
            plt.ioff()
            
            # First stage processing (uncurve_text_tight)
            st.text("Đang chạy xử lý giai đoạn 1...")
            first_stage_figures = uncurve_text_tight(input_path, intermediate_path, n1_splines, arc_equal=arc_equal_tight, return_figures=True)
            
            # Second stage processing (uncurve_text)
            st.text("Đang chạy xử lý giai đoạn 2...")            
            second_stage_figures = uncurve_text(intermediate_path, final_path, n2_splines, arc_equal=arc_equal_final, return_figures=True)
            
            # Determine output filenames based on input source
            if image_source == "Tải Hình Ảnh Lên":
                base_name = os.path.splitext(uploaded_file.name)[0]
            else:
                base_name = os.path.splitext(selected_image)[0]
            
            # Create result directory if it doesn't exist
            result_dir = "result"
            os.makedirs(result_dir, exist_ok=True)
            
            # Define output paths in result directory
            intermediate_result_path = os.path.join(result_dir, f"{base_name}_output.png")
            final_result_path = os.path.join(result_dir, f"{base_name}_final.png")
            
            # Save results to result directory
            intermediate_image = cv2.imread(intermediate_path)
            cv2.imwrite(intermediate_result_path, intermediate_image)
            
            final_image = cv2.imread(final_path)
            cv2.imwrite(final_result_path, final_image)
            
            # Display the results
            with result_container:
                st.subheader("Kết Quả Xử Lý")
                
                # Stage 1 results
                st.markdown("### Giai Đoạn 1: Phát Hiện Đường Cong Văn Bản")
                cols = st.columns(len(first_stage_figures))
                for i, (title, fig) in enumerate(first_stage_figures):
                    with cols[i]:
                        if title == "Text with Curve Detection":
                            title = "Văn Bản với Đường Cong Phát Hiện"
                        elif title == "Perpendicular Sampling Lines":
                            title = "Đường Lấy Mẫu Vuông Góc"
                        elif title == "First Stage Result":
                            title = "Kết Quả Giai Đoạn 1"
                        st.image(plot_to_image(fig), caption=title)
                
                # Stage 2 results
                st.markdown("### Giai Đoạn 2: Căn Chỉnh Cuối Cùng")
                cols = st.columns(len(second_stage_figures))
                for i, (title, fig) in enumerate(second_stage_figures):
                    with cols[i]:
                        if title == "Second Stage Curve Detection":
                            title = "Phát Hiện Đường Cong Giai Đoạn 2"
                        elif title == "Final Result":
                            title = "Kết Quả Cuối Cùng"
                        st.image(plot_to_image(fig), caption=title)
                
                # Final result
                st.markdown("### Kết Quả Cuối Cùng")
                final_image_rgb = cv2.cvtColor(final_image, cv2.COLOR_BGR2RGB)
                st.image(final_image_rgb, caption="Văn Bản Đã Được Căn Chỉnh")
             
            
            try:
                os.unlink(intermediate_path)
                os.unlink(final_path)
                # No need to delete uploaded images as they are saved in images/ folder
            except:
                pass  # Ignore cleanup errors
            plt.close('all')
            
        except Exception as e:
            st.error(f"Đã xảy ra lỗi trong quá trình xử lý: {str(e)}")
            st.exception(e)
else:
    with result_container:
        st.info("Nhấp 'Xử Lý Hình Ảnh' để bắt đầu căn chỉnh văn bản.")
# Footer
st.markdown("---")
