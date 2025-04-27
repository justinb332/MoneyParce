google.charts.load('current', {'packages':['bar']});
function drawBar(chartData, title, subtitle, colorArray) {
    var data = google.visualization.arrayToDataTable(chartData);

    var options = {
        chart: {
            title: '',
            subtitle: '',
        },
        colors: colorArray,
        backgroundColor: '#FFFFF',
    };

    var chart = new google.charts.Bar(document.getElementById('bar'));
    chart.draw(data, google.charts.Bar.convertOptions(options));
}