from flask import Flask, render_template, request, jsonify, send_file
import toml
from facture_generation import create_invoice, invoices_data, update_invoice
import re
import yaml
import math
import sqlite3

	
# Connect to the database or create it if it doesn't exist
conn = sqlite3.connect('./databases/contacts.db')
cursor = conn.cursor()

# Create a table if it doesn't exist to store contact form data
cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    message TEXT NOT NULL
                )''')
conn.commit()

# For reviews database
conn_review = sqlite3.connect('./databases/reviews.db')
cursor_review = conn_review.cursor()

cursor_review.execute('''
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rating INTEGER,
        feedback TEXT
    )
''')
conn_review.commit()


# Load the TOML file
data = toml.load("construction_devis.toml")

with open("price_prediction.yaml", "r") as file:
    data_house_prices = yaml.safe_load(file)

with open("rent_prediction.yaml", "r") as file:
    data_rent_prices = yaml.safe_load(file)

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
#Materiaux_list = [Nivellement_de_terrain, Tranchee_epaisse, Tranchee_etroite, Fouille_en_masse, Fouille_manuelle, Deblai, Remblai_terre, Remblai_sable, Enrochement, Beton, coffrage, plancger_beton, chape_de_ciment, construction_mur_parpaing, mur_en_agglo_de_ciment_creaux, Cloison_en_plaque_de_platre_simple, Porte_dentree_en_aluminium, Portes_interieures, Fenetre_aluminium, Volets_en_bois]

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

#second_oeuvre_list = [Charpente_traditionnelle, Couverture_toiture_en_tuiles, Isolation_des_murs_par_interieur, Isolation_des_combles, Branchement_alimentation, Raccordement_evacuation_en_cuivre, Raccordement_au_compteur_deau, Coffret_de_raccordement_exterieur_encastrer, Coffrets_pre_equipes, Interrupteur_differentiel, Coupe_circuit_domestique, Robinetterie_pour_machine_a_laver, Robinetterie_salle_de_bain, Robinetterie_chasse_deau_WC, Robinetterie_pour_lavabo_et_eviers, Prise_murale, Point_lumineux]


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
Porte_dentree_en_aluminium = main_doeuvre["Porte_dentree_en_aluminium"]
Portes_interieures = main_doeuvre["Portes_interieures"]
Fenetre_aluminium = main_doeuvre["Fenetre_aluminium"]
Volets_en_bois = main_doeuvre["Volets_en_bois"]

main_oeuvre_list  = [Installation_charpente, Isolation_des_murs_par_interieur_main, Isolation_des_combles_main, Branchement_alimentation_main, Raccordement_evacuation_en_cuivre_main, Raccordement_au_compteur_deau_main, Coffret_de_raccordement_exterieur_encastrer_main*0.01, Coffrets_pre_equipes_main*0.01, Coupe_circuit_domestique_main*0.01, Interrupteur_differentiel_main*0.01, Prise_murale_main*0.01, Point_lumineux_main*0.01, Robinetterie_pour_machine_a_laver_main*0.01, Robinetterie_salle_de_bain_main*0.01, Robinetterie_chasse_deau_WC_main*0.01, Robinetterie_pour_lavabo_et_eviers_main*0.01, Portes_interieures*0.1, Fenetre_aluminium*0.1, Volets_en_bois*0.1, Porte_dentree_en_aluminium]
Materiaux_list = [Remblai_terre*0.01, Remblai_sable*0.1, Enrochement*0.3, Beton, coffrage, chape_de_ciment, mur_en_agglo_de_ciment_creaux, Porte_dentree_en_aluminium*0.02, Portes_interieures*0.1, Fenetre_aluminium*0.1, Volets_en_bois*0.1, Charpente_traditionnelle, Couverture_toiture_en_tuiles]
gros_oeuvre_list = [Reperage_et_piquetage_du_terrain, Nivellement_de_terrain, Tranchee_epaisse, Tranchee_etroite, Fouille_en_masse, Fouille_manuelle, Deblai, Fondations_profondes, construction_mur_parpaing, plancger_beton]# Access TVA values
second_oeuvre_list = [Isolation_des_murs_par_interieur, Isolation_des_combles, Cloison_en_plaque_de_platre_simple, Coffret_de_raccordement_exterieur_encastrer*0.01, Coffrets_pre_equipes*0.01, Interrupteur_differentiel*0.01, Coupe_circuit_domestique*0.1, Prise_murale*0.1, Point_lumineux*0.1, Robinetterie_salle_de_bain, Robinetterie_chasse_deau_WC, Robinetterie_pour_lavabo_et_eviers, Robinetterie_pour_machine_a_laver]

TVA = data["TVA"]
app = Flask(__name__)
invoice_data = invoices_data()

def extract_zipcode(input_string):
    # Define a regular expression pattern to match a 5-digit zip code
    pattern = r'\b\d{5}\b'

    # Use re.search to find the first match
    match = re.search(pattern, input_string)

    if match:
        return match.group(0)
    else:
        return None

def get_prices(zip_code, surface, terrain, hauteur_price):
    zip_code = str(int(zip_code) // 1000)
    for entry in data_house_prices:
        department = entry["department"]
        zip_codes = entry.get("postal_code", [])
        if zip_code in zip_codes:
            price_1 = entry["price_per_sqm"][0] * surface * hauteur_price + entry["price_per_sqm"][0] * (terrain - surface) * 1 / 12
            price_2 = (entry["price_per_sqm"][0] + entry["price_per_sqm"][1]) / 2  * surface * hauteur_price + ((entry["price_per_sqm"][0] / 2 + entry["price_per_sqm"][1] / 2) * (terrain-surface))*  1 / 12
            prince_3 = entry["price_per_sqm"][1] * surface * hauteur_price + (entry["price_per_sqm"][1] * (terrain - surface)) * 1 / 12  
            return round(price_1, 2), round(price_2, 2), round(prince_3, 2)

    return None, None  # Return None if the ZIP code is not found

def get_rent_prices(zip_code, surface, hauteur_price):
    zip_code = str(int(zip_code) // 1000)
    for entry in data_rent_prices:
        department = entry["department"]
        zip_codes = entry.get("postal_code", [])
        if zip_code in zip_codes:
            price_rent_1 = entry["price_per_sqm"][0] * surface * hauteur_price
            price_rent_2 = ((entry["price_per_sqm"][0] + entry["price_per_sqm"][1]) / 2 ) * surface * hauteur_price
            prince_rent_3 = entry["price_per_sqm"][1] * surface * hauteur_price
            return round(price_rent_1, 2), round(price_rent_2, 2), round(prince_rent_3, 2)
    return None, None  # Return None if the ZIP code is not found

def AI_surface_optimisation(surface, limites_hauteur):
	pieces = math.ceil(surface / 20)
	chambre = pieces // 2
	if limites_hauteur == "rdc":
		pieces =  pieces
		chambre = chambre
	elif limites_hauteur == "r+1etage":
		pieces =  pieces * 2
		chambre = chambre * 2
	elif limites_hauteur == "r+2etage":
		pieces =  pieces * 3
		chambre = chambre * 3
	elif limites_hauteur == "r+3etage":
		pieces =  pieces * 4
		chambre = chambre * 4
	elif limites_hauteur == "r+4etage":
		pieces =  pieces * 5
		chambre = chambre * 5
	elif limites_hauteur == "r+5etage":
		pieces =  pieces * 6
		chambre = chambre * 6
	elif limites_hauteur == "r+6etage":
		pieces =  pieces * 7
		chambre = chambre * 7
	elif limites_hauteur == "soussoul+r":
		pieces =  pieces
		chambre = chambre
	elif limites_hauteur == "soussoul+1etage":
		pieces =  pieces * 2
		chambre = chambre * 2
	elif limites_hauteur == "soussoul+2etage":
		pieces =  pieces * 3
		chambre = chambre * 3
	elif limites_hauteur == "soussoul+3etage":
		pieces =  pieces * 4
		chambre = chambre * 4
	elif limites_hauteur == "soussoul+4etage":
		pieces =  pieces * 5
		chambre = chambre * 5
	elif limites_hauteur == "soussoul+5etage":
		pieces =  pieces * 6
		chambre = chambre * 6
	elif limites_hauteur == "soussoul+6etage":
		pieces =  pieces * 7
		chambre = chambre * 7
	return pieces, chambre
def Materiaux_calculation(Materiaux_list, surface, limites_hauteur):
	materiaux_price = 0
	for material in Materiaux_list:
		materiaux_price += material * surface
	if limites_hauteur == "fondation":
		materiaux_price =  materiaux_price * 0.25
	elif limites_hauteur == "rdc":
		materiaux_price =  materiaux_price * 1
	elif limites_hauteur == "r+1etage":
		materiaux_price =  materiaux_price * 1.4
	elif limites_hauteur == "r+2etage":
		materiaux_price =  materiaux_price * 1.83
	elif limites_hauteur == "r+3etage":
		materiaux_price =  materiaux_price * 2.25
	elif limites_hauteur == "r+4etage":
		materiaux_price =  materiaux_price * 2.66
	elif limites_hauteur == "r+5etage":
		materiaux_price =  materiaux_price * 3
	elif limites_hauteur == "r+6etage":
		materiaux_price =  materiaux_price * 3.5
	elif limites_hauteur == "soussoul+r":
		materiaux_price =  materiaux_price * 1.4
	elif limites_hauteur == "soussoul+1etage":
		materiaux_price =  materiaux_price * 1.83
	elif limites_hauteur == "soussoul+2etage":
		materiaux_price =  materiaux_price * 2.25
	elif limites_hauteur == "soussoul+3etage":
		materiaux_price =  materiaux_price * 2.66
	elif limites_hauteur == "soussoul+4etage":
		materiaux_price =  materiaux_price * 3
	elif limites_hauteur == "soussoul+5etage":
		materiaux_price =  materiaux_price * 3.5
	elif limites_hauteur == "soussoul+6etage":
		materiaux_price =  materiaux_price * 3.8
	return materiaux_price

def hauteur_to_price(limites_hauteur):
	hauteur_price = 0
	if limites_hauteur == "fondation":
		hauteur_price =  0
	elif limites_hauteur == "rdc":
		hauteur_price =  1
	elif limites_hauteur == "r+1etage":
		hauteur_price =  1.4
	elif limites_hauteur == "r+2etage":
		hauteur_price =  1.8
	elif limites_hauteur == "r+3etage":
		hauteur_price =  2.2
	elif limites_hauteur == "r+4etage":
		hauteur_price =  2.6
	elif limites_hauteur == "r+5etage":
		hauteur_price =  3
	elif limites_hauteur == "r+6etage":
		hauteur_price =  3.4
	elif limites_hauteur == "soussoul+r":
		hauteur_price =  1.4
	elif limites_hauteur == "soussoul+1etage":
		hauteur_price =  1.8
	elif limites_hauteur == "soussoul+2etage":
		hauteur_price =  2.2
	elif limites_hauteur == "soussoul+3etage":
		hauteur_price =  2.6
	elif limites_hauteur == "soussoul+4etage":
		hauteur_price =  3
	elif limites_hauteur == "soussoul+5etage":
		hauteur_price =  3.4
	elif limites_hauteur == "soussoul+6etage":
		hauteur_price =  3.8
	return hauteur_price



def prices_for_type_bien(type_bien, materiaux_price):
	if type_bien == "traditionnelle":
		materiaux_price = materiaux_price * 1
	elif type_bien == "bois":
		materiaux_price = materiaux_price * 1.18
	elif type_bien == "contemporaine":
		materiaux_price = materiaux_price * 1.15
	elif type_bien == "ecologique":
		materiaux_price = materiaux_price * 1.15
	elif type_bien == "container":
		materiaux_price = materiaux_price * 1.1
	elif type_bien == "brique":
		materiaux_price = materiaux_price * 1.25
	return materiaux_price

def prices_for_typeLocalisation(type_Localisation, materiaux_price):
	if type_Localisation == "urbain":
		materiaux_price = materiaux_price * 1
	elif type_Localisation == "Semi-urbain":
		materiaux_price = materiaux_price * 0.85
	elif type_Localisation == "rural":
		materiaux_price = materiaux_price * 0.65
	elif type_Localisation == "littoral":
		materiaux_price = materiaux_price * 1.2
	return materiaux_price

def add_price_plan_house(plans, materiaux_price):
	if plans == "plan_simple":
		materiaux_price = materiaux_price + plans_de_maison_simple
	elif plans == "plan_standard":
		materiaux_price = materiaux_price + plans_de_maison_standard
	elif plans == "plan_sur_mesure":
		materiaux_price = materiaux_price + plans_de_maison_sur_mesure
	elif plans == "plan_architecte":
		materiaux_price = materiaux_price + plans_de_maison_par_un_architecte
	return materiaux_price

def Materiaux_totale_price(Materiaux_list, surface, limites_hauteur, type_bien, type_Localisation, plans):
	materieux_cal = Materiaux_calculation(Materiaux_list, int(surface), limites_hauteur)
	price_typebien = prices_for_type_bien(type_bien, materieux_cal)
	price_typeLocalisation = prices_for_typeLocalisation(type_Localisation, price_typebien)
	price_added = add_price_plan_house(plans, price_typeLocalisation)
	return price_added
	
def gros_oeuvre(gros_oeuvre_list, surface, limites_hauteur):
	gros_oeuvre_price = 0
	for gros in gros_oeuvre_list:
		gros_oeuvre_price += gros * surface
	if limites_hauteur == "fondation":
		gros_oeuvre_price =  gros_oeuvre_price * 0.25
	elif limites_hauteur == "rdc":
		gros_oeuvre_price =  gros_oeuvre_price * 1
	elif limites_hauteur == "r+1etage":
		gros_oeuvre_price =  gros_oeuvre_price * 1.4
	elif limites_hauteur == "r+2etage":
		gros_oeuvre_price =  gros_oeuvre_price * 1.83
	elif limites_hauteur == "r+3etage":
		gros_oeuvre_price =  gros_oeuvre_price * 2.25
	elif limites_hauteur == "r+4etage":
		gros_oeuvre_price =  gros_oeuvre_price * 2.66
	elif limites_hauteur == "r+5etage":
		gros_oeuvre_price =  gros_oeuvre_price * 3
	elif limites_hauteur == "r+6etage":
		gros_oeuvre_price =  gros_oeuvre_price * 3.5
	elif limites_hauteur == "soussoul+r":
		gros_oeuvre_price =  gros_oeuvre_price * 1.4
	elif limites_hauteur == "soussoul+1etage":
		gros_oeuvre_price =  gros_oeuvre_price * 1.83
	elif limites_hauteur == "soussoul+2etage":
		gros_oeuvre_price =  gros_oeuvre_price * 2.25
	elif limites_hauteur == "soussoul+3etage":
		gros_oeuvre_price =  gros_oeuvre_price * 2.66
	elif limites_hauteur == "soussoul+4etage":
		gros_oeuvre_price =  gros_oeuvre_price * 3
	elif limites_hauteur == "soussoul+5etage":
		gros_oeuvre_price =  gros_oeuvre_price * 3.5
	elif limites_hauteur == "soussoul+6etage":
		gros_oeuvre_price =  gros_oeuvre_price * 3.8
	return gros_oeuvre_price
	

def main_oeuvre(main_oeuvre_list, surface, limites_hauteur):
    main_oeuvre_price = main_oeuvre_list[-1]
    for oeuvre in main_oeuvre_list[:-1]:
    	main_oeuvre_price += oeuvre * surface
    if limites_hauteur == "fondation":
	    main_oeuvre_price =  main_oeuvre_price * 0.25
    elif limites_hauteur == "rdc":
	    main_oeuvre_price =  main_oeuvre_price * 1
    elif limites_hauteur == "r+1etage":
	    main_oeuvre_price =  main_oeuvre_price * 1.4
    elif limites_hauteur == "r+2etage":
	    main_oeuvre_price =  main_oeuvre_price * 1.83
    elif limites_hauteur == "r+3etage":
	    main_oeuvre_price =  main_oeuvre_price * 2.25
    elif limites_hauteur == "r+4etage":
	    main_oeuvre_price =  main_oeuvre_price * 2.66
    elif limites_hauteur == "r+5etage":
	    main_oeuvre_price =  main_oeuvre_price * 3
    elif limites_hauteur == "r+6etage":
	    main_oeuvre_price =  main_oeuvre_price * 3.5
    elif limites_hauteur == "soussoul+r":
        main_oeuvre_price =  main_oeuvre_price * 1.4
    elif limites_hauteur == "soussoul+1etage":
	    main_oeuvre_price =  main_oeuvre_price * 1.83
    elif limites_hauteur == "soussoul+2etage":
	    main_oeuvre_price =  main_oeuvre_price * 2.25
    elif limites_hauteur == "soussoul+3etage":
	    main_oeuvre_price =  main_oeuvre_price * 2.66
    elif limites_hauteur == "soussoul+4etage":
	    main_oeuvre_price =  main_oeuvre_price * 3
    elif limites_hauteur == "soussoul+5etage":
	    main_oeuvre_price =  main_oeuvre_price * 3.5
    elif limites_hauteur == "soussoul+6etage":
	    main_oeuvre_price =  main_oeuvre_price * 3.8
    return main_oeuvre_price

def second_oeuvre(second_oeuvre_list, surface, limites_hauteur):
    second_oeuvre_price = 0
    for second_1 in second_oeuvre_list[:-4]:
    	        second_oeuvre_price += second_1 * surface
    for second_2 in second_oeuvre_list[-4:]:
    	        second_oeuvre_price += second_2
    if limites_hauteur == "fondation":
	    second_oeuvre_price =  second_oeuvre_price * 0.25
    elif limites_hauteur == "rdc":
	    second_oeuvre_price =  second_oeuvre_price * 1
    elif limites_hauteur == "r+1etage":
	    second_oeuvre_price =  second_oeuvre_price * 1.4
    elif limites_hauteur == "r+2etage":
	    second_oeuvre_price =  second_oeuvre_price * 1.83
    elif limites_hauteur == "r+3etage":
	    second_oeuvre_price =  second_oeuvre_price * 2.25
    elif limites_hauteur == "r+4etage":
	    second_oeuvre_price =  second_oeuvre_price * 2.66
    elif limites_hauteur == "r+5etage":
	    second_oeuvre_price =  second_oeuvre_price * 3
    elif limites_hauteur == "r+6etage":
	    second_oeuvre_price =  second_oeuvre_price * 3.5
    elif limites_hauteur == "soussoul+r":
	    second_oeuvre_price =  second_oeuvre_price * 1.4
    elif limites_hauteur == "soussoul+1etage":
	    second_oeuvre_price =  second_oeuvre_price * 1.83
    elif limites_hauteur == "soussoul+2etage":
	    second_oeuvre_price =  second_oeuvre_price * 2.25
    elif limites_hauteur == "soussoul+3etage":
	    second_oeuvre_price =  second_oeuvre_price * 2.66
    elif limites_hauteur == "soussoul+4etage":
	    second_oeuvre_price =  second_oeuvre_price * 3
    elif limites_hauteur == "soussoul+5etage":
	    second_oeuvre_price =  second_oeuvre_price * 3.5
    elif limites_hauteur == "soussoul+6etage":
	    second_oeuvre_price =  second_oeuvre_price * 3.8
    return second_oeuvre_price
	
	
# Initialize x with a default value
@app.route('/')
def index():
    x = 0 
    return render_template('index.html', x=x)
@app.route('/blog')
def blog():
    return render_template('blog.html')
@app.route('/article1')
def article1():
    return render_template('article1.html')
@app.route('/article2')
def article2():
    return render_template('article2.html')
@app.route('/article3')
def article3():
    return render_template('article3.html')
@app.route('/article4')
def article4():
    return render_template('article4.html')
@app.route('/article5')
def article5():
    return render_template('article5.html')
@app.route('/article6')
def article6():
    return render_template('article6.html')
@app.route('/article7')
def article7():
    return render_template('article7.html')
@app.route('/article8')
def article8():
    return render_template('article8.html')
@app.route('/download_invoice', methods=['GET'])
def download_invoice():
    return send_file('invoice.pdf', as_attachment=True)

@app.route('/submit', methods=['POST'])
def contact():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    message = request.form['message']

    conn = sqlite3.connect('./databases/contacts.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO contacts (name, email, phone, message) VALUES (?, ?, ?, ?)''', (name, email, phone, message))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Success'})

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    data = request.json  # Get the data sent from JavaScript
    rating = data.get('rating')
    feedback = data.get('feedback')

    # Store the data in the SQLite database
    conn_review = sqlite3.connect('./databases/reviews.db')
    cursor_review = conn_review.cursor()
    cursor_review.execute('''
        INSERT INTO reviews (rating, feedback) VALUES (?, ?)
    ''', (rating, feedback))
    conn_review.commit()
    conn_review.close()

    return jsonify({'message': 'Feedback received successfully!'})

