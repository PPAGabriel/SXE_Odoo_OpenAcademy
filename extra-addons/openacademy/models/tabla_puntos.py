from odoo import fields, models

class TestPuntos(models.Model):
    _name = "test_points"
    _description = "Segunda tabla de prueba con puntos"

    namePoints = fields.Char(string="Nombre en Interfaz")
    points = fields.Integer(string="Puntos en Interfaz")