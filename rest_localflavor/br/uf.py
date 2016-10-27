# -*- coding: utf-8 -*-
"""
Source code based in:
https://github.com/douglasmiranda/django-localflavor-br

An alphabetical list of Brazilian states for use as `choices` in a formfield.
This exists in this standalone file so that it's only imported into memory
when explicitly needed.
"""
from __future__ import unicode_literals

AC = 'ac'
AL = 'al'
AP = 'ap'
AM = 'am'
BA = 'ba'
CE = 'ce'
DF = 'df'
ES = 'es'
GO = 'go'
MA = 'ma'
MT = 'mt'
MS = 'ms'
MG = 'mg'
PA = 'pa'
PB = 'pb'
PR = 'pr'
PE = 'pe'
PI = 'pi'
RJ = 'rj'
RN = 'rn'
RS = 'rs'
RO = 'ro'
RR = 'rr'
SC = 'sc'
SP = 'sp'
SE = 'se'
TO = 'to'

STATE_CHOICES = (
    (AC, 'Acre'),
    (AL, 'Alagoas'),
    (AP, 'Amapá'),
    (AM, 'Amazonas'),
    (BA, 'Bahia'),
    (CE, 'Ceará'),
    (DF, 'Distrito Federal'),
    (ES, 'Espírito Santo'),
    (GO, 'Goiás'),
    (MA, 'Maranhão'),
    (MT, 'Mato Grosso'),
    (MS, 'Mato Grosso do Sul'),
    (MG, 'Minas Gerais'),
    (PA, 'Pará'),
    (PB, 'Paraíba'),
    (PR, 'Paraná'),
    (PE, 'Pernambuco'),
    (PI, 'Piauí'),
    (RJ, 'Rio de Janeiro'),
    (RN, 'Rio Grande do Norte'),
    (RS, 'Rio Grande do Sul'),
    (RO, 'Rondônia'),
    (RR, 'Roraima'),
    (SC, 'Santa Catarina'),
    (SP, 'São Paulo'),
    (SE, 'Sergipe'),
    (TO, 'Tocantins'),
)
