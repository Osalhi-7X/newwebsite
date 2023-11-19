from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def invoices_data():
    invoice_data = {
    'invoice_number': 'INV001',
    'invoice_date': '2023-10-29',
    'due_date': '2023-11-29',
    'customer_name': 'John Doe',
    'tables': [
        {
            'table_title': 'Réalisation des plans',
            'table_data': [
                ['Plans de maison', 'Description', 'Montant HT', 'TVA', 'Montant TTC'],
                ['Plan 1', 'Sample description', 100, 10, 110],  # Sample row of data
            ]
        },
        {
            'table_title': 'Travaux de terrassement',
            'table_data': [
                ['Réalisations', 'Description', 'PU', 'Montant'],
                ['Repérage et piquetage du terrain',' ', ' ', 40],
                ['Nivellement de terrain', 'Aplanissement d’un terrain accidenté', '10 €/m2', 30],
                ['Tranchée épaisse', '70 cm de profondeur/40 cm de largeur', '10 €/ml', 45],
                ['Tranchée étroite', 'Pose de câble', '3 €/ml', 50],
                ['Fouille en masse', 'Création de fossé, chargement compris', '10 €/m3', 60],
                ['Fouille manuelle', 'Fouille en terrain meuble', '43 €/m3', 70],
                ['Déblai', 'Extraction des terres excédentaires', '15 €/m3', 80],
                ['Remblai terre', 'Rembourrage du terrain', ' ', 90],
                ['Remblai sable', 'Rembourrage du terrain, apport de sable compris', '30 €/m3', 100],
                ['Enrochement', 'Mur de soutènement en cas de terrain en pente ou cours d’eau', '50 €/tonne', 110],
                ['Sous-Total HT', ' ', ' ', 120],
                ['TVA (20 %)', ' ', ' ', 130],
                ['Sous-Total TTC', ' ', ' ', 140],
            ]
        },
        {
            'table_title': 'Réalisation des fondations',
            'table_data': [
                ['Réalisations', 'Description', 'PU', 'Montant'],
                ['Fondations profondes', 'Au-delà de 6 ou 7 m, il faut aller chercher le sol dur à 10 ou 12 m en utilisant des pieux et non des semelles', '200 €/m3', 50],
                ['Béton', ' ', '150 €/m3', 60],
                ['Coffrage', ' ', '50 €/m2', 70],
                ['Plancher béton', ' ', '90 €/m2', 80],
                ['Chape de ciment', ' ', '60 €/m2', 90],
                ['Construction mur parpaing', ' ', '20 €/m2', 100],
                ['Mur en agglo de ciment creux', ' ', '40€/m2', 110],
                ['Cloison en plaque de plâtre simple', ' ', '35€/m2', 120],
                ['Sous-Total HT', ' ', ' ', 130],
                ['TVA (20 %)', ' ', ' ', 140],
                ['Sous-Total TTC', ' ', ' ', 150],
            ]
        },
        {
            'table_title': 'Charpente et Toiture',
            'table_data': [
                ['Réalisations', 'Description', 'PU', 'Montant'],
                ['Charpente traditionnelle', 'Adapté à tous les modèles architecturaux et facilite l’aménagement des combles', '250€/m2', 60],
                ['Main d’œuvre', 'Installation charpente', '120€/m2', 80],
                ['Couverture toiture en tuiles', ' ', '55€/m2', 70],
                ['Sous-Total HT', ' ', ' ', 50],
                ['TVA (20 %)', ' ', ' ', 40],
                ['Sous-Total TTC', ' ',' ', 30],
            ]
        },
        {
            'table_title': 'Isolation',
            'table_data': [
                ['Réalisations', 'PU Fourniture', 'Main d’œuvre', 'Montant'],
                ['Isolation des murs par l’intérieur', '30 €/m2', '60 €/m2', 30],
                ['Isolation des combles', '30 €/m2', '45 €/m2', 40],
                ['Sous-Total HT', ' ', ' ', 50],
                ['TVA (20 %)', ' ', ' ', 60],
                ['Sous-Total TTC', ' ', ' ', 70],
            ]
        },
        {
            'table_title': 'Installations électriques et plomberie',
            'table_data': [
                ['Réalisations', 'PU Fourniture', 'Main d’œuvre', 'Montant'],
                ['Coffret de raccordement extérieur à encastrer', 20, 30, 50],
                ['Coffrets pré-équipés', 25, 35, 60],
                ['Interrupteur différentiel', '70 à 300 €', '80 à 350 €', 70],
                ['Coupe-circuit domestique', 35, 45, 80],
                ['Prise murale', '30 €/unité', 50, 90],
                ['Point lumineux', '40 €/ unité', 55, 100],
                ['Branchement alimentation', '20€/ml', '50€/m2', 110],
                ['Raccordement d’évacuation en cuivre', '50€/ml', '70€/m2', 120],
                ['Robinetterie pour machine à laver', '30 €/unité', 70, 130],
                ['Robinetterie salle de bain', 65, 75, 140],
                ['Robinetterie chasse d’eau WC', 70, 80, 150],
                ['Robinetterie pour lavabo et éviers', 75, 85, 160],
                ['Raccordement au compteur d’eau', '5 €/ml', '20€/ml', 170],
                ['Sous-Total HT', ' ', ' ', 180],
                ['TVA (20 %)', ' ', ' ', 190],
                ['Sous-Total TTC', ' ', ' ', 200],
            ]
        },
        {
            'table_title': 'Menuiseries',
            'table_data': [
                ['Réalisations', 'PU Fournitures', 'Main d’œuvre', 'Quantité', 'Montant'],
                ['Porte d’entrée en aluminium', '900€/unité', 1200, 5, 150],
                ['Portes intérieures', '600 €/unité', 500, 3, 120],
                ['Fenêtre aluminium', '400 €/unité', 500, 8, 320],
                ['Volets en bois', '400 €/unité', 400, 7, 245],
                ['Sous-Total HT', ' ', ' ', ' ', 160],
                ['TVA (20 %)', ' ', ' ', ' ', 270],
                ['Sous-Total TTC', ' ', ' ', ' ', 450],
            ]
        },
        {
            'table_title': 'Coûts des travaux par rubrique',
            'table_data': [
                ['Rubrique', 'Sous-Total HT', 'TVA', 'Sous-Total TTC'],
                ['Terrassement', 500, 50, 550],
                ['Fondations', 600, 60, 660],
                ['Charpente et toiture', 700, 70, 770],
                ['Isolation', 800, 80, 880],
                ['Electricité et plomberie', 900, 90, 990],
                ['Menuiseries', 1000, 100, 1100],
            ]
        },
        {
            'table_title': 'Devis Travaux (montant total)',
            'table_data': [
                ['TOTAL HT', 10],
                ['TVA', 10],
                ['TOTAL TTC', 20],
            ]
        },

    ]
}
    return invoice_data

