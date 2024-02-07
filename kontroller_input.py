# Bibliotek for å kommunisere over USB med Pico-en vår:
import serial
import serial.tools.list_ports

# Følgende biblioteker brukes til testing:
from math import sin, cos
from time import perf_counter, sleep

# Følgende er kodene til 1, 2 og 3 på tastaturet og piltastene
PYGAME_K_1 = 49
PYGAME_K_2 = 50
PYGAME_K_3 = 51
PYGAME_K_RIGHT = 1073741903
PYGAME_K_LEFT = 1073741904
PYGAME_K_DOWN = 1073741905
PYGAME_K_UP = 1073741906

# Liste for å lagre alle tilkoblede kontrollere
kontrollere = []

# Sett for å lagre tilkoblede porter slik at vi enkelt kan sjekke
#  om vi er koblet til en port fra før av eller ikke i hent_kontrollere()
kontrollere_porter = set()

# Foreløpig er ikke koden feilfri. Denne variabelen teller ting som går galt
feil_teller = 0


class Kontroller:
    def __init__(self, port):

        # Serial-tilkoblingen vi bruker til å kommunisere med Pico-en
        # Underscore foran navnet forteller at variabelen kun bør brukes
        #  innad i klassen (og ikke utenifra)
        self._tilkobling = serial.serial_for_url(
            port, baudrate=115200, timeout=0)
        self.port = port
        kontrollere_porter.add(port)

        # Vi lagrer de forrige input-ene vi mottok slik at hvis vi ikke mottar noe
        # nytt innen neste gang hent() kjøres retunerer vi bare de gamle input-ene
        self.x = 0
        self.y = 0
        self.knappJ = 0
        self.knappA = 0
        self.knappB = 0

        self.deadzone = 0.03

        self.pause = False

        kontrollere.append(self)

    def hent(self, keys=None):
        """
        Henter data fra kontrolleren og retunerer dem.
        Argumentet keys gjør ingenting: Dette er kun for kompatibilitet med
         kode som bruker PygameKontroller, der man må gi en verdi for keys
        """
        tekst = ""

        while True:
            # Henter en linje med tekst og fjerner whitespace
            ny_tekst = self._tilkobling.readline().decode().strip()
            if len(ny_tekst) > 0:
                tekst = ny_tekst
            else:
                break

        if len(tekst) > 0:
            kontroller_data = tekst.split(" ")
            if len(kontroller_data) == 5:
                self.x = float(kontroller_data[0])
                self.y = float(kontroller_data[1])

                lengde = (self.x**2 + self.y**2)**0.5
                if lengde < self.deadzone:
                    self.x = 0.0
                    self.y = 0.0
                elif lengde > 1:
                    self.x = self.x / lengde
                    self.y = self.y / lengde

                self.knappJ = int(kontroller_data[2])
                self.knappA = int(kontroller_data[3])
                self.knappB = int(kontroller_data[4])
            else:
                # Hvis vi leser dataene fra kontrolleren samtidig som den er i
                #  ferd med å sende nye data, vil vi ikke lese dataene riktig
                #  og vil få feil antall datapunkter. Dette bør fikses i
                #  fremtiden, men foreløpig teller vi antall ganger dette
                #  skjer, som heldigvis ikke er så ofte
                global feil_teller
                feil_teller += 1

        return self.x, self.y, self.knappJ, self.knappA, self.knappB

    def koble_fra(self):
        self._tilkobling.close()
        kontrollere_porter.remove(self.port)
        kontrollere.remove(self)
        del self

    def test_data_send(self):
        """Send test-data. Brukes i kombinasjon med port='loop://' for
            å teste programmet uten å være koblet til en kontroller"""

        if self.port != "loop://":
            print(
                "Advarsel: test_data_send() bør brukes i kombinasjon \
                  med port='loop://' for å teste programmet uten å være \
                  koblet til en kontroller")

        t = perf_counter()
        x = cos(t)
        y = sin(t)
        kJ = int(sin(t) > 0.9)
        kA = 0
        kB = 0
        tekst_ut = f"{x} {y} {kJ} {kA} {kB}\n"
        self._tilkobling.write(tekst_ut.encode())


class TestKontroller(Kontroller):
    def __init__(self, test_data: bool = True):
        # Data sendt til 'loop://' blir sendt tilbake igjen
        self.test_data = test_data
        super().__init__(port="loop://")

    def hent(self):
        if self.test_data:
            self.test_data_send()
        return super().hent()


class PygameKontroller:
    """
    En 'falsk' kontroller som kan brukes til testing siden den emulerer en
     kontroller ved hjelp av piltastene på tastaturet. Se pygame-eksempel.py
    """

    def __init__(self):
        self.x = 0
        self.y = 0
        self.knappJ = 0
        self.knappA = 0
        self.knappB = 0

    def hent(self, keys):
        self.x = 0
        self.y = 0
        if keys[PYGAME_K_RIGHT]:
            self.x += 1
        if keys[PYGAME_K_LEFT]:
            self.x -= 1
        if keys[PYGAME_K_DOWN]:
            self.y += 1
        if keys[PYGAME_K_UP]:
            self.y -= 1

        lengde = (self.x**2 + self.y**2)**0.5
        if lengde > 1:
            self.x = self.x / lengde
            self.y = self.y / lengde

        self.knappJ = keys[PYGAME_K_1]
        self.knappA = keys[PYGAME_K_2]
        self.knappB = keys[PYGAME_K_3]

        return self.x, self.y, self.knappJ, self.knappA, self.knappB


def hent_nye_kontrollere(maks_antall: int = -1) -> list[Kontroller]:
    """
    Hent nye Kontroller-objekter som har blitt tilkoblet siden sist.
    maks_antall (int): Antall kontrollere vi prøver å hente. Negative tall betyr så
        mange som mulig (dette er default)
    """
    enheter = serial.tools.list_ports.comports()

    nye_kontrollere = []
    for enhet in enheter:
        if len(kontrollere) == maks_antall:
            break
        if enhet.name in kontrollere_porter:
            # Hopper over enheten hvis vi allerede er koblet til den
            continue
        if enhet.vid == 11914:
            # __init__-funksjonen lagrer automatisk til kontrollere-listen
            kontroller = Kontroller(port=enhet.name)

            nye_kontrollere.append(kontroller)
            print("Pico?:", end=" ")
        print(enhet)

    return nye_kontrollere


if __name__ == "__main__":
    TEST_MODUS = True

    if TEST_MODUS:
        print("TEST_MODUS!")
        kontroller = TestKontroller()
    else:
        nye_kontrollere = hent_nye_kontrollere()
        if len(nye_kontrollere) < 1:
            print("Koble til kontroller!")
            exit()
        kontroller = nye_kontrollere[0]

    while True:
        sleep(0.5)
        print(*kontroller.hent())
