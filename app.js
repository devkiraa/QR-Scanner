const video = document.getElementById('qr-video');
const scannedDataElement = document.getElementById('scanned-data');

// Use getUserMedia to access the webcam
navigator.mediaDevices
    .getUserMedia({ video: { facingMode: 'environment' } }) // Use the device's rear camera
    .then(function (stream) {
        video.srcObject = stream;
        video.play();
        scanQRCode();
    })
    .catch(function (error) {
        console.error('Error accessing the webcam:', error);
    });

function scanQRCode() {
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');

    // Continuously scan for QR codes
    function checkForQRCode() {
        if (video.readyState === video.HAVE_ENOUGH_DATA) {
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            context.drawImage(video, 0, 0, canvas.width, canvas.height);

            const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
            const code = jsQR(imageData.data, imageData.width, imageData.height);

            if (code) {
                scannedDataElement.textContent = code.data;
            }
        }
        requestAnimationFrame(checkForQRCode);
    }

    checkForQRCode();
}
