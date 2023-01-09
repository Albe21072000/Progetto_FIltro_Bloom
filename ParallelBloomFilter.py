from BloomFilter import *
import time


class ParallelBloomFilter(BloomFilter):
    def __init__(self, size, numFunzHash, numero_thread):  # Ridefinisco il costruttore inserendo come parametro
        # anche il numero di thread paralleli massimi desiderati
        super().__init__(size, numFunzHash)
        self.numero_thread = numero_thread  # numero di thread paralleli massimo

    def inizializzaFiltro(self, indirizzisicuri):  # metodo che inizializza il filtro in parallelo
        risHash = []  # inizializzo la lista che conterrà il risultato dei vari hash
        with Parallel(n_jobs=self.numero_thread) as parallel:  # evito che i threads vengano distrutti e ricreati ad
            # ogni iterazione del ciclo for
            for j in range(0, self.numFunzHash):  # applico in parallelo una funzione hash alla volta
                risHash.extend(  # appendo volta volta i risultati dell'applicazione della j-esima funzione hash alla
                    # lista
                    parallel(delayed(applicahash)(indirizzisicuri[i], self.size, j)
                             for i in range(0, len(indirizzisicuri)))) # il metodo applicahash verrà eseguito in
                # parallelo su più elementi da inizializzare contemporaneamente (come in un parallel for)
        for i in range(0, len(risHash)):  # vado quindi a porre a uno le celle del filtro
            # nelle posizioni trovate in precedenza
            self.filter[risHash[i]] = 1


if __name__ == "__main__":  # non necessario, lo uso per tenere in ordine il codice
    bfp = ParallelBloomFilter(800, 7, 16)  # Instanzio un nuovo filtro di Bloom parallelo
    print("Probabilità di incontrare falsi positivi inizializzando il filtro con una lista di " + str(
        len(indirizziSicuri)) + " parole che non si ripetono: " + str(
        bfp.probFalsiPositivi(indirizziSicuri) * 100) + '%')
    tempo_inizio = time.time()
    bfp.inizializzaFiltro(indirizziSicuri)  # inizializzo il filtro con la lista degli indirizzi giudicati sicuri
    tempo_fine = time.time()
    print('Tempo di inizializzazione del filtro parallelo con ' + str(bfp.numero_thread) + ' thread: ' + str(
        tempo_fine - tempo_inizio) + ' secondi')
    print('Risultato dei controlli: ')
    # Testo il controllo con alcuni indirizzi sicuri e non
    print(bfp.controllaIndirizzo("spam.scam@fraud.com"))
    print(bfp.controllaIndirizzo("alberto.biliotti@stud.unifi.it"))  # indirizzo sicuro
    print(bfp.controllaIndirizzo("albe.biliotti@gmail.com"))
    print(bfp.controllaIndirizzo("sam.scam@fraud.com"))
    print(bfp.controllaIndirizzo("albrto.biliotti@stud.unifi.it"))
    print(bfp.controllaIndirizzo("ale.biliott@gmail.com"))
    print(bfp.controllaIndirizzo("thomasj@icloud.com"))  # indirizzo sicuro
    print(bfp.controllaIndirizzo("boh"))
    print(bfp.controllaIndirizzo("prova"))
