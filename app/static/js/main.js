const scene = document.getElementById("scene");
const app = document.getElementById("app");
const glow = document.getElementById("cursorGlow");
const title = document.getElementById("authTitle");
const text = document.getElementById("authText");
const toggle = document.getElementById("authToggle");
const nameRow = document.getElementById("nameRow");
const authForm = document.getElementById("authForm");
const loginBtn = document.getElementById("loginBtn");
const signupBtn = document.getElementById("signupBtn");
const firstNameInput = authForm?.querySelector('input[name="first_name"]');
const lastNameInput = authForm?.querySelector('input[name="last_name"]');
const emailInput = authForm?.querySelector('input[name="email"]');
const passwordInput = authForm?.querySelector('input[name="password"]');

document.addEventListener("mousemove", (event) => {
  if (!glow) return;
  glow.style.left = `${event.clientX}px`;
  glow.style.top = `${event.clientY}px`;
});

if (loginBtn && scene) {
  loginBtn.onclick = () => {
    scene.classList.add("auth-open");
    setMode("login");
  };
}

if (signupBtn && scene) {
  signupBtn.onclick = () => {
    scene.classList.add("auth-open");
    setMode("signup");
  };
}

if (toggle && title) {
  toggle.onclick = (event) => {
    event.preventDefault();
    setMode(title.textContent === "Log in" ? "signup" : "login");
  };
}

if (authForm && title && scene && app) {
  authForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const isSignup = title.textContent === "Sign up";

    const data = isSignup
      ? {
          email: emailInput?.value.trim(),
          password: passwordInput?.value,
          name: firstNameInput?.value.trim(),
          surname: lastNameInput?.value.trim()
        }
      : {
          email: emailInput?.value.trim(),
          password: passwordInput?.value
        };

    if (!data.email || !data.password || (isSignup && (!data.name || !data.surname))) {
      alert("Please fill in all required fields.");
      return;
    }

    const endpoint = isSignup ? "/register" : "/login";

    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify(data)
      });

      const result = await response.json().catch(() => ({}));

      if (response.ok) {
        scene.style.opacity = "0";
        setTimeout(() => {
          scene.style.display = "none";
          app.classList.add("active");
        }, 500);
      } else if (Array.isArray(result?.detail)) {
        alert(result.detail.map((item) => item.msg).join("\n"));
      } else {
        alert(result.detail || result.message || "Authentication failed");
      }
    } catch (err) {
      alert("Server not reachable");
    }
  });
}

function setMode(mode) {
  if (!title || !text || !toggle || !nameRow || !authForm) return;

  if (mode === "login") {
    title.textContent = "Log in";
    text.textContent = "No account?";
    toggle.textContent = "Sign up";
    nameRow.classList.remove("active");
    if (firstNameInput) firstNameInput.required = false;
    if (lastNameInput) lastNameInput.required = false;
    authForm.action = "/login";
  } else {
    title.textContent = "Sign up";
    text.textContent = "Already registered?";
    toggle.textContent = "Log in";
    nameRow.classList.add("active");
    if (firstNameInput) firstNameInput.required = true;
    if (lastNameInput) lastNameInput.required = true;
    authForm.action = "/register";
  }
}

setMode("login");

const navButtons = document.querySelectorAll(".nav-btn[data-section]");
const sections = document.querySelectorAll(".content, .content-section");

if (navButtons.length && sections.length) {
  navButtons.forEach((button) => {
    button.addEventListener("click", () => {
      navButtons.forEach((otherButton) => otherButton.classList.remove("active"));
      button.classList.add("active");

      sections.forEach((section) => section.classList.remove("active-section"));
      const targetSection = document.getElementById(button.dataset.section);
      if (targetSection) targetSection.classList.add("active-section");
    });
  });
}

const departmentSelect = document.getElementById("department");
const softwareSelect = document.getElementById("included_software");
const deviceTypeSelect = document.getElementById("device_type");
const operatingSystemSelect = document.getElementById("operating_system");

const presets = {
  it: { dept: "IT", software: "Office 365", device: "Desktop", os: "Windows 11 Pro" },
  hr: { dept: "HR", software: "Office 365", device: "Laptop", os: "Windows 11 Pro" },
  dev: { dept: "IT", software: "Developer Tools", device: "Laptop", os: "Ubuntu 24.04 LTS" }
};

if (departmentSelect && softwareSelect) {
  document.querySelectorAll("[data-preset]").forEach((presetButton) => {
    presetButton.onclick = () => {
      const preset = presets[presetButton.dataset.preset];
      if (!preset) return;
      departmentSelect.value = preset.dept;
      softwareSelect.value = preset.software;
      if (deviceTypeSelect) deviceTypeSelect.value = preset.device;
      if (operatingSystemSelect) operatingSystemSelect.value = preset.os;
    };
  });
}

const confidentialitySelect = document.getElementById("c");
const integritySelect = document.getElementById("i");
const availabilitySelect = document.getElementById("a");
const riskElement = document.getElementById("risk");

if (confidentialitySelect && integritySelect && availabilitySelect && riskElement) {
  const updateRisk = () => {
    const score =
      Number(confidentialitySelect.value) +
      Number(integritySelect.value) +
      Number(availabilitySelect.value);

    if (score <= 4) {
      riskElement.textContent = "Low";
    } else if (score <= 7) {
      riskElement.textContent = "Medium";
    } else {
      riskElement.textContent = "High";
    }
  };

  confidentialitySelect.addEventListener("change", updateRisk);
  integritySelect.addEventListener("change", updateRisk);
  availabilitySelect.addEventListener("change", updateRisk);
  updateRisk();
}
