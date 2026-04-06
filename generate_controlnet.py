import os
import torch
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel, UniPCMultistepScheduler
from PIL import Image

def stylize_with_controlnet(depth_map_path, output_image_path, detected_subject):
    print(f"\n--- Démarrage de la Stylisation Guidée par Géométrie ---")
    
    if not os.path.exists(depth_map_path):
        print(f"Erreur : La carte de profondeur {depth_map_path} est introuvable. As-tu lancé generate_depth.py ?")
        return

    # 1. Chargement du "Calque de Structure" (La Depth Map)
    print("1. Lecture et redimensionnement du scan de profondeur...")
    depth_image = Image.open(depth_map_path).convert("RGB")
    
    # CORRECTIF MAC/MPS : On force la résolution à 512x512 pixels
    # pour éviter l'explosion de la mémoire vive (Erreur 1839 GiB)
    depth_image = depth_image.resize((512, 512))

    # 2. Préparation des IA (LOCAL MAC)
    print("2. Chargement des moteurs IA (Ceci va télécharger env. 5 Go la première fois)...")
    
    # Le moteur qui force le respect de la profondeur
    controlnet = ControlNetModel.from_pretrained(
        "lllyasviel/sd-controlnet-depth", 
        torch_dtype=torch.float16, 
        use_safetensors=True
    )
    
    # Le moteur de dessin (Stable Diffusion 1.5, très rapide et optimisé)
    pipe = StableDiffusionControlNetPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5", 
        controlnet=controlnet, 
        torch_dtype=torch.float16, 
        use_safetensors=True
    )
    
    # Optimisation pour accélérer le calcul
    pipe.scheduler = UniPCMultistepScheduler.from_config(pipe.scheduler.config)
    
    # ACTIVATION DE LA PUCE APPLE SILICON (La magie de ton Mac)
    pipe = pipe.to("mps") 
    
    # 3. Le Prompt Chirurgical
    # On indique à l'IA d'utiliser le style Cubot sur l'objet détecté
    prompt = (
        f"A simplified low poly geometric stylization of a {detected_subject}, "
        "reconstructed from clean sharp geometric faceted panels, flat design, "
        "solid unlit colors, clean edges, minimalistic, 3D render, masterpiece"
    )
    
    # Mots-clés négatifs pour empêcher l'IA de rajouter du réalisme
    negative_prompt = "realistic, photographic, complex textures, shadows, messy, text, watermark, bad anatomy, extra limbs"

    print("3. Application de la peinture géométrique sur la structure...")
    
    # L'IA génère l'image en 20 étapes
    image = pipe(
        prompt, 
        negative_prompt=negative_prompt,
        image=depth_image, 
        num_inference_steps=20,
        controlnet_conditioning_scale=1.0 # Force de respect de la géométrie (1.0 = Strict)
    ).images[0]

    # 4. Sauvegarde
    image.save(output_image_path)
    print(f"\nSuccès ! L'image finale hyper-fidèle est sauvegardée ici : {output_image_path}\n")

# Lancement du script
if __name__ == "__main__":
    # L'entrée est la CARTE DE PROFONDEUR, pas l'image d'origine !
    depth_source = "temp/chair_depth.png"
    result_final = "temp/chair_final_cubot.jpg"
    
    # En situation réelle (Phase 4), ce mot viendra automatiquement de BLIP. 
    # Pour ce test, on le met manuellement.
    sujet = "gray armchair with light wood legs" 
    
    stylize_with_controlnet(depth_source, result_final, sujet)