# traceroute.py
import logging
from location import obtenerInformacionIP
import sys
import location
from time import time #importamos la bliblioteca para calcular tiempos
import cimbala
from maps import obtenerMapa
from urllib2 import urlopen
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *



if len(sys.argv)!= 2:
    print "uso: ./traceroute.py www.google.com"
    print sys.argv
    sys.exit(1)
ttl=1
TO=3 #Valor maximo de espera de la respuesta VER CUAL SERIA UN VALOR RAZONABLE
destino=sys.argv[1]
cantidad_de_traceroutes = 40
# Dentro de RTT master van a estar los RTT promediados.
RTT_master = [] 
# Lo lleno de 0's (como mucho el numero equivalente a la cota de ttl.)
for i in range(0,29):
    RTT_master.append(0)

# Hago traceroute 40 veces (tiempo arbitrario de monitoreo considerado suificiente)
for iteracion_traceroute in range(0,cantidad_de_traceroutes-1):
    hop = []
    RTT = []
    locs = []
    paquete=IP(dst=destino,ttl=ttl) / ICMP() #Manda paquete ICMP. El default es echo-request
    tanterior=time.time()
    resp,noresp=sr(paquete, verbose=False) #Recibe todas las respuestas. Solo estoy considerando una

    #FALTA VER COMO SE COMPORTA SI CORTA POR TIMEOUT

    # obtengo mi ip 
    mi_ip = urlopen('http://ip.42.pl/raw').read()
    print "Ubicacion de origen: "
    locs.append(obtenerInformacionIP(mi_ip))
    print "\n"
    #Explicacion estructura
    #print resp[0].display() #Mensaje enviado
    #print resp[0].type
    #print resp[1].display() #Mensaje de vuelta

    if (resp[0][1].type==11): #Time exceeded
        tactual=time.time()    
        hop.append(resp[0][1].src) #IP destino del paquete recibido
        dif = tactual - tanterior
        print "ttl: 1"
        print "Se obtuvo una respuesta al paquete enviado. (Time exceeded)"
        locs.append(obtenerInformacionIP(resp[0][1].src))
        
        RTT.append(tactual - tanterior)
        RTT_master[0] += (tactual - tanterior)
        tanterior=tactual
    else:
        hop.append("*")
        print "No se obtuvo una respuesta al paquete ICMP enviado (timeout)"
        obtenerInformacionIP(resp[0][1].src)
        RTT.append(0)
        RTT_master[0] += 0
        
    while ttl < 30 and (len(resp) == 0 or resp[0][1].type !=0):                    
        ttl=ttl+1
        print "\nttl: " + str(ttl)
        paquete=IP(dst=destino,ttl=ttl) / ICMP() #Manda paquete ICMP. El default es echo-request
        resp,noresp=sr(paquete,timeout=TO, verbose=False) #Recibe la primer respuesta
        if len(resp)==0: #Salio por timeout
            hop.append("*")
            print "No se obtuvo una respuesta al paquete ICMP enviado (timeout)"
            RTT.append(RTT[-1])
            RTT_master[ttl] += RTT[-1]
        else:
            if (resp[0][1].type==11): #Time exceeded
                tactual=time.time()
                hop.append(resp[0][1].src) #IP destino del paquete recibido
                print "Se obtuvo una respuesta al paquete enviado. (Time exceeded)"
                locs.append(obtenerInformacionIP(resp[0][1].src))
                print "Delta RTT: " + str(tactual - tanterior)
                RTT.append(tactual - tanterior)
                RTT_master[ttl] += (tactual - tanterior)
                tanterior=tactual
            else:
                hop.append(resp[0][1].src)
                if (resp[0][1].type==0):
                    print "Se obtuvo una respuesta al paquete enviado. (Echo Reply)"
                else:
                    print "Se obtuvo una respuesta al paquete enviado. Codigo: " + str(resp[0][1].type)
                locs.append(obtenerInformacionIP(resp[0][1].src))
                RTT_master[ttl] += RTT[-1]                
                RTT.append(RTT[-1])
                
    print "\nInformacion final:"
    print "RTTs: " + str(RTT)
    print "Candidatos Outliers (indice del salto empezando en 0 y con eliminacion): " + str(cimbala.cimbala(RTT)) 
    print "hops: " + str(hop)
    print "url mapa: " + str(obtenerMapa(locs))
    ttl=1

# Calculo el promedio dividiendo cada suma de RTT's por la cantidad de veces que hice traceroute
for i in range(0,29):
    RTT_master[i] = RTT_master[i] / cantidad_de_traceroutes
# Nota: RTT Promediados asume que tardaste 30 ttl. Por eso, tendra 0's dependiendo de cuantos menos ttl's tardaste. Ignorar los 0's.
print "RTTs Promediados: " + str(RTT_master)