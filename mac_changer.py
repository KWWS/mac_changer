#!/usr/bin/env python

import subprocess
import optparse
import re
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface do endereco MAC a ser alterado")
    parser.add_option("-m", "--mac", dest="new_mac", help="Novo endereco MAC a ser aplicado")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Por favor, especifique uma interface, use --help para mais info.")
    elif not options.new_mac:
        parser.error("[-] Por favor, especifique um novo MAC, use --help para mais info.")
    return options

def change_mac(interface, new_mac):
    print("[+] Mudando o endereco MAC " + interface + " para " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])
def get_current_mac(interface):
    ifconfig_result_bytes = subprocess.check_output(["ifconfig", interface])
    ifconfig_result_str = ifconfig_result_bytes.decode('utf-8')
    print(ifconfig_result_str)
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result_str)
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Nao foi possivel ler o endereco MAC")

options = get_arguments()

current_mac = get_current_mac(options.interface)
print("MAC atual = " + str(current_mac))

change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] Endereco MAC foi alterado com sucesso para " + current_mac)
else:
    print("[-] Endereco MAC nao foi alterado")

