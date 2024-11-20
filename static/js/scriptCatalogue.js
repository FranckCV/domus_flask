document.addEventListener('DOMContentLoaded', () => {
    const filterElements = document.querySelectorAll('.ctlg_filters_element');
    const products = document.querySelectorAll('.product');
    const clearFiltersButton = document.querySelector('.ctlg_filters_clean');
    const priceInputs = {
        min: document.querySelector('#min_price'),
        max: document.querySelector('#max_price')
    };
    const messageContainer = document.createElement('div');
    messageContainer.className = 'no-products-message';
    messageContainer.textContent = 'No hay productos disponibles para los filtros seleccionados.';
    messageContainer.style.display = 'none';
    document.querySelector('.gallery_product').appendChild(messageContainer);

    // Mostrar y ocultar subcontenidos de los filtros
    filterElements.forEach(element => {
        const subContent = element.nextElementSibling;

        element.addEventListener('click', () => {
            const isVisible = !subContent.classList.contains('ctlg_filters_subcontent_hidden');

            // Ocultar todos los subcontenidos
            document.querySelectorAll('.ctlg_filters_subcontent').forEach(sub => {
                sub.classList.add('ctlg_filters_subcontent_hidden');
            });

            // Mostrar el actual si no estaba visible
            if (!isVisible) {
                subContent.classList.remove('ctlg_filters_subcontent_hidden');
            }
        });
    });

    const cantidad_productos = () => {
        const campoCant = document.querySelector('#cantProductsCatalogue');
        const products = document.querySelectorAll('.gallery_product .product');
        let cantidad = 0;
    
        // Contar productos visibles (display: grid)
        products.forEach(product => {
            if (window.getComputedStyle(product).display === 'grid') {
                cantidad++;
            }
        });
    
        // Actualizar el campo con la cantidad
        campoCant.textContent = cantidad;
    };

    // Función para aplicar filtros
    const applyFilters = () => {
        // Obtener categorías seleccionadas
        const selectedCategories = Array.from(
            document.querySelectorAll('.filter_cat input[type="checkbox"]:checked')
        ).map(checkbox => checkbox.value.trim());

        // Obtener subcategorías seleccionadas
        const selectedSubcategories = Array.from(
            document.querySelectorAll('.filter_subcat input[type="checkbox"]:checked')
        ).map(checkbox => checkbox.value.trim());

        // Obtener rangos de precios
        const minPrice = parseFloat(priceInputs.min?.value) || 0;
        const maxPrice = parseFloat(priceInputs.max?.value) || Infinity;

        // Sincronizar visibilidad de subcategorías
        const subcategoryFilters = document.querySelectorAll('.filter_subcat');
        subcategoryFilters.forEach(subcategoryFilter => {
            const subcategoryCategory = subcategoryFilter.dataset.category;

            // Mostrar u ocultar subcategorías según las categorías seleccionadas
            if (selectedCategories.length === 0 || selectedCategories.includes(subcategoryCategory)) {
                subcategoryFilter.style.display = 'grid';
            } else {
                subcategoryFilter.style.display = 'none';
            }
        });

        // Filtrar productos
        let visibleProductsCount = 0;
        products.forEach(product => {
            const productCategory = product.dataset.category;
            const productSubcategory = product.dataset.subcategory;
            const productPrice = parseFloat(product.dataset.price);

            const matchesCategory = selectedCategories.length === 0 || selectedCategories.includes(productCategory);
            const matchesSubcategory = selectedSubcategories.length === 0 || selectedSubcategories.includes(productSubcategory);
            const matchesPrice = productPrice >= minPrice && productPrice <= maxPrice;

            if (matchesCategory && matchesSubcategory && matchesPrice) {
                product.style.display = 'grid'; // Mostrar producto
                visibleProductsCount++;
            } else {
                product.style.display = 'none'; // Ocultar producto
            }
        });

        // Mostrar mensaje si no hay productos
        if (visibleProductsCount === 0) {
            messageContainer.style.display = 'block';
        } else {
            messageContainer.style.display = 'none';
        }
        cantidad_productos();
    };

    // Evento para los checkboxes
    const checkboxes = document.querySelectorAll('.ctlg_filters_subelement input[type="checkbox"], .filter_subcat input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            applyFilters();
            cantidad_productos();
        });
    });

    // Evento para los campos de precio
    const priceInputsElements = document.querySelectorAll('#min_price, #max_price');
    priceInputsElements.forEach(input => {
        input.addEventListener('input',  () => {
            applyFilters();
            cantidad_productos();
        });
    });

    // Botón para limpiar filtros
    clearFiltersButton.addEventListener('click', () => {
        // Desmarcar todos los checkboxes
        checkboxes.forEach(checkbox => {
            checkbox.checked = false;
        });

        // Resetear campos de precio
        if (priceInputs.min) priceInputs.min.value = '';
        if (priceInputs.max) priceInputs.max.value = '';

        // Restablecer visibilidad de subcategorías y productos
        document.querySelectorAll('.filter_subcat').forEach(subcat => {
            subcat.style.display = 'grid'; // Mostrar todas las subcategorías
        });
        products.forEach(product => {
            product.style.display = 'grid'; // Mostrar todos los productos
        });

        // Ocultar mensaje de "No hay productos"
        messageContainer.style.display = 'none';
        cantidad_productos();
    });

    // Activar y desactivar checkboxes al hacer clic en el div padre
    const filterSubElements = document.querySelectorAll('.ctlg_filters_subelement');
    filterSubElements.forEach(subelement => {
        subelement.addEventListener('click', (event) => {
            if (event.target.tagName !== 'INPUT') {
                const checkbox = subelement.querySelector('input[type="checkbox"]');
                checkbox.checked = !checkbox.checked;
                applyFilters();
                cantidad_productos();
            }
        });
    });

    // Inicialización
    applyFilters();
    cantidad_productos();

});
