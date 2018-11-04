$(document).ready(function(){
    $("#Dark").fadeIn(500);
	$("#Dialog").slideDown(500);
	$("#Dark,#Dialog_close").click(function(){
		$("#Dark").fadeOut(500);
		$("#Dialog").slideUp(500);
		setTimeout(function () {
			location.href = $("#nexturl").text();
        }, 400)
	});
	setTimeout('$("#Dark,#Dialog_close").click()', 3000);
});