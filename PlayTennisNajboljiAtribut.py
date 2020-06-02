import pandas as pd
import math

days = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
outlook = ["Sunny", "Sunny", "Overcast", "Rain", "Rain", "Rain", "Overcast", "Sunny", "Sunny", "Rain", "Sunny", "Overcast", "Overcast", "Rain"]
temperature = ["Hot", "Hot", "Hot", "Mild", "Cool", "Cool", "Cool", "Mild", "Cool", "Mild", "Mild", "Mild", "Hot", "Mild"]
humidity = ["High", "High", "High", "High", "Normal", "Normal", "Normal", "High", "Normal", "Normal", "Normal", "High", "Normal", "High"]
wind = ["Weak", "Strong", "Weak", "Weak", "Weak", "Strong", "Strong", "Weak", "Weak", "Weak", "Strong", "Strong", "Weak", "Strong"]
playTennisYesNo = ["No", "No", "Yes", "Yes", "Yes", "No", "Yes", "No", "Yes", "Yes", "Yes", "Yes", "Yes", "No"]
dataframe = pd.DataFrame({"Days": days, "Outlook": outlook, "Temperature": temperature, "Humidity": humidity, "Wind": wind, "Play Tennis": playTennisYesNo})

# Racunamo meru neodredjenosti atributa sumiranjem logaritama sa razlomkom razlicitih vrednosti
# U ovom slucaju entropija predstavlja meru nehomogensoti klasa
def entropija(n, values):
  entropija = 0.0
  for i in values:
    ucestalostVrednosti = i / n
    if ucestalostVrednosti > 0.0:
      entropija -= ucestalostVrednosti * math.log2(ucestalostVrednosti)
  return entropija

# Racunamo meru informativnosti atrbuta preko formule informacionog dobitka
# Ovo predstavlja meru efektivnosti atributa pri klasifikaciji obucavanja
# To je informacija o vrednosti ciljne funkcije za poznatu vrednost odredjenog atributa
def informacioniDobitak(df, entropyY, attribute, vrednosti):
  infDobitak = entropyY
  for i in vrednosti:
    brojPozINeg = df.loc[df[attribute] == i, "Play Tennis"].value_counts().reindex(df["Play Tennis"].unique(), fill_value=0)
    valuesForEntropy = [brojPozINeg["Yes"], brojPozINeg["No"]]
    vrednosti = brojPozINeg.sum() / len(df)
    # Radimo redukciju polazne entropije particionisanjem primera na osnovu trenutnog atributa
    infDobitak -= vrednosti * entropija(brojPozINeg.sum(), valuesForEntropy)
  return infDobitak


# Odredjuje koliko je informacija razdvojena razlicitm vrednostima.
def razdvojenostInformacije(n, vrednosti):
  razdvojenost = 0.0
  for i in vrednosti:
    ucestalostVrednosti = i / n
    if ucestalostVrednosti > 0.0:
      razdvojenost -= ucestalostVrednosti * math.log2(ucestalostVrednosti)
  return razdvojenost

# Formula koja je robusnija od samog informacionog dobitka
def stepenDobitka(informacioniDobitak, razdvojenostInformacije):
  return informacioniDobitak / razdvojenostInformacije

def nadjiNajboljiAtributZaKlasifikaciju(df, koloneVrednosti):
  n = len(df)
  # Naci prvo entropiju za Target Value kolonu 'Play Tennis'
  pozitivnih = len(df[df["Play Tennis"] == "Yes"])
  negativnih = len(df[df["Play Tennis"] == "No"])
  entropijaVrednostiPozNeg= [pozitivnih, negativnih]
  entropijaYesNo = entropija(n, entropijaVrednostiPozNeg)

  # Naci atribut sa najvecim informacionim dobitkom
  informacioniDobici = {}
  sumaInformacionihDobitaka = 0.0
  for kolona in koloneVrednosti:
    infDobitak = informacioniDobitak(df, entropijaYesNo, kolona, koloneVrednosti[kolona])
    informacioniDobici[kolona] = infDobitak
    sumaInformacionihDobitaka += infDobitak

  # Ako je razdvojenostInformacije veoma mala, to moze dati za neke atribute veliki informacioni dobitak
  # Zato cemo racunati stepenDobitka samo za one atribute ciji je stepen dobitka iznad prosecnog
  avgInfoDobitak = sumaInformacionihDobitaka / len(koloneVrednosti)
  najveciStepenDobitka = 0.0
  najboljiAtribut = ""
  for kolona in informacioniDobici.keys():

    # Heuristika: Racunaj stepen dobitka samo atribute sa vecim informacionim dobitkom od prosecnog
    if informacioniDobici[kolona] > avgInfoDobitak:
      vrednosti = []
      for j in koloneVrednosti[kolona]: # Prikupi broj ponavljanja svih vrednosti atributa u skupu
        brojPojavljivanjaVrednosti = len(df[df[kolona] == j])
        vrednosti.append(brojPojavljivanjaVrednosti)
      razdvojenost = razdvojenostInformacije(n, vrednosti) 
      racioDobitka = stepenDobitka(informacioniDobici[kolona], razdvojenost)
      if racioDobitka > najveciStepenDobitka:
        najveciStepenDobitka = racioDobitka
        najboljiAtribut = kolona

  return najboljiAtribut, najveciStepenDobitka

koloneVrednosti = {"Outlook": ["Sunny", "Overcast", "Rain"], "Temperature": ["Hot", "Mild", "Cool"], "Humidity": ["Normal", "High"], "Wind": ["Weak", "Strong"]}
najAtr, infDobitak = nadjiNajboljiAtributZaKlasifikaciju(dataframe, koloneVrednosti)
print("Najbolji atribut za klasifikaciju je: " + najAtr + " sa stepenom dobitka: " + str(infDobitak))