const views = document.querySelectorAll(".view");
const sections = document.querySelectorAll(".section");
const sidebarLinks = document.querySelectorAll(".sidebar a");

const loginBtn = document.getElementById("loginBtn");
const signupBtn = document.getElementById("signupBtn");
const authForm = document.getElementById("authForm");
const authTitle = document.getElementById("authTitle");
const themeToggle = document.getElementById("themeToggle");

/* ---------- VIEW SWITCH (GSAP) ---------- */
function showView(id) {
  views.forEach(v => v.classList.remove("is-active"));
  const view = document.getElementById(id);
  view.classList.add("is-active");

  gsap.fromTo(view, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.6 });
}

/* Landing → Auth */
loginBtn.onclick = () => {
  authTitle.textContent = "Log in";
  showView("auth");
};

signupBtn.onclick = () => {
  authTitle.textContent = "Sign up";
  showView("auth");
};

/* Auth → Dashboard */
authForm.onsubmit = e => {
  e.preventDefault();
  showView("dashboard");
  activateSection("config");
};

/* ---------- SECTION NAV ---------- */
sidebarLinks.forEach(link => {
  link.onclick = () => activateSection(link.dataset.target);
});

function activateSection(id) {
  sections.forEach(s => s.classList.remove("is-active"));
  document.getElementById(id).classList.add("is-active");
}

/* ---------- CALCULATOR ---------- */
const teamSize = document.getElementById("teamSize");
const deviceCost = document.getElementById("deviceCost");
const softwareCost = document.getElementById("softwareCost");
const totalCostEl = document.getElementById("totalCost");

function calculate() {
  const total =
    teamSize.value * (deviceCost.value / 36 + Number(softwareCost.value));
  totalCostEl.textContent = `€${total.toFixed(2)}`;
  updateChart(total);
}

[teamSize, deviceCost, softwareCost].forEach(i =>
  i.addEventListener("input", calculate)
);

/* ---------- CHART ---------- */
const ctx = document.getElementById("costChart");
const chart = new Chart(ctx, {
  type: "bar",
  data: {
    labels: ["Monthly Cost"],
    datasets: [{
      label: "€",
      data: [0],
      backgroundColor: "#35d1d1"
    }]
  }
});

function updateChart(val) {
  chart.data.datasets[0].data[0] = val;
  chart.update();
}

/* ---------- THEME ---------- */
themeToggle.onclick = () => {
  document.body.classList.toggle("light");
};

/* ---------- PARTICLES ---------- */
particlesJS("particles-js", {
  particles: {
    number: { value: 70 },
    color: { value: "#35d1d1" },
    size: { value: 3, random: true },
    line_linked: { enable: true, color: "#35d1d1", opacity: 0.3 },
    move: { speed: 1.3 }
  }
});