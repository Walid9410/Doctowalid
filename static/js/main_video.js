let videoEmit = document.querySelector('#localVideo');

const mediaStreamConstraints = {
  video: true,
  audio: true,
};

function gotLocalMediaStream(mediaStream) {
  videoEmit.srcObject = mediaStream;
  videoEmit.play;
}

function handleLocalMediaStreamError(error) {
  //console.log("Error getUserMedia()");
  //console.log("Error getUserMedia(): ${error.toString()}");
  console.error('Error: ', error);
}

document.querySelector('#start').addEventListener('click', function (e) {

  navigator.mediaDevices.getUserMedia(mediaStreamConstraints)
    .then(gotLocalMediaStream).catch(handleLocalMediaStreamError);

}
);
