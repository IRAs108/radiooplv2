from __future__ import print_function

import json
import re
import struct
import urllib
import time
import sys
import urllib.request as urllib2
import requests
#from icyparser import IcyParser

def get_meta_stream(url):
    encoding = 'iso-8859-1'
    request = urllib2.Request(url, headers={'Icy-MetaData': 1})
    response = urllib2.urlopen(request)
    time.sleep(1)
    meta_il = int(response.headers['icy-metaint'])
    rds = ""
    ll = 0
    while rds == "":
        ll = ll + 1
        if ll > 10:
            break
        for _ in range(10):
            response.read(meta_il)
            metadata_length = struct.unpack('B', response.read(1))[0] * 16
            metadata = response.read(metadata_length).rstrip(b'\0')
            m = re.search(br"StreamTitle='([^']*)';", metadata)
            if m:
                title = m.group(1)
                title_dec = title.decode(encoding, errors='replace')
                if title_dec == "STOP_AD_BREAK":
                    time.sleep(5)
                    continue
                if title:
                    break
        else:
            rds = 'no title found'
        try:
            rds = title.decode(encoding, errors='replace')
            rds = rds.replace("; ", " & ")
        except:
            rds = "ERROR"

    return rds, 0

def get_meta_stream_n(url):
    try:
        np = IcyParser()
        np.getIcyInformation(url)
        rds = np.icy_streamtitle
        np.stop()
    except:
        rds = "Error"
    listeners = 0
    return rds, listeners

def get_meta_revma(url):
    try:
        headers = {
        'User-Agent': 'radioo.pl v. 2',        
        'From': 'ireneusz@pocza.fm'  # This is another valid field
        }
        r = requests.get(url, headers=headers)
        dane = r.text
        r.close
        dane_json = json.loads(dane)
        rds = dane_json['artist'] + ' - ' + dane_json['title']
    except:
        rds = "ERR"
    return rds

def get_meta_rmfon(url):
    try:
        headers = {
        'User-Agent': 'radioo.pl v. 2',        
        'From': 'ireneusz@pocza.fm'  # This is another valid field
        }
        r = requests.get(url, headers=headers)
        dane = r.text
        r.close
        # dane = dane.replace(' / ', ' & ')
        dane_json = json.loads(dane)
        rds = dane_json[3]
        rds2 = rds['author'].replace(' / ', ' & ') + " - " + rds['title']
        #print(dane)
    except:
        rds2 = "ERR"
    return rds2

def get_meta_eurozet(url):
    try:
        headers = {
        'User-Agent': 'radioo.pl v. 2',        
        'From': 'ireneusz@pocza.fm'  # This is another valid field
        }
        r = requests.get(url, headers=headers)
        dane = r.text
        r.close
        dane = dane.replace('rdsData({"now":','')
        dane = dane.replace('})','')
        dane = dane.replace('\/', '&')
        dane_json = json.loads(dane)
        #rds = dane_json[3]
        #print(dane_json)
        rds2 = dane_json['artist'] + " - " + dane_json['title']
        #print(dane)
    except:
        rds2 = "ERR-zet"
        print(rds2)
    return rds2





def get_meta_service(url, service_id):
    #print(url, service_id)
    try:
        #fp = urllib.request.urlopen(url)
        #dane = fp.read()
        #dane = dane.decode('utf8')
        #fp.close()
        headers = {
    'User-Agent': 'radioo.pl v. 0.1',
    'From': 'ireneusz@pocza.fm'  # This is another valid field
}
        r = requests.get(url, headers=headers)
        dane = r.text
        r.close
        # print(dane)
        if service_id == -1:
            #dane = dane.replace("\\/", "&")
            # dane = dane.replace("\\u0", "&#x")
            # dane.replace("\\\\", "\\")
            # dane = dane.encode('latin1').decode('utf8')
            #dane = dane.split('"status":-1')[1]
            artist = ""
            title = ""
            json_data = json.loads(re.sub(r'([a-zA-Z_0-9\.]*\()|(\);?$)','',dane), encoding="UTF-8")
            if json_data[1]['status'] == -1:
                idx = 0
            else:
                idx = 1
            if json_data[idx]['status'] == 0:
                for art in json_data[idx]['artists']:
                    artist = artist + " & " + art['name']
            #artist = dane.split('"name":"')[2].split('"')[0]
            #title = dane.split('"name":"')[1].split('",')[0]
                title = json_data[idx]['name'] 
            if title == "":
                return "None", 0
            artist = artist[3:]
            rds = artist + " - " + title
            rds.replace('&Amp; ','(')
            listeners = 0
        elif service_id == -2:
            artist = dane.split('"artist":"')[1].split('","')[0]
            title = dane.split('"title":"')[1].split('","')[0]
            artist = artist.replace('\\/', '&')
            if title.lower == 'meloradio' or title.lower == 'radiozet':
                rds = 'None'
            else:
                rds = artist + " - " + title
            listeners = 0

        elif service_id == -3:
            dane = dane[1:-1]
            dane_json = json.loads(dane, encoding="UTF-8")
            artist = dane_json['artist_name']
            title = dane_json['song_title']
            rds = dane_json['artist_name'] + " - " + dane_json['song_title']
            listeners = 0
        elif service_id == -4:
            dane_json = json.loads(dane, encoding="UTF-8")
            rds = dane_json['artist'] + " - " + dane_json['song']
            listeners = 0
        elif service_id == -5: #muzo
            dane_json = json.loads(dane, encoding="UTF-8")
            print(dane_json)
            rds = dane_json['emisja'][0]['wykonawca'] + " - " + dane_json['emisja'][0]['tytul']
            # print(rds)
            rds = rds.replace(' - Muzo.Fm', 'None')
            listeners = 0
        elif service_id == -7: #radiobielsko
            # print('tujestem')
            dane_json = json.loads(dane)
            rds = dane_json['artist'] + ' - ' + dane_json['title']
            listeners = 0
            # print(dane_json)

        else:
            dane_json = json.loads(dane)
            rds = dane_json[service_id]['metadata']
            listeners = int(dane_json[service_id]['recipients_count'])
    except:
        rds = "Error"
        listeners = 0

    return rds, listeners


