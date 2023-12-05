// Chame a API para obter os dados do gráfico
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

    // Configurações do gráfico
    var options = {
      series: [
        {
          name: "sales", // Nome da série
          data: seriesData, // Dados da série
        },
      ],
      chart: {
        type: "bar", // Tipo de gráfico (barra)
        height: 380, // Altura do gráfico
      },
      xaxis: {
        type: "category", // Tipo de eixo (categorias)
        labels: {
          formatter: function (val) {
            // Formato da label no eixo X
            return dayjs(val).format("MMM YYYY");
          },
        },
      },
      title: {
        text: "Gráfico de Contas por Ano e Mês", // Título do gráfico
      },
      tooltip: {
        x: {
          formatter: function (val) {
            // Formato do tooltip no eixo X
            return dayjs(val).format("MMM YYYY");
          },
        },
      },
    };

    // Crie e renderize o gráfico usando a biblioteca ApexCharts
    var chart = new ApexCharts(document.querySelector("#chart"), options);
    chart.render();
  })
  .catch((error) => console.error("Erro ao obter dados do gráfico:", error));
