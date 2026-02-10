const scene = document.getElementById("scene");
const app = document.getElementById("app");
const glow = document.getElementById("cursorGlow");

document.addEventListener("mousemove", e=>{
  glow.style.left=e.clientX+"px";
  glow.style.top=e.clientY+"px";
});

// AUTH
const loginBtn = document.getElementById("loginBtn");
const signupBtn = document.getElementById("signupBtn");
const authForm = document.getElementById("authForm");
const nameRow = document.getElementById("nameRow");
const title = document.getElementById("authTitle");
const toggle = document.getElementById("authToggle");

loginBtn.onclick=()=>{scene.classList.add("auth-open");setMode("login")}
signupBtn.onclick=()=>{scene.classList.add("auth-open");setMode("signup")}

toggle.onclick=e=>{
  e.preventDefault();
  setMode(title.textContent==="Log in"?"signup":"login");
}

function setMode(mode){
  if(mode==="signup"){
    authForm.action="/auth/signup";
    title.textContent="Sign up";
    nameRow.classList.add("active");
  }else{
    authForm.action="/auth/login";
    title.textContent="Log in";
    nameRow.classList.remove("active");
  }
}

// UMAR BYPASS
authForm.addEventListener("submit",e=>{
  const fn = authForm.first_name?.value;
  const ln = authForm.last_name?.value;

  if(fn==="UMAR" && ln==="UMAR"){
    e.preventDefault();
    enterApp("admin");
  }
});

// ENTER APP
function enterApp(role){
  scene.style.display="none";
  app.classList.add("active");
  applyRole(role);
}

// ROLES
function applyRole(role){
  document.getElementById("roleBadge").textContent=role.toUpperCase();
  document.querySelectorAll(".technician-only").forEach(el=>{
    el.style.display = (role==="technician"||role==="admin")?"block":"none";
  });
}

// NAV
document.querySelectorAll(".nav-btn").forEach(btn=>{
  btn.onclick=()=>{
    document.querySelectorAll(".nav-btn").forEach(b=>b.classList.remove("active"));
    btn.classList.add("active");
    document.querySelectorAll(".content").forEach(c=>c.classList.remove("active-section"));
    document.getElementById(btn.dataset.section).classList.add("active-section");
  }
});

// SECURITY LOGIC
["c","i","a"].forEach(id=>{
  document.getElementById(id)?.addEventListener("change",calcRisk);
});
function calcRisk(){
  const max = Math.max(+c.value,+i.value,+a.value);
  risk.textContent = max===3?"High":max===2?"Medium":"Low";
}
