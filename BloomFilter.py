import hashlib
import mmh3
from joblib import *
import math


def basicHash(string, n) -> int:  # funzione hash di base che somma i valori ASCII dei caratteri della stringa e
    # ne calcola il modulo n
    tot = 0
    for i in string:
        tot = tot + ord(i)
    return tot % n


def repeatedHash(string, n) -> int:  # funzione che ripete l'hash visto prima un numero di volte pari alla lunghezza
    # della stringa alla quarta con un modulo sempre diverso
    ris = 0
    for i in range(0, len(string) ** 4):
        ris += basicHash(string, i + 1)
        ris %= n
    return ris


def swapCaseHash(string, n) -> int:  # funzione che applica la prima funzione hash alla stringa contenente le
    # maiuscole e le minuscole invertite rispetto alla stringa in ingresso
    return basicHash(string.swapcase(), n)


def doubleHash(string, n) -> int:  # funzione che applica sempre il basic hash alla stringa criptata con la funzione
    # di crittografia hash fornita da joblib
    return basicHash(hash(string), n) % n


def sha256Hash(string, n) -> int:  # funzione che applica il basic hash alla stringa criptata con la funzione sha256
    # della libreria hashlib
    return basicHash(hashlib.sha256(string.encode('utf-8')).hexdigest(), n)


def repeatedsha256Hash(string,
                       n) -> int:  # funzione che ripete l'hash visto prima un numero di volte pari alla lunghezza
    # della stringa alla quarta variando il modulo
    ris = 0
    for i in range(0, len(string) ** 4):  # All elements of the matrix are added together
        ris += sha256Hash(string, i + 1)
        ris %= n
    return ris  # The module n operation is applied to return an index for the bit array


def mmh3hash(string, i, n) -> int:  # funzione che ritorna il valore fornito dalla funzione di hash della libreria
    # mmh3, con il parametro i che rappresenta il seed desiderato,
    # a cui devo andare ad applicare il modulo n per evitare che tale valore possa essere maggiore di n
    return mmh3.hash(string, i) % n


def applicahash(string, n, i) -> int:  # funzione che, in base all'indice i passato in ingresso, applica una funzione di
    # hash diversa e ne restituisce il risultato (in caso d'indici maggiori di 5 ritornerà
    # il valore della function mmh3hash ma con seed pari all'indice i stesso)
    match i:
        case 0:
            return basicHash(string, n)
        case 1:
            return repeatedHash(string, n)
        case 2:
            return doubleHash(string, n)
        case 3:
            return swapCaseHash(string, n)
        case 4:
            return sha256Hash(string, n)
        case 5:
            return repeatedsha256Hash(string, n)

    return mmh3hash(string, n, i)


class BloomFilter:  # superclasse che definisce il costruttore e il metodo per ottenere la probabilità di falsi
    # positivi del filtro
    def __init__(self, size, numFunzHash):  # Costruttore della superclasse
        self.size = size  # lunghezza del filtro
        self.filter = [0] * size  # inizializzo il filtro con tutti i valori a zero
        self.numFunzHash = numFunzHash  # numero di funzioni hash desiderate

    def probFalsiPositivi(self, array) -> float:  # restituisce la probabilità che il controllo classifichi
        # erroneamente un indirizzo come sicuro
        return (1 - math.e ** (-1 * self.numFunzHash * len(array) / self.size)) ** self.numFunzHash

    # metodi astratti che, una volta definiti, conterranno il codice che permetterà d'inizializzare il filtro
    # e di controllare se un indirizzo è sicuro o meno
    def inizializzaFiltro(self, array):
        pass

    def controllaIndirizzo(self, address) -> bool:
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
