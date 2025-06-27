from flask import Flask, request, render_template_string
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)
SERVICE_LINK_FILE = 'service_link.csv'

HTML_FORM = """
<!doctype html>
<html lang="en">
<head>
  <title>CSV Upload Portal</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {
      background-color: #f8f9fa;
      padding-top: 50px;
    }
    .container {
      max-width: 600px;
    }
    .card {
      box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .upload-btn {
      width: 100%;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="card p-4">
      <h2 class="text-center mb-4">Upload CSV File</h2>
      <form method="POST" action="/upload-csv" enctype="multipart/form-data">
        <div class="mb-3">
          <input class="form-control" type="file" name="file" accept=".csv" required>
        </div>
        <button class="btn btn-primary upload-btn" type="submit">Upload</button>
      </form>
    </div>

    {% if info %}
      <div class="card p-4 mt-4 border-success">
        <h4 class="text-success">✅ Upload Summary</h4>
        <ul class="list-group list-group-flush">
          <li class="list-group-item"><strong>Timestamp:</strong> {{ info.timestamp }}</li>
          <li class="list-group-item"><strong>Rows in Uploaded File:</strong> {{ info.rows_uploaded }}</li>
          <li class="list-group-item"><strong>New Addresses Added:</strong> {{ info.new_addresses }}</li>
          <li class="list-group-item"><strong>Total Unique Addresses in service_link.csv:</strong> {{ info.total_unique }}</li>
        </ul>
      </div>
    {% endif %}
  </div>
</body>
</html>
"""


@app.route('/', methods=['GET'])
def home():
    return render_template_string(HTML_FORM)


@app.route('/upload-csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return 'No file uploaded', 400

    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        return 'No selected file', 400

    try:
        new_df = pd.read_csv(uploaded_file)

        address_col = None
        for col in new_df.columns:
            if 'address' in col.lower():
                address_col = col
                break

        if not address_col:
            return 'No address column found in uploaded file.', 400

        new_df.rename(columns={address_col: 'address'}, inplace=True)
        new_df['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        rows_uploaded = len(new_df)

        if os.path.exists(SERVICE_LINK_FILE):
            existing_df = pd.read_csv(SERVICE_LINK_FILE)
        else:
            existing_df = pd.DataFrame(columns=new_df.columns)

        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        before = len(existing_df)
        combined_df.drop_duplicates(subset='address', keep='first', inplace=True)
        after = len(combined_df)
        new_addresses = after - before

        combined_df.to_csv(SERVICE_LINK_FILE, index=False)

        return render_template_string(HTML_FORM, info={
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'rows_uploaded': rows_uploaded,
            'new_addresses': new_addresses,
            'total_unique': after
        })

    except Exception as e:
        return f"Error: {str(e)}", 500


if __name__ == '__main__':
    app.run(debug=True)
