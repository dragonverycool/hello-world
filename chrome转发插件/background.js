function updateEnableIcon() {
  chrome.browserAction.setIcon({path:"logo.png"});
}

function updateDisenableIcon() {
  chrome.browserAction.setIcon({path:"ayg_disenable.png"});
}
 
 var listeners = {};
 var reg=new RegExp("http://.+?/","i");
chrome.browserAction.onClicked.addListener(function(tab) {
    if (listeners[tab.id]) {
		console.log("remove listener:" + tab.id );
        // Callback was previously set. Remove the listeners.
        chrome.webRequest.onBeforeRequest.removeListener(listeners[tab.id]);
        delete listeners[tab.id];
		updateDisenableIcon();	
		
    } else {

		console.log("add listener:" + tab.id);
		var filterURL = window.localStorage.getItem("filter");

        listeners[tab.id] = function(details) {
			console.log("Cat intercepted: " + details.url);
			var toURL = window.localStorage.getItem("redirect");
			if(toURL == null || toURL == "undefined" || toURL.trim() == ''){				
				toURL = details.url.replace(reg,"http://localhost:8080/");
			}else{
				toURL = details.url.replace(new RegExp(filterURL,"i"), toURL+"/");
			}
			console.log("redirect URL: " + toURL);
			return {redirectUrl: toURL};
        };

		
		if(filterURL == null || filterURL == "undefined" || filterURL == ''){
			filterURL = "http://dragon/*";
		}
        chrome.webRequest.onBeforeRequest.addListener(listeners[tab.id], {
            urls: [filterURL],
            types: ['main_frame', 'sub_frame', 'xmlhttprequest'],
            tabId: tab.id
        }, ['blocking']);

        updateEnableIcon();
    }
});

// Remove obsolete listener when the tab is closed.
chrome.tabs.onRemoved.addListener(function(tabId) {
    if (listeners[tabId]) {
		console.log("tab closed, remove listener");
        chrome.webRequest.onBeforeRequest.removeListener(listeners[tabId]);
        delete listeners[tabId];
    }
});

 chrome.tabs.onUpdated.addListener(function(tabId) {
	if (listeners[tabId]) {
		updateEnableIcon();
	}else{
		updateDisenableIcon();
	}
 });


 chrome.runtime.onMessage.addListener(  function(request, sender, sendResponse) { 
	console.log("Receive message:" + request.cmd);
	if (request.cmd== "reload"){
	  for(var each in listeners){
		console.log("remove listener: " + each);
		chrome.webRequest.onBeforeRequest.removeListener(listeners[each]);

		var filter = window.localStorage.getItem("filter");
		listeners[each] = function(details) {
			console.log("Cat intercepted: " + details.url);
            var toURL = window.localStorage.getItem("redirect");
			console.log("localStorage to: " + toURL);
			if(toURL == null || toURL == "undefined" || toURL.trim() == ''){				
				toURL = details.url.replace(reg,"http://localhost:8080/");
			}else{				
				console.log("filter: " + filter);
				console.log("toURL: " + toURL);
				toURL = details.url.replace(new RegExp(filter,"i"), toURL+"/");
			}
			console.log("redirect URL: " + toURL);
			return {redirectUrl: toURL};
        };
		
		console.log("add listener: " + filter);
		chrome.webRequest.onBeforeRequest.addListener(listeners[each], {
            urls: [filter],
            types: ['main_frame', 'sub_frame', 'xmlhttprequest'],
            tabId: parseInt(each)
        }, ['blocking']);

		sendResponse( "OK, reload listener is complated!"); 
	  }
	}
  });