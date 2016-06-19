function draw_line_graph(chart) {
    var ctx = $("#chart").get(0).getContext("2d");
    var output = $(document.getElementById('json'));

    if(chart['value_x'].length == 0){
        output.text("Cannot get data. Please check the worker ID.");
    }else{
        output.text("Get data.");
    }
    var dataset = {
        label: chart['label'],
        fillColor: "rgba(220,220,220,0.2)",
        strokeColor: "rgba(220,220,220,1)",
        pointColor: "rgba(220,220,220,1)",
        pointStrokeColor: "#fff",
        pointHighlightFill: "#fff",
        pointHighlightStroke: "rgba(220,220,220,1)",
        data: chart['value_y']
    };
    var data = {
        labels: chart['value_x'],
        datasets: [dataset,]
    };
    var lineChart = new Chart(ctx, {
        type: "line",
        data: data,
    });
    console.log("draw:", chart['label']);
}

$(function() {
    $('#get').submit(function(event) {
        var post_data = JSON.stringify({
            workerId: document.forms.get.workerId.value,
            category: document.forms.get.category.value
        });
        console.log("post:", post_data);

        event.preventDefault();
        $.ajax({
            url: "_get_personal_data",
            type: 'post',
            data: post_data,
            contentType: 'application/json',
            success: function(result) {
                draw_line_graph(JSON.parse(result['data']));
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                console.log(textStatus);
            }
        });
    });
});
