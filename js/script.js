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

const contactForm = document.getElementById('contact-form');
const contactStatus = document.getElementById('contact-status');

contactForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  const submitButton = contactForm.querySelector('button[type="submit"]');
  const formData = new FormData(contactForm);
  const values = Object.fromEntries(formData.entries());

  submitButton.disabled = true;
  contactStatus.textContent = 'Sending your message…';
  contactStatus.classList.remove('is-error');

  try {
    const response = await fetch('/api/contact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(values)
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || 'Your message could not be sent.');

    contactForm.reset();
    contactStatus.textContent = result.message;
  } catch (error) {
    contactStatus.textContent = error.message === 'Failed to fetch'
      ? 'The message service is unavailable. Please try again later or email me directly.'
      : error.message;
    contactStatus.classList.add('is-error');
  } finally {
    submitButton.disabled = false;
  }
});
