/* ═══════════════════════════════════════════════════════
   Le Secret de la Bibliothèque Interdite
   JavaScript côté client — timer temps réel
   ═══════════════════════════════════════════════════════ */

(function () {
  "use strict";

  // Timer côté client (synchronisé avec le serveur toutes les 30s)
  let timeRemaining = window.GAME_TIME_REMAINING || 0;
  const timerEl = document.getElementById("timer-value");
  const timerContainer = document.getElementById("timer");

  function formatTime(sec) {
    const m = Math.floor(sec / 60);
    const s = sec % 60;
    return String(m).padStart(2, "0") + ":" + String(s).padStart(2, "0");
  }

  function updateTimerDisplay() {
    if (!timerEl) return;
    timerEl.textContent = formatTime(timeRemaining);

    if (timerContainer) {
      timerContainer.classList.remove("warning", "critical");
      if (timeRemaining <= 300) {
        timerContainer.classList.add("critical");
      } else if (timeRemaining <= 600) {
        timerContainer.classList.add("warning");
      }
    }
  }

  function tick() {
    if (timeRemaining <= 0) {
      // Temps écoulé → redirection vers la défaite
      window.location.href = "/defeat";
      return;
    }
    timeRemaining--;
    updateTimerDisplay();

    // Synchronisation avec le serveur toutes les 30 secondes
    if (timeRemaining % 30 === 0) {
      fetch("/api/time")
        .then(function (r) { return r.json(); })
        .then(function (data) {
          if (data.defeat) {
            window.location.href = "/defeat";
            return;
          }
          timeRemaining = data.time_remaining;
          updateTimerDisplay();
        })
        .catch(function () { /* ignore les erreurs réseau */ });
    }
  }

  // Démarre le timer seulement si la partie est commencée
  if (window.GAME_STARTED && timeRemaining > 0) {
    updateTimerDisplay();
    setInterval(tick, 1000);
  }

  // Auto-submit du cadenas quand 4 chiffres sont saisis
  const combinationForm = document.getElementById("combination-form");
  if (combinationForm) {
    const inputs = combinationForm.querySelectorAll("input[data-combo]");
    if (inputs.length === 4) {
      inputs.forEach(function (input, idx) {
        input.addEventListener("input", function () {
          input.value = input.value.replace(/[^0-9]/g, "").slice(0, 1);
          if (input.value && idx < inputs.length - 1) {
            inputs[idx + 1].focus();
          }
          // Vérifie si tous les champs sont remplis
          const code = Array.from(inputs).map(function (i) { return i.value; }).join("");
          if (code.length === 4) {
            // Soumet automatiquement
            setTimeout(function () { combinationForm.submit(); }, 200);
          }
        });

        input.addEventListener("keydown", function (e) {
          if (e.key === "Backspace" && !input.value && idx > 0) {
            inputs[idx - 1].focus();
          }
        });
      });
    }
  }
})();
