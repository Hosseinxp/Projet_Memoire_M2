import bpy
import os
import sys # <-- Nouveau

# Récupération des arguments passés après "--" par le script principal
try:
    index = sys.argv.index("--") + 1
    args = sys.argv[index:]
except ValueError:
    args = []

if len(args) < 4:
    print("ERREUR : Il manque des chemins pour le script Blender.")
    sys.exit(1)

# --- CONFIGURATION DES CHEMINS DYNAMIQUES ---
CHEMIN_DEPTH = os.path.abspath(args[0])
CHEMIN_COULEUR = os.path.abspath(args[1])
CHEMIN_SAUVEGARDE = os.path.abspath(args[2])
CHEMIN_EXPORT_FBX = os.path.abspath(args[3])

# 1. Nettoyer la scène
bpy.ops.wm.read_factory_settings(use_empty=True)

# 2. Créer le plan
bpy.ops.mesh.primitive_plane_add(size=2.0, location=(0, 0, 0))
plane = bpy.context.active_object
plane.name = "Relief_2_5D"

# --- NOUVEAU : Étirer le plan au format paysage (Ratio 2:1) ---
plane.scale[0] = 2.0 
bpy.ops.object.transform_apply(scale=True)

# 3. Subdiviser le plan
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.subdivide(number_cuts=100)
bpy.ops.object.mode_set(mode='OBJECT')

print("\n" + "="*50)

# 4. LE DISPLACEMENT (Sculpture)
if os.path.exists(CHEMIN_DEPTH):
    img_depth = bpy.data.images.load(CHEMIN_DEPTH)
    tex_depth = bpy.data.textures.new("Texture_Profondeur", type='IMAGE')
    tex_depth.image = img_depth
    mod_displace = plane.modifiers.new("Sculpture_Profondeur", type='DISPLACE')
    mod_displace.texture = tex_depth
    mod_displace.strength = 0.3
    mod_displace.mid_level = 0.0
    print("SUCCÈS : Le modificateur de Displacement a sculpté le maillage !")
    
    # --- AJOUT CRUCIAL : Geler la géométrie ---
    bpy.context.view_layer.objects.active = plane
    bpy.ops.object.modifier_apply(modifier=mod_displace.name)
    print("SUCCÈS : La géométrie 3D a été figée (Modificateur appliqué) !")

# 5. L'HABILLAGE (Version Blindée)
print("\n--- Création du Matériau ---")
if os.path.exists(CHEMIN_COULEUR):
    try:
        mat = bpy.data.materials.new(name="Materiel_LowPoly")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()

        node_output = nodes.new(type='ShaderNodeOutputMaterial')
        node_bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
        node_tex = nodes.new(type='ShaderNodeTexImage')

        node_tex.image = bpy.data.images.load(CHEMIN_COULEUR)

        links.new(node_tex.outputs['Color'], node_bsdf.inputs['Base Color'])
        links.new(node_bsdf.outputs['BSDF'], node_output.inputs['Surface'])

        objet_cible = bpy.data.objects.get("Relief_2_5D")
        
        if objet_cible:
            if len(objet_cible.data.materials) == 0:
                objet_cible.data.materials.append(mat)
            else:
                objet_cible.data.materials[0] = mat
            print("SUCCÈS : Le matériau a été accroché à l'objet 'Relief_2_5D' !")
        else:
            print("ERREUR GRAVE : L'objet 3D a disparu de la mémoire.")
            
    except Exception as e:
        print(f"CRASH PYTHON durant la création du matériau : {e}")
else:
    print(f"ERREUR : L'image couleur est introuvable au chemin : {CHEMIN_COULEUR}")

print("="*50 + "\n")

# 6. Sauvegarder le fichier .blend
try:
    bpy.ops.wm.save_as_mainfile(filepath=CHEMIN_SAUVEGARDE)
    print(f"Fichier de contrôle sauvegardé ici : {CHEMIN_SAUVEGARDE}\n")
except Exception as e:
    print(f"ERREUR LORS DE LA SAUVEGARDE : {e}")

# 7. L'EXPORTATION FBX (Configuration selon capture d'écran)
print("\n--- Exportation du Modèle FBX ---")
try:
    bpy.ops.object.select_all(action='DESELECT')
    objet_cible = bpy.data.objects.get("Relief_2_5D")
    
    if objet_cible:
        objet_cible.select_set(True)
        
        # Application des réglages : Path Mode Copy, Embed Textures, -Z Forward, Y Up
        bpy.ops.export_scene.fbx(
            filepath=CHEMIN_EXPORT_FBX,
            use_selection=True,
            object_types={'MESH'}, # <- CORRECTION ICI
            path_mode='COPY',
            embed_textures=True,
            batch_mode='OFF',
            global_scale=1.0,
            apply_scale_options='FBX_SCALE_ALL',
            axis_forward='-Z',
            axis_up='Y',
            apply_unit_scale=True,
            use_space_transform=True,
            mesh_smooth_type='OFF',
            use_mesh_modifiers=True,
            colors_type='SRGB'
        )
        print(f"SUCCÈS : Le modèle FBX est prêt avec la configuration demandée : {CHEMIN_EXPORT_FBX}")
    else:
        print("ERREUR : Objet introuvable pour l'exportation.")
except Exception as e:
    print(f"ERREUR LORS DE L'EXPORTATION FBX : {e}")