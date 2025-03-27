import pygame
from variable import *


class Marouxo(pygame.sprite.Sprite):

    def __init__(self,niveau):
        super().__init__()
        self.niveau = niveau
        self.image = m_immobile_droite
        self.rect = self.image.get_rect()
        self.rect.x = int(2*surface.get_width()/11.67)
        self.rect.y = int(4*surface.get_height()/5.5)
        self.direction = "Droite"
        self.vitesse = 3
        self.vitesse_saut = 50
        self.hauter_saut = 15.5 # Niveau 1 et 3 : 15.5 et Niveau 2 : 50.5
        self.vu_x = 0  # Normal : -5
        self.vu_y = -5  # Niveau 1 et 3 : 0 et Niveau 2 : 1080
        self.plateformes = None
        self.murs = None
        self.ennemies = None
        self.n_scène_cinématique = 0
        self.n_cinématique = 1
        self.compteur_pour_saut = 0
        self.limite_saute = False
        self.verifie_en_saut = False
        self.verifie_platforme = True
        self.verifie_mur = False
        self.en_cinématique = True
        self.boss_mort = False

    def déplacement_gauche(self):
        if self.rect.x >= -int(surface.get_width() / 100) and (self.verifie_mur == False or (self.verifie_mur == True and self.direction == "Droite")):
            if self.verifie_en_saut == False:
                self.image = m_mouvement_gauche
            else:
                self.image = m_saute_gauche
            self.direction = "Gauche"
            self.rect.x -= self.vitesse

    def déplacement_droite(self):
        if self.rect.x <= int(surface.get_width() / 1.05) and (self.verifie_mur == False or (self.verifie_mur == True and self.direction == "Gauche")):
            if self.verifie_en_saut == False:
                self.image = m_mouvement_droite
            else:
                self.image = m_saute_droite
            self.direction = "Droite"
            self.rect.x += self.vitesse


    def camera(self):
        if self.niveau == niveau2:
            if self.rect.bottom >= int(surface.get_width() / 2.1) and self.vu_y <= 1078: #caméra vers le bas
                self.rect.y -= abs(self.vitesse)
                
                for ennemie in self.ennemies:
                        ennemie.rect.y -= abs(self.vitesse)

                for plateforme in self.plateformes:
                    plateforme.rect.y -= abs(self.vitesse)

                for mur in self.murs:
                    mur.rect.y -= abs(self.vitesse)

                self.vu_y += abs(self.vitesse)

            if self.rect.top <= int(surface.get_width() / 16) and self.vu_y >= 0: #caméra vers le haut
                self.rect.y += abs(self.vitesse)
                
                for ennemie in self.ennemies:
                        ennemie.rect.y += abs(self.vitesse)

                for plateforme in self.plateformes:
                    plateforme.rect.y += abs(self.vitesse)

                for mur in self.murs:
                    mur.rect.y += abs(self.vitesse)

                self.vu_y -= abs(self.vitesse)

                self.compteur_pour_saut += 1

        if self.niveau == niveau1:
            if self.rect.right >= int(surface.get_width() / 1.5) and self.vu_x <= 3815: #caméra vers la droite
                if self.verifie_mur == False:
                    self.rect.x -= abs(self.vitesse)

                    for ennemie in self.ennemies:
                        ennemie.rect.x -= abs(self.vitesse)
                        if ennemie.type_ennemi == "Panda":
                            ennemie.limite_gauche -= abs(self.vitesse)
                            ennemie.limite_droit -= abs(self.vitesse)
                            

                    for plateforme in self.plateformes:
                        plateforme.rect.x -= abs(self.vitesse)

                    for mur in self.murs:
                        mur.rect.x -= abs(self.vitesse)

                    self.vu_x += abs(self.vitesse)

            if self.rect.left <= int(surface.get_width() / 16) and self.vu_x >= 0: #caméra vers la gauche
                if self.verifie_mur == False:
                    self.rect.x += abs(self.vitesse)

                    for ennemie in self.ennemies:
                        ennemie.rect.x += abs(self.vitesse)
                        if ennemie.type_ennemi == "Panda":
                            ennemie.limite_gauche += abs(self.vitesse)
                            ennemie.limite_droit += abs(self.vitesse)

                    for plateforme in self.plateformes:
                        plateforme.rect.x += abs(self.vitesse)

                    for mur in self.murs:
                        mur.rect.x += abs(self.vitesse)

                    self.vu_x -= abs(self.vitesse)



    def ajouter_plateforme(self):
        self.plateformes = definir_les_plateformes(self)[0]

    def ajouter_mur(self):
        self.murs = definir_les_plateformes(self)[1]

    def ajouter_ennemie(self):
        self.ennemies = definir_les_ennemie(self)


    def est_sur_plateforme(self):
        for plateforme in self.plateformes:
            if self.rect.colliderect(plateforme.rect) and self.rect.bottom <= plateforme.rect.centery:
                return True
        return False

    def est_contre_un_mur(self):
        for mur in self.murs:
            if self.rect.colliderect(mur.rect):
                return True
        return False

    def est_sous_un_mur(self):
        for mur in self.murs:
            if self.rect.colliderect(mur.rect) and self.rect.top >= mur.rect.centery:
                return True
        return False

    def déplacement_saute(self):
        if self.verifie_platforme == True:
            self.image = m_saute_droite if self.direction == "Droite" else m_saute_gauche
            self.rect.y -= int(self.vitesse/1.5)
            self.verifie_en_saut = True

    def saut(self):
        if self.rect.y <= self.vitesse_saut-int(4*self.niveau.get_height()/ self.hauter_saut) or self.est_sous_un_mur() == True or self.compteur_pour_saut > int(self.hauter_saut/2):
                self.limite_saute = True

        if self.limite_saute == True:
            self.image = m_saute_droite if self.direction == "Droite" else m_saute_gauche
            if self.verifie_platforme == True:
                self.verifie_en_saut = False
                self.compteur_pour_saut = 0
                self.limite_saute = False
            else:
                self.rect.y += int(self.vitesse/1.01)

        if self.limite_saute == False:
            self.image = m_saute_droite if self.direction == "Droite" else m_saute_gauche
            self.rect.y -= int(self.vitesse/1.01)

    def cinématique(self):
        if self.n_cinématique == 1:

            self.n_scène_cinématique += 1
            surface.blit(background_jeu,(0,0))
            surface.blit(ligne, (0, int(4*surface.get_height()/20)))

            if  self.n_scène_cinématique == 1:
                surface.blit(m_immobile_droite_cinématique, (int(2*surface.get_width()/21), int(4*surface.get_height()/6.5)))
                surface.blit(panda_roux_happy_gauche, (int(2*surface.get_width()/6), int(4*surface.get_height()/6.5)))

            elif  self.n_scène_cinématique == 2:
                surface.blit(m_immobile_gauche_cinématique, (int(2*surface.get_width()/21), int(4*surface.get_height()/6.5)))
                surface.blit(panda_roux_happy_droite, (int(2*surface.get_width()/6), int(4*surface.get_height()/6.5)))

            elif  self.n_scène_cinématique == 3:
                surface.blit(m_immobile_droite_cinématique, (int(2*surface.get_width()/21), int(4*surface.get_height()/6.5)))
                surface.blit(panda_roux_happy_gauche, (int(2*surface.get_width()/6), int(4*surface.get_height()/6.5)))

            elif  self.n_scène_cinématique == 4:
                surface.blit(m_immobile_gauche_cinématique, (int(2*surface.get_width()/21), int(4*surface.get_height()/6.5)))
                surface.blit(panda_roux_happy_droite, (int(2*surface.get_width()/6), int(4*surface.get_height()/6.5)))

            elif  self.n_scène_cinématique == 5:
                surface.blit(m_immobile_droite_cinématique, (int(2*surface.get_width()/21), int(4*surface.get_height()/6.5)))
                surface.blit(panda_roux_happy_gauche, (int(2*surface.get_width()/6), int(4*surface.get_height()/6.5)))

            elif  self.n_scène_cinématique == 6:
                surface.blit(m_immobile_gauche_cinématique, (int(2*surface.get_width()/21), int(4*surface.get_height()/6.5)))
                surface.blit(panda_roux_happy_droite, (int(2*surface.get_width()/6), int(4*surface.get_height()/6.5)))

            elif  self.n_scène_cinématique == 7:
                surface.blit(m_immobile_droite_cinématique, (int(2*surface.get_width()/21), int(4*surface.get_height()/6.5)))
                surface.blit(panda_roux_happy_gauche, (int(2*surface.get_width()/6), int(4*surface.get_height()/6.5)))
                surface.blit(gorilla_gauche, (int(2*surface.get_width()/2), int(4*surface.get_height()/9)))

            elif  self.n_scène_cinématique == 8:
                surface.blit(m_immobile_droite_cinématique, (int(2*surface.get_width()/21), int(4*surface.get_height()/6.5)))
                surface.blit(panda_roux_happy_gauche, (int(2*surface.get_width()/6), int(4*surface.get_height()/6.5)))
                surface.blit(gorilla_gauche, (int(2*surface.get_width()/2.5), int(4*surface.get_height()/9)))

            elif  self.n_scène_cinématique == 9:
                surface.blit(m_immobile_droite_cinématique, (int(2*surface.get_width()/21), int(4*surface.get_height()/6.5)))
                surface.blit(panda_roux_happy_gauche, (int(2*surface.get_width()/6), int(4*surface.get_height()/6.5)))
                surface.blit(gorilla_gauche, (int(2*surface.get_width()/3), int(4*surface.get_height()/9)))

            elif  self.n_scène_cinématique == 10:
                surface.blit(m_immobile_droite_cinématique, (int(2*surface.get_width()/21), int(4*surface.get_height()/6.5)))
                surface.blit(panda_roux_happy_gauche, (int(2*surface.get_width()/6), int(4*surface.get_height()/6.5)))
                surface.blit(gorilla_gauche, (int(2*surface.get_width()/4), int(4*surface.get_height()/9)))

            elif  self.n_scène_cinématique == 11:
                surface.blit(m_immobile_droite_cinématique, (int(2*surface.get_width()/21), int(4*surface.get_height()/6.5)))
                surface.blit(panda_roux_happy_gauche, (int(2*surface.get_width()/6), int(4*surface.get_height()/6.5)))
                surface.blit(gorilla_gauche, (int(2*surface.get_width()/5), int(4*surface.get_height()/9)))

            elif  self.n_scène_cinématique == 12:
                surface.blit(m_immobile_droite_cinématique, (int(2*surface.get_width()/21), int(4*surface.get_height()/6.5)))
                surface.blit(panda_roux_happy_gauche, (int(2*surface.get_width()/6), int(4*surface.get_height()/6.5)))
                surface.blit(gorilla_gauche, (int(2*surface.get_width()/5), int(4*surface.get_height()/9)))

            elif  self.n_scène_cinématique == 13:
                surface.blit(m_immobile_droite_cinématique, (int(2*surface.get_width()/21), int(4*surface.get_height()/6.5)))
                surface.blit(panda_roux_sad_gauche, (int(2*surface.get_width()/6), int(4*surface.get_height()/6.5)))
                surface.blit(gorilla_gauche, (int(2*surface.get_width()/5), int(4*surface.get_height()/9)))

            elif  self.n_scène_cinématique == 14:
                surface.blit(m_immobile_droite_cinématique, (int(2*surface.get_width()/21), int(4*surface.get_height()/6.5)))
                surface.blit(panda_roux_sad_gauche, (int(2*surface.get_width()/5), int(4*surface.get_height()/6.5)))
                surface.blit(gorilla_gauche, (int(2*surface.get_width()/4.5), int(4*surface.get_height()/9)))

            elif  self.n_scène_cinématique == 15:
                surface.blit(m_immobile_droite_cinématique, (int(2*surface.get_width()/21), int(4*surface.get_height()/6.5)))
                surface.blit(panda_roux_sad_gauche, (int(2*surface.get_width()/4.1), int(4*surface.get_height()/6.5)))
                surface.blit(gorilla_gauche, (int(2*surface.get_width()/4), int(4*surface.get_height()/9)))

            elif  self.n_scène_cinématique == 16:
                surface.blit(m_immobile_droite_cinématique, (int(2*surface.get_width()/21), int(4*surface.get_height()/6.5)))
                surface.blit(panda_roux_sad_gauche, (int(2*surface.get_width()/2.7), int(4*surface.get_height()/6.5)))
                surface.blit(gorilla_gauche, (int(2*surface.get_width()/2.5), int(4*surface.get_height()/9)))

            elif  self.n_scène_cinématique == 17:
                surface.blit(m_immobile_droite_cinématique, (int(2*surface.get_width()/21), int(4*surface.get_height()/6.5)))
                surface.blit(panda_roux_sad_gauche, (int(2*surface.get_width()/1.3), int(4*surface.get_height()/6.5)))
                surface.blit(gorilla_gauche, (int(2*surface.get_width()/1.1), int(4*surface.get_height()/9)))

            elif  self.n_scène_cinématique == 18:
                surface.blit(m_immobile_droite_cinématique, (int(2*surface.get_width()/21), int(4*surface.get_height()/6.5)))

        
        if self.n_cinématique == 2:
            
            self.n_scène_cinématique += 1
            surface.blit(background_jeu,(0,0))
            surface.blit(self.niveau,(0, int(4*surface.get_height()/20)), (self.vu_x, self.vu_y, surface.get_width(), surface.get_height()))
            
            if  self.n_scène_cinématique == 1:
                surface.blit(pygame.transform.scale(lianes, (int(surface.get_width()/32),int(surface.get_height()/12.4))),(int(2*surface.get_width()/ 2.8),int(4*surface.get_height()/ 8000.7)))
                surface.blit(m_immobile_gauche, (int(2*surface.get_width()/2.8), int(4*surface.get_height()/12.3)))
                
            elif  self.n_scène_cinématique == 2:
                surface.blit(pygame.transform.scale(lianes, (int(surface.get_width()/32),int(surface.get_height()/10.4))),(int(2*surface.get_width()/ 2.8),int(4*surface.get_height()/ 8000.7)))
                surface.blit(m_immobile_gauche, (int(2*surface.get_width()/2.8), int(4*surface.get_height()/12.3)))
                
            elif  self.n_scène_cinématique == 3:
                surface.blit(pygame.transform.scale(lianes, (int(surface.get_width()/32),int(surface.get_height()/8.4))),(int(2*surface.get_width()/ 2.8),int(4*surface.get_height()/ 8000.7)))
                surface.blit(m_immobile_gauche, (int(2*surface.get_width()/2.8), int(4*surface.get_height()/12.3)))
                
            elif  self.n_scène_cinématique == 4:
                surface.blit(pygame.transform.scale(lianes, (int(surface.get_width()/32),int(surface.get_height()/6.4))),(int(2*surface.get_width()/ 2.8),int(4*surface.get_height()/ 8000.7)))
                surface.blit(m_immobile_gauche, (int(2*surface.get_width()/2.8), int(4*surface.get_height()/12.3)))
                
            elif  self.n_scène_cinématique == 5:
                surface.blit(pygame.transform.scale(lianes, (int(surface.get_width()/32),int(surface.get_height()/4.4))),(int(2*surface.get_width()/ 2.8),int(4*surface.get_height()/ 8000.7)))
                surface.blit(m_immobile_gauche, (int(2*surface.get_width()/2.8), int(4*surface.get_height()/12.3)))
                
            elif  self.n_scène_cinématique == 6:
                surface.blit(liane_fixe,(int(2*surface.get_width()/ 2.8),int(4*surface.get_height()/ 8000.7)))
                surface.blit(m_immobile_gauche, (int(2*surface.get_width()/2.8), int(4*surface.get_height()/12.3)))
                
            elif  self.n_scène_cinématique == 7:
                surface.blit(liane_fixe,(int(2*surface.get_width()/ 2.8),int(4*surface.get_height()/ 8000.7)))
                surface.blit(m_immobile_droite, (int(2*surface.get_width()/2.8), int(4*surface.get_height()/12.3)))
                
            elif  self.n_scène_cinématique == 8:
                surface.blit(liane_fixe,(int(2*surface.get_width()/ 2.8),int(4*surface.get_height()/ 8000.7)))
                surface.blit(m_immobile_droite, (int(2*surface.get_width()/2.8), int(4*surface.get_height()/15.3)))
                
            elif  self.n_scène_cinématique == 9:
                surface.blit(liane_fixe,(int(2*surface.get_width()/ 2.8),int(4*surface.get_height()/ 8000.7)))
                surface.blit(m_immobile_droite, (int(2*surface.get_width()/2.8), int(4*surface.get_height()/20.3)))
                
            elif  self.n_scène_cinématique == 10:
                surface.blit(liane_fixe,(int(2*surface.get_width()/ 2.8),int(4*surface.get_height()/ 8000.7)))
                surface.blit(m_immobile_droite, (int(2*surface.get_width()/2.8), int(4*surface.get_height()/30.3)))
                
            elif  self.n_scène_cinématique == 11:
                surface.blit(liane_fixe,(int(2*surface.get_width()/ 2.8),int(4*surface.get_height()/ 8000.7)))
                surface.blit(m_immobile_droite, (int(2*surface.get_width()/2.8), int(4*surface.get_height()/50.3)))
                
            elif  self.n_scène_cinématique == 12:
                surface.blit(liane_fixe,(int(2*surface.get_width()/ 2.8),int(4*surface.get_height()/ 8000.7)))
                surface.blit(m_immobile_droite, (int(2*surface.get_width()/2.8), int(4*surface.get_height()/5000.3)))
                
            elif  self.n_scène_cinématique == 13:
                surface.blit(liane_fixe,(int(2*surface.get_width()/ 2.8),int(4*surface.get_height()/ 8000.7)))
                surface.blit(m_immobile_droite, (int(2*surface.get_width()/2.8), int(4*surface.get_height()/5000.3)))

        if self.n_cinématique == 3:
            
            self.n_scène_cinématique += 1
            surface.blit(background_jeu,(0,0))
            surface.blit(self.niveau,(0, 0), (self.vu_x, self.vu_y, surface.get_width(), surface.get_height()))
            
            if  self.n_scène_cinématique == 1:
                surface.blit(m_immobile_droite, (int(2*surface.get_width()/2.3), int(4*surface.get_height()/500.3)))
                
            elif  self.n_scène_cinématique == 2:
                surface.blit(m_immobile_droite, (int(2*surface.get_width()/2.3), int(4*surface.get_height()/500.3)))
                
            elif  self.n_scène_cinématique == 3:
                surface.blit(m_mouvement_droite, (int(2*surface.get_width()/2.29), int(4*surface.get_height()/500.3)))
                
            elif  self.n_scène_cinématique == 4:
                surface.blit(m_mouvement_droite, (int(2*surface.get_width()/2.25), int(4*surface.get_height()/500.3)))
                
            elif  self.n_scène_cinématique == 5:
                surface.blit(m_mouvement_droite, (int(2*surface.get_width()/2.225), int(4*surface.get_height()/500.3)))
                
            elif  self.n_scène_cinématique == 6:
                surface.blit(m_mouvement_droite, (int(2*surface.get_width()/2.2), int(4*surface.get_height()/500.3)))
                
            elif  self.n_scène_cinématique == 7:
                surface.blit(m_mouvement_droite, (int(2*surface.get_width()/2.18), int(4*surface.get_height()/500.3)))
                
            elif  self.n_scène_cinématique == 8:
                surface.blit(m_mouvement_droite, (int(2*surface.get_width()/2.14), int(4*surface.get_height()/500.3)))
                
            elif  self.n_scène_cinématique == 9:
                surface.blit(m_mouvement_droite, (int(2*surface.get_width()/2.1), int(4*surface.get_height()/500.3)))
                
            elif  self.n_scène_cinématique == 10:
                surface.blit(m_saute_droite, (int(2*surface.get_width()/2.08), int(4*surface.get_height()/5000.3)))
                
            elif  self.n_scène_cinématique == 11:
                surface.blit(m_saute_droite, (int(2*surface.get_width()/2.01), int(4*surface.get_height()/5000.3)))
            
        
        
            
            




