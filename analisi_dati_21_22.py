import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statistics


def pie_chart(dictionary, title, color_list, label_list):
    fig, ax = plt.subplots()
    ax.pie(list(dictionary.values()), colors=color_list, autopct="%1.1f%%", counterclock=False,
           labels=label_list, startangle=90)
    ax.set_title(title)


def bar_chart(data_dictionary, x_labels, barWidth, separate, colors, ylim, title):
    fig = plt.subplots(figsize=(9, 6))
    k = 0
    if separate:
        k = 1/10
    br = np.arange(len(x_labels))
    i = 0
    for key in data_dictionary.keys():
        br1 = [y + barWidth*i*(1+k) for y in br]
        plt.bar(br1, data_dictionary[key] , width=barWidth, color=colors[i], label=key)
    plt.ylim(0, ylim)
    plt.xticks([x + barWidth for x in br], x_labels)
    plt.title(title)
    plt.legend()


# Iniziamo con estrarre e pulire i dati
# df_esami_20_21 = dict(pd.read_excel("/home/nick/PycharmProjects/analisi_dati_pls/PLS-Analisi Dati-2022/PLS-Analisi Dati/Coorte 2020-2021/Dettaglio sup esami_Coorte 2020_1° anno_pulito_SOLO ID STUDENTE_2.xlsx"))
# df_esami_21_22 = dict(pd.read_excel("/home/nick/PycharmProjects/analisi_dati_pls/PLS-Analisi Dati-2022/PLS-Analisi Dati/Coorte 2021-2022/Esami sostenuti fine primo anno_Coorte 21-22_SOLO ID STUDENTE_2.xlsx"))
df_iscritti_tolc_21_22 = dict(pd.read_excel("C:\Users\lctal\Desktop\bonino\iscrizioni_23_24"))

# Otteniamo il numero di immatricolazioni

tot_immatricolati = len(df_iscritti_tolc_21_22['ID STUDENTE'])

# Togliamo i dati che non ci servono da entrambi i dizionari

keys_removed_esami = ['MAT_ID', 'CDS_ID', 'STU_ID', 'AA_ORD_ID', 'PDS_ID', 'Unnamed: 7', 'COORTE', 'ANNO_CORSO',
                      'CODICE_CLASSE', 'CODICE_ESAME', 'ANNO_CORSO_LIB', 'LODE_FLG', 'STATO_AD', 'STATO_AD2']
