$(function() {
var ctx;
    ctx = $("#chart").get(0).getContext("2d");
    var itemData;
    var vitalData;

    $.ajax({
        url: "/_item_ranking",
        type: "get",
        contentType: 'application/json',
        success: function(result) {
            itemData=result;
            console.log(result);
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            console.log("error");
        }
    });

    // $.ajax({
    //     url: "/_vital_ranking",
    //     type: "get",
    //     contentType: 'application/json',
    //     success: function(result) {
    //         vitalData=result;
    //         console.log(result);
    //     },
    //     error: function(XMLHttpRequest, textStatus, errorThrown) {
    //         console.log("error");
    //     }
    // });


    $('#rank').submit(function(event) {
        var targetRank = $("[name=ranktitle]:checked").val()
        console.log(targetRank)
        var datax=[];
        var datay=[];    

        event.preventDefault();
 
        for ( var key in itemData) {
           datax.push(key);
           datay.push(itemData[key]);
            console.log(key);
            console.log(itemData[key]);
	    }

        var barChartData = {
        labels : datax,
        datasets : [
        {
          fillColor : "blue",
          strokeColor : "blue",
          data : datay
        },
        ]};

     var barChart = new Chart(ctx, {
        type: "bar",
        data: barChartData,
    });   });
});
