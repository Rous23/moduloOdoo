# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import models, fields, api, exceptions


class Sesions(models.Model):
    _name = 'openacademy.sesions'

    name = fields.Char(string="Nombre", required=True)
    date = fields.Date(default=fields.Date.today)
    duration = fields.Float(digits=(5,1))
    asientos = fields.Integer(string="Numero de Asientos")
    active = fields.Boolean(default=True)
    color = fields.Integer()

    instructor_id = fields.Many2one('res.partner', ondelete='set null', string="Instructor", domain=['|',('instructor','=',True), ('category_id.name', 'ilike', "Teacher")])

    id_course = fields.Many2one('openacademy.courses', ondelete='cascade',string="Curso", required=True)

    id_asistente = fields.Many2many('res.partner', string="Asistentes")

    asientos_ocupados = fields.Float('Asientos Ocupados', compute="_asientos_ocupados")
    fecha_final = fields.Date(string="Finalización", store=True,
        compute='_get_fecha_final', inverse='_set_fecha_final')

    horas = fields.Float(string="Horas de duración", compute='_get_horas', inverse='_set_horas')

    cant_asistentes = fields.Integer(
        string="Cantidad de participantes", compute='_get_cant_asistentes', store=True)

    @api.depends('asientos', 'id_asistente')
    def _asientos_ocupados(self):
        for record in self:
            if not record.asientos:
                record.asientos_ocupados = 0.0
            else:
                record.asientos_ocupados = 100.0 * len(record.id_asistente) / record.asientos

    @api.onchange('asientos', 'id_asistente')
    def _valores_validos(self):
        if self.asientos < 0:
            return {
                'warning': {
                    'title': "Valor incorrecto",
                    'message': "Escriba un número válido.",
                }
            }
        
        if self.asientos < len(self.id_asistente):
            return {
                'warning': {
                    'title': "Muchos asientos",
                    'message': "Aumentar o eliminar exceso de asientos.",
                }
            }

    @api.constrains('instructor_id', 'id_asistente')
    def _verificacion_instrucctor(self):
        for r in self:
            if r.instructor_id and r.instructor_id in r.id_asistente:
                raise exceptions.ValidationError("El instructor no puede ser un asistente")

    @api.depends('date', 'duration')
    def _get_fecha_final(self):
        for r in self:
            if not (r.date and r.duration):
                r.fecha_final = r.date
                continue

            start = fields.Datetime.from_string(r.date)
            duration = timedelta(days=r.duration, seconds=-1)
            r.fecha_final = start + duration

    @api.depends('date', 'duration')
    def _set_fecha_final(self):
        for r in self:
            if not (r.date and r.fecha_final):
                continue

            start_date = fields.Datetime.from_string(r.date)
            fecha_final = fields.Datetime.from_string(r.fecha_final)
            r.duration = (fecha_final - start_date).days + 1

    @api.depends('duration')
    def _get_horas(self):
        for r in self:
            r.horas = r.duration * 24

    def _set_horas(self):
        for r in self:
            r.duration = r.horas / 24

    @api.depends('id_asistente')
    def _get_cant_asistentes(self):
        for r in self:
            r.cant_asistentes = len(r.id_asistente)
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
