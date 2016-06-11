
$(function() {
    var output = $(document.getElementById('json'));
    var message = $(document.getElementById('message'));
    var ctx = $("#chart").get(0).getContext("2d");
    var secret_key;
    var dataset_gray = {
        label: "",
        fillColor: "rgba(220,220,220,0.2)",
        strokeColor: "rgba(220,220,220,1)",
        pointColor: "rgba(220,220,220,1)",
        pointStrokeColor: "#fff",
        pointHighlightFill: "#fff",
        pointHighlightStroke: "rgba(220,220,220,1)",
        data: []
    };
    var dataset_blue = {
        label: "",
        fillColor: "rgba(151,187,205,0.2)",
        strokeColor: "rgba(151,187,205,1)",
        pointColor: "rgba(151,187,205,1)",
        pointStrokeColor: "#fff",
        pointHighlightFill: "#fff",
        pointHighlightStroke: "rgba(151,187,205,1)",
        data: []
    };
    var data = {
        labels: [],
        datasets: []
    };

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
        $.ajax({
            url: "https://api.frameworxopendata.jp/api/v3/datapoints",
            type: "get",
            data: sendData,
            success: function(result) {
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
                data.labels = times;
                dataset_gray.label = "step";
                dataset_gray.data = steps;
                data.datasets.push(dataset_gray);

                var lineChart = new Chart(ctx, {
                    type: "line",
                    data: data,
                });

                // pythonへデータ転送
                step_data = JSON.stringify(result);
                output.text(step_data);
                $.ajax({
                    url: "_step_graph",
                    data: step_data,
                    dataType: "JSON",
                    type: "post",
                    contentType: 'application/json',
                    success: function(result) {
                    },
                    error: function(XMLHttpRequest, textStatus, errorThrown) {
                        console.log(textStatus);
                    }
                });
                
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                console.log(textStatus);
            }
        });
    });
});


