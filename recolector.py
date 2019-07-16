import requests
import lxml.etree
import lxml.html
import re
import math
from datetime import datetime as dt, timezone

cookies = {
        #'cpttxhHQrES2eWopmC6e+yrKFa1G': 'v1RbeGSQSDF6E',
        #'PHPSESSID': '435f4d82f91fadf6703deaaad3d68e69',
        }

headers = {
        #'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
        #'Accept': '*/*',
        #'Accept-Language': 'en-US,en;q=0.5',
        #'Referer': 'https://www.sicoes.gob.bo/portal/contrataciones/busqueda/convocatorias.php?tipo=convNacional',
        #'DNT': '1',
        #'Connection': 'keep-alive',
        }

def getTK(sesion):
    ret = sesion.get('https://www.sicoes.gob.bo/lib/download/tk.php')
    return ret

def proord(A, c, s, w, x): 
    i = len(A)
    B = s
    j = 0
    if (i % 2 == 0):
        j = math.floor(i / 2) - 1
    else:
        j = Math.floor(i / 2)
    y = 0
    z = []
    for u in range(i):
        z.insert(u,0)
    for v in range(c, j):
        for t in range(i):
            y = y + B
            if (y >= i):
                y = y - i
            z[t] = A[y]
        for t in range(i):
            A[t] = z[t]
    if ((i == 3 and s == 2) or (i == 4 and s == 3) or (i == 7 and s == 6) or (i == 8 and s == 7) or (i == 12 and s == 11) or (i == 15 and s == 14) or (i == 16 and s == 15) or (i == 19 and s == 18) or (i == 20 and s == 19)):
        for u in range(i):
            z[u] = 0
            z[u] = A[u]
        k = 0
        for t in range(i - 1,-1,-1):
            A[k] = z[t]
            k = k + 1
    if ((i == 3 and s == 1) or (i == 4 and s == 1)):
        for u in range(i):
            z[u] = A[u]
        k = 0
        A[0] = z[(i - 1)]
        for t in range( 1, i):
            A[t] = z[(t - 1)]
    return A

def botcolobt(operacion, tipo, timehour, sesion):
    captcha = getTK(sesion=sesion)
    data = {
            'opetpo': operacion, # 'convNacional','convInternacional','contResueltos','desistimientoCont'
            'tpoope': tipo,      # 'Simple','Avanzada'
            'time': timehour
            }
    ret =  sesion.post('https://www.sicoes.gob.bo/portal/contrataciones/operacion2.php', data=data)
    return ( ret, captcha )

def getRutaColumnasContrataciones(operacion, tipo, sesion):
    ruta = "/portal/contrataciones/operacion.php"
    rpto = botcolobt(operacion, tipo, int(dt.now().replace(tzinfo=timezone.utc).timestamp()), sesion=sesion )
    columnastmp = rpto[0].json()['sectorsec']
    columnas = proord(columnastmp, rpto[0].json()['a'], rpto[0].json()['b'], rpto[0].json()['fx'], rpto[0].json()['fy'])
    return [ruta, columnas, rpto[1]]

def getRutaColumnasADJ(operacion, tipo):
    return getRutaColumnasContrataciones(operacion, tipo)

def getDatos(operacion, tipo, columnas, ruta, pag, captcha, sesion, b9 ):
    c = re.compile(r"ntv\s*=\s*'([a-zA-Z0-9]+)'\s*;vtv\s*=\s'([a-zA-Z0-9]+)'\s*;")
    d = re.findall(c, captcha.text)[0]
    e = re.compile(r"%([A-F0-9]{2})")
    data = {
            'arpcDespliegue': 'option3',
            'B903A6B7': b9,
            'captcha': '',
            'codigoContrato': '',
            'codigoDpto': '',
            'codigoModalidad': '',
            'codigoNormativa': '',
            'costoPlieDespliegue': 'option3',
            'cuce1': '',
            'cuce2': '',
            'cuce3': '',
            'cuce4': '',
            'cuce5': '',
            'cuce6': '',
            'desiertaDesde': '',
            'desiertaHasta': '',
            'dptoDespliegue': 'option3',
            'draw': str(pag),
            'entidad': '',
            'fechaAdjudicacionDespliegue': 'option2',
            'fechaReunionDespliegue': 'option1',
            'length': '10',
            'montoDesde': '',
            'montoHasta': '',
            'nomtoGarDespliegue': 'option2',
            'normativaDespliegue': 'option3',
            'nroContrato': '',
            'nroRegistros': '10',
            'objetoContrato': '',
            'operacion': operacion,
            'personaContDespliegue': 'on',
            'presentacionPropuestasDesde': '',
            'presentacionPropuestasHasta': '',
            'publicacionDesde': '',
            'publicacionHasta': '',
            'r1': '11',
            'start': '0',
            #'bienes': 'B',
            #'obras': 'O',
            #'servicios': 'S',
            #'consultoria': 'C',
            d[0]: d[1]
            }
    res = sesion.post('https://www.sicoes.gob.bo' + ruta, data=data).json()
    r1 = []
    try:
      for a in res.get('data'):
        c=[]
        for b in columnas:
            c.append( bytes.fromhex( ''.join(re.findall(e, a[b] ) ) ).decode('ISO_8859-1') )
        r1.append(c)
    except:
        print(res)
    return {'datos':r1,'recordsTotal':res.get('recordsTotal')}

# r = getRutaColumnasContrataciones('convNacional', 'Simple')
#getDatos(columnas=r[1],ruta=r[0],operacion='convNacional',tipo='Simple')


def convNacional():
    tipo = 'Avanzada'
    s = requests.Session()
    s.headers.update({'Referer': 'https://www.sicoes.gob.bo/portal/contrataciones/busqueda/convocatorias.php?tipo=convNacional',
                      'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'})
    index = s.get("https://www.sicoes.gob.bo/portal/contrataciones/busqueda/convocatorias.php?tipo=convNacional")
    b52=re.compile(r'name="B903A6B7" value="([0-9A-F]+)"')
    b53 = b52.findall(index.text)
    if len(b53) < 4:
        index = s.get("https://www.sicoes.gob.bo/portal/contrataciones/busqueda/convocatorias.php?tipo=convNacional")
    b53 = b52.findall(index.text)
    r = getRutaColumnasContrataciones(operacion='convNacional', tipo=tipo, sesion=s)
    total = 1
    pag = 1
    while(pag<=total):
      r = getRutaColumnasContrataciones(operacion='convNacional', tipo=tipo, sesion=s)
      datos = getDatos(columnas=r[1],ruta=r[0],operacion='convNacional',tipo=tipo, sesion=s, captcha=r[2], pag=pag, b9=b53[2])
      total = int(datos['recordsTotal'])/10
      pag = pag + 1
      #index = s.get("https://www.sicoes.gob.bo/portal/contrataciones/busqueda/convocatorias.php?tipo=convNacional")
      #b52=re.compile(r'name="B903A6B7" value="([0-9A-F]+)"')
      #b53 = b52.findall(index.text)
      #b53 = [b53[2]]
      #print(b53)
 
      print(datos)
      print("Pagina")
      print(pag)
      print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")

