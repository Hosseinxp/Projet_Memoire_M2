import os
import torch
import sys 
from diffusers import StableDiffusionControlNetImg2ImgPipeline, ControlNetModel, UniPCMultistepScheduler
from PIL import Image

def generate_true_lowpoly(original_image_path, depth_map_path, output_image_path, detected_subject):
    print(f"\n--- Démarrage de la Stylisation Low-Poly Avancée ---")
    
 
    print("1. Lecture et redimensionnement...")
    init_image = Image.open(original_image_path).convert("RGB").resize((1024, 512))
    depth_image = Image.open(depth_map_path).convert("RGB").resize((1024, 512))


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
    

    prompt = (
        f"A simplified geometric low poly 3D render of a {detected_subject}, "
        "reconstructed from highly visible flat triangular and polygonal faces with sharp defined edges, "
        "faceted structure, solid unlit colors, clean edges, minimalistic, masterpiece"
    )
    
    negative_prompt = "realistic, photographic, fabric texture, round, smooth, curved, noise, shadows, complex details"

    print("3. Sculpture géométrique en cours...")
    

    image = pipe(
        prompt=prompt, 
        negative_prompt=negative_prompt,
        image=init_image,          
        control_image=depth_image, 
        num_inference_steps=20,
        strength=0.3,                     
        controlnet_conditioning_scale=0.80 
    ).images[0]

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