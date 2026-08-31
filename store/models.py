from django.db import models
from django.utils.text import slugify
from django.conf import settings

# 1️⃣ Category Model
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.CharField(max_length=50, help_text="Emoji ula FontAwesome icon (e.g. 🏠)")
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# 2️⃣ TemplateProduct Model
class TemplateProduct(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='templates')
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    
    price_template_only = models.DecimalField(max_digits=8, decimal_places=2, default=799.00)
    price_ready_to_use = models.DecimalField(max_digits=8, decimal_places=2, default=1199.00)
    
    demo_url = models.CharField(max_length=200, help_text="Nom de la vue Django (ex: store:demo_luxury_living)")
    thumbnail = models.ImageField(upload_to='templates/thumbnails/')
    
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# 3️⃣ Property Model
class Property(models.Model):
    STATUS_CHOICES = [
        ('LIVRABLE', 'Livrable Immédiatement'),
        ('OFF_MARKET', 'Lancement Off-Market'),
        ('INVESTISSEMENT', 'Investissement Pro'),
    ]

    PROPERTY_TYPES = [
        ('Appartement', 'Appartement Haut Standing'),
        ('Villa', 'Villa Moderne / Luxe'),
        ('Bureaux', 'Bureaux & Commerces'),
    ]

    title = models.CharField(max_length=200, verbose_name="Titre du projet")
    badge_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='LIVRABLE')
    city = models.CharField(max_length=100, default="Casablanca", help_text="Ex: Casablanca, Rabat")
    district = models.CharField(max_length=100, default="Anfa", help_text="Ex: Anfa, Souissi, CFC")
    
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Prix en DH (Ex: 2400000)")
    price_display = models.CharField(max_length=50, help_text="Ex: À partir de 2.4 MDH ou Sur Devis Pro")
    
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES, default='Appartement')
    description = models.TextField()
    
    rooms = models.CharField(max_length=50, help_text="Ex: 2-4 Ch. ou 5 Ch.")
    surface = models.CharField(max_length=50, help_text="Ex: 82-185 m²")
    feature_tag = models.CharField(max_length=50, help_text="Ex: Piscine, Jardin, Parking 3N")
    
    image = models.ImageField(upload_to='properties/', blank=True, null=True, verbose_name="Image Principale")
    pdf_brochure = models.FileField(upload_to='brochures/', blank=True, null=True, verbose_name="Brochure PDF")
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Properties"

    def __str__(self):
        return f"{self.title} - {self.city}"


# 4️⃣ PropertyImage Model
class PropertyImage(models.Model):
    property = models.ForeignKey(
        Property, 
        on_delete=models.CASCADE, 
        related_name='gallery_images'
    )
    image = models.ImageField(upload_to='properties/gallery/')
    caption = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Image pour {self.property.title}"


# 5️⃣ FurnitureProduct Model
class FurnitureProduct(models.Model):
    CATEGORY_CHOICES = [
        ('salons', 'Salons & Canapés'),
        ('tables', 'Tables & Chaises'),
        ('luminaires', 'Luminaires'),
        ('deco', 'Décoration & Accessoires'),
    ]

    title = models.CharField(max_length=200, verbose_name="Nom du produit")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='salons', verbose_name="Catégorie")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix (DH)")
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Ancien Prix (Optionnel)")
    badge_tag = models.CharField(max_length=50, blank=True, null=True, help_text="Ex: Top Vente, Sur-Mesure, Promo", verbose_name="Badge / Tag")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    image = models.ImageField(upload_to='furniture/', blank=True, null=True, verbose_name="Image du produit")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.price} DH"


# 6️⃣ Product Model (Cart/Session)
class Product(models.Model):
    session_key = models.CharField(max_length=40, blank=True, null=True, db_index=True)
    title = models.CharField(max_length=200, verbose_name="Titre du Produit")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix (DH)")
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Ancien Prix (DH)")
    
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Image Principale")
    image_secondary = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Image Secondaire")
    
    badge_tag = models.CharField(max_length=50, blank=True, null=True, verbose_name="Badge (ex: PROMO, NEW)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# 7️⃣ Order Model
class Order(models.Model):
    PACK_CHOICES = (
        ('starter', 'Starter'),
        ('pro', 'Pro'),
        ('elite', 'Elite'),
    )

    STATUS_CHOICES = (
        ('pending', 'En attente'),
        ('paid', 'Payé'),
        ('cancelled', 'Annulé'),
    )

    # التعديل الرئيسي هنا: SET_NULL + null=True + blank=True باش الزائر يدوز الطلب بلا حساب
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        related_name='orders', 
        null=True, 
        blank=True
    )
    full_name = models.CharField(max_length=150, verbose_name="Nom Complet")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Téléphone / WhatsApp")
    domain_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Domaine souhaité")
    template_choice = models.CharField(max_length=100, blank=True, null=True, verbose_name="Modèle choisi")
    
    pack_type = models.CharField(max_length=20, choices=PACK_CHOICES, verbose_name="Type de Pack")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant (DH)")
    payment_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Statut du paiement")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.full_name}"