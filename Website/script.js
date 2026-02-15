const submitBtn = document.getElementById("submitBtn");
const queryInput = document.getElementById("query");
const responseDiv = document.getElementById("response");

submitBtn.addEventListener("click", async () => {
  const question = queryInput.value;
  if (!question) return;

  responseDiv.innerText = "Loading...";

  try {
    const res = await fetch("http://127.0.0.1:8000/rag/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: question})
    });

    if (!res.ok) throw new Error(`HTTP error ${res.status}`);

    const data = await res.json();
    let text = `Answer:\n${data["answer"]}\n\nContext chunks:\n`;
    data["sources"].forEach((c, i) => { text += `[${i+1}] ${c}\n`; });

    responseDiv.innerText = text;
  } catch (err) {
    responseDiv.innerText = "Error: " + err.message;
  }
});
