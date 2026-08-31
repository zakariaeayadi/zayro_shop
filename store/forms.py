from django import forms
from .models import Property

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title', 'description', 'city', 'district', 
            'price_display', 'rooms', 'surface', 'feature_tag', 
            'badge_status', 'image', 'pdf_brochure'  # 👈 تبديل pdf_file بـ pdf_brochure
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full bg-[#0F172A] border border-slate-700 rounded-xl px-4 py-3 text-xs text-white focus:outline-none focus:border-[#C59B27]', 'placeholder': 'Ex: Residence Anfa Park'}),
            'city': forms.TextInput(attrs={'class': 'w-full bg-[#0F172A] border border-slate-700 rounded-xl px-4 py-3 text-xs text-white focus:outline-none focus:border-[#C59B27]', 'placeholder': 'Ex: Casablanca'}),
            'district': forms.TextInput(attrs={'class': 'w-full bg-[#0F172A] border border-slate-700 rounded-xl px-4 py-3 text-xs text-white focus:outline-none focus:border-[#C59B27]', 'placeholder': 'Ex: CFC / Bourgogne'}),
            'price_display': forms.TextInput(attrs={'class': 'w-full bg-[#0F172A] border border-slate-700 rounded-xl px-4 py-3 text-xs text-white focus:outline-none focus:border-[#C59B27]', 'placeholder': 'Ex: À partir de 1.8 MDH'}),
            'rooms': forms.TextInput(attrs={'class': 'w-full bg-[#0F172A] border border-slate-700 rounded-xl px-4 py-3 text-xs text-white focus:outline-none focus:border-[#C59B27]', 'placeholder': 'Ex: 2 à 4 ch.'}),
            'surface': forms.TextInput(attrs={'class': 'w-full bg-[#0F172A] border border-slate-700 rounded-xl px-4 py-3 text-xs text-white focus:outline-none focus:border-[#C59B27]', 'placeholder': 'Ex: 85 - 140 m²'}),
            'feature_tag': forms.TextInput(attrs={'class': 'w-full bg-[#0F172A] border border-slate-700 rounded-xl px-4 py-3 text-xs text-white focus:outline-none focus:border-[#C59B27]', 'placeholder': 'Ex: Piscine / Vue sur mer'}),
            'badge_status': forms.Select(attrs={'class': 'w-full bg-[#0F172A] border border-slate-700 rounded-xl px-4 py-3 text-xs text-white focus:outline-none focus:border-[#C59B27]'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'w-full bg-[#0F172A] border border-slate-700 rounded-xl px-4 py-3 text-xs text-white focus:outline-none focus:border-[#C59B27]'}),
        }