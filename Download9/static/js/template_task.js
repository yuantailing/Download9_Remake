$(document).ready(function(){
	$.gettaskstate = function(){
		$(".task_line_0, .task_line_1").each(function(){
			if ($(this).attr("id") == "task_line_head") {
				return ;
			}
			thisnum = $(this).find(".task_id:first").html();
			thisid = '#task_line_' + thisnum;
			var post_data = {
				"task_name": $(thisid + ' .task_name:first').html(),
				"gid": $(thisid + ' .task_gid:first').html(),
				"workid": thisnum,
			};
			$.ajax({url: "/get_task_state",
					data: post_data,
					type: "POST",
					success: function(data) {
						data = JSON.parse(data);
						if (data['result'] == 'success') {
							thisid = '#task_line_' + data['workid'];
							$(thisid + ' .task_state').html(data['state']);
							$(thisid + ' .task_size').html(data['size']);
							$(thisid + ' .task_velocity').html(data['velocity']);
							$(thisid + ' .task_filename').html(data['filename']);
						}
						else {
							window.alert(data['result'])
						}
					}
			});
		});
	};
	setInterval($.gettaskstate, 1000);
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
		$atleastone = false;
		$("input[type='checkbox']").each(function(){
			if ($(this).attr("id") != "task_tick_a") {
				if (!($(this).is(":checked"))) {
					$allchecked = false;
					$atleastone = true;
				}
			}
		});
		if ($atleastone) {
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
		}
	});
});