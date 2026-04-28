import os
from transformers import pipeline
from PIL import Image

def generate_depth_map_local(input_image_path, output_image_path):
    print(f"\n--- Démarrage de la Phase 2 (Scanner 3D Local) pour : {input_image_path} ---")
    
    if not os.path.exists(input_image_path):
        print("Erreur : L'image source n'existe pas. As-tu bien terminé la Phase 1 ?")
        return

    print("1. Chargement du modèle IA en mémoire (peut prendre quelques secondes)...")
    pipe = pipeline(task="depth-estimation", model="depth-anything/Depth-Anything-V2-Small-hf")

    print("2. Scan 3D de l'image en cours...")
    image = Image.open(input_image_path)
    result = pipe(image)
    depth_image = result["depth"]

    print("3. Sauvegarde de la carte de profondeur...")
    depth_image.save(output_image_path)
    
    print(f"Succès ! La carte de profondeur a été sauvegardée ici : {output_image_path}\n")

if __name__ == "__main__":
    image_source = "inputs/Desk/Desk.png"
    image_resultat = "temp/Desk/Desk_depth.png" 
    generate_depth_map_local(image_source, image_resultat)


    