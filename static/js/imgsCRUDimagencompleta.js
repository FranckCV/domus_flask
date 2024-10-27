function openImage(src) {
    const overlay = document.getElementById('overlayImage');
    const enlargedImage = document.getElementById('enlargedImage');
  
    enlargedImage.src = src; // Establece la fuente de la imagen
    overlay.style.display = 'flex'; // Muestra el overlay
  }
  
  // Función para cerrar el overlay
  function closeImage() {
    const overlay = document.getElementById('overlayImage');
    overlay.style.display = 'none'; // Oculta el overlay
  }
  
  // Asigna el evento click a las imágenes con la clase 'clickable-image'
  document.querySelectorAll('.clickable-image').forEach(image => {
    image.addEventListener('click', function() {
      openImage(this.src);
    });
  });