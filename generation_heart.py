import os
import subprocess
import sys



PROJET = "Parc"


IMG_SOURCE = f"Experimentation/{PROJET}/{PROJET}_source.png"
DEPTH_BRUTE = f"temp/{PROJET}/{PROJET}_depth.png"
DEPTH_CLEAN = f"temp/{PROJET}/{PROJET}_depth_clean.png"
IMG_FINAL = f"temp/{PROJET}/{PROJET}_final.png"


BLENDER_BLEND = f"Blender_output/Experimentation/{PROJET}/{PROJET}.blend"
BLENDER_FBX = f"Blender_output/Experimentation/{PROJET}/{PROJET}.fbx"


SUJET_PROMPT = "underground subway station platform" 

CHEMIN_BLENDER = "/Applications/Blender.app/Contents/MacOS/Blender" 


for chemin in [IMG_SOURCE, DEPTH_BRUTE, BLENDER_BLEND]:
    dossier = os.path.dirname(chemin)
    if dossier:
        os.makedirs(dossier, exist_ok=True)


def executer_script(commande):
    print(f"\n{'='*60}")
    print(f"LANCEMENT : {' '.join(commande)}")
    try:
        subprocess.run(commande, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"RASH : La commande a échoué avec l'erreur {e}")
        return False


if __name__ == "__main__":
    print(f"--- DÉMARRAGE DU PIPELINE POUR : {PROJET} ---")
    

    python_exe = sys.executable
    
    # Phase 1 : Profondeur
    if not executer_script([python_exe, "generate_depth.py", IMG_SOURCE, DEPTH_BRUTE]):
        sys.exit("\nARRÊT DU PIPELINE : La Phase 1 (Scanner 3D) a échoué.")
    
    # Phase 2 : Nettoyage sans YOLO pour le décor
    if not executer_script([python_exe, "clean_depth.py", DEPTH_BRUTE, DEPTH_CLEAN]):
        sys.exit("\nARRÊT DU PIPELINE : La Phase 2 (Optimisation) a échoué.")
    
    # Phase 3 : Texture IA
    if not executer_script([python_exe, "generate_controlnet.py", IMG_SOURCE, DEPTH_CLEAN, IMG_FINAL, SUJET_PROMPT]):
        sys.exit("\nARRÊT DU PIPELINE : La Phase 3 (Texture IA) a échoué.")
    
    # Phase 4 : Blender (ATTENTION: le "--" est obligatoire)
    if not executer_script([
        CHEMIN_BLENDER, "-b", "-P", "generate_3d.py", 
        "--", DEPTH_CLEAN, IMG_FINAL, BLENDER_BLEND, BLENDER_FBX
    ]):
        sys.exit("\n ARRÊT DU PIPELINE : La Phase 4 (Blender) a échoué.")
    
    print("\n✅ GÉNÉRATION TERMINÉE ! Le fichier FBX est prêt.")