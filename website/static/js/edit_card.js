// static/js/edit_card.js

function displayError(message) {
    const errorDiv = document.getElementById("flashcard-error");
    errorDiv.textContent = message;
    errorDiv.style.display = "block";
}

function displaySuccess(message) {
    const successDiv = document.getElementById("flashcard-success");
    successDiv.textContent = message;
    successDiv.style.display = "block";
}

// Initialize Quill editors
const quillFront = new Quill("#editor-front", { theme: "snow" });
const quillBack = new Quill("#editor-back", { theme: "snow" });

// Load initial content from hidden elements
const frontContent = document.getElementById("front-content").textContent;
const backContent = document.getElementById("back-content").textContent;

try {
    const frontDelta = JSON.parse(frontContent);
    const backDelta = JSON.parse(backContent);
    quillFront.setContents(frontDelta);
    quillBack.setContents(backDelta);
} catch (e) {
    // Fallback for old content format
    quillFront.clipboard.dangerouslyPasteHTML(frontContent);
    quillBack.clipboard.dangerouslyPasteHTML(backContent);
}

// Form submission handler
document.getElementById("edit-flashcard-form").addEventListener("submit", function(event) {
    event.preventDefault();

    const front = JSON.stringify(quillFront.getContents());
    const back = JSON.stringify(quillBack.getContents());
    const frontText = quillFront.getText().trim();
    const backText = quillBack.getText().trim();

    if (frontText === "" || backText === "") {
        displayError("Both front and back are required");
        return;
    }

    const form = this;
    const flashcardId = form.dataset.flashcardId;
    const deckId = form.dataset.deckId;

    fetch(`/edit-flashcard/${flashcardId}`, {
        method: "POST",
        body: JSON.stringify({ front: front, back: back }),
        headers: { "Content-Type": "application/json" }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = `/deck/${deckId}`;
        } else {
            displayError(data.message || "Failed to update flashcard");
        }
    })
    .catch(error => {
        alert("Error occurred: " + error);
    });
});