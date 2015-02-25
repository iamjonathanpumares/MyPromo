# -*- encoding: utf-8 -*-
from __future__ import absolute_import

from celery import shared_task

import csv
from django.contrib.auth.models import User, Group
from django.db import IntegrityError, transaction
from .models import UsuarioFinal
from async_messages import messages

from datetime import date
from cupones.models import Cupon
from promociones.models import Promocion

@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)

@shared_task
def importarCSV(dataReader, usuario_actual):
	group = Group.objects.get(name='UsuarioFinal')
	user_current = User.objects.get(username=usuario_actual)
	for row in dataReader:
		if row[0] != 'ID': # ignoramos la primera línea del archivo CSV
			commit = True
			usuario = User()
			usuario.username = row[0]
			usuario.set_password(row[0])
			usuario.first_name = row[1]
			usuario.last_name = row[2]
			usuario.email = row[3]
			if commit:
				try:
					with transaction.atomic():
						usuario.save()
						usuario.groups.add(group)		
				except IntegrityError:
					pass
				else:
					usuario_final = UsuarioFinal(user=usuario)
					usuario_final.save()
	messages.info(user_current, "La base de datos ha sido cargada completamente")
	return True

@shared_task
def convertirCSV(data):
	dataReader = csv.reader(data, delimiter=',', quotechar='"')
	lista_externa = []
	for row in dataReader:
		lista_interna = []
		lista_interna.append(row[0])
		lista_interna.append(row[1])
		lista_interna.append(row[2])
		lista_interna.append(row[3])
		lista_externa.append(lista_interna)
	return lista_externa

@shared_task
def cambiarStatus():
	hoy = date.today()
	fecha_actual = str(hoy.year) + "-" + str(hoy.month) + "-" + str(hoy.day)
	Cupon.objects.filter(vigencia__lt=fecha_actual).update(status='Inactivo')
	Promocion.objects.filter(vigencia__lt=fecha_actual).update(status='Inactivo')