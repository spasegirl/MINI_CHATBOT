document.addEventListener("DOMContentLoaded", () => {
    const uploadForm = document.getElementById("upload-form");
    const queryForm = document.getElementById("query-form");
    const chatMessages = document.getElementById("chat-messages");
    const uploadMessage = document.getElementById("upload-message");

    let pdfUploaded = false;

    // Handle PDF upload
    uploadForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const fileInput = document.getElementById("pdf-file");
        const file = fileInput.files[0];

        if (!file) {
            uploadMessage.textContent = "Please select a PDF file.";
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        uploadMessage.textContent = "Uploading...";

        try {
            const response = await fetch("/", {
                method: "POST",
                body: formData,
            });

            if (response.ok) {
                uploadMessage.textContent = "PDF uploaded successfully! You can now ask questions about it.";
                pdfUploaded = true;
            } else {
                const error = await response.text();
                uploadMessage.textContent = `Error: ${error}`;
                pdfUploaded = false; // Reset the flag in case of failure
            }
        } catch (err) {
            uploadMessage.textContent = "An error occurred during upload.";
            pdfUploaded = false; // Reset the flag in case of failure
        }
    });

    // Handle chat queries
    // Handle chat queries
    queryForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const userQueryInput = document.getElementById("user-query");
        const userQuery = userQueryInput.value.trim();

        if (!userQuery) return;

        // Display user message
        const userMessage = document.createElement("div");
        userMessage.textContent = userQuery;
        userMessage.className = "user";
        chatMessages.appendChild(userMessage);

        userQueryInput.value = "";

        // Send query to backend
        try {
            const endpoint = pdfUploaded ? "/query" : "/chat"; // Adjust depending on upload state
            const response = await fetch(endpoint, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query: userQuery }),
            });

            const data = await response.json();
            const botMessage = document.createElement("div");
            botMessage.textContent = data.response;
            botMessage.className = "bot";
            chatMessages.appendChild(botMessage);

            // Scroll to the latest message
            chatMessages.scrollTop = chatMessages.scrollHeight;
        } catch (err) {
            const botMessage = document.createElement("div");
            botMessage.textContent = "An error occurred while processing your query.";
            botMessage.className = "bot";
            chatMessages.appendChild(botMessage);
        }
    });

});
