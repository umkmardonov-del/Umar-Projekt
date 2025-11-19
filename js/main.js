document.getElementById("tryBtn").addEventListener("click", function () {
    const calculator = document.getElementById("calculator");

    calculator.scrollIntoView({ behavior: "smooth" });

    setTimeout(() => {
        calculator.classList.add("show");
    }, 500);
});