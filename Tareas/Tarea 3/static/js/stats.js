document.addEventListener('DOMContentLoaded', function () {
    // Inicializar el primer gráfico de Highcharts para productos
    Highcharts.chart("container", {
      chart: {
        type: "pie",
      },
      title: {
        text: "Distribución de Productos",
      },
      series: [
        {
          name: "Cantidad",
          colorByPoint: true,
          data: [],
        },
      ],
    });
  
    // Inicializar el segundo gráfico de Highcharts para ciudades
      chart: {
        type: "pie",
      },
      title: {
        text: "Distribución de Ciudades por Pedidos",
      },
      series: [
        {
          name: "Cantidad",
          colorByPoint: true,
          data: [],
        },
      ],
    });
  
    // Fetch data from the server
    fetch("/get-stats-data")
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        console.log(data); 
        if (!data.products_data || !data.cities_data) {
          throw new Error("Missing data from response");
        }
  
        const productsData = data.products_data.map((item) => ({
          name: item[0],
          y: item[1],
        }));
  
        const citiesData = data.cities_data.map((item) => ({
          name: item[0],
          y: item[1],
        }));
  
        // Get the chart for products by ID
        const productsChart = Highcharts.charts.find(
          (chart) => chart && chart.renderTo.id === "container"
        );
  
        // Update the products chart with new data
        productsChart.update({
          series: [
            {
              data: productsData,
            },
          ],
        });
  
        // Get the chart for cities by ID
        const citiesChart = Highcharts.charts.find(
          (chart) => chart && chart.renderTo.id === "container2"
        );
  
        // Update the cities chart with new data
        citiesChart.update({
          series: [
            {
              data: citiesData,
            },
          ],
        });
      })
      .catch((error) => console.error("Error:", error));
  });
  