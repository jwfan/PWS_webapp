var audioCtx;
var recorder;

$(document).ready(function() {
  var analyzer = new Analyzer();
  var isRecording="0";

  init();

  $("#start-record").click( function() {
  	if(isRecording==="0"){
  	  if ($('#is-authenticated').length <= 0) {
        // unlogged in
        //alert("If you want to save your image and recording, please login.");
      }
  	  $("#record-states").html("Recording now...");	
  	  $("#ongoing-record").css("color","#b4d5c4");
  	  isRecording="1";
      analyzer && analyzer.startRecording();
      recorder && recorder.record();
      drawpicture(analyzer);
  	}
  });

  $("#stop-record").click( function() {
  	if(isRecording==="1"){
  	  $("#record-states").html("Record ended. Click the button below to start recording again.");	
  	  $("#ongoing-record").css("color","#a8505f");
  	  isRecording="0";
      analyzer.stopRecording();
      recorder && recorder.stop();
      createDownloadLink();
      recorder.clear();
      stopdrawpicture();

  	}
    // get audio data
    // console.log(analyzer.timeData);
    // console.log(analyzer.freqData);
    // console.log(analyzer.convTimeData);
    // console.log(analyzer.convFreqData);

  });

  function createDownloadLink() {
      recorder && recorder.exportWAV(function(blob) {
      var url = URL.createObjectURL(blob);
      var li = document.createElement('li');
      var au = document.createElement('audio');
      var hf = document.createElement('a');

      au.controls = true;
      au.src = url;
      hf.href = url;
      hf.download = new Date().toISOString() + '.wav';
      hf.innerHTML = hf.download;
      li.appendChild(au);
      li.appendChild(hf);
      $("#recording-list").append(li);
    });
  }

});

function startUserMedia(stream) {
    var input = audioCtx.createMediaStreamSource(stream);
    console.log('Media stream created.');

    recorder = new Recorder(input);
    console.log('Recorder initialised.');
  }

function init() {
    try {
      // webkit shim
      window.AudioContext = window.AudioContext || window.webkitAudioContext;
      navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia;
      window.URL = window.URL || window.webkitURL;

      audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      console.log('Audio context set up.');
      console.log('navigator.getUserMedia ' + (navigator.getUserMedia ? 'available.' : 'not present!'));
    } catch (e) {
      alert('No web audio support in this browser!');
    }

    navigator.getUserMedia({audio: true}, startUserMedia, function(e) {
      console.log('No live audio input: ' + e);
    });
  }

