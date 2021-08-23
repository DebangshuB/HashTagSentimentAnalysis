function myFunction() {

    var results = document.getElementById("results");
    var loading = document.getElementById("loading");
    var text_field = document.getElementById("input_text");

    if (text_field.value === "") {
        return;
    }

    var numPositive = document.getElementById("num-result-positive");
    var numNeutral = document.getElementById("num-result-neutral");
    var numNegative = document.getElementById("num-result-negative");
    var avgText = document.getElementById("avg-sentiment-text");
    var avgNum = document.getElementById("avg-sentiment-num");
    let chartpie = document.getElementById('chart-pie').getContext('2d');


    results.style.display = "none";
    loading.style.display = "block";

    Chart.defaults.global.defaultFontFamily = 'Kaisei Opti';
    Chart.defaults.global.defaultFontSize = 12;
    Chart.defaults.global.defaultFontColor = '#777';

    console.log("Fetching started....")

    fetch("/api/" + text_field.value)
        .then(res => {
            res.json()
                .then(data => {
                    var arr = data.data;
                    arr = arr.split(",");
                    arr = arr.map(parseFloat);

                    var positives = 0;
                    var neutrals = 0;
                    var negatives = 0;
                    var count_ele = 0;
                    var sum_ele = 0;

                    for (const item of arr) {

                        sum_ele += item;
                        count_ele += 1;

                        if (item <= 0.30)
                            negatives += 1;
                        else if (item <= 0.70)
                            neutrals += 1;
                        else if (item > 0.70)
                            positives += 1;
                    }

                    var average_sentiment = sum_ele / count_ele;
                    var sentiment_string = ""

                    if (average_sentiment <= 0.30)
                        sentiment_string = "Negative";
                    else if (average_sentiment <= 0.70)
                        sentiment_string = "Neutral";
                    else if (average_sentiment > 0.70)
                        sentiment_string = "Positive";

                    numPositive.innerHTML = positives;
                    numNeutral.innerHTML = neutrals;
                    numNegative.innerHTML = negatives;
                    avgText.innerHTML = sentiment_string;
                    avgNum.innerHTML = (average_sentiment * 100).toFixed(2) + "%";

                    var data_plots = {
                        labels: ['Positive', 'Neutral', 'Negative'],
                        datasets: [{
                            data: [
                                positives, neutrals, negatives
                            ],
                            backgroundColor: [
                                'rgba(166, 255, 163, 0.6)',
                                'rgba(163, 200, 255, 0.6)',
                                'rgba(255, 163, 163, 0.6)',
                            ],
                            borderWidth: 1,
                            borderColor: '#777',
                            hoverBorderWidth: 3,
                            hoverBorderColor: '#000'
                        }]
                    }

                    let chartpieplot = new Chart(chartpie, {
                        type: 'pie', // bar, horizontalBar, pie, line, doughnut, radar, polarArea
                        data: data_plots,
                        options: {
                            aspectRatio: 1,
                            maintainAspectRatio: false,

                            legend: {
                                position: 'bottom'
                            }

                        }
                    });

                    results.style.display = "block";
                    loading.style.display = "none";


                })

        })
        .catch(err => console.log(err))
}