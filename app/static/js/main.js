const scene = document.getElementById("scene");
const app = document.getElementById("app");
const glow = document.getElementById("cursorGlow");
const title = document.getElementById("authTitle");
const text = document.getElementById("authText");
const toggle = document.getElementById("authToggle");
const nameRow = document.getElementById("nameRow");

document.addEventListener("mousemove", e => {
  glow.style.left = e.clientX + "px";
  glow.style.top = e.clientY + "px";
});

document.getElementById("loginBtn").onclick = () => {
  scene.classList.add("auth-open");
  setMode("login");
};

document.getElementById("signupBtn").onclick = () => {
  scene.classList.add("auth-open");
  setMode("signup");
};

toggle.onclick = e => {
  e.preventDefault();
  setMode(title.textContent === "Log in" ? "signup" : "login");
};

document.getElementById("enterApp").onclick = async () => {

  const isSignup = title.textContent === "Sign up";

  const data = {
    firstName: document.getElementById("firstName").value,
    lastName: document.getElementById("lastName").value,
    email: document.querySelector('input[type="email"]').value,
    password: document.querySelector('input[type="password"]').value
  };

  const endpoint = isSignup ? "/api/signup" : "/api/login";

  try {
    const response = await fetch(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      credentials: "include", // wichtig falls Backend Sessions nutzt
      body: JSON.stringify(data)
    });

    const result = await response.json();

    if (response.ok) {

      // Nur bei erfolgreichem Login App öffnen
      scene.style.opacity = "0";
      setTimeout(()=>{
        scene.style.display = "none";
        app.classList.add("active");
      },500);

    } else {
      alert(result.message || "Authentication failed");
    }

  } catch (err) {
    alert("Server not reachable");
  }
};


/* SIDEBAR SWITCH */
const navButtons = document.querySelectorAll(".nav-btn");
const sections = document.querySelectorAll(".content-section");

navButtons.forEach(btn=>{
  btn.addEventListener("click",()=>{
    navButtons.forEach(b=>b.classList.remove("active"));
    btn.classList.add("active");

    sections.forEach(sec=>sec.classList.remove("active-section"));
    document.getElementById(btn.dataset.section)
      .classList.add("active-section");
  });
});

/* PRESETS */
const presets={
  it:{dept:"IT",software:"Office 365"},
  hr:{dept:"HR",software:"Office 365"},
  dev:{dept:"IT",software:"Developer Tools"}
};

document.querySelectorAll("[data-preset]").forEach(b=>{
  b.onclick=()=>{
    department.value=presets[b.dataset.preset].dept;
    included_software.value=presets[b.dataset.preset].software;
  };
});

