'use strict';

(function () {

    var constraints = {
        video: true,
        audio: false
    };

    var video = null
    var canvas = null
    var takephoto = null
    var startplayback = null
    var stopplayback = null
    // |streaming| indicates whether or not we're currently streaming
    // video from the camera. Obviously, we start at false.
    var streaming = false
    var width = 320;    // We will scale the photo width to this
    var height = 0; // This will be computed based on the input stream

    function startup() {
        video = document.getElementById('video');
        canvas = document.getElementById('canvas');
        takephoto = document.getElementById('takephoto');
        startplayback = document.getElementById('startplayback');
        stopplayback = document.getElementById('stopplayback');

        video.addEventListener('canplay', setWidthAndHeigth, false);
        takephoto.addEventListener('click', function (ev) {
            takepicture();
            ev.preventDefault();
        }, false);
        startplayback.addEventListener('click', function (ev) {
            start();
            ev.preventDefault();
        }, false);
        stopplayback.addEventListener('click', function (ev) {
            stop();
            ev.preventDefault();
        }, false);
    }

    function setWidthAndHeigth() {
        if (!streaming) {
            height = video.videoHeight / (video.videoWidth / width);

            // Firefox currently has a bug where the height can't be read from
            // the video, so we will make assumptions if this happens.

            if (isNaN(height)) {
                height = width / (4 / 3);
            }

            video.setAttribute('width', width);
            video.setAttribute('height', height);
            canvas.setAttribute('width', width);
            canvas.setAttribute('height', height);
            streaming = true;
        }
    }

    function clearphoto() {
        var context = canvas.getContext('2d');
        context.clearRect(0, 0, canvas.width, canvas.height);
    }

    function takepicture() {
        var context = canvas.getContext('2d');
        if (width && height) {
            canvas.width = width;
            canvas.height = height;
            context.drawImage(video, 0, 0, width, height);
            canvas.toBlob(function (blob) {
                var formdata = new FormData();
                formdata.append("image", blob);
                $.ajax({
                    url: "/predict",
                    type: "POST",
                    data: formdata,
                    processData: false,
                    contentType: false,
                }).done(function (response) {
                    var faces = (response && response.data) || [];
                    faces.forEach(function (face) {
                        context.beginPath();
                        context.lineWidth = "2";
                        context.strokeStyle = "red";
                        context.rect(face.x, face.y, face.w, face.h);
                        context.stroke();
                    })
                });
            })
        } else {
            clearphoto();
        }
    }

    function start() {
        stop();
        navigator.mediaDevices.getUserMedia(constraints)
            .then(function (stream) {
                video.srcObject = stream;
                video.play();
            })
            .catch(function (error) {
                console.log('getUserMedia error: ', error);
            });
        clearphoto();
    }

    function stop() {
        var src = video.srcObject
        if (src && src.active) {
            src.getTracks().forEach(function (track) {
                track.stop();
            })
        }
    }

    window.addEventListener('load', startup, false);

}());