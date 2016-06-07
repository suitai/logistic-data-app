
$(function() {
    var output = $(document.getElementById('json'));
    var message = $(document.getElementById('message'));
    var secret_key;

    $.ajax({
        url: "_get_key",
        type: "GET",
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
        sendData[key] = value

        event.preventDefault();
        $.ajax({
            url: "https://api.frameworxopendata.jp/api/v3/datapoints",
            type: "GET",
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
                });
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                console.log(textStatus);
            }
        });
    });
});


