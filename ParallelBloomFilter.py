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
                             for i in range(0, len(indirizzisicuri))))  # il metodo applicahash verrà eseguito in
                # parallelo su più elementi da inizializzare contemporaneamente (come in un parallel for)
        for i in range(0, len(risHash)):  # vado quindi a porre a uno le celle del filtro
            # nelle posizioni trovate in precedenza
            self.filter[risHash[i]] = 1

    def controllaIndirizzi(self, indirizzi):
        ris = []
        ris.extend(Parallel(n_jobs=self.numero_thread)(delayed(self.controllaIndirizzo)(indirizzi[i])
                                                       for i in range(0, len(indirizzi))))
        # parallelizzo applicando contemporaneamente la stessa funzione per il controllo della stringa a più parole
        # in contemporanea
        return ris


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
    # Testo il controllo con una lista d'indirizzi sicuri e non
    tempo_inizio = time.time()
    print(bfp.controllaIndirizzi(indirizziTest))
    tempo_fine = time.time()
    print('Tempo di controllo: ' + str(tempo_fine - tempo_inizio) + ' secondi')
