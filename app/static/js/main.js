document.getElementById("tryBtn").addEventListener("click", function () {
    const calculator = document.getElementById("calculator");
    const config = document.getElementById("configSection");

    // Smooth scroll zum Config Section
    config.scrollIntoView({ behavior: "smooth" });

    // Fade-in nach 0,5s
    setTimeout(() => {
        calculator.classList.add("show");
        config.classList.add("show");
    }, 500);
});