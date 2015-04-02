$(document).ready(function(){
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