import streamlit as st
from rembg import remove
from PIL import Image
from io import BytesIO
import base64

st.set_page_config(layout="wide", page_title="Image Background Remover")

st.write("## Remove background from your image")
st.sidebar.write("## Upload and download :gear:")

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im

def fix_image(image_bytes):
    if isinstance(image_bytes, BytesIO):
        image = Image.open(image_bytes)
    else:
        image = Image.open(BytesIO(image_bytes))
    fixed = remove(image)
    return image, fixed

def main():
    st.title("Google Lens with Streamlit")
    
    # 카메라로 이미지를 입력받거나 파일을 업로드하기
    img_file_buffer = st.camera_input("Take a picture")
    uploaded_images = st.sidebar.file_uploader("Upload an image", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

    session_state = st.session_state

    if "processed_images" not in session_state:
        session_state.processed_images = []
        session_state.last_processed = 0

    # Process Images 버튼을 누르기 전에 미리 이미지를 처리하기
    new_images = []

    if img_file_buffer is not None:
        # 카메라로 찍은 이미지를 읽어오기
        image_bytes = img_file_buffer.getvalue()
        if image_bytes is not None:
            if len(image_bytes) > MAX_FILE_SIZE:
                st.error("The uploaded file is too large. Please upload an image smaller than 5MB.")
            else:
                original_image, fixed_image = fix_image(image_bytes)
                new_images.append((original_image, fixed_image))

    if uploaded_images is not None:
        # 업로드한 이미지를 읽어오기
        for upload in uploaded_images[session_state.last_processed:]:
            image_bytes = upload.read()

            if image_bytes is not None:
                if len(image_bytes) > MAX_FILE_SIZE:
                    st.error("The uploaded file is too large. Please upload an image smaller than 5MB.")
                else:
                    original_image, fixed_image = fix_image(image_bytes)
                    new_images.append((original_image, fixed_image))

    if st.sidebar.button("Process Images"):
        # Process Images 버튼을 누르면 새롭게 처리한 이미지만 추가하기
        session_state.processed_images.extend(new_images)
        session_state.last_processed = len(uploaded_images)

    for i, (original_image, fixed_image) in enumerate(session_state.processed_images):
        col1, col2 = st.columns(2)
        col1.write("Original Image :camera:")
        col1.image(original_image)
        col2.write("Fixed Image :wrench:")
        col2.image(fixed_image)
        st.sidebar.markdown("")
        st.sidebar.download_button(f"Download fixed image #{i+1}", convert_image(fixed_image), f"fixed_{i+1}.png", "image/png", key=f"download_button_{i}")

if __name__ == "__main__":
    main()
