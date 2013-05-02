google.load("visualization", "1", {packages: ["corechart"]});
google.setOnLoadCallback(drawChart);
function drawChart() {
    var data = google.visualization.arrayToDataTable([
        ['Day in month', 'Votes'],
        ['7', 20],
        ['14', 30],
        ['21', 13],
        ['28', 5]
    ]);

    var options = {
        title: 'Server Votes',
        curveType: 'function',
        hAxis: {title: 'Date in Month'},
        vAxis: {title: 'Number of Votes'},
        legend: {position: 'none'}
    };

    var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
    chart.draw(data, options);
}