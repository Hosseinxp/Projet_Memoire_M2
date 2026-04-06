import os
import requests
import base64
from dotenv import load_dotenv
# CHANGEMENT ICI : On importe les pièces explicites au lieu du raccourci pipeline
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

# 1. Chargement de la clé de sécurité
load_dotenv()
hf_token = os.getenv("HF_TOKEN")

if not hf_token:
    print("Erreur : Clé HF_TOKEN introuvable.")
    exit()

headers = {"Authorization": f"Bearer {hf_token}"}

DRAWING_API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"

def stylize_environment_auto(input_image_path, output_image_path):
    print(f"\n--- Démarrage de la Phase 1 (Génération 2D) pour : {input_image_path} ---")
    
    if not os.path.exists(input_image_path):
        print("Erreur : L'image d'entrée n'existe pas.")
        return

    with open(input_image_path, "rb") as f:
        image_binary = f.read()
        image_base64 = base64.b64encode(image_binary).decode("utf-8")

    # =========================================================
    # ÉTAPE A : Analyse Vision (LOCAL sur ton Mac)
    # =========================================================
    print("1. Analyse de l'image par l'IA de vision (Local)...")
    try:
        # On sécurise le format de l'image
        image_pil = Image.open(input_image_path).convert('RGB')
        
        # Approche robuste : On charge explicitement le cerveau et le traducteur
        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        
        # On prépare l'image pour l'IA
        inputs = processor(image_pil, return_tensors="pt")
        
        # L'IA génère la description
        out = model.generate(**inputs)
        detected_subject = processor.decode(out[0], skip_special_tokens=True)
        
        print(f"   -> Sujet détecté : '{detected_subject}'")
    except Exception as e:
        print(f"   -> Erreur Vision : {e}")
        detected_subject = "object" # Sécurité en cas d'échec

    # =========================================================
    # ÉTAPE B : Prompt Dynamique
    # =========================================================
    dynamic_prompt = (
        f"A simplified low poly geometric stylization of {detected_subject}, "
        "reconstructed from clean sharp geometric faceted panels preserving the exact structure of the object, "
        "flat design, solid unlit colors, clean edges, no complex textures, minimalistic, plain background"
    )

    # =========================================================
    # ÉTAPE C : Stylisation (CLOUD Hugging Face)
    # =========================================================
    print("2. Stylisation géométrique en cours (Cloud)...")
    payload = {
        "inputs": dynamic_prompt,
        "image": image_base64,
        "parameters": {"strength": 0.70}
    }

    response_draw = requests.post(DRAWING_API_URL, headers=headers, json=payload)

    if response_draw.status_code == 200:
        with open(output_image_path, "wb") as f:
            f.write(response_draw.content)
        print(f"3. Succès ! L'image est sauvegardée ici : {output_image_path}\n")
    else:
        print(f"Erreur Dessin ({response_draw.status_code}) : {response_draw.text}")

# Lancement du script
if __name__ == "__main__":
    image_source = "inputs/chair.jpg"
    image_resultat = "temp/chair_stylized.jpg"
    
    stylize_environment_auto(image_source, image_resultat)