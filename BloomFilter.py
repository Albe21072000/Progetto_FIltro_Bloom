import hashlib
import mmh3
from joblib import *
import math


def basicHash(stringa, n) -> int:  # funzione hash di base che somma i valori ASCII dei caratteri della stringa e
    # ne calcola il modulo n
    tot = 0
    for i in stringa:
        tot = tot + ord(i)
    return tot % n


def repeatedHash(stringa, n) -> int:  # funzione che ripete l'hash visto prima un numero di volte pari alla lunghezza
    # della stringa alla quarta con un modulo sempre diverso
    ris = 0
    for i in range(0, len(stringa) ** 4):
        ris += basicHash(stringa, i + 1)
        ris %= n
    return ris


def swapCaseHash(stringa, n) -> int:  # funzione che applica la prima funzione hash alla stringa contenente le
    # maiuscole e le minuscole invertite rispetto alla stringa in ingresso
    return basicHash(stringa.swapcase(), n)


def doubleHash(stringa, n) -> int:  # funzione che applica sempre il basic hash alla stringa criptata con la funzione
    # di crittografia hash fornita da joblib
    return basicHash(hash(stringa), n)


def sha256Hash(stringa, n) -> int:  # funzione che applica il basic hash alla stringa criptata con la funzione sha256
    # della libreria hashlib
    return basicHash(hashlib.sha256(stringa.encode('utf-8')).hexdigest(), n)


def repeatedsha256Hash(stringa,
                       n) -> int:  # funzione che ripete l'hash visto prima un numero di volte pari alla lunghezza
    # della stringa alla quarta variando il modulo
    ris = 0
    for i in range(0, len(stringa) ** 4):  # All elements of the matrix are added together
        ris += sha256Hash(stringa, i + 1)
        ris %= n
    return ris  # The module n operation is applied to return an index for the bit array


def mmh3hash(stringa, i, n) -> int:  # funzione che ritorna il valore fornito dalla funzione di hash della libreria
    # mmh3, con il parametro i che rappresenta il seed desiderato,
    # a cui devo andare ad applicare il modulo n per evitare che tale valore possa essere maggiore di n
    return mmh3.hash(stringa, i) % n


def applicahash(stringa, n,
                i) -> int:  # funzione che, in base all'indice i passato in ingresso, applica una funzione di
    # hash diversa e ne restituisce il risultato (in caso d'indici maggiori di 5 ritornerà
    # il valore della function mmh3hash ma con seed pari all'indice i stesso)
    match i:
        case 0:
            return basicHash(stringa, n)
        case 1:
            return repeatedHash(stringa, n)
        case 2:
            return doubleHash(stringa, n)
        case 3:
            return swapCaseHash(stringa, n)
        case 4:
            return sha256Hash(stringa, n)
        case 5:
            return repeatedsha256Hash(stringa, n)
    return mmh3hash(stringa, n, i)


class BloomFilter:  # superclasse che definisce il costruttore e il metodo per ottenere la probabilità di falsi
    # positivi del filtro
    def __init__(self, size, numFunzHash):  # Costruttore della superclasse
        self.size = size  # lunghezza del filtro
        self.filter = [0] * size  # inizializzo il filtro con tutti i valori a zero
        self.numFunzHash = numFunzHash  # numero di funzioni hash desiderate

    def probFalsiPositivi(self, listaIndirizzisicuri) -> float:  # restituisce la probabilità che il controllo
        # classifichi erroneamente un indirizzo come sicuro
        return (1 - math.e ** (-1 * self.numFunzHash * len(listaIndirizzisicuri) / self.size)) ** self.numFunzHash

    # metodo astratto che, una volta definito, conterrà il codice che permetterà d'inizializzare il filtro
    def inizializzaFiltro(self, indirizzisicuri):
        pass

    def controllaIndirizzo(self, indirizzo) -> bool:  # metodo per verificare se un indirizzo è considerato sicuro
        for i in range(0, self.numFunzHash):
            if self.filter[applicahash(indirizzo, self.size, i)] == 0:
                return False
        return True

    # metodo astratto che, una volta definito, conterrà il codice che permetterà di controllare una lista di stringhe
    def controllaIndirizzi(self, indirizzi):
        pass


