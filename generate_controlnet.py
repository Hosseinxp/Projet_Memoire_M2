import os
import torch
import sys # <-- Ajouter en haut avec les imports
from diffusers import StableDiffusionControlNetImg2ImgPipeline, ControlNetModel, UniPCMultistepScheduler
from PIL import Image

def generate_true_lowpoly(original_image_path, depth_map_path, output_image_path, detected_subject):
    print(f"\n--- Démarrage de la Stylisation Low-Poly Avancée ---")
    
    # 1. PRÉPARATION DES IMAGES (Format Paysage 2:1)
    print("1. Lecture et redimensionnement...")
    # MODIFICATION ICI : On passe de (512, 512) à (1024, 512)
    init_image = Image.open(original_image_path).convert("RGB").resize((1024, 512))
    depth_image = Image.open(depth_map_path).convert("RGB").resize((1024, 512))

    # 2. CHARGEMENT DES MOTEURS (Pipeline Img2Img pour les couleurs)
    print("2. Chargement des moteurs IA sur puce Apple Silicon...")
    controlnet = ControlNetModel.from_pretrained(
        "lllyasviel/sd-controlnet-depth", 
        torch_dtype=torch.float16, 
        use_safetensors=True
    )
    
    pipe = StableDiffusionControlNetImg2ImgPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5", 
        controlnet=controlnet, 
        torch_dtype=torch.float16, 
        use_safetensors=True
    )
    
    pipe.scheduler = UniPCMultistepScheduler.from_config(pipe.scheduler.config)
    pipe = pipe.to("mps")
    
    # 3. LE PROMPT CHIRURGICAL (Priorité absolue aux polygones)
    prompt = (
        f"A simplified geometric low poly 3D render of a {detected_subject}, "
        "reconstructed from highly visible flat triangular and polygonal faces with sharp defined edges, "
        "faceted structure, solid unlit colors, clean edges, minimalistic, masterpiece"
    )
    
    negative_prompt = "realistic, photographic, fabric texture, round, smooth, curved, noise, shadows, complex details"

    print("3. Sculpture géométrique en cours...")
    
    # 4. LES RÉGLAGES DE PRÉCISION
    image = pipe(
        prompt=prompt, 
        negative_prompt=negative_prompt,
        image=init_image,          # La photo originale (Couleurs)
        control_image=depth_image, # Le moule 3D (Structure)
        num_inference_steps=20,
        strength=0.3,                     # Permet de générer des polygones tout en gardant les couleurs
        controlnet_conditioning_scale=0.80 # 0.80 : Laisse l'IA casser les arrondis du moule
    ).images[0]

    # 5. SAUVEGARDE
    image.save(output_image_path)
    print(f"\nSuccès ! L'asset géométrique est sauvegardé ici : {output_image_path}\n")



if __name__ == "__main__":
    if len(sys.argv) > 4:
        image_originale = sys.argv[1]
        image_depth = sys.argv[2]
        image_resultat = sys.argv[3]
        sujet = sys.argv[4]
        
        generate_true_lowpoly(image_originale, image_depth, image_resultat, sujet)
    else:
        print("Erreur: Arguments manquants.")