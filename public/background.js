chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "fetchData") {
    // Interact with the `chrome` API or fetch data from a Python backend
    fetch("http://localhost:5000/api/data") // Example API call
      .then((response) => response.json())
      .then((data) => sendResponse({ message: data.message })) // Send back the response
      .catch((error) => sendResponse({ message: "Error occurred!" }));

    return true; // Keep the message channel open for async response
  }
});
