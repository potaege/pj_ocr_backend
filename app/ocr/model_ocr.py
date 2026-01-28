import os
os.environ["DISABLE_MODEL_SOURCE_CHECK"] = "True"
os.environ["GLOG_minloglevel"] = "3"
os.environ["FLAGS_logtostderr"] = "0"
os.environ["FLAGS_enable_pir_api"] = "0"
os.environ["FLAGS_enable_pir_in_executor"] = "0"
os.environ["FLAGS_use_mkldnn"] = "0"     
os.environ["FLAGS_use_onednn"] = "0"      

from paddleocr import PaddleOCR

# ตัวปกติ
ocr = PaddleOCR(lang="th", use_textline_orientation=True)

# ตัวที่ปิดการเดาองศาเอกสาร/แก้เอกสาร (กันหมุนมั่ว)
ocr_no_doc = PaddleOCR(
    lang="th",
    use_textline_orientation=True,
    use_doc_orientation_classify=False,
    use_doc_unwarping=False
)

ocr_raw = PaddleOCR(
    lang="th",
    use_textline_orientation=False,  
    use_doc_orientation_classify=False,
    use_doc_unwarping=False
)

def run_ocr(image_bgr, no_doc: bool = False, no_textline: bool = False):
    
    if no_doc and no_textline:
        engine = ocr_raw
    elif no_doc:
        engine = ocr_no_doc
    else:
        engine = ocr

    try:
        res = engine.predict(image_bgr)
        if not isinstance(res, (list, tuple, dict, str)) and hasattr(res, "__iter__"):
            res = list(res)
        return res, "predict"
    except Exception:
        pass

    try:
        res = engine.ocr(image_bgr)
        if not isinstance(res, (list, tuple, dict, str)) and hasattr(res, "__iter__"):
            res = list(res)
        return res, "ocr"
    except Exception as e:
        raise RuntimeError(f"OCR failed: {e}")
