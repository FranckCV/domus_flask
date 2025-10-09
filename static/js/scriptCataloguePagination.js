document.addEventListener("DOMContentLoaded", () => {
    const blockContainer = '#gallery_product';
    const classItem = '.product';
    const displayItem = 'grid';
    const paginations = document.querySelectorAll(".ctlg_pagination");
    const galleryItems = document.querySelectorAll(`${blockContainer} ${classItem}`);
    const limitPerPage = 24; // Número de elementos por página
    const paginationSize = 5; // Número máximo de elementos en la paginación
    let currentPage = 1;

    function getPageList(totalPages, page, maxLength) {
        function range(start, end) {
            return Array.from({ length: end - start + 1 }, (_, i) => i + start);
        }

        const sideWidth = maxLength < 9 ? 1 : 2;
        const leftWidth = (maxLength - sideWidth * 2 - 3) >> 1;
        const rightWidth = (maxLength - sideWidth * 2 - 3) >> 1;

        if (totalPages <= maxLength) {
            return range(1, totalPages);
        }

        if (page <= maxLength - sideWidth - 1 - rightWidth) {
            return range(1, maxLength - sideWidth - 1).concat(0, range(totalPages - sideWidth + 1, totalPages));
        }

        if (page >= totalPages - sideWidth - 1 - rightWidth) {
            return range(1, sideWidth).concat(0, range(totalPages - sideWidth - 1 - rightWidth - leftWidth, totalPages));
        }

        return range(1, sideWidth).concat(0, range(page - leftWidth, page + rightWidth), 0, range(totalPages - sideWidth + 1, totalPages));
    }

    function showPage(page) {
        const totalPages = Math.ceil(galleryItems.length / limitPerPage);

        if (page < 1 || page > totalPages) return false;
        currentPage = page;

        // Mostrar los elementos de la página actual
        galleryItems.forEach((item, index) => {
            if (index >= (currentPage - 1) * limitPerPage && index < currentPage * limitPerPage) {
                item.style.display = `${displayItem}`; // Usar flex ya que los elementos lo requieren
            } else {
                item.style.display = "none";
            }
        });

        // Actualizar ambas paginaciones
        paginations.forEach(pagination => {
            pagination.innerHTML = ""; // Limpiar paginación

            // Agregar botón "Anterior"
            const prev = document.createElement("p");
            prev.className = `page-item previous-page${currentPage === 1 ? " disable" : ""}`;
            prev.innerHTML = `<a class="page-link" href="${blockContainer}"><i class="fa-solid fa-caret-left"></i></a>`;
            prev.addEventListener("click", () => showPage(currentPage - 1));
            pagination.appendChild(prev);

            // Agregar números de página
            getPageList(totalPages, currentPage, paginationSize).forEach(item => {
                const pageItem = document.createElement("p");
                pageItem.className = `page-item ${item ? "current-page" : "dots"}${item === currentPage ? " active" : ""}`;
                pageItem.innerHTML = item
                    ? `<a class="page-link" href="${blockContainer}">${item}</a>`
                    : `<span class="page-link">...</span>`;
                if (item) {
                    pageItem.addEventListener("click", () => showPage(item));
                }
                pagination.appendChild(pageItem);
            });

            // Agregar botón "Siguiente"
            const next = document.createElement("p");
            next.className = `page-item next-page${currentPage === totalPages ? " disable" : ""}`;
            next.innerHTML = `<a class="page-link" href="${blockContainer}"><i class="fa-solid fa-caret-right"></i></a>`;
            next.addEventListener("click", () => showPage(currentPage + 1));
            pagination.appendChild(next);
        });

        // Volver a agregar el desplazamiento ajustado a los enlaces
        addScrollToPaginationLinks();

        return true;
    }

    function addScrollToPaginationLinks() {
        document.querySelectorAll('.ctlg_pagination a').forEach(link => {
            link.addEventListener('click', function(event) {
                event.preventDefault(); // Prevenir el comportamiento predeterminado del enlace
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    const headerHeight = document.querySelector('header').offsetHeight;
                    const targetPosition = target.getBoundingClientRect().top + window.scrollY; // Posición relativa al documento
                    window.scrollTo({
                        top: targetPosition - headerHeight, // Ajustar con el alto del header
                        behavior: 'smooth' // Desplazamiento suave
                    });
                }
            });
        });
    }

    // Inicializar ambas paginaciones
    showPage(1);
});
