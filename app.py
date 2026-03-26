import os

missing_modules = []

def safe_import(module_name, install_name=None):
    try:
        return __import__(module_name)
    except ImportError:
        missing_modules.append((module_name, install_name or module_name))
        return None

streamlit = safe_import("streamlit")
cv2 = safe_import("cv2", "opencv-python")
numpy = safe_import("numpy")
openai_mod = safe_import("openai")
PIL_mod = safe_import("PIL", "pillow")

if missing_modules:
    print("❌ Missing dependencies:")
    for mod, install in missing_modules:
        print(f"- {mod} → pip install {install}")
    print("\n⚠️ Install these and rerun.")

if streamlit:
    import streamlit as st
    import numpy as np
    import cv2
    from openai import OpenAI

    API_KEY = os.getenv("OPENAI_API_KEY") or "YOUR_API_KEY"

    st.set_page_config(page_title="AI Stylist 🔥", layout="centered")

    st.title("👗 AI Stylist PRO 🌐")
    st.write("Upload your photo → AI analyzes + gives REAL suggestions 😎")

    if API_KEY == "YOUR_API_KEY":
        st.warning("⚠️ Add your OpenAI API key")

    client = OpenAI(api_key=API_KEY)

    uploaded_file = st.file_uploader("Upload your selfie", type=["jpg", "png", "jpeg"])

    occasion = st.selectbox(
        "Select occasion",
        ["Casual", "Party", "Wedding", "Formal", "College"]
    )

    def estimate_face_shape(w, h):
        ratio = w / h
        if ratio > 0.9:
            return "round"
        elif ratio > 0.75:
            return "oval"
        else:
            return "long"

    def estimate_skin_tone(face_region):
        avg = np.mean(face_region)
        if avg > 170:
            return "light"
        elif avg > 120:
            return "medium"
        else:
            return "dark"

    if uploaded_file:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)

        if img is None:
            st.error("❌ Image error")
            st.stop()

        original = img.copy()

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) > 0:
            st.success("Face detected ✅")

            for (x, y, w, h) in faces:
                face_shape = estimate_face_shape(w, h)
                skin_tone = estimate_skin_tone(gray[y:y+h, x:x+w])

                overlay = img.copy()
                center = (x + w // 2, int(y - h * 0.15))
                axes = (w // 2, int(h * 0.4))

                cv2.ellipse(overlay, center, axes, 0, 0, 180, (30,30,30), -1)
                img = cv2.addWeighted(overlay, 0.6, img, 0.4, 0)

        else:
            st.warning("Face not clear 😅")
            face_shape = "unknown"
            skin_tone = "unknown"

        st.subheader("📸 Original")
        st.image(original, channels="BGR")

        st.subheader("💇 Preview")
        st.image(img, channels="BGR")

        st.subheader("🧠 Detected")
        st.write(f"Face Shape: {face_shape}")
        st.write(f"Skin Tone: {skin_tone}")

        if st.button("Generate Glow Up 🔥"):
            if API_KEY == "YOUR_API_KEY":
                st.error("Add API key bro 😭")
            else:
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{
                            "role": "user",
                            "content": f"Face shape: {face_shape}, Skin tone: {skin_tone}, Occasion: {occasion}. Suggest styles."
                        }]
                    )

                    st.subheader("🔥 AI Advice")
                    st.write(response.choices[0].message.content)

                except Exception as e:
                    st.error(f"API Error: {str(e)}")

print("✅ STABLE VERSION READY 🚀")