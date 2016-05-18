"use strict";

$(() => {
    var output = $(document.getElementById('json'));
    var message = $(document.getElementById('message'));
    var secret_key;

    $.ajax({
        url: "_get_key",
        type: "GET",
        contentType: 'application/json',
        success: (result) => {
            secret_key = result.key;
        },
        error: (XMLHttpRequest, textStatus, errorThrown) => {
            console.log(textStatus);
        }
    });

    $('#get').submit((event) => {
        var type = document.forms.get.type.value;
        var key = document.forms.get.key.value;
        var value = document.forms.get.value.value;

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
            success: (result) => {
                output.text(JSON.stringify(result, null, '    '));
            },
            error: (XMLHttpRequest, textStatus, errorThrown) => {
                console.log(textStatus);
            }
        });
    });

});

