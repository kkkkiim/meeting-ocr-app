import pytesseract
from PIL import Image
import re

def extract_card_info(image_file):
    image = Image.open(image_file)
    text = pytesseract.image_to_string(image, lang='kor+eng')

    date_match = re.search(r'\d{4}[-./]\d{2}[-./]\d{2}', text)
    amount_match = re.search(r'(\d{1,3}(,\d{3})+)', text)
    store_match = re.search(r'(프랭크버거|커피|식당|고기집|호텔)', text)
    approval_match = re.search(r'승인\s?번호\s?:?\s?(\d{4,})', text)

    return {
        "date": date_match.group() if date_match else "추출 실패",
        "amount": amount_match.group().replace(",", "") if amount_match else "추출 실패",
        "store_name": store_match.group() if store_match else "추출 실패",
        "approval_no": approval_match.group(1) if approval_match else "추출 실패"
    }
