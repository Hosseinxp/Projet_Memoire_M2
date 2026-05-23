import cv2
import numpy as np
import sys 

if len(sys.argv) < 3:
    print("Erreur: arguments manquants. Usage: python clean_depth.py <entree> <sortie>")
    sys.exit(1)

chemin_entree = sys.argv[1]
chemin_sortie = sys.argv[2]

print("--- Démarrage de l'optimisation OpenCV ---")


img = cv2.imread(chemin_entree, cv2.IMREAD_GRAYSCALE)

if img is not None:

    img_lisse = cv2.bilateralFilter(img, d=9, sigmaColor=75, sigmaSpace=75)
    

    seuil_noir = 15
    img_lisse[img_lisse < seuil_noir] = 0

    cv2.imwrite(chemin_sortie, img_lisse)
    print(f"Succès : Carte de profondeur optimisée enregistrée sous '{chemin_sortie}'")
    
else:
    print(f"Erreur : Impossible de lire le fichier '{chemin_entree}'. Vérifiez le chemin.")