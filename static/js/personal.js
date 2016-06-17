function draw_line_graph(chart) {
    var ctx = $("#chart").get(0).getContext("2d");
    var dataset = {
        label: chart['label'],
        fillColor: "rgba(220,220,220,0.2)",
        strokeColor: "rgba(220,220,220,1)",
        pointColor: "rgba(220,220,220,1)",
        pointStrokeColor: "#fff",
        pointHighlightFill: "#fff",
        pointHighlightStroke: "rgba(220,220,220,1)",
        data: chart['data']
    };
    var data = {
        labels: chart['labels'],
        datasets: [dataset,]
    };
    var lineChart = new Chart(ctx, {
        type: "line",
        data: data,
    });
    console.log("draw:", chart['label'])
}

$(function() {
    $('#get').submit(function(event) {
        var worker_id =  document.forms.get.worker_id.value;
        var item =  document.forms.get.item.value;

        post_data = JSON.stringify({'workerId': worker_id, 'item': item});
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
