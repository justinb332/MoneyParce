import { ChartStrategy } from './ChartStrategy.js';

export class BarChartStrategy extends ChartStrategy {
    hi() {
        console.log('test')
    }
    draw(chartData, title, subtitle, colorArray) {
        const data = google.visualization.arrayToDataTable(chartData);

        const options = {
            chart: {
                title: title,
                subtitle: subtitle,
            },
            colors: colorArray,
            backgroundColor: '#FFFFFF',
        };

        const chart = new google.charts.Bar(document.getElementById('bar'));
        chart.draw(data, google.charts.Bar.convertOptions(options));
    }
}