# Process the form submission
@app.route('/calculate', methods=['POST'])
def calculate():
    if request.method == 'POST':
        data = request.get_json()
        surface = data.get('surface')
        plans = data.get('plans')
        num_facades = data.get('num_facades')
        limites_hauteur = data.get('limites_hauteur')
        type_bien = data.get('type_bien')
        type_Localisation = data.get('type_Localisation')
        zipcode = data.get("zipcode")
        terrain = data.get('terrain')
        zip_code = extract_zipcode(zipcode)
        hauteur_price  = hauteur_to_price(limites_hauteur)
        price1, price2, price3 = get_prices(zip_code, int(surface), int(terrain), hauteur_price)
        price_rent_1, price_rent_2, price_rent_3 = get_rent_prices(zip_code, int(surface), hauteur_price)
        pieces_op, chambre_op = AI_surface_optimisation(int(surface), limites_hauteur)
        update = update_invoice(invoice_data, plans, int(surface), hauteur_price)
        create_invoice(invoice_data, 'invoice.pdf')
        materieux_totale_prince = Materiaux_totale_price(Materiaux_list, int(surface), limites_hauteur, type_bien, type_Localisation, plans)
        materieux_mag = materieux_totale_prince * 1.2
        #print("materieux_totale_prince: ", "de : ", int(materieux_totale_prince), " à : ", int(materieux_mag))
        gros_oeuvre_totale_prince = gros_oeuvre(gros_oeuvre_list, int(surface), limites_hauteur)
        gros_oeuvre_mag = gros_oeuvre_totale_prince * 1.2
        #print("gros_oeuvre_totale_prince: ", "de : ", int(gros_oeuvre_totale_prince), " à : ", int(gros_oeuvre_mag))
        main_oeuvre_totale_prince = main_oeuvre(main_oeuvre_list, int(surface), limites_hauteur)
        main_oeuvre_mag = main_oeuvre_totale_prince * 1.2
        #print("main_oeuvre_totale_prince: ", "de : ", int(main_oeuvre_totale_prince), " à : ", int(main_oeuvre_mag))
        second_oeuvre_totale_prince = second_oeuvre(second_oeuvre_list, int(surface), limites_hauteur)
        second_oeuvre_mag = second_oeuvre_totale_prince * 1.2
        #print("second_oeuvre_totale_prince: ", "de : ", int(second_oeuvre_totale_prince), " à : ", int(second_oeuvre_mag))
        result = {
            'value1': int(main_oeuvre_totale_prince),
            'value2': int(main_oeuvre_mag),
            'value3': int(materieux_totale_prince),
            'value4': int(materieux_mag),
            'value5': int(gros_oeuvre_totale_prince),
            'value6': int(gros_oeuvre_mag),
            'value7': int(second_oeuvre_totale_prince),
            'value8': int(second_oeuvre_mag),
			'value9':int(price1),
			'value10':int(price2),
			'value11':int(price3),
			'value12':str(zipcode),
			'value13':int(price_rent_1),
			'value14':int(price_rent_2),
			'value15':int(price_rent_3),
			'value16':int(pieces_op),
			'value17':int(chambre_op),
			'value18':int(surface)
        }
        return jsonify(result)
    
if __name__ == '__main__':
    app.run(debug=True)
