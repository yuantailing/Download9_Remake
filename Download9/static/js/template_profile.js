$(document).ready(function(){
	$hovered = false;
	$("#info_user,#info").hover(function(){
		$hovered ^= true;
		if ($hovered) {
			$("#info_user").attr("class", "info_user_hover");
			$("#info").attr("class", "info_hover");
		}
		else {
			$("#info_user").attr("class", "info_user");
			$("#info").attr("class", "info");
		}
	});
});