class Platforme(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


def definir_les_plateformes(marouxo):
    if marouxo.niveau == niveau1:
        
        platformes= pygame.sprite.Group()

        platformes.add( (Platforme(int(2*marouxo.niveau.get_width()/8000), int(4*marouxo.niveau.get_height()/ (4.85 / 1.31)), int(2*marouxo.niveau.get_width()/10.16), marouxo.niveau.get_height()/55)),
                        (Platforme(int(2*marouxo.niveau.get_width()/8.67), int(4*marouxo.niveau.get_height()/ (4.85 / 1.31)), int(2*marouxo.niveau.get_width()/7.38), marouxo.niveau.get_height()/55)),
                        (Platforme(int(2*marouxo.niveau.get_width()/2.799), int(4*marouxo.niveau.get_height()/ (4.85 / 1.31)), int(2*marouxo.niveau.get_width()/180), marouxo.niveau.get_height()/55)),
                        (Platforme(int(2*marouxo.niveau.get_width()/3.782), int(4*marouxo.niveau.get_height()/ (4.85 / 1.31)), int(2*marouxo.niveau.get_width()/150), marouxo.niveau.get_height()/55)),
                        (Platforme(int(2*marouxo.niveau.get_width()/3.562), int(4*marouxo.niveau.get_height()/ (4.85 / 1.31)), int(2*marouxo.niveau.get_width()/23), marouxo.niveau.get_height()/55)),
                        (Platforme(int(2*marouxo.niveau.get_width()/2.702), int(4*marouxo.niveau.get_height()/ (4.85 / 1.31)), int(2*marouxo.niveau.get_width()/31), marouxo.niveau.get_height()/55)),
                        (Platforme(int(2*marouxo.niveau.get_width()/2.275), int(4*marouxo.niveau.get_height()/ (4.85 / 1.31)), int(2*marouxo.niveau.get_width()/15), marouxo.niveau.get_height()/55)),
                        (Platforme(int(2*marouxo.niveau.get_width()/16.92), int(4*marouxo.niveau.get_height()/ (7.6 / 1.48)), int(2*marouxo.niveau.get_width()/125), marouxo.niveau.get_height()/55)),
                        (Platforme(int(2*marouxo.niveau.get_width()/13.02), int(4*marouxo.niveau.get_height()/ (6.425 / 1.41)), int(2*marouxo.niveau.get_width()/72.5), marouxo.niveau.get_height()/55)),
                        (Platforme(int(2*marouxo.niveau.get_width()/9.23), int(4*marouxo.niveau.get_height()/ (4.325 / 1.28)), int(2*marouxo.niveau.get_width()/125), marouxo.niveau.get_height()/55)),
                        (Platforme(int(2*marouxo.niveau.get_width()/8.25), int(4*marouxo.niveau.get_height()/ (6.425 / 1.41)), int(2*marouxo.niveau.get_width()/33), marouxo.niveau.get_height()/55)),
                        (Platforme(int(2*marouxo.niveau.get_width()/8.25), int(4*marouxo.niveau.get_height()/ (9.425 / 1.59)), int(2*marouxo.niveau.get_width()/47.8), marouxo.niveau.get_height()/55)),
                        (Platforme(int(2*marouxo.niveau.get_width()/8.25), int(4*marouxo.niveau.get_height()/ (17.5 / 2.1)), int(2*marouxo.niveau.get_width()/78), marouxo.niveau.get_height()/55)),
                        (Platforme(int(2*marouxo.niveau.get_width()/10.12), int(4*marouxo.niveau.get_height()/ (24.5 / 2.55)), int(2*marouxo.niveau.get_width()/78), marouxo.niveau.get_height()/55)),
                        (Platforme(int(2*marouxo.niveau.get_width()/5.50), int(4*marouxo.niveau.get_height()/ (6.3 / 1.41)), int(2*marouxo.niveau.get_width()/78), marouxo.niveau.get_height()/55)),
                        (Platforme(int(2*marouxo.niveau.get_width()/5.73), int(4*marouxo.niveau.get_height()/ (11.2 / 1.72)), int(2*marouxo.niveau.get_width()/102), marouxo.niveau.get_height()/55)),
                        (Platforme(int(2*marouxo.niveau.get_width()/5.135), int(4*marouxo.niveau.get_height()/ (19.9 / 2.25)), int(2*marouxo.niveau.get_width()/36.7), marouxo.niveau.get_height()/55)),
                        (Platforme(int(2*marouxo.niveau.get_width()/2.942), int(4*marouxo.niveau.get_height()/ (15.5 / 2)), int(2*marouxo.niveau.get_width()/110), marouxo.niveau.get_height()/55)),
                        (Platforme(int(2*marouxo.niveau.get_width()/3.095), int(4*marouxo.niveau.get_height()/ (6.4 / 1.41)), int(2*marouxo.niveau.get_width()/103), marouxo.niveau.get_height()/55)),
                        (Platforme(int(2*marouxo.niveau.get_width()/3.283), int(4*marouxo.niveau.get_height()/ (8.7 / 1.54)), int(2*marouxo.niveau.get_width()/140), marouxo.niveau.get_height()/55)),
                        (Platforme(int(2*marouxo.niveau.get_width()/3.347), int(4*marouxo.niveau.get_height()/ (9.9 / 1.62)), int(2*marouxo.niveau.get_width()/170), marouxo.niveau.get_height()/55)),
                        (Platforme(int(2*marouxo.niveau.get_width()/3.458), int(4*marouxo.niveau.get_height()/ (13.8 / 1.84)), int(2*marouxo.niveau.get_width()/110), marouxo.niveau.get_height()/55)),
                        (Platforme(int(2*marouxo.niveau.get_width()/3.087), int(4*marouxo.niveau.get_height()/ (22.8 /2.45)), int(2*marouxo.niveau.get_width()/82), marouxo.niveau.get_height()/55)),
                        (Platforme(int(2*marouxo.niveau.get_width()/3.215), int(4*marouxo.niveau.get_height()/ (44 / 3.8)), int(2*marouxo.niveau.get_width()/77), marouxo.niveau.get_height()/55)),
                        (Platforme(int(2*marouxo.niveau.get_width()/2.492), int(4*marouxo.niveau.get_height()/ (6.37 / 1.41)), int(2*marouxo.niveau.get_width()/166), marouxo.niveau.get_height()/55)),
                        (Platforme(int(2*marouxo.niveau.get_width()/2.455), int(4*marouxo.niveau.get_height()/ (8.2 / 1.49)), int(2*marouxo.niveau.get_width()/146), marouxo.niveau.get_height()/55)),
                        (Platforme(int(2*marouxo.niveau.get_width()/2.22), int(4*marouxo.niveau.get_height()/ (15.4 / 2)), int(2*marouxo.niveau.get_width()/146), marouxo.niveau.get_height()/55)),
                        (Platforme(int(2*marouxo.niveau.get_width()/2.163), int(4*marouxo.niveau.get_height()/ (10.7 / 1.65)), int(2*marouxo.niveau.get_width()/180), marouxo.niveau.get_height()/55)),
                        (Platforme(int(2*marouxo.niveau.get_width()/2.1215), int(4*marouxo.niveau.get_height()/ (7 / 1.44)), int(2*marouxo.niveau.get_width()/180), marouxo.niveau.get_height()/55)))

        murs = pygame.sprite.Group()

        murs.add(   (Platforme(int(2*marouxo.niveau.get_width()/8.7), int(4*marouxo.niveau.get_height()/(4.85 / 1.35)), int(2*marouxo.niveau.get_width()/666), marouxo.niveau.get_height()/8)),
                    (Platforme(int(2*marouxo.niveau.get_width()/3.095), int(4*marouxo.niveau.get_height()/(6.4 / 1.45)), int(2*marouxo.niveau.get_width()/666), marouxo.niveau.get_height()/5)),
                    (Platforme(int(2*marouxo.niveau.get_width()/5.13), int(4*marouxo.niveau.get_height()/(19.9 / 2.40)), int(2*marouxo.niveau.get_width()/666), marouxo.niveau.get_height()/2.3)),
                    (Platforme(int(2*marouxo.niveau.get_width()/3.1), int(4*marouxo.niveau.get_height()/(44 / 4)), int(2*marouxo.niveau.get_width()/666), marouxo.niveau.get_height()/10)),
                    (Platforme(int(2*marouxo.niveau.get_width()/3.37), int(4*marouxo.niveau.get_height()/(13.8 / 1.88)), int(2*marouxo.niveau.get_width()/666), marouxo.niveau.get_height()/8)),
                    (Platforme(int(2*marouxo.niveau.get_width()/3.3), int(4*marouxo.niveau.get_height()/(9.9 / 1.67)), int(2*marouxo.niveau.get_width()/666), marouxo.niveau.get_height()/16)),
                    (Platforme(int(2*marouxo.niveau.get_width()/2.492), int(4*marouxo.niveau.get_height()/(6.37 / 1.45)), int(2*marouxo.niveau.get_width()/666), marouxo.niveau.get_height()/5)),
                    (Platforme(int(2*marouxo.niveau.get_width()/2.455), int(4*marouxo.niveau.get_height()/(8.2 / 1.55)), int(2*marouxo.niveau.get_width()/666), marouxo.niveau.get_height()/7)))

    if marouxo.niveau == niveau2:
        
        platformes= pygame.sprite.Group()

        platformes.add( (Platforme(int(2*marouxo.niveau.get_width()/2.3), int(4*marouxo.niveau.get_height()/-11.2), int(2*marouxo.niveau.get_width()/10), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/2.34), int(4*marouxo.niveau.get_height()/-11.56), int(2*marouxo.niveau.get_width()/10), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/2.3), int(4*marouxo.niveau.get_height()/-12), int(2*marouxo.niveau.get_width()/10), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/2.55), int(4*marouxo.niveau.get_height()/-8.76), int(2*marouxo.niveau.get_width()/8), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/2.6), int(4*marouxo.niveau.get_height()/-8.96), int(2*marouxo.niveau.get_width()/8), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/2.55), int(4*marouxo.niveau.get_height()/-9.15), int(2*marouxo.niveau.get_width()/8), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/3.05), int(4*marouxo.niveau.get_height()/-9.56), int(2*marouxo.niveau.get_width()/13), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/3.15), int(4*marouxo.niveau.get_height()/-9.8), int(2*marouxo.niveau.get_width()/10), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/3.05), int(4*marouxo.niveau.get_height()/-10.1), int(2*marouxo.niveau.get_width()/13), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/3.3), int(4*marouxo.niveau.get_height()/-12.2), int(2*marouxo.niveau.get_width()/13), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/3.43), int(4*marouxo.niveau.get_height()/-12.56), int(2*marouxo.niveau.get_width()/10), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/3.3), int(4*marouxo.niveau.get_height()/-13), int(2*marouxo.niveau.get_width()/13), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/11), int(4*marouxo.niveau.get_height()/-12.56), int(2*marouxo.niveau.get_width()/8.3), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/11.97), int(4*marouxo.niveau.get_height()/-13), int(2*marouxo.niveau.get_width()/7.3), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/11), int(4*marouxo.niveau.get_height()/-13.56), int(2*marouxo.niveau.get_width()/8.3), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/58.53), int(4*marouxo.niveau.get_height()/-17.86), int(2*marouxo.niveau.get_width()/11.8), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/58.97), int(4*marouxo.niveau.get_height()/-18.56), int(2*marouxo.niveau.get_width()/10.5), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/58.53), int(4*marouxo.niveau.get_height()/-19.36), int(2*marouxo.niveau.get_width()/11.8), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/58.53), int(4*marouxo.niveau.get_height()/-41.56), int(2*marouxo.niveau.get_width()/15.5), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/58.97), int(4*marouxo.niveau.get_height()/-46.56), int(2*marouxo.niveau.get_width()/13.5), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/58.53), int(4*marouxo.niveau.get_height()/-53.86), int(2*marouxo.niveau.get_width()/15.5), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/6.53), int(4*marouxo.niveau.get_height()/-32.26), int(2*marouxo.niveau.get_width()/16.5), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/6.97), int(4*marouxo.niveau.get_height()/-34.56), int(2*marouxo.niveau.get_width()/13), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/6.53), int(4*marouxo.niveau.get_height()/-37.86), int(2*marouxo.niveau.get_width()/16.5), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/5.83), int(4*marouxo.niveau.get_height()/-21.56), int(2*marouxo.niveau.get_width()/12.5), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/6.17), int(4*marouxo.niveau.get_height()/-22.56), int(2*marouxo.niveau.get_width()/10), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/5.83), int(4*marouxo.niveau.get_height()/-23.86), int(2*marouxo.niveau.get_width()/12.5), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/2.77), int(4*marouxo.niveau.get_height()/-22.56), int(2*marouxo.niveau.get_width()/16.55), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/2.83), int(4*marouxo.niveau.get_height()/-21.56), int(2*marouxo.niveau.get_width()/13), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/2.77), int(4*marouxo.niveau.get_height()/-20.56), int(2*marouxo.niveau.get_width()/16.55), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/9.81), int(4*marouxo.niveau.get_height()/-88.56), int(2*marouxo.niveau.get_width()/20.55), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/10.83), int(4*marouxo.niveau.get_height()/-73.56), int(2*marouxo.niveau.get_width()/15), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/9.81), int(4*marouxo.niveau.get_height()/-60.56), int(2*marouxo.niveau.get_width()/20.55), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/2.77), int(4*marouxo.niveau.get_height()/-113.56), int(2*marouxo.niveau.get_width()/25.55), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/2.83), int(4*marouxo.niveau.get_height()/-163.56), int(2*marouxo.niveau.get_width()/17), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/2.77), int(4*marouxo.niveau.get_height()/-263.56), int(2*marouxo.niveau.get_width()/25.55), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/3.61), int(4*marouxo.niveau.get_height()/-88.56), int(2*marouxo.niveau.get_width()/20.55), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/3.73), int(4*marouxo.niveau.get_height()/-73.56), int(2*marouxo.niveau.get_width()/14), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/3.61), int(4*marouxo.niveau.get_height()/-60.56), int(2*marouxo.niveau.get_width()/20.55), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/2.31), int(4*marouxo.niveau.get_height()/-46.56), int(2*marouxo.niveau.get_width()/20.55), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/2.37), int(4*marouxo.niveau.get_height()/-53.56), int(2*marouxo.niveau.get_width()/14), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/2.31), int(4*marouxo.niveau.get_height()/-60.56), int(2*marouxo.niveau.get_width()/20.55), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/7.6), int(4*marouxo.niveau.get_height()/-700.56), int(2*marouxo.niveau.get_width()/12.55), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/8.3), int(4*marouxo.niveau.get_height()/700.89), int(2*marouxo.niveau.get_width()/9.8), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/7.6), int(4*marouxo.niveau.get_height()/250.09), int(2*marouxo.niveau.get_width()/12.55), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/3.97), int(4*marouxo.niveau.get_height()/113.56), int(2*marouxo.niveau.get_width()/12.55), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/4.13), int(4*marouxo.niveau.get_height()/88.56), int(2*marouxo.niveau.get_width()/10), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/3.97), int(4*marouxo.niveau.get_height()/70.56), int(2*marouxo.niveau.get_width()/12.55), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/2.76), int(4*marouxo.niveau.get_height()/52.56), int(2*marouxo.niveau.get_width()/12.55), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/2.84), int(4*marouxo.niveau.get_height()/46.56), int(2*marouxo.niveau.get_width()/10), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/2.76), int(4*marouxo.niveau.get_height()/42.36), int(2*marouxo.niveau.get_width()/12.55), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/3.823), int(4*marouxo.niveau.get_height()/34.56), int(2*marouxo.niveau.get_width()/12.55), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/4), int(4*marouxo.niveau.get_height()/31.56), int(2*marouxo.niveau.get_width()/10), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/3.823), int(4*marouxo.niveau.get_height()/29.56), int(2*marouxo.niveau.get_width()/12.55), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/7), int(4*marouxo.niveau.get_height()/31.56), int(2*marouxo.niveau.get_width()/12.55), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/7.6), int(4*marouxo.niveau.get_height()/29.56), int(2*marouxo.niveau.get_width()/10), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/7), int(4*marouxo.niveau.get_height()/27.56), int(2*marouxo.niveau.get_width()/12.55), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/10.8), int(4*marouxo.niveau.get_height()/24.16), int(2*marouxo.niveau.get_width()/12.55), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/12.2), int(4*marouxo.niveau.get_height()/22.76), int(2*marouxo.niveau.get_width()/10), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/10.8), int(4*marouxo.niveau.get_height()/21.56), int(2*marouxo.niveau.get_width()/12.55), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/4.723), int(4*marouxo.niveau.get_height()/20.56), int(2*marouxo.niveau.get_width()/12.55), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/4.95), int(4*marouxo.niveau.get_height()/19.56), int(2*marouxo.niveau.get_width()/10), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/4.723), int(4*marouxo.niveau.get_height()/18.56), int(2*marouxo.niveau.get_width()/12.55), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/3.423), int(4*marouxo.niveau.get_height()/18.56), int(2*marouxo.niveau.get_width()/12.55), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/3.55), int(4*marouxo.niveau.get_height()/17.66), int(2*marouxo.niveau.get_width()/9.8), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/3.423), int(4*marouxo.niveau.get_height()/16.89), int(2*marouxo.niveau.get_width()/12.55), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/7.6), int(4*marouxo.niveau.get_height()/17.56), int(2*marouxo.niveau.get_width()/12.55), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/8.3), int(4*marouxo.niveau.get_height()/16.89), int(2*marouxo.niveau.get_width()/9.8), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/7.6), int(4*marouxo.niveau.get_height()/16.09), int(2*marouxo.niveau.get_width()/12.55), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/4.7), int(4*marouxo.niveau.get_height()/13.56), int(2*marouxo.niveau.get_width()/14.55), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/4.97), int(4*marouxo.niveau.get_height()/13.09), int(2*marouxo.niveau.get_width()/10.8), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/4.7), int(4*marouxo.niveau.get_height()/12.71), int(2*marouxo.niveau.get_width()/14.55), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/3.55), int(4*marouxo.niveau.get_height()/12.71), int(2*marouxo.niveau.get_width()/12.75), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/3.67), int(4*marouxo.niveau.get_height()/12.26), int(2*marouxo.niveau.get_width()/10), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/3.55), int(4*marouxo.niveau.get_height()/11.9), int(2*marouxo.niveau.get_width()/12.75), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/5.48), int(4*marouxo.niveau.get_height()/12.26), int(2*marouxo.niveau.get_width()/14.55), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/5.86), int(4*marouxo.niveau.get_height()/11.9), int(2*marouxo.niveau.get_width()/10.8), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/5.48), int(4*marouxo.niveau.get_height()/11.56), int(2*marouxo.niveau.get_width()/14.55), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/3.98), int(4*marouxo.niveau.get_height()/11.56), int(2*marouxo.niveau.get_width()/12.45), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/4.16), int(4*marouxo.niveau.get_height()/11.25), int(2*marouxo.niveau.get_width()/10.2), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/3.98), int(4*marouxo.niveau.get_height()/10.9), int(2*marouxo.niveau.get_width()/12.45), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/17.5), int(4*marouxo.niveau.get_height()/10.9), int(2*marouxo.niveau.get_width()/20.5), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/24), int(4*marouxo.niveau.get_height()/10.63), int(2*marouxo.niveau.get_width()/13.4), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/15.5), int(4*marouxo.niveau.get_height()/10.35), int(2*marouxo.niveau.get_width()/26.5), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/16), int(4*marouxo.niveau.get_height()/9.5), int(2*marouxo.niveau.get_width()/13.5), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/20), int(4*marouxo.niveau.get_height()/9.28), int(2*marouxo.niveau.get_width()/9.8), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/15), int(4*marouxo.niveau.get_height()/12.88), int(2*marouxo.niveau.get_width()/29.8), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/2.93), int(4*marouxo.niveau.get_height()/8.88), int(2*marouxo.niveau.get_width()/9.8), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/2.93), int(4*marouxo.niveau.get_height()/9.28), int(2*marouxo.niveau.get_width()/9.8), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/2.93), int(4*marouxo.niveau.get_height()/9.58), int(2*marouxo.niveau.get_width()/9.8), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/2.5), int(4*marouxo.niveau.get_height()/10.28), int(2*marouxo.niveau.get_width()/29.8), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/2.4), int(4*marouxo.niveau.get_height()/11.68), int(2*marouxo.niveau.get_width()/29.8), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/2.83), int(4*marouxo.niveau.get_height()/15.58), int(2*marouxo.niveau.get_width()/14.8), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/2.93), int(4*marouxo.niveau.get_height()/14.98), int(2*marouxo.niveau.get_width()/9.8), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/2.83), int(4*marouxo.niveau.get_height()/14.48), int(2*marouxo.niveau.get_width()/14.2), marouxo.niveau.get_height()/150)),
                        (Platforme(int(2*marouxo.niveau.get_width()/13), int(4*marouxo.niveau.get_height()/9.05), int(2*marouxo.niveau.get_width()/18.5), marouxo.niveau.get_height()/150)))

        murs = pygame.sprite.Group()
        
        murs.add((Platforme(int(2*marouxo.niveau.get_width()/20), int(4*marouxo.niveau.get_height()/9.38), int(2*marouxo.niveau.get_width()/666), marouxo.niveau.get_height()/5)),
                 (Platforme(int(2*marouxo.niveau.get_width()/22), int(4*marouxo.niveau.get_height()/10), int(2*marouxo.niveau.get_width()/666), marouxo.niveau.get_height()/5)),
                 (Platforme(int(2*marouxo.niveau.get_width()/22), int(4*marouxo.niveau.get_height()/85.8), int(2*marouxo.niveau.get_width()/666), marouxo.niveau.get_height()/3.3)),
                 (Platforme(int(2*marouxo.niveau.get_width()/22), int(4*marouxo.niveau.get_height()/13.8), int(2*marouxo.niveau.get_width()/666), marouxo.niveau.get_height()/13)),
                 (Platforme(int(2*marouxo.niveau.get_width()/20), int(4*marouxo.niveau.get_height()/13.5), int(2*marouxo.niveau.get_width()/666), marouxo.niveau.get_height()/15)),
                 (Platforme(int(2*marouxo.niveau.get_width()/18.25), int(4*marouxo.niveau.get_height()/13.05), int(2*marouxo.niveau.get_width()/666), marouxo.niveau.get_height()/19)),
                 (Platforme(int(2*marouxo.niveau.get_width()/16.5), int(4*marouxo.niveau.get_height()/13.05), int(2*marouxo.niveau.get_width()/666), marouxo.niveau.get_height()/45)),
                 (Platforme(int(2*marouxo.niveau.get_width()/15.25), int(4*marouxo.niveau.get_height()/12.9), int(2*marouxo.niveau.get_width()/666), marouxo.niveau.get_height()/65)),
                 (Platforme(int(2*marouxo.niveau.get_width()/2.165), int(4*marouxo.niveau.get_height()/85.8), int(2*marouxo.niveau.get_width()/666), marouxo.niveau.get_height()/2.2)),
                 (Platforme(int(2*marouxo.niveau.get_width()/2.215), int(4*marouxo.niveau.get_height()/24.8), int(2*marouxo.niveau.get_width()/666), marouxo.niveau.get_height()/3.2)),
                 (Platforme(int(2*marouxo.niveau.get_width()/2.255), int(4*marouxo.niveau.get_height()/15), int(2*marouxo.niveau.get_width()/666), marouxo.niveau.get_height()/8)),
                 (Platforme(int(2*marouxo.niveau.get_width()/2.285), int(4*marouxo.niveau.get_height()/13.8), int(2*marouxo.niveau.get_width()/666), marouxo.niveau.get_height()/28)),
                 (Platforme(int(2*marouxo.niveau.get_width()/2.285), int(4*marouxo.niveau.get_height()/10.9), int(2*marouxo.niveau.get_width()/666), marouxo.niveau.get_height()/58)),
                 (Platforme(int(2*marouxo.niveau.get_width()/58.97), int(4*marouxo.niveau.get_height()/-14.86), int(2*marouxo.niveau.get_width()/666), marouxo.niveau.get_height()/1.3)),
                 (Platforme(int(2*marouxo.niveau.get_width()/25), int(4*marouxo.niveau.get_height()/21.8), int(2*marouxo.niveau.get_width()/666), marouxo.niveau.get_height()/3)))

    if marouxo.niveau == salle_du_boss:

        platformes=[(Platforme(int(2*marouxo.niveau.get_width()/48), int(4*marouxo.niveau.get_height()/4.45), int(2*marouxo.niveau.get_width()/2.15), marouxo.niveau.get_height()/95))]

        murs = []

    return (platformes,murs)

