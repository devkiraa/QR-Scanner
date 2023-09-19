const video = document.getElementById('qr-video');
const scannedDataElement = document.getElementById('scanned-data');
const captureButton = document.getElementById('capture-button');
const sendButton = document.getElementById('send-button');
const sendStatus = document.getElementById('send-status');
const capturedImageCanvas = document.getElementById('captured-image');
const capturedImageContext = capturedImageCanvas.getContext('2d');
let isCaptured = false;

navigator.mediaDevices
    .getUserMedia({ video: { facingMode: 'environment' } })
    .then(function (stream) {
        video.srcObject = stream;
        video.play();
    })
    .catch(function (error) {
        console.error('Error accessing the webcam:', error);
    });

captureButton.addEventListener('click', captureImage);

function captureImage() {
    if (!isCaptured) {
        isCaptured = true;
        captureButton.textContent = 'Recapture';
        sendButton.style.display = 'none';
        sendStatus.textContent = '';

        capturedImageCanvas.width = video.videoWidth;
        capturedImageCanvas.height = video.videoHeight;
        capturedImageContext.drawImage(video, 0, 0, capturedImageCanvas.width, capturedImageCanvas.height);
        capturedImageContext.filter = 'grayscale(100%)';
        capturedImageContext.drawImage(video, 0, 0, capturedImageCanvas.width, capturedImageCanvas.height);

        const imageDataURL = capturedImageCanvas.toDataURL('image/jpeg');
        const image = new Image();
        image.src = imageDataURL;

        image.onload = function () {
            const qrCode = jsQR(
                capturedImageContext.getImageData(0, 0, capturedImageCanvas.width, capturedImageCanvas.height).data,
                capturedImageCanvas.width,
                capturedImageCanvas.height
            );

            if (qrCode) {
                const scannedData = qrCode.data;
                scannedDataElement.textContent = scannedData;
                sendButton.style.display = 'block';
            } else {
                alert('No QR code found in the captured image.');
            }
        };
    } else {
        isCaptured = false;
        captureButton.textContent = 'Capture';
        sendButton.style.display = 'none';
        scannedDataElement.textContent = '';
        sendStatus.textContent = '';
    }
}

sendButton.addEventListener('click', sendDataToServer);

function sendDataToServer() {
    if (isCaptured) {
        const scannedData = scannedDataElement.textContent;

        if (scannedData) {
            fetch('/scan', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ qrData: scannedData }),
            })
                .then(response => response.json())
                .then(result => {
                    sendStatus.textContent = result.message;
                })
                .catch(error => {
                    console.error('Error sending data to server:', error);
                    sendStatus.textContent = 'Error sending data to server.';
                });
        } else {
            alert('No data to send.');
        }
    } else {
        alert('Please capture an image first.');
    }
}
