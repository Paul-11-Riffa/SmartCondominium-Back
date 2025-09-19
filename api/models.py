from django.db import models


class Rol(models.Model):
    id = models.SmallAutoField(primary_key=True, db_column="Id")
    descripcion = models.TextField(null=True, blank=True, db_column="Descripcion")
    tipo = models.TextField(null=True, blank=True, db_column="Tipo")
    estado = models.TextField(null=True, blank=True, db_column="Estado")

    class Meta:
        managed = False
        db_table = "Rol"

    def __str__(self):
        return self.descripcion or f"Rol {self.id}"


class Usuario(models.Model):
    codigo = models.BigAutoField(primary_key=True, db_column="Codigo")
    nombre = models.TextField(null=True, blank=True, db_column="Nombre")
    apellido = models.TextField(null=True, blank=True, db_column="Apellido")
    correo = models.TextField(null=True, blank=True, db_column="Correo")
    contrasena = models.TextField(null=True, blank=True, db_column="Contrasena")
    sexo = models.TextField(null=True, blank=True, db_column="Sexo")
    telefono = models.IntegerField(null=True, blank=True, db_column="Telefono")
    estado = models.TextField(null=True, blank=True, db_column="Estado")
    idrol = models.ForeignKey(
        "Rol",
        models.DO_NOTHING,
        null=True,
        blank=True,
        db_column="IdRol",
        related_name="usuarios",
    )

    class Meta:
        managed = False
        db_table = "Usuario"

    def __str__(self):
        return f"{self.nombre or ''} {self.apellido or ''}".strip() or f"Usuario {self.codigo}"


class Propiedad(models.Model):
    codigo = models.SmallAutoField(primary_key=True, db_column="Codigo")
    tamano_m2 = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True, db_column="Tamano m2"
    )
    nro_casa = models.SmallIntegerField(null=True, blank=True, db_column="NroCasa")
    piso = models.SmallIntegerField(null=True, blank=True, db_column="Piso")
    descripcion = models.TextField(null=True, blank=True, db_column="Descripcion")

    class Meta:
        managed = False
        db_table = "Propiedad"

    def __str__(self):
        return f"Propiedad {self.codigo}"


class Multa(models.Model):
    id = models.SmallAutoField(primary_key=True, db_column="Id")
    descripcion = models.TextField(null=True, blank=True, db_column="Descripcion")
    monto = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, db_column="Monto")

    class Meta:
        managed = False
        db_table = "Multa"

    def __str__(self):
        return f"Multa {self.id}"


class Pagos(models.Model):
    id = models.SmallAutoField(primary_key=True, db_column="Id")
    tipo = models.TextField(null=True, blank=True, db_column="Tipo")
    descripcion = models.TextField(null=True, blank=True, db_column="Descripcion")
    monto = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, db_column="Monto")

    class Meta:
        managed = False
        db_table = "Pagos"

    def __str__(self):
        return f"Pago {self.id} - {self.tipo or ''}".strip()


class Notificaciones(models.Model):
    id = models.SmallAutoField(primary_key=True, db_column="Id")
    tipo = models.TextField(null=True, blank=True, db_column="Tipo")
    descripcion = models.TextField(null=True, blank=True, db_column="Descripcion")

    class Meta:
        managed = False
        db_table = "Notificaciones"

    def __str__(self):
        return f"Notificación {self.id}"


class AreasComunes(models.Model):
    id = models.SmallAutoField(primary_key=True, db_column="Id")
    descripcion = models.TextField(null=True, blank=True, db_column="Descripcion")
    costo = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, db_column="Costo")
    capacidad_max = models.SmallIntegerField(null=True, blank=True, db_column="CapacidadMax")
    estado = models.TextField(null=True, blank=True, db_column="Estado")

    class Meta:
        managed = False
        db_table = "AreasComunes"

    def __str__(self):
        return self.descripcion or f"Área {self.id}"


class Tareas(models.Model):
    id = models.SmallAutoField(primary_key=True, db_column="Id")
    tipo = models.TextField(null=True, blank=True, db_column="Tipo")
    descripcion = models.TextField(null=True, blank=True, db_column="Descripcion")
    costos = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, db_column="Costos")
    vigencia = models.SmallIntegerField(null=True, blank=True, db_column="Vigencia")

    class Meta:
        managed = False
        db_table = "Tareas"

    def __str__(self):
        return f"Tarea {self.id}"


