#!/usr/bin/python
#-*-coding:utf-8-*-
#- utility Bind Class

#- AdminServer / System Management Server
#- Copyright (C) 2014 GoldraK & Interhack 
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License 
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. 
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty 
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. 
# You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>

# WebSite: http://adminserver.org/
# Email: contacto@adminserver.org
# Facebook: https://www.facebook.com/pages/Admin-Server/795147837179555?fref=ts
# Twitter: https://twitter.com/4dminserver

import sys, os
sys.path.append('modules/management_bind9/model')
from generate import generate

class utility(object):
	@staticmethod
	def edit_domain(translate, output, id_domain, conectionBrain, log):
		cursor = conectionBrain.cursor()
		cursor.execute("SELECT * FROM dns WHERE id = '" + id_domain + "'")
		for info in cursor:
			_ = translate

			domain_name = raw_input('Domain Name [' + info[1] + ']: ')
			email = raw_input('Email Contact [' + info[2] + ']: ')
			ip_server = raw_input('Ip Server [' + info[3] + ']: ')
			ns_primary = raw_input('NS Primary [' + info[4] + ']: ')
			ns_secundary =  raw_input('NS Secundary [' + info[5] + ']: ')
			if str(info[6]) == '1':
				valor = 'y'
			else:
				valor = 'n'
			server_mail = raw_input('Server Mail [' + str(valor) + ']: ')
			type_zone = raw_input('Type Zone [' + info[9] + ']: ')
			ip_transfer =  raw_input('Ip transfer [' + info[10] + ']: ')
			domain_key = ''
			spf = ip_server

			control = False

			valores = ''

			if domain_name != "":
				control = True
				valores += "domain = '" + str(domain_name) + "', "

			if email != "":
				control = True
				valores += "email = '" + str(email) + "', "

			if ip_server != "":
				control = True
				valores += "ipserver = '" + str(ip_server) + "', "
			
			if ns_primary != "":
				control = True
				valores += "NS_primary = '" + str(ns_primary) + "', "
			
			if ns_secundary != "":
				control = True
				valores += "NS_secundary = '" + str(ns_secundary) + "', "
			
			if server_mail !="":
				control = True
				if server_mail == 'y':
					e_server = '1'
				else:
					e_server = '0'
				valores += "email_server = '" + str(e_server) + "', "
			
			if type_zone !="":
				control = True
				valores += "type_zone = '" + str(type_zone) + "', "
			
			if ip_transfer != "":
				control = True
				valores += "ip_transfer = '" + str(ip_transfer) + "', "
			
			if control == True:
				final = valores + 'F'
				cursor.execute("UPDATE dns SET "  + final.split(', F')[0] + " WHERE id = '" + str(info[0]) + "'")
				conectionBrain.commit()
				generate.all(str(info[0]), conectionBrain)
				log.write(_('Edit Domain ') + str(domain_name))

	@staticmethod
	def delete_domain(translate, output, id_domain, conectionBrain, log):
		_ = translate
		sentencia = raw_input('disable[0]/delete[1]: [0] ')
		while sentencia != '0' and sentencia != '1':
			output.error(_('Option not valid'))
			sentencia = raw_input('disable[0]/delete[1]: [0] ')
		cursor = conectionBrain.cursor()
		cursor.execute("SELECT domain FROM dns WHERE id = '" + str(id_domain) + "'")
		for info in cursor:
			domain = info[0]

		if sentencia == '0':
			cursor.execute("UPDATE dns SET status = '0' WHERE id = '" + id_domain + "'")
		else:
			cursor.execute("DELETE FROM dns WHERE id = '" + id_domain + "'")
		conectionBrain.commit()
		os.system('rm -f /etc/bind/pri.' + domain)
		generate.all('all', conectionBrain)
		log.write(_('Delete Domain ') + str(domain))

	@staticmethod
	def activate_domain(translate, output, id_domain, conectionBrain, log):
		_ = translate
		cursor = conectionBrain.cursor()
		cursor.execute("UPDATE dns SET status = '1' WHERE id = '" + str(id_domain) + "'")
		conectionBrain.commit()
		generate.all(id_domain, conectionBrain)
		log.write(_('Activate domain'))