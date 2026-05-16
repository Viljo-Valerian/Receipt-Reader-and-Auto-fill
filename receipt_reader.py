import streamlit as st
from groq import Groq
from PIL import Image
import pytesseract
import json
import io

# Add your tesseract.exe path here
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

st.title("Receipt Auto-Fill")

api_key = st.text_input("Groq API Key", type="password")
uploaded = st.file_uploader("Upload a receipt image", type=["jpg", "jpeg", "png", "webp"])

if uploaded and api_key:
    st.image(uploaded, caption="Uploaded receipt", use_column_width=True)

    if st.button("Extract from Receipt"):
        with st.spinner("Reading receipt..."):
            img_bytes = uploaded.read()
            img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
            receipt_text = pytesseract.image_to_string(img)

            client = Groq(api_key=api_key)
            prompt = f"""Extract recepit data. Analyze receipt text carefully.
For merchant_name: The shop name is usually at the very top of the receipt. Even if some letters look separated due to bad printing, make your best guess by looking up well-known business name based on context clues, nearby words, or common store name patterns.
For date: Look for any string that could be a date, like DD/MM/YYYY, DD.MM.YY, or even just 6 or more digit numbers clumped together, especially something with 26 (2026 is the current year). Make your best guess.
For currency: If no currency symbol is shown, guess based on the language of the receipt text.
For total_amount: Look for the largest amount, or words like "Total", "Grand Total", "Amount".
Return ONLY raw JSON, no markdown, no explanation:
{{"merchant_name": "...", "date": "...", "total_amount": "...", "currency": "..."}}

Use null only if you truly cannot make any guess.

Receipt text:
{receipt_text}"""

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=256,
            )
            raw = response.choices[0].message.content.strip()
            data = json.loads(raw.replace("```json", "").replace("```", "").strip())
            st.session_state.data = data

if "data" in st.session_state:
    st.subheader("Review & Edit")
    d = st.session_state.data
    merchant = st.text_input("Merchant Name", value=d.get("merchant_name") or "")
    date = st.text_input("Date", value=d.get("date") or "")
    total = st.text_input("Total Amount", value=str(d.get("total_amount") or ""))
    currency = st.text_input("Currency", value=d.get("currency") or "")

    if st.button("Submit"):
        st.success(f"Submitted: {merchant} | {date} | {total} {currency}")