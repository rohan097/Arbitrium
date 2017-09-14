// cagr chart
function init_cagr_chart( data ){
  if( typeof ($.plot) === 'undefined'){ return; }

  console.log('init_cagr_chart');

  var cagr_plot_01_settings = {
        series: {
          lines: {
            show: true,
            fill: true
          },
          points: {
            radius: 3,
            show: true
          },
          shadowSize: 2
        },
        grid: {
          verticalLines: true,
          hoverable: true,
          clickable: true,
          tickColor: "#313C57",
          borderWidth: 0,
          color: '#313C57'
        },
        colors: ["#6495ED"],
        xaxis: {
          minTickSize: 1,
          axisLabel: 'Year',
          axisLabelUseCanvas: true,
          axisLabelFontSizePixels: 12,
          axisLabelFontFamily: 'Verdana, Arial, Helvetica, Tahoma, sans-serif',
          axisLabelPadding: 5,
          ticks: 5,
          tickDecimals: 0,
          tickColor: "rgba(51, 51, 51, 0.06)",
        },
        yaxis: {
          axisLabel: 'Value',
          axisLabelUseCanvas: true,
          axisLabelFontSizePixels: 12,
          axisLabelFontFamily: 'Verdana, Arial, Helvetica, Tahoma, sans-serif',
          axisLabelPadding: 5,
          ticks: 5,
          tickColor: "rgba(51, 51, 51, 0.06)",
        },
        tooltip: false
      }
  if ($("#cagr_plot_01").length){
    console.log('Plot1');
    plottedData = [];
    plottedData = data.sort()
    $.plot( $("#cagr_plot_01"), [ plottedData ],  cagr_plot_01_settings );
  }
}
// /cagr chart

// predict churn gauge meter
function predict_churn(val){
  console.log(val);
  var opts = {
    angle: 0.35, // The span of the gauge arc
    lineWidth: 0.1, // The line thickness
    radiusScale: 1, // Relative radius
    pointer: {
      length: 0.6, // // Relative to gauge radius
      strokeWidth: 0.035, // The thickness
      color: '#000000' // Fill color
    },
    limitMax: false,     // If false, max value increases automatically if value > maxValue
    limitMin: false,     // If true, the min value of the gauge will be fixed
    colorStart: '#6F6EA0',   // Colors
    colorStop: '#00C79F',    // just experiment with them
    strokeColor: '#EEEEEE',  // to see which ones work best for you
    generateGradient: true,
    highDpiSupport: true     // High resolution support
  };
  var target = document.getElementById('predict_chart_gauge'); // your canvas element
  var gauge = new Donut(target).setOptions(opts); // create sexy gauge!
  gauge.maxValue = 100; // set max gauge value
  gauge.setMinValue(0);  // Prefer setter over gauge.minValue = 0
  gauge.animationSpeed = 32; // set animation speed (32 is default value)
  gauge.set(val); // set actual value
  document.getElementById('churn_val').innerHTML=val;
};
// /predict churn gauge meter

// predict churn gauge meter for generic company
function predict_churn_gen(val){
  console.log(val);
  var opts = {
    angle: 0.35, // The span of the gauge arc
    lineWidth: 0.1, // The line thickness
    radiusScale: 1, // Relative radius
    pointer: {
      length: 0.6, // // Relative to gauge radius
      strokeWidth: 0.035, // The thickness
      color: '#000000' // Fill color
    },
    limitMax: false,     // If false, max value increases automatically if value > maxValue
    limitMin: false,     // If true, the min value of the gauge will be fixed
    colorStart: '#6F6EA0',   // Colors
    colorStop: '#00C79F',    // just experiment with them
    strokeColor: '#EEEEEE',  // to see which ones work best for you
    generateGradient: true,
    highDpiSupport: true     // High resolution support
  };
  var target = document.getElementById('predict_chart_gauge_gen'); // your canvas element
  var gauge = new Donut(target).setOptions(opts); // create sexy gauge!
  gauge.maxValue = 100; // set max gauge value
  gauge.setMinValue(0);  // Prefer setter over gauge.minValue = 0
  gauge.animationSpeed = 32; // set animation speed (32 is default value)
  gauge.set(val); // set actual value
  document.getElementById('churn_val_gen').innerHTML=val;
}
// predict churn gauge meter for generic company

// CAGR line chart
function card1_linechart(lbl, vlu) {
      var data = {
          labels: lbl,
          datasets: [
              {
                  label: "dataset",
                  fillColor: "rgb(111, 176, 169, 0.4)",
                  strokeColor: "rgba(251,187,205,1)",
                  pointColor: "rgba(151,187,205,1)",
                  pointStrokeColor: "#fff",
                  pointHighlightFill: "#fff",
                  pointHighlightStroke: "rgba(151,187,205,1)",
                  data: vlu,
              }
          ]
      };
      var ctx = document.getElementById("lineChart1").getContext("2d");
      var options = { };
      var lineChart = new Chart(
        (ctx),
        {
          type: "line",
          data: data
        });
    }
// / CAGR line chart

// customer performance value meter
function performance_val(val){
  var opts = {
    angle: 0.15, // The span of the gauge arc
    lineWidth: 0.44, // The line thickness
    radiusScale: 1, // Relative radius
    pointer: {
      length: 0.6, // // Relative to gauge radius
      strokeWidth: 0.035, // The thickness
      color: '#000000' // Fill color
    },
    limitMax: false,     // If false, max value increases automatically if value > maxValue
    limitMin: false,     // If true, the min value of the gauge will be fixed
    colorStart: '#6FADCF',   // Colors
    colorStop: '#8FC0DA',    // just experiment with them
    strokeColor: '#E0E0E0',  // to see which ones work best for you
    generateGradient: true,
    highDpiSupport: true     // High resolution support
  };
  var target = document.getElementById('performance_chart'); // your canvas element
  var gauge = new Gauge(target).setOptions(opts); // create sexy gauge!
  gauge.maxValue = 100; // set max gauge value
  gauge.setMinValue(0);  // Prefer setter over gauge.minValue = 0
  gauge.animationSpeed = 80; // set animation speed (32 is default value)
  gauge.set(val); // set actual value
  document.getElementById('performance_val_text').innerHTML=val;
}
// /customer performance value meter

// preloader timeout
jQuery(window).load(function(){
    jQuery("#loader-wrapper").fadeOut();
});
// /preloader timeout

// fullscreen toggler
function toggleFullscreen(elem) {
  elem = elem || document.documentElement;
  if (!document.fullscreenElement && !document.mozFullScreenElement &&
    !document.webkitFullscreenElement && !document.msFullscreenElement) {
    if (elem.requestFullscreen) {
      elem.requestFullscreen();
    } else if (elem.msRequestFullscreen) {
      elem.msRequestFullscreen();
    } else if (elem.mozRequestFullScreen) {
      elem.mozRequestFullScreen();
    } else if (elem.webkitRequestFullscreen) {
      elem.webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT);
    }
  } else {
    if (document.exitFullscreen) {
      document.exitFullscreen();
    } else if (document.msExitFullscreen) {
      document.msExitFullscreen();
    } else if (document.mozCancelFullScreen) {
      document.mozCancelFullScreen();
    } else if (document.webkitExitFullscreen) {
      document.webkitExitFullscreen();
    }
  }
}

document.getElementById('btnFullscreen').addEventListener('click', function() {
  toggleFullscreen();
});
// / fullscreen toggler
