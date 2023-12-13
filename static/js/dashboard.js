const ctx = document.getElementById('myChart'); 

new Chart(ctx, {
  type: 'line',
  data: {
    labels: timeData,
    datasets: [{
      label: 'Time',
      data: scoresData,
      borderWidth: 1
    }]
  },
  options: {
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }
});