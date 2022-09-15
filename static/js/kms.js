/*!
 * codigo p gerar grafico de kms
 */
function linechart_tot_id(months, totals_id) {
    var ctx_km = document.getElementById("linechart_tot_id").getContext("2d");
    var linechart = new Chart(ctx_km, {
        type: "line",
        // Data options
        data: {
            labels: {{ months | safe }}, // Safe is for populate
            datasets: [{
                backgroundColor: 'rgba(55, 174, 148, 0.81)',
                borderColor: "rgba(55, 174, 148, 0.81)",
                data: {{ totals_id | safe }},
                datalabels: {
                    align: 'end',
                    anchor: 'end',
                }
            }]
        },
        plugins: [ChartDataLabels],
        options: {
            responsive: false,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Your Transports by month',
                    position: 'top',
                    align: 'start',
                    fullSize: 'false',
                    color: 'rgb(0,0,0)',
                    font: {
                        weight: 'bold',
                        size: 20
                    }
                    
                },
                datalabels: {
                    backgroundColor: 'rgba(55, 174, 148, 0.81)',
                    borderRadius: 4,
                    color: 'white',
                    font: {
                        weight: 'bold'
                    },
                    formatter: Math.round,
                    padding: 6
                }
            },

            // Core options
            aspectRatio: 5 / 3,
            layout: {
                padding: {
                    top: 32,
                    right: 16,
                    bottom: 16,
                    left: 8
                }
            },
            elements: {
                line: {
                    fill: false,
                    tension: 0.4
                }
            },
            scales: {
                y: {
                    stacked: true,
                    display: false
                },
                offset: true,
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}
