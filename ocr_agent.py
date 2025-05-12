from google.cloud import vision
from google.oauth2 import service_account
import streamlit as st 
import json             
import re

# ✅ 수정된 부분: Streamlit Secrets에서 GCP 키 로딩
service_account_info = json.loads(st.secrets["GCP_KEY_JSON"])
credentials = service_account.Credentials.from_service_account_info(service_account_info)
client = vision.ImageAnnotatorClient(credentials=credentials)

def extract_card_info(image_file):
    # 이미지 파일 바이트로 읽기
    content = image_file.read()
    image = vision.Image(content=content)

    # OCR 요청
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if not texts:
        return {"error": "텍스트 추출 실패"}

    # 전체 인식된 텍스트
    text = texts[0].description

    # 정규식으로 정보 추출
    date_match = re.search(r'\d{4}[-./]\d{2}[-./]\d{2}', text)
    amount_match = re.search(r'(\d{1,3}(,\d{3})+)', text)
    store_match = re.search(r'(프랭크버거|커피|식당|고기|호텔)', text)
    approval_match = re.search(r'승인\s?번호\s?:?\s?(\d{4,})', text)

    return {
        "raw_text": text,
        "date": date_match.group() if date_match else "없음",
        "amount": amount_match.group().replace(",", "") if amount_match else "없음",
        "store_name": store_match.group() if store_match else "없음",
        "approval_no": approval_match.group(1) if approval_match else "없음"
    }
