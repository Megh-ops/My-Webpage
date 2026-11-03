const body = document.body;
const themeButton = document.querySelector('.theme-toggle');
const themeIcon = document.querySelector('.theme-icon');
const themeLabel = document.querySelector('.theme-label');

function setTheme(theme) {
  const isLight = theme === 'light';
  body.classList.toggle('light-mode', isLight);
  body.classList.toggle('dark-mode', !isLight);
  themeIcon.textContent = isLight ? '☾' : '☼';
  themeLabel.textContent = isLight ? 'Dark mode' : 'Light mode';
  themeButton.setAttribute('aria-label', isLight ? 'Switch to dark theme' : 'Switch to light theme');
  document.querySelector('meta[name="theme-color"]').content = isLight ? '#fff8fc' : '#100d25';
}

themeButton.addEventListener('click', () => {
  const nextTheme = body.classList.contains('dark-mode') ? 'light' : 'dark';
  setTheme(nextTheme);
  try { localStorage.setItem('portfolio-theme', nextTheme); } catch (_) {}
});

try {
  const savedTheme = localStorage.getItem('portfolio-theme');
  if (savedTheme === 'light' || savedTheme === 'dark') setTheme(savedTheme);
} catch (_) {}

document.getElementById('year').textContent = new Date().getFullYear();
