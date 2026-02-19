# Piwik PRO Website Analytics (Odoo 18)

This module injects a Piwik PRO container script into your website `<head>` and sends GA4-like ecommerce dataLayer events for Odoo `website_sale`.

## Features
- Dedicated configuration menu: Website → Piwik PRO → Configuration
- Stores settings in `piwikpro.config` and mirrors to `ir.config_parameter` for template access
- Inject container script (domain + container id)
- Ecommerce events:
  - view_item (product page)
  - add_to_cart (best-effort via fetch interception)
  - view_cart (/shop/cart)
  - begin_checkout (/shop/checkout)
  - purchase (confirmation page) with full order totals + line items (server-side accurate)

## Notes
- In Piwik PRO Tag Manager, create triggers matching:
  - view_item, add_to_cart, view_cart, begin_checkout
  - purchase event name from config (default: piwik_order)
- Configure your Ecommerce Order tag to map:
  - Order ID: {{ ecommerce }}.transaction_id
  - Grand total: {{ ecommerce }}.value
  - Currency: {{ ecommerce }}.currency
  - Product array: {{ ecommerce }}.items