class Vehiculo(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="Id")
    nro_placa = models.TextField(null=True, blank=True, db_column="NroPlaca")
    descripcion = models.TextField(null=True, blank=True, db_column="Descripcion")
    estado = models.TextField(null=True, blank=True, db_column="Estado")

    class Meta:
        managed = False
        db_table = "Vehiculo"

    def __str__(self):
        return self.nro_placa or f"Vehículo {self.id}"


class Pertenece(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="Id")
    codigo_usuario = models.ForeignKey(
        "Usuario", models.DO_NOTHING, null=True, blank=True,
        db_column="CodigoUsuario", related_name="pertenencias"
    )
    codigo_propiedad = models.ForeignKey(
        "Propiedad", models.DO_NOTHING, null=True, blank=True,
        db_column="CodigoPropiedad", related_name="pertenentes"
    )
    fecha_ini = models.DateField(null=True, blank=True, db_column="FechaIni")
    fecha_fin = models.DateField(null=True, blank=True, db_column="FechaFin")

    class Meta:
        managed = False
        db_table = "Pertenece"

    def __str__(self):
        return f"Pertenece {self.id}"


class ListaVisitantes(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="Id")
    nombre = models.TextField(null=True, blank=True, db_column="Nombre")
    apellido = models.TextField(null=True, blank=True, db_column="Apellido")
    carnet = models.TextField(null=True, blank=True, db_column="Carnet")
    motivo_visita = models.TextField(null=True, blank=True, db_column="MotivoVisita")
    fecha_ini = models.DateField(null=True, blank=True, db_column="FechaIni")
    fecha_fin = models.DateField(null=True, blank=True, db_column="FechaFin")
    codigo_propiedad = models.ForeignKey(
        "Propiedad", models.DO_NOTHING, null=True, blank=True,
        db_column="CodigoPropiedad", related_name="visitas"
    )

    class Meta:
        managed = False
        db_table = "ListaVisitantes"

    def __str__(self):
        return f"Visitante {self.id}"


class DetalleMulta(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="Id")
    codigo_propiedad = models.ForeignKey(
        "Propiedad", models.DO_NOTHING, db_column="Codigo Propiedad",
        related_name="detalles_multa"
    )
    id_multa = models.ForeignKey(
        "Multa", models.DO_NOTHING, db_column="IdMulta",
        related_name="detalles"
    )
    fecha_emi = models.DateField(null=True, blank=True, db_column="FechaEmi")
    fecha_lim = models.DateField(null=True, blank=True, db_column="FechaLim")

    class Meta:
        managed = False
        db_table = "DetalleMulta"

    def __str__(self):
        return f"DetalleMulta {self.id}"


class Factura(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="Id")
    codigo_usuario = models.ForeignKey(
        "Usuario", models.DO_NOTHING, null=True, blank=True,
        db_column="CodigoUsuario", related_name="facturas"
    )
    id_pago = models.ForeignKey(
        "Pagos", models.DO_NOTHING, null=True, blank=True,
        db_column="IdPago", related_name="facturas"
    )
    fecha = models.DateField(null=True, blank=True, db_column="Fecha")
    hora = models.TimeField(null=True, blank=True, db_column="Hora")
    tipo_pago = models.TextField(null=True, blank=True, db_column="TipoPago")
    estado = models.TextField(null=True, blank=True, db_column="Estado")

    class Meta:
        managed = False
        db_table = "Factura"

    def __str__(self):
        return f"Factura {self.id}"


class Finanzas(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="Id")
    tipo = models.TextField(null=True, blank=True, db_column="Tipo")
    descripcion = models.TextField(null=True, blank=True, db_column="Descripcion")
    monto = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, db_column="Monto")
    fecha = models.DateField(null=True, blank=True, db_column="Fecha")
    origen = models.TextField(null=True, blank=True, db_column="Origen")
    id_factura = models.ForeignKey(
        "Factura", models.DO_NOTHING, null=True, blank=True,
        db_column="IdFactura", related_name="movimientos"
    )

    class Meta:
        managed = False
        db_table = "Finanzas"

    def __str__(self):
        return f"{self.tipo or 'mov'} {self.id}"


class Comunicados(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="Id")
    tipo = models.TextField(null=True, blank=True, db_column="Tipo")
    fecha = models.DateField(null=True, blank=True, db_column="Fecha")
    hora = models.TimeField(null=True, blank=True, db_column="Hora")
    titulo = models.TextField(null=True, blank=True, db_column="Titulo")
    contenido = models.TextField(null=True, blank=True, db_column="Contenido")
    url = models.TextField(null=True, blank=True, db_column="Url")
    estado = models.TextField(null=True, blank=True, db_column="Estado")
    codigo_usuario = models.ForeignKey(
        "Usuario", models.DO_NOTHING, null=True, blank=True,
        db_column="CodigoUsuario", related_name="comunicados"
    )

    class Meta:
        managed = False
        db_table = "Comunicados"

    def __str__(self):
        return self.titulo or f"Comunicado {self.id}"


