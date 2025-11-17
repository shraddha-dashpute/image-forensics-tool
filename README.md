# Digital Image Integrity Verification Tool

Python + Streamlit app to check image authenticity (hashing, EXIF, entropy, ELA) and generate PDF reports.

## Run locally
1. `python -m pip install -r requirements.txt`
2. `python -m streamlit run app.py`


# Digital Image Integrity Verification Tool

A Python + Streamlit application that verifies image authenticity using **hashing (MD5/SHA1/SHA256)**, **EXIF metadata extraction**, **entropy analysis**, and **Error Level Analysis (ELA)**. The tool also generates a **PDF forensic report** containing all analysis results.

---

## Features
- Computes MD5, SHA1, and SHA256 hashes  
- Extracts EXIF metadata (camera details, timestamp, software)  
- Calculates entropy to detect anomalies  
- Performs Error Level Analysis (ELA) to highlight edited regions  
- Generates a PDF forensic report with original + ELA images  
- Simple and user-friendly Streamlit interface  

---

## Run Locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt

streamlit run app.py

http://localhost:8501

ImageForensicsTool/
│
├── app.py               # Main Streamlit application
├── forensic.py          # Hashing, EXIF, entropy, ELA processing
├── reportgen.py         # PDF report generator
├── requirements.txt     # Package dependencies
└── README.md            # Documentation