def update_invoice(invoice_data, plans, surface, hauteur_price):
	for table in invoice_data['tables']:
		if table['table_title'] == 'Réalisation des plans':
			for row in table['table_data'][1:]:
					# Update the values in the row by multiplying with the variable s
					if plans == "plan_simple":
						row[0] = "Plan simple"
						row[1] = "Coupe et façade issues d’un catalogue"
						row[2] =  surface * 2 * hauteur_price
					elif plans == "plan_standard":
						row[0] = "Plan standard"
						row[1] = "Plan complet pour dépôt permis de construire"
						row[2] = surface * 10 * hauteur_price
					elif plans == "plan_sur_mesure":
						row[0] = "Plan sur mesure"
						row[1] = "Plan sur mesure et aide à la demande de permis de construire"
						row[2] =  surface * 12 * hauteur_price
					elif plans == "plan_architecte":
						row[0] = "Plan architecte"
						row[1] = "Plan en détails, accompagnement personnalisé pour constitution dossier de demande de permis de construire"
						row[2] = surface * 25 * hauteur_price
					row[3] = '20%'  # TVA
					row[4] = row[2] * 1.2  # Montant TTC
		elif table['table_title'] == 'Travaux de terrassement':
			tera_tot = 0
			tera_sub_tot = 0
			for row in table['table_data'][1:]:
				if row[0] == 'Repérage et piquetage du terrain':
					row[3] = surface * 20
					tera_tot += row[3]
				elif row[0] == 'Nivellement de terrain':
					row[3] = surface * 10
					tera_tot += row[3]
				elif row[0] == 'Tranchée épaisse':
					row[3] = surface * 10
					tera_tot += row[3]
				elif row[0] == 'Tranchée étroite':
					row[3] = surface * 3
					tera_tot += row[3]
				elif row[0] == 'Fouille en masse':
					row[3] = surface * 10 * 0.2
					tera_tot += row[3]
				elif row[0] == 'Fouille manuelle':
					row[3] = surface * 43 * 0.2
					tera_tot += row[3]
				elif row[0] == 'Déblai':
					row[3] = surface * 15 * 0.2
					tera_tot += row[3]
				elif row[0] == 'Remblai terre':
					row[3] = surface * 1.54 * hauteur_price
					tera_tot += row[3]
				elif row[0] == 'Remblai sable':
					row[3] = surface * 30 * 0.1 * hauteur_price
					tera_tot += row[3]
				elif row[0] == 'Enrochement':
					row[3] = surface * 50 * 0.3
					tera_tot += row[3]
				elif row[0] == 'Sous-Total HT':
					row[3] = round(tera_tot, 2)
					tera_sub_tot = row[3]
				elif row[0] == 'TVA (20 %)':
					row[3] = round(tera_tot * 0.2, 2)
				elif row[0] == 'Sous-Total TTC':
					row[3] = round(tera_tot * 1.2, 2)
		elif table['table_title'] == 'Réalisation des fondations':
			fon_tot = 0
			fon_sub_tot = 0
			for row in table['table_data'][1:]:
				if row[0] == 'Fondations profondes':
					row[3] = surface * 200
					fon_tot += row[3]
				elif row[0] == 'Béton':
					row[3] = surface * 150 * hauteur_price
					fon_tot += row[3]
				elif row[0] == 'Coffrage':
					row[3] = surface * 50 * hauteur_price
					fon_tot += row[3]
				elif row[0] == 'Plancher béton':
					row[3] = surface * 90 * hauteur_price
					fon_tot += row[3]
				elif row[0] == 'Chape de ciment':
					row[3] = surface * 60 * hauteur_price
					fon_tot += row[3]
				elif row[0] == 'Construction mur parpaing':
					row[3] = surface * 20 * hauteur_price
					fon_tot += row[3]
				elif row[0] == 'Mur en agglo de ciment creux':
					row[3] = surface * 40 * hauteur_price
					fon_tot += row[3]
				elif row[0] == 'Cloison en plaque de plâtre simple':
					row[3] = surface * 35 * hauteur_price
					fon_tot += row[3]
				elif row[0] == 'Sous-Total HT':
					row[3] = round(fon_tot, 2)
					fon_sub_tot =  row[3]
				elif row[0] == 'TVA (20 %)':
					row[3] = round(fon_tot * 0.2, 2)
				elif row[0] == 'Sous-Total TTC':
					row[3] = round(fon_tot * 1.2, 2)
		elif table['table_title'] == 'Charpente et Toiture':
			Charp_tot = 0
			Charp_sub_tot = 0
			for row in table['table_data'][1:]:
				if row[0] == 'Charpente traditionnelle':
					row[3] = surface * 250
					Charp_tot += row[3]
				elif row[0] == 'Main d’œuvre':
					row[3] = surface * 120
					Charp_tot += row[3]
				elif row[0] == 'Couverture toiture en tuiles':
					row[3] = surface * 55
					Charp_tot += row[3]
				elif row[0] == 'Sous-Total HT':
					row[3] = round(Charp_tot, 2)
					Charp_sub_tot = row[3]
				elif row[0] == 'TVA (20 %)':
					row[3] = round(Charp_tot * 0.2, 2)
				elif row[0] == 'Sous-Total TTC':
					row[3] = round(Charp_tot * 1.2, 2)
		elif table['table_title'] == 'Isolation':
			Iso_tot = 0
			Iso_sub_tot = 0
			for row in table['table_data'][1:]:
				if row[0] == 'Isolation des murs par l’intérieur':
					row[3] = surface * 90 * hauteur_price
					Iso_tot += row[3]
				elif row[0] == 'Isolation des combles':
					row[3] = surface * 75 * hauteur_price
					Iso_tot += row[3]
				elif row[0] == 'Sous-Total HT':
					row[3] = round(Iso_tot, 2)
					Iso_sub_tot = row[3]
				elif row[0] == 'TVA (20 %)':
					row[3] = round(Iso_tot * 0.2, 2)
				elif row[0] == 'Sous-Total TTC':
					row[3] = round(Iso_tot * 1.2, 2)
		elif table['table_title'] == 'Installations électriques et plomberie':
			plo_tot = 0
			plo_sub_tot = 0
			for row in table['table_data'][1:]:
				if row[0] == 'Coffret de raccordement extérieur à encastrer':
					row[1] = round(surface * 3.5 * hauteur_price,2)
					row[2] = round(surface * 3 * hauteur_price,2)
					row[3] = row[1] + row[2]
					plo_tot += row[3]
				elif row[0] == 'Coffrets pré-équipés':
					row[1] = surface * 4 * hauteur_price
					row[2] = surface * 2.5 * hauteur_price
					row[3] = row[1] + row[2] 
					plo_tot += row[3]
				elif row[0] == 'Interrupteur différentiel':
					row[3] = surface * 1.5 * hauteur_price
					plo_tot += row[3]
				elif row[0] == 'Coupe-circuit domestique':
					row[1] = surface * 0.2 * hauteur_price
					row[2] = surface * 0.25 * hauteur_price
					row[3] = row[1] + row[2] 
					plo_tot += row[3]
				elif row[0] == 'Prise murale':
					row[3] = surface * 2.5 + 30 * 10 * hauteur_price
					plo_tot += row[3]
				elif row[0] == 'Point lumineux':
					row[3] = surface * 3 + 40 * 10 * hauteur_price
					plo_tot += row[3]
				elif row[0] == 'Branchement alimentation':
					row[3] = surface * 70 * hauteur_price
					plo_tot += row[3]
				elif row[0] == 'Raccordement d’évacuation en cuivre':
					row[3] = surface * 120 * hauteur_price
					plo_tot += row[3]
				elif row[0] == 'Robinetterie pour machine à laver':
					row[3] = surface * 0.5 + 30 * hauteur_price
					plo_tot += row[3]
				elif row[0] == 'Robinetterie salle de bain':
					row[1] = surface * 3 * hauteur_price
					row[2] = surface * 3.5 * hauteur_price
					row[3] = row[1] + row[2] 
					plo_tot += row[3]
				elif row[0] == 'Robinetterie chasse d’eau WC':
					row[1] = surface * 0.5 * hauteur_price
					row[2] = surface * 1
					plo_tot += row[3]
				elif row[0] == 'Robinetterie pour lavabo et éviers':
					row[1] = surface * 1.5 * hauteur_price
					row[2] = surface * 2 * hauteur_price
					row[3] = row[1] + row[2] 
					plo_tot += row[3]
				elif row[0] == 'Raccordement au compteur d’eau':
					row[3] = surface * 25 * hauteur_price
					plo_tot += row[3]
				elif row[0] == 'Sous-Total HT':
					row[3] = round(plo_tot, 2)
					plo_sub_tot =  row[3]
				elif row[0] == 'TVA (20 %)':
					row[3] = round(plo_tot * 0.2, 2)
				elif row[0] == 'Sous-Total TTC':
					row[3] = round(plo_tot * 1.2, 2)
		elif table['table_title'] == 'Menuiseries':
			Men_tot = 0
			Men_sub_tot = 0
			for row in table['table_data'][1:]:
				if row[0] == 'Porte d’entrée en aluminium':
					row[3] = surface * 0.02
					row[4] = (900 + 2100) * row[3]
					Men_tot += row[4]
				elif row[0] == 'Portes intérieures':
					row[3] = surface * 0.1 * hauteur_price
					row[4] = (600 + 500) * row[3]
					Men_tot += row[4]
				elif row[0] == 'Fenêtre aluminium':
					row[3] = surface * 0.1 * hauteur_price
					row[4] = (400 + 500) * row[3]
					Men_tot += row[4]
				elif row[0] == 'Volets en bois':
					row[3] = surface * 0.1 * hauteur_price
					row[4] = (400 + 400) * row[3]
					Men_tot += row[4]
				elif row[0] == 'Sous-Total HT':
					row[4] = round(Men_tot, 2)
					Men_sub_tot = row[4]
				elif row[0] == 'TVA (20 %)':
					row[4] = round(Men_tot * 0.2, 2)
				elif row[0] == 'Sous-Total TTC':
					row[4] = round(Men_tot * 1.2, 2)
		elif table['table_title'] == 'Coûts des travaux par rubrique':
			TV_tot = 0
			for row in table['table_data'][1:]:
				if row[0] == 'Terrassement':
					row[1] = round(tera_sub_tot, 2)
					TV_tot += row[1]
					row[2] = round(tera_sub_tot * 0.2, 2)
					row[3] = round(tera_sub_tot * 1.2, 2)
				elif row[0] == 'Fondations':
					row[1] = round(fon_sub_tot, 2)
					TV_tot += row[1]
					row[2] = round(fon_sub_tot * 0.2, 2)
					row[3] = round(fon_sub_tot * 1.2, 2)
				elif row[0] == 'Charpente et toiture':
					row[1] = round(Charp_sub_tot, 2)
					TV_tot += row[1]
					row[2] = round(Charp_sub_tot * 0.2, 2)
					row[3] = round(Charp_sub_tot * 1.2, 2)
				elif row[0] == 'Isolation':
					row[1] = round(Iso_sub_tot, 2)
					TV_tot += row[1]
					row[2] = round(Iso_sub_tot * 0.2)
					row[3] = round(Iso_sub_tot * 1.2)
				elif row[0] == 'Electricité et plomberie':
					row[1] = plo_sub_tot
					TV_tot += row[1]
					row[2] = round(plo_sub_tot * 0.2)
					row[3] = round(plo_sub_tot * 1.2, 2)
				elif row[0] == 'Menuiseries':
					row[1] = round(Men_sub_tot, 2)
					TV_tot += row[1]
					row[2] = round(Men_sub_tot * 0.2, 2)
					row[3] = round(Men_sub_tot * 1.2, 2)
		elif table['table_title'] == 'Devis Travaux (montant total)':
			for row in table['table_data']:
				if row[0] == 'TOTAL HT':
					row[1] = round(TV_tot, 2)
				elif row[0] == 'TVA':
					row[1] = round(TV_tot*0.2, 2)
				elif row[0] == 'TOTAL TTC':
					row[1] = round(TV_tot * 1.2, 2)
	return invoice_data


