const [labels_methods, amounts_methods] = getMethodsData();
const [labels_monthly, amounts_monthly] = getMonthlyAmountData();

const monthNames = ["January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];

function monthsFunction() {
  let months = [];
  for(let i = -5; i <= 0; i += 1) {
  d = new Date();
  month = d.getMonth() + i
      if (month < 0) {
          month += 12
      }
  months.push(monthNames[month])
}
  return months
}

let bgcolor = [
         'rgba(255, 99, 132, 0.2)',
         'rgba(54, 162, 235, 0.2)',
         'rgba(255, 206, 86, 0.2)',
         'rgba(75, 192, 192, 0.2)',
         'rgba(153, 102, 255, 0.2)',
         'rgba(255, 159, 64, 0.2)'
       ]
let brcolor = [
        'rgba(255,99,132,1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        'rgba(255, 159, 64, 1)'
      ]
let ChartData = {
  labels: [],
  datasets: []
};

labels_monthly.forEach(function (a) {
  ChartData.labels.push(a)
});

amounts_monthly.forEach(function (a, i){
  ChartData.datasets.push({
    label: ChartData.labels[i],
    backgroundColor: bgcolor[i],
    borderColor: brcolor[i],
    borderWidth: 1,
    data: a
  });
});


let ctxB = document.getElementById("barChart_1").getContext('2d');
let myBarChart = new Chart(ctxB, {
  type: 'bar',
  data: {
    labels: labels_methods,
    datasets: [{
      label: 'Оплаты по методам оплаты',
      data: amounts_methods,
      backgroundColor: bgcolor,
      borderColor: brcolor,
      borderWidth: 1
    }]
  },
  options: {
    scales: {
      yAxes: [{
        ticks: {
          beginAtZero: true
        }
      }]
    }
  }
});


let ctxB2 = document.getElementById("barChart_2").getContext('2d');
let myBarChart2 = new Chart(ctxB2, {
  type: 'bar',
  data: {
      labels: monthsFunction(),
      datasets: ChartData.datasets
  },
  options: {
      plugins: {
          title: {
            display: true,
            text: 'Выручка за последние 6 месяцев'
          },
          tooltip: {
              callbacks: {
                  label: function(context) {
                        let label = context.dataset.label || '';

                        if (label) {
                            label += ': ';
                        }

                        if (context.parsed.y !== null) {
                            label += new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(context.parsed.y);
                        }
                        return label;
                    },
                  footer: function(tooltipItems) {
                          let sum = 0;

                          tooltipItems.forEach(function(tooltipItem) {
                            sum += tooltipItem.parsed.y;
                          });
                          return 'Sum: ' + new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(sum);
                        },
              }
          }
      },
    responsive: true,
    scales: {
      x: {
        stacked: true,
      },
      y: {
        stacked: true
      }
    }
  }
});
