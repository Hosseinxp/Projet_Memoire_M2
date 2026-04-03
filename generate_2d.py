import os
import requests
import base64
from dotenv import load_dotenv

# 1. Chargement de la clé de sécurité
load_dotenv()
hf_token = os.getenv("HF_TOKEN")

if not hf_token:
    print("Erreur : Clé HF_TOKEN introuvable.")
    exit()

# 2. Configuration de l'API
# On utilise la nouvelle URL de routage
API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {hf_token}"}

# 3. Fonction principale d'Image-to-Image
def stylize_environment(input_image_path, output_image_path):
    print(f"Lecture de l'image source : {input_image_path}")
    
    if not os.path.exists(input_image_path):
        print("Erreur : L'image d'entrée n'existe pas. Vérifie ton dossier 'inputs/'.")
        return

    # Transformation de l'image binaire en texte (Base64)
    with open(input_image_path, "rb") as f:
        image_base64 = base64.b64encode(f.read()).decode("utf-8")

    print("Envoi à l'IA pour stylisation (cela peut prendre quelques secondes)...")
    
    # --- NOUVEAU PROMPT CHIRURGICAL ---
    # On définit d'abord le SUJET : "A single modern upholstered chair, centered asset"
    # Puis on applique le STYLE Cubot : "constructed from clean, large, sharp geometric panels and facets"
    # Et on précise les couleurs des facettes pour le seat (gris) et les legs (wood)
    prompt = (
        "A single modern upholstered chair, centered asset, reconstructed from clean large sharp geometric faceted panels, "
        "grey fabric facets for the seat, light wood facets for the legs, low poly geometric art style, flat design, solid unlit colors, "
        "clean edges, no complex textures, minimalistic, plain grey background"
    )
    
    # Nouveau format de données (100% texte JSON) pour que le serveur comprenne
    payload = {
        "inputs": prompt,
        "image": image_base64,
        "parameters": {
            "strength": 0.70 # On augmente un peu la force pour casser la texture complexe du tissu
        }
    }

    # On envoie le paquet avec le paramètre "json="
    response = requests.post(API_URL, headers=headers, json=payload)

    # 4. Traitement du résultat
    if response.status_code == 200:
        with open(output_image_path, "wb") as f:
            f.write(response.content)
        print(f"Succès ! L'image stylisée a été sauvegardée ici : {output_image_path}")
    else:
        print(f"Erreur API ({response.status_code}) : {response.text}")

# Lancement du script
if __name__ == "__main__":
    image_source = "inputs/chair.jpg"
    image_resultat = "temp/chair_stylized.jpg"
    
    stylize_environment(image_source, image_resultat)