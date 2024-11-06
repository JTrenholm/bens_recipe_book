// Search Bar Autocomplete
const searchInput = document.getElementById("search-input");
const autocompleteList = document.getElementById("autocomplete-list");

searchInput.addEventListener("input", async (e) => {
  const query = e.target.value.trim();
  const response = await fetch(
    `https://api.yummly.com/v1/api/recipes/autocomplete?q=${query}`
  );
  const data = await response.json();
  const suggestions = data.suggestions;

  autocompleteList.innerHTML = "";
  suggestions.forEach((suggestion) => {
    const listItem = document.createElement("li");
    listItem.textContent = suggestion;
    autocompleteList.appendChild(listItem);
  });
});

// Recipe Filtering
const filterButtons = document.querySelectorAll(".filter-button");
const recipeList = document.getElementById("recipe-list");

filterButtons.forEach((button) => {
  button.addEventListener("click", (e) => {
    const filterType = e.target.dataset.filter;
    const recipes = recipeList.children;

    Array.from(recipes).forEach((recipe) => {
      if (recipe.dataset[filterType] === "true") {
        recipe.style.display = "block";
      } else {
        recipe.style.display = "none";
      }
    });
  });
});

// Favorite Recipe Toggle
const favoriteButtons = document.querySelectorAll(".favorite-button");

favoriteButtons.forEach((button) => {
  button.addEventListener("click", (e) => {
    const recipeId = e.target.dataset.recipeId;
    const favoriteIcon = e.target.children[0];

    // Toggle favorite icon
    favoriteIcon.classList.toggle("fa-heart");
    favoriteIcon.classList.toggle("fa-heart-o");

    // Update favorite status in database
    fetch(`/favorite/${recipeId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ favorite: true }),
    });
  });
});

// Mobile Navigation
const mobileMenu = document.getElementById("mobile-menu");
const navToggle = document.getElementById("nav-toggle");

navToggle.addEventListener("click", () => {
  mobileMenu.classList.toggle("open");
});

// Recipe Modal
const recipeModal = document.getElementById("recipe-modal");
const recipeLinks = document.querySelectorAll(".recipe-link");

recipeLinks.forEach((link) => {
  link.addEventListener("click", (e) => {
    const recipeId = e.target.dataset.recipeId;
    fetch(`/recipe/${recipeId}`)
      .then((response) => response.json())
      .then((data) => {
        recipeModal.innerHTML = `
          <h2>${data.name}</h2>
          <p>${data.description}</p>
          <img src="${data.image}" alt="Recipe Image">
        `;
        recipeModal.classList.add("open");
      });
  });
});
