import { PieChartStrategy } from './PieChartStrategy.js';
import { BarChartStrategy } from './BarChartStrategy.js';

export function chart(input, title, subtitle, strategy, colorChoice) {
    google.charts.load('current', {
        packages: ['corechart', 'bar']
    });
    google.charts.setOnLoadCallback(function () {

        let colorsArray = getColor(colorChoice);

        const transactions = input;

        const categoriesSet = new Set();
        const datesSet = new Set();

        transactions.forEach(t => {
            categoriesSet.add(t['category__name']);
            datesSet.add(t['date']);
        });

        const categories = Array.from(categoriesSet);
        const dates = Array.from(datesSet).reverse();
        const prices = [];

        dates.forEach(date => {
            prices.push([date, ...new Array(categories.length).fill(0)]);
        });

        transactions.forEach(t => {
            const dateIndex = dates.indexOf(t.date);
            const categoryIndex = categories.indexOf(t['category__name']);
            if (dateIndex !== -1 && categoryIndex !== -1) {
                prices[dateIndex][categoryIndex + 1] += parseFloat(t.amount);
            }
        });

        // Final chart data
        const chartData = [
            ['Date', ...categories],
              ...prices,
        ];

        const title = 'Transactions';
        const subtitle = 'Money';

        console.log('Categories:', categories);
        console.log('Dates:', dates);
        console.log('Prices:', prices);
        console.log('Final:', chartData);

        console.log('Strategy:', strategy);
        console.log('Methods in strategy:', Object.getOwnPropertyNames(strategy));
        strategy.draw(chartData, title, subtitle, colorsArray)
    });
}

function getColor(colorChoice) {
    let color1, color2, color3, color4, color5, color6;

    switch (colorChoice) {
        case 'color1':
            color1 = '#6d4caf';
            color2 = '#2196f3';
            color3 = '#3bff9d';
            color4 = '#c63ed0';
            color5 = '#b02737';
            color6 = '#95cde1';
            break;
        case 'color2':
            color1 = '#3f51b5';
            color2 = '#00bcd4';
            color3 = '#8bc34a';
            color4 = '#ff5722';
            color5 = '#795548';
            color6 = '#607d8b';
            break;
        case 'color3':
            color1 = '#9e9e9e';
            color2 = '#ff9800';
            color3 = '#673ab7';
            color4 = '#ff5722';
            color5 = '#4caf50';
            color6 = '#f44336';
            break;
        case 'color4':
            color1 = '#c2185b';
            color2 = '#f44336';
            color3 = '#9c27b0';
            color4 = '#3f51b5';
            color5 = '#00bcd4';
            color6 = '#8bc34a';
            break;
        default:
            color1 = '#000000';
            color2 = '#000000';
            color3 = '#000000';
            color4 = '#000000';
            color5 = '#000000';
            color6 = '#000000';
            break;
        }
        return [color1, color2, color3, color4, color5, color6]
}