from flask import Flask, render_template, request, jsonify
import cv2
from pyzbar.pyzbar import decode
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Define the scope and credentials for accessing Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
# Replace 'your-service-account.json' with the actual filename or provide the full path
credentials = ServiceAccountCredentials.from_json_keyfile_name('your-service-account.json', scope)
gc = gspread.authorize(credentials)

# Open the Google Sheet by its URL and specify the worksheet by name
sheet_url = 'https://docs.google.com/spreadsheets/d/18qa612LxTadmS6QgUhGPkIEkUgqqKYxSFrKgwlPVVd8/edit?usp=sharing'  # Replace with your Google Sheet URL
worksheet_name = 'Sheet1'  # Replace with your actual sheet name
worksheet = gc.open_by_url(sheet_url).worksheet(worksheet_name)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan_qr():
    if request.method == 'POST':
        qr_image_data = request.json.get('qrImageData', None)
        if qr_image_data:
            # Decode QR codes from the image data
            qr_image = cv2.imdecode(qr_image_data, cv2.IMREAD_COLOR)
            decoded_objects = decode(qr_image)

            for obj in decoded_objects:
                data = obj.data.decode('utf-8')
                print("QR Code Data:", data)

                try:
                    # Send the QR code data to Google Sheets
                    worksheet.append_row([data])
                    print("Data sent to Sheets successfully.")
                except Exception as e:
                    print("Error sending data to Sheets:", str(e))

            return jsonify({"message": "QR code scanned and data sent to Sheets successfully"})

if __name__ == '__main__':
    app.run(debug=True)
