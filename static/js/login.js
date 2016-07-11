$(function() {
    $("#login_btn").on('click', function(event) {
        var workerId = $(":text[name='workerId']").val();
        console.log(workerId);
        $.ajax({
            url: "login",
            type: 'post',
            data: {"username": workerId},
            dataType: "html",
        });
    });
});
