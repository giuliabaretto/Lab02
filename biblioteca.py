import csv

def carica_da_file(file_path):
    """Carica i libri dal file"""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            # prendo il file, lo leggo, tolgo \n a fine di ogni riga, e divido il file in righe
            righe = file.read().strip().splitlines()
            numero_sezioni = int(righe[0])  # considero la prima riga che mi indica il numero di sezioni (così nel caso modificassi in file csv il numero di sezioni non devo cambiare il codice)

    except FileNotFoundError:
        print("File non trovato")
        return None

    if not righe:
        return None      # nel caso non trovassi righe nel file

    """ creare e popolare una struttura dati che rappresenta la biblioteca distribuendo i libri presenti nel file nelle sezioni corrette """
    biblioteca = []

    """ vedo la biblioteca come lista di liste """
    biblioteca = [[] for i in range(numero_sezioni)] # lista di 5 (numero delle mie sezioni) liste

    for riga in righe[1:]: # metto 1: sennò parto da riga 0 e mi legge solo "5"
        # print(riga)  (avevo fatto un controllo)
        titolo, autore, anno, pagine, sezione = riga.strip().split(",")
        anno = int(anno)
        pagine = int(pagine)
        sezione = int(sezione)
        """ creo il libro come un dizionario """
        libro = {"titolo": titolo, "autore": autore, "anno": anno, "pagine": pagine, "sezione": sezione}  # potrei eliminare il campo sezione perchè lo considero dopo (è ridondante)

        """ devo aggiungere il libro alla sezione giusta """
        # essendo che le liste partono da 0 (e per me 'sezione' è una lista) ->
        indice_sezione = int(sezione)-1
        if indice_sezione < numero_sezioni:
            biblioteca[indice_sezione].append(libro)
    # print(biblioteca) (avevo fatto un controllo, stampo una lista di liste (le sezioni), che a loro volta contengono dizionari (i libri))
    return biblioteca



def aggiungi_libro(biblioteca, titolo, autore, anno, pagine, sezione, file_path):
    """Aggiunge un libro nella biblioteca"""

    """ In caso errori, quali 
    -titolo già presente, 
    -sezione non esistente 
    -file non trovato, 
    la funzione deve restituire None"""

    try:
        # controllo gli errori
        # titolo già presente
        for sez in biblioteca:
            for libro in sez:
                if libro["titolo"].lower() == titolo.lower():  # metto .lower così ignoro le maiuscole/minuscole
                    print("Il libro è già presente nella biblioteca")
                    return None

        # sezione non esistente
        indice_sezione = sezione - 1
        if indice_sezione < 0 or indice_sezione >= len(biblioteca):
            print("La sezione non esiste")
            return None

        nuovo_libro = {"titolo": titolo, "autore": autore, "anno": anno, "pagine": pagine, "sezione": sezione}

        """La funzione deve aggiornare la struttura dati (aggiungo il libro alla strutt. dati) ..."""
        biblioteca[indice_sezione].append(nuovo_libro)

        """... ed il file, inserendo una nuova riga in fondo a quest'ultimo"""
        with open(file_path, "a", newline="", encoding="utf-8") as file: # metto a (per append, e non write) e newline, altrimenti sovrascrive e cancella ciò che avevo
            file_aggiornato = csv.writer(file)
            # scrivo una nuova riga con i dati separati da virgola
            file_aggiornato.writerow([titolo, autore, anno, pagine, sezione])
        print(f"Libro {titolo} aggiunto con successo alla sezione {sezione}")
        return nuovo_libro

    except FileNotFoundError:
        print("File non trovato")
        return None



def cerca_libro(biblioteca, titolo):
    """Cerca un libro nella biblioteca dato il titolo"""

    """Nel caso in cui il libro non esista, 
    -la funzione restituisce None; altrimenti, 
    -restituisce una stringa contenente il titolo, l'autore, l'anno di pubblicazione, il numero di pagine e la sezione in cui si trova il libro"""
    for libro_sez in biblioteca: # cerco in tutte le sezioni
        for libro in libro_sez: # cerco tra tutti i libri della sez corrente
            if libro["titolo"].lower() == titolo.lower(): # confronto i titoli, metto .lower così ignoro le maiuscole/minuscole come prima
                """ devo restituire la stringa formattata come (I Promessi Sposi, Alessandro Manzoni, 1827, 720, 1)"""
                return f"{libro['titolo']}, {libro['autore']}, {libro['anno']}, {libro['pagine']}, {libro['sezione']}"

    return None # se non lo trova



def elenco_libri_sezione_per_titolo(biblioteca, sezione):
    """Ordina i titoli di una data sezione della biblioteca in ordine alfabetico"""
    # Nel caso in cui la sezione non esista, la funzione restituisce None.
    indice_sezione = sezione-1
    if indice_sezione < 0 or indice_sezione >= len(biblioteca):
        print(f"La sezione non esiste. Sezioni disponibili: da 1 a {len(biblioteca)}")

    libri_sezione_richiesta = biblioteca[indice_sezione]
    # se la sezione richiesta è vuota -> l'elenco restituito sarà una lista vuota
    if not libri_sezione_richiesta:  # esegue il return se questa condizione risulta falsa
        return []

    #estraggo i titoli dalla sezione richiesta e li ordino
    titoli = [libro["titolo"] for libro in libri_sezione_richiesta]
    titoli.sort()

    return titoli  # restituisce la lista dei titoli della sezione richiesta in ordine alfabetico




def main():
    biblioteca = []
    file_path = "biblioteca.csv"

    while True:
        print("\n--- MENU BIBLIOTECA ---")
        print("1. Carica biblioteca da file")
        print("2. Aggiungi un nuovo libro")
        print("3. Cerca un libro per titolo")
        print("4. Ordina titoli di una sezione")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                biblioteca = carica_da_file(file_path)
                if biblioteca is not None:
                    break

        elif scelta == "2":
            if not biblioteca:
                print("Prima carica la biblioteca da file.")
                continue

            titolo = input("Titolo del libro: ").strip()
            autore = input("Autore: ").strip()
            try:
                anno = int(input("Anno di pubblicazione: ").strip())
                pagine = int(input("Numero di pagine: ").strip())
                sezione = int(input("Sezione: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per anno, pagine e sezione.")
                continue

            libro = aggiungi_libro(biblioteca, titolo, autore, anno, pagine, sezione, file_path)
            if libro:
                print(f"Libro aggiunto con successo!")
            else:
                print("Non è stato possibile aggiungere il libro.")

        elif scelta == "3":
            if not biblioteca:
                print("La biblioteca è vuota.")
                continue

            titolo = input("Inserisci il titolo del libro da cercare: ").strip()
            risultato = cerca_libro(biblioteca, titolo)
            if risultato:
                print(f"Libro trovato: {risultato}")
            else:
                print("Libro non trovato.")

        elif scelta == "4":
            if not biblioteca:
                print("La biblioteca è vuota.")
                continue

            try:
                sezione = int(input("Inserisci numero della sezione da ordinare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_libri_sezione_per_titolo(biblioteca, sezione)
            if titoli is not None:
                print(f'\nSezione {sezione} ordinata:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()