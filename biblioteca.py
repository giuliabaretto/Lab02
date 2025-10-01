def carica_da_file(file_path):
    """Carica i libri dal file"""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            # prendo il file, lo leggo, tolgo \n a fine di ogni riga, e divido il file in righe
            righe = file.read().strip().splitlines()

    except FileNotFoundError:
        return None

    if not righe:
        return None      # nel caso non trovassi righe nel file

    # creare e popolare una struttura dati che rappresenta la biblioteca distribuendo i libri presenti nel file nelle sezioni corrette
    biblioteca = []

    numero_sezioni = int(righe[0])  # considero la prima riga che mi indica il numero di sezioni

    biblioteca = [[] for i in range(numero_sezioni)] # lista di 5 (numero delle mie sezioni) liste

    for riga in righe[1:]: # sennò parto da riga 0 e mi legge solo 5
        # print(riga)  (avevo fatto un controllo)
        titolo, autore, anno, pagine, sezione = riga.strip().split(",")
        anno = int(anno)
        pagine = int(pagine)
        sezione = int(sezione)
        if sezione < 1:
            continue
        libro = {"titolo": titolo, "autore": autore, "anno": anno, "pagine": pagine, "sezione": sezione}  # potrei eliminare il campo sezione perchè lo considero dopo (è ridondante)
        biblioteca[numero_sezioni-1].append(libro)
    # print(biblioteca) (avevo fatto un controllo, stampo una lista di dizionari)
    return biblioteca



def aggiungi_libro(biblioteca, titolo, autore, anno, pagine, sezione, file_path):
    """Aggiunge un libro nella biblioteca"""
    nuovo_libro = {"titolo": titolo, "autore": autore, "anno": anno, "pagine": pagine, "sezione": sezione }
    biblioteca.append(nuovo_libro)
    print(biblioteca)



def cerca_libro(biblioteca, titolo):
    """Cerca un libro nella biblioteca dato il titolo"""
    # TODO


def elenco_libri_sezione_per_titolo(biblioteca, sezione):
    """Ordina i titoli di una data sezione della biblioteca in ordine alfabetico"""
    # TODO


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

