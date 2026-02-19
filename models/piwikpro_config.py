from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

PARAM_PREFIX = "piwikpro."

class PiwikProConfig(models.Model):
    """
    Singleton-ish config model (1 record recommended).
    Values are stored on the record itself (so you can edit easily),
    and mirrored to ir.config_parameter so website templates & JS can read without sudo issues.
    """
    _name = "piwikpro.config"
    _description = "Piwik PRO Configuration"
    _rec_name = "name"

    name = fields.Char(default="Piwik PRO", required=True)
    active = fields.Boolean(default=False)

    container_domain = fields.Char(
        string="Container Domain",
        help="Example: moyeecoffee.containers.piwik.pro (no protocol, no trailing slash)."
    )
    container_id = fields.Char(
        string="Container ID",
        help="Example: 5b868fbc-c24b-4102-8ea5-7669666a7699"
    )
    data_layer_name = fields.Char(default="dataLayer", help="Default: dataLayer")
    purchase_event_name = fields.Char(default="piwik_order", help="Event name listened by Piwik PRO trigger.")
    enable_view_item = fields.Boolean(default=True)
    enable_add_to_cart = fields.Boolean(default=True)
    enable_view_cart = fields.Boolean(default=True)
    enable_begin_checkout = fields.Boolean(default=True)
    enable_purchase = fields.Boolean(default=True)

    # Optional: advanced
    respect_dnt = fields.Boolean(string="Respect DNT / Opt-out", default=True)

    @api.constrains("container_domain")
    def _check_domain(self):
        for rec in self:
            if rec.container_domain and "://" in rec.container_domain:
                raise ValidationError(_("Container Domain must not include protocol (https://)."))
            if rec.container_domain and rec.container_domain.endswith("/"):
                raise ValidationError(_("Container Domain must not end with '/'."))

    @api.model
    def get_active_config(self):
        cfg = self.search([("active", "=", True)], limit=1)
        return cfg

    def _param_set(self, key, value):
        self.env["ir.config_parameter"].sudo().set_param(PARAM_PREFIX + key, value if value is not None else "")

    def _mirror_to_params(self):
        self.ensure_one()
        self._param_set("active", "1" if self.active else "0")
        self._param_set("container_domain", self.container_domain or "")
        self._param_set("container_id", self.container_id or "")
        self._param_set("data_layer_name", self.data_layer_name or "dataLayer")
        self._param_set("purchase_event_name", self.purchase_event_name or "piwik_order")
        self._param_set("enable_view_item", "1" if self.enable_view_item else "0")
        self._param_set("enable_add_to_cart", "1" if self.enable_add_to_cart else "0")
        self._param_set("enable_view_cart", "1" if self.enable_view_cart else "0")
        self._param_set("enable_begin_checkout", "1" if self.enable_begin_checkout else "0")
        self._param_set("enable_purchase", "1" if self.enable_purchase else "0")
        self._param_set("respect_dnt", "1" if self.respect_dnt else "0")

    @api.model_create_multi
    def create(self, vals_list):
        recs = super().create(vals_list)
        for rec in recs:
            rec._mirror_to_params()
        return recs

    def write(self, vals):
        res = super().write(vals)
        for rec in self:
            rec._mirror_to_params()
        return res

    def action_open(self):
        """Convenience action for menu."""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Piwik PRO Configuration"),
            "res_model": "piwikpro.config",
            "view_mode": "form",
            "res_id": self.id,
            "target": "current",
        }
