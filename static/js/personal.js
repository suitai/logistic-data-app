function draw_line_graph(chart, ctx, output) {

    if(chart['value_x'].length == 0){
        output.text("Cannot get data. Please check the worker ID.");
        return;
    }else{
        output.text("Get data.");
    }

    var colors = {
        "カロリー": {borderColor: "rgba(255,204,51,0.6)",
                     backgroundColor: "rgba(255,204,102,0.4)"},
        "歩数": {borderColor: "rgba(0,102,255,0.6)",
                 backgroundColor: "rgba(0,153,255,0.4)"},
        "脈拍": {borderColor: "rgba(255,0,102,0.6)",
                 backgroundColor: "rgba(255,51,102,0.4)"},
    };

    var dataset = {
        label: chart['label'],
        data: chart['value_y']
    };
    $.extend(dataset, colors[chart['label']]);
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
    var output = $(document.getElementById('json'));

    for (var i = 0; i < charts.length; i++) {
        var canvas = $('<canvas>').attr("id", "chart" + String(i))
        $('#canvas_content').append(canvas)
        var ctx = $("#chart" + String(i)).get(0).getContext("2d")
        draw_line_graph(charts[i], ctx, output);
    }
}


$(function() {
    $("#loading").hide();

    $('#get').submit(function(event) {
        var post_data = JSON.stringify({
            workerId: document.forms.get.workerId.value,
        });
        console.log("post:", post_data);

        $("#loading").show();

        event.preventDefault();
        $.ajax({
            url: "_get_personal_data",
            type: 'post',
            data: post_data,
            contentType: 'application/json',
            success: function(result) {
                console.log("get:", result['data']);
                $("#loading").hide();
                draw_line_graphs(JSON.parse(result['data']));
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                console.log(textStatus);
            }
        });
    });
});