keys_removed_iscritti = ['TIPO_TITOLO_STRANIERO', 'TIPO_TITOLO_SUP_DESC', 'TIPO_TITST_COD', 'TIPO_TITOLO_STRA_DESC',
                         'VOTO_MAX', 'P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'Unnamed: 22']

for key_to_remove in keys_removed_esami:
    df_esami_21_22.pop(key_to_remove)
for key_to_remove in keys_removed_iscritti:
    df_iscritti_tolc_21_22.pop(key_to_remove)

# Ora accorpiamo diversi tipi di maturità

dict_titolo_sup = df_iscritti_tolc_21_22['TIPO_TITOLO_SUP']
len_titolo_sup = len(dict_titolo_sup)

for i in range(len_titolo_sup):
    name = dict_titolo_sup[i].lower()
    if "tecnic" in name or "perito" in name or "professionale" in name:
        dict_titolo_sup[i] = "Maturità tecnica"
    elif name == "maturità scientifica tecnologica" or "scienze applicate" in name:
        dict_titolo_sup[i] = "Maturità scientifica tecnologica"
    elif "scientific" in name:
        dict_titolo_sup[i] = "Maturità scientifica"
    elif "classic" in name:
        dict_titolo_sup[i] = "Maturità classica"
    else:
        dict_titolo_sup[i] = "Altro"

# Ora costruiamo dei dizionari più adatti alla nostra analisi
# new_df avrà per keys i numeri identificativi dell* studente, e come argomenti una serie di altri dizionari
# per maturità, tolc ed esami.
# A ogni studente è associato un tolc, una maturità e degli esami
# A ogni tolc è associata una serie di sezioni del tolc
# A ogni maturità è associato un tipo e un voto
# A ogni esami è associato un nome cui è associato un voto o giudizio e dei crediti
new_df = {}

esami = []

for i in range(0, len(df_esami_21_22['VALORE UNIVOCO'])):
    if df_esami_21_22['DESCRIZIONE_ESAME'][i] not in esami:
        esami.append(df_esami_21_22['DESCRIZIONE_ESAME'][i])

# Nel file d'origine ci sono 6 celle senza identificativo. I dati di queste non vengono considerati

for student in df_esami_21_22['VALORE UNIVOCO']:
    if student not in new_df.keys():
        new_df[student] = {}
    new_df[student]['maturità'] = {}
    new_df[student]['maturità']['TIPO_TITOLO_SUP'] = ''
    new_df[student]['maturità']['VOTO'] = 0
    new_df[student]['tolc'] = {}
    new_df[student]['esami'] = {}
    new_df[student]['tolc']['MATEMATICA_DI_BASE'] = 0
    new_df[student]['tolc']['SCIENZE_DI_BASE'] = 0
    new_df[student]['tolc']['TEST_ACCERTAMENTO'] = 0
    new_df[student]['tolc']['Ragionamento e problemi'] = 0
    for esame in esami:
        new_df[student]['esami'][esame] = {}
        new_df[student]['esami'][esame]['CFU_ESAME'] = 0
        new_df[student]['esami'][esame]['VOTO_ESAME'] = 0
        new_df[student]['esami'][esame]['GIUDIZIO'] = ''

# Riempimento esami da df_esami_21_22

for i in range(0, len(df_esami_21_22['VALORE UNIVOCO'])):
    studente = df_esami_21_22['VALORE UNIVOCO'][i]
    esame = df_esami_21_22['DESCRIZIONE_ESAME'][i]
    cfu = df_esami_21_22['CFU_ESAME'][i]
    voto = df_esami_21_22['VOTO_ESAME'][i]
    giudizio = df_esami_21_22['GIUDIZIO'][i]

    new_df[studente]['esami'][esame]['CFU_ESAME'] = cfu
    new_df[studente]['esami'][esame]['VOTO_ESAME'] = voto
    new_df[studente]['esami'][esame]['GIUDIZIO'] = giudizio

# Riempimento tolc e provenienza da df_iscritti_tolc_21_22

for i in range(0, len(df_iscritti_tolc_21_22['ID STUDENTE'])):
    studente = df_iscritti_tolc_21_22['ID STUDENTE'][i]
    tipo = df_iscritti_tolc_21_22['TIPO_TITOLO_SUP'][i]
    voto = df_iscritti_tolc_21_22['VOTO'][i]
    ragprob = df_iscritti_tolc_21_22['Ragionamento e problemi'][i]
    mate = df_iscritti_tolc_21_22['MATEMATICA_DI_BASE'][i]
    sciebas = df_iscritti_tolc_21_22['SCIENZE_DI_BASE'][i]
    tarm = df_iscritti_tolc_21_22['TEST_ACCERTAMENTO'][i]

    if studente in new_df.keys():
        new_df[studente]['maturità']['TIPO_TITOLO_SUP'] = tipo
        new_df[studente]['maturità']['VOTO'] = voto
        new_df[studente]['tolc']['MATEMATICA_DI_BASE'] = mate
        new_df[studente]['tolc']['Ragionamento e problemi'] = ragprob
        new_df[studente]['tolc']['SCIENZE_DI_BASE'] = sciebas
        new_df[studente]['tolc']['TEST_ACCERTAMENTO'] = tarm

# C'è una asimmetria tra i numeri idntificativi dei due file. Se un numero non appare negli esami è considerato
# abbandono

# Creiamo ora un dizionario per gli abbandoni analogo a new_df, però solo con maturità e tolc

abbandoni = {}
i = 0
for studente in df_iscritti_tolc_21_22['ID STUDENTE']:
    if studente not in new_df.keys():
        abbandoni[studente] = {}
        abbandoni[studente]['maturità'] = {}
        abbandoni[studente]['maturità']['TIPO_TITOLO_SUP'] = df_iscritti_tolc_21_22['TIPO_TITOLO_SUP'][i]
        abbandoni[studente]['maturità']['VOTO'] = df_iscritti_tolc_21_22['VOTO'][i]
        abbandoni[studente]['tolc'] = {}
        abbandoni[studente]['tolc']['MATEMATICA_DI_BASE'] = df_iscritti_tolc_21_22['MATEMATICA_DI_BASE'][i]
        abbandoni[studente]['tolc']['SCIENZE_DI_BASE'] = df_iscritti_tolc_21_22['SCIENZE_DI_BASE'][i]
        abbandoni[studente]['tolc']['TEST_ACCERTAMENTO'] = df_iscritti_tolc_21_22['TEST_ACCERTAMENTO'][i]
        abbandoni[studente]['tolc']['Ragionamento e problemi'] = df_iscritti_tolc_21_22['Ragionamento e problemi'][i]
    i += 1

# Di seguito il totale degli/delle iscritt* al secondo anno

tot_iscritti_2 = tot_immatricolati-len(list(abbandoni.keys()))

tot_per_maturità = {}
tot_per_maturità_0 = {}
tot_abbandoni_per_maturità = {}

etichette = ['Maturità scientifica', 'Maturità scientifica tecnologica', 'Maturità classica', 'Maturità tecnica',
             'Altro']
labels = ['Maturità \n scientifica', 'Maturità \n scientifica \n tecnologica', 'Maturità \n classica',
          'Maturità \n tecnica', 'Altro']
for etichetta in etichette:
    tot_per_maturità[etichetta] = 0
    tot_per_maturità_0[etichetta] = 0
    tot_abbandoni_per_maturità[etichetta] = 0

for studente in new_df.keys():
    tot_per_maturità[new_df[studente]['maturità']['TIPO_TITOLO_SUP']] += 1

for i in range(0, len(df_iscritti_tolc_21_22['TIPO_TITOLO_SUP'])):
    scuola = df_iscritti_tolc_21_22['TIPO_TITOLO_SUP'][i]
    tot_per_maturità_0[scuola] += 1

for key in tot_per_maturità.keys():
    tot_abbandoni_per_maturità[key] = tot_per_maturità_0[key]- tot_per_maturità[key]


colori = ['tab:blue', 'tab:red', 'gold', 'tab:green', 'tab:orange', 'tab:cyan']

corsi = ['GEOMETRIA E ALGEBRA LINEARE I',
         'INTRODUZIONE ALLA PROGRAMMAZIONE',
         'ANALISI I',
         'ESPERIMENTAZIONI I',
         'FISICA 1',
         'ANALISI II']

name_legend = ['GAL 1',
         'PROGRAMMAZIONE',
         'ANALISI I',
         'ESP I',
         'FISICA 1',
         'ANALISI II']


def voto_esame(studente, corso):
    return new_df[studente]['esami'][corso]['VOTO_ESAME']


def giudizio_esame(studente, corso):
    return new_df[studente]['esami'][corso]['GIUDIZIO']


def provenienza(studente):
    return new_df[studente]['maturità']['TIPO_TITOLO_SUP']


def graph11_heights(corso):
    h = {}
    for etichetta in etichette:
        h[etichetta] = 0

    for studente in new_df.keys():
        voto = new_df[studente]['esami'][corso]['VOTO_ESAME']
        giudizio = new_df[studente]['esami'][corso]['GIUDIZIO']
        scuola = new_df[studente]['maturità']['TIPO_TITOLO_SUP']
        if voto >=18 or giudizio=='Approvato':
            h[scuola] += 1/tot_per_maturità_0[scuola]
    return list(h.values())


barWidth = 0.12
fig = plt.subplots(figsize =(9, 6))

for i in range(0, len(corsi)):
    br = np.arange(len(etichette))
    x = [y + i*barWidth for y in br]
    plt.bar(x, graph11_heights(corsi[i]), width=barWidth, color=colori[i], label=name_legend[i])

plt.xticks([r + 2*barWidth for r in range(len(etichette))],labels)
plt.legend()
plt.title("Percentuale di superamento esami\n per indirizzo di provenienza")


etichette = ['ESPERIMENTAZIONI I', 'TECNICHE INFORMATICHE PER LA FISICA',
            'GEOMETRIA E ALGEBRA LINEARE I',
            'ANALISI I',
            'ANALISI II',
            'FISICA 1',
            'INTRODUZIONE ALLA PROGRAMMAZIONE',
            ]
x_labels = ['ESPERIMENTI 1',
            'TIF',
            'GEOMETRIA',
            'ANALISI I',
            'ANALISI II',
            'FISICA 1',
            'PROGRAMMAZIONE',
            ]

dati_19_20 = [0.48, 0.62, 0.42, 0.44, 0.39, 0.17, 0.42] #trascritti da presentazione 19-20
dati_20_21 = [0.42, 0.59, 0.42, 0.40, 0.33, 0.2, 0.46] #trascritti da excel

cfu_esami = [12, 3, 9, ]

dati_21_22 = {}

for corso in etichette:
    dati_21_22[corso] = 0

for studente in new_df.keys():
    for corso in etichette:
        if voto_esame(studente, corso)>=18 or giudizio_esame(studente, corso)=='Approvato':
            dati_21_22[corso] += 1/tot_immatricolati

print('----Superamento Fisica----')
print(dati_21_22)
print('--------------')

barWidth = 0.22
fig = plt.subplots(figsize =(9, 6))
br = np.arange(len(etichette))
br1 = [y + barWidth + barWidth/10 for y in br]
br2 = [y + 2*barWidth + 2*barWidth/10 for y in br]
plt.bar(br, dati_19_20, width=barWidth, color='tab:red', label='19-20')
plt.bar(br1, dati_20_21, width=barWidth, color='gold', label='20-21')
plt.bar(br2, list(dati_21_22.values()), width=barWidth, color='tab:green', label='21-22')
plt.ylim(0,1)
plt.xticks([x + barWidth for x in br],x_labels)

plt.title('Superamento esami - confronto')
plt.legend()

boundaries = [-1,7,15,23,31,39,47,180]
fette = ['<8','8-15','16-23','24-31','32-39','40-47','>48']
cfu_torta = {}
for fetta in fette:
    cfu_torta[fetta] = 0


def conta_cfu(cfu):
    for i in range(0,len(boundaries)-1):
        if boundaries[i]+1 <= cfu <= boundaries[i+1]:
            cfu_torta[fette[i]] += 1


# Ora contiamo i CFU
cfu_tot_studente = {}
for studente in new_df.keys():
    cfu_tot_studente[studente] = 0
    for esame in new_df[studente]['esami'].keys():
        if voto_esame(studente, esame) >= 18 or giudizio_esame(studente, esame) == 'Approvato':
            cfu_tot_studente[studente] += new_df[studente]['esami'][esame]['CFU_ESAME']
    conta_cfu(cfu_tot_studente[studente])

colors = ['tab:blue', 'tab:red', 'gold', 'tab:green', 'tab:orange','tab:cyan','cornflowerblue']

cfu_torta['<8'] += 240-189

pie_chart(cfu_torta,'CFU acquisiti', colors, list(cfu_torta.keys()))

cfu_20_21 = [45.5,6.8,6.1,3.4,4.9,12.5,20.8]
cfu_21_22 = [x/tot_immatricolati*100 for x in cfu_torta.values()]


fig = plt.subplots(figsize =(9, 6))
br = np.arange(len(fette))
br1 = [y + barWidth + barWidth/10 for y in br]
plt.bar(br, cfu_20_21, width=barWidth, color='tab:red', label='20-21')
plt.bar(br1, cfu_21_22, width=barWidth, color='gold', label='21-22')
plt.xticks([x + barWidth for x in br],fette)
plt.title("Confronto CFU acquisiti")
plt.xlabel("CFU acquisiti")
plt.ylabel("% studenti")
plt.legend()
#plt.show()

etichette = ['Maturità scientifica', 'Maturità scientifica tecnologica', 'Maturità classica', 'Maturità tecnica',
             'Altro']

prov_abbandoni = {}
prov_20_21 = [137, 21, 22, 48, 36]
prov_abbandoni_20_21 = {}
abbandoni_prov_20_21 = [36, 7, 8, 26, 21] # Dati presi dalla presentazione
j = 0
for scuola in etichette:
    prov_abbandoni[scuola] = 0
    prov_abbandoni_20_21[scuola] = abbandoni_prov_20_21[j]
    j += 1


for studente in abbandoni.keys():
    scuola = abbandoni[studente]['maturità']['TIPO_TITOLO_SUP']
    # if scuola not in prov_abbandoni.keys():
     #  prov_abbandoni[scuola] = 0
    prov_abbandoni[scuola] += 1


pie_chart(prov_abbandoni, '% abbandoni rispetto a provenienza', colori, labels)
pie_chart(prov_abbandoni_20_21, '% abbandoni rispetto a provenienza', colori, labels)


fig = plt.subplots(figsize =(9, 6))
barWidth = 0.4
br = np.arange(len(labels))
br1 = [y + barWidth + barWidth/10 for y in br]
bar1 = plt.bar(br, prov_20_21, width=barWidth, color='tab:blue', label='Immatricolazioni')
bar2 = plt.bar(br1, list(prov_abbandoni_20_21.values()), width=barWidth, color='tab:red', label='Abbandoni')
plt.xticks([x + barWidth/2 for x in br],labels)
for rect in bar1 + bar2:
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width() / 2.0, height, f'{height:.0f}', ha='center', va='bottom')
i=0
for rect in bar2:
    height = rect.get_height()
    plt.text(rect.get_x(), bar1[i].get_height()+5 , f'{height/bar1[i].get_height()*100:.0f}%', ha='center', va='bottom')
    i+=1
