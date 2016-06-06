

function save(e) {
	window.localStorage.setItem('filter', document.getElementById('fromTxt').value);
	window.localStorage.setItem('redirect', document.getElementById('toTxt').value);
	
	chrome.runtime.sendMessage({cmd: "reload"}, function(response) {  console.log(response); });
}

document.addEventListener('DOMContentLoaded', function () {
	document.getElementById('fromTxt').value = window.localStorage.getItem("filter");
	document.getElementById('toTxt').value = window.localStorage.getItem("redirect");
	document.getElementById('save').addEventListener('click', save);
});
