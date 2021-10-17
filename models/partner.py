# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Partner(models.Model):
    _inherit = 'res.partner'

    instructor = fields.Boolean("Instructor", default=False)
    id_sesiones = fields.Many2many('openacademy.sesions', string="Sesiones atendidas", readonly=True)