plt.ylim(0,160)
plt.title("Abbandoni in funzione della scuola di provenienza 20-21")
plt.legend()

fig = plt.subplots(figsize =(9, 6))
barWidth = 0.4
br = np.arange(len(labels))
br1 = [y + barWidth + barWidth/10 for y in br]
bar1 = plt.bar(br, list(tot_per_maturità_0.values()), width=barWidth, color='tab:blue', label='Immatricolazioni')
bar2 = plt.bar(br1, list(prov_abbandoni.values()), width=barWidth, color='tab:red', label='Abbandoni')
plt.xticks([x + barWidth/2 for x in br],labels)
for rect in bar1 + bar2:
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width() / 2.0, height, f'{height:.0f}', ha='center', va='bottom')
i = 0
for rect in bar2:
    height = rect.get_height()
    plt.text(rect.get_x(), bar1[i].get_height()+5 , f'{height/bar1[i].get_height()*100:.0f}%', ha='center', va='bottom')
    i += 1
plt.ylim(0,160)
plt.title("Abbandoni in funzione della scuola di provenienza")
plt.legend()

labels = ['Maturità \n scientifica', 'Maturità \n scientifica \n tecnologica', 'Maturità \n classica',
          'Maturità \n tecnica', 'Altro']

fig = plt.subplots(figsize =(9, 6))
barWidth = 0.4
br = np.arange(len(labels))
br1 = [y + barWidth + barWidth/10 for y in br]
plt.bar(br, [x/sum(abbandoni_prov_20_21) for x in abbandoni_prov_20_21], width=barWidth, color='tab:red', label='20-21')
plt.bar(br1, [x/sum(list(prov_abbandoni.values())) for x in list(prov_abbandoni.values())], width=barWidth,
        color='tab:blue', label='21-22')
