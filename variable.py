import pygame


surface = pygame.display.set_mode((0,0),pygame.FULLSCREEN)

logo = pygame.image.load('images/Marouxo_Logo.png').convert_alpha()

background_fin = pygame.transform.scale(pygame.image.load('images/Fond de fin.png').convert_alpha(), (surface.get_size()))
background_fin.convert()

background_jeu = pygame.transform.scale(pygame.image.load('images/Jungle_Background.png').convert_alpha(), (surface.get_size()))
background_jeu.convert()

game_over = pygame.transform.scale(pygame.image.load('images/game-over.jpg').convert_alpha(), (surface.get_size()))
game_over.convert()

ligne = pygame.transform.scale(pygame.image.load('images/Plateforme/ligne.png').convert_alpha(), (int(3*surface.get_width()),int(4*surface.get_height()/5)))
ligne.convert()

drapeau = pygame.transform.scale(pygame.image.load('images/Plateforme/Drapeau.png').convert_alpha(), (int(surface.get_width()/32),int(surface.get_height()/4.8)))
drapeau.convert()

lianes = pygame.image.load('images/Plateforme/liane.png').convert_alpha()
lianes.convert()
liane_fixe = pygame.transform.scale(lianes, (int(surface.get_width()/32),int(surface.get_height()/2.4)))

bouton_on = pygame.transform.scale(pygame.image.load('images/Plateforme/bouton on.png').convert_alpha(), (int(surface.get_width()/25),int(surface.get_height()/25)))
bouton_on.convert()

bouton_off = pygame.transform.scale(pygame.image.load('images/Plateforme/bouton off.png').convert_alpha(), (int(surface.get_width()/25),int(surface.get_height()/25)))
bouton_off_rect = bouton_off.get_rect()
bouton_off_rect.x = int(2*surface.get_width()/ 2.17)
bouton_off_rect.y = int(4*surface.get_height()/ 4.7)

niveau1 = pygame.transform.scale(pygame.image.load('images/Plateforme/niveau1.png').convert_alpha(), (int(3*surface.get_width()),int(4*surface.get_height()/5)))
niveau1.convert()

niveau2 = pygame.transform.scale(pygame.image.load('images/Plateforme/niveau2.png').convert_alpha(), (int(surface.get_width()),int(2*surface.get_height())))
niveau2.convert()

salle_du_boss = pygame.transform.scale(pygame.image.load('images/Plateforme/salle du boss.png').convert_alpha(), (int(surface.get_width()),int(surface.get_height())))
salle_du_boss.convert()


m_saute_droite = pygame.transform.scale(pygame.image.load("images/Personnages/marouxo saut.png"), (int(2*surface.get_width()/48),int(4*surface.get_height()/45)))
m_saute_gauche = pygame.transform.flip(m_saute_droite,True,False)

m_immobile_droite = pygame.transform.scale(pygame.image.load("images/Personnages/marouxo immobile.png"), (int(2*surface.get_width()/48),int(4*surface.get_height()/45)))
m_immobile_gauche = pygame.transform.flip(m_immobile_droite,True,False)

m_mouvement_droite = pygame.transform.scale(pygame.image.load("images/Personnages/marouxo mouvement.png"), (int(2*surface.get_width()/48),int(4*surface.get_height()/45)))
m_mouvement_gauche = pygame.transform.flip(m_mouvement_droite,True,False)



m_immobile_droite_cinématique = pygame.transform.scale(pygame.image.load("images/Personnages/marouxo immobile.png"), (int(2*surface.get_width()/16),int(4*surface.get_height()/16)))
m_immobile_gauche_cinématique = pygame.transform.flip(m_immobile_droite_cinématique,True,False)

panda_roux_happy_droite = pygame.transform.scale(pygame.image.load("images/Personnages/panda_roux_happy.png"), (int(2*surface.get_width()/16),int(4*surface.get_height()/16)))
panda_roux_happy_gauche = pygame.transform.flip(panda_roux_happy_droite,True,False)

panda_roux_droite = pygame.transform.scale(pygame.image.load("images/Personnages/panda_roux.png"), (int(2*surface.get_width()/16),int(4*surface.get_height()/16)))
panda_roux_gauche = pygame.transform.flip(panda_roux_droite,True,False)

