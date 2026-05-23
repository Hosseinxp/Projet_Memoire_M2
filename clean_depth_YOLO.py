import cv2
import numpy as np
import os
from ultralytics import YOLO

def process_smart_depth(color_path, depth_path, output_path):
    print("1. Initialisation de l'IA YOLO...")
    model = YOLO('yolov8m-seg.pt')

    print("2. Chargement des matrices...")
    
 
    if not os.path.exists(color_path):
        print(f"ERREUR CRITIQUE : Impossible de trouver l'image couleur ici -> {color_path}")
        return
    if not os.path.exists(depth_path):
        print(f"ERREUR CRITIQUE : Impossible de trouver la carte de profondeur ici -> {depth_path}")
        return

    img_color = cv2.imread(color_path)
    depth_map = cv2.imread(depth_path, cv2.IMREAD_GRAYSCALE)

    mask = np.zeros(depth_map.shape, dtype=np.uint8)

    print("3. Analyse sémantique en cours...")
    results = model(img_color)

    if results[0].masks is not None:
        mask_tensor = results[0].masks.data[0].cpu().numpy()
        mask_resized = cv2.resize(mask_tensor, (depth_map.shape[1], depth_map.shape[0]))
        mask = (mask_resized * 255).astype(np.uint8)

    print("4. Traitement OpenCV (Lissage et Normalisation)...")
    depth_smoothed = cv2.bilateralFilter(depth_map, d=9, sigmaColor=75, sigmaSpace=75)

    seuil_noir = 15
    depth_smoothed[depth_smoothed < seuil_noir] = 0
    depth_map[depth_map < seuil_noir] = 0 

    print("5. Fusion intelligente des données...")
    final_depth = np.where(mask > 127, depth_map, depth_smoothed)

    print("6. Sauvegarde du fichier optimisé...")
    cv2.imwrite(output_path, final_depth)
    print(f"✅ Succès ! L'image finale est sauvegardée sous : {output_path}")

# ==========================================
# EXÉCUTION DU SCRIPT
# ==========================================
if __name__ == "__main__":
 
    FICHIER_COULEUR = "inputs/Plant/Plant.png"     
    FICHIER_PROFONDEUR = "temp/Plant/Plant_depth.png" 
    FICHIER_SORTIE = "temp/Plant/Plant_depth_smart.png" 

    process_smart_depth(FICHIER_COULEUR, FICHIER_PROFONDEUR, FICHIER_SORTIE)