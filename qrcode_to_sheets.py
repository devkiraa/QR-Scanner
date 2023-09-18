import cv2
from pyzbar.pyzbar import decode
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Set up Google Sheets API authentication
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("your-credentials.json", scope)
client = gspread.authorize(creds)

# Open the Google Sheet by its title
sheet = client.open("Your Google Sheet Title").sheet1

# Initialize the webcam
cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()

    # Decode QR codes from the frame
    decoded_objects = decode(frame)

    for obj in decoded_objects:
        data = obj.data.decode("utf-8")

        # Append the data to the Google Sheet
        sheet.append_row([data])

    cv2.imshow("QR Code Scanner", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
