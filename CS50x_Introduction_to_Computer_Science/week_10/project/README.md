# FOCUS SUITE
#### Video Demo: <To be Added>
#### Description:

Focus Suite is a minimal, single-page, non-scrolling task management and focus productivity application built with Python (Flask), SQLite, HTML5, CSS3, and modern vanilla JavaScript powered by `anime.js`. Designed explicitly to combat digital distractions, Focus Suite replaces bloated, complex dashboard interfaces with a single, highly refined viewport workspace that unifies an adaptable Pomodoro/custom focus timer, priority goal management, and daily habit tracking.

The application addresses a common problem in modern productivity tools: visual clutter and over-engineering. Many popular task managers overwhelm users with unnecessary sub-menus, heavy animations, nested project trees, and noisy notifications. Focus Suite strips away all extraneous elements, offering a dark AMOLED aesthetic (`#070709` and `#121316`), high-contrast off-white typography, zero scrolling requirements on desktop displays, and tactile micro-interactions that make tracking progress intuitive and satisfying.

---

### Key Features & Design Philosophy

1. **Single-Page Viewport Layout**:
   The entire application is constrained to `100vh` without page scrolling on desktop viewports. Everything needed for a productive session—the live wall clock, focus timer, task manager, and habit tracker—is visible simultaneously in a balanced dual-column grid.

2. **Versatile Focus Timer**:
   Users can toggle between preset Pomodoro sessions (25-minute focus, 5-minute break, 15-minute break) or launch a hidden custom duration drawer. Unlike typical timer apps limited to minute presets, Focus Suite supports exact custom hours, minutes, and seconds input. The timer display dynamically resizes between `MM:SS` for short sessions and `HH:MM:SS` for extended deep-work sessions, surrounded by a custom SVG progress ring.

3. **Dynamic Control System**:
   The timer controls feature state-aware button visibility: a vibrant emerald green Start button (`▶ Start`) automatically transitions into a crimson Red Pause button (`⏸ Pause`) upon activation, accompanied by a neutral Reset button (`↺ Reset`).

4. **Priority Tasks & Daily Habit Tracking**:
   The right column provides quick-add forms and real-time completion toggles for single-day tasks and recurring habits. Completing a task instantly updates completion ratios (`X/Y`), while habit completion increments streak counters with rapid `+1` actions backed by persistent SQLite storage.

5. **Live Digital Clock & Date**:
   A real-time 12-hour wall clock sits centered in the top navigation bar alongside the current day and date. An optional "Show Clock Seconds" toggle in the Settings modal allows users to customize their visual environment for either maximum calm or exact timekeeping.

6. **Responsive Design**:
   While desktop viewports maintain a strict single-screen layout, media queries automatically adapt the grid on mobile and tablet devices (`<900px`) into a fluid, single-column scrollable interface with enlarged touch targets.

---

### Detailed File Breakdown

- **`app.py`**:
  The backend server written in Python using Flask. It initializes and manages an SQLite database (`focusflow.db`), defining tables for `goals`, `habits`, and `settings`. It exposes structured REST API endpoints:
  - `GET /`: Renders the single-page application (`templates/index.html`).
  - `GET, POST /api/goals`: Retrieves all active/completed tasks or creates new ones.
  - `PUT, DELETE /api/goals/<id>`: Updates completion states or removes goals.
  - `GET, POST /api/habits`: Lists habits or inserts new habit entries.
  - `POST /api/habits/<id>/increment`: Increments streak counts and records completion dates.
  - `DELETE /api/habits/<id>`: Deletes specific habits.
  - `GET /api/stats`: Computes live aggregate statistics for task progress and streak records.
  - `POST /api/reset`: Offers a clean database reset endpoint for clearing workspace data.

- **`templates/index.html`**:
  The core structural markup of the application. Built using HTML5 semantic elements (`header`, `main`, `section`, `form`), it structures the top navigation bar, the timer hero section, the dual widget section (tasks and habits), and a backdrop-blurred Settings modal dialog. SVG vector icons are used exclusively for settings and modal dismissal, avoiding heavy font libraries or emojis.

- **`static/css/style.css`**:
  The complete styling system written in pure CSS. It utilizes root CSS custom properties (`--bg-main`, `--bg-card`, `--border-main`, `--btn-primary-bg`) to maintain a dark AMOLED theme. It includes zero-scrollbar list utilities, SVG circle progress ring dash-array math (`stroke-dasharray: 848`), custom toggle switch sliders, glassmorphism modal overlays (`backdrop-filter: blur(12px)`), and media queries for responsive mobile layouts.

- **`static/js/app.js`**:
  The client-side interactivity layer written in modular JavaScript. It communicates asynchronously with `app.py` via the `fetch` API, manages live countdown intervals, handles custom duration logic across hours/minutes/seconds, renders task/habit DOM nodes dynamically, toggles button states, and triggers spring micro-animations using `anime.js`.

- **`static/js/anime.min.js`**:
  A lightweight JavaScript animation library used to deliver elastic bounce micro-interactions (`easeOutElastic`, `easeOutBack`) on button presses, task checkbox checks, and modal dialog openings without introducing frame drops or DOM lag.

---

### Design Decisions & Trade-Offs

During development, several design choices were debated:

1. **Monochrome AMOLED vs. Colorful UI**:
   Early iterations included colorful gradients and background particles. However, feedback during testing highlighted that colorful visuals distracted from intense focus. We transitioned to a stark, AMOLED black aesthetic (`#070709`) with high contrast white elements and selective green (`#10B981`) and red (`#EF4444`) accents for active controls only.

2. **Single-Page Viewport vs. Multi-Tab Dashboard**:
   A multi-tab design with separate routes for tasks, habits, and stats was initially considered. We chose a single-page non-scrolling layout to keep all relevant information visible simultaneously, eliminating navigation friction during study or work sessions.

3. **Pure SQLite & Flask vs. Frontend Frameworks (React/Vue)**:
   To keep the codebase fast, lightweight, and easily maintainable without complex build steps or node_modules dependencies, we implemented vanilla JavaScript with Flask and SQLite. This delivers instant page load times and minimal memory footprint.

---

### How to Run Locally

1. Ensure Python 3 and Flask are installed:
   ```bash
   pip install flask
   ```
2. Navigate to the project directory:
   ```bash
   cd focusflow
   ```
3. Run the Flask application:
   ```bash
   python3 app.py
   ```
4. Open your web browser and navigate to `http://127.0.0.1:5000`.

---

### AI Assistance & Citations

AI coding assistance (Google Antigravity / Gemini) was utilized during the development of this project to assist with refactoring CSS layouts, optimizing Flask REST API routes, and tuning `anime.js` spring easing parameters. All core architecture, database schemas, styling guidelines, and feature logic were designed, reviewed, and finalized by the author in accordance with CS50's Academic Honesty guidelines.
