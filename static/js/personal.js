function draw_line_graph(chart, ctx) {
    var colors = {
        "カロリー": {borderColor: "rgba(255,204,51,0.6)",
                     backgroundColor: "rgba(255,204,102,0.4)"},
        "歩数": {borderColor: "rgba(0,102,255,0.6)",
                 backgroundColor: "rgba(0,153,255,0.4)"},
        "脈拍": {borderColor: "rgba(255,0,102,0.6)",
                 backgroundColor: "rgba(255,51,102,0.4)"},
        "気温": {borderColor: "rgba(153,255,153,0.6)",
                 backgroundColor: "rgba(204,255,15,0.4)"},
        "湿度": {borderColor: "rgba(153,255,255,0.6)",
                 backgroundColor: "rgba(204,255,255,0.4)"},
        "商品数": {borderColor: "rgba(153,153,153,0.6)",
                   backgroundColor: "rgba(204,204,204,0.4)"},
        "距離": {borderColor: "rgba(0,153,51,0.6)",
                   backgroundColor: "rgba(0,204,51,0.4)"},
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

function draw_radar_graph(chart, ctx) {
    var labels = [];
    var data = [];

    for(c in chart){
        labels.push(c);
        data.push(100 * chart[c][0]/chart[c][1]);
    }

    var dataset = {
        label: "summary",
        data: data
    };
    var data = {
        labels: labels,
        datasets: [dataset,]
    };
    var radarChart = new Chart(ctx, {
        type: "radar",
        data: data,
        options: {
            scale: {
                type: "radialLinear",
                ticks: {
                    min: 0,
                    max: 100,
                    maxTicksLimit: 5
                }
            }
        }
    });
    console.log("draw: summary");
}

function draw_log_graph(charts) {

    for (var i = 0; i < charts.length; i++) {
        if(charts[i]['value_x'].length == 0){
            $('#canvas_content').append("<h2>" + charts[i]['label'] + "</h2>");
            $('#canvas_content').append("<p>Can not find data.</p>");
            continue;
        }
        var message = charts[i]['title'] + ": " + charts[i]['result'] + " " + charts[i]['unit'];

        $('#canvas_content').append("<h2>" + charts[i]['label'] + "</h2>");
        $('#canvas_content').append($('<div>').attr('id', "chart_content" + String(i)));
        $('#chart_content' + String(i)).attr('class', "chart-section");
        $('#chart_content' + String(i)).append($('<canvas>').attr('id', "chart" + String(i)));
        $("#chart" + String(i)).attr('width', 250);
        $('#chart_content' + String(i)).append($("<p>" + message + "</p>"));

        var ctx = $("#chart" + String(i)).get(0).getContext("2d");
        draw_line_graph(charts[i], ctx);
    }
}

function draw_summary_graph(charts) {
    $('#canvas_content').append($('<div>').attr('id', "chart_content"));
    $('#chart_content').attr('class', "chart-section");
    $('#chart_content').append($('<canvas>').attr('id', "chart_summary"));
    $('#chart_content').append($('<table>').attr('id', "table_summary"));
    $('#table_summary').append("<tr><th>項目</th><th>数値</th><th>基準値</th>/tr>");
    for (c in charts) {
        $('#table_summary').append("<tr><td>" + c + "</td><td>" + charts[c][0] + "</td><td>" + charts[c][1] +  "</td></tr>");
    }
    $('#chart_content').append($('</table>'));
    $('#canvas_content').append($('</div>'));

    var ctx = $("#chart_summary").get(0).getContext("2d");
    draw_radar_graph(charts, ctx);
}

function get_data(url, post_data){
    return $.ajax({
        url: url,
        type: 'post',
        data: post_data,
        contentType: 'application/json',
    });
}

function get_category(){
    var all_categories = ["カロリー", "歩数", "脈拍", "気温", "湿度", "商品数", "距離"];
    var category = [];

    for (var i = 0; i < all_categories.length; i++){
        if ($('#' + all_categories[i] + 'ボタン').attr('aria-pressed') == "true"){
            category.push(all_categories[i]);
        }
    }
    return category;
}

function log_event_fn(workerId) {
    return function log_event(event) {
        $('#canvas_content').html("");

        var category = get_category();
        var post_data = JSON.stringify({
            workerId: workerId,
            category: category
        });
        console.log("post:", post_data);

       $("#loading").show();

        event.preventDefault();
        get_data("_get_personal_log_data", post_data).done(function(result) {
            console.log("get:", result['data']);
            $("#loading").hide();
            draw_log_graph(JSON.parse(result['data']));
        }).fail(function(result) {
            console.log("error: ", result);
        });
    };
}

function summary_event_fn(workerId) {
    return function summary_event(event){
        $('#canvas_content').html("");

        var post_data = JSON.stringify({
            workerId: workerId,
        });
        console.log("post:", post_data);

        $("#loading").show();

        event.preventDefault();
        get_data("_get_personal_summary_data", post_data).done(function(result) {
            console.log("get:", result['data']);
            $("#loading").hide();
            draw_summary_graph(JSON.parse(result['data']));
        }).fail(function(result) {
            console.log("error: ", result);
        });
    };
}

$(function() {
    var workerId = -1;
    $.ajax({
        url: '/_get_session',
        type: 'get',
        data: {key: "username"},
        contentType: 'application/json',
    }).done(function(result) {
        workerId = result;
        $('#display_log_btn').on('click', log_event_fn(workerId));
        $('#display_summary_btn').on('click', summary_event_fn(workerId));
    });

    $("#loading").hide();
    console.log("welcome to personal page");

});

