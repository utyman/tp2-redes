# traceroute.py
import logging
from location import obtenerInformacionIP
import sys
import location
from time import time #importamos la bliblioteca para calcular tiempos
import cimbala 
from maps import obtenerMapa
from urllib2 import urlopen
from cimbala import calcularDesvioStandard, calcularDiferenciaPromedio
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
import matplotlib.pyplot as plt



if len(sys.argv)!= 2:
    print "uso: ./traceroute.py www.google.com"
    print sys.argv
    sys.exit(1)
ttl=1
TO=1 #Valor maximo de espera de la respuesta
destino=sys.argv[1]
cantidad_de_traceroutes = 40
# Dentro de RTT master van a estar los RTT promediados.
RTT_master = []
RTT_master_cant = []
# Lo llenamos de 0's (como mucho el numero equivalente a la cota de ttl.)
for i in range(0,29):
    RTT_master.append(0)
    RTT_master_cant.append(0)

# Hago traceroute 40 veces (tiempo arbitrario de monitoreo considerado suficiente)
for iteracion_traceroute in range(0,cantidad_de_traceroutes):
    print("\n")
    print "Monitoreo: " + str(iteracion_traceroute)
    print("=========================================")
    hop = []
    RTT = []
    locs = []
    fin=0
    # obtenemos nuestro ip 
    mi_ip = urlopen('http://ip.42.pl/raw').read()
    print "Ubicacion de origen: "
    locs.append(obtenerInformacionIP(mi_ip))
    print "\n"
    
    paquete=IP(dst=destino,ttl=ttl) / ICMP() #Manda paquete ICMP. El default es echo-request. A
    RTT_suma=0
    RTT_cant=0        

    # ttl 0
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
         RTT.append(0) # el primer salto tendria que responder casi siempre. Si no lo consideramos inmediato
         RTT_master[ttl] += 0
         RTT_master_cant[ttl] += 1
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
            RTT.append(RTT[-1]) # se tomo tomar como RTT entre saltos el ultimo RTT en caso de que el nodo no responda 
                                # time exceeded
            RTT_master[ttl] += (RTT[-1])
            RTT_master_cant[ttl] += 1
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
                
    print "\nInformacion final traceroute:"
    print "=============================\n"
    print "RTTs: " + str(RTT)
    print "Desvio standard: " +  str(calcularDesvioStandard(cimbala.obtenerDiferenciasRTT(RTT)))
    print "Candidatos Outliers (indice del salto empezando en 0 (nodo 1 -> nodo 2) y con eliminacion): " + str(cimbala.cimbala(RTT))
    print "(Xi - media) / S: " + str(calcularDiferenciaPromedio(cimbala.obtenerDiferenciasRTT(RTT)))
    print "hops: " + str(hop)
    print "url mapa: " + str(obtenerMapa(locs))
    ttl=1

# Calculo el promedio dividiendo cada suma de RTT's por la cantidad de veces que hicimos traceroute y el RTT no fue 0.
RTT_promediados = []
for i in range(0,len(RTT_master)):
    if RTT_master_cant[i] != 0:
        RTT_promediados.append(RTT_master[i] /  RTT_master_cant[i])
# Nota: RTT tendra el promedio de los promedios de las rafagas para cada ttl. Ignorar los 0's.
print("\n")
print("Informacion del promedio del monitoreo de varios traceroutes")
print("============================================================")
print "RTTs por TTL promediados entre saltos : " + str(RTT_promediados)
print "RTTs entre saltos promediados entre saltos : " + str(cimbala.obtenerDiferenciasRTT(RTT_promediados))
print "Desvio standard promediado monitoreo: " +  str(cimbala.obtenerDiferenciasRTT(RTT_promediados))
print "Candidatos Outliers (indice del salto empezando en 0 (nodo 1 -> nodo 2) y con eliminacion) promediado: " + str(cimbala.cimbala(RTT_promediados))
print "(Xi - media) / S: " + str(calcularDiferenciaPromedio(cimbala.obtenerDiferenciasRTT(RTT_promediados)))
plt.plot(cimbala.obtenerDiferenciasRTT(RTT_promediados))
plt.ylabel('RTT promediados entre saltos')
plt.xlabel('Salto')
plt.title('RTT entre saltos (Promedio)')
plt.savefig('RTT_promediados.png', bbox_inches='tight')
plt.close()
plt.plot(calcularDiferenciaPromedio(cimbala.obtenerDiferenciasRTT(RTT_promediados)))
plt.ylabel('(Xi - media)/S')
plt.xlabel('Salto')
plt.title('Desvio relativo del salto con respecto a la media')
plt.savefig('desvio_media.png', bbox_inches='tight')
