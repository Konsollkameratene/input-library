import pygame
import kontroller_input
import random

pygame.init()

# Bruk TEST_MODUS = True hvis du vil teste programmet uten kontroller
# Hvis TEST_ROBHUSTHET = True varierer antall input-er som sendes hver
# frame for å teste hvordan kontroller_input håndterer å enten ha
# flere ventende input-data eller ingen
TEST_MODUS = False
TEST_ROBUSTHET = False


if TEST_MODUS:
    # Når vi bruker port='loop://' blir alt vi sender sendt tilbake til oss
    # Dette brukes til testing når vi ikke er koblet til en kontroller
    kontroller_input.init(port="loop://")
else:
    kontroller_input.init(port="COM6")


BREDDE = 480
HOYDE = 480
HALV_BREDDE = BREDDE // 2
HALV_HOYDE = HOYDE // 2

FPS = 60
BG_FARGE = (175, 175, 175)

vindu = pygame.display.set_mode((BREDDE, HOYDE))
font = pygame.font.SysFont("Consolas", 14)
clock = pygame.time.Clock()


def omgjor_koordinater(x, y):
    x = HALV_BREDDE + x * BREDDE // 3
    y = HALV_HOYDE + y * HOYDE // 3
    return (x, y)


def tegn_tekst(x, y, tekst: str):
    skrift = font.render(tekst, True, BG_FARGE)
    vindu.blit(skrift, (x + 5, y + 5))


def tegn_bakgrunn():
    pygame.draw.circle(vindu, BG_FARGE, (HALV_HOYDE,
                       HALV_HOYDE), BREDDE // 3, width=1)

    pygame.draw.line(vindu, BG_FARGE,
                     (0, HALV_HOYDE), (BREDDE, HALV_HOYDE))
    pygame.draw.line(vindu, BG_FARGE,
                     (HALV_BREDDE, 0), (HALV_BREDDE, HOYDE))

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

    # Sender falske test-data som vi så mottar i retur
    if TEST_MODUS:
        if not TEST_ROBUSTHET:
            # Hvis vi ikke tester robustheten sender vi en input
            # for hver gang vi leser input
            kontroller_input.test_data_send()
        else:
            # Ellers sender vi mellom 0 og 3 input-er
            for i in range(random.randint(0, 3)):
                kontroller_input.test_data_send()

    # Henter kontroller-input
    x_enhetssirkel, y_enhetssirkel, knappJ, knappA, knappB = kontroller_input.hent()

    # Konverterer koordinater i enhetssirkelen til koordinater på skjermen
    x_skjerm, y_skjerm = omgjor_koordinater(
        x_enhetssirkel, y_enhetssirkel)

    # Gjør bakgrunnen rød hvis knapp1 er trykket
    fill_farge = (255, 255, 255) if not knappJ else (255, 100, 100)
    vindu.fill(fill_farge)
    tegn_bakgrunn()

    pygame.draw.aaline(vindu, (0, 0, 0), (HALV_BREDDE,
                       HALV_HOYDE), (x_skjerm, y_skjerm))

    pygame.draw.circle(vindu, (50, 50, 50),
                       (x_skjerm, y_skjerm), 5)

    pygame.display.flip()

pygame.quit()
