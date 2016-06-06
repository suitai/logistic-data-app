
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
                $.each(result, function(i){
                    output.append(
                        result[i]['dc:date'] + " " +
                        result[i]['frameworx:step'] + " " +
                        result[i]['frameworx:calorie'] + " " +
                        "<br>");
                });
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                console.log(textStatus);
            }
        });
    });
});


