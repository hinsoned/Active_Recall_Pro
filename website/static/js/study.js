// static/js/study.js
document.addEventListener("DOMContentLoaded", () => {
    // Variables
    let deckId, deckLength;
    let currentIndex = 0;
    let showFront = true;
    let currentFlashcard = null;
    let deckMode = 'normal'; // Will be updated from the deck data
  
    // Helper function to convert Delta JSON to HTML
    function deltaToHtml(delta) {
        const tempQuill = new Quill(document.createElement('div'));
        tempQuill.setContents(JSON.parse(delta));
        return tempQuill.root.innerHTML;
    }

    // Extract deckId from URL for initial fetch
    const pathParts = window.location.pathname.split("/");
    const deckIdFromUrl = pathParts[2]; // Assumes URL is /study/<deck_id>
  
    // Helper function to Fetch cards based on study mode
    function fetchCards() {
        let url;
        if (deckMode === 'sm2') {
            url = `/study/${deckId}/due`;  // Use the due cards endpoint for SM-2
        } else {
            url = `/study/${deckId}/${currentIndex}`;  // Use index-based for normal mode
        }

        fetch(url)
            .then((response) => response.json())
            .then((data) => {
                if (data.success) {
                    if (deckMode === 'sm2') {
                        // For SM-2, we get an array of due cards
                        if (data.cards && data.cards.length > 0) {
                            currentFlashcard = data.cards[0];  // Show the first due card
                            displayCard();
                        } else {
                            document.getElementById("flashcard-front").textContent = "No cards due for review";
                            document.getElementById("flashcard-content").textContent = "Come back later!";
                            document.getElementById("sm2-controls").style.display = "none";
                        }
                    } else {
                        // For normal mode, we get a single flashcard
                        currentFlashcard = data.flashcard;
                        displayCard();
                    }
                } else {
                    console.error("Failed to load cards:", data.message);
                    document.getElementById("flashcard-front").textContent = "No cards available";
                }
            })
            .catch((error) => {
                console.error("Error fetching cards:", error);
                document.getElementById("flashcard-front").textContent = "Error loading cards";
            });
    }

    // Set up UI based on study mode
    function setupStudyMode() {
        const normalControls = document.getElementById("normal-controls");
        const sm2Controls = document.getElementById("sm2-controls");
        
        if (deckMode === 'sm2') {
            normalControls.style.display = "none";
            sm2Controls.style.display = "block";
            
            // Add SM-2 event listeners for rating buttons and toggle button
            document.getElementById("toggle-button-sm2").addEventListener("click", toggleCard);
            document.querySelectorAll('[data-rating]').forEach(button => {
                button.addEventListener('click', (e) => {
                    const rating = parseInt(e.target.dataset.rating);
                    rateFlashcard(rating);
                });
            });
        } else {
            normalControls.style.display = "block";
            sm2Controls.style.display = "none";
            
            // Add normal mode event listeners
            document.getElementById("toggle-button").addEventListener("click", toggleCard);
            document.getElementById("next-button").addEventListener("click", nextCard);
        }
    }
  
    // Update the initialization to use fetchCards instead of fetchFlashcard
    // This is the first request to run upon loading the page
    fetch(`/study/${deckIdFromUrl}/config`)
        .then((response) => response.json())
        .then((data) => {
            deckId = data.deck_id;
            deckLength = data.deck_length;
            deckMode = data.study_mode || 'normal';

            console.log("Deck ID:", deckId);
            console.log("Deck Length:", deckLength);
            console.log("Study Mode:", deckMode);

            setupStudyMode(); // See function above
            fetchCards();  // Use the new fetchCards function
        })
        .catch((error) => {
            console.error("Error fetching config:", error);
            document.getElementById("flashcard-front").textContent = "Error loading deck";
        });

    // Toggle between front and back
    function toggleCard() {
      showFront = !showFront;
      displayCard();
  
      if (deckMode === 'sm2') {
        let toggleButton = document.getElementById("toggle-button-sm2");
        let ratingButtons = document.getElementById("rating-buttons");
        
        if (!showFront) {
          toggleButton.style.display = "none";
          ratingButtons.style.display = "block";
        }
      } else {
        let toggleButton = document.getElementById("toggle-button");
        let nextButton = document.getElementById("next-button");
        
        if (!showFront) {
          toggleButton.style.display = "none";
          nextButton.style.display = "inline";
        }
      }

      // Update study frequency
      fetch(`/study/${deckId}`, {
        method: "POST",
        body: JSON.stringify({ flashcard_id: currentFlashcard.id }),
        headers: { "Content-Type": "application/json" },
      })
        .then((response) => response.json())
        .then((data) => {
          if (!data.success) console.error("Failed to update study frequency:", data.message);
        })
        .catch((error) => console.error("Error updating study frequency:", error));
    }

    // Update nextCard to use fetchCards
    function nextCard() {
        if (deckMode === 'sm2') {
            fetchCards();  // For SM-2, fetch the next due card
        } else {
            currentIndex = (currentIndex + 1) % deckLength;
            fetchCards();  // For normal mode, increment index and fetch
        }
        
        // Reset UI and state
        showFront = true;
        document.getElementById("toggle-button").style.display = "inline";
        document.getElementById("next-button").style.display = "none";
    }

    // Update rateFlashcard to use fetchCards
    function rateFlashcard(rating) {
        if (deckMode !== 'sm2') return;

        fetch(`/study/${deckId}/rate`, {
            method: "POST",
            body: JSON.stringify({
                flashcard_id: currentFlashcard.id,
                rating: rating
            }),
            headers: { "Content-Type": "application/json" }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // After rating, fetch the next due card
                showFront = true;
                fetchCards();
                
                // Reset UI
                document.getElementById("toggle-button-sm2").style.display = "inline";
                document.getElementById("rating-buttons").style.display = "none";
            } else {
                console.error("Failed to rate flashcard:", data.message);
            }
        })
        .catch(error => console.error("Error rating flashcard:", error));
    }
  
    // Display the current flashcard
    function displayCard() {
      let flashcardFront = document.getElementById("flashcard-front");
      let flashcardContent = document.getElementById("flashcard-content");
  
      if (!currentFlashcard) return;
  
      // Convert Delta to HTML before displaying
      flashcardFront.innerHTML = deltaToHtml(currentFlashcard.front);
  
      if (showFront) {
        flashcardContent.textContent = "";
        if (deckMode === 'sm2') {
          document.getElementById("toggle-button-sm2").textContent = "Show Back";
          document.getElementById("toggle-button-sm2").style.display = "inline";
          document.getElementById("rating-buttons").style.display = "none";
        } else {
          document.getElementById("toggle-button").textContent = "Show Back";
          document.getElementById("toggle-button").style.display = "inline";
          document.getElementById("next-button").style.display = "none";
        }
      } else {
        // Convert Delta to HTML before displaying
        flashcardContent.innerHTML = deltaToHtml(currentFlashcard.back);
      }
    }
});