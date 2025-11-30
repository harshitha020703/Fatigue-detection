import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import av
import cv2
import mediapipe as mp
import time

st.set_page_config(page_title="Fatigue Detection", layout="centered")
st.title("Driver Fatigue Detection 🚗😴")
st.write("Enable Camera ⬇")

mp_face_mesh = mp.solutions.face_mesh.FaceMesh(
    refine_landmarks=False,    # disable iris processing → faster
    max_num_faces=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)


class Detector(VideoProcessorBase):
    def __init__(self):
        self.blink_start = None
        self.frame_count = 0

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img = cv2.resize(img, (480, 360))  # lower resolution → faster

        self.frame_count = (self.frame_count + 1) % 3
        if self.frame_count != 0:
            return av.VideoFrame.from_ndarray(img, format="bgr24")

        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = mp_face_mesh.process(rgb)

        if results.multi_face_landmarks:
            img_h, img_w, _ = img.shape
            landmarks = results.multi_face_landmarks[0].landmark

            # eye landmark drawing
            for id_ in [145, 159]:
                x = int(landmarks[id_].x * img_w)
                y = int(landmarks[id_].y * img_h)
                cv2.circle(img, (x, y), 4, (0, 255, 255), -1)

            eye_dist = abs(landmarks[159].y - landmarks[145].y)

            if eye_dist < 0.009:
                if self.blink_start is None:
                    self.blink_start = time.perf_counter()
                if time.perf_counter() - self.blink_start >= 1:
                    cv2.putText(img, "⚠ DROWSY", (50, 70),
                                cv2.FONT_HERSHEY_DUPLEX, 1.5, (0, 0, 255), 3)
            else:
                self.blink_start = None

        return av.VideoFrame.from_ndarray(img, format="bgr24")


webrtc_streamer(
    key="fatigue",
    video_processor_factory=Detector,
    media_stream_constraints={"video": True, "audio": False}
)
