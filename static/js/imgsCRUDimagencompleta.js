function openImage(src) {
  const overlay = document.getElementById('overlayImage');
  const enlargedImage = document.getElementById('enlargedImage');

  enlargedImage.src = src;
  overlay.style.display = 'flex'; 
}

function closeImage() {
  const overlay = document.getElementById('overlayImage');
  overlay.style.display = 'none';
}

document.querySelectorAll('.clickable-image').forEach(image => {
  image.addEventListener('click', function() {
    openImage(this.src);
  });
});