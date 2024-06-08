import cv2
import numpy as np
import streamlit as st
from object_detector import *
import base64

st.title("Measure Object Size")
st.text("## 오류해결이 필요함.")
st.text("로컬에서는 잘 처리되나 배포할 때 애러가 남. 스트리밍에 대한 해결 후 배포할 예정!")

# Aruco 모듈을 가져오고 예외를 처리합니다.
try:
    parameters = cv2.aruco.DetectorParameters_create()
    aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)
except AttributeError:
    st.error("Aruco 모듈을 찾을 수 없습니다. opencv-contrib-python이 설치되어 있는지 확인하세요.")

# 객체 감지기 로드
detector = HomogeneousBgDetector()

# 비디오 캡처 로드
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# 이미지를 표시할 자리 표시자 생성
image_placeholder = st.empty()

# 다운로드 링크를 표시할 자리 표시자 생성
download_placeholder = st.empty()

capture_button = st.button("캡쳐하기")

# Streamlit 루프
while True:
    ret, img = cap.read()

    if not ret:
        st.error("카메라 스트림을 읽을 수 없습니다.")
        break

    # Aruco 마커 감지
    try:
        corners, _, _ = cv2.aruco.detectMarkers(img, aruco_dict, parameters=parameters)
        if corners:
            # 마커 주위에 다각형 그리기
            int_corners = np.int0(corners)
            cv2.polylines(img, int_corners, True, (0, 255, 0), 5)

            # Aruco 둘레 계산
            aruco_perimeter = cv2.arcLength(corners[0], True)

            # 픽셀을 cm로 변환하는 비율
            pixel_cm_ratio = aruco_perimeter / 20

            contours = detector.detect_objects(img)

            # 객체 경계선 그리기
            for cnt in contours:
                # 직사각형 구하기
                rect = cv2.minAreaRect(cnt)
                (x, y), (w, h), angle = rect

                # 픽셀을 cm로 변환하여 객체의 너비와 높이 구하기
                object_width = w / pixel_cm_ratio
                object_height = h / pixel_cm_ratio

                # 사각형 표시
                box = cv2.boxPoints(rect)
                box = np.int0(box)

                cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1)
                cv2.polylines(img, [box], True, (255, 0, 0), 2)
                cv2.putText(img, "너비 {} cm".format(round(object_width, 1)), (int(x - 100), int(y - 20)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)
                cv2.putText(img, "높이 {} cm".format(round(object_height, 1)), (int(x - 100), int(y + 15)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)
    except Exception as e:
        st.error(f"Aruco 마커 처리 중 오류 발생: {e}")

    # 이미지 표시
    image_placeholder.image(img, channels="BGR", use_column_width=True)

    # '캡쳐하기' 버튼이 클릭되면 현재 프레임을 저장합니다.
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
