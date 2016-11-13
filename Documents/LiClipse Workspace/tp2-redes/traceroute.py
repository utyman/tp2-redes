# traceroute.py
import logging
import location
import funciones
from location import obtenerInformacionIP
from funciones import *
import sys
from time import time #importamos la bliblioteca para calcular tiempos
import cimbala 
from maps import obtenerMapa
from urllib2 import urlopen
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *

if len(sys.argv)!= 2:
    print "uso: ./traceroute.py www.google.com"
    print "     o ./traceroute.py 181.15.221.226"
    sys.exit(1)

ttl=1
TO=1 #Valor maximo de espera de la respuesta
destino=sys.argv[1]
cantidad_de_traceroutes = 1

# Dentro de RTT master van a estar los RTT promediados.
RTT_master = [] #Sumador de RRT promedio que respondieron time exceeded en cada salto entre todas las iteraciones.
RTT_master_cant = [] #Contador que indica los RTT promedio que respondieron time exceeded en cada salto entre todas las iteraciones.
hop = [] # Guarda la IP destino de cada salto
locs = []
    
# Lo llenamos de 0's (como mucho el numero equivalente a la cota de ttl.)
for i in range(0,30):
    RTT_master.append(0)
    RTT_master_cant.append(0)
    hop.append(0)
    locs.append(0)

# obtenemos nuestro ip 
mi_ip = urlopen('http://ip.42.pl/raw').read()
locs[ttl-1] = (obtenerInformacionIP(mi_ip))
        
# Hacemos traceroute 40 veces (tiempo arbitrario de monitoreo considerado suificiente)
for iteracion_traceroute in range(0,cantidad_de_traceroutes):
    fin=0 # Indica si ya llegamos a destino
               
    while ttl < 30 and (fin==0):                    
        fin=RTTpromedio(ttl,TO,fin,destino,hop,locs,RTT_master,RTT_master_cant)
        ttl=ttl+1

    ttl=1

# Calculo el promedio dividiendo cada suma de RTT's promedio por la cantidad de veces que hicimos traceroute y el RTT no fue 0.
for i in range(0,30):
    if RTT_master_cant[i] !=0:
        RTT_master[i] = RTT_master[i] /  RTT_master_cant[i]

RTT_master=eliminarcerosfinales(RTT_master)
hop=eliminarcerosfinales(hop)
locs=eliminarcerosfinales(locs)

# Mostramos ruta a destino
mostrarruta(hop,RTT_master,fin,mi_ip)
# Mostramos informacion final
mostrarinfofinal(RTT_master,hop,mi_ip)

print "Candidatos Outliers (indice del salto empezando en 0 y con eliminacion): " + str(cimbala.cimbala(RTT_master))
locs.insert(0, obtenerInformacionIP(mi_ip))
print "url mapa: " + str(obtenerMapa(locs))


# se imprimen los graficos
imprimirGraficos(RTT_master)