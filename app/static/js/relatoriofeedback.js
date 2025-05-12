document.addEventListener('DOMContentLoaded', () => {
  const ctx = document.getElementById('graficoEstrelas').getContext('2d');

  const chart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['5 estrelas', '4 estrelas', '3 estrelas', '2 estrelas', '1 estrela'],
      datasets: [{
        label: '% de Avaliações',
        data: [0, 0, 0, 0, 0],
        backgroundColor: ['#28a745', '#17a2b8', '#ffc107', '#fd7e14', '#dc3545'],
        borderRadius: 6
      }]
    },
    options: {
      indexAxis: 'y',
      animation: {
        duration: 1200,
        easing: 'easeOutQuart'
      },
      scales: {
        x: {
          min: 0,
          max: 100,
          ticks: {
            callback: value => value + '%'
          }
        }
      },
      plugins: {
        legend: { display: false }
      }
    }
  });

  const select = document.getElementById('unidade-select');
  select.addEventListener('change', () => {
    const unidadeId = select.value;
    fetch(`/api/feedback_porcentagem/${unidadeId}`)
      .then(res => res.json())
      .then(data => {
        // Garante que todos os valores existam, mesmo se faltarem no retorno
        chart.data.datasets[0].data = [
          data['5 estrelas'] || 0,
          data['4 estrelas'] || 0,
          data['3 estrelas'] || 0,
          data['2 estrelas'] || 0,
          data['1 estrela'] || 0
        ];
        chart.update();
      })
      .catch(error => {
        console.error('Erro ao carregar dados:', error);
        chart.data.datasets[0].data = [0, 0, 0, 0, 0];
        chart.update();
      });
  });

  // Gatilho inicial
  select.dispatchEvent(new Event('change'));
});
