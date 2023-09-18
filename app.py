from flask import Flask, request, render_template
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Define the scope and credentials for accessing Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('your-service-account.json', scope)
gc = gspread.authorize(credentials)

# Open the Google Sheet by its URL and specify the worksheet by name
sheet_url = 'https://docs.google.com/spreadsheets/d/18qa612LxTadmS6QgUhGPkIEkUgqqKYxSFrKgwlPVVd8/edit?usp=sharing'  # Replace with your Google Sheet URL
worksheet_name = 'Sheet1'  # Replace with your actual sheet name
worksheet = gc.open_by_url(sheet_url).worksheet(worksheet_name)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    try:
        data = request.json.get('qrImageData', '')

        # Send the QR code data to Google Sheets
        worksheet.append_row([data])
        
        return 'Data sent to Sheets successfully.', 200
    except Exception as e:
        return f'Error sending data to Sheets: {str(e)}', 500

if __name__ == '__main__':
    app.run(debug=True)
