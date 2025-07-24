# Medical_Prescription_Extractor
Reads Doctors Handwritten Prescription and Extracts data fields as output as json File
# Azure + GPT-4 Prescription Structurer

An intelligent, end-to-end pipeline that **extracts handwritten medical prescriptions** using Azure OCR and **structures them into clean, machine-readable JSON** using OpenAI’s GPT-4o.

Developed by **Subbiah C**, Department of Computer Science,  
**SRM Institute of Science and Technology – Kattankulathur (SRMIST-KTR)**

---

## 🔍 What This Project Does

Healthcare systems often rely on handwritten prescriptions, which are difficult to digitize at scale. This project solves that problem by:

- Using **Azure Cognitive Services OCR** to extract handwritten text
- Leveraging **GPT-4o** to convert raw text into a **structured JSON format**
- Saving both raw and structured outputs for downstream use

> Example use cases include:  
> - Pharmacy automation  
> - Health record digitization  
> - Medication data analysis and auditing  

---

## 📥 Input

- A handwritten prescription image (e.g., `Prescription_1.jpg`)

## 📤 Output

- `Extracted_Prescription_1.txt`: OCR-extracted raw text
- `Extracted_Prescription_1.json`: Structured prescription data

---

## 🗂 Structured JSON Format

Each prescription is converted into the following JSON structure:

```json
{
  "name": "John Doe",
  "age": "45",
  "gender": "Male",
  "date": "2024-06-01",
  "medicines": [
    {
      "name": "Paracetamol",
      "dosage": "500mg",
      "days": "5"
    },
    {
      "name": "Cetrizine",
      "dosage": "10mg",
      "days": "3"
    }
  ]
}
