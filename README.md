# 📤 CSV Upload Portal (Flask App)

A simple and responsive web portal built with **Flask** that allows users to upload `.csv` files containing address data. Uploaded addresses are appended to a master file (`service_link.csv`) while ensuring **deduplication** based on the address field. The portal provides a clean summary after each upload.

---

## 🌟 Features

- 🖥️ User-friendly web interface with **Bootstrap 5**
- 📁 Upload and parse `.csv` files
- ✅ Automatically detects the column containing "address"
- 🔄 Appends new rows to `service_link.csv`
- 🧼 Deduplicates entries based on the address column
- 📊 Displays summary of upload:
  - Timestamp
  - Rows uploaded
  - New addresses added
  - Total unique addresses

---

## 🚀 Getting Started

### 📦 Prerequisites

Make sure you have Python 3.7+ installed.

Install required packages:

```bash
pip install flask pandas
```
### ▶️ Run the App

```bash
python app.py
```
#### Then open your browser and go to:
#### http://127.0.0.1:5000

### 🧠 How It Works
1. The web form allows a user to upload a `.csv` file.
2. The backend detects the column containing "address".
3. Each uploaded row is timestamped and added to the `service_link.csv`.
4. Duplicate addresses are removed automatically.
5. A summary of the upload is shown to the user.

---------------------------------------------------------------------------------------------------------------------------------------------------
