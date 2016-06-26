$(function() {
	var ctx = $("#rankingCanvas").get(0).getContext("2d");

	var itemData;
	var vitalData;

	getData("_item_ranking").done(function(result) {
		itemData = result;
		console.log(result);
		var datasets = setData(itemData)
		totalItemNumChartData = setChartData(datasets[0], datasets[1])

		$("#result").text("ピッキングした商品数");
		$("#employee1").text(datasets[0][0]);
		$("#result1").text(datasets[1][0]);
		$("#employee2").text(datasets[0][1]);
		$("#result2").text(datasets[1][1]);
		$("#employee3").text(datasets[0][2]);
		$("#result3").text(datasets[1][2]);

		var totalItemNumChart = new Chart(ctx, {
			type : "bar",
			data : totalItemNumChartData,
		});
	}).fail(function(result) {
		console.log("error");
	});

	$('#rank').submit(function(event) {
		event.preventDefault();
		getData("_item_ranking").done(function(result) {
			itemData = result;
			console.log(result);
		}).fail(function(result) {
			console.log("error");
		});
		var datasets = setData(itemData)
		totalItemNumChartData = setChartData(datasets[0], datasets[1])

		var totalItemNumChart = new Chart(ctx, {
			type : "bar",
			data : totalItemNumChartData,
		});

		datasets[1].sort(function(a, b) {
			if (a > b)
				return -1;
			if (a < b)
				return 1;
			return 0;
		});
		console.log(datasets[1]);

		var rank1Id;
		var rank2Id;
		var rank3Id;

		for ( var key in itemData) {
			var datay = itemData[key];
			if (datay = datasets[1][0]) {
				rank1Id = key;
			} else if (datay = datasets[1][1]) {
				rank2Id = key;
			} else if (datay = datasets[1][2]) {
				rank3Id = key;
			}
		}

		$("#result").text("ピッキングした商品数");
		$("#employee1").text(rank1Id);
		$("#result1").text(datasets[1][0]);
		$("#employee2").text(rank2Id);
		$("#result2").text(datasets[1][1]);
		$("#employee3").text(rank3Id);
		$("#result3").text(datasets[1][2]);

	})
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

function setChartData(datax, datay) {
	var chartData = {
		labels : datax,
		datasets : [ {
			fillColor : "blue",
			strokeColor : "blue",
			data : datay
		}, ]
	};
	return chartData;
}

function getData(url) {
	return $.ajax({
		url : url,
		type : "get",
		contentType : 'application/json',
	});
}