import streamlit as st
from ocr_agent import extract_card_info

st.title("카드 영수증 OCR 추출기 (Google Vision)")

uploaded_file = st.file_uploader("영수증 이미지를 업로드하세요", type=["png", "jpg", "jpeg"])

if uploaded_file:
    result = extract_card_info(uploaded_file)

    st.subheader("OCR 추출 결과")
    st.write(f"날짜: {result['date']}")
    st.write(f"금액: {result['amount']}")
    st.write(f"상호명: {result['store_name']}")
    st.write(f"승인번호: {result['approval_no']}")
