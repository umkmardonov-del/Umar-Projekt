// ======== ELEMENTE ========
const scene = document.getElementById("scene");
const app = document.getElementById("app");
const glow = document.getElementById("cursorGlow");
const title = document.getElementById("authTitle");
const text = document.getElementById("authText");
const toggle = document.getElementById("authToggle");
const nameRow = document.getElementById("nameRow");

// ======== CURSOR GLOW ========
document.addEventListener("mousemove", e => {
  glow.style.left = e.clientX + "px";
  glow.style.top = e.clientY + "px";
});

// ======== AUTH SZENE ÖFFNEN ========
document.getElementById("loginBtn").onclick = () => {
  scene.classList.add("auth-open");
  setMode("login");
};

document.getElementById("signupBtn").onclick = () => {
  scene.classList.add("auth-open");
  setMode("signup");
};

// ======== TOGGLE LOGIN/SIGNUP ========
toggle.onclick = e => {
  e.preventDefault();
  setMode(title.textContent === "Log in" ? "signup" : "login");
};

// ======== LOGIN / SIGNUP ACTION ========
document.getElementById("enterApp").onclick = async () => {
  const isSignup = title.textContent === "Sign up";

  const data = {
    firstName: document.getElementById("firstName")?.value,
    lastName: document.getElementById("lastName")?.value,
    email: document.getElementById("email").value,
    password: document.getElementById("password").value
  };

  // Backend-Endpunkte anpassen
  const endpoint = isSignup ? "/api/register" : "/api/login";

  try {
    const response = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include", // für Sessions/Cookies
      body: JSON.stringify(data)
    });

    const result = await response.json();

    if (response.ok) {
      // Erfolgreicher Login/Signup
      scene.style.opacity = "0";
      setTimeout(() => {
        scene.style.display = "none";
        app.classList.add("active");
      }, 500);
    } else {
      alert(result.detail || result.message || "Authentication failed");
    }
  } catch (err) {
    alert("Server not reachable");
  }
};

// ======== MODUS SETZEN (LOGIN / SIGNUP) ========
function setMode(mode) {
  if (mode === "login") {
    title.textContent = "Log in";
    text.textContent = "No account?";
    toggle.textContent = "Sign up";
    nameRow.classList.remove("active");
  } else {
    title.textContent = "Sign up";
    text.textContent = "Already registered?";
    toggle.textContent = "Log in";
    nameRow.classList.add("active");
  }
}

// ======== SIDEBAR SWITCH ========
const navButtons = document.querySelectorAll(".nav-btn");
const sections = document.querySelectorAll(".content-section");

navButtons.forEach(btn => {
  btn.addEventListener("click", () => {
    navButtons.forEach(b => b.classList.remove("active"));
    btn.classList.add("active");

    sections.forEach(sec => sec.classList.remove("active-section"));
    document.getElementById(btn.dataset.section).classList.add("active-section");
  });
});

// ======== PRESETS ========
const presets = {
  it: { dept: "IT", software: "Office 365" },
  hr: { dept: "HR", software: "Office 365" },
  dev: { dept: "IT", software: "Developer Tools" }
};

document.querySelectorAll("[data-preset]").forEach(b => {
  b.onclick = () => {
    document.getElementById("department").value = presets[b.dataset.preset].dept;
    document.getElementById("included_software").value = presets[b.dataset.preset].software;
  };
});