panda_roux_sad_droite = pygame.transform.scale(pygame.image.load("images/Personnages/panda_roux_sad.png"), (int(2*surface.get_width()/16),int(4*surface.get_height()/16)))
panda_roux_sad_gauche = pygame.transform.flip(panda_roux_sad_droite,True,False)
panda_roux_sad = pygame.transform.scale(panda_roux_sad_gauche, (int(2*surface.get_width()/50),int(4*surface.get_height()/50)))

Toadd = pygame.transform.scale(pygame.image.load("images/Personnages/Toadd.png"), (int(2*surface.get_width()/50),int(4*surface.get_height()/50)))

gorilla_droite = pygame.transform.scale(pygame.image.load("images/Personnages/gorilla.png"), (int(2*surface.get_width()/10),int(4*surface.get_height()/10)))
gorilla_gauche = pygame.transform.flip(gorilla_droite,True,False)


gorilla_moitié_vivent = pygame.transform.scale(pygame.image.load("images/Personnages/gorilla not alive.png"), (int(2*surface.get_width()/10),int(4*surface.get_height()/10)))
gorilla_mort = pygame.transform.scale(pygame.image.load("images/Personnages/gorilla dead.png"), (int(2*surface.get_width()/10),int(4*surface.get_height()/10)))



serpent_bleu_vivent = pygame.transform.scale(pygame.image.load("images/Personnages/snake blue alive.png"), (int(2*surface.get_width()/50),int(4*surface.get_height()/50)))
serpent_bleu_moitié_vivent = pygame.transform.scale(pygame.image.load("images/Personnages/snake blue not alive.png"), (int(2*surface.get_width()/50),int(4*surface.get_height()/50)))
serpent_bleu_mort = pygame.transform.scale(pygame.image.load("images/Personnages/snake blue dead.png"), (int(2*surface.get_width()/50),int(4*surface.get_height()/50)))

serpent_rouge_vivent = pygame.transform.scale(pygame.image.load("images/Personnages/snake red alive.png"), (int(2*surface.get_width()/50),int(4*surface.get_height()/50)))
serpent_rouge_moitié_vivent = pygame.transform.scale(pygame.image.load("images/Personnages/snake red not alive.png"), (int(2*surface.get_width()/50),int(4*surface.get_height()/50)))
serpent_rouge_mort = pygame.transform.scale(pygame.image.load("images/Personnages/snake red dead.png"), (int(2*surface.get_width()/50),int(4*surface.get_height()/50)))

serpent_vert_vivent = pygame.transform.scale(pygame.image.load("images/Personnages/snake green alive.png"), (int(2*surface.get_width()/50),int(4*surface.get_height()/50)))
serpent_vert_moitié_vivent = pygame.transform.scale(pygame.image.load("images/Personnages/snake green not alive.png"), (int(2*surface.get_width()/50),int(4*surface.get_height()/50)))
serpent_vert_mort = pygame.transform.scale(pygame.image.load("images/Personnages/snake green dead.png"), (int(2*surface.get_width()/50),int(4*surface.get_height()/50)))

panda_vivent = pygame.transform.scale(pygame.image.load("images/Personnages/panda alive.png"), (int(2*surface.get_width()/50),int(4*surface.get_height()/50)))
panda_moitié_vivent = pygame.transform.scale(pygame.image.load("images/Personnages/panda not alive.png"), (int(2*surface.get_width()/50),int(4*surface.get_height()/50)))
panda_mort = pygame.transform.scale(pygame.image.load("images/Personnages/panda dead.png"), (int(2*surface.get_width()/50),int(4*surface.get_height()/50)))



def bouton_text_arrondi(texte, couleur, x, y, largeur, hauteur, surface):
    pygame.draw.rect(surface, couleur, (x, y, largeur, hauteur), border_radius=int(hauteur//2))
    texte = pygame.font.Font("LuckiestGuy.ttf", int((largeur, hauteur)[1]*0.5)).render(texte, True, (255, 255, 255))
    surface.blit(texte, texte.get_rect(center=pygame.Rect(x, y, largeur, hauteur).center))

