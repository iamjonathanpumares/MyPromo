# -*- encoding: utf-8 -*-
csv_filepathname="C:\Users\JonathanEmmanuel\Documents\usuarios.csv"
import csv
from django.contrib.auth.models import User
from .models import UsuarioFinal



def importarCSV(archivo_csv):
	dataReader = csv.reader(archivo_csv, delimiter=',', quotechar='"')
	for row in dataReader:
		if row[0] != 'matricula': # ignoramos la primera línea del archivo CSV
			commit = True
			usuario = User()
			usuario.username = row[0]
			usuario.first_name = row[1]
			usuario.last_name = row[2]
			usuario.set_password(row[3])
			if commit:
				usuario.save()
				usuario_final = UsuarioFinal(user=usuario)
				usuario_final.save()
