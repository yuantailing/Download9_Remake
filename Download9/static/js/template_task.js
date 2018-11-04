$(document).ready(function(){
	$("#task_tick_a").click(function(){
		if ($("#task_tick_a").is(":checked")) {
			$("input[type='checkbox']").each(function(){
				this.checked = true;
			});
		}
		else {
			$("input[type='checkbox']").each(function(){
				this.checked = false;
			});
		}
	});
	$("input").click(function(){
		$allchecked = true;
		$("input[type='checkbox']").each(function(){
			if ($(this).attr("id") != "task_tick_a") {
				if (!($(this).is(":checked"))) {
					$allchecked = false;
				}
			}
		});
		if ($allchecked) {
			$("#task_tick_a").each(function(){
				this.checked = true;
			});
		}
		else {
			$("#task_tick_a").each(function(){
				this.checked = false;
			});
		}
	});
});