from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings

from .models import (
    Category, TemplateProduct, Property, PropertyImage, FurnitureProduct, Order
)
from .forms import PropertyForm

# ----------------- AUTHENTIFICATION VIEWS ----------------- #

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        user_obj = User.objects.filter(email__iexact=email).first()
        if user_obj is not None:
            user = authenticate(request, username=user_obj.username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bienvenue {user.first_name or user.username}!")
                return redirect('store:home')
        messages.error(request, "Email ou mot de passe incorrect.")
    return redirect('store:home')

def user_register(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip().split()
        first_name = full_name[0] if full_name else ''
        last_name = " ".join(full_name[1:]) if len(full_name) > 1 else ''
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        
        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, "Cet email est déjà utilisé.")
        else:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            login(request, user)
            messages.success(request, "Votre compte a été créé avec succès!")
    return redirect('store:home')

def user_logout(request):
    logout(request)
    messages.info(request, "Vous êtes déconnecté.")
    return redirect('store:home')

@login_required
def account_settings(request):
    return render(request, 'store/account_settings.html')


# ----------------- PAGES PRINCIPALES ----------------- #

def home(request):
    categories = Category.objects.filter(is_active=True)
    return render(request, 'store/home.html', {'categories': categories})

def category_immobilier(request):
    return render(request, 'store/category_immobilier.html')

def category_mobilier(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category')
        price = request.POST.get('price')
        old_price = request.POST.get('old_price')
        badge_tag = request.POST.get('badge_tag')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        
        FurnitureProduct.objects.create(
            title=title,
            category=category,
            price=price or 0,
            old_price=old_price or None,
            badge_tag=badge_tag,
            description=description,
            image=image
        )
        return redirect('store:demo_luxury_living')
    return render(request, 'store/category_mobilier.html')

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    templates = category.templates.filter(is_active=True)
    return render(request, 'store/category_detail.html', {'category': category, 'templates': templates})

def template_detail(request, slug):
    template_obj = get_object_or_404(TemplateProduct, slug=slug, is_active=True)
    return render(request, 'store/template_detail.html', {'template': template_obj})


# ----------------- DEMOS IMMOBILIER ----------------- #

def demo_modern_estate(request):
    return render(request, 'store/demos/modern_estate/index.html')

def demo_minimal_loft(request):
    return render(request, 'store/demo_minimal_loft.html')

def demo_residence_plus(request):
    if request.method == 'POST':
        Property.objects.create(
            title=request.POST.get('title'),
            city=request.POST.get('city'),
            district=request.POST.get('district'),
            price=request.POST.get('price') or 0,
            price_display=request.POST.get('price_display'),
            property_type=request.POST.get('property_type'),
            badge_status=request.POST.get('badge_status'),
            rooms=request.POST.get('rooms'),
            surface=request.POST.get('surface'),
            feature_tag=request.POST.get('feature_tag'),
            description=request.POST.get('description'),
            image=request.FILES.get('image')
        )
        return redirect('store:demo_residence_plus')
    properties = Property.objects.all().order_by('-id')
    return render(request, 'store/demos/demo_residence_plus.html', {'properties': properties})


# ----------------- DEMOS MOBILIER ----------------- #

def demo_maison_elegante(request):
    return render(request, 'store/demo_maison_elegante.html')

def demo_woodcraft(request):
    return render(request, 'store/demos/demo_woodcraft.html')

def demo_luxury_living(request):
    selected_category = request.GET.get('cat', 'all')
    products = FurnitureProduct.objects.all().order_by('-id')
    if selected_category and selected_category != 'all':
        products = products.filter(category=selected_category)
    context = {
        'products': products,
        'selected_category': selected_category,
    }
    return render(request, 'store/demo_luxury_living.html', context)

def delete_furniture_product(request, pk):
    product = get_object_or_404(FurnitureProduct, pk=pk)
    if request.method == 'POST':
        product.delete()
    return redirect('store:demo_luxury_living')

def nordic_living_demo(request):
    return render(request, 'store/demos/nordic_living.html')


# ----------------- PROPERTIES DETAILS & ADMIN DASHBOARD ----------------- #

def property_list(request):
    properties = Property.objects.all()
    return render(request, 'store/property_list.html', {'properties': properties})

def property_detail(request, pk):
    property_item = get_object_or_404(Property, pk=pk)
    return render(request, 'store/property_detail.html', {'property': property_item})

def admin_dashboard(request):
    properties = Property.objects.all().order_by('-id')
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property_obj = form.save()
            gallery_files = request.FILES.getlist('gallery_images')
            for f in gallery_files:
                PropertyImage.objects.create(property=property_obj, image=f)
            return redirect('store:admin_dashboard')
    else:
        form = PropertyForm()
    return render(request, 'store/admin_dashboard.html', {
        'form': form,
        'properties': properties
    })

def delete_property(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        property_obj.delete()
    return redirect('store:admin_dashboard')


# ----------------- CHECKOUT & ORDERS ----------------- #

PACK_PRICES = {
    'starter': 999,   # Pack Starter
    'pro': 2599,     # Pack Pro
    'elite': 8999,    # Pack Elite
}

def checkout_pack(request, pack_type):
    if pack_type not in PACK_PRICES:
        return redirect('store:home')
        
    price = PACK_PRICES[pack_type]

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        domain_name = request.POST.get('domain_name', '').strip()
        template_choice = request.POST.get('template_choice', '').strip()

        # التسجيل مع الطلب إذا كان المستخدم متصلاً، أو كزائر بـ None
        user_obj = request.user if request.user.is_authenticated else None

        order = Order.objects.create(
            user=user_obj,
            full_name=full_name,
            email=email,
            phone=phone,
            domain_name=domain_name,
            template_choice=template_choice,
            pack_type=pack_type,
            amount=price,
            payment_status='pending'
        )

        admin_subject = f"🚨 Nouvelle Commande #{order.id} - {full_name}"
        admin_message = f"""
Nouveau message d'achat sur ZAYRO:
----------------------------------
Commande ID: #{order.id}
Client: {full_name}
Email: {email}
Téléphone: {phone}
Pack: {pack_type.upper()} ({price} DH)
Modèle choisi: {template_choice}
Domaine souhaité: {domain_name}
"""

        client_subject = f"Confirmation de votre commande #{order.id} — ZAYRO"
        client_message = f"""
Bonjour {full_name},

Nous avons bien enregistré votre commande sur ZAYRO !

Détails de votre commande :
----------------------------------
- Référence : #{order.id}
- Pack : {pack_type.title()}
- Modèle choisi : {template_choice}
- Montant Total : {price} DH
- Acompte pour démarrage : 200 DH

Pour lancer l'installation de votre site, merci de régler l'acompte de 200 DH.

L'équipe ZAYRO vous remercie pour votre confiance !
"""

        try:
            send_mail(
                admin_subject,
                admin_message,
                getattr(settings, 'DEFAULT_FROM_EMAIL', 'zayroshop05@gmail.com'),
                ['zayroshop05@gmail.com'],
                fail_silently=False,
            )
            if email:
                send_mail(
                    client_subject,
                    client_message,
                    getattr(settings, 'DEFAULT_FROM_EMAIL', 'zayroshop05@gmail.com'),
                    [email],
                    fail_silently=False,
                )
        except Exception as e:
            print(f"Erreur d'envoi d'email: {e}")

        return redirect('store:order_confirmation', order_id=order.id)

    context = {
        'pack_type': pack_type,
        'price': price,
    }
    return render(request, 'store/checkout.html', context)

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'store/order_confirmation.html', {'order': order})