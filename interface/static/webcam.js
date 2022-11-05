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
console.log(ocument.querySelector('#capture'));
document.querySelector('#capture').addEventListener('click', function (e) {
    var canvas = document.querySelector("#canvas");  
    canvas.height = video.videoHeight;
    canvas.width = video.videoWidth;
    var context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
});