class Horarios(models.Model):
    id = models.SmallAutoField(primary_key=True, db_column="Id")
    hora_ini = models.TimeField(null=True, blank=True, db_column="HoraIni")
    hora_fin = models.TimeField(null=True, blank=True, db_column="HoraFin")
    id_area_c = models.ForeignKey(
        "AreasComunes", models.DO_NOTHING, null=True, blank=True,
        db_column="IdAreaC", related_name="horarios"
    )

    class Meta:
        managed = False
        db_table = "Horarios"

    def __str__(self):
        return f"Horario {self.id}"


class Reserva(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="ID")
    codigo_usuario = models.ForeignKey(
        "Usuario", models.DO_NOTHING, null=True, blank=True,
        db_column="CodigoUsuario", related_name="reservas"
    )
    id_area_c = models.ForeignKey(
        "AreasComunes", models.DO_NOTHING, null=True, blank=True,
        db_column="IdAreaC", related_name="reservas"
    )
    fecha = models.DateField(null=True, blank=True, db_column="Fecha")
    estado = models.TextField(null=True, blank=True, db_column="Estado")

    class Meta:
        managed = False
        db_table = "Reserva"

    def __str__(self):
        return f"Reserva {self.id}"


class Asignacion(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="Id")
    codigo_usuario = models.ForeignKey(
        "Usuario", models.DO_NOTHING, null=True, blank=True,
        db_column="CodigoUsuario", related_name="asignaciones"
    )
    id_tarea = models.ForeignKey(
        "Tareas", models.DO_NOTHING, null=True, blank=True,
        db_column="IdTarea", related_name="asignaciones"
    )
    fecha_ini = models.DateField(null=True, blank=True, db_column="FechaIni")
    fecha_fin = models.DateField(null=True, blank=True, db_column="FechaFin")
    descripcion = models.TextField(null=True, blank=True, db_column="Descripcion")
    costo = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, db_column="Costo")
    dificultades = models.TextField(null=True, blank=True, db_column="Dificultades")
    estado = models.TextField(null=True, blank=True, db_column="Estado")

    class Meta:
        managed = False
        db_table = "Asignacion"

    def __str__(self):
        return f"Asignación {self.id}"


class Envio(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="Id")
    codigo_usuario = models.ForeignKey(
        "Usuario", models.DO_NOTHING, null=True, blank=True,
        db_column="CodigoUsuario", related_name="envios"
    )
    id_notific = models.ForeignKey(
        "Notificaciones", models.DO_NOTHING, null=True, blank=True,
        db_column="IdNotific", related_name="envios"
    )
    fecha = models.DateField(null=True, blank=True, db_column="Fecha")
    hora = models.TimeField(null=True, blank=True, db_column="Hora")
    estado = models.TextField(null=True, blank=True, db_column="Estado")

    class Meta:
        managed = False
        db_table = "Envio"

    def __str__(self):
        return f"Envio {self.id}"


class Registro(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="Id")
    codigo_usuario = models.ForeignKey(
        "Usuario", models.DO_NOTHING, null=True, blank=True,
        db_column="CodigoUsuario", related_name="registros"
    )
    id_vehic = models.ForeignKey(
        "Vehiculo", models.DO_NOTHING, null=True, blank=True,
        db_column="IdVehic", related_name="registros"
    )
    fecha = models.DateField(null=True, blank=True, db_column="Fecha")
    hora = models.TimeField(null=True, blank=True, db_column="Hora")

    class Meta:
        managed = False
        db_table = "Registro"

    def __str__(self):
        return f"Registro {self.id}"


class Bitacora(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="Id")
    ip = models.TextField(null=True, blank=True, db_column="IP")
    accion = models.TextField(null=True, blank=True, db_column="Accion")
    fecha = models.DateField(null=True, blank=True, db_column="Fecha")
    hora = models.TimeField(null=True, blank=True, db_column="Hora")
    codigo_usuario = models.ForeignKey(
        "Usuario", models.DO_NOTHING, null=True, blank=True,
        db_column="CodigoUsuario", related_name="bitacora"
    )

    class Meta:
        managed = False
        db_table = "Bitacora"

    def __str__(self):
        return f"Bitácora {self.id}"
