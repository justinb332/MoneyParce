import { ChartStrategy } from './ChartStrategy.js';

export class PieChartStrategy extends ChartStrategy {
    draw(chartData, title, subtitle, colorArray) {
        const convertedData = this.convertToPie(chartData);
        const data = google.visualization.arrayToDataTable(convertedData);

        const options = {
            title: title,
            subtitle: subtitle,
            is3D: false,
            slices: {
                0: { color: colorArray[0] },
                1: { color: colorArray[1] },
                2: { color: colorArray[2] },
                4: { color: colorArray[3] },
                5: { color: colorArray[4] },
                6: { color: colorArray[5] },
            }
        };

        const chart = new google.visualization.PieChart(document.getElementById('pie'));
        chart.draw(data, options);
    }

    convertToPie(chartData) {
        let pieData = [];
        for (let i = 1; i < chartData[0].length; i++) {
            pieData[i - 1] = [];
            pieData[i - 1][0] = chartData[0][i];
            pieData[i - 1][1] = chartData[chartData.length - 1][i];
        }
        console.log(...pieData);
        pieData = [['.', '.'], ...pieData];
        return pieData;
    }
}