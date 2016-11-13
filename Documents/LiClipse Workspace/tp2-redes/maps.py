from motionless import VisibleMap, DecoratedMap, LatLonMarker
from dns.rdatatype import NULL
import polyline

def obtenerMapa(latLongs):
    """Obtener un mapa con las localizaciones
    """
    camino = [] 
    
    indice = 1
    dmap = DecoratedMap(scale=4)
    for latLong in latLongs:
        if latLong == 0:
            continue
            
        if latLong == None: 
            indice = indice+1
            continue
        info = latLong.split(",")
        dmap.add_marker(LatLonMarker(info[0], info[1]))
        camino.append((float(info[0]), float(info[1])))
        indice = indice+1
            
    enc = polyline.encode(camino, 5)

    return dmap.generate_url() + '&path=weight:3%7Ccolor:orange%7Cenc:' + enc