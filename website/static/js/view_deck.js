//view_deck.js

document.addEventListener('DOMContentLoaded', function() {
    const flashcardContainer = document.getElementById("flashcard-container");
    
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

    // Function to convert Delta to HTML
    function deltaToHtml(delta) {
        // If delta is already a string (JSON), parse it first
        const deltaObj = typeof delta === 'string' ? JSON.parse(delta) : delta;
        const tempQuill = new Quill(document.createElement('div'));
        tempQuill.setContents(deltaObj);
        return tempQuill.root.innerHTML;
    }

    // Function to create a flashcard element
    function createFlashcardElement(flashcard) {
        const frontHtml = deltaToHtml(flashcard.front);
        const backHtml = deltaToHtml(flashcard.back);

        const flashcardElement = document.createElement('div');
        flashcardElement.className = 'row shadow mb-4 flashcard-element';
        flashcardElement.id = `flashcard-${flashcard.id}`;
        flashcardElement.innerHTML = `
            <div class="col-md-10 col-sm-8">
                    <h5>${frontHtml}</h5>
                    <p>${backHtml}</p>
            </div>
            <div class="col-md-2 col-sm-4">
            <a href="/edit-flashcard/${flashcard.id}" class="btn btn-primary">Edit</a>
            <button class="btn btn-danger delete-flashcard" data-flashcard-id="${flashcard.id}">Delete</button>
            </div>
            
        `;
        return flashcardElement;
    }

    // Initialize Quill editors
    var quillFront = new Quill("#editor-front", { theme: "snow" });
    var quillBack = new Quill("#editor-back", { theme: "snow" });

    // Fetch initial flashcards
    const deckId = document.getElementById("deck-page").dataset.deckId;
    fetch(`/deck/${deckId}/flashcards`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                data.flashcards.forEach(flashcard => {
                    const flashcardElement = createFlashcardElement(flashcard);
                    flashcardContainer.appendChild(flashcardElement);
                });
            } else {
                displayError("Failed to load flashcards");
            }
        })
        .catch(error => {
            displayError("Error loading flashcards: " + error);
        });

    document.getElementById("add-flashcard").addEventListener("submit", function(event) {
        event.preventDefault();
        let front = JSON.stringify(quillFront.getContents());
        let back = JSON.stringify(quillBack.getContents());
        let frontText = quillFront.getText().trim();
        let backText = quillBack.getText().trim();

        if (frontText === "" || backText === "") {
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
                const flashcardElement = createFlashcardElement(data.flashcard);
                flashcardContainer.appendChild(flashcardElement);
                
                quillFront.setContents([]);
                quillBack.setContents([]);
                displaySuccess("Flashcard added successfully");
            } else {
                displayError("Failed to add flashcard: " + (data.message || "Unknown error"));
            }
        })
        .catch((error) => {
            displayError("Error occurred: " + error);
        });
    });

    // Use event delegation for delete buttons
    document.addEventListener('click', function(event) {
        if (event.target.classList.contains('delete-flashcard')) {
            const flashcardId = event.target.dataset.flashcardId;
            deleteFlashcard(flashcardId);
        }
    });

    // Handle study mode changes
    const studyModeRadios = document.querySelectorAll('input[name="study-mode"]');
    studyModeRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            const deckId = document.getElementById("deck-page").dataset.deckId;
            const studyMode = this.value;
            
            fetch(`/update-study-mode/${deckId}`, {
                method: "POST",
                body: JSON.stringify({ study_mode: studyMode }),
                headers: {
                    "Content-Type": "application/json",
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    displaySuccess("Study mode updated successfully");
                } else {
                    displayError(data.message || "Failed to update study mode");
                }
            })
            .catch(error => {
                displayError("Error updating study mode: " + error);
            });
        });
    });
});