import matplotlib.pyplot as plt
from datetime import datetime
import random
import json
import os
import plotly.express as px
import pandas as pd


def pridat_prijem(prijem, zustatek, kategorie_castky):
    zustatek += prijem
    print(f"\n{'-'*40}\nPříjem ve výši {prijem} Kč byl úspěšně přidán.\nNový zůstatek je {zustatek} Kč.\n{'-'*40}")
    
    aktualni_prijem = kategorie_castky.get("prijem", 0)
    nova_hodnota_prijmu = aktualni_prijem + prijem
    kategorie_castky["prijem"] = nova_hodnota_prijmu
    
    return zustatek, kategorie_castky


def pridat_vydaj(vydaj, kategorie, zustatek, kategorie_castky):
    zustatek -= vydaj
    print(f"\n{'-'*40}\nVýdaj ve výši {vydaj} Kč byl přidán do kategorie '{kategorie}'.\nNový zůstatek je {zustatek} Kč.\n{'-'*40}")
    
    aktualni_vydaj = kategorie_castky.get(kategorie, 0)
    nova_hodnota_vydaje = aktualni_vydaj - vydaj
    kategorie_castky[kategorie] = nova_hodnota_vydaje
    
    return zustatek, kategorie_castky


def zobrazit_zustatek(zustatek):
    print(f"\n{'-'*40}\nAktuální zůstatek na účtu je {zustatek} Kč.\n{'-'*40}")


def zobrazit_kategorie(kategorie_castky):
    print("\nKategorie příjmů a výdajů:\n" + '-'*40)
    for kategorie, castka in kategorie_castky.items():
        print(f"{kategorie}: {castka} Kč")
    print('-'*40)


def zobrazit_graf_kategorii(kategorie_castky):
    prijmy = kategorie_castky.get("prijem", 0)
    vydaje = {k: -v for k, v in kategorie_castky.items() if k != "prijem" and v < 0}

    if vydaje:
        labels = ["Příjem"] + list(vydaje.keys())
        sizes = [prijmy] + list(vydaje.values())
        colors = ['#ff9999'] + [plt.cm.Spectral(random.random()) for _ in range(len(vydaje))]
        explode = (0.1,) * len(labels)

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors, explode=explode, shadow=True)
        ax.axis('equal')
        plt.title('Přehled kategorií')

        plt.legend(labels, loc="best")
        plt.show()
    else:
        print("Chyba: Žádné kategorie nebo žádné záporné hodnoty výdajů pro vykreslení grafu.")


def zobrazit_interaktivni_graf_kategorii(kategorie_castky):
    prijmy = kategorie_castky.get("prijem", 0)
    vydaje = {k: -v for k, v in kategorie_castky.items() if k != "prijem" and v < 0}

    if vydaje:
        labels = ["Příjem"] + list(vydaje.keys())
        sizes = [prijmy] + list(vydaje.values())
        
        df = pd.DataFrame({'Kategorie': labels, 'Částka': sizes})

        fig = px.pie(df, names='Kategorie', values='Částka', title='Přehled kategorií')
        fig.show()
    else:
        print("Chyba: Žádné kategorie nebo žádné záporné hodnoty výdajů pro vykreslení grafu.")


def mesicni_report(kategorie_castky):
    mesic = datetime.now().strftime("%B %Y")
    print(f"\nMěsíční report za {mesic}:\n" + '-'*30)

    celkove_prijmy = kategorie_castky.get("prijem", 0)
    celkove_vydaje = sum(-castka for kategorie, castka in kategorie_castky.items() if kategorie != "prijem" and castka < 0)

    print(f"Celkové příjmy: {celkove_prijmy} Kč")
    print(f"Celkové výdaje: {celkove_vydaje} Kč")

    print("Detailní přehled výdajů:")
    for kategorie, castka in kategorie_castky.items():
        if kategorie != "prijem" and castka < 0:
            print(f"- {kategorie}: {-castka} Kč")
    print('-'*30)