plt.xticks([x + barWidth/2 for x in br],labels)
plt.title("Abbandoni in funzione della scuola di provenienza")
plt.legend()


imm_anni = [264, 302, 264, tot_immatricolati]
abbandoni_anni = [91, 121, 98, 51]
anni = ['18-19', '19-20', '20-21', '21-22']

fig = plt.subplots(figsize =(9, 6))
barWidth = 0.4
br = np.arange(len(anni))
br1 = [y + barWidth + barWidth/10 for y in br]
bar1 = plt.bar(br, imm_anni, width=barWidth, color='tab:blue', label='Immatricolazioni')
bar2 = plt.bar(br1, abbandoni_anni, width=barWidth, color='tab:red', label='Abbandoni')
plt.xticks([x + barWidth/2 for x in br],anni)
for rect in bar1 + bar2:
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width() / 2.0, height, f'{height:.0f}', ha='center', va='bottom')
plt.legend()
plt.title("Immatricolazioni e abbandoni 2018-2022")

fig = plt.subplots(figsize =(9, 6))
plt.bar(br, [abbandoni_anni[i]/imm_anni[i] for i in range(0, len(anni))], width=barWidth,
        color='gold', label='% abbandoni')
plt.xticks([x for x in br],anni)
plt.legend()
plt.title("Percentuale di abbandoni negli anni")

