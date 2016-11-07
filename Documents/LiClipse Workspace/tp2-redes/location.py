import re
import json
from urllib2 import urlopen


def obtenerInformacionIP(IP):
    url = 'http://ipinfo.io/' + IP + '/json'
    response = urlopen(url)
    data = json.load(response)
    
    if 'bogon' in data.keys() or IP.startswith('192.168') or IP.startswith('10.0') or IP.startswith('172.16'):
        print 'IP: ' + str(IP)
        print 'Direccion bogon o interna'
        return None
    
    if 'org' in data.keys():
        org=data['org']
    else:
        org=""
    
    loc=data['loc']
    ciudad = data['city']
    pais=data['country']
    region=data['region']
    
    print 'IP : {4} \nRegion : {1} \nCountry : {2} \nCity : {3} \nOrg : {0}'.format(org,region,pais,ciudad,IP)
    return loc