def ulozit_data(zustatek, kategorie_castky, soubor="financni_data.json"):
    data = {
        "zustatek": zustatek,
        "kategorie_castky": kategorie_castky
    }
    with open(soubor, "w") as file:
        json.dump(data, file)
    print("Data byla úspěšně uložena.")


def nacist_data(soubor="financni_data.json"):
    if os.path.exists(soubor):
        with open(soubor, "r") as file:
            data = json.load(file)
        return data["zustatek"], data["kategorie_castky"]
    else:
        return 0, {}


def planovac_rozpoctu(zustatek,kategorie_castky):
    print("Plánovač rozpočtu na příští měsíc.")
    planovany_prijem = float(input("Zadejte plánovaný příjem na příští měsíc: "))
    planovane_vydaje = {}

    while True:
        kategorie = input("Zadejte kategorii výdaje (nebo 'konec' pro ukončení): ")
        if kategorie == 'konec':
            break
        castka = float(input(f"Zadejte částku pro kategorii '{kategorie}': "))
        planovane_vydaje[kategorie] = castka

    print("\nPlánovaný rozpočet:\n" + '-'*30)
    print(f"Plánovaný příjem: {planovany_prijem} Kč")
    for kategorie, castka in planovane_vydaje.items():
        print(f"{kategorie}: {castka} Kč")
    
    celkove_vydaje = sum(planovane_vydaje.values())
    predpokladany_zustatek = zustatek + planovany_prijem - celkove_vydaje
    print(f"Počáteční zůstatek: {zustatek} Kč")
    print(f"Předpokládaný zůstatek na konci měsíce: {predpokladany_zustatek} Kč\n" + '-'*30)


def resetovat_data(soubor="financni_data.json"):
    if os.path.exists(soubor):
        os.remove(soubor)
        print("Data byla úspěšně resetována.")
    else:
        print("Soubor s daty neexistuje.")


def hlavni():
    zustatek, kategorie_castky = nacist_data()

    print("Vítejte v programu pro správu financí!")

    while True:
        print("\nCo chcete udělat?")
        print("1. Přidat příjem")
        print("2. Přidat výdaj")
        print("3. Zobrazit aktuální zůstatek")
        print("4. Zobrazit kategorie příjmů a výdajů")
        print("5. Zobrazit graf kategorií")
        print("6. Zobrazit interaktivní graf kategorií")
        print("7. Měsíční report")
        print("8. Uložit data")
        print("9. Plánovač rozpočtu na příští měsíc")
        print("10. Resetovat data")  
        print("11. Konec")

        volba = input("Zadejte číslo možnosti: ")

        if volba == '1':
            prijem = float(input("Zadejte částku příjmu: "))
            zustatek, kategorie_castky = pridat_prijem(prijem, zustatek, kategorie_castky)
        elif volba == '2':
            vydaj = float(input("Zadejte částku výdaje: "))
            kategorie = input("Zadejte kategorii výdaje: ")
            zustatek, kategorie_castky = pridat_vydaj(vydaj, kategorie, zustatek, kategorie_castky)
        elif volba == '3':
            zobrazit_zustatek(zustatek)
        elif volba == '4':
            zobrazit_kategorie(kategorie_castky)
        elif volba == '5':
            zobrazit_graf_kategorii(kategorie_castky)
        elif volba == '6':
            zobrazit_interaktivni_graf_kategorii(kategorie_castky)
        elif volba == '7':
            mesicni_report(kategorie_castky)
        elif volba == '8':
            ulozit_data(zustatek, kategorie_castky)
        elif volba == '9':
            planovac_rozpoctu(zustatek, kategorie_castky)
        elif volba == '10':
            resetovat_data()  
        elif volba == '11':
            ulozit_data(zustatek, kategorie_castky)
            print("Děkujeme za použití programu. Nashledanou!")
            break
        else:
            print("Neplatná volba. Zkuste to znovu.")

if __name__ == "__main__":
    hlavni()
