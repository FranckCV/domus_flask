document.getElementById('categorySelect').addEventListener('change', function() {
    const selectedCategory = this.value;
    const rows = document.querySelectorAll('#productTableBody tr');

    const options = document.querySelectorAll('#subcategorySelect option');

    options.forEach(option => {
        const productCategory = option ? option.getAttribute('data-category') : null;
  
        // Si el valor seleccionado es "0", mostrar todas las filas
        if (selectedCategory === "0" || productCategory === selectedCategory) {
            option.style.display = '';
        } else {
            option.style.display = 'none';
        }
    });

    rows.forEach(row => {
      const categoryDiv = row.querySelector('[data-category]');
      const productCategory = categoryDiv ? categoryDiv.getAttribute('data-category') : null;

      // Si el valor seleccionado es "0", mostrar todas las filas
      if (selectedCategory === "0" || productCategory === selectedCategory) {
        row.style.display = '';
      } else {
        row.style.display = 'none';
      }
    });
});


document.getElementById('subcategorySelect').addEventListener('change', function() {
    const selectedCategory = this.value;
    const rows = document.querySelectorAll('#productTableBody tr');

    rows.forEach(row => {
      const categoryDiv = row.querySelector('[data-subcategory]');
      const productCategory = categoryDiv ? categoryDiv.getAttribute('data-subcategory') : null;

      // Si el valor seleccionado es "0", mostrar todas las filas
      if (selectedCategory === "0" || productCategory === selectedCategory) {
        row.style.display = '';
      } else {
        row.style.display = 'none';
      }
    });
});



document.getElementById('brandSelect').addEventListener('change', function() {
    const selectedBrand = this.value;
    const rows = document.querySelectorAll('#productTableBody tr');

    rows.forEach(row => {
      const brandDiv = row.querySelector('[data-brand]');
      const productBrand = brandDiv ? brandDiv.getAttribute('data-brand') : null;

      // Si el valor seleccionado es "0", mostrar todas las filas
      if (selectedBrand === "0" || productBrand === selectedBrand) {
        row.style.display = '';
      } else {
        row.style.display = 'none';
      }
    });
});


