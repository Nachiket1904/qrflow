import streamlit as st
from PIL import Image
import numpy as np
import io
import cv2
from qrcodegen import QrCode

# Helper: Generate QR code image
def generate_qr_image(text: str, scale: int = 10) -> Image.Image:
    qr = QrCode.encode_text(text, QrCode.Ecc.LOW)
    size = qr.get_size()
    border = 4
    pixels = np.full(((size + border * 2) * scale, (size + border * 2) * scale), 255, dtype=np.uint8)
    
    for y in range(size):
        for x in range(size):
            if qr.get_module(x, y):
                x1 = (x + border) * scale
                y1 = (y + border) * scale
                pixels[y1:y1+scale, x1:x1+scale] = 0
    return Image.fromarray(pixels)

# Helper: Decode QR code from image using OpenCV
def decode_qr_from_image(image: Image.Image) -> str:
    cv_image = np.array(image.convert('RGB'))
    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(cv_image)
    return data

# Set up session state for step control
if "step" not in st.session_state:
    st.session_state["step"] = 1

# Streamlit UI
st.set_page_config(page_title="QR Code Visualizer", layout="centered")
st.title("🔳 QR Code Generator & Visual Decoder")

# Step 1: Input
st.subheader("Step 1: Enter Text or URL")
user_input = st.text_input("Enter text or URL", value="")


# Function to show step visuals
def show_step(step_num, title, description, image_path=None):
    with st.container():
        st.markdown(f"### Step {step_num}: {title}")
        st.info(description)
        if image_path:
            st.image(image_path, use_column_width=True)


if user_input:
    # Step 2: Generate QR
    st.subheader("Step 2: QR Code Generated")
    qr_img = generate_qr_image(user_input)
    st.image(qr_img, caption="Generated QR Code", use_column_width=False)

    # Step 3: Simulate QR Scanning - Interactive Steps
    st.subheader("Step 3: Simulate Camera Scanning (Step-by-Step)")

    # Show steps based on current step state
    step = st.session_state["step"]

    if st.button("Next Step"):
        if step < 6:
            st.session_state["step"] += 1

    
    # Step simulation UI
    if step >= 1:
        show_step(
            1,
            "Camera Capture",
            "📷 Your phone camera captures the image of the QR code.",
            "C:\\Users\\chinmay\\Videos\\codes\\python\\QR_Attendance-main\\assets\\step1_camera_capture.png"
        )

    if step >= 2:
        show_step(
            2,
            "Pattern Detection",
            "🧱 QR code patterns (finder, alignment, timing) are identified.",
            "C:\\Users\\chinmay\\Videos\\codes\\python\\QR_Attendance-main\\assets\\step2_pattern_detection.png"
        )

    if step >= 3:
        show_step(
            3,
            "Perspective Correction",
            "📐 The QR code image is corrected to a square for accurate decoding.",
            "C:\\Users\\chinmay\\Videos\\codes\\python\\QR_Attendance-main\\assets\\step3_perspective_correction.png"
        )

    if step >= 4:
        show_step(
            4,
            "Bitstream Extraction",
            "🧬 The QR code modules are translated into a binary bitstream.",
            "C:\\Users\\chinmay\\Videos\\codes\\python\\QR_Attendance-main\\assets\\step4_bitstream_extraction.png"
        )

    if step >= 5:
        show_step(
            5,
            "Error Correction & Decoding",
            "🔓 The bitstream is decoded to recover the original text using error correction.",
            "C:\\Users\\chinmay\\Videos\\codes\\python\\QR_Attendance-main\\assets\\step5_error_correction.png"
        )
    if step >= 6:
        st.success("✅ **Decoded Content:**")
        decoded_text = decode_qr_from_image(qr_img)
        st.code(decoded_text, language='text')

        # Optional Download
        buf = io.BytesIO()
        qr_img.save(buf, format="PNG")
        st.download_button(
            label="Download QR Code as PNG",
            data=buf.getvalue(),
            file_name="qr_code.png",
            mime="image/png"
        )



# Footer
st.markdown("---")
st.markdown("""
Made with ❤️ by [**Nachiket Kapure**](mailto:kapnachi1904@gmail.com)  
[GitHub](https://github.com/Nachiket1904) | [LinkedIn](https://www.linkedin.com/in/nachiket-kapure-ml-enginner)
""")
