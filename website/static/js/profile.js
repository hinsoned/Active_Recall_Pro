function displayError(message) {
    const errorDiv = document.getElementById("deck-error");
    errorDiv.textContent = message;
    errorDiv.style.display = "block";
    document.getElementById("create-deck").reset();
    document.getElementById("deckName").focus();
  }

  function displaySuccess(message) {
    const errorDiv = document.getElementById("deck-success");
    errorDiv.textContent = message;
    errorDiv.style.display = "block";
  }

document.addEventListener("DOMContentLoaded", () => {
  let deckToDelete = null;
  console.log('DOM Content Loaded');
  
  const deleteModalEl = document.getElementById('deleteDeckModal');
  console.log('Modal element:', deleteModalEl);
  
  //This uses fetch to send the deckId to the back end, then removes the element from the DOM when it gets a good response.
  function deleteDeck(DeckId) {
    console.log('Deleting deck:', DeckId);
    fetch("/delete-deck", {
      method: "POST",
      body: JSON.stringify({ deckId: DeckId }),
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((_res) => {
        if (_res.ok) {
          document.getElementById("deck-" + DeckId).remove();
          const modal = bootstrap.Modal.getInstance(deleteModalEl);
          if (modal) {
            modal.hide();
          }
        } else {
          alert("Failed to delete deck");
        }
      })
      .catch((_err) => {
        alert("Failed to delete deck");
      });
  }

  // Use event delegation for delete buttons
  document.getElementById('deck-container').addEventListener('click', (e) => {
    if (e.target.classList.contains('btn-danger')) {
      console.log('Delete button clicked');
      e.preventDefault();
      const deckId = e.target.closest(".col-md-4").id.replace("deck-", "");
      console.log('Deck ID:', deckId);
      deckToDelete = deckId;
      
      // Remove any existing modal instances
      const existingModal = bootstrap.Modal.getInstance(deleteModalEl);
      if (existingModal) {
        existingModal.dispose();
      }
      
      // Create and show new modal
      const modal = new bootstrap.Modal(deleteModalEl);
      modal.show();
    }
  });

  // Handle confirm delete button click
  document.getElementById('confirmDeleteDeck').addEventListener('click', () => {
    console.log('Confirm delete clicked');
    if (deckToDelete) {
      deleteDeck(deckToDelete);
    }
  });

  document
    .getElementById("create-deck")
    .addEventListener("submit", function (event) {
      event.preventDefault(); // Prevent the default form submission that would refresh the page

      //Get the values from the form based on the id
      let deckName = document.getElementById("deckName").value.trim();
      let studyMode = document.querySelector('input[name="study-mode"]:checked').value;

      const errorDiv = document.getElementById("deck-error");
      errorDiv.textContent = "";
      errorDiv.style.display = "none";

      const successDiv = document.getElementById("deck-success");
      successDiv.textContent = "";
      successDiv.style.display = "none";

      if (!deckName) { // Check after trimming
        displayError("Deck name cannot be empty");
        return;
      }

    
      //The deck value was passed in when by views.py when the template was rendered so deck.id will pass the
      //id of the deck to the back end
      console.log("deckName:", JSON.stringify(deckName));//check the data
      fetch("/profile", {
        method: "POST",
        body: JSON.stringify({ deckName: deckName, studyMode: studyMode }),
        headers: {
          "Content-Type": "application/json",
        },
      })
        //Parses the JSON response and resolves with a javascript object
        .then((response) => response.json())
        //data refers to the javascript object
        .then((data) => {
          //Update the DOM
          if (data.success) {
            // Create a new deck element and add it to the DOM
            let deckContainer = document.getElementById("deck-container");

            let newDeck = document.createElement("div");
            newDeck.className = "col-md-4";
            newDeck.id = "deck-" + data.deck.id;

            // Create the card div
            let cardDiv = document.createElement("div");
            cardDiv.className = "card mb-4";

            // Create the card body div
            let cardBodyDiv = document.createElement("div");
            cardBodyDiv.className = "card-body";

            // Create the card title
            let cardTitle = document.createElement("h5");
            cardTitle.className = "card-title";
            cardTitle.textContent = data.deck.name;

            // Create the card text for number of cards
            let cardText = document.createElement("p");
            cardText.className = "card-text";
            cardText.textContent = "Cards: 0";

            // Create the card text for study mode
            let modeText = document.createElement("p");
            modeText.className = "card-text";
            let modeSmall = document.createElement("small");
            modeSmall.className = "text-muted";
            modeSmall.textContent = "Mode: " + data.deck.study_mode.charAt(0).toUpperCase() + data.deck.study_mode.slice(1);
            modeText.appendChild(modeSmall);

            // Create the "View Deck" link
            let viewDeckLink = document.createElement("a");
            viewDeckLink.href = "/deck/" + data.deck.id;
            viewDeckLink.className = "btn btn-primary me-1";
            viewDeckLink.textContent = "View Deck";

            // Create the "Study" link
            let studyLink = document.createElement("a");
            studyLink.href = "/study/" + data.deck.id;
            studyLink.className = "btn btn-primary me-1";
            studyLink.textContent = "Study";

            // Create the "Delete" button
            let deleteButton = document.createElement("button");
            deleteButton.className = "btn btn-danger";
            deleteButton.textContent = "Delete";

            // Append the elements together
            cardBodyDiv.appendChild(cardTitle);
            cardBodyDiv.appendChild(cardText);
            cardBodyDiv.appendChild(modeText);
            cardBodyDiv.appendChild(viewDeckLink);
            cardBodyDiv.appendChild(studyLink);
            cardBodyDiv.appendChild(deleteButton);

            cardDiv.appendChild(cardBodyDiv);
            newDeck.appendChild(cardDiv);

            //Actually adds the flashcard to the DOM
            deckContainer.appendChild(newDeck);

            //Clear the form but setting the values to empty strings
            document.getElementById("deckName").value = "";

            //If the response is good, alert the user
            displaySuccess("Deck added successfully");

            //If the response is not good, alert the user
          } else {
            displayError(
              "Failed to add flashcard: " + (data.message || "Unknown error")
            );
          }
        })
        .catch((error) => {
          alert("Error occurred: " + error);
        });
    });
});