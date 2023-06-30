document.getElementById("sentimentForm").addEventListener("submit", async (event) => {
    event.preventDefault();

    const reviewInput = document.getElementById("reviewInput").value.trim();
    if (!reviewInput) {
        return;
    }

    const data = { text: reviewInput };

    const response = await fetch("http://127.0.0.1:8000/predict-review", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    if (response.ok) {
        const result = await response.json();
        displayResult(result);
    } else {
        console.error("Failed to fetch the prediction result.");
    }
});

function displayResult(result) {
    document.getElementById("sentiment").textContent = `Sentiment: ${result.sentiment}`;
    document.getElementById("confidence").textContent = `Confidence: ${result.confidence}`;

    document.getElementById("resultContainer").style.display = "block";
}