# print(new_df)
print(abbandoni)
print(dict(df_iscritti_tolc_21_22).keys())


def calcolo_medie_stdev(sezione):
    tot = []
    for value in list(dict(df_iscritti_tolc_21_22)[sezione]):
        if value == value:
            tot.append(value)
    media = round(statistics.mean(tot), 2)
    stdev = round(statistics.stdev(tot), 2)
    return media, stdev


def calcolo_medie_stdev_abbandoni(sezione):
    tot = []
    for key in abbandoni.keys():
        value = abbandoni[key]['tolc'][sezione]
        if value == value:
            tot.append(value)
    media = round(statistics.mean(tot), 2)
    stdev = round(statistics.stdev(tot), 2)
    return media, stdev

# for key in abbandoni['21O10']['tolc'].keys():
    # print(f"{key}: totale = {calcolo_medie_stdev(key)}, abbandoni = {calcolo_medie_stdev_abbandoni(key)}")


etichette = ['0-25%', '25-50%', '50-75%', '75-100%']
massimi = [20, 10, 10, 10]
limiti = [0, 0.25, 0.5, 0.75, 1]


def classe_punteggio(limiti, valore):
    j = 0
    for i in range(0,len(limiti)-1):
        if limiti[i] <= valore <= limiti[i+1]:
            j = i
    return i


