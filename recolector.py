import requests
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

def getTK():
    return requests.get('https://www.sicoes.gob.bo/lib/download/tk.php', headers=headers, cookies=cookies)

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

def botcolobt(operacion, tipo, timehour):
    data = {
            'opetpo': operacion, # 'convNacional',
            'tpoope': tipo,      # 'Simple',
            'time': timehour
            }
    return requests.post('https://www.sicoes.gob.bo/portal/contrataciones/operacion2.php', headers=headers, cookies=cookies, data=data)

def getRutaColumnasContrataciones(operacion, tipo):
    ruta = "/portal/contrataciones/operacion.php"
    rpto = botcolobt(operacion, tipo, int(dt.now().replace(tzinfo=timezone.utc).timestamp()))
    columnastmp = rpto.json()['sectorsec']
    columnas = proord(columnastmp, rpto.json()['a'], rpto.json()['b'], rpto.json()['fx'], rpto.json()['fy'])
    return [ruta, columnas]

def getRutaColumnasADJ(operacion, tipo):
    return getRutaColumnasContrataciones(operacion, tipo)

def getDatos(operacion, tipo, columnas, ruta, pag ):
    captcha = getTK()
    c = re.compile(r"ntv\s*=\s*'([a-zA-Z0-9]+)'\s*;vtv\s*=\s'([a-zA-Z0-9]+)'\s*;")
    d = re.findall(c, captcha.text)[0]
    e = re.compile(r"%([A-F0-9]{2})")
    data = {
            'entidad': '',
            'objetoContrato': '',
            'publicacionDesde': '',
            'publicacionHasta': '',
            'presentacionPropuestasDesde': '',
            'presentacionPropuestasHasta': '',
            'cuce1': '',
            'cuce2': '',
            'cuce3': '',
            'cuce4': '',
            'cuce5': '',
            'cuce6': '',
            'r1': '11',
            'bienes': 'B',
            'obras': 'O',
            'servicios': 'S',
            'consultoria': 'C',
            'B903A6B7': '71FD0BFAC3F2E7277707F9191D46CF71',
            'operacion': operacion,
            'nroRegistros': '50',
            'draw': str(pag),
            'start': '0',
            'length': '50',
            'captcha': '',
            d[0]: d[1]
            }
    res = requests.post('https://www.sicoes.gob.bo' + ruta, headers=headers, cookies=cookies, data=data).json()
    r1 = []
    for a in res.get('data'):
        c=[]
        for b in columnas:
            c.append( bytes.fromhex( ''.join(re.findall(e, a[b] ) ) ).decode('ISO_8859-1') )
        r1.append(c)
    return r1

# r = getRutaColumnasContrataciones('convNacional', 'Simple')
#getDatos(columnas=r[1],ruta=r[0],operacion='convNacional',tipo='Simple')
