# AI STYLIST APP (FINAL CLEAN VERSION 🚀)
# Run: streamlit run app.py

import os

# ---- SAFE IMPORTS (prevents crash if not installed) ----
try:
    import streamlit as st
except ImportError:
    raise ImportError("Streamlit not installed. Check requirements.txt")

try:
    import numpy as np
    import cv2
except ImportError:
    import streamlit as st
    st.error("❌ OpenCV or NumPy not installed. Fix requirements.txt")
    st.stop()

# ❌ Removed OpenAI (no payment needed)
# We'll use smart rule-based AI instead 😈

# ---- INPUT ----
uploaded_file = st.file_uploader("Upload your selfie", type=["jpg", "png", "jpeg"])

occasion = st.selectbox(
    "Select occasion",
    ["Casual", "Party", "Wedding", "Formal", "College"]
)

# ---- FUNCTIONS ----
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

# ---- PROCESS ----
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

    # DISPLAY
    st.subheader("📸 Original")
    st.image(original, channels="BGR")

    st.subheader("💇 Preview")
    st.image(img, channels="BGR")

    st.subheader("🧠 Detected")
    st.write(f"Face Shape: {face_shape}")
    st.write(f"Skin Tone: {skin_tone}")

    if st.button("Generate Glow Up 🔥"):
        st.subheader("🔥 AI Advice")

        # ---- FREE AI LOGIC ----
        advice = ""

        # Face shape based suggestions
        if face_shape == "round":
            advice += "• Try sharp hairstyles (fade, undercut) to add angles.
"
        elif face_shape == "oval":
            advice += "• Most hairstyles suit you 😎 try textured or messy styles.
"
        else:
            advice += "• Medium length hair with volume works best.
"

        # Skin tone based suggestions
        if skin_tone == "light":
            advice += "• Dark colors like black, navy, maroon look 🔥
"
        elif skin_tone == "medium":
            advice += "• Earth tones (olive, brown, beige) suit you well 🌿
"
        else:
            advice += "• Bright colors (white, yellow, pastel) pop on you ✨
"

        # Occasion based suggestions
        if occasion == "Party":
            advice += "• Go for stylish jacket + sneakers combo 😈
"
        elif occasion == "Formal":
            advice += "• Try clean shirt + blazer look 💼
"
        elif occasion == "Wedding":
            advice += "• Traditional or classy suit look 💍
"
        elif occasion == "College":
            advice += "• Casual hoodie + jeans vibe 🎧
"
        else:
            advice += "• Keep it chill with t-shirt + jeans 😎
"

        st.write(advice)

print("✅ CLEAN VERSION READY 🚀")
