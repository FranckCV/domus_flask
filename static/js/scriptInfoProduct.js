document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.product').forEach(product => {
        const productLink = product.getAttribute('data-link');
        const productPicture = product.getAttribute('data-picture');
        const productName = product.getAttribute('data-name');

        const productPriceRegular = parseFloat(product.getAttribute('data-price-regular'));
        const numberRegular = Math.floor(productPriceRegular);
        const decimalRegular = Math.round((productPriceRegular % 1) * 100);

        const productPriceOnline = parseFloat(product.getAttribute('data-price-Online'));
        const numberOnline = Math.floor(productPriceOnline);
        const decimalOnline = Math.round((productPriceOnline % 1) * 100);

        const productPriceForSale = parseFloat(product.getAttribute('data-price-ForSale'));
        const numberForSale = Math.floor(productPriceForSale);
        const decimalForSale = Math.round((productPriceForSale % 1) * 100);

        const productInfo = product.querySelector('.product_info');
        
        productInfo.href = productLink;
        
        productInfo.innerHTML = 
        `<img class="product_pic" src="${productPicture}" alt="${productName}">
        <p class="product_name">            
            ${productName}
        </p>                                    
        ` + addRegularProductCardInfo() + `
        <div class="product_price price_online">
            <p class="product_price_title">
                Online
            </p>                    
            <p class="product_price_number">
                S/. ${numberOnline}
                <sup>.${decimalOnline}</sup>
            </p>
        </div>        
        ` + addForSaleProductCardInfo();

        function addRegularProductCardInfo() {
            const htmlRegular =
            `<div class="product_price price_regular">
                <p class="product_price_title">
                    Regular
                </p>                    
                <p class="product_price_number">
                    S/. ${numberRegular}
                    <sup>.${decimalRegular}</sup>
                </p>
            </div>`;

            if (productPriceRegular) {
                return htmlRegular;
            } else {
                return "";
            }
        };

        function addForSaleProductCardInfo() {
            const htmlForSale =
            `<div class="product_price price_for_sale">
                <p class="product_price_title">
                    Oferta
                </p>                    
                <p class="product_price_number">
                    S/. ${numberForSale}
                    <sup>.${decimalForSale}</sup>
                </p>
            </div>`;

            if (productPriceForSale) {
                return htmlForSale;
            } else {
                return "";
            }
        };

        

    });
});













