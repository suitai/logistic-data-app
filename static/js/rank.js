var ctx;

$(function() {
    ctx = $("#chart2").get(0).getContext("2d");
    var data;

    $.ajax({
        url: "/_item_ranking",
        type: "get",
        contentType: 'application/json',
        success: function(result) {
            data=result;
            console.log(result);
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            console.log("bbb");
        }
    });

    $('#rank').submit(function(event) {

        event.preventDefault();

        var datax=[];
        var datay=[];     
        for ( var key in data) {
           datax.push(key);
           datay.push(data[key]);
            console.log(key);
            console.log(data[key]);
	 }

    var barChartData = {
      datasets : [
        {
          fillColor : "red",
          strokeColor : "red",
          data : datax
        },
        {
          fillColor : "blue",
          strokeColor : "blue",
          data : datay
        },
      ]
    }

        var chart = new Chart(ctx, {
        type: "bar",
        data: barChartData,
    });
});


