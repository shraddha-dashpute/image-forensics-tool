# app.py
import streamlit as st
from PIL import Image
import io
from forensic import compute_hashes, extract_exif, calc_entropy, create_ela
from reportgen import generate_report
import tempfile

st.set_page_config("Image Forensics", layout="wide")

st.title("Digital Image Integrity Verification")

uploaded = st.file_uploader("Upload image (JPEG/PNG)", type=['jpg','jpeg','png'])
if uploaded:
    file_bytes = uploaded.read()
    st.image(file_bytes, caption="Uploaded Image", use_column_width=True)

    # Hashes
    hashes = compute_hashes(file_bytes)
    st.subheader("File Hashes")
    st.write(hashes)

    # EXIF
    exif = extract_exif(file_bytes)
    st.subheader("EXIF Metadata")
    if exif:
        st.json(exif)
    else:
        st.write("No EXIF metadata found or it's been stripped.")

    # Open PIL image
    img = Image.open(io.BytesIO(file_bytes))

    # Entropy
    entropy = calc_entropy(img)
    st.write(f"Entropy (grayscale): {entropy:.4f}")

    # ELA
    ela_img = create_ela(img, quality=90)
    st.subheader("Error Level Analysis (ELA)")
    st.image(ela_img, use_column_width=True)

    # Suspicion level heuristic (simple)
    suspicion = "Low"
    if entropy < 4.0 or (max(hashes.values()) and False):
        suspicion = "Medium"
    # NOTE: you should combine ELA bright-spot count, missing metadata, entropy thresholds
    if not exif or entropy < 3.5:
        suspicion = "High"

    st.markdown(f"**Suspicion Level:** {suspicion}")

    # Generate PDF
    if st.button("Generate PDF Report"):
        tmpf = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
        results = {
            "md5": hashes['md5'],
            "sha1": hashes['sha1'],
            "sha256": hashes['sha256'],
            "entropy": f"{entropy:.4f}",
            "suspicion": suspicion
        }
        generate_report(tmpf.name, img, ela_img, results)
        with open(tmpf.name, "rb") as f:
            st.download_button("Download Report", f, file_name="forensic_report.pdf", mime="application/pdf")
