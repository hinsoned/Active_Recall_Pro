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

// Function to handle deck copying
function copyDeck() {
    const deckPage = document.getElementById('deck-page');
    const deckId = deckPage.dataset.deckId;
    const errorDiv = document.getElementById('flashcard-error');
    const successDiv = document.getElementById('flashcard-success');

    fetch(`/api/deck/${deckId}/copy`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to copy deck');
        }
        return response.json();
    })
    .then(data => {
        if (!data.success) {
            throw new Error(data.message || 'Failed to copy deck');
        }
        //successDiv.textContent = 'Deck copied successfully!' ;
        successDiv.innerHTML = 'Deck copied successfully! <a class="text-info" href="/profile">View in your profile</a>';
        successDiv.style.display = 'block';
    })
    .catch(error => {
        console.error('Error copying deck:', error);
        errorDiv.textContent = 'Failed to copy deck. Please try again later.';
        errorDiv.style.display = 'block';
    });
}

// Add event listener for copy button
document.addEventListener('DOMContentLoaded', () => {
    loadFlashcards();
    const copyButton = document.getElementById('copy-deck-btn');
    if (copyButton) {
        copyButton.addEventListener('click', copyDeck);
    }
}); 