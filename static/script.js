const fileInput = document.getElementById("fileInput");
const analyzeBtn = document.getElementById("analyzeBtn");
const spinner = document.getElementById("spinner");
const errorBox = document.getElementById("errorBox");
const results = document.getElementById("results");
const successBanner = document.getElementById("successBanner");
const totalCount = document.getElementById("totalCount");
const fraudCount = document.getElementById("fraudCount");
const resultsBody = document.getElementById("resultsBody");

analyzeBtn.addEventListener("click", async () => {
  const file = fileInput.files[0];

  if (!file) {
    showError("Please choose a CSV file first.");
    return;
  }

  // Reset UI state
  hide(errorBox);
  hide(results);
  show(spinner);
  analyzeBtn.disabled = true;

  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch("/predict", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Something went wrong while analyzing the file.");
    }

    renderResults(data);
  } catch (err) {
    showError(err.message);
  } finally {
    hide(spinner);
    analyzeBtn.disabled = false;
  }
});

function renderResults(data) {
  successBanner.innerHTML =
    `Analysis complete — flagged <strong>${data.flagged_fraud}</strong> out of ` +
    `<strong>${data.total_transactions}</strong> transactions as fraud.`;

  totalCount.textContent = data.total_transactions;
  fraudCount.textContent = data.flagged_fraud;

  resultsBody.innerHTML = "";
  data.results.forEach((row) => {
    const tr = document.createElement("tr");
    if (row.Prediction === "Fraud") {
      tr.classList.add("fraud-row");
    }
    tr.innerHTML = `<td>${row.Prediction}</td><td>${row["Fraud Probability"]}</td>`;
    resultsBody.appendChild(tr);
  });

  show(results);
}

function showError(message) {
  errorBox.textContent = message;
  show(errorBox);
}

function show(el) {
  el.classList.remove("hidden");
}

function hide(el) {
  el.classList.add("hidden");
}
