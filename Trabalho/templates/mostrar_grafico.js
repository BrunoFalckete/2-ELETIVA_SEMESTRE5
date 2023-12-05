// Modifique a função para obter os dados do gráfico
fetch("/mostrat_grafico")
  .then((response) => response.json())
  .then((data) => {
    // Transforme os dados recebidos em um formato adequado para o gráfico
    var seriesData = [];

    // Itere sobre os dados recebidos e agrupe por ano e mês
    for (var ano in data) {
      for (var mes in data[ano]) {
        seriesData.push({
          x: ano + "/" + mes + "/01",
          y: data[ano][mes],
        });
      }
    }

    // Crie as opções do gráfico
    var options = {
      series: [
        {
          name: "sales",
          data: seriesData,
        },
      ],
      chart: {
        type: "bar",
        height: 380,
      },
      xaxis: {
        type: "category",
        labels: {
          formatter: function (val) {
            return dayjs(val).format("MMM YYYY");
          },
        },
      },
      title: {
        text: "Gráfico de Contas por Ano e Mês",
      },
      tooltip: {
        x: {
          formatter: function (val) {
            return dayjs(val).format("MMM YYYY");
          },
        },
      },
    };

    // Crie e renderize o gráfico
    var chart = new ApexCharts(document.querySelector("#chart"), options);
    chart.render();
  })
  .catch((error) => console.error("Erro ao obter dados do gráfico:", error));
