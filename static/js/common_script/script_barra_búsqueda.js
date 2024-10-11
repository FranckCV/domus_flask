$(document).ready(function() {
    let suggestions = [
        "Celulares",
        "Exclusividad Domus",
        "Samsung",
        "Blue Label",
        "Laptop",
        "Gloria",
        "Oster",
        "Arroz"
    ];

    $("#search").on("input", function() {
        let query = $(this).val().toLowerCase();
        let matchedSuggestions = suggestions.filter(function(suggestion) {
            return suggestion.toLowerCase().includes(query);
        });

        displaySuggestions(matchedSuggestions);
    });

    function displaySuggestions(suggestions) {
        let suggestionsContainer = $("#suggestions");
        suggestionsContainer.empty();

        suggestions.forEach(function(suggestion) {
            let suggestionElement = $("<p></p>").text(suggestion);
            suggestionElement.on("click", function() {
                $("#search").val(suggestion);
                suggestionsContainer.empty();
            });
            suggestionsContainer.append(suggestionElement);
        });
    }
});

