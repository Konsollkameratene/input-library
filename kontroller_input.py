# Bibliotek for å kommunisere over USB med Pico-en vår:
import serial
import serial.tools.list_ports

# Følgende biblioteker brukes til testing:
from math import sin, cos
from time import perf_counter, sleep


# Vi lagrer de forrige input-ene vi mottok slik at hvis vi ikke mottar noe
# nytt innen neste gang hent() kjøres retunerer vi bare de gamle input-ene
x_joystick = 0
y_joystick = 0
knappJ = 0
knappA = 0
knappB = 0

# Serial-tilkoblingen vår lages i init() og lagres i ser:
ser = None


def init(port):
    global ser

    # timeout = 0: Venter ikke hvis
    ser = serial.serial_for_url(port, baudrate=115200, timeout=0)

# Work in progress:
# def hent_kontroller():
#     serial.tools.list_ports.comports()
#     return


def hent():
    global x_joystick, y_joystick, knappJ, knappA, knappB

    # Hvis init() ikke har blitt kjørt kan variabelen ser fortsatt være
    # None. Gi i så fall en feilmelding
    if ser is None:
        feil_har_ikke_kjort_init("hent()")

    tekst = ""

    while True:
        # Henter en linje med tekst og fjerner whitespace
        ny_tekst = ser.readline().decode().strip()
        if len(ny_tekst) > 0:
            tekst = ny_tekst
        else:
            break

    if len(tekst) > 0:
        kontroller_data = tekst.split(" ")
        if len(kontroller_data) == 5:
            x_joystick = float(kontroller_data[0])
            y_joystick = float(kontroller_data[1])

            lengde = (x_joystick**2 + y_joystick**2)**0.5
            if lengde > 1:
                x_joystick = x_joystick / lengde
                y_joystick = y_joystick / lengde

            knappJ = int(kontroller_data[2])
            knappA = int(kontroller_data[3])
            knappB = int(kontroller_data[4])

        else:
            rest_tekst = ser.readlines()
            rest_tekst = [x.decode() for x in rest_tekst]
            rest_tekst = "\n".join(rest_tekst)
            raise Exception(
                f"Mottok tekst med feil antall datapunkter: {tekst}")

    return x_joystick, y_joystick, knappJ, knappA, knappB


def test_data_send():
    """Send test-data. Brukes i kombinasjon med init('loop://') for
        å teste programmet uten å være koblet til en kontroller"""

    if ser is None:
        feil_har_ikke_kjort_init("test_send()")

    t = perf_counter()
    x = cos(t)
    y = sin(t)
    kJ = int(sin(t) > 3**0.5 / 3)
    kA = 0
    kB = 0
    tekst_ut = f"{x} {y} {kJ} {kA} {kB}\n"
    ser.write(tekst_ut.encode())


def feil_har_ikke_kjort_init(funksjon):
    raise Exception(
        f"Du må kjøre kontroller_input.init(port) før du kan kjøre {funksjon}!")


# Hvis programmet ikke importeres men kjøres direkte tester vi koden

TEST_MODUS = False

if __name__ == "__main__":
    if TEST_MODUS:
        # Data sendt til 'loop://' blir sendt tilbake igjen
        init("loop://")
    else:
        init("COM6")

    while True:
        sleep(1)
        print(*hent())

        if TEST_MODUS:
            # Generer og send test-data. Fordi vi sender til 'loop://' vil
            # vi motta disse dataene selv
            test_data_send()
