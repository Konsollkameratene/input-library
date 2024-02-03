import kontroller_input
from time import sleep

# Forsøker å hente 1 kontroller
kontrollere = kontroller_input.hent_nye_kontrollere(maks_antall=1)


if len(kontrollere) == 0:
    print("Ingen tilkoblede kontrollere: Lager TestKontroller")
    min_kontroller = kontroller_input.TestKontroller()
else:
    min_kontroller = kontrollere[0]


while True:
    x, y, knappJ, knappA, knappB = min_kontroller.hent()
    if knappJ:
        print("Joystick-knappen er trykket! Joysticken er i posisjon",
              round(x, 2), round(y, 2))
    sleep(0.5)
