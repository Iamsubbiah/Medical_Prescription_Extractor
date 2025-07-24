import os
import requests
import time
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load keys from .env
load_dotenv()
AZURE_API_KEY = os.getenv("AZURE_API_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def extract_filename_stem(path):
    return os.path.splitext(os.path.basename(path))[0]

def extract_handwritten_text_azure(image_path):
    if not os.path.exists(image_path):
        print(f"File '{image_path}' not found.")
        return None, None

    filename_stem = extract_filename_stem(image_path)
    ocr_url = AZURE_ENDPOINT + "/vision/v3.2/read/analyze"

    headers = {
        'Ocp-Apim-Subscription-Key': AZURE_API_KEY,
        'Content-Type': 'application/octet-stream'
    }

    print(f"Uploading image '{image_path}' to Azure Read OCR...\n")
    with open(image_path, 'rb') as f:
        response = requests.post(ocr_url, headers=headers, data=f)

    if response.status_code != 202:
        print(f"API call failed: {response.status_code}")
        print("Response:", response.text)
        return None, None

    # Poll for result
    operation_url = response.headers["Operation-Location"]
    print("Processing OCR...")
    while True:
        result = requests.get(operation_url, headers={'Ocp-Apim-Subscription-Key': AZURE_API_KEY}).json()
        if result['status'] == 'succeeded':
            break
        elif result['status'] == 'failed':
            print("OCR failed.")
            return None, None
        time.sleep(1)

    lines = result['analyzeResult']['readResults'][0]['lines']
    full_text = "\n".join([line['text'] for line in lines])

    txt_output_file = f"Extracted_{filename_stem}.txt"
    with open(txt_output_file, "w", encoding="utf-8") as f:
        f.write(full_text)

    print(f"Text extracted and saved to '{txt_output_file}'")
    return full_text, filename_stem

def extract_structured_data_with_gpt(text, filename_stem):
    print("\nSending extracted text to GPT for structuring...\n")
    prompt = f"""
You are an assistant that extracts structured data from prescriptions.

Extract and format the following details from the prescription text below:
- patient name
- age
- gender
- date
- a list of medicines with dosage and days of consumption

Return the data in JSON format like this:
{{
  "name": "John Doe",
  "age": "45",
  "gender": "Male",
  "date": "2024-06-01",
  "medicines": [
    {{
      "name": "Paracetamol",
      "dosage": "500mg",
      "days": "5"
    }}
  ]
}}

Prescription text:
\"\"\"
{text}
\"\"\"
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    try:
        json_text = response.choices[0].message.content.strip()

        # Clean markdown code block formatting
        if json_text.startswith("```"):
            json_text = json_text.strip("```")
            if json_text.startswith("json"):
                json_text = json_text[4:].strip()

        data = json.loads(json_text)
        json_output_file = f"Extracted_{filename_stem}.json"
        with open(json_output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"Structured JSON saved to '{json_output_file}'")
        return data
    except Exception as e:
        print("Failed to parse GPT response:", e)
        print("Raw GPT response:\n", response.choices[0].message.content)
        return None

if __name__ == "__main__":
    IMAGE_PATH = "Prescription_2.jpg"  # change image filename here
    extracted_text, stem = extract_handwritten_text_azure(IMAGE_PATH)
    if extracted_text and stem:
        structured_json = extract_structured_data_with_gpt(extracted_text, stem)
        print("\nFinal Structured Data:\n", json.dumps(structured_json, indent=2))
