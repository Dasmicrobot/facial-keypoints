'use strict';

(function () {

    var constraints = {
        video: true,
        audio: false
    };

    var video = null;
    var imagecapture = null;
    var videooverlay = null;
    var startplayback = null;
    var stopplayback = null;
    var prediction_interval = 1000;

    function startup() {
        video = document.getElementById('video');
        imagecapture = document.getElementById('imagecapture');
        videooverlay = document.getElementById('videooverlay');
        startplayback = document.getElementById('startplayback');
        stopplayback = document.getElementById('stopplayback');

        video.addEventListener('canplay', function () {
            // init some code here
        }, false);
        startplayback.addEventListener('click', function (ev) {
            start();
            ev.preventDefault();
        }, false);
        stopplayback.addEventListener('click', function (ev) {
            stop();
            ev.preventDefault();
        }, false);
        stopplayback.hidden = true;
    }

    function clearphoto() {
        imagecapture.getContext('2d')
            .clearRect(0, 0, imagecapture.width, imagecapture.height);
    }

    function clearoverlay() {
        videooverlay.getContext('2d')
            .clearRect(0, 0, videooverlay.width, videooverlay.height);
    }

    function takepicture() {
        imagecapture.getContext('2d')
            .drawImage(video, 0, 0, imagecapture.width, imagecapture.height);
        imagecapture.toBlob(function (blob) {
            var formdata = new FormData();
            formdata.append("image", blob);
            $.ajax({
                url: "/predict",
                type: "POST",
                data: formdata,
                processData: false,
                contentType: false,
            }).done(function (response) {
                clearoverlay();
                var context = videooverlay.getContext('2d');
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
    }

    var interval;
    function start() {
        stop();
        navigator.mediaDevices.getUserMedia(constraints)
            .then(function (stream) {
                video.srcObject = stream;
                video.play();
                interval = setInterval(takepicture.bind(this), prediction_interval);

                startplayback.hidden = true;
                stopplayback.hidden = false;
            })
            .catch(function (error) {
                console.log('getUserMedia error: ', error);
            });
        clearphoto();
        clearoverlay();
    }

    function stop() {
        var src = video.srcObject;
        if (src && src.active) {
            src.getTracks().forEach(function (track) {
                track.stop();
            })
        }
        if (interval) {
            clearInterval(interval);
        }

        startplayback.hidden = false;
        stopplayback.hidden = true;
    }

    window.addEventListener('load', startup, false);

}());