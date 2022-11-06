// This file is for the webcam module of the app


// gets the user video input and displays it on the page
navigator.mediaDevices.getUserMedia({video: true})
.then(function (mediaStream) {
    const video = document.getElementById('webcam-input');
    video.srcObject = mediaStream;
    video.play();
})
.catch(function (err) {
    console.log('Webcam permission denied');
})

// adds an event listener to the button to take a picture
capture_btn = document.getElementById("capture");

capture_btn.addEventListener('click', function (e) {
    var canvas = document.querySelector("#canvas");  
    const video = document.getElementById('webcam-input');
    canvas.height = video.videoHeight;
    canvas.width = video.videoWidth;
    var context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // sends the image to the server
    upload();
});