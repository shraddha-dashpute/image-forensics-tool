# forensic.py
from PIL import Image, ImageChops
import hashlib, io, piexif, numpy as np

def compute_hashes(file_bytes):
    md5 = hashlib.md5(file_bytes).hexdigest()
    sha1 = hashlib.sha1(file_bytes).hexdigest()
    sha256 = hashlib.sha256(file_bytes).hexdigest()
    return {"md5": md5, "sha1": sha1, "sha256": sha256}

# def extract_exif(file_bytes):
#     try:
#         exif_dict = piexif.load(file_bytes)
#         # convert to simple dict of entries (some values are bytes)
#         out = {}
#         for ifd in exif_dict:
#             for tag, val in exif_dict[ifd].items():
#                 out[f"{ifd}:{tag}"] = str(val)
#         return out
#     except Exception:
#         return {}

def extract_exif(file_bytes):
    from PIL import Image, ExifTags
    import io

    try:
        img = Image.open(io.BytesIO(file_bytes))
        exif_data = img._getexif()

        if not exif_data:
            return {}

        # Convert tag IDs to readable names
        exif = {}
        for tag_id, value in exif_data.items():
            tag = ExifTags.TAGS.get(tag_id, tag_id)
            exif[tag] = str(value)
        return exif

    except Exception as e:
        print("EXIF extraction error:", e)
        return {}


def calc_entropy(pil_img):
    gray = pil_img.convert("L")
    arr = np.array(gray).ravel()
    vals, counts = np.unique(arr, return_counts=True)
    probs = counts / counts.sum()
    entropy = -(probs * np.log2(probs)).sum()
    return float(entropy)

def create_ela(pil_img, quality=90):
    # Re-save image to JPEG in memory at given quality then diff
    buf = io.BytesIO()
    rgb = pil_img.convert("RGB")
    rgb.save(buf, format="JPEG", quality=quality)
    recompressed = Image.open(buf)
    ela_img = ImageChops.difference(rgb, recompressed)
    # amplify differences
    extrema = ela_img.getextrema()
    max_diff = max([e[1] for e in extrema]) or 1
    scale = 255.0 / max_diff
    ela_img = ela_img.point(lambda i: i * scale)
    return ela_img
