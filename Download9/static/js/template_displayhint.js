$(document).ready(function(){
	$.loadhint = function(data) {
		data = JSON.parse(data);
		if (data['nexturl'] != undefined) {
			$('#nexturl').html(data['nexturl']);
		}
		else {
			$('#nexturl').html('');
		}
		$('#Dialog_Content h1').html(data['title']);
		var str = '';
		for (var i = 0; i < data['context'].length; i++)
			str = str + data['context'][i] + '<br>';
		$('#Dialog_Content p').html(str);
	};

	$.displayhint = function() {
	    $("#Dark").fadeIn(500);
		$("#Dialog").slideDown(500);
		$("#Dark,#Dialog_close").click(function(){
			clearTimeout(ref);
			$("#Dark").fadeOut(500);
			$("#Dialog").slideUp(500);
			ref2 = window.setTimeout(function () {
				clearTimeout(ref2);
				if ($("#hint_form").length > 0) {
					$("#hint_form").submit();
				}
				else if ($("#nexturl").text() != '') {
            	   	location.href = $("#nexturl").text();
        	    }
				else if ($("#close").text() != '') {
					window.close();
				}
   		    }, 400)
		});
		ref = window.setTimeout('$("#Dark,#Dialog_close").click()', 5000);
	};
});