def replacer(rds):
    replacing = [("  ", "  "), ("  ", " "), ("&#x142;", "??"), ("&#x15B;", "??"), ("&#x119;", "??"), ("&#xF3;", "??"),
                 ("\\u0142", "??"), ("\\u015b", "??"), ("\\u0119", "??"), ("\\u00f3", "??"), ("\\u0141", "??"),
                 ("\\u0107", "??"), ("\\u0104", "??"), ("\\u0d3", "??"), ("\\u015a", "??"), ("\\u017c", "??"),
                 ("\\u0105", "??"), ("\\u0144", "??"), ("\\u017b", "??"), ("\\u017a", "??"), ("\\u0118", "??"),
                 ("\\u0104", "??"), ("\\u0106", "??"), ("\\u015a", "??"),
                 ("&#x141;", "??"), ("&#x107;", "??"), ('H&#xE4;', '??'), ('&#x104', '??'), ('&#xD3;', '??'),
                 ("&#x15A;", "??"), ("&#x17C;", "??"), ("&#x105;", "??"), ("&#x144;", "??"), ("&#x17B;", "??"),
                 ("&#x17A;", "??"), ("&#x118;", "??"), ("&#x104;", "??"),
                 ("&#x141;", "??"), ("&#x106;", "??"), ("  ", " - "), ("\r", ""), ("\\n", ""), ("&#xD;", ""),
                 ("Off Radio Krak??w - ", ""), ("DOBRA MUZYKA I WSZYSTKO GRA - Meloradio", ""),
                 ("TERAZ: ", ""), ("TERAZ GRAMY ", ""), ("Radio Zachod - ", ""), ("TERAZ NA ANTENIE ", ""),
                 ("RADIO - RADIO", "NIEMA"), ("RADIOZET - ", ""), ("VOX FM - ", ""),
                 ("H?Nni", "H??nni"), ("Mi?D", "Mi??d"), ("h?nni", "H??nni"), ("mi?d", "Mi??d"),
                 ("G?Nther", "G??nther"), ("St?L", "St????"), ("Canci?N", "Canci??n"), ("G?Raleczko", "G??raleczko"),
                 ("P?Lnocy", "P????nocy"), ("Kt?Rych", "Kt??rych"), ("Cl?Udia", "Cl??udia"), ("R?Zowe", "R????owe"),
                 ("Um?W", "Um??W"), ("Kr?L", "Kr??l"), ("Tw?J", "Tw??j"), ("D?Ja", "D??j??"), ("R???e", "R????e"),
                 ("Canci?N", "Cancion"), ("Zr?Bmy", "Zr??bmy"), ("Aserej?", "Aserej??"),
                 ("M?W", "M??w"), ("Studni?Wka", "Studni??wka"), ("M?Wi", "M??wi"), ("Perd?N", "Perd??n"),
                 ("Kr?Tka", "Kr??tka"), ("G?ry", "G??ry"), ("Pszcz?Lka", "Pszcz????ka"),
                 ("Tr?J", "Tr??j"), ("M?J", "M??j"), ("G?Re", "G??r??"), ("R???a", "R????a"), ("R???e", "R????e"),
                 ("P?Jde", "P??jde"),
                 ("&#x2019;", "???"), ("&#xe9;", "??"), ("&#X2019;", "???"), ("&#Xe9;", "??"),
                 ("G?RNIAK", "G??RNIAK"), ("G?rniak", "G??rniak"), ("Mon?E", "Mon??e"), ("Zawr?", "Zawr??"), ("Zr?", "Zr??"),
                 ("Kr?L", "Kr??l"), ("P?Lnocy", "P????nocy"), ("St?L", "St????"), ("Tw?J", "Tw??j"), ("R?Za", "R????a"),
                 ("RADIOZET - RADIO ZET I JUZ", "None"), (" - MELORADIO", "None"), ("VOX FM - ", "None")
                 ]
    rds2 = ""
    for s in replacing:
        rds = rds.replace(s[0], s[1])

    splitting = " - "
    pattern = re.compile("[Ff][Ee][Aa][Tt]?.")

    if len(rds.split(splitting)) != 2:
        return None

    rds2 = rds

    if pattern.search(rds):
        artist_feat_s = str(pattern.search(rds).group(0))
        artist_feat = rds.split(artist_feat_s)[1]
        artist_feat = artist_feat.split(" - ")[0]
        replace = " " + artist_feat_s + artist_feat
        rds = rds.replace(replace, "")
    else:
        artist_feat = "None"

    if artist_feat[0] == " ":
        artist_feat = artist_feat[1:]

    rds_s = rds.split(splitting)
    # print(rds_s)
    if len(rds_s) == 2:
        artist = rds_s[0].upper()
        title = rds_s[1].title()
    else:
        return None

    if artist.count(" & ") > 0:
        artists = artist.split(" & ")

    else:
        if artist.count("; ") > 0:
            artists = artist.split("; ")
        else:
            artists = [artist]
    if title[-1:] == " ":
        title = title[:-1]

    rds = artist + " - " + title

    ret_data = {"artist": artists, "title": title, "feat": artist_feat, "rds": rds, "old": rds2}

    return ret_data
