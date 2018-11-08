$(document).ready(function(){
    $('#submit_button').click(function(){
        var post_data = {"task_name": $('#task_name').val(), "task_link": $('#task_link').val(), };
        $.ajax({url: "/new_url_task",
                data: post_data,
                async: false,
                type: "POST",
                success: function(data) {
                    data = JSON.parse(data);
                    window.alert(data["result"]);
                    if (data["result"] == "success") {
                        window.location = "/index";
                    }
                }
        });
    });
});