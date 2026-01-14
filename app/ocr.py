from paddleocr import PaddleOCR

ocr = None

def extract_text(image_path: str) -> str:
    global ocr

    if ocr is None:
        # Lightweight English OCR
        ocr = PaddleOCR(
            use_angle_cls=False,
            lang='en',
            use_gpu=False,
            show_log=False
        )

    result = ocr.ocr(image_path, cls=False)

    text_lines = []
    for line in result:
        for word in line:
            text_lines.append(word[1][0])

    return "\n".join(text_lines).strip()
