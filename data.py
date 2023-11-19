import toml

# Load the TOML file
data = toml.load("construction_devis.toml")

# Access Maison plans
maison_plans = data["Plans"]["maison"]
plans_de_maison_simple = maison_plans["Plans_de_maison_simple"]
plans_de_maison_standard = maison_plans["Plans_de_maison_standard"]
plans_de_maison_sur_mesure = maison_plans["Plans_de_maison_sur_mesure"]
plans_de_maison_par_un_architecte = maison_plans["Plans_de_maison_par_un_architecte"]

# Access values from travaux_terrassement
gros_oeuvre = data["travaux"]["gros_oeuvre"]
travaux_terrassement = gros_oeuvre["travaux_terrassement"]
Reperage_et_piquetage_du_terrain = travaux_terrassement["Reperage_et_piquetage_du_terrain"]

# Access values from Fondations_profondes
fondations = gros_oeuvre["fondations"]
Fondations_profondes = fondations["Fondations_profondes"]

# Access values from travaux.materiaux
materiaux = data["travaux"]["materiaux"]
Nivellement_de_terrain = materiaux["Nivellement_de_terrain"]
Tranchee_epaisse = materiaux["Tranchee_epaisse"]
Tranchee_etroite = materiaux["Tranchee_etroite"]
Fouille_en_masse = materiaux["Fouille_en_masse"]
Fouille_manuelle = materiaux["Fouille_manuelle"]
Deblai = materiaux["Deblai"]
Remblai_terre = materiaux["Remblai_terre"]
Remblai_sable = materiaux["Remblai_sable"]
Enrochement = materiaux["Enrochement"]
Beton = materiaux["Beton"]
coffrage = materiaux["coffrage"]
plancger_beton = materiaux["plancger_beton"]
chape_de_ciment = materiaux["chape_de_ciment"]
construction_mur_parpaing = materiaux["construction_mur_parpaing"]
mur_en_agglo_de_ciment_creaux = materiaux["mur_en_agglo_de_ciment_creaux"]
Cloison_en_plaque_de_platre_simple = materiaux["Cloison_en_plaque_de_platre_simple"]
Porte_dentree_en_aluminium = materiaux["Porte_dentree_en_aluminium"]
Portes_interieures = materiaux["Portes_interieures"]
Fenetre_aluminium = materiaux["Fenetre_aluminium"]
Volets_en_bois = materiaux["Volets_en_bois"]

# Access values from travaux.second_oeuvre
second_oeuvre = data["travaux"]["second_oeuvre"]
Charpente_traditionnelle = second_oeuvre["Charpente_traditionnelle"]
Couverture_toiture_en_tuiles = second_oeuvre["Couverture_toiture_en_tuiles"]
Isolation_des_murs_par_interieur = second_oeuvre["Isolation_des_murs_par_interieur"]
Isolation_des_combles = second_oeuvre["Isolation_des_combles"]
Coffret_de_raccordement_exterieur_encastrer = second_oeuvre["Coffret_de_raccordement_exterieur_encastrer"]
Coffrets_pre_equipes = second_oeuvre["Coffrets_pre-equipes"]
Interrupteur_differentiel = second_oeuvre["Interrupteur_differentiel"]
Coupe_circuit_domestique = second_oeuvre["Coupe_circuit_domestique"]
Prise_murale = second_oeuvre["Prise_murale"]
Point_lumineux = second_oeuvre["Point_lumineux"]
Branchement_alimentation = second_oeuvre["Branchement_alimentation"]
Raccordement_evacuation_en_cuivre = second_oeuvre["Raccordement_evacuation_en_cuivre"]
Robinetterie_pour_machine_a_laver = second_oeuvre["Robinetterie_pour_machine_a_laver"]
Robinetterie_salle_de_bain = second_oeuvre["Robinetterie_salle_de_bain"]
Robinetterie_chasse_deau_WC = second_oeuvre["Robinetterie_chasse_deau_WC"]
Robinetterie_pour_lavabo_et_eviers = second_oeuvre["Robinetterie_pour_lavabo_et_eviers"]
Raccordement_au_compteur_deau = second_oeuvre["Raccordement_au_compteur_deau"]

# Access values from travaux.main_doeuvre
main_doeuvre = data["travaux"]["main_doeuvre"]
Installation_charpente = main_doeuvre["Installation_charpente"]
Isolation_des_murs_par_interieur_main = main_doeuvre["Isolation_des_murs_par_interieur"]
Isolation_des_combles_main = main_doeuvre["Isolation_des_combles"]
Coffret_de_raccordement_exterieur_encastrer_main = main_doeuvre["Coffret_de_raccordement_exterieur_encastrer"]
Coffrets_pre_equipes_main = main_doeuvre["Coffrets_pre-equipes"]
Coupe_circuit_domestique_main = main_doeuvre["Coupe_circuit_domestique"]
Interrupteur_differentiel_main = main_doeuvre["Interrupteur_differentiel"]
Prise_murale_main = main_doeuvre["Prise_murale"]
Point_lumineux_main = main_doeuvre["Point_lumineux"]
Branchement_alimentation_main = main_doeuvre["Branchement_alimentation"]
Raccordement_evacuation_en_cuivre_main = main_doeuvre["Raccordement_evacuation_en_cuivre"]
Robinetterie_pour_machine_a_laver_main = main_doeuvre["Robinetterie_pour_machine_a_laver"]
Robinetterie_salle_de_bain_main = main_doeuvre["Robinetterie_salle_de_bain"]
Robinetterie_chasse_deau_WC_main = main_doeuvre["Robinetterie_chasse_deau_WC"]
Robinetterie_pour_lavabo_et_eviers_main = main_doeuvre["Robinetterie_pour_lavabo_et_eviers"]
Raccordement_au_compteur_deau_main = main_doeuvre["Raccordement_au_compteur_deau"]

# Access TVA values
TVA = data["TVA"]

