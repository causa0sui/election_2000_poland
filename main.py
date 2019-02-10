from jinja2 import *

env = Environment(
    loader=PackageLoader('app', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


wojewodztwa = {}


with open('pkw2000.csv', encoding="utf8") as file:
    lines = file.readlines()
    header = lines[0].strip('\n').split(',')
    uprawnieni_idx = header.index('Uprawnieni')
    karty_wydane_idx = header.index('Karty wydane')
    glosy_oddane_idx = header.index('Głosy oddane')
    glosy_niewazne_idx = header.index('Głosy nieważne')
    glosy_wazne_idx = header.index('Głosy ważne')

    wojewodztwo_idx = header.index('Województwo')
    okreg_idx = header.index('Nr okręgu')
    gmina_idx = header.index('Gmina')
    powiat_idx = header.index('Powiat')

    wynik_grabowski_idx = header.index('Dariusz Maciej GRABOWSKI')
    wynik_ikonowicz_idx = header.index('Piotr IKONOWICZ')
    wynik_kalinowski_idx = header.index('Jarosław KALINOWSKI')
    wynik_krzaklewski_idx = header.index('Marian KRZAKLEWSKI')
    wynik_kwasniewski_idx = header.index('Aleksander KWAŚNIEWSKI')
    wynik_lepper_idx = header.index('Andrzej LEPPER')
    wynik_lopuszanski_idx = header.index('Jan ŁOPUSZAŃSKI')
    wynik_olechowski_idx = header.index('Andrzej Marian OLECHOWSKI')
    wynik_pawlowski_idx = header.index('Bogdan PAWŁOWSKI')
    wynik_walesa_idx = header.index('Lech WAŁĘSA')
    wynik_wilecki_idx = header.index('Tadeusz Adam WILECKI')
    wynik_korwin_idx = header.index('Janusz KORWIN-MIKKE')

    for line in lines[1:]:
        line = line.strip('\n')
        dane = line.split(',')
        nazwa_gminy = dane[gmina_idx]

        gmina = {}
        gmina['nazwa'] = nazwa_gminy
        gmina['uprawnieni'] = int(dane[uprawnieni_idx])
        gmina['głosy_ważne'] = int(dane[glosy_wazne_idx])
        gmina['głosy_nieważne'] = int(dane[glosy_niewazne_idx])
        gmina['głosy_oddane'] = int(dane[glosy_oddane_idx])
        gmina['karty_wydane'] = int(dane[karty_wydane_idx])

        wyniki = {}
        wyniki['Dariusz Maciej GRABOWSKI'] = int(dane[wynik_grabowski_idx])
        wyniki['Piotr IKONOWICZ'] = int(dane[wynik_ikonowicz_idx])
        wyniki['Jarosław KALINOWSKI'] = int(dane[wynik_kalinowski_idx])
        wyniki['Marian KRZAKLEWSKI'] = int(dane[wynik_krzaklewski_idx])
        wyniki['Aleksander KWAŚNIEWSKI'] = int(dane[wynik_kwasniewski_idx])
        wyniki['Andrzej LEPPER'] = int(dane[wynik_lepper_idx])
        wyniki['Jan ŁOPUSZAŃSKI'] = int(dane[wynik_lopuszanski_idx])
        wyniki['Andrzej Marian OLECHOWSKI'] = int(dane[wynik_olechowski_idx])
        wyniki['Bogdan PAWŁOWSKI'] = int(dane[wynik_pawlowski_idx])
        wyniki['Lech WAŁĘSA'] = int(dane[wynik_walesa_idx])
        wyniki['Tadeusz Adam WILECKI'] = int(dane[wynik_wilecki_idx])
        wyniki['Janusz KORWIN-MIKKE'] = int(dane[wynik_korwin_idx])

        gmina['wyniki'] = wyniki
        nazwa_wojewodztwa = dane[wojewodztwo_idx]
        if nazwa_wojewodztwa in wojewodztwa:
            wojewodztwo = wojewodztwa[nazwa_wojewodztwa]
        else:
            wojewodztwo = {}
            wojewodztwo['nazwa'] = nazwa_wojewodztwa
            wojewodztwo['okręgi'] = {}
            wojewodztwa[nazwa_wojewodztwa] = wojewodztwo

        okregi = wojewodztwo['okręgi']
        nazwa_okregu = dane[okreg_idx]

        if nazwa_okregu in okregi:
            okreg = okregi[nazwa_okregu]
        else:
            okreg = {}
            okreg['nazwa'] = nazwa_okregu
            okreg['powiaty'] = {}
            okregi[nazwa_okregu] = okreg

        nazwa_powiatu = dane[powiat_idx]

        powiaty = okreg['powiaty']
        if nazwa_powiatu in powiaty:
            powiat = powiaty[nazwa_powiatu]
        else:
            powiat = {}
            powiat['nazwa'] = nazwa_powiatu
            powiat['gminy'] = {}
            powiaty[nazwa_powiatu] = powiat
        gminy = powiat['gminy']
        gminy[nazwa_gminy] = gmina



gmina_template = env.get_template('gminy.html')
kraj_template = env.get_template('kraj.html')



def uzupelnij_dane(jednostka, skladowa):

    jednostka['uprawnieni'] = sum(gmina['uprawnieni'] for gmina in jednostka[skladowa].values())
    jednostka['głosy_ważne'] = sum(gmina['głosy_ważne'] for gmina in jednostka[skladowa].values())
    jednostka['głosy_nieważne'] = sum(gmina['głosy_nieważne'] for gmina in jednostka[skladowa].values())
    jednostka['głosy_oddane'] = sum(gmina['głosy_oddane'] for gmina in jednostka[skladowa].values())
    jednostka['karty_wydane'] = sum(gmina['karty_wydane'] for gmina in jednostka[skladowa].values())

    wyniki = {}

    wyniki['Dariusz Maciej GRABOWSKI'] = sum(
        gmina['wyniki']['Dariusz Maciej GRABOWSKI'] for gmina in jednostka[skladowa].values())
    wyniki['Piotr IKONOWICZ'] = sum(gmina['wyniki']['Piotr IKONOWICZ'] for gmina in jednostka[skladowa].values())
    wyniki['Jarosław KALINOWSKI'] = sum(
        gmina['wyniki']['Jarosław KALINOWSKI'] for gmina in jednostka[skladowa].values())
    wyniki['Marian KRZAKLEWSKI'] = sum(gmina['wyniki']['Marian KRZAKLEWSKI'] for gmina in jednostka[skladowa].values())
    wyniki['Aleksander KWAŚNIEWSKI'] = sum(
        gmina['wyniki']['Aleksander KWAŚNIEWSKI'] for gmina in jednostka[skladowa].values())
    wyniki['Andrzej LEPPER'] = sum(gmina['wyniki']['Andrzej LEPPER'] for gmina in jednostka[skladowa].values())
    wyniki['Jan ŁOPUSZAŃSKI'] = sum(gmina['wyniki']['Jan ŁOPUSZAŃSKI'] for gmina in jednostka[skladowa].values())
    wyniki['Andrzej Marian OLECHOWSKI'] = sum(
        gmina['wyniki']['Andrzej Marian OLECHOWSKI'] for gmina in jednostka[skladowa].values())
    wyniki['Bogdan PAWŁOWSKI'] = sum(gmina['wyniki']['Bogdan PAWŁOWSKI'] for gmina in jednostka[skladowa].values())
    wyniki['Lech WAŁĘSA'] = sum(gmina['wyniki']['Lech WAŁĘSA'] for gmina in jednostka[skladowa].values())
    wyniki['Tadeusz Adam WILECKI'] = sum(
        gmina['wyniki']['Tadeusz Adam WILECKI'] for gmina in jednostka[skladowa].values())
    wyniki['Janusz KORWIN-MIKKE'] = sum(
        gmina['wyniki']['Janusz KORWIN-MIKKE'] for gmina in jednostka[skladowa].values())




    jednostka['wyniki'] = wyniki


for nazwa_woj, wojewodztwo in wojewodztwa.items():
    okregi = wojewodztwo['okręgi']
    for nazwa_okr, okreg in okregi.items():
        powiaty = okreg['powiaty']
        for nazwa_pow, powiat in powiaty.items():
            gminy = powiat['gminy']
            for nazwa_gm, gmina in gminy.items():
                with open("gminy/" + nazwa_gm + ".html", "w", encoding='utf-8') as file:
                    file.write(gmina_template.render(
                        {'typ': 'Gmina',
                         'typ_1': 'gminie',
                         'gmina': gmina,
                         'frekwencja': round(gmina['karty_wydane'] / gmina['uprawnieni'] * 100, 2), 'skladowe': {},
                         'folder': ''
                         }))
            uzupelnij_dane(powiat, 'gminy')
            with open("powiaty/" + nazwa_pow + ".html", "w", encoding='utf-8') as file:
                file.write(gmina_template.render(
                    {'typ': 'Powiat',
                     'typ_1': 'powiecie',
                     'gmina': powiat, 'frekwencja': round(powiat['karty_wydane'] / powiat['uprawnieni'] * 100, 2),
                     'skladowe': gminy,
                     'folder': '../gminy'}))

        uzupelnij_dane(okreg, 'powiaty')
        with open("okregi/" + nazwa_okr + ".html", "w", encoding='utf-8') as file:
            file.write(gmina_template.render(
                {'typ': 'Okręg',
                 'typ_1': 'okręgu',
                 'gmina': okreg, 'frekwencja': round(okreg['karty_wydane'] / okreg['uprawnieni'] * 100, 2),
                 'skladowe': powiaty,
                 'folder': '../powiaty'}))

    uzupelnij_dane(wojewodztwo, 'okręgi')
    with open("wojewodztwa/" + nazwa_woj + ".html", "w", encoding='utf-8') as file:
        file.write(gmina_template.render(
            {'typ': 'Województwo',
             'typ_1': 'województwie',
             'gmina': wojewodztwo,
             'frekwencja': round(wojewodztwo['karty_wydane'] / wojewodztwo['uprawnieni'] * 100, 2),
             'skladowe': okregi,
             'folder': '../okregi'}))

Polska = {}
Polska['nazwa'] = 'Polska'
Polska['wojewodztwa'] = wojewodztwa

uzupelnij_dane(Polska, 'wojewodztwa')

with open("index.html", "w", encoding='utf-8') as file:
    file.write(kraj_template.render(
        {'typ': 'kraj',
         'typ_1': 'kraju',
         'gmina': Polska, 'frekwencja': round(Polska['karty_wydane'] / Polska['uprawnieni'] * 100, 2),
         'skladowe': wojewodztwa, 'folder': 'wojewodztwa'}))
