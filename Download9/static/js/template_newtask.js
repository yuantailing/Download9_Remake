$(document).ready(function(){
    $.getoverallstate = function(){
        $.ajax({
            url: "/get_overall_state",
            type: "POST",
            success: function(data) {
                var raw_data = data;
				data = JSON.parse(data);
				if (data['result'] === 'success') {
					$('#task_number').html("任务数量：" + parseInt(data['overall_cnt']) + "/" + $('#task_number_limit').html());
					$('#memory_used').html("已用空间：" + parseInt(data['memory_used']) + "/" + $('#memory_used_limit').html() + "MB");
				}
				else {
				    $.loadhint(raw_data);
				    $.displayhint();
                }
            }
        })
    };
    setInterval($.getoverallstate, 1000);
    $.getoverallstate();
    $('#submit_button').click(function(){
        if (window.location.href.includes("newbt")) {
            var post_data = new FormData();
            post_data.append("csrfmiddlewaretoken", $('#csrfmiddlewaretoken').val());
            post_data.append("task_name", $('#task_name').val());
            post_data.append("task_link", $(':file')[0].files[0]);
            $.ajax({url: "/new_bt_task",
                data: post_data,
                cache: false,
                processData: false,
                contentType: false,
                async: true,
                type: "POST",
                success: function(data) {
                    $.loadhint(data);
                    $.displayhint();
                }
            });
        }
        else if (window.location.href.includes("newmeta")) {
            var post_data = {"task_name": $('#task_name').val(), "task_link": $('#task_link').val(), };
            $.ajax({url: "/new_meta_task",
                data: post_data,
                async: true,
                type: "POST",
                success: function(data) {
                    $.loadhint(data);
                    $.displayhint();
                }
            });
        }
        else {
            var post_data = {"task_name": $('#task_name').val(), "task_link": $('#task_link').val(), };
            $.ajax({url: "/new_url_task",
                data: post_data,
                async: true,
                type: "POST",
                success: function(data) {
                    $.loadhint(data);
                    $.displayhint();
                }
            });
        }
    });
});