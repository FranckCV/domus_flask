function showErrorModal(message) {
    var modal = document.getElementById("errorModal");
    var messageEl = document.getElementById("error-message");
    messageEl.textContent = message;  
    modal.style.display = "block";  

    var closeBtn = document.getElementsByClassName("close")[0];
    closeBtn.onclick = function() {
        modal.style.display = "none";
    };

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    };
}