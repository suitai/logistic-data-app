$(function() {
	var DESC = -1;
	var ASCE = 1;
	var chart;
    $(".rank_1st").addClass("on");
    $(".rank_2nd").addClass("on");
    $(".rank_3rd").addClass("on");
	$('#rank').submit(
			function(event) {
				event.preventDefault();
                $(".rank_1st").removeClass("on");
                $(".rank_2nd").removeClass("on");
                $(".rank_3rd").removeClass("on").onCSSTransitionEnd(function() {
                    var ctx = $("#rankingCanvas").get(0).getContext("2d");
                    var obtainedData;
                    var rank1Id = [ ];
                    var rank2Id = [ ];
                    var rank3Id = [ ];
                    var url;
                    var unit;
                    var sortType;
                    var rankingText;
                    var targetRanking = $('#ranking-select').children(':selected').attr('value');
                    switch (targetRanking) {
                    case 'item':
                        url = "_item_ranking";
                        sortType = DESC;
                        rankingText = "ピッキング商品数(個)";
                        break;
                    case 'calorie':
                        url = "_cal_ranking";
                        sortType = DESC;
                        rankingText = "消費カロリー(KCal)";
                        break;
                    case 'step':
                        url = "_step_ranking";
                        sortType = DESC;
                        rankingText = "歩数(歩)";
                        break;
                    case 'distance':
                        url = "_distance_ranking";
                        sortType = DESC;
                        rankingText = "従業員移動距離";
                        break;
                    default:
                        console.log('error');
                        break;
                    }

                    getData(url).done(function(result) {
                        obtainedData = result;
                        $(".rank_1st").addClass("on");
                        $(".rank_2nd").addClass("on");
                        $(".rank_3rd").addClass("on");
                        console.log(obtainedData);
                    }).fail(function(result) {
                        console.log("error");
                    });
                    var datasets = setData(obtainedData)
                    chartData = setChartData(datasets[0], datasets[1], rankingText)

                    if (typeof(chart) != "undefined") {
                        chart.destroy();
                    }
                    chart = new Chart(ctx, {
                        type : "bar",
                        data : chartData,
                        options: {
                            title: {
                                display: true,
                                text: ''
                            }
                        }
                    });

                    var sortdata = datasets[1].concat();
                    sortdata.sort(function(a, b) {
                        if (a > b)
                            return sortType;
                        if (a < b)
                            return -1 * sortType;
                        return 0;
                    });
                    var filtersortdata = sortdata.filter(function (value, index, self) {
                          return self.indexOf(value) === index;
                    });

                    for ( var key in obtainedData) {
                        var datay = obtainedData[key];
                        if (datay == filtersortdata[0]) {
                            rank1Id.push(key);
                        } else if (datay == filtersortdata[1]) {
                            rank2Id.push(key);
                        } else if (datay == filtersortdata[2]) {
                            rank3Id.push(key);
                        }
                    }

                    $("#rankingtable").attr("style","visibility:visible")
                    $("#result").text(rankingText);
                    $("#employee1").text(rank1Id);
                    $("#result1").text(sortdata[0]);
                    $("#employee2").text(rank2Id);
                    $("#result2").text(sortdata[1]);
                    $("#employee3").text(rank3Id);
                    $("#result3").text(sortdata[2]);

                })
            });
});

function setData(resuestResult) {
	var datax = [];
	var datay = [];
	for ( var key in resuestResult) {
		datax.push(key);
		datay.push(resuestResult[key]);
	}
	return [ datax, datay ]
}

function setChartData(datax, datay, text) {
	var chartData = {
		labels : datax,
		datasets : [ {
			label: text,
			fillColor : "blue",
			strokeColor : "blue",
			data : datay,
			borderColor: "rgba(255,204,51,0.6)",
            backgroundColor: "rgba(255,204,102,0.4)"
		}, ]
	};
	return chartData;
}

function getData(url) {
	return $.ajax({
		url : url,
		type : "get",
		async : false,
		contentType : 'application/json'
	});
}