def conta_punteggio_tot(sezione, x_labels, massimo):
    punteggi = []
    for i in range(0, len(x_labels)):
        punteggi.append(0)
    for value in list(dict(df_iscritti_tolc_21_22)[sezione]):
        if str(value) != 'nan':
            if 0 <= value/massimo <= 0.25:
                punteggi[0] += 1
            elif 0.25 <= value/massimo <= 0.5:
                punteggi[1] += 1
            elif 0.5 <= value/massimo <= 0.75:
                punteggi[2] += 1
            else:
                punteggi[3] += 1
    return punteggi


def conta_punteggio_abbandoni(sezione, x_labels, massimo):
    punteggi = []
    for i in range(0, len(x_labels)):
        punteggi.append(0)

    for key in abbandoni.keys():
        value = abbandoni[key]['tolc'][sezione]
        if 0 <= value / massimo <= 0.25:
            punteggi[0] += 1
        elif 0.25 <= value / massimo <= 0.5:
            punteggi[1] += 1
        elif 0.5 <= value / massimo <= 0.75:
            punteggi[2] += 1
        else:
            punteggi[3] += 1
    return punteggi


rb_tot = conta_punteggio_tot('Ragionamento e problemi', etichette, 10)
mb_tot = conta_punteggio_tot('MATEMATICA_DI_BASE', etichette, 20)
sb_tot = conta_punteggio_tot('SCIENZE_DI_BASE', etichette, 10)

rb_abb = conta_punteggio_abbandoni('Ragionamento e problemi', etichette, 10)
mb_abb = conta_punteggio_abbandoni('MATEMATICA_DI_BASE', etichette, 20)
sb_abb = conta_punteggio_abbandoni('SCIENZE_DI_BASE', etichette, 10)

fig = plt.subplots(figsize =(9, 6))
barWidth = 0.2
br = np.arange(len(anni))
br1 = [y + barWidth for y in br]
br2 = [y + 2*barWidth for y in br]
plt.bar(br, rb_tot, width=barWidth, color='tab:blue', label='Ragionamento e problemi')
plt.bar(br, rb_abb, width=barWidth, color='red')
plt.bar(br1, mb_tot, width=barWidth, color='tab:green', label='Matematica di base')
plt.bar(br1, mb_abb, width=barWidth, color='red')
plt.bar(br2, sb_tot, width=barWidth, color='gold', label='Scienze di base')
plt.bar(br2, sb_abb, width=barWidth, color='red', label='Abbandoni')
plt.xticks([x + barWidth for x in br],etichette)
plt.legend()
plt.xlabel('% di punteggio')
plt.ylabel('# studenti')
plt.title("Abbandoni e TOLC")

