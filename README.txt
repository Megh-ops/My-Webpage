MEGHANA'S PORTFOLIO

FILES
- index.html       Page structure and content
- css/style.css    Layout, colours, responsive styling and animations
- js/script.js     Theme toggle and current year

RUN LOCALLY
1. Keep the folder structure intact.
2. Install Python 3.8 or newer.
3. In a terminal, change into this folder and run: python server.py
4. Open http://localhost:8000 in a modern web browser.
5. No internet connection is needed to view or use the portfolio locally.

BACKEND
- The contact form sends messages to the Python backend.
- Messages are validated and saved in data/messages.sqlite3 (created automatically).
- The database is local to this server; deploy the backend and its persistent database storage together.
- Set PORTFOLIO_DB_PATH to use a different SQLite file location.
- Set PORT to choose the listening port; set PORTFOLIO_HOST=0.0.0.0 when hosting behind a web server.

CUSTOMISE
- Edit text and links in index.html.
- Change colours, spacing and layout in css/style.css.
- Change theme behaviour in js/script.js.

The site uses CSS-generated decorative artwork, so no extra image files are required.
