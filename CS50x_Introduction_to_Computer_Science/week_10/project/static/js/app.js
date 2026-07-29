document.addEventListener('DOMContentLoaded', () => {
  let timerMode = 'work';
  let workDurationMinutes = 25;
  let shortDurationMinutes = 5;
  let timerDuration = workDurationMinutes * 60;
  let timerTimeLeft = timerDuration;
  let timerInterval = null;
  let isTimerRunning = false;

  let showSecondsOnClock = false;

  function updateLiveClock() {
    const clockEl = document.getElementById('live-clock-digits');
    if (!clockEl) return;
    const now = new Date();
    const opts = {
      hour: '2-digit',
      minute: '2-digit',
      hour12: true
    };
    if (showSecondsOnClock) opts.second = '2-digit';
    clockEl.textContent = now.toLocaleTimeString('en-US', opts);
  }

  updateLiveClock();
  setInterval(updateLiveClock, 1000);

  function animateBounce(element, scaleAmount = 0.92) {
    if (!element) return;
    anime({
      targets: element,
      scale: [scaleAmount, 1],
      duration: 450,
      easing: 'easeOutElastic(1, .5)'
    });
  }

  function fetchStats() {
    fetch('/api/stats')
      .then(res => res.json())
      .then(data => {
        const compEl = document.getElementById('stat-completed-tasks');
        const streakEl = document.getElementById('stat-max-streak');
        if (compEl) compEl.textContent = `${data.goals.completed}/${data.goals.total}`;
        if (streakEl) streakEl.textContent = `${data.habits.max_streak} Days`;
      })
      .catch(() => {});
  }

  function fetchGoals() {
    fetch('/api/goals')
      .then(res => res.json())
      .then(goals => {
        renderGoals(goals);
        fetchStats();
      })
      .catch(() => {});
  }

  function renderGoals(goals) {
    const dashList = document.getElementById('dash-goals-list');
    if (!dashList) return;

    dashList.innerHTML = goals.map(g => `
      <div class="task-row ${g.completed ? 'completed' : ''}" data-id="${g.id}">
        <div style="display: flex; align-items: center; gap: 0.75rem;">
          <div class="glass-checkbox" data-id="${g.id}" data-completed="${g.completed}">
            ${g.completed ? '✓' : ''}
          </div>
          <span class="task-label">${escapeHTML(g.title)}</span>
        </div>
        <button class="mono-btn mono-btn-sm delete-goal-btn" data-id="${g.id}">✕</button>
      </div>
    `).join('');
  }

  document.addEventListener('click', (e) => {
    const chk = e.target.closest('.glass-checkbox');
    if (chk) {
      animateBounce(chk, 1.25);
      const goalId = chk.getAttribute('data-id');
      const isDone = chk.getAttribute('data-completed') === '1' || chk.getAttribute('data-completed') === 'true';
      const nextState = !isDone;

      fetch(`/api/goals/${goalId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ completed: nextState })
      }).then(() => fetchGoals());
    }

    const delBtn = e.target.closest('.delete-goal-btn');
    if (delBtn) {
      animateBounce(delBtn, 0.85);
      const goalId = delBtn.getAttribute('data-id');
      fetch(`/api/goals/${goalId}`, { method: 'DELETE' }).then(() => fetchGoals());
    }
  });

  const dashGoalForm = document.getElementById('dash-goal-form');
  if (dashGoalForm) {
    dashGoalForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const input = document.getElementById('dash-goal-input');
      const title = input.value.trim();
      if (!title) return;

      fetch('/api/goals', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, category: 'General' })
      }).then(() => { input.value = ''; fetchGoals(); });
    });
  }

  function fetchHabits() {
    fetch('/api/habits')
      .then(res => res.json())
      .then(habits => {
        renderHabits(habits);
        fetchStats();
      })
      .catch(() => {});
  }

  function renderHabits(habits) {
    const dashList = document.getElementById('dash-habits-list');
    if (!dashList) return;

    dashList.innerHTML = habits.map(h => `
      <div class="task-row" data-id="${h.id}">
        <div style="flex: 1;">
          <div class="task-label">${escapeHTML(h.title)}</div>
          <div style="font-size: 0.8rem; font-weight: 700; opacity: 0.6; margin-top: 0.1rem;">
            🔥 ${h.streak} Day Streak
          </div>
        </div>
        <div style="display: flex; gap: 0.4rem;">
          <button class="mono-btn mono-btn-sm habit-done-btn" data-id="${h.id}">+1</button>
          <button class="mono-btn mono-btn-sm delete-habit-btn" data-id="${h.id}">✕</button>
        </div>
      </div>
    `).join('');
  }

  document.addEventListener('click', (e) => {
    const doneBtn = e.target.closest('.habit-done-btn');
    if (doneBtn) {
      animateBounce(doneBtn, 0.88);
      const habitId = doneBtn.getAttribute('data-id');

      fetch(`/api/habits/${habitId}/increment`, { method: 'POST' })
        .then(() => fetchHabits());
    }

    const delHabitBtn = e.target.closest('.delete-habit-btn');
    if (delHabitBtn) {
      animateBounce(delHabitBtn, 0.85);
      const habitId = delHabitBtn.getAttribute('data-id');
      fetch(`/api/habits/${habitId}`, { method: 'DELETE' }).then(() => fetchHabits());
    }
  });

  const dashHabitForm = document.getElementById('dash-habit-form');
  if (dashHabitForm) {
    dashHabitForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const input = document.getElementById('dash-habit-input');
      const title = input.value.trim();
      if (!title) return;

      fetch('/api/habits', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, target_days: 30 })
      }).then(() => { input.value = ''; fetchHabits(); });
    });
  }

  const timerDigits = document.getElementById('timer-digits');
  const timerProgressRing = document.getElementById('timer-progress-ring');
  const timerStartBtn = document.getElementById('timer-start');
  const timerPauseBtn = document.getElementById('timer-pause');
  const timerResetBtn = document.getElementById('timer-reset');
  const timerTabBtns = document.querySelectorAll('.timer-tab-btn');
  const customToggleBtn = document.getElementById('custom-toggle-btn');
  const customTimerBox = document.getElementById('custom-timer-box');
  const customHoursInput = document.getElementById('custom-hours-input');
  const customMinutesInput = document.getElementById('custom-minutes-input');
  const customSecondsInput = document.getElementById('custom-seconds-input');
  const applyCustomTimeBtn = document.getElementById('apply-custom-time');

  const settingsToggleBtn = document.getElementById('settings-toggle-btn');
  const settingsModal = document.getElementById('settings-modal');
  const closeSettingsBtn = document.getElementById('close-settings-btn');
  const saveSettingsBtn = document.getElementById('save-settings-btn');
  const resetDataBtn = document.getElementById('reset-data-btn');
  const settingWorkTime = document.getElementById('setting-work-time');
  const settingShortTime = document.getElementById('setting-short-time');
  const toggleShowSeconds = document.getElementById('toggle-show-seconds');

  if (settingsToggleBtn && settingsModal) {
    settingsToggleBtn.addEventListener('click', () => {
      animateBounce(settingsToggleBtn, 0.9);
      settingsModal.style.display = 'flex';
      const modalContent = settingsModal.querySelector('.modal-card');
      if (modalContent) {
        anime({
          targets: modalContent,
          scale: [0.8, 1],
          opacity: [0, 1],
          duration: 350,
          easing: 'easeOutBack'
        });
      }
    });
  }

  if (closeSettingsBtn && settingsModal) {
    closeSettingsBtn.addEventListener('click', () => {
      animateBounce(closeSettingsBtn, 0.9);
      settingsModal.style.display = 'none';
    });
  }

  if (saveSettingsBtn && settingsModal) {
    saveSettingsBtn.addEventListener('click', () => {
      animateBounce(saveSettingsBtn, 0.9);
      const wVal = parseInt(settingWorkTime.value) || 25;
      const sVal = parseInt(settingShortTime.value) || 5;
      workDurationMinutes = Math.max(1, Math.min(180, wVal));
      shortDurationMinutes = Math.max(1, Math.min(60, sVal));
      
      if (toggleShowSeconds) showSecondsOnClock = toggleShowSeconds.checked;
      
      updateLiveClock();

      const workBtn = document.querySelector('.timer-tab-btn[data-mode="work"]');
      const shortBtn = document.querySelector('.timer-tab-btn[data-mode="short"]');
      if (workBtn) workBtn.textContent = `${workDurationMinutes}m Focus`;
      if (shortBtn) shortBtn.textContent = `${shortDurationMinutes}m Break`;
      
      settingsModal.style.display = 'none';
      setTimerMode('work');
    });
  }

  if (resetDataBtn) {
    resetDataBtn.addEventListener('click', () => {
      animateBounce(resetDataBtn, 0.9);
      if (confirm('Are you sure you want to reset all tasks and habits?')) {
        fetch('/api/reset', { method: 'POST' })
          .then(() => {
            fetchGoals();
            fetchHabits();
            if (settingsModal) settingsModal.style.display = 'none';
          });
      }
    });
  }

  function updateTimerButtons() {
    if (isTimerRunning) {
      if (timerStartBtn) timerStartBtn.style.display = 'none';
      if (timerPauseBtn) {
        timerPauseBtn.style.display = 'inline-flex';
        animateBounce(timerPauseBtn, 0.9);
      }
    } else {
      if (timerPauseBtn) timerPauseBtn.style.display = 'none';
      if (timerStartBtn) {
        timerStartBtn.style.display = 'inline-flex';
        animateBounce(timerStartBtn, 0.9);
      }
    }
  }

  function updateTimerDisplay() {
    const hrs = Math.floor(timerTimeLeft / 3600);
    const mins = Math.floor((timerTimeLeft % 3600) / 60);
    const secs = timerTimeLeft % 60;

    if (timerDigits) {
      if (hrs > 0 || timerDuration >= 3600) {
        timerDigits.textContent = `${String(hrs).padStart(2, '0')}:${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
        timerDigits.style.fontSize = '3.6rem';
      } else {
        timerDigits.textContent = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
        timerDigits.style.fontSize = '4.8rem';
      }
    }

    if (timerProgressRing) {
      const offset = 848 * (1 - timerTimeLeft / timerDuration);
      timerProgressRing.style.strokeDashoffset = offset;
    }
  }

  if (customToggleBtn && customTimerBox) {
    customToggleBtn.addEventListener('click', () => {
      animateBounce(customToggleBtn, 0.9);
      const isHidden = customTimerBox.style.display === 'none';
      if (isHidden) {
        customTimerBox.style.display = 'flex';
        anime({
          targets: customTimerBox,
          scale: [0.85, 1],
          opacity: [0, 1],
          translateY: [-10, 0],
          duration: 400,
          easing: 'easeOutBack'
        });
        if (customMinutesInput) customMinutesInput.focus();
      } else {
        customTimerBox.style.display = 'none';
      }
    });
  }

  function setCustomTimer() {
    const h = parseInt(customHoursInput ? customHoursInput.value : 0) || 0;
    const m = parseInt(customMinutesInput ? customMinutesInput.value : 0) || 0;
    const s = parseInt(customSecondsInput ? customSecondsInput.value : 0) || 0;
    
    let totalSecs = (h * 3600) + (m * 60) + s;
    if (totalSecs <= 0) totalSecs = 60;

    timerDuration = totalSecs;
    timerTimeLeft = timerDuration;
    isTimerRunning = false;
    clearInterval(timerInterval);
    updateTimerButtons();
    timerTabBtns.forEach(btn => {
      if (btn.id === 'custom-toggle-btn') btn.classList.add('active');
      else btn.classList.remove('active');
    });
    updateTimerDisplay();
  }

  if (applyCustomTimeBtn) {
    applyCustomTimeBtn.addEventListener('click', () => {
      animateBounce(applyCustomTimeBtn, 0.9);
      setCustomTimer();
    });
  }

  [customHoursInput, customMinutesInput, customSecondsInput].forEach(inp => {
    if (inp) {
      inp.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
          e.preventDefault();
          setCustomTimer();
        }
      });
    }
  });

  function setTimerMode(mode) {
    timerMode = mode;
    isTimerRunning = false;
    clearInterval(timerInterval);
    updateTimerButtons();

    if (customTimerBox) customTimerBox.style.display = 'none';

    timerTabBtns.forEach(btn => {
      if (btn.getAttribute('data-mode') === mode) {
        btn.classList.add('active');
        animateBounce(btn, 0.9);
      } else {
        btn.classList.remove('active');
      }
    });

    if (mode === 'work') timerDuration = workDurationMinutes * 60;
    else if (mode === 'short') timerDuration = shortDurationMinutes * 60;
    else if (mode === 'long') timerDuration = 15 * 60;

    timerTimeLeft = timerDuration;
    updateTimerDisplay();
  }

  timerTabBtns.forEach(btn => {
    if (btn.hasAttribute('data-mode')) {
      btn.addEventListener('click', () => setTimerMode(btn.getAttribute('data-mode')));
    }
  });

  if (timerStartBtn) {
    timerStartBtn.addEventListener('click', () => {
      if (isTimerRunning) return;
      isTimerRunning = true;
      updateTimerButtons();

      timerInterval = setInterval(() => {
        if (timerTimeLeft > 0) {
          timerTimeLeft--;
          updateTimerDisplay();
        } else {
          clearInterval(timerInterval);
          isTimerRunning = false;
          updateTimerButtons();
          if (timerDigits) animateBounce(timerDigits, 1.2);
          alert("🎉 Session finished!");
          setTimerMode('short');
        }
      }, 1000);
    });
  }

  if (timerPauseBtn) {
    timerPauseBtn.addEventListener('click', () => {
      isTimerRunning = false;
      clearInterval(timerInterval);
      updateTimerButtons();
    });
  }

  if (timerResetBtn) {
    timerResetBtn.addEventListener('click', () => {
      isTimerRunning = false;
      clearInterval(timerInterval);
      setTimerMode(timerMode);
    });
  }

  const dateEl = document.getElementById('current-date-text');
  if (dateEl) {
    const now = new Date();
    dateEl.textContent = now.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' });
  }

  function escapeHTML(str) {
    if (!str) return '';
    return str.replace(/[&<>"']/g, (m) => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    })[m]);
  }

  setTimerMode('work');
  fetchGoals();
  fetchHabits();
});
