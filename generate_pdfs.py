import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Dossier d'enregistrement : store/static/store/pdf/
OUTPUT_DIR = os.path.join('store', 'static', 'store', 'pdf')
os.makedirs(OUTPUT_DIR, exist_ok=True)

def create_admin_pdf(filename, category_title, is_immobilier):
    pdf_path = os.path.join(OUTPUT_DIR, filename)
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    
    # Palette ZAYRO (Dark Slate & Gold)
    dark_slate = colors.HexColor("#0f172a")
    gold_color = colors.HexColor("#eab308")
    dark_gray  = colors.HexColor("#334155")

    title_style = ParagraphStyle(
        'DocTitle', parent=styles['Heading1'],
        fontName='Helvetica-Bold', fontSize=20,
        textColor=gold_color, spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle', parent=styles['Normal'],
        fontName='Helvetica', fontSize=10,
        textColor=dark_slate, spaceAfter=10
    )

    h2_style = ParagraphStyle(
        'SectionHeader', parent=styles['Heading2'],
        fontName='Helvetica-Bold', fontSize=12,
        textColor=dark_slate, spaceBefore=12, spaceAfter=6
    )

    body_style = ParagraphStyle(
        'BodyTextCustom', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9,
        textColor=dark_gray, leading=13, spaceAfter=6
    )

    story = []

    # Header / Title Block
    story.append(Paragraph("ZAYRO .", title_style))
    story.append(Paragraph(f"Catégorie : {category_title} &nbsp;|&nbsp; GUIDE D'UTILISATION DASHBOARD ADMIN", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=gold_color, spaceAfter=15))

    # Section 1: Intro
    story.append(Paragraph("1. PRÉSENTATION DU DASHBOARD ADMIN", h2_style))
    if is_immobilier:
        intro = "Ce panneau d'administration vous permet de gérer entièrement le catalogue immobilier : ajouter de nouveaux biens (Villas, Appartements), gérer la disponibilité, ajouter des visuels et joindre des brochures PDF destinées aux clients."
    else:
        intro = "Ce panneau d'administration vous permet de gérer entièrement le catalogue de mobilier : ajouter de nouveaux meubles (Canapés, Tables, Lits), gérer le stock, ajouter des visuels et joindre des fiches techniques PDF."
    story.append(Paragraph(intro, body_style))

    # Section 2: Champs
    story.append(Paragraph("2. GUIDE DES CHAMPS DU FORMULAIRE", h2_style))
    if is_immobilier:
        fields = [
            "• <b>Nom du Bien / Intitulé :</b> Titre de l'annonce (ex: Villa Deluxe Oasis).",
            "• <b>Prix (DH / MDH) :</b> Prix du bien immobilier.",
            "• <b>Ville / Emplacement :</b> Localisation du bien (ex: Rabat, Casablanca).",
            "• <b>Statut / Tag :</b> Disponibilité (ex: LIVRABLE IMMÉDIAT).",
            "• <b>Finition / Type :</b> Niveau de finition (ex: Haute Finition).",
            "• <b>Chambres / Pièces :</b> Nombre de pièces (ex: 4 Ch.).",
            "• <b>Surface / Dimensions :</b> Superficie en m² (ex: 350 m²).",
            "• <b>Description Complète :</b> Caractéristiques (piscine, vue sur mer, etc.).",
            "• <b>Brochure PDF (Optionnel) :</b> Fichier PDF explicatif du bien.",
            "• <b>Photo Principale & Secondaires :</b> Galerie d'images du bien."
        ]
    else:
        fields = [
            "• <b>Nom du Meuble / Article :</b> Titre du produit (ex: Canapé d'Angle Velvet).",
            "• <b>Prix (DH) :</b> Prix de vente unitaire.",
            "• <b>Ville / Emplacement :</b> Showroom ou dépôt de stock (ex: Casablanca).",
            "• <b>Statut / Tag :</b> État du stock (ex: EN STOCK, SUR COMMANDE).",
            "• <b>Finition / Type :</b> Matières et style (ex: Bois Massif, Velours).",
            "• <b>Chambres / Pièces :</b> Destination (ex: Salon, Chambre).",
            "• <b>Surface / Dimensions :</b> Dimensions du meuble (ex: 220x90x85 cm).",
            "• <b>Description Complète :</b> Conseils d'entretien et caractéristiques.",
            "• <b>Fiche Technique PDF (Optionnel) :</b> Catalogue ou guide de montage.",
            "• <b>Photo Principale & Secondaires :</b> Galerie d'images du meuble."
        ]
    
    for f in fields:
        story.append(Paragraph(f, body_style))

    # Section 3: Étapes
    story.append(Paragraph("3. ÉTAPES POUR AJOUTER UNE ENTRÉE", h2_style))
    steps = [
        "1. Remplissez tous les champs obligatoires du formulaire.",
        "2. Ajoutez un document PDF téléchargeable (optionnel).",
        "3. Glissez-déposez la photo principale et les images secondaires.",
        "4. Cliquez sur le bouton '+ Enregistrer' pour valider et publier dans le catalogue."
    ]
    for s in steps:
        story.append(Paragraph(s, body_style))

    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", thickness=1, color=dark_slate, spaceAfter=10))

    # Footer / Contacts
    story.append(Paragraph("<b>SUPPORT TECHNIQUE & ASSISTANCE ZAYRO</b>", ParagraphStyle('FootH', parent=body_style, fontSize=10, textColor=dark_slate)))
    story.append(Paragraph("Pour toute assistance concernant la gestion de votre plateforme ZAYRO :", body_style))
    story.append(Paragraph("• <b>Téléphone / WhatsApp :</b> +212 777 587 034", body_style))
    story.append(Paragraph("• <b>Email Support :</b> zayroshop05@gmail.com", body_style))

    doc.build(story)
    print(f"✅ Fichier PDF généré avec succès : {pdf_path}")

# Executer pour les 2 fichiers
create_admin_pdf("Guide_Utilisation_Admin_Immobilier.pdf", "Immobilier & Agences", is_immobilier=True)
create_admin_pdf("Guide_Utilisation_Admin_Mobilier.pdf", "Mobilier & Meubles", is_immobilier=False)