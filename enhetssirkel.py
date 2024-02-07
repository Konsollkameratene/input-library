import pygame
import kontroller_input
import random

pygame.init()

# Bruk TEST_MODUS = True hvis du vil teste programmet uten kontroller
# Hvis TEST_ROBHUSTHET = True varierer antall input-er som sendes hver
# frame for å teste hvordan kontroller_input håndterer å ha
# flere ventende input-data
TEST_MODUS = True
TEST_ROBUSTHET = False

if TEST_MODUS:
    # Lager en TestKontroller som ikke automatisk sender test-data, slik at
    #  vi kan variere hvor mange ganger vi sender test-data (trenges
    #  til TEST_ROBUSTHET)
    kontroller = kontroller_input.TestKontroller(test_data=False)
else:
    nye_kontrollere = kontroller_input.hent_nye_kontrollere()
    if len(nye_kontrollere) < 1:
        print("Koble til en kontroller før du kjører programmet!")
        exit()
    kontroller = nye_kontrollere[0]

BREDDE = 480
HALV_BREDDE = BREDDE // 2

FPS = 60
BG_FARGE = (175, 175, 175)

vindu = pygame.display.set_mode((BREDDE, BREDDE))
font = pygame.font.SysFont("Consolas", 14)
clock = pygame.time.Clock()


def omgjor_koordinater(x, y):
    x = HALV_BREDDE + x * BREDDE // 3
    y = HALV_BREDDE + y * BREDDE // 3
    return (x, y)


def tegn_tekst(x, y, tekst: str):
    skrift = font.render(tekst, True, BG_FARGE)
    vindu.blit(skrift, (x + 5, y + 5))


def tegn_bakgrunn():
    pygame.draw.circle(vindu, BG_FARGE, (HALV_BREDDE,
                       HALV_BREDDE), BREDDE // 3, width=1)

    pygame.draw.line(vindu, BG_FARGE,
                     (0, HALV_BREDDE), (BREDDE, HALV_BREDDE))
    pygame.draw.line(vindu, BG_FARGE,
                     (HALV_BREDDE, 0), (HALV_BREDDE, BREDDE))

    x, y = omgjor_koordinater(1, 0)
    tegn_tekst(x, y, "1")

    x, y = omgjor_koordinater(-1, 0)
    tegn_tekst(x, y, "-1")

    x, y = omgjor_koordinater(0, 1)
    tegn_tekst(x, y, "1")

    x, y = omgjor_koordinater(0, -1)
    tegn_tekst(x, y, "-1")


fortsett = True

while fortsett:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fortsett = False

    # Følgende er kun for testing og bør ikke brukes i et faktisk program
    # Du kan trygt ignorere det hvis du ikke forstår
    if TEST_MODUS:
        # Sender falske test-data som vi så mottar i retur
        if TEST_ROBUSTHET:
            for i in range(random.randint(0, 3)):
                kontroller.test_data_send()
        else:
            kontroller.test_data_send()

    # Henter input fra kontrolleren vår
    x_enhetssirkel, y_enhetssirkel, knappJ, knappA, knappB = kontroller.hent()

    # Konverterer koordinater i enhetssirkelen til koordinater på skjermen
    x_skjerm, y_skjerm = omgjor_koordinater(
        x_enhetssirkel, y_enhetssirkel)

    # Gjør bakgrunnen rød hvis joystick-knappen er trykket
    fill_farge = (255, 100, 100) if knappJ else (255, 255, 255)
    vindu.fill(fill_farge)
    tegn_bakgrunn()

    pygame.draw.aaline(vindu, (0, 0, 0), (HALV_BREDDE,
                       HALV_BREDDE), (x_skjerm, y_skjerm))

    pygame.draw.circle(vindu, (50, 50, 50),
                       (x_skjerm, y_skjerm), 5)

    pygame.display.flip()

pygame.quit()
