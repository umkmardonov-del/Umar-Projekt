document.addEventListener("DOMContentLoaded", function() {
    particlesJS("particles-js", {
      "particles": {
        "number": { "value": 80, "density": { "enable": true, "value_area": 800 } },
        "color": { "value": "#0A5D5D" },
        "shape": { "type": "circle" },
        "opacity": { "value": 0.8 },
        "size": { "value": 4, "random": true },
        "line_linked": {
          "enable": true,
          "distance": 150,
          "color": "#0A5D5D",
          "opacity": 0.4,
          "width": 1
        },
        "move": { "enable": true, "speed": 1.5, "out_mode": "out" }
      },
      "interactivity": {
        "events": {
          "onhover": { "enable": true, "mode": "grab" }
        },
        "modes": {
          "grab": { "distance": 200, "line_linked": { "opacity": 0.6 } }
        }
      },
      "retina_detect": true
    });
});