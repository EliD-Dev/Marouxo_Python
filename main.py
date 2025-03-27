import pygame
from variable import *
from classe import *


def acceuil(surface):
    bouton_jouer = pygame.Rect(surface.get_width()*0.4, surface.get_height()*0.725, surface.get_width()*0.2, surface.get_height()*0.1)
    running = True
    while running:
        surface.blit(background_jeu,(0,0))
        surface.blit(logo,(int((surface.get_width()-logo.get_width())/1.95),int(0.75*surface.get_height()/5)))
        bouton_text_arrondi("Jouer", (0, 200, 0), surface.get_width()*0.4, surface.get_height()*0.725, surface.get_width()*0.2, surface.get_height()*0.1, surface)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_RETURN:
                    jouer(surface,True,1,niveau1)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_jouer.collidepoint(event.pos):
                    jouer(surface,True,1,niveau1)

        pygame.display.update()


def jouer(surface,jouer_cinématique,numero_de_la_cinématique,niveau):
    marouxo = Marouxo(niveau)
    marouxo.ajouter_plateforme()
    marouxo.ajouter_mur()
    marouxo.ennemies = definir_les_ennemie(marouxo)
    tmp = 0
    marouxo.n_cinématique = numero_de_la_cinématique
    if jouer_cinématique == True:
        marouxo.en_cinématique = True
    elif jouer_cinématique == False:
        marouxo.en_cinématique = False

    if marouxo.niveau == niveau2:
        marouxo.vu_y = 1080
    else:
        marouxo.vu_y = 0

    running = True
    while running:
        
        surface.blit(background_jeu,(0,0))

        touche_preser = pygame.key.get_pressed()

        if touche_preser[pygame.K_ESCAPE]:
            running = False
            pygame.quit()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()


        else:
            marouxo.image = m_immobile_droite if marouxo.direction == "Droite" else m_immobile_gauche


        if marouxo.en_cinématique == False:
            if marouxo.verifie_en_saut == True:
                marouxo.saut()
                if marouxo.rect.y >= surface.get_height():

                    surface.blit(game_over,(0,0))
                    pygame.display.update()
                    pygame.time.wait(2000)

                    running = False
                    return jouer(surface,False,numero_de_la_cinématique,niveau)

            if marouxo.verifie_en_saut == False and marouxo.verifie_platforme == False:
                if marouxo.rect.y <= surface.get_height():
                    marouxo.rect.y += int(marouxo.vitesse/1.01)
                else:

                    surface.blit(game_over,(0,0))
                    pygame.display.update()
                    pygame.time.wait(2000)

                    running = False
                    return jouer(surface,False,numero_de_la_cinématique,niveau)



            touche_preser = pygame.key.get_pressed()

            if touche_preser[pygame.K_ESCAPE]:
                pygame.quit()
                quit()

            elif touche_preser[pygame.K_r]:
                return jouer(surface,False)


            elif touche_preser[pygame.K_LEFT] or touche_preser[pygame.K_q]:
                marouxo.déplacement_gauche()
                if marouxo.verifie_en_saut == False and (touche_preser[pygame.K_UP] or touche_preser[pygame.K_z] or touche_preser[pygame.K_SPACE]):
                        marouxo.vitesse_saut = marouxo.rect.y
                        marouxo.déplacement_saute()


            elif touche_preser[pygame.K_RIGHT] or touche_preser[pygame.K_d]:
                marouxo.déplacement_droite()
                if marouxo.verifie_en_saut == False and (touche_preser[pygame.K_UP] or touche_preser[pygame.K_z] or touche_preser[pygame.K_SPACE]):
                    marouxo.vitesse_saut = marouxo.rect.y
                    marouxo.déplacement_saute()

            elif marouxo.verifie_en_saut == False and (touche_preser[pygame.K_UP] or touche_preser[pygame.K_z] or touche_preser[pygame.K_SPACE]):
                marouxo.vitesse_saut = marouxo.rect.y
                marouxo.déplacement_saute()

            if marouxo.niveau == niveau1:
                
                surface.blit(marouxo.niveau,(0, int(4*surface.get_height()/20)), (marouxo.vu_x, marouxo.vu_y, surface.get_width(), surface.get_height()))
                marouxo.niveau.blit(drapeau,(int(2*marouxo.niveau.get_width()/2.223), int(4*marouxo.niveau.get_height()/ 5000)))
                marouxo.hauter_saut = 15.5
                
            else:
                surface.blit(marouxo.niveau,(0, 0), (marouxo.vu_x, marouxo.vu_y, surface.get_width(), surface.get_height()))
                
                if marouxo.niveau == niveau2:
                    marouxo.hauter_saut = 50.5
                    
                if marouxo.niveau == salle_du_boss:
                    marouxo.hauter_saut = 15.5
                    
                    surface.blit(panda_roux_sad,(int(2*surface.get_width()/ 2.7),int(4*surface.get_height()/ 8000.7)))
                    surface.blit(Toadd,(int(2*surface.get_width()/ 2.9),int(4*surface.get_height()/ 8000.7)))
                    
                    if marouxo.boss_mort == True:
                        surface.blit(bouton_on,bouton_off_rect)
                    else:
                        surface.blit(bouton_off,bouton_off_rect)
                        


            surface.blit(marouxo.image, marouxo.rect)
            """ Afficher les plateformes et les murs
            P = pygame.sprite.Group()
            P.add(marouxo.plateformes)

            M = pygame.sprite.Group()
            M.add(marouxo.murs)

            P.draw(surface)
            M.draw(surface)
            """
            if marouxo.rect.colliderect(bouton_off_rect) and marouxo.rect.bottom <= bouton_off_rect.centery:
                marouxo.boss_mort = True
                
            for ennemie in marouxo.ennemies:
                if ennemie.type_ennemi != "Fin Niveau":
                    ennemie.affiche_ennemie()
                if marouxo.boss_mort != True:
                    ennemie.déplacement()
                if ennemie.type_ennemi == "Fin Niveau" and marouxo.rect.colliderect(ennemie.rect):
                    marouxo.en_cinématique = True
                    
                if marouxo.boss_mort == True:
                    ennemie.mort()

                if marouxo.rect.colliderect(ennemie.rect) and marouxo.rect.bottom <= ennemie.rect.centery and ennemie.type_ennemi != "Fin Niveau":
                    ennemie.mort()
                    
                if marouxo.rect.colliderect(ennemie.rect) and not marouxo.rect.bottom <= ennemie.rect.centery and ennemie.type_ennemi != "Fin Niveau" and ennemie.est_mort == False:
                    
                    surface.blit(game_over,(0,0))
                    pygame.display.update()
                    pygame.time.wait(2000)

                    running = False
                    return jouer(surface,False,numero_de_la_cinématique,niveau)
                    
            if marouxo.niveau == salle_du_boss and marouxo.ennemies.sprites() == []:
                surface.blit(background_fin,(0,0))
                tmp += 1
                if tmp == 1000:
                    running = False
                    return acceuil(surface)
               
            marouxo.verifie_platforme = marouxo.est_sur_plateforme()
            marouxo.verifie_mur = marouxo.est_contre_un_mur()
            marouxo.camera()


        if marouxo.en_cinématique == True:
            touche_preser = pygame.key.get_pressed()

            if touche_preser[pygame.K_ESCAPE]:
                pygame.quit()
                quit()
                
            if marouxo.n_cinématique == 1 and marouxo.n_scène_cinématique >= 18:
                return jouer(surface,False,2,niveau1)
            
            if marouxo.n_cinématique == 2 and marouxo.n_scène_cinématique >= 13:
                return jouer(surface,False,3,niveau2)
            
            if marouxo.n_cinématique == 3 and marouxo.n_scène_cinématique >= 11:
                return jouer(surface,False,4,salle_du_boss)

            marouxo.cinématique()
            pygame.time.wait(500)

        pygame.display.update()



def main():
   pygame.init()
   pygame.display.set_caption("Marouxo")
   surface=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
   return acceuil(surface)

main()