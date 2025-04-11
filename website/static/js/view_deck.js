//view_deck.js

function displayError(message) {
    const errorDiv = document.getElementById("flashcard-error");
    errorDiv.textContent = message;
    errorDiv.style.display = "block";
  }

  function displaySuccess(message) {
    const errorDiv = document.getElementById("flashcard-success");
    errorDiv.textContent = message;
    errorDiv.style.display = "block";
  }

  //This uses fetch to send the flashcardId to the back end, then removes the element from the DOM when it gets a good response.
  //Takes in a flashcardId as a parameter
  function deleteFlashcard(flashcardId) {
    fetch("/delete-flashcard", {
      method: "POST",
      body: JSON.stringify({ flashcardId: flashcardId }),
      headers: {
        "Content-Type": "application/json",
      },
    })
      //If the response is good, remove the element from the DOM
      .then((_res) => {
        if (_res.ok) {
          document.getElementById("flashcard-" + flashcardId).remove();
        } else {
          displayError("Failed to delete flashcard");
        }
      })
      .catch((_err) => {
        displayError("Error occurred: " + error.message);
      });
  }

var quillFront = new Quill("#editor-front", { theme: "snow" });
var quillBack = new Quill("#editor-back", { theme: "snow" });

document.getElementById("add-flashcard").addEventListener("submit", function(event) {
    event.preventDefault();
    let front = quillFront.root.innerHTML;
    let back = quillBack.root.innerHTML;
    let frontText = quillFront.getText().trim();
    let backText = quillBack.getText().trim();
    let blankCard = "<p><br></p>";

    if (frontText === "" || backText === "" || front === blankCard || back === blankCard) {
        displayError("Both front and back are required");
        return;
    }

    const errorDiv = document.getElementById("flashcard-error");
    errorDiv.textContent = "";
    errorDiv.style.display = "none";

    const successDiv = document.getElementById("flashcard-success");
    successDiv.textContent = "";
    successDiv.style.display = "none";

    const deckId = document.getElementById("deck-page").dataset.deckId;
    fetch(`/deck/${deckId}`, {
        method: "POST",
        body: JSON.stringify({ front: front, back: back }),
        headers: { "Content-Type": "application/json" },
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.success) {
            let flashcardContainer = document.getElementById("flashcard-container");
            let newFlashcard = document.createElement("div");
            newFlashcard.className = "col-md-4";
            newFlashcard.id = "flashcard-" + data.flashcard.id;
            newFlashcard.innerHTML = `
                <div class="card mb-4">
                    <div class="card-body">
                        <h5 class="card-title">${data.flashcard.front}</h5>
                        <p class="card-text">${data.flashcard.back}</p>
                        <a href="/edit-flashcard/${data.flashcard.id}" class="btn btn-primary">Edit</a>
                        <button class="btn btn-danger" onclick="deleteFlashcard(${data.flashcard.id})">Delete</button>
                    </div>
                </div>
            `;
            flashcardContainer.appendChild(newFlashcard);

            newFlashcard.querySelector('.delete-flashcard').addEventListener('click', () => {
                deleteFlashcard(data.flashcard.id);
            });
            
            quillFront.root.innerHTML = "";
            quillBack.root.innerHTML = "";
            displaySuccess("Flashcard added successfully");
        } else {
            displayError("Failed to add flashcard: " + (data.message || "Unknown error"));
        }
    })
    .catch((error) => {
        alert("Error occurred: " + error);
    });
});

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.delete-flashcard').forEach(button => {
        button.addEventListener('click', () => {
            const flashcardId = button.dataset.flashcardId;
            deleteFlashcard(flashcardId);
        });
    });
});