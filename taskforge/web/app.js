const API_BASE = "";

const qs = (sel) => document.querySelector(sel);
const qsa = (sel) => Array.from(document.querySelectorAll(sel));

function showStatus(element, message, type = "") {
  if (!element) return;
  element.textContent = message;
  element.className = `form-status ${type}`.trim();
  if (message) {
    setTimeout(() => {
      element.textContent = "";
      element.className = "form-status";
    }, 3500);
  }
}

async function request(url, options = {}) {
  const finalUrl = `${API_BASE}${url}`;
  const config = {
    headers: { "Content-Type": "application/json" },
    ...options,
  };
  if (options.body && typeof options.body !== "string") {
    config.body = JSON.stringify(options.body);
  }

  const res = await fetch(finalUrl, config);
  if (!res.ok) {
    let detail = res.statusText;
    try {
      const data = await res.json();
      detail = data.detail || data.message || JSON.stringify(data);
    } catch (error) {
      /* ignore JSON errors */
    }
    throw new Error(detail || `İstek başarısız (${res.status})`);
  }
  if (res.status === 204) {
    return null;
  }
  return res.json();
}

async function loadActivities() {
  const select = qs("#entry-activity");
  select.innerHTML = "";
  try {
    const items = await request("/api/activities");
    if (!items.length) {
      const opt = document.createElement("option");
      opt.value = "";
      opt.textContent = "Önce aktivite oluştur";
      select.append(opt);
      select.disabled = true;
      return;
    }
    select.disabled = false;
    for (const item of items) {
      const opt = document.createElement("option");
      opt.value = item.name;
      opt.textContent = `${item.name} (${item.points_per_10_min})`;
      opt.dataset.category = item.category || "";
      select.append(opt);
    }
  } catch (error) {
    console.error("Aktiviteler alınamadı", error);
  }
}

async function loadEntries() {
  const tbody = qs("#entries-table tbody");
  const count = qs("#entries-count");
  tbody.innerHTML = "";
  try {
    const entries = await request("/api/entries");
    count.textContent = entries.length;
    for (const entry of entries) {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${entry.activity}</td>
        <td>${entry.duration_min} dk</td>
        <td>${entry.score_delta}</td>
        <td>${entry.note || ""}</td>
        <td>${(entry.tags || []).join(", ")}</td>
        <td>${new Date(entry.started_at).toLocaleString()}</td>
      `;
      tbody.append(tr);
    }
  } catch (error) {
    count.textContent = "0";
    console.error("Kayıtlar yüklenemedi", error);
  }
}

async function loadSummary() {
  try {
    const summary = await request("/api/daily-summary");
    qs("#summary-date").textContent = summary.date;
    qs("#summary-minutes").textContent = summary.total_minutes;
    qs("#summary-score").textContent = summary.total_score;
  } catch (error) {
    console.error("Özet alınamadı", error);
  }
}

async function loadReminders() {
  const list = qs("#reminders-list");
  const count = qs("#reminders-count");
  list.innerHTML = "";
  try {
    const reminders = await request("/api/reminders");
    const pending = reminders.filter((item) => !item.acknowledged);
    count.textContent = pending.length;
    if (!pending.length) {
      const li = document.createElement("li");
      li.textContent = "Henüz hatırlatma yok. Çalışmaya devam!";
      list.append(li);
      return;
    }

    for (const reminder of pending) {
      const li = document.createElement("li");
      li.className = "reminder-item";
      const span = document.createElement("span");
      span.textContent = `${new Date(reminder.created_at).toLocaleTimeString()} · ${reminder.message}`;
      const btn = document.createElement("button");
      btn.textContent = "Tamam";
      btn.addEventListener("click", async () => {
        btn.disabled = true;
        try {
          await request(`/api/reminders/${reminder.id}/ack`, { method: "POST" });
          await loadReminders();
        } catch (error) {
          console.error("Hatırlatma kapatılamadı", error);
          btn.disabled = false;
        }
      });
      li.append(span, btn);
      list.append(li);
    }
  } catch (error) {
    count.textContent = "0";
    console.error("Hatırlatmalar alınamadı", error);
  }
}

async function handleActivitySubmit(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const status = qs("#activity-status");
  const payload = {
    name: form.name.value.trim(),
    category: form.category.value.trim() || null,
    points_per_10_min: Number(form.points_per_10_min.value),
  };

  if (!payload.name || Number.isNaN(payload.points_per_10_min)) {
    showStatus(status, "Alanları doğru doldur", "error");
    return;
  }

  try {
    showStatus(status, "Kaydediliyor...");
    await request("/api/activities", { method: "POST", body: payload });
    showStatus(status, "Aktivite kaydedildi", "success");
    form.reset();
    await loadActivities();
  } catch (error) {
    showStatus(status, error.message, "error");
  }
}

async function handleEntrySubmit(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const status = qs("#entry-status");
  const activitySelect = qs("#entry-activity");
  const selectedOption = activitySelect.options[activitySelect.selectedIndex];
  const tagsValue = form.tags.value.trim();
  const payload = {
    activity_name: form.activity_name.value,
    duration_min: Number(form.duration_min.value),
    note: form.note.value.trim() || null,
    tags: tagsValue ? tagsValue.split(",").map((tag) => tag.trim()).filter(Boolean) : [],
    category: selectedOption?.dataset?.category || null,
  };

  if (!payload.activity_name || Number.isNaN(payload.duration_min) || payload.duration_min <= 0) {
    showStatus(status, "Aktivite ve süre gerekli", "error");
    return;
  }

  try {
    showStatus(status, "Kaydediliyor...");
    await request("/api/entries", { method: "POST", body: payload });
    showStatus(status, "Kayıt eklendi", "success");
    form.reset();
    await Promise.all([loadEntries(), loadSummary(), loadReminders()]);
  } catch (error) {
    showStatus(status, error.message, "error");
  }
}

async function refreshAll() {
  await Promise.all([loadActivities(), loadEntries(), loadSummary(), loadReminders()]);
}

function registerEvents() {
  qs("#activity-form")?.addEventListener("submit", handleActivitySubmit);
  qs("#entry-form")?.addEventListener("submit", handleEntrySubmit);
  qs("#refresh-button")?.addEventListener("click", () => {
    refreshAll().catch((error) => console.error(error));
  });
}

document.addEventListener("DOMContentLoaded", () => {
  registerEvents();
  refreshAll().catch((error) => console.error(error));
  // periodic refresh for reminders / summary
  setInterval(() => {
    loadReminders();
    loadSummary();
  }, 60_000);
});
