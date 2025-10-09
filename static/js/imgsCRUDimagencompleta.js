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


document.addEventListener('click', function(event) {
  if (event.target.classList.contains('clickable-image')) {
    openImage(event.target.src);
  }
});