const body = document.body;
const themeToggle = document.getElementById("themeToggle");
const savedTheme = localStorage.getItem("theme") || "dark";
body.classList.add(`theme-${savedTheme}`);
themeToggle.checked = savedTheme === "dark";
themeToggle.addEventListener("change", () => {
  if (themeToggle.checked) {
    body.classList.add("theme-dark");
    body.classList.remove("theme-light");
    localStorage.setItem("theme", "dark");
  } else {
    body.classList.add("theme-light");
    body.classList.remove("theme-dark");
    localStorage.setItem("theme", "light");
  }
});
