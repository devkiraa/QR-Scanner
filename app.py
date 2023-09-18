import cv2
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Define the scope and credentials for accessing Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('your-service-account.json', scope)
gc = gspread.authorize(credentials)

# Open the Google Sheet by its URL and specify the worksheet by name
sheet_url = 'https://docs.google.com/spreadsheets/d/1k1jeAG_hsUA8sni6yu7fYM_fXaPDpRrm4ynWElqEn1A/edit?usp=sharing'  # Replace with your Google Sheet URL
worksheet_name = 'Sheet1'  # Replace with your actual sheet name
worksheet = gc.open_by_url(sheet_url).worksheet(worksheet_name)

# Open the webcam for QR code scanning
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    # Initialize the QR code detector
    detector = cv2.QRCodeDetector()
    
    # Detect QR codes in the frame
    data, vertices = detector.detectAndDecode(frame)
    
    if data:
        # Data is the QR code content
        print("QR Code Data:", data)
        
        try:
            # Send the QR code data to Google Sheets
            worksheet.append_row([data])
            print("Data sent to Sheets successfully.")
        except Exception as e:
            print("Error sending data to Sheets:", str(e))
    
    cv2.imshow('QR Code Scanner', frame)
    
    # Press 'q' to exit the app
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
