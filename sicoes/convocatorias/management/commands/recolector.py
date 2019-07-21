#!/usr/bin/env python3
from django.core.management.base import BaseCommand, CommandError
from convocatorias.models import Convocatoria

import requests
import threading
import re
import math
import time
from datetime import datetime as dt, timezone


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
        j = math.floor(i / 2)
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
    ret = sesion.post('https://www.sicoes.gob.bo/portal/contrataciones/operacion2.php', data=data)
    return (ret, captcha)


def getRutaColumnasContrataciones(operacion, tipo, sesion):
    ruta = "/portal/contrataciones/operacion.php"
    rpto = botcolobt(operacion, tipo, int(dt.now().replace(tzinfo=timezone.utc).timestamp()), sesion=sesion)
    print(rpto[0].text)
    columnastmp = rpto[0].json()['sectorsec']
    columnas = proord(columnastmp, rpto[0].json()['a'], rpto[0].json()['b'], rpto[0].json()['fx'], rpto[0].json()['fy'])
    return [ruta, columnas, rpto[1]]


def getRutaColumnasADJ(operacion, tipo, sesion):
    return getRutaColumnasContrataciones(operacion, tipo, sesion)


def getDatos(operacion, tipo, columnas, ruta, pag, captcha, sesion, b9):
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

def guardaConvocatorias(datos):
    nombreColumnas = ('CUCE', 'Entidad', 'Modalidad', 'Objeto de Contratación', 'Estado', 'Monto Contrato (Bs)', 'Fecha Presentación', 'Fecha Publicación', 'Archivos', 'Formularios', 'Persona contacto', 'Garantía', 'CostoPliego', 'ARPC', 'Reunión aclaración', 'Fecha Adjudicación / Desierta', 'Departamento', 'Normativa')
    for dato in datos['datos']:
        m = []
        c = 0
        for col in dato:
            if len(m) <= c:
                m.append(0)
            m[c] = max( m[c], len( col ) )
            print( nombreColumnas[c] + ': "'+ col.strip() + '"' )
            print("Len: " + str(len(col)) + ", Col: " + str(c) )
            c = c + 1
        conv = {}
        try:
            conv = Convocatoria.objects.get(pk=dato[0])
        except Convocatoria.DoesNotExist:
            conv = Convocatoria(cuce=dato[0])
        conv.entidad = dato[1]
        conv.modalidad = dato[2]
        conv.objetoContratación = dato[3]
        conv.estado = dato[4]
        conv.montoContrato = dato[5]
        conv.fechaPresentación = dt.strptime(dato[6],'%d/%m/%Y')
        conv.fechaPublicación = dt.strptime(dato[7],'%d/%m/%Y')
        conv.archivos = dato[8]
        conv.formularios = dato[9]
        conv.personaContacto = dato[10]
        conv.garantía = dato[11]
        if len(dato[12].strip()) > 0:
            conv.costoPliego = dato[12]
        conv.arpc = dato[13]
        if len(dato[14].strip()) > 0:
            conv.reuniónAclaración = dt.strptime(dato[14],'%d/%m/%Y %H:%M')
        if len(dato[15].strip()) > 0:
            conv.fechaAdjudicaciónDesierta = dt.strptime(dato[15],'%d/%m/%Y')
        conv.departamento = dato[16]
        conv.normativa = dato[17]
        conv.save()

# r = getRutaColumnasContrataciones('convNacional', 'Simple')
#getDatos(columnas=r[1],ruta=r[0],operacion='convNacional',tipo='Simple')
def convBase(operacion, tipo, pag):
    sesion = requests.Session()
    sesion.headers.update(
        {'Referer': 'https://www.sicoes.gob.bo/portal/contrataciones/busqueda/convocatorias.php?tipo=convNacional',
         'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'})
    index = sesion.get(
        "https://www.sicoes.gob.bo/portal/contrataciones/busqueda/convocatorias.php?tipo=convNacional")
    b52=re.compile(r'name="B903A6B7" value="([0-9A-F]+)"')
    b53 = b52.findall(index.text)
    if len(b53) < 4:
        index = sesion.get("https://www.sicoes.gob.bo/portal/contrataciones/busqueda/convocatorias.php?tipo=convNacional")
    b53 = b52.findall(index.text)[2]
    r = getRutaColumnasContrataciones(operacion=operacion, tipo=tipo, sesion=sesion)
    datos = getDatos(columnas=r[1],ruta=r[0],operacion=operacion, tipo=tipo, sesion=sesion, captcha=r[2], pag=pag, b9=b53)
    guardaConvocatorias(datos)
    return datos

def convNacional():
    tipo = 'Avanzada'
    operacion = 'convNacional'
    pag = 1
    datos = []
    datos=convBase(operacion=operacion, tipo=tipo, pag=pag)
    total = int(datos['recordsTotal'])/10
    pag = pag + 1
    while(pag<=total):
        datos=convBase(operacion=operacion, tipo=tipo, pag=pag)
        #threading.Thread(target=convBase, args={'operacion': operacion, 'tipo': tipo, 'pag': pag}).start()
        pag = pag + 1
        #print(threading.enumerate())
        #if len(threading.enumerate()) > 10:
        #    time.sleep(1)


# 'CUCE', 'Entidad', 'Modalidad', 'Objeto de Contratación', 'Estado', 'Monto Contrato (Bs)', 'Fecha Presentación', 'Fecha Publicación', 'Archivos', 'Formularios', 'Persona contacto', 'Garantía', 'CostoPliego', 'ARPC', 'Reunión aclaración', 'Fecha Adjudicación / Desierta', 'Departamento', 'Normativa'

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

#    def add_arguments(self, parser):
#        parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        convNacional()
