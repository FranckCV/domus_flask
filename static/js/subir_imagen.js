document.getElementById("btnSubirImagen").addEventListener("click", function() {
    document.getElementById("inputImagen").click();
});

document.getElementById("inputImagen").addEventListener("change", function() {
    this.form.submit(); 
});