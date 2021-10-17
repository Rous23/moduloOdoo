# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions


class Courses(models.Model):
    _name = 'openacademy.courses'
    _description = 'openacademy modulo odoo'

    name = fields.Char(string='Titulo')
    description = fields.Html(string='Descripción',placeholder="breve descripcion")
    
    id_responsable = fields.Many2one('res.users',ondelete='set null',string="Responsable")
    id_sesion = fields.One2many('openacademy.sesions','id_course',string="Sesión")
    
    def copiar(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', u"Copy of {}%".format(self.name))])
        if not copied_count:
            nuevo_nombre = u"Copy of {}".format(self.name)
        else:
            nuevo_nombre = u"Copy of {} ({})".format(self.name, copied_count)

        default['name'] = nuevo_nombre
        return super(Courses, self).copy(default)
    
    _sql_constraints = [
        ('name_description_check', 'CHECK(name != description)', "El titulo no puede ser una descripción."),

        ('name_unique','UNIQUE(name)',"El título debe ser unico"),
    ]
    