class Ennemie(pygame.sprite.Sprite):
    def __init__(self, x, y, type_ennemi,image_vivent,images_de_mort,limite_gauche,limite_droit):
        super().__init__()
        self.est_mort = False
        self.type_ennemi = type_ennemi
        self.image_vivent = image_vivent
        self.images_de_mort = images_de_mort
        self.rect = self.image_vivent.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.limite_gauche = limite_gauche
        self.limite_droit = limite_droit
        self.vitesse = 2
        self.FPS_mort = 0
        self.FPS_boss = 0


    def déplacement(self):
        if self.type_ennemi == "Boss":
            self.FPS_boss += 0.58
            
            if self.FPS_boss <= 40:
                self.rect.y -= 5
                
            elif 41 <=  self.FPS_boss <= 80:
                self.rect.y += 5

            elif 81 <=  self.FPS_boss <= 120:
                self.rect.x -= 5
                
            elif 121 <=  self.FPS_boss <= 160:
                self.rect.x += 5
                
            elif self.FPS_boss >= 180:
                self.rect.x = int(2*surface.get_width()/2.923)
                self.rect.y = int(4*surface.get_height()/ 8.1)
                self.FPS_boss = 0
                
        if self.type_ennemi == "Panda":
            self.rect.x += self.vitesse

            if self.rect.x < self.limite_gauche or self.rect.x > self.limite_droit:
                self.vitesse *= -1

    def mort(self):
        self.est_mort = True

    def affiche_ennemie(self):
        if not self.est_mort:
            surface.blit(self.image_vivent, self.rect.topleft)
        else:
            self.animation_de_mort()

    def animation_de_mort(self):
        self.FPS_mort += 1
        
        if self.type_ennemi == "Boss":
            if self.FPS_mort <= 80:
                surface.blit(self.images_de_mort[0], self.rect.topleft)
            if 81 <= self.FPS_mort <= 160:
                surface.blit(self.images_de_mort[1], self.rect.topleft)
            if self.FPS_mort == 320:
                self.kill()
                
        else:
            if self.FPS_mort <= 20:
                surface.blit(self.images_de_mort[0], self.rect.topleft)
            if 21 <= self.FPS_mort <= 40:
                surface.blit(self.images_de_mort[1], self.rect.topleft)
            if self.FPS_mort == 41:
                self.kill()


