var ctx;

function get_data(sendData) {
    return $.ajax({
        url: "https://api.frameworxopendata.jp/api/v3/datapoints",
        type: "get",
        data: sendData,
    });
}

function show_personal_data(result) {
    var times = [];
    var steps = [];
    var calories = [];
    var heartrates = [];
    var date;
    var time;

    $.each(result, function(i){
        date = new Date(result[i]['dc:date']);
        time = ("0"+date.getHours()).slice(-2) + ":" + ("0"+date.getMinutes()).slice(-2)
        if (time != times[times.length - 1]){
            times.push(time);
            steps.push(result[i]['frameworx:step']);
            calories.push(result[i]['frameworx:calorie']);
            heartrates.push(result[i]['frameworx:heartrate']);
        }
    });

    draw_line_graph(times, "steps", steps)

    // pythonへデータ転送
    step_data = JSON.stringify(result);
    return $.ajax({
        url: "_step_graph",
        data: "",
        dataType: "JSON",
        type: "post",
        contentType: 'application/json',
    });
}

function draw_line_graph(labels, label, value) {
    var dataset = {
        label: label,
        fillColor: "rgba(220,220,220,0.2)",
        strokeColor: "rgba(220,220,220,1)",
        pointColor: "rgba(220,220,220,1)",
        pointStrokeColor: "#fff",
        pointHighlightFill: "#fff",
        pointHighlightStroke: "rgba(220,220,220,1)",
        data: value
    };
    var data = {
        labels: labels,
        datasets: [dataset,]
    };
    var lineChart = new Chart(ctx, {
        type: "line",
        data: data,
    });
}

function fini(data) {
    console.log("success");
}


$(function() {
    var output = $(document.getElementById('json'));
    var message = $(document.getElementById('message'));
    ctx = $("#chart").get(0).getContext("2d");
    var secret_key;

    $.ajax({
        url: "_get_key",
        type: "get",
        contentType: 'application/json',
        success: function(result) {
            secret_key = result.key;
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            console.log(textStatus);
        }
    });

    $('#get').submit(function(event) {
        var type = "frameworx:WarehouseVital"
        var key = "frameworx:workerId"
        var value =  document.forms.get.value.value;

        var sendData = {
            "acl:consumerKey": secret_key,
            "rdf:type": type
        }
        sendData[key] = value;

        event.preventDefault();

        get_data(sendData)
            .then(show_personal_data)
            .then(fini);
    });
});


