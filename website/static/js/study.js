// static/js/study.js
document.addEventListener("DOMContentLoaded", () => {
    // Variables
    let deckId, deckLength;
    let currentIndex = 0;
    let showFront = true;
    let currentFlashcard = null;
  
    // Helper function to convert Delta JSON to HTML
    function deltaToHtml(delta) {
        const tempQuill = new Quill(document.createElement('div'));
        tempQuill.setContents(JSON.parse(delta));
        return tempQuill.root.innerHTML;
    }

    // Extract deckId from URL for initial fetch
    const pathParts = window.location.pathname.split("/");
    const deckIdFromUrl = pathParts[2]; // Assumes URL is /study/<deck_id>
  
    // Fetch config data
    fetch(`/study/${deckIdFromUrl}/config`)
      .then((response) => response.json())
      .then((data) => {
        deckId = data.deck_id;
        deckLength = data.deck_length;

        console.log("Deck ID:", deckId);
        console.log("Deck Length:", deckLength);
  
        // Add event listeners
        document.getElementById("toggle-button").addEventListener("click", toggleCard);
        document.getElementById("next-button").addEventListener("click", nextCard);
  
        // Initial fetch
        fetchFlashcard(currentIndex);
      })
      .catch((error) => {
        console.error("Error fetching config:", error);
        document.getElementById("flashcard-front").textContent = "Error loading deck";
      });
  
    // Fetch a specific flashcard
    function fetchFlashcard(index) {
      fetch(`/study/${deckId}/${index}`)
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            currentFlashcard = data.flashcard;
            displayCard();
          } else {
            console.error("Failed to load flashcard:", data.message);
            document.getElementById("flashcard-front").textContent = "No flashcards available";
          }
        })
        .catch((error) => {
          console.error("Error fetching flashcard:", error);
          document.getElementById("flashcard-front").textContent = "Error loading card";
        });
    }
  
    // Toggle between front and back
    function toggleCard() {
      showFront = !showFront;
      displayCard();
  
      let nextButton = document.getElementById("next-button");
      if (!showFront) {
        nextButton.style.display = "inline";
  
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
    }
  
    // Move to next card
    function nextCard() {
      currentIndex = (currentIndex + 1) % deckLength;
      showFront = true;
      fetchFlashcard(currentIndex);
  
      let nextButton = document.getElementById("next-button");
      if (showFront) nextButton.style.display = "none";
    }
  
    // Display the current flashcard
    function displayCard() {
      let flashcardFront = document.getElementById("flashcard-front");
      let flashcardContent = document.getElementById("flashcard-content");
      let toggleButton = document.getElementById("toggle-button");
  
      if (!currentFlashcard) return;
  
      toggleButton.style.display = "inline";
      // Convert Delta to HTML before displaying
      flashcardFront.innerHTML = deltaToHtml(currentFlashcard.front);
  
      if (showFront) {
        flashcardContent.textContent = "";
        toggleButton.textContent = "Show Back";
      } else {
        // Convert Delta to HTML before displaying
        flashcardContent.innerHTML = deltaToHtml(currentFlashcard.back);
        toggleButton.style.display = "none";
      }
    }
  });