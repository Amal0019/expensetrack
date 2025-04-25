// Example of a simple script to highlight the navbar when scrolling
window.onscroll = function () {
    var navbar = document.querySelector(".navbar");
    if (window.scrollY > 50) {
        navbar.classList.add("bg-dark");
    } else {
        navbar.classList.remove("bg-dark");
    }
};

// Example of handling chart hover effects (optional)
const chartCanvas = document.getElementById('expenseChart');
if (chartCanvas) {
    chartCanvas.addEventListener('mousemove', function (event) {
        // Example interaction on hover
        const activePoints = myChart.getElementsAtEventForMode(event, 'nearest', {intersect: true}, true);
        if (activePoints.length) {
            // Do something when hovering over chart
        }
    });
}
