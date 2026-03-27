const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => Array.from(root.querySelectorAll(selector));

const ui = {
  scene: $("#scene"),
  app: $("#app"),
  glow: $("#cursorGlow"),
  auth: {
    title: $("#authTitle"),
    text: $("#authText"),
    toggle: $("#authToggle"),
    form: $("#authForm"),
    nameRow: $("#nameRow"),
    loginBtn: $("#loginBtn"),
    signupBtn: $("#signupBtn")
  }
};

const authInputs = {
  firstName: ui.auth.form?.querySelector('input[name="first_name"]'),
  lastName: ui.auth.form?.querySelector('input[name="last_name"]'),
  email: ui.auth.form?.querySelector('input[name="email"]'),
  password: ui.auth.form?.querySelector('input[name="password"]')
};

const setAuthMode = (mode) => {
  const { title, text, toggle, nameRow, form } = ui.auth;
  if (!title || !text || !toggle || !nameRow || !form) return;

  const isLogin = mode === "login";

  title.textContent = isLogin ? "Log in" : "Sign up";
  text.textContent = isLogin ? "No account?" : "Already registered?";
  toggle.textContent = isLogin ? "Sign up" : "Log in";
  nameRow.classList.toggle("active", !isLogin);
  form.action = isLogin ? "/login" : "/register";

  if (authInputs.firstName) authInputs.firstName.required = !isLogin;
  if (authInputs.lastName) authInputs.lastName.required = !isLogin;
};

const getAuthPayload = (isSignup) => {
  const base = {
    email: authInputs.email?.value.trim(),
    password: authInputs.password?.value
  };

  if (!isSignup) return base;

  return {
    ...base,
    name: authInputs.firstName?.value.trim(),
    surname: authInputs.lastName?.value.trim()
  };
};

const isValidAuthPayload = (payload, isSignup) => {
  if (!payload.email || !payload.password) return false;
  if (!isSignup) return true;
  return Boolean(payload.name && payload.surname);
};

const submitAuth = async (event) => {
  event.preventDefault();

  const isSignup = ui.auth.title?.textContent === "Sign up";
  const payload = getAuthPayload(isSignup);

  if (!isValidAuthPayload(payload, isSignup)) {
    alert("Please fill in all required fields.");
    return;
  }

  try {
    const response = await fetch(isSignup ? "/register" : "/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify(payload)
    });

    const result = await response.json().catch(() => ({}));

    if (!response.ok) {
      const detail = Array.isArray(result?.detail)
        ? result.detail.map((item) => item.msg).join("\n")
        : result.detail || result.message || "Authentication failed";
      alert(detail);
      return;
    }

    if (!ui.scene || !ui.app) return;
    ui.scene.style.opacity = "0";
    setTimeout(() => {
      ui.scene.style.display = "none";
      ui.app.classList.add("active");
    }, 500);
  } catch {
    alert("Server not reachable");
  }
};

const initGlow = () => {
  if (!ui.glow) return;
  document.addEventListener("mousemove", (event) => {
    ui.glow.style.left = `${event.clientX}px`;
    ui.glow.style.top = `${event.clientY}px`;
  });
};

const initAuth = () => {
  const { loginBtn, signupBtn, toggle, title, form, scene } = {
    ...ui.auth,
    scene: ui.scene
  };

  if (loginBtn && scene) {
    loginBtn.addEventListener("click", () => {
      scene.classList.add("auth-open");
      setAuthMode("login");
    });
  }

  if (signupBtn && scene) {
    signupBtn.addEventListener("click", () => {
      scene.classList.add("auth-open");
      setAuthMode("signup");
    });
  }

  if (toggle && title) {
    toggle.addEventListener("click", (event) => {
      event.preventDefault();
      setAuthMode(title.textContent === "Log in" ? "signup" : "login");
    });
  }

  if (form) form.addEventListener("submit", submitAuth);
  setAuthMode("login");
};

const initNavigation = () => {
  const navButtons = $$(".nav-btn[data-section]");
  const sections = $$(".content, .content-section");

  if (!navButtons.length || !sections.length) return;

  navButtons.forEach((button) => {
    button.addEventListener("click", () => {
      navButtons.forEach((item) => item.classList.remove("active"));
      sections.forEach((section) => section.classList.remove("active-section"));

      button.classList.add("active");
      const target = $(`#${button.dataset.section}`);
      if (target) target.classList.add("active-section");
    });
  });
};

const initPresets = () => {
  const department = $("#department");
  const software = $("#included_software");
  const deviceType = $("#device_type");
  const operatingSystem = $("#operating_system");

  if (!department || !software) return;

  const presets = {
    it: { dept: "IT", software: "Office 365", device: "Desktop", os: "Windows 11 Pro" },
    hr: { dept: "HR", software: "Office 365", device: "Laptop", os: "Windows 11 Pro" },
    dev: { dept: "IT", software: "Developer Tools", device: "Laptop", os: "Ubuntu 24.04 LTS" }
  };

  $$('[data-preset]').forEach((button) => {
    button.addEventListener("click", () => {
      const preset = presets[button.dataset.preset];
      if (!preset) return;

      department.value = preset.dept;
      software.value = preset.software;
      if (deviceType) deviceType.value = preset.device;
      if (operatingSystem) operatingSystem.value = preset.os;
    });
  });
};

const initRiskCalculator = () => {
  const confidentiality = $("#c");
  const integrity = $("#i");
  const availability = $("#a");
  const risk = $("#risk");

  if (!confidentiality || !integrity || !availability || !risk) return;

  const updateRisk = () => {
    const score = Number(confidentiality.value) + Number(integrity.value) + Number(availability.value);

    if (score <= 4) risk.textContent = "Low";
    else if (score <= 7) risk.textContent = "Medium";
    else risk.textContent = "High";
  };

  [confidentiality, integrity, availability].forEach((field) => {
    field.addEventListener("change", updateRisk);
  });

  updateRisk();
};

initGlow();
initAuth();
initNavigation();
initPresets();
initRiskCalculator();