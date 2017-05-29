
$(document).ready(function () {

window.tmp_pred = 10

function evaluate(){
    $(".preloader").fadeIn();

    $.getJSON('predict/',{"dana" : window.tmp_pred},  function(data) {
        //data is the JSON string
        prediction_labels = data['prediction_labels']
        prediction_list = data['prediction_list']
        prediction_energy_sum = data['prediction_energy_sum']
        prediction_days = data['prediction_days']
        maximum_temperatures_list = data['maximum_temperatures_list']


        // set the energy sum calculated
        $("#prediction_energy2").text(prediction_energy_sum + " kWh");

        // set prediction days
        $("#prediction_days").text("Dijagram predviđene potrošnje  - " + prediction_days + " dana");
        $("#range_title").text("Model za " + prediction_days + " dana");
         //insert the graph on place the "ct-visites" id tag
         new Chartist.Line('#ct-visits', {
             labels: prediction_labels,
             series: [ [] , prediction_list ]
         }, {
             top: 0,
             low: 0,
             showPoint: true,
             fullWidth: true,
             plugins: [
                Chartist.plugins.tooltip()
                    ],
             axisY: {
                 labelInterpolationFnc: function (value) {
                     return (value / 1) + 'kW';
                 }
             },
             showArea: true
         });

        // set temperatures bar
         $('#sparklinedash').sparkline(maximum_temperatures_list, {
             type: 'bar',
             height: '40',
             barWidth: '7',
             resize: true,
             barSpacing: '7',
             barColor: '#599370'
         });


        // show the view
        $(".preloader").fadeOut();
        });
    }

//on document successfull load perform request
evaluate();
document.getElementById("eval_button").onclick = evaluate;
});

function showValue(newValue) {
document.getElementById("range_title").innerHTML="Model za " + newValue + " dana";
window.tmp_pred = newValue
}
