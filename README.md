# Konsollkameratene™ Input Library

## Diverse kode fra Konsollkameratene Ltd.

`kontroller_input.py` er et (uferdig) bibliotek for å hente input fra kontrollere

`mini-eksempel.py` er et lite eksempel på hvordan du kan bruke biblioteket

`pygame-eksempel.py` er et program som viser hvordan du kan bruke Pygamekontroller til å emulere en fysisk kontroller med piltastene

`enhetssirkel.py` er et program for å teste biblioteket

## Kom i gang 01: Installer

Start med å installere biblioteket pyserial som brukes til å snakke med kontrollerne. Åpne CMD og kjør følgende kommando:

    pip install pyserial

Hvis kommandoen ikke funker er det sannsynligvis fordi du ikke har python installert på riktig måte. Gå i så fall inn på [python.org/downloads/](https://www.python.org/downloads/), last ned nyeste versjon og sørg for å velge:

- [x] Add python.exe to path

Endre til riktig versjon av python i vscode ved å trykke på knappen helt nederst til høyre der det står 3.10.9 eller noe liknende.

## Kom i gang 02: Programmer

Så kan vi begynne å bruke kontroller_input.py-biblioteket:
```python
import kontroller_input
```
Funksjonen hent_nye_kontrollere returnerer en liste med Kontroller-objekter:
```python
kontrollere = kontroller_input.hent_nye_kontrollere()
if len(kontrollere) == 0:
	print("Ingen tilkoblede kontrollere!")
	exit()
else:
	min_kontroller = kontrollere[0]
```
Kontroller-objektene har nyttige funksjoner og variabler som for eksempel `hent()`, som returnerer posisjonen til joysticken og hvilke knapper som er trykket:
```python
x, y, knappJ, knappA, knappB = min_kontroller.hent()
if knappJ:
	print("Joystick-knappen er trykket!")
```
Variablene x og y er posisjonen til joysticken. De vil begge være et desimaltall mellom -1 og 1. Når man ikke rører joysticken vil den altså være i [0, 0]. Merk også at posisjonen er normalisert sånn at den alltid vil være innenfor enhetssirkelen. Det betyr at den maksimale lengden til vektoren [x, y] er 1.

Dette betyr at du nå kan bruke variablene x og y til å for eksempel endre posisjonen til en spiller, uten å være bekymret for om den vil bevege seg raskere diagonalt enn horisontalt.

Si for eksempel at du har et objekt som heter spiller. Da kan vi bruke x og y som vi nå har hentet fra kontrolleren til å bevege spilleren:

```python
spiller.x += x * 10
spiller.y += y * 10
```

## Kom i gang 03: Testing uten kontroller

Det kan være nyttig å teste koden uten å være koblet til en fysisk kontroller. Derfor finnes også PygameKontroller-klassen som lar deg bruke piltastene til å emulere en kontroller.
```python
min_kontroller = kontroller_input.PygameKontroller()
```
Merk at du må gi hvilke knapper som er trykket som et argument til `hent()`:
```python
keys = pygame.key.get_pressed() # Henter trykkede knapper
x, y, knappJ, knappA, knappB = min_kontroller.hent(keys)
```
