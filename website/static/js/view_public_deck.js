// Function to convert Quill Delta format to HTML
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

    const cardDiv = document.createElement('div');
    cardDiv.className = 'col-lg-12 mb-4';
    cardDiv.innerHTML = `
        <div class="card h-100">
            <div class="card-body">
                <div class="card-front">
                    <h5 class="card-title">Front:</h5>
                    <div class="card-text">${frontHtml}</div>
                </div>
                <hr>
                <div class="card-back">
                    <h5 class="card-title">Back:</h5>
                    <div class="card-text">${backHtml}</div>
                </div>
            </div>
        </div>
    `;
    return cardDiv;
}

// Function to load flashcards
function loadFlashcards() {
    const deckPage = document.getElementById('deck-page');
    const deckId = deckPage.dataset.deckId;
    const flashcardContainer = document.getElementById('flashcard-container');
    const errorDiv = document.getElementById('flashcard-error');

    fetch(`/api/deck/${deckId}/flashcards`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch flashcards');
            }
            return response.json();
        })
        .then(data => {
            if (!data.success) {
                throw new Error(data.message || 'Failed to load flashcards');
            }

            // Clear existing flashcards
            flashcardContainer.innerHTML = '';

            // Add each flashcard to the container
            data.flashcards.forEach(flashcard => {
                const cardElement = createFlashcardElement(flashcard);
                flashcardContainer.appendChild(cardElement);
            });
        })
        .catch(error => {
            console.error('Error loading flashcards:', error);
            errorDiv.textContent = 'Failed to load flashcards. Please try again later.';
            errorDiv.style.display = 'block';
        });
}

// Load flashcards when the page loads
document.addEventListener('DOMContentLoaded', loadFlashcards); 