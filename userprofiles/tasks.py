# -*- encoding: utf-8 -*-
from __future__ import absolute_import

from celery import shared_task

import csv
from django.contrib.auth.models import User, Group
from django.db import IntegrityError, transaction
from .models import UsuarioFinal


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
def importarCSV(dataReader):
	group = Group.objects.get(name='UsuarioFinal')
	for row in dataReader:
		if row[0] != 'ID': # ignoramos la primera línea del archivo CSV
			commit = True
			usuario = User()
			usuario.save()
			usuario.username = row[0]
			usuario.set_password(row[0])
			usuario.first_name = row[1]
			usuario.last_name = row[2]
			usuario.email = row[3]
			usuario.groups = group
			if commit:
				try:
					with transaction.atomic():
						usuario.save()
				except IntegrityError:
					pass
				else:
					usuario_final = UsuarioFinal(user=usuario)
					usuario_final.save()
	return True

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