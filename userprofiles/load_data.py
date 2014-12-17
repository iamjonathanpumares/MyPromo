# -*- encoding: utf-8 -*-
csv_filepathname="C:\Users\JonathanEmmanuel\Documents\usuarios.csv"
import csv
from django.contrib.auth.models import User, Group



def importarCSV(archivo_csv):
	dataReader = csv.reader(archivo_csv, delimiter=',', quotechar='"')
	for row in dataReader:
		if row[0] != 'matricula': # ignoramos la primera línea del archivo CSV
			usuario = User()
			usuario.username = row[0]
			usuario.first_name = row[1].encode('utf-8')
			usuario.last_name = row[2].encode('utf-8')
			usuario.set_password = row[3]
			usuario.save()
			group_usuario = Group.objects.get(name='Usuario')
			usuario.groups.add(group_usuario)
			usuario.save()
