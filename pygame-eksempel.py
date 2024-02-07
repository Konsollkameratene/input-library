import pygame
import kontroller_input
import random

BREDDE = 640
HOYDE = 480
FPS = 30

pygame.init()
vindu = pygame.display.set_mode((BREDDE, HOYDE))
clock = pygame.time.Clock()


class Spiller:
    """
    Spilleren er en rød sirkel som kan bevege seg
    """

    def __init__(self, kontroller):
        # Kontrolleren som skal styre spilleren
        self.kontroller = kontroller

        self.radius = 15
        # Plasserer spilleren et tilfeldig sted på skjermen
        self.x = random.randint(self.radius, BREDDE-self.radius)
        self.y = random.randint(self.radius, HOYDE-self.radius)

    def tegn(self):
        # Tegner sirkelen
        pygame.draw.circle(vindu, (200, 0, 0), (self.x, self.y), self.radius)

    def logikk(self, keys):
        # Henter input fra kontrolleren som hører til spilleren
        # Dette kan enten være en fysisk Kontroller eller en PygameKontroller
        x, y, knappJ, knappA, knappB = self.kontroller.hent(keys)
        # Merk at vi må gi keys (altså knappene som er trykket) for at
        #  PygameKontroller skal funke. Hvis self.kontroller er en fysisk
        #  kontroller ignoreres dette

        if knappJ:
            self.radius = 15
        if knappA:
            self.radius += 1
        if knappB:
            self.radius -= 1

        self.x += x * 5
        self.y += y * 5


spillere = []
for ny_kontroller in kontroller_input.hent_nye_kontrollere():
    ny_spiller = Spiller(kontroller=ny_kontroller)
    spillere.append(ny_spiller)

# Hvis det ikke er noen tilkoblede kontrollere lager vi en spiller som
#  kan kontrolleres med piltastene
if len(spillere) == 0:
    # PygameKontroller lar deg bruke piltastene
    ny_spiller = Spiller(kontroller=kontroller_input.PygameKontroller())
    spillere.append(ny_spiller)

fortsett = True
while fortsett:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fortsett = False

    vindu.fill((255, 255, 255))

    # Henter knappene som er trykket
    keys = pygame.key.get_pressed()

    for spiller in spillere:
        # Gir keys inn som argument til logikk-funksjonen som skal
        #  flytte på spilleren
        spiller.logikk(keys)

    for spiller in spillere:
        spiller.tegn()

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
