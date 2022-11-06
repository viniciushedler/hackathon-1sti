// This file contains the http requests 
// used to send the images to the server

function upload(){
    var canvas = document.getElementById("canvas");

    canvas.toBlob(function(blob) {
        // create a form with the image
        var formData = new FormData();
        formData.append("image", blob, "image.png");

        console.log(formData);

        var oReq = new XMLHttpRequest();
        oReq.open("POST", "/upload_webcam_file", true);

        oReq.onload = function(oEvent) {
            if (oReq.status == 200) {
                console.log("Uploaded");
            } else {
                console.log("Error " + oReq.status + " occurred uploading your file.");
            }
        }
        console.log("Sending file...");
        oReq.send(formData);
    });
}