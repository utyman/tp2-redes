Para compilar e instalar los paquetes necesarios:

make 

Se necesita tener instalado python y python-tk. 
Instrucciones para instalar python-tk para la creación de gráficos automática:

http://www.tkdocs.com/tutorial/install.html

(se puede obtener por lo general de los repositorios de paquetes. Por ejemplo en ubuntu sudo apt-get install python-tk)

Modo de uso:

(ip)

sudo python ./traceroute.py 133.3.250.46

(dominio)

sudo python ./traceroute.py www.google.com

Los paquetes de python que usa se encuentran en requirements.txt (en caso de que se quiera probar en Windows hay que instalar esos paquetes)