def definir_les_ennemie(marouxo):
    if marouxo.niveau == niveau1:
        
        ennemis_group = pygame.sprite.Group()

        ennemis_group.add((Ennemie(int(2*marouxo.niveau.get_width()/16.57), int(4*marouxo.niveau.get_height()/ 4.1), "Serpent",serpent_rouge_vivent, [serpent_rouge_moitié_vivent,serpent_rouge_mort],None,None)),
                          (Ennemie(int(2*marouxo.niveau.get_width()/12.50), int(4*marouxo.niveau.get_height()/ 5.1), "Serpent",serpent_bleu_vivent, [serpent_bleu_moitié_vivent,serpent_bleu_mort],None,None)),
                          (Ennemie(int(2*marouxo.niveau.get_width()/8.10), int(4*marouxo.niveau.get_height()/ 5.1), "Panda",panda_vivent, [panda_moitié_vivent,panda_mort],int(2*marouxo.niveau.get_width()/8.27),int(2*marouxo.niveau.get_width()/6.87))),
                          (Ennemie(int(2*marouxo.niveau.get_width()/7.80), int(4*marouxo.niveau.get_height()/ 6.9), "Panda",panda_vivent, [panda_moitié_vivent,panda_mort],int(2*marouxo.niveau.get_width()/8.27),int(2*marouxo.niveau.get_width()/7.37))),
                          (Ennemie(int(2*marouxo.niveau.get_width()/8.10), int(4*marouxo.niveau.get_height()/ 10.4), "Panda",panda_vivent, [panda_moitié_vivent,panda_mort],int(2*marouxo.niveau.get_width()/8.27),int(2*marouxo.niveau.get_width()/7.87))),
                          (Ennemie(int(2*marouxo.niveau.get_width()/5.67), int(4*marouxo.niveau.get_height()/ 7.7), "Serpent",serpent_vert_vivent, [serpent_vert_moitié_vivent,serpent_vert_mort],None,None)),
                          (Ennemie(int(2*marouxo.niveau.get_width()/5.75), int(4*marouxo.niveau.get_height()/ 4.1), "Panda",panda_vivent, [panda_moitié_vivent,panda_mort],int(2*marouxo.niveau.get_width()/6.57),int(2*marouxo.niveau.get_width()/5.65))),
                          (Ennemie(int(2*marouxo.niveau.get_width()/4.35), int(4*marouxo.niveau.get_height()/ 4.1), "Panda",panda_vivent, [panda_moitié_vivent,panda_mort],int(2*marouxo.niveau.get_width()/4.5),int(2*marouxo.niveau.get_width()/4.1))),
                          (Ennemie(int(2*marouxo.niveau.get_width()/3.075), int(4*marouxo.niveau.get_height()/ 5.1), "Panda",panda_vivent, [panda_moitié_vivent,panda_mort],int(2*marouxo.niveau.get_width()/3.09),int(2*marouxo.niveau.get_width()/3.05))),
                          (Ennemie(int(2*marouxo.niveau.get_width()/2.93), int(4*marouxo.niveau.get_height()/ 9.5), "Serpent",serpent_rouge_vivent, [serpent_rouge_moitié_vivent,serpent_rouge_mort],None,None)),
                          (Ennemie(int(2*marouxo.niveau.get_width()/2.65), int(4*marouxo.niveau.get_height()/ 4.1), "Panda",panda_vivent, [panda_moitié_vivent,panda_mort],int(2*marouxo.niveau.get_width()/2.71),int(2*marouxo.niveau.get_width()/2.55))),
                          (Ennemie(int(2*marouxo.niveau.get_width()/2.223), int(4*marouxo.niveau.get_height()/ 4.1), "Panda",panda_vivent, [panda_moitié_vivent,panda_mort],int(2*marouxo.niveau.get_width()/2.25),int(2*marouxo.niveau.get_width()/2.07))),
                          (Ennemie(int(2*marouxo.niveau.get_width()/2.223), int(4*marouxo.niveau.get_height()/ 12), "Fin Niveau",serpent_rouge_vivent, [serpent_rouge_moitié_vivent,serpent_rouge_mort],None,None)))
                        
    if marouxo.niveau == niveau2:
        
        ennemis_group = pygame.sprite.Group()

        ennemis_group.add((Ennemie(int(2*marouxo.niveau.get_width()/4.35), int(4*marouxo.niveau.get_height()/ 15.1), "Panda",panda_vivent, [panda_moitié_vivent,panda_mort],int(2*marouxo.niveau.get_width()/4.8),int(2*marouxo.niveau.get_width()/3.75))),
                          (Ennemie(int(2*marouxo.niveau.get_width()/3.35), int(4*marouxo.niveau.get_height()/ 14.1), "Panda",panda_vivent, [panda_moitié_vivent,panda_mort],int(2*marouxo.niveau.get_width()/3.6),int(2*marouxo.niveau.get_width()/3))),
                          (Ennemie(int(2*marouxo.niveau.get_width()/6.35), int(4*marouxo.niveau.get_height()/ 20.1), "Panda",panda_vivent, [panda_moitié_vivent,panda_mort],int(2*marouxo.niveau.get_width()/8.9),int(2*marouxo.niveau.get_width()/5.05))),
                          (Ennemie(int(2*marouxo.niveau.get_width()/2.73), int(4*marouxo.niveau.get_height()/ 17.5), "Serpent",serpent_rouge_vivent, [serpent_rouge_moitié_vivent,serpent_rouge_mort],None,None)),
                          (Ennemie(int(2*marouxo.niveau.get_width()/3.35), int(4*marouxo.niveau.get_height()/ 52.1), "Panda",panda_vivent, [panda_moitié_vivent,panda_mort],int(2*marouxo.niveau.get_width()/3.8),int(2*marouxo.niveau.get_width()/3.1))),
                          (Ennemie(int(2*marouxo.niveau.get_width()/3.70), int(4*marouxo.niveau.get_height()/ 1005.1), "Serpent",serpent_bleu_vivent, [serpent_bleu_moitié_vivent,serpent_bleu_mort],None,None)),
                          (Ennemie(int(2*marouxo.niveau.get_width()/3.30), int(4*marouxo.niveau.get_height()/ 1005.1), "Serpent",serpent_bleu_vivent, [serpent_bleu_moitié_vivent,serpent_bleu_mort],None,None)),
                          (Ennemie(int(2*marouxo.niveau.get_width()/2.8), int(4*marouxo.niveau.get_height()/ -17.7), "Panda",panda_vivent, [panda_moitié_vivent,panda_mort],int(2*marouxo.niveau.get_width()/2.9),int(2*marouxo.niveau.get_width()/2.43))),
                          (Ennemie(int(2*marouxo.niveau.get_width()/20), int(4*marouxo.niveau.get_height()/ -15.1), "Panda",panda_vivent, [panda_moitié_vivent,panda_mort],int(2*marouxo.niveau.get_width()/62),int(2*marouxo.niveau.get_width()/12))),
                          (Ennemie(int(2*marouxo.niveau.get_width()/7), int(4*marouxo.niveau.get_height()/ -11.5), "Panda",panda_vivent, [panda_moitié_vivent,panda_mort],int(2*marouxo.niveau.get_width()/12),int(2*marouxo.niveau.get_width()/5))),
                          (Ennemie(int(2*marouxo.niveau.get_width()/3.30), int(4*marouxo.niveau.get_height()/ -11.25), "Serpent",serpent_bleu_vivent, [serpent_bleu_moitié_vivent,serpent_bleu_mort],None,None)),
                          (Ennemie(int(2*marouxo.niveau.get_width()/2.73), int(4*marouxo.niveau.get_height()/ -8.75), "Serpent",serpent_rouge_vivent, [serpent_rouge_moitié_vivent,serpent_rouge_mort],None,None)),
                          (Ennemie(int(2*marouxo.niveau.get_width()/3), int(4*marouxo.niveau.get_height()/ -8.75), "Serpent",serpent_vert_vivent, [serpent_vert_moitié_vivent,serpent_vert_mort],None,None)),
                          (Ennemie(int(2*marouxo.niveau.get_width()/2.3), int(4*marouxo.niveau.get_height()/-7.9), "Fin Niveau",serpent_rouge_vivent, [serpent_rouge_moitié_vivent,serpent_rouge_mort],None,None)))

    if marouxo.niveau == salle_du_boss:

        ennemis_group = pygame.sprite.Group()
        
        ennemis_group.add((Ennemie(int(2*surface.get_width()/2.923), int(4*surface.get_height()/ 8.1), "Boss",gorilla_gauche, [gorilla_moitié_vivent, gorilla_mort],None,None)))

    return ennemis_group