# Create a PDF invoice for the first, second, third, fourth, fifth, sixth, seventh, eighth, and ninth tables
def create_invoice(invoice_data, pdf_filename):
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    story = []

    styles = getSampleStyleSheet()

    # Invoice header
    story.append(Paragraph('Invoice', styles['Heading1']))
    story.append(Spacer(1, 12))
    story.append(Paragraph('Invoice Number: {}'.format(invoice_data['invoice_number'])))
    story.append(Paragraph('Invoice Date: {}'.format(invoice_data['invoice_date'])))
    story.append(Paragraph('Due Date: {}'.format(invoice_data['due_date'])))
    story.append(Spacer(1, 12))
    story.append(Paragraph('Bill To:', styles['Normal']))
    story.append(Paragraph(invoice_data['customer_name'], styles['Normal']))
    story.append(Spacer(1, 12))

    # Invoice tables
    for table_info in invoice_data['tables']:
        table_title = table_info['table_title']
        table_data = table_info['table_data']

        story.append(Paragraph(table_title, styles['Normal']))

        data = []

        # Add the table header with column names
        data.append([Paragraph(str(cell), styles['Normal']) for cell in table_data[0]])

        # Add the table data with long text wrapped within table cells
        for row in table_data[1:]:
            row_data = []
            for cell in row:
                if isinstance(cell, str):
                    if len(cell) > 30:
                        # Allow text to wrap within the cell
                        cell_style = styles['Normal'].clone('table.cell')
                        cell_style.wordWrap = 'CJK'
                        cell_style.leading = 8
                        row_data.append(Paragraph(cell, cell_style))
                    else:
                        row_data.append(Paragraph(cell, styles['Normal']))
                else:
                    row_data.append(Paragraph(str(cell), styles['Normal']))
            data.append(row_data)

        t = Table(data, colWidths=[2 * inch, 2.5 * inch, 1 * inch, 1 * inch, 1 * inch])
        t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                              ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                              ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                              ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                              ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                              ('BACKGROUND', (0, 1), (-1, 1), colors.beige),
                              ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

        story.append(t)
        story.append(Spacer(1, 12))

    # Invoice totals
    doc.build(story)

# Generate the invoice and save it as a PDF
#create_invoice(invoice_data, 'invoice.pdf')