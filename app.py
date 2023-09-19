from flask import Flask, render_template, request, jsonify
import cv2
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Define the scope and credentials for accessing Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('your-service-account.json', scope)
gc = gspread.authorize(credentials)

# Open the Google Sheet by its URL and specify the worksheet by name
sheet_url = 'https://docs.google.com/spreadsheets/d/18qa612LxTadmS6QgUhGPkIEkUgqqKYxSFrKgwlPVVd8/edit#gid=0'
worksheet_name = 'Sheet1'
worksheet = gc.open_by_url(sheet_url).worksheet(worksheet_name)

# Open the webcam for QR code scanning
cap = cv2.VideoCapture(0)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    ret, frame = cap.read()
    detector = cv2.QRCodeDetector()
    data, _ = detector.detectAndDecode(frame)
    
    if data:
        try:
            worksheet.append_row([data])
            response = {'message': 'Data sent to Sheets successfully.'}
        except Exception as e:
            response = {'error': f'Error sending data to Sheets: {str(e)}'}
    else:
        response = {'message': 'No QR code data found.'}
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
