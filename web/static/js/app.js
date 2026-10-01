const $ = (id) => document.getElementById(id);
let chart;

function badge(text, detected) {
  return `<span class="badge ${detected ? "yes" : "no"}">${text}</span>`;
}
async function refreshDashboard() {
  const [analyticsRes, historyRes] = await Promise.all([
    fetch("/api/v1/analytics"), fetch("/api/v1/experiments")
  ]);
  if (!analyticsRes.ok || !historyRes.ok) return;
  const analytics = await analyticsRes.json();
  const history = await historyRes.json();
  $("totalMetric").textContent = analytics.total_experiments;
  $("originalMetric").textContent = analytics.original_detection_count;
  $("transformedMetric").textContent = analytics.transformed_detection_count;
  $("changedMetric").textContent = analytics.detection_state_changed_count;
  const body = $("historyBody");
  body.innerHTML = "";
  if (!history.experiments.length) {
    body.innerHTML = '<tr><td colspan="6">No experiments yet. Run one above to populate the workspace.</td></tr>';
  } else {
    history.experiments.forEach(item => {
      const tr = document.createElement("tr");
      const values = [
        new Date(item.created_at).toLocaleString(), item.label,
        item.original_detected ? "MATCH" : "NO MATCH",
        item.transformed_detected ? "MATCH" : "NO MATCH",
        `${item.duration_ms} ms`
      ];
      values.forEach(value => { const td = document.createElement("td"); td.textContent = value; tr.appendChild(td); });
      const td = document.createElement("td");
      const link = document.createElement("a"); link.href = `/api/v1/reports/${item.id}.json`; link.textContent = "JSON";
      td.appendChild(link); tr.appendChild(td); body.appendChild(tr);
    });
  }
  const ctx = $("detectionChart");
  if (chart) chart.destroy();
  chart = new Chart(ctx, {
    type: "bar",
    data: { labels: ["Original sample", "Transformed sample"],
      datasets: [{ label: "Synthetic matches", data: [analytics.original_detection_count, analytics.transformed_detection_count],
        backgroundColor: ["rgba(123,167,255,.75)", "rgba(88,224,208,.75)"], borderRadius: 7 }] },
    options: { responsive: true, plugins: { legend: { labels: { color: "#b8c7d9" } } },
      scales: { x: { ticks: { color: "#93a4ba" }, grid: { color: "#233248" } },
        y: { beginAtZero: true, ticks: { precision: 0, color: "#93a4ba" }, grid: { color: "#233248" } } } }
  });
}

$("experimentForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const button = $("runButton"); button.disabled = true; $("status").textContent = "Running controlled analysis…";
  const pipeline = [...document.querySelectorAll("[data-kind]:checked")].map(el => ({
    kind: el.dataset.kind, name: el.value,
    params: el.value === "xor_hex" ? { key: "lab-key" } : {}
  }));
  try {
    const response = await fetch("/api/v1/experiments", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sample: $("sample").value, label: $("label").value,
        notes: $("notes").value, pipeline })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Experiment failed.");
    const item = data.experiment;
    $("resultPanel").hidden = false;
    $("resultTitle").textContent = item.label;
    $("resultBadges").innerHTML = badge(`Original: ${item.original_detection.detected ? "MATCH" : "NO MATCH"}`, item.original_detection.detected)
      + badge(`Transformed: ${item.transformed_detection.detected ? "MATCH" : "NO MATCH"}`, item.transformed_detection.detected)
      + badge(`State changed: ${item.detection_changed ? "YES" : "NO"}`, item.detection_changed);
    $("originalHash").textContent = item.sample_sha256;
    $("transformedHash").textContent = item.transformed_sha256;
    $("transformedText").textContent = item.transformed_sample;
    $("jsonLink").href = `/api/v1/reports/${item.id}.json`;
    $("csvLink").href = `/api/v1/reports/${item.id}.csv`;
    $("status").textContent = `Experiment saved: ${item.id}`;
    await refreshDashboard();
    $("resultPanel").scrollIntoView({ behavior: "smooth", block: "start" });
  } catch (error) { $("status").textContent = error.message; }
  finally { button.disabled = false; }
});
$("copyButton").addEventListener("click", async () => {
  await navigator.clipboard.writeText($("transformedText").textContent);
  $("status").textContent = "Transformed representation copied.";
});
$("refreshButton").addEventListener("click", refreshDashboard);
refreshDashboard().catch(() => { $("historyBody").innerHTML = "<tr><td colspan='6'>Could not load experiment history.</td></tr>"; });