y1 = []
y2 = []
y3 = []

for i in range(0,len(rb_tot)):
    y1.append(rb_abb[i] / rb_tot[i])
    y2.append(mb_abb[i] / mb_tot[i])
    y3.append(sb_abb[i] / sb_tot[i])
x = [0.25, 0.50, 0.75, 1]

fig = plt.subplots(figsize =(9, 6))
plt.plot(x, y1, color='tab:blue', label='Ragionamento e problemi', marker='o')
plt.plot(x, y2, color='tab:green', label='Matematica di base', marker='o')
plt.plot(x, y3, color='gold', label='Scienze di base', marker='o')
plt.xlabel('% di punteggio')
plt.ylabel('# abbandoni / # studenti')
plt.title("Abbandoni e TOLC")
plt.legend()

print(new_df)

esami_con_voto = ['ESPERIMENTAZIONI I',
            'GEOMETRIA E ALGEBRA LINEARE I',
            'ANALISI I',
            'ANALISI II',
            'FISICA 1',
            'INTRODUZIONE ALLA PROGRAMMAZIONE',
            ]

x_labels = ['ESP I',
            'GAL I',
            'ANALISI I',
            'ANALISI II',
            'FISICA 1',
            'PROGRAMMAZIONE',
            ]

voti_21_22 = {}
voti_20_21 = {}
for esame in esami_con_voto:
    voti_21_22[esame] = []
    voti_20_21[esame] = []

for studente in new_df.keys():
    for esame in esami_con_voto:
        voto = voto_esame(studente, esame)
        if voto >= 18:
            voti_21_22[esame].append(voto)

for i in range(0,len(df_esami_20_21['DESCRIZIONE_ESAME'])):
    esame = df_esami_20_21['DESCRIZIONE_ESAME'][i]
    voto = df_esami_20_21['VOTO_ESAME'][i]
    if esame in voti_20_21.keys():
        voti_20_21[esame].append(voto)

medie_esami_21_22 = []
stdev_esami_21_22 = []
medie_esami_20_21 = []
stdev_esami_20_21 = []

for esame in esami_con_voto:
    medie_esami_21_22.append(round(statistics.mean(voti_21_22[esame]), 2))
    stdev_esami_21_22.append(round(statistics.stdev(voti_21_22[esame]), 2))
    medie_esami_20_21.append(round(statistics.mean(voti_20_21[esame]), 2))
    stdev_esami_20_21.append(round(statistics.stdev(voti_20_21[esame]), 2))

for i in range(0,len(medie_esami_20_21)):
    print(esami_con_voto[i])
    print(f"20-21: {medie_esami_20_21[i]}+-{stdev_esami_20_21[i]}")
    print(f"21-22: {medie_esami_21_22[i]}+-{stdev_esami_21_22[i]}")

for esame in esami_con_voto:
    print(esame)
    print(f"20-21:{len(voti_20_21[esame])}")
    print(f"21-22:{len(voti_21_22[esame])}")

fig = plt.subplots(figsize =(9, 6))
barWidth = 0.3
br = np.arange(len(esami_con_voto))
br1 = [y + barWidth + barWidth/10 for y in br]
plt.bar(br, medie_esami_20_21, yerr=stdev_esami_20_21, width=barWidth, color='tab:blue', label='20/21')
plt.bar(br1, medie_esami_21_22, yerr=stdev_esami_21_22, width=barWidth, color='gold', label='21/22')
plt.xticks([x + barWidth/2 for x in br], x_labels)
plt.xlabel("Esami")
plt.ylabel("Voto medio")
plt.title("Voti medi")
plt.ylim([0,30])
plt.legend()
#print(voti_21_22)
plt.show()

