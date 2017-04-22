function makeHttpObject() {
    try {return new XMLHttpRequest();}
    catch (error) {}
    try {return new ActiveXObject("Msxml2.XMLHTTP");}
    catch (error) {}
    try {return new ActiveXObject("Microsoft.XMLHTTP");}
    catch (error) {}
    throw new Error("Could not create HTTP request object.");
}
var request = makeHttpObject();
var getSensors = makeHttpObject();
var linkCheckTimer = 5000;
var heartbeatTimer = 1000;
var video = false;
var framerate = 0;
var link = true;
var videoimg = '<img src="/video_feed" alt="Connecting to Live Video">'
var frameimg = '<img id="sframe" src="/single_frame.jpg" alt="Connecting to Live Video">'
var framesrc = '/single_frame.jpg'
var linkCheck = setTimeout(linkLost, linkCheckTimer);
setInterval(heartbeat, heartbeatTimer);
getSensors.onreadystatechange = updateStatus;
setTimeout(checkVideo, 500);
function linkLost() {
    link = false;
}
function checkVideo() {
	if (video) {
		if (framerate > 0) {
			document.getElementById("video").innerHTML = frameimg;
			setInterval(reloadFrame, framerate);
		} else {
			document.getElementById("video").innerHTML = videoimg;
		}
	}
}
function reloadFrame() {
	document.getElementById("sframe").src = framesrc + "?" + new Date().getTime();
}
function heartbeat() {
    var heartbeat_url = "/heartbeat";
    getSensors.open("GET", heartbeat_url, true);
    getSensors.send(null);
}
function updateStatus(e) {
	if (getSensors.readyState == 4 && getSensors.status == 200) {
        var response = JSON.parse(getSensors.responseText);
        video = response.v;
        framerate = response.f;
        clearTimeout(linkCheck);
		linkCheck = setTimeout(linkLost, linkCheckTimer);
		if (!link) {
			location.reload();
		}
		link = true;
	}
}
heartbeat();
