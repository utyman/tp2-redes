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
    region_str = region.encode("utf-8")
    print 'IP : ' + str(IP)
    print 'Region: '+ region_str
    print 'Country: ' + str(pais)
    print 'City: ' + str(ciudad)
    print 'Org: ' + str(org)
    return loc