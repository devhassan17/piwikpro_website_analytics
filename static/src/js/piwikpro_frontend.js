/** Piwik PRO - Website Sale events (Odoo 18)
 *  - add_to_cart via fetch interception to /shop/cart/update
 *  Uses window.PIWIKPRO_CFG + global dlPush from head injection.
 */
(function () {
    function shouldBlockForDnt() {
        try {
            if (!window.PIWIKPRO_CFG || !window.PIWIKPRO_CFG.respectDnt) return false;
            return (navigator && (navigator.doNotTrack === "1" || navigator.doNotTrack === "yes"));
        } catch (e) { return false; }
    }

    if (shouldBlockForDnt()) return;

    const cfg = window.PIWIKPRO_CFG || {};
    if (!cfg.enableAddToCart) return;

    const originalFetch = window.fetch;
    if (!originalFetch) return;

    window.fetch = function () {
        return originalFetch.apply(this, arguments).then((response) => {
            try {
                const url = arguments[0];
                const urlStr = (typeof url === "string") ? url : (url && url.url ? url.url : "");

                // Odoo website_sale cart update endpoint
                if (urlStr && urlStr.indexOf("/shop/cart/update") !== -1) {
                    response.clone().json().then((data) => {
                        // data format varies; attempt best-effort mapping
                        if (!data) return;

                        // If Odoo returns a product_id (some configurations do), use it
                        const productId = data.product_id || data.productId || (data.line && data.line.product_id);
                        const qty = Number(data.quantity || data.add_qty || (data.line && data.line.quantity) || 1) || 1;

                        // In some Odoo builds, the payload doesn't include product details.
                        // We still push event with what we have; purchase event is accurate server-side.
                        dlPush({
                            event: "add_to_cart",
                            ecommerce: {
                                currency: data.currency || "EUR",
                                items: [{
                                    item_id: productId ? String(productId) : "unknown",
                                    item_name: data.product_name || data.productName || "Unknown product",
                                    price: Number(data.price || data.unit_price || 0) || 0,
                                    quantity: qty
                                }]
                            }
                        });
                    }).catch(() => {});
                }
            } catch (e) {}
            return response;
        });
    };
})();
