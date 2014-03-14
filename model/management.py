#!/usr/bin/python
#-*-coding:utf-8-*-
#- Add Bind Class

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

import sqlite3, sys
sys.path.append('model')
from teco import color

class management(object):
	
	@staticmethod
	def add_dns(translate, log):
		_ = translate
		domain_name = raw_input(_('Domain Name: '))
		while domain_name == "":
			domain_name = raw_input(_('Domain Name: '))
		email = raw_input(_('Email Contact: '))
		while email == "":
			email = raw_input(_('Email Contact: '))
		ip_server = raw_input(_('Ip Server: '))
		while ip_server == "":
			ip_server = raw_input(_('Ip Server: '))
		ns_primary = raw_input(_('NS Primary: '))
		while ns_primary == "":
			ns_primary = raw_input(_('NS Primary: '))
		ns_secundary =  raw_input(_('NS Secundary: '))
		while ns_secundary == "":
			ns_secundary =  raw_input(_('NS Secundary: '))
		server_mail = raw_input(_('Server Mail [y/N]: '))
		type_zone = raw_input(_('Type Zone [master]:'))
		ip_transfer =  raw_input(_('Ip transfer: '))
		while ip_transfer == "":
			ip_transfer =  raw_input(_('Ip transfer: '))
		domain_key = ''
		spf = ip_server

		if server_mail == 'y':
			server_mail = '1'
		else:
			server_mail = '0'

		if type_zone == '':
			type_zone = 'master'

		conectionBrain = sqlite3.connect('modules/management_bind9/brain/bind9.db')
		bind = conectionBrain.cursor()
		bind.execute("INSERT INTO dns (domain, email, ipserver, NS_primary, NS_secundary, email_server, domain_key, SFP, type_zone, ip_transfer, status) VALUES ('" + domain_name + "', '" + email + "', '" + ip_server + "', '" + ns_primary + "', '" + ns_secundary + "', '" + str(server_mail) + "', '" + domain_key + "', '" +  ip_server + "', '" +  str(type_zone) + "', '" +  str(ip_transfer) + "', '1')")
		conectionBrain.commit()

		if spf != '':
			spf_save = '''@       IN      TXT     "v=spf1 ip4:''' + spf +''' ~all"'''
		else:
			spf_save = ""
		if server_mail == '1':
			email_server_save = '''mail 3600 A        ''' + ip_server
			mx_email_save = domain_name + '''. 3600      MX    10   mail.''' + domain_name + '''.'''
		else:
			spf_save = ""
			email_server_save = ""
			mx_email_save = ""

		save = open('/etc/bind/pri.' + domain_name, 'w')
		save.write("""$TTL        3600
@       IN      SOA     """ + domain_name +""". """ + email.replace('@', '.') +""". (
                        2013061702       ; serial, todays date + todays serial 
                        7200              ; refresh, seconds
                        540              ; retry, seconds
                        604800              ; expire, seconds
                        86400 )            ; minimum, seconds
;
""" + spf_save + """

""" + domain_key + """

""" + email_server_save + """
stats 3600 A        """ + ip_server + """
""" + domain_name +""". 3600 A        """ + ip_server + """
""" + mx_email_save + """
""" + domain_name +""". 3600      NS        """ + ns_primary +""".
""" + domain_name +""". 3600      NS        """ + ns_secundary +""".
www 3600 A        """+ ip_server)


		bind.execute("SELECT domain, type_zone, ip_transfer FROM dns WHERE status = '1'")
		zones = open('/etc/bind/named.conf.local', 'w')
		zones.write("""//
// Do any local configuration here
//

// Consider adding the 1918 zones here, if they are not used in your
// organization
//include "/etc/bind/zones.rfc1918";\n\n""")

		for domain in bind:
			zones.write('''zone "''' + domain[0] + '''" {
	type ''' + domain[1] + ''';
	allow-transfer {''' + domain[2] + ''';};
	file "/etc/bind/pri.''' + domain[0] + '''";
};\n\n''')
		log.write(_('Add Domain ') + str(domain_name))

	@staticmethod
	def edit_dns(translate, output, log):
		_ = translate
		conectionBrain = sqlite3.connect('modules/management_bind9/brain/bind9.db')
		bind = conectionBrain.cursor()
		bind.execute("SELECT id, domain FROM dns WHERE status = '1'")
		contador = 0
		domains_active = {}
		for domain in bind:
			contador +=1
			domains_active[domain[0]] = domain[1]

		for domain in domains_active:
			output.default(str(domain) + ' - ' + domains_active[domain])
		output.default("0 - Exit")

		control = True
		while control == True:
			sentencia = raw_input("bind9[edit] >> ")
			try:
				if int(sentencia) < 0:
					output.default(_('Must be a positive number'))
				elif sentencia == '0':
					control = False
				
				elif domains_active[int(sentencia)]:
					sys.path.append('modules/management_bind9/model')
					from utility import utility
					utility.edit_domain(_, output, sentencia, conectionBrain, log)
					control = False
			except:
				output.error(_('Must be listed'))

	@staticmethod
	def delete_dns(translate, output, log):
		_ = translate
		conectionBrain = sqlite3.connect('modules/management_bind9/brain/bind9.db')
		bind = conectionBrain.cursor()
		bind.execute("SELECT id, domain FROM dns WHERE status = '1'")
		contador = 0
		domains_active = {}
		for domain in bind:
			contador +=1
			domains_active[domain[0]] = domain[1]

		for domain in domains_active:
			output.default(str(domain) + ' - ' + domains_active[domain])
		output.default("0 - Exit")

		control = True
		while control == True:
			sentencia = raw_input("bind9[delete] >> ")
			try:
				if int(sentencia) < 0:
					output.default(_('Must be a positive number'))
				elif sentencia == '0':
					control = False
				
				elif domains_active[int(sentencia)]:
					sys.path.append('modules/management_bind9/model')
					from utility import utility
					utility.delete_domain(_, output, sentencia, conectionBrain, log)
					control = False
			except:
				output.error(_('Must be listed'))

	@staticmethod
	def activate_dns(translate, output, log):
		_ = translate
		conectionBrain = sqlite3.connect('modules/management_bind9/brain/bind9.db')
		bind = conectionBrain.cursor()
		bind.execute("SELECT id, domain FROM dns WHERE status = '0'")
		contador = 0
		domains_active = {}
		for domain in bind:
			contador +=1
			domains_active[domain[0]] = domain[1]

		for domain in domains_active:
			output.default(str(domain) + ' - ' + domains_active[domain])
		output.default("0 - Exit")

		control = True
		while control == True:
			sentencia = raw_input("bind9[activate] >> ")
			try:
				if int(sentencia) < 0:
					output.default(_('Must be a positive number'))
				elif sentencia == '0':
					control = False
				
				elif domains_active[int(sentencia)]:
					sys.path.append('modules/management_bind9/model')
					from utility import utility
					utility.activate_domain(_, output, sentencia, conectionBrain, log)
					control = False
			except:
				output.error(_('Must be listed'))

	@staticmethod
	def reload_service(translate, output, log):
		import subprocess
		_ = translate
		output.default(color('magenta',_('Restarting Service...') + 'Bind9'))
		command_restart = '/etc/init.d/bind9 restart'
		restart = subprocess.Popen(command_restart, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		restart_error = restart.stderr.read()
		if restart_error != '': 
			output.error(color('rojo',_('Failed to restart service')))
			log.write(_('Failed to restart service'), 1)
		else:
			output.default(color('verde', _('Restart service ok')))
			log.write(_('Restart service ok'))