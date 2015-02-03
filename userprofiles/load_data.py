# -*- encoding: utf-8 -*-
csv_filepathname="C:\Users\JonathanEmmanuel\Documents\usuarios.csv"
import csv
from django.contrib.auth.models import User
from .models import UsuarioFinal



def importarCSV(archivo_csv):
	dataReader = csv.reader(archivo_csv, delimiter=',', quotechar='"')
	dataWriter = csv.writer(archivo_csv, delimiter=',', quotechar='"')
	for row in dataReader:
		if row[0] != 'matricula': # ignoramos la primera línea del archivo CSV
			commit = True
			usuario = User()
			usuario.username = row[0]
			usuario.set_password(row[0])
			usuario.first_name = row[1]
			usuario.last_name = row[2]
			usuario.email = row[3]
			if commit:
				usuario.save()
				usuario_final = UsuarioFinal(user=usuario)
				usuario_final.save()

def writerCSV(archivo_csv):
	dataReader = csv.reader(archivo_csv, delimiter=',', quotechar='"')
	dataWriter = csv.writer(archivo_csv, delimiter=',', quotechar='"')
	new_password = User.objects.make_random_password()
	#dataWriter.writerow(("00106612", "Jonathan Emmanuel", "Pumares Chab", "jepc1491@gmail.com", new_password))
	for row in dataReader:
		new_password = User.objects.make_random_password()
		username = row[0]
		first_name = row[1]
		last_name = row[2]
		email = row[3]
		dataWriter.writerow((username, first_name, last_name, email, new_password))

