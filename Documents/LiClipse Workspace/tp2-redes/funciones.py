from location import *
import logging
import location
import sys
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *


def mostrarruta(hop,RTT,fin,mi_ip):
    print "Ubicacion de origen: "
    mostrarInformacionIP(mi_ip)

    for nodo in range(0,len(hop)):
        print "\nttl: " + str(nodo+1)
        if RTT[nodo]==0: #Timeout.
            print "No se obtuvo una respuesta al paquete ICMP enviado (timeout)"
        else:
            mostrarInformacionIP(hop[nodo])
            if fin==1 and nodo==len(hop)-1:
                print "Se obtuvo una respuesta al paquete enviado. (Echo Reply)"
            else:
                if fin==0 and nodo==len(hop)-1:
                    print "No se logro alcanzar el destino en menos de 30 saltos."
                else:
                    print "Se obtuvo una respuesta al paquete enviado. (Time exceeded)"
        print "RTT promedio del nodo entre todas las iteraciones: : " + str(RTT[nodo])  


def mostrarinfofinal(RTT,hop,mi_ip):
    print "\nInformacion final:"
    print "Salto        IP         RTT promediado entre todas las iteraciones"
    width=18

    print str(0).rjust(7) + str(mi_ip).rjust(16) + "    " + str(0).rjust(20)
      
    for nodo in range(0,len(hop)):
        print str(nodo+1).rjust(7) + str(hop[nodo]).rjust(16) + "    " + str(RTT[nodo]).rjust(20)


def eliminarcerosfinales(RTT):
    while RTT[len(RTT)-1] == 0:
        RTT.pop()
    
    return RTT


def RTTpromedio(ttl,TO,fin,destino,hop,locs, RTT_master,RTT_master_cant):
    paquete=IP(dst=destino,ttl=ttl) / ICMP() #Manda paquete ICMP. El default es echo-request
    RTT_suma=0 #Sumador de RRT para los que respondieron time exceeded en cada salto.
    RTT_cant=0 #Contador que indica los que respondieron time exceeded en cada salto.

    for p in range (0,5): # Enviamos 5 paquetes en tiempos distintos por cada ttl.

         tpri=time.time()     
         resp,noresp=sr(paquete,timeout=TO, verbose=False) #Recibe varias respuestas. Solo consideramos la primera

         if len(resp)!=0: #No salio por timeout
             if (resp[0][1].type==11): #Time exceeded
                 tactual=time.time()
                 if RTT_cant==0:
                     hop[ttl-1] = (resp[0][1].src) #IP destino del primer paquete recibido con time exceeded
                     locs[ttl-1] = (obtenerInformacionIP(resp[0][1].src)) #Guardamos informacion del primer paquete recibido con time exceeded
                 RTT_suma += tactual - tpri #Para el promedio consideramos solo los que respondieron time exceeded.
                 RTT_cant += 1 #Para el promedio consideramos solo los que respondieron time exceeded.
             else:
                 tactual=time.time()
                 if RTT_cant==0:
                     hop[ttl-1] = (resp[0][1].src) #IP destino del primer paquete recibido con time exceeded
                     locs[ttl-1] = (obtenerInformacionIP(resp[0][1].src)) #Guardamos informacion del primer paquete recibido con time exceeded
                 RTT_suma += tactual - tpri #Para el promedio consideramos solo los que respondieron time exceeded.
                 RTT_cant += 1 #Para el promedio consideramos solo los que respondieron time exceeded y el echo reply.
 
                 if (resp[0][1].type==0):
                     #print "Se obtuvo una respuesta al paquete enviado. (Echo Reply)"
                     fin=1
                 #else:
                     #print "Se obtuvo una respuesta al paquete enviado. Codigo: " + str(resp[0][1].type)

    if RTT_cant==0: #Todos los paquetes de este ttl dieron timeout.
        if hop[ttl-1] == 0:
            hop[ttl-1] = ("*")
           #RTT.append(-1)
            #print "No se obtuvo una respuesta al paquete ICMP enviado (timeout)"
    else:
            #RTT.append(RTT_suma/RTT_cant) #Se agrega el promedio de los RTT del nodo en la lista de RTT.
        RTT_master[ttl-1] += (RTT_suma/RTT_cant) #Se suma el promedio de los RTT del nodo para el promedio de todas las iteraciones.
        RTT_master_cant[ttl-1] += 1
            #if fin==1:
                #print "Se obtuvo una respuesta al paquete enviado. (Echo Reply)"
            #else:
         #print "Se obtuvo una respuesta al paquete enviado. (Time exceeded)"
                
    print "\nttl: " + str(ttl) + " IP: " + str(hop[ttl-1]) + " RTT Promedio rafaga: " + str(RTT_master[ttl-1]) 
    return fin
