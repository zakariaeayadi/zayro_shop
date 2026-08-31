from django import forms
from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline
from .models import Category, TemplateProduct, Property, PropertyImage, FurnitureProduct

# إعدادات العناوين الخاصة بالـ Admin
admin.site.site_header = "RESIDENCE+ — Administration"
admin.site.site_title = "RESIDENCE+ Admin"
admin.site.index_title = "Gestion des Programmes Immobiliers & Mobilier"

# 📝 Formulaire pour Property
class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = '__all__'
        widgets = {
            'image': forms.ClearableFileInput(attrs={'clear_checkbox_label': "Effacer l'image actuelle"}),
            'pdf_brochure': forms.ClearableFileInput(attrs={'clear_checkbox_label': 'Effacer le PDF actuel'}),
        }


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('name', 'is_active', 'order')
    list_editable = ('is_active', 'order')


@admin.register(TemplateProduct)
class TemplateProductAdmin(ModelAdmin):
    list_display = ('title', 'category', 'price_template_only', 'price_ready_to_use', 'is_featured', 'is_active')
    list_filter = ('category', 'is_featured', 'is_active')
    search_fields = ('title', 'description')


# 📸 Galerie Images (Compatible Unfold)
class PropertyImageInline(TabularInline):
    model = PropertyImage
    extra = 1
    fields = ('image', 'image_preview', 'caption')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 80px; height: 60px; object-fit: cover; border-radius: 6px; border: 1px solid #C59B27;" />', obj.image.url)
        return "Pas d'image"
    
    image_preview.short_description = "Aperçu"


# 🏢 Property Admin
@admin.register(Property)
class PropertyAdmin(ModelAdmin):
    form = PropertyForm
    
    list_display = ('title', 'city', 'district', 'price_display', 'badge_status', 'has_pdf')
    # 👈 صلحت هنا: حيدت 'property_type' حيت ما كايناش فـ Model
    list_filter = ('city', 'badge_status') 
    search_fields = ('title', 'city', 'district')
    
    inlines = [PropertyImageInline]
    
    readonly_fields = ('main_image_preview', 'pdf_preview')

    fieldsets = (
        ('Informations Générales', {
            'fields': ('title', 'badge_status', 'description')
        }),
        ('Localisation & Prix', {
            'fields': ('city', 'district', 'price_display')
        }),
        ('Caractéristiques', {
            'fields': ('rooms', 'surface', 'feature_tag')
        }),
        ('Image Principale', {
            'fields': ('image', 'main_image_preview')
        }),
        ('Brochure PDF', {
            'fields': ('pdf_brochure', 'pdf_preview')
        }),
    )

    def main_image_preview(self, obj):
        if obj.image:
            return format_html(
                '<div style="margin-top: 5px;">'
                '<img src="{}" style="max-width: 180px; height: auto; border-radius: 8px; border: 2px solid #C59B27;" />'
                '</div>', 
                obj.image.url
            )
        return "Aucune image principale"
    main_image_preview.short_description = "Aperçu Image Principale"

    def pdf_preview(self, obj):
        if obj.pdf_brochure:
            return format_html('<a href="{}" target="_blank" style="color: #C59B27; font-weight: bold; text-decoration: underline;">📄 Voir / Télécharger le PDF actuel</a>', obj.pdf_brochure.url)
        return "Aucun PDF"
    pdf_preview.short_description = "Aperçu PDF"

    def has_pdf(self, obj):
        return bool(obj.pdf_brochure)
    has_pdf.boolean = True
    has_pdf.short_description = "Brochure PDF"


# 🛋️ Furniture Product Admin
@admin.register(FurnitureProduct)
class FurnitureProductAdmin(ModelAdmin):
    list_display = ('title', 'category', 'price', 'old_price', 'badge_tag', 'created_at')
    list_filter = ('category', 'badge_tag')
    search_fields = ('title', 'description')
    list_editable = ('price', 'badge_tag')