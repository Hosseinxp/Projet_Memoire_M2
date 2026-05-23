# Automatisation de la Génération de Backgrounds 2.5D Low Poly sur Blender

> **Projet de fin d'études — Mémoire de Master 2 MIAGE (Université Paris Nanterre / OPmobility)** > **Développeur :** Hossein ZAER  
> **Date de soutenance :** 1er juin 2026  

---

## 🎯 But du Projet & Problématique

Ce projet a pour objectif de concevoir et d'implémenter un pipeline logiciel automatisé capable de transformer une **photographie bidimensionnelle unique du monde réel** en un **maillage 3D (2.5D) stylisé en *low poly***, directement exploitable comme décor d'arrière-plan (*background*) dans un moteur de jeu temps réel tel qu'Unity.

### La Problématique
Comment s'affranchir des dépendances matérielles lourdes liées aux architectures propriétaires NVIDIA/CUDA (généralement requises par les IA 3D natives comme Consistent123 ou 3DGS) pour proposer une solution agile, ultra-rapide (exécution en moins de 30 secondes) et optimisée localement pour les architectures **Apple Silicon** ?

---

## 🏗️ Architecture du Pipeline (Les 4 Phases)

Le système est piloté de manière centralisée par un script d'orchestration Python (`generation_heart.py`) fonctionnant en mode *headless* (sans interface graphique), qui fait communiquer quatre intelligences artificielles de manière séquentielle :

1. **Phase 1 — Inférence & Génération Latente (Le Noyau IA)** : Extraction sémantique du contexte textuel par **BLIP**, estimation de la topologie par **Depth Anything V2**, et application de la direction artistique *flat design* via **Stable Diffusion 1.5** conditionné spatialement par **ControlNet**.
2. **Phase 2 — Reconstruction Géométrique Brute** : Injection de la carte de profondeur dans Blender via l'API `bpy` et application d'un modificateur *Displace* sur un plan subdivisé pour ériger le premier relief.
3. **Phase 3 — Pré-traitement Algorithmique (Smart Depth)** : Nettoyage matriciel de la carte de profondeur via **OpenCV** (filtre bilatéral pour lisser les surfaces architecturales) couplé à une segmentation sémantique par **YOLOv8-seg** pour isoler et protéger l'intégrité des structures organiques complexes (ex: feuillages de plantes).
4. **Phase 4 — Assemblage Spatial & Intégration** : Sculpture finale du maillage optimisé dans Blender, projection des textures et exportation automatique au format `.fbx` pour une intégration directe avec gestion des lumières dynamiques dans **Unity**.

---

## 💻 Prérequis & Installation

### Matériel cible
* Station de travail **Apple Silicon (Puce ARM M4 Pro)** avec **24 Go de mémoire unifiée** (ou configuration équivalente).

### Dépendances Logicielles
L'environnement nécessite Python 3.11, Blender (exécutable natif accessible en ligne de commande) et les bibliothèques listées dans le fichier `requirements.txt`.

1. Cloner le dépôt :
```bash
git clone [https://github.com/votre-username/Cubot_Pipeline.git](https://github.com/votre-username/Cubot_Pipeline.git)
cd Cubot_Pipeline