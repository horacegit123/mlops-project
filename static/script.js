document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("predictionForm").addEventListener("submit", async function (event) {
    event.preventDefault(); // Prevent page reload

    let formData = new FormData(this);

    let jsonData = {};
    formData.forEach((value, key) => {
      jsonData[key] = value;
    });

    try {
      let response = await fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(jsonData)
      });

      let result = await response.json();

      let resultDiv = document.getElementById("result");

      if (result.predicted_price) {
        resultDiv.innerHTML = `<h2>Predicted Price: $${result.predicted_price.toLocaleString()}</h2>`;
      } else if (result.error) {
        resultDiv.innerHTML = `<p style="color:red;">Error: ${result.error}</p>`;
      }
    } catch (error) {
      document.getElementById("result").innerHTML = `<p style="color:red;">Error: ${error.message}</p>`;
    }
  });
});
