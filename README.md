# Receipt-Reader-and-Auto-fill

## Functionality

The goal of this web app is using generative AI to extract data from an image of a receipt and auto-fills a form. It uses Tesseract OCR to extract raw text from the image. The text is then passed to Groq's LLaMA model with a prompt asking it to identify the specified data and return results as raw JSON. The data is stored in memory only, nothing is saved to disk or a database.

## Extracted Data

The extracted data for the form includes:
- Merchant name
- Date
- Total amount
- Currency

## Prerequisites

The prerequisite installations for this web app includes:
1. Python 3.8+
2. Groq API key (free at free at [console.groq.com](https://console.groq.com))
3. Tesseract OCR
    - **For Windows:** download the installer from https://github.com/UB-Mannheim/tesseract/wiki
    - **Mac:** `brew install tesseract`
    - **Linux:** `sudo apt install tesseract-ocr`

## How to setup and run

1. Have the prerequisites installed.
2. (For Windows) In `receipt_reader.py`, add the path to tesseract.exe installed in your machine on this line:

```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```
3. Run `receipt_reader.py`, then open http://localhost:8501 in your browser.

```bash
streamlit run app.py
```
4. Paste your Groq API key before using the app.

## How it works

1. Upload an image of a receipt.
2. Tesseract OCR reads the text from the image.
3. Groq extracts the key fields from the text.
4. A pre-filled form appears for the user to review and edit.
5. Submit to save the data in-session.

## Model & Prompt
Model: llama-3.3-70b-versatile via Groq API
Prompt: "Extract recepit data. Analyze receipt text carefully.
For merchant_name: The shop name is usually at the very top of the receipt. Even if some letters look separated due to bad printing, make your best guess by looking up well-known business name based on context clues, nearby words, or common store name patterns.
For date: Look for any string that could be a date, like DD/MM/YYYY, DD.MM.YY, or even just 6 or more digit numbers clumped together, especially something with 26 (2026 is the current year). Make your best guess.
For currency: If no currency symbol is shown, guess based on the language of the receipt text.
For total_amount: Look for the largest amount, or words like "Total", "Grand Total", "Amount".
Return ONLY raw JSON, no markdown, no explanation:
{{"merchant_name": "...", "date": "...", "total_amount": "...", "currency": "..."}}
Use null only if you truly cannot make any guess."
