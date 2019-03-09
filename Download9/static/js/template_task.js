$(document).ready(function(){
	$.gettaskstate = function(){
		var post_data_all = [];
		var overall = 0;
		$(".task_line_0, .task_line_1").each(function(){
			if ($(this).attr("id") === "task_line_head") {
				return ;
			}
			var thisnum = $(this).find(".task_id:first").html();
			var thisid = '#task_line_' + thisnum;
			var post_data = {
				"task_name": $(thisid + ' .task_name:first').html(),
				"gid": $(thisid + ' .task_gid:first').html(),
				"workid": thisnum,
			};
			post_data_all.push(post_data);
		});
		var pd = {'data' : JSON.stringify(post_data_all), 'from' : window.location.pathname};
		$.ajax({
			url: "/get_task_state",
			data: pd,
			type: "POST",
			success: function(data) {
				var raw_data = data;
				data = JSON.parse(data);
				if (data['result'] === 'success') {
					if (data['refresh'] === '1') {
						window.location.reload();
					}
					else {
						for (var i = 0; i < data['data'].length; i++) {
							var thisid = '#task_line_' + data['data'][i]['workid'];
							$(thisid + ' .task_state').html(data['data'][i]['state']);
							$(thisid + ' .task_size').html(data['data'][i]['size']);
							$(thisid + ' .task_velocity').html(data['data'][i]['velocity']);
							$(thisid + ' .task_timeremain').html(data['data'][i]['timeremain']);
							$(thisid + ' .task_filename').html(data['data'][i]['filename']);
							$(thisid + ' .task_process').html(data['data'][i]['process']);
							$(thisid + ' .task_attr').html(data['data'][i]['attr']);
						}
						$('#download_number').html(parseInt(data['download_cnt']) + '个任务正在下载');
						$('#task_number').html("任务数量：" + parseInt(data['overall_cnt']) + "/" + $('#task_number_limit').html());
						$('#memory_used').html("已用空间：" + parseInt(data['memory_used']) + "/" + $('#memory_used_limit').html() + "MB");
					}
				}
				else {
					$.loadhint(raw_data);
					$.displayhint();
				}
			}
		});
	};
	$.operation = function(str) {
		var post_data = '[';
		$fir = false;
		$(".task_line_0, .task_line_1").each(function(){
			if ($(this).attr("id") == "task_line_head") {
				return ;
			}
			$thisnum = $(this).find(".task_id:first").html();
			if ($('#task_tick_' + $thisnum).is(":checked")) {
				$thisid = '#task_line_' + $thisnum;
				if ($fir)
					post_data += ',';
				post_data += '{"task_name": "' + $($thisid + ' .task_name:first').html() + '" , "gid": "' + $($thisid + ' .task_gid:first').html() + '" }';
				$fir = true;
			}
		});
		if ($fir) {
			post_data = post_data + ']';
			$.ajax({
				url: "/" + str,
				data: {jsonData: post_data},
				type: "POST",
				sync: false,
				success: function(data) {
					$.loadhint(data);
	                $.displayhint();
				}
			});
		}
	};
	$.gettaskstate();
	setInterval($.gettaskstate, 1000);
	$("#operation_delete").click(function(){
		if (confirm("你确定要删除吗？"))
			$.operation("delete_task")
	});
	$("#operation_pause").click(function(){$.operation("pause_task")});
	$("#operation_continue").click(function(){$.operation("continue_task")});
	$("#operation_switch").click(function(){$.operation("switch_task")});
	$("#operation_download").click(function(){
		$(".task_line_0, .task_line_1").each(function(){
			if ($(this).attr("id") == "task_line_head") {
				return ;
			}
			$thisnum = $(this).find(".task_id:first").html();
			if ($('#task_tick_' + $thisnum).is(":checked")) {
				$thisid = '#task_line_' + $thisnum;
				$openurl = '/download_task/task_name=' + $($thisid + ' .task_name:first').html() + '/gid=' + $($thisid + ' .task_gid:first').html();
				window.open($openurl);
			}
		});
	});
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
	$("input[type='checkbox']").click(function(){
		$allchecked = true;
		$atleastone = false;
		$("input[type='checkbox']").each(function(){
			if ($(this).attr("id") != "task_tick_a") {
				$atleastone = true;
				if (!($(this).is(":checked"))) {
					$allchecked = false;
				}
			}
		});
		if ($atleastone) {
			if ($allchecked) {
				$("#task_tick_a").attr('checked', 'true');
			}
			else {
				$("#task_tick_a").removeAttr('checked');
			}
		}
	});
});