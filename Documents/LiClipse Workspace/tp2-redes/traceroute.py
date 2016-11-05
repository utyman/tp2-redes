# traceroute.py
import logging
#import pkt_utils
#import inf_utils
#import plac
import sys
from time import time #importamos la bliblioteca para calcular tiempos

#from clint.textui import colored, puts
logging.getLogger("scapy.runtime").setLevel(logging.ERROR) 
from scapy.all import *

if len(sys.argv)!= 2:
    print "uso: ./traceroute.py www.google.com"
    print sys.argv
    sys.exit(1)

destino=sys.argv[1]
hop = []
RTT = []

ttl=1
TO=3 #Valor maximo de espera de la respuesta VER CUAL SERIA UN VALOR RAZONABLE
paquete=IP(dst=destino,ttl=ttl) / ICMP() #Manda paquete ICMP. El default es echo-request
tanterior=time.time()
resp,noresp=sr(paquete) #Recibe todas las respuestas. Solo estoy considerando una

#FALTA VER COMO SE COMPORTA SI CORTA POR TIMEOUT

#Explicacion estructura
#print resp[0].display() #Mensaje enviado
#print resp[0].type
#print resp[1].display() #Mensaje de vuelta

if (resp[0][1].type==11): #Time exceeded
    tactual=time.time()    
    hop.append(resp[0][1].src) #IP destino del paquete recibido
    dif = tactual - tanterior
    print resp[0][1].type,ttl,(tactual - tanterior)
    RTT.append(tactual - tanterior)
    tanterior=tactual
else:
    hop.append("*")
    print resp[0][1].type,ttl
    RTT.append(-1)
    
while resp[0][1].type !=0:
    ttl=ttl+1
    paquete=IP(dst=destino,ttl=ttl) / ICMP() #Manda paquete ICMP. El default es echo-request
    resp,noresp=sr(paquete,timeout=TO) #Recibe la primer respuesta
    if len(resp)==0: #Salio por timeout
        hop.append("*")
    else:
        if (resp[0][1].type==11): #Time exceeded
            tactual=time.time()
            hop.append(resp[0][1].src) #IP destino del paquete recibido
            print resp[0][1].type,ttl,"TE",(tactual - tanterior)
            RTT.append(tactual - tanterior)
            tanterior=tactual
        else:
            hop.append("*")
            RTT.append(-1)
            print resp[0][1].type,ttl,"`"
            
print "echo reply"

#hop[ttl]=resp.src #IP destino del paquete recibido
        
#if __name__ == '__main__':
    #import plac; plac.call(main)
