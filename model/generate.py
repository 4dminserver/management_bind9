#!/usr/bin/python
#-*-coding:utf-8-*-
#- adminServer
#- regenerate Bind Class

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

import sqlite3

class generate(object):
	@staticmethod
	def all(domain_id, conectionBrain):
		
		if str(domain_id) == 'all':
			conectionBrain = sqlite3.connect('modules/management_bind9/brain/bind9.db')
			cursor = conectionBrain.cursor()
			cursor.execute("SELECT * FROM dns WHERE status = '1'")
		else:
			cursor = conectionBrain.cursor()
			cursor.execute("SELECT * FROM dns WHERE id = '" + str(domain_id) + "'")

		for info in cursor:
			domain_name = str(info[1])
			email = str(info[2])
			ip_server = str(info[3])
			ns_primary = str(info[4])
			ns_secundary =  str(info[5])
			server_mail = str(info[6])
			type_zone = str(info[9])
			ip_transfer =  str(info[10])
			domain_key = ''
			spf = ip_server

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
			save.close()

		cursor.execute("SELECT domain, type_zone, ip_transfer FROM dns WHERE status = '1'")
		zones = open('/etc/bind/named.conf.local', 'w')
		zones.write("""//
// Do any local configuration here
//

// Consider adding the 1918 zones here, if they are not used in your
// organization
//include "/etc/bind/zones.rfc1918";\n\n""")

		for domain in cursor:
			zones.write('''zone "''' + domain[0] + '''" {
	type ''' + domain[1] + ''';
	allow-transfer {''' + domain[2] + ''';};
	file "/etc/bind/pri.''' + domain[0] + '''";
};\n\n''')
		zones.close()