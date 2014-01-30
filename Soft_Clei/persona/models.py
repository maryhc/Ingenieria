#*****************************************************************************
#  persona.models
# Clase: Persona
# Descripcion : modelo que implementa a las personas que participan en  el CLEI
#
# Autores : 
#           David Lilue       #  carnet: 09-10444
#           Veronica Linayo   #  carnet: 08-10615
#           Audry Morillo     #  carnet: 07-41253
#           Vanessa Rivas     #  carnet: 10-10608
#           Michael Woo       #  carnet: 09-10912
#
# Grupo :1, 3, 4 
# Seccion : 1
#
#*****************************************************************************


from django.db import models

class Persona(models.Model):
    cedula               = models.IntegerField()
    nombre               = models.CharField(max_length=100)
    apellido             = models.CharField(max_length=100)
    institucion_afiliada = models.CharField(max_length=100)
    email                = models.EmailField(max_length=50)
    pais                 = models.CharField(max_length=100)

    def __str__(self):
        """ Metodo : __str__
        Parametros : self
        Descripcion: Metodo que permite mostrar en un string caracteristicas del objero
        """
        return str(self.nombre) + " " + str(self.apellido) + ", " + str(self.cedula)
