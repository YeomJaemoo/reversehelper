import cv2
import numpy as np
import streamlit as st
from object_detector import *
import base64
st.title("Measure Object Size")
st.text("##오류해결이 필요함.")
st.text("로컬에서는 잘 처리되나 배포할 때 애러가 남. 스트리밍에 대한 해결 후 배포할 예정!")
# Load Aruco detector
parameters = cv2.aruco.DetectorParameters_create()
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)

# Load Object Detector
detector = HomogeneousBgDetector()

# Load Cap
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


# Create a placeholder for the image
image_placeholder = st.empty()

# Create a placeholder for the download link
download_placeholder = st.empty()

capture_button = st.button("캡쳐하기")

# Streamlit loop
while True:
    _, img = cap.read()

    # Get Aruco marker
    corners, _, _ = cv2.aruco.detectMarkers(img, aruco_dict, parameters=parameters)
    if corners:

        # Draw polygon around the marker
        int_corners = np.int0(corners)
        cv2.polylines(img, int_corners, True, (0, 255, 0), 5)

        # Aruco Perimeter
        aruco_perimeter = cv2.arcLength(corners[0], True)

        # Pixel to cm ratio
        pixel_cm_ratio = aruco_perimeter / 20

        contours = detector.detect_objects(img)

        # Draw objects boundaries
        for cnt in contours:
            # Get rect
            rect = cv2.minAreaRect(cnt)
            (x, y), (w, h), angle = rect

            # Get Width and Height of the Objects by applying the Ratio pixel to cm
            object_width = w / pixel_cm_ratio
            object_height = h / pixel_cm_ratio

            # Display rectangle
            box = cv2.boxPoints(rect)
            box = np.int0(box)

            cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1)
            cv2.polylines(img, [box], True, (255, 0, 0), 2)
            cv2.putText(img, "Width {} cm".format(round(object_width, 1)), (int(x - 100), int(y - 20)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)
            cv2.putText(img, "Height {} cm".format(round(object_height, 1)), (int(x - 100), int(y + 15)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)

    # Display the image
    image_placeholder.image(img, channels="BGR", use_column_width=True)

    # If the '캡쳐하기' button is clicked, save the current frame
    if capture_button:
        cv2.imwrite('captured_image.jpg', img)
        with open('captured_image.jpg', "rb") as img_file:
            img_bytes = img_file.read()
        b64_img = base64.b64encode(img_bytes).decode()
        img_href = f'<a href="data:image/jpg;base64,{b64_img}" download="captured_image.jpg">다운로드</a>'
        download_placeholder.markdown(img_href, unsafe_allow_html=True)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
