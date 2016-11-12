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
TO=3 #Valor maximo de espera de la respuesta
destino=sys.argv[1]
cantidad_de_traceroutes = 40
# Dentro de RTT master van a estar los RTT promediados.
RTT_master = []
RTT_master_cant = []
# Lo llenamos de 0's (como mucho el numero equivalente a la cota de ttl.)
for i in range(0,29):
    RTT_master.append(0)
    RTT_master_cant.append(0)

# Hago traceroute 40 veces (tiempo arbitrario de monitoreo considerado suificiente)
for iteracion_traceroute in range(0,cantidad_de_traceroutes-1):
    hop = []
    RTT = []
    locs = []
    fin=0
    # obtenemos nuestro ip 
    mi_ip = urlopen('http://ip.42.pl/raw').read()
    print "Ubicacion de origen: "
    locs.append(obtenerInformacionIP(mi_ip))
    print "\n"
    
    paquete=IP(dst=destino,ttl=ttl) / ICMP() #Manda paquete ICMP. El default es echo-request. Arma 3 paquetes iguales
    RTT_suma=0
    RTT_cant=0        

    for p in range(0,5):
        tpri=time.time()
        resp,noresp=sr(paquete, verbose=False) #Recibe varias respuestas. Solo consideramos la primera

        if (resp[0][1].type==11): #Time exceeded
            tactual=time.time()
            if RTT_cant==0:
                hop.append(resp[0][1].src) #IP destino del primer paquete recibido con time exceeded
                locs.append(obtenerInformacionIP(resp[0][1].src))
            RTT_suma += tactual - tpri
            RTT_cant = RTT_cant+1
 
    if RTT_cant==0:
         hop.append("*")
         RTT.append(-1)
         print "No se obtuvo una respuesta al paquete ICMP enviado (timeout)"
    else:
         RTT.append(RTT_suma/RTT_cant)
         RTT_master[0] += (RTT_suma/RTT_cant)
         RTT_master_cant[0] += 1
         print "ttl: 1"
         print "Se obtuvo una respuesta al paquete enviado. (Time exceeded)"
              
    while ttl < 30 and (len(resp) == 0 or resp[0][1].type !=0) and fin==0:                    
        ttl=ttl+1
        print "\nttl: " + str(ttl)
        paquete=IP(dst=destino,ttl=ttl) / ICMP() #Manda paquete ICMP. El default es echo-request
        RTT_suma=0
        RTT_cant=0
            
        for p in range (0,5):
            tpri=time.time()     
            resp,noresp=sr(paquete,timeout=TO, verbose=False) #Recibe varias respuestas. Solo consideramos la primera

            if len(resp)!=0: #No salio por timeout
                if (resp[0][1].type==11): #Time exceeded
                    tactual=time.time()
                    if RTT_cant==0:
                        hop.append(resp[0][1].src) #IP destino del primer paquete recibido con time exceeded
                        locs.append(obtenerInformacionIP(resp[0][1].src))
                    RTT_suma += tactual - tpri
                    RTT_cant += 1
                else:
                    tactual=time.time()
                    if RTT_cant==0:
                        hop.append(resp[0][1].src) #IP destino del primer paquete recibido con time exceeded
                        locs.append(obtenerInformacionIP(resp[0][1].src))
                    RTT_suma += tactual - tpri
                    RTT_cant += 1
    
                    if (resp[0][1].type==0):
                        print "Se obtuvo una respuesta al paquete enviado. (Echo Reply)"
                        fin=1
                    else:
                        print "Se obtuvo una respuesta al paquete enviado. Codigo: " + str(resp[0][1].type)

        if RTT_cant==0:
            hop.append("*")
            RTT.append(-1)
            print "No se obtuvo una respuesta al paquete ICMP enviado (timeout)"
        else:
            RTT.append(RTT_suma/RTT_cant)
            RTT_master[ttl] += (RTT_suma/RTT_cant)
            RTT_master_cant[ttl] += 1
            if fin==1:
                print "Se obtuvo una respuesta al paquete enviado. (Echo Reply)"
            else:
                print "Se obtuvo una respuesta al paquete enviado. (Time exceeded)"
                
            print "RTT: " + str(RTT_suma/RTT_cant)           
                
    print "\nInformacion final:"
    print "RTTs: " + str(RTT)
#PONER    print "Candidatos Outliers (indice del salto empezando en 0 y con eliminacion): " + str(cimbala.cimbala(RTT))
    print "hops: " + str(hop)
#z    print "url mapa: " + str(obtenerMapa(locs))
    print "url mapa: " + str(obtenerMapa(locs))
    ttl=1

# Calculo el promedio dividiendo cada suma de RTT's por la cantidad de veces que hicimos traceroute y el RTT no fue 0.
for i in range(0,30):
    RTT_master[i] = RTT_master[i] /  RTT_master_cant[i]
# Nota: RTT Promediados asume que tardaste 30 ttl. Por eso, tendra 0's dependiendo de cuantos menos ttl's tardaste. Ignorar los 0's.
print "RTTs Promediados: " + str(RTT_master)