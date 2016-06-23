function draw_line_graph(chart, ctx, output) {

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

function draw_line_graphs(charts) {
    var ctx = [$("#chart1").get(0).getContext("2d"),
               $("#chart2").get(0).getContext("2d"),
               $("#chart3").get(0).getContext("2d")]
    var output = $(document.getElementById('json'));

    for (var i = 0; i < ctx.length; i++) {
        draw_line_graph(charts[i], ctx[i], output);
    }
}

$(function() {
    $('#get').submit(function(event) {
        var post_data = JSON.stringify({
            workerId: document.forms.get.workerId.value,
        });
        console.log("post:", post_data);

        event.preventDefault();
        $.ajax({
            url: "_get_personal_data",
            type: 'post',
            data: post_data,
            contentType: 'application/json',
            success: function(result) {
                console.log("get:", result['data']);
                draw_line_graphs(JSON.parse(result['data']));
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                console.log(textStatus);
            }
        });
    });
});
