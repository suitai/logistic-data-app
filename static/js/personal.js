function draw_line_graph(chart, ctx, color, output) {

    if(chart['value_x'].length == 0){
        output.text("Cannot get data. Please check the worker ID.");
    }else{
        output.text("Get data.");
    }
    var dataset = {
        label: chart['label'],
        data: chart['value_y']
    };
    $.extend(dataset, color);
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
    var colors = [
        {borderColor: "rgba(255,204,51,0.6)",
         backgroundColor: "rgba(255,204,102,0.4)"},
        {borderColor: "rgba(0,102,255,0.6)",
         backgroundColor: "rgba(0,153,255,0.4)"},
        {borderColor: "rgba(255,0,102,0.6)",
         backgroundColor: "rgba(255,51,102,0.4)"},
    ]

    for (var i = 0; i < ctx.length; i++) {
        draw_line_graph(charts[i], ctx[i], colors[i], output);
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
