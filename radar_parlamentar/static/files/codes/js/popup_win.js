$(document).ready(function(){

	if(checkCookie() == true){
		setTimeout(openPopup, 2000);
	}
	$("#modal-open-button").click(function(e) {
		openPopup();
	});
	$("#modal-close-button").click(function(e){
		closePopup();
	});
	$("#overlay-bg").click(function(e){
		closePopup();
	});
	$(window).resize(function(){
		updatePopup();
	});
});

function openPopup(){
	$("#modal-open-button").prop("disabled", true);
	$("#popup-content").fadeIn();
	$("#overlay-bg").fadeIn();
	updatePopup();
}

function closePopup(){
	$("#modal-open-button").prop("disabled", false);
	$("#modal-open-button").fadeIn();
	$("#popup-content").fadeOut();
	$("#overlay-bg").fadeOut();
}

function updatePopup(){
	var $popupContent = $("#popup-content");
	var top = ($(window).height()-$popupContent.outerHeight()) / 2; // Center Vertical
	var left = ($(window).width()-$popupContent.outerWidth()) / 2; // Center Horizontal
	$popupContent.css({
		'top':top,
		'left':left
	});
}

function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires="+d.toUTCString();
    document.cookie = cname + "=" + cvalue + "; " + expires;
}

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1);
        if (c.indexOf(name) == 0) return c.substring(name.length, c.length);
    }
    return "";
}

function checkCookie() {
	var check = false;
    var user = getCookie("username");
    if (user != "") {
        check = false;
    } else {
        user = "user";
        if (user != "" && user != null) {
            setCookie("username", user, 365);
        }
        check = true;
    }
    return check;
}