# lista d'indirizzi sicuri (per la maggior parte generata casualmente)
indirizziSicuri = [
    'mgreen @ gmail.com', 'alberto.biliotti@stud.unifi.it',
    'hoangle @ yahoo.ca', 'drezet @ live.com', 'ahmad @ optonline.net',
    'rande @ msn.com', 'jgwang @ hotmail.com', 'tangsh @ outlook.com', 'skoch @ comcast.net', 'lbecchi @ msn.com',
    'ideguy @ aol.com', 'seano @ hotmail.com', 'oster @ verizon.net', 'graham @ hotmail.com', 'adillon @ mac.com',
    'thomasj@icloud.com', 'dkasak @ yahoo.ca', 'sisyphus @ yahoo.com', 'staikos @ live.com', 'geekoid @ comcast.net',
    'ijackson @ outlook.com', 'sbmrjbr @ optonline.net', 'duchamp @ aol.com', 'tubajon @ yahoo.com', 'flakeg @ me.com',
    'maneesh @ outlook.com', 'marin @ gmail.com', 'oneiros @ aol.com', 'chaikin @ msn.com', 'frikazoyd @ sbcglobal.net',
    'markjugg @ me.com', 'ewaters @ live.com', 'formis @ yahoo.ca', 'hauma @ msn.com', 'bflong @ live.com',
    'moonlapse @ msn.com', 'eurohack @ gmail.com', 'kalpol @ gmail.com', 'kmself @ mac.com', 'clkao @ verizon.net',
    'empathy @ hotmail.com', 'sherzodr @ yahoo.ca', 'temmink @ msn.com', 'knorr @ outlook.com', 'adamk @ optonline.net',
    'drewf @ sbcglobal.net', 'yxing @ hotmail.com', 'telbij @ mac.com', 'malvar @ optonline.net',
    'lridener @ sbcglobal.net', 'keutzer @ msn.com', 'kempsonc @ me.com', 'hedwig @ gmail.com', 'barjam @ att.net',
    'ovprit @ mac.com', 'salesgeek @ aol.com', 'majordick @ verizon.net', 'dgriffith @ yahoo.com',
    'josem @ outlook.com',
    'nweaver @ mac.com', 'mxiao @ me.com', 'gomor @ me.com', 'pthomsen @ optonline.net', 'purvis @ comcast.net',
    'keijser @ aol.com', 'phish @ comcast.net', 'hmbrand @ aol.com', 'okroeger @ icloud.com',
    'csilvers @ sbcglobal.net',
    'sagal @ live.com', 'kevinm @ att.net', 'janusfury @ yahoo.com', 'ahmad @ comcast.net', 'cgarcia @ yahoo.com',
    'raines @ mac.com', 'oster @ outlook.com', 'bjornk @ yahoo.ca', 'avalon @ optonline.net', 'fairbank @ aol.com',
    'fluffy @ outlook.com', 'msroth @ optonline.net', 'jimxugle @ att.net', 'wilsonpm @ outlook.com',
    'cderoove @ verizon.net', 'cvrcek @ gmail.com', 'phyruxus @ gmail.com', 'garland @ live.com',
    'barnett @ hotmail.com',
    'shazow @ att.net', 'miami @ outlook.com', 'yruan @ verizon.net', 'pemungkah @ msn.com', 'kdawson @ live.com',
    'moxfulder @ optonline.net', 'engelen @ aol.com', 'agolomsh @ msn.com', 'kalpol @ msn.com', 'sinkou @ att.net',
    'scitext @ sbcglobal.net', 'tangsh @ verizon.net'
]
indirizziTest = ['mgrssn @ gmail.com', 'albsrto.biliotti@stud.unifi.it',
    'hoangls @ yahoo.ca', 'drszst @ livs.com', 'ahmad @ optonlins.nst',
    'rands @ msn.com', 'jgwang @ hotmail.com', 'tangsh @ outlook.com', 'skoch @ comcast.nst', 'lbscchi @ msn.com',
    'idsguy @ aol.com', 'ssano @ hotmail.com', 'ostsr @ vsrizon.nst', 'graham @ hotmail.com', 'adillon @ mac.com',
    'thomasj@icloud.com', 'dkasak @ yahoo.ca', 'sisyphus @ yahoo.com', 'staikos @ livs.com', 'gsskoid @ comcast.nst',
    'ijackson @ outlook.com', 'sbmrjbr @ optonlins.nst', 'duchamp @ aol.com', 'tubajon @ yahoo.com', 'flaksg @ ms.com',
    'mansssh @ outlook.com', 'marin @ gmail.com', 'onsiros @ aol.com', 'chaikin @ msn.com', 'frikazoyd @ sbcglobal.nst',
    'markjugg @ ms.com', 'swatsrs @ livs.com', 'formis @ yahoo.ca', 'hauma @ msn.com', 'bflong @ livs.com',
    'moonlapss @ msn.com', 'surohack @ gmail.com', 'kalpol @ gmail.com', 'kmsslf @ mac.com', 'clkao @ vsrizon.nst',
    'smpathy @ hotmail.com', 'shsrzodr @ yahoo.ca', 'tsmmink @ msn.com', 'knorr @ outlook.com', 'adamk @ optonlins.nst',
    'drswf @ sbcglobal.nst', 'yxing @ hotmail.com', 'tslbij @ mac.com', 'malvar @ optonlins.nst',
    'lridsnsr @ sbcglobal.nst', 'ksutzsr @ msn.com', 'ksmpsonc @ ms.com', 'hsdwig @ gmail.com', 'barjam @ att.nst',
    'ovprit @ mac.com', 'salssgssk @ aol.com', 'majordick @ vsrizon.nst', 'dgriffith @ yahoo.com',
    'jossm @ outlook.com',
    'nwsavsr @ mac.com', 'mxiao @ ms.com', 'gomor @ ms.com', 'pthomssn @ optonlins.nst', 'purvis @ comcast.nst',
    'ksijssr @ aol.com', 'phish @ comcast.nst', 'hmbrand @ aol.com', 'okrosgsr @ icloud.com',
    'csilvsrs @ sbcglobal.nst',
    'sagal @ livs.com', 'ksvinm @ att.nst', 'janusfury @ yahoo.com', 'ahmad @ comcast.nst', 'cgarcia @ yahoo.com',
    'rainss @ mac.com', 'ostsr @ outlook.com', 'bjornk @ yahoo.ca', 'avalon @ optonlins.nst', 'fairbank @ aol.com',
    'fluffy @ outlook.com', 'msroth @ optonlins.nst', 'jimxugls @ att.nst', 'wilsonpm @ outlook.com',
    'cdsroovs @ vsrizon.nst', 'cvrcsk @ gmail.com', 'phyruxus @ gmail.com', 'garland @ livs.com',
    'barnstt @ hotmail.com',
    'shazow @ att.nst', 'miami @ outlook.com', 'yruan @ vsrizon.nst', 'psmungkah @ msn.com', 'kdawson @ livs.com',
    'moxfuldsr @ optonlins.nst', 'sngslsn @ aol.com', 'agolomsh @ msn.com', 'kalpol @ msn.com', 'sinkou @ att.nst',
    'scitsxt @ sbcglobal.nst', 'tangsh @ vsrizon.nst']
