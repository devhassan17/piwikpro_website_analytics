{
    'name': "Piwik PRO Website Analytics (Odoo 18)",
    'version': "18.0.1.1.0",
    'summary': "Piwik PRO container injection + ecommerce dataLayer events for Odoo Website Sale",
    'category': "Website",
    'author': "Managemyweb.co",
    'license': "LGPL-3",
    'depends': ["website", "website_sale"],
    'data': ["security/ir.model.access.csv", "views/piwikpro_menu.xml", "views/piwikpro_config_views.xml", "views/templates_head.xml", "views/templates_events.xml"],
    'assets': {"web.assets_frontend": ["piwikpro_website_analytics/static/src/js/piwikpro_frontend.js"]},
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
