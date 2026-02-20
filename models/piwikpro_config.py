# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PiwikProConfig(models.Model):
    _name = "piwikpro.config"
    _description = "Piwik PRO Configuration"
    _rec_name = "name"

    name = fields.Char(required=True, default="Piwik PRO")
    active = fields.Boolean(default=True)

    # Piwik PRO container settings
    container_url = fields.Char(
        string="Container Base URL",
        help="Example: https://moyeecoffee.containers.piwik.pro"
    )
    container_id = fields.Char(
        string="Container ID",
        help="Example: 5b868fbc-c24b-4102-8ea5-7669666a7699"
    )

    data_layer_name = fields.Char(
        string="Data Layer Name",
        default="dataLayer",
        help="Usually 'dataLayer'. Use a custom name only if needed."
    )

    purchase_event_name = fields.Char(
        string="Purchase Event Name",
        default="piwik_order",
        help="Must match the Data Layer Event trigger name in Piwik PRO Tag Manager."
    )

    @api.constrains("container_url")
    def _check_container_url(self):
        # Keep it simple; do not hard-block install if empty.
        # Users may configure after installing.
        pass
