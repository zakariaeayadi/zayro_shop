from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    
    # --- AUTHENTIFICATION ROUTES ---
    path('auth/login/', views.user_login, name='login'),
    path('auth/register/', views.user_register, name='register'),
    path('auth/logout/', views.user_logout, name='logout'),

    # --- CATEGORIES & STORE ---
    path('category/immobilier/', views.category_immobilier, name='category_immobilier'),
    path('category/mobilier/', views.category_mobilier, name='category_mobilier'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    
    # --- ADMIN DASHBOARD ---
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/admin/delete/<int:pk>/', views.delete_property, name='delete_property'),

    # --- DEMOS IMMOBILIER ---
    path('template/residence-plus/', views.demo_residence_plus, name='demo_residence_plus'),
    path('demo/residence-plus/', views.demo_residence_plus, name='demo_residence_plus'),
    path('demo/modern-estate/', views.demo_modern_estate, name='demo_modern_estate'),
    path('demo/minimal-loft/', views.demo_minimal_loft, name='demo_minimal_loft'),
    
    # --- DEMOS MOBILIER ---
    path('demo/maison-elegante/', views.demo_maison_elegante, name='demo_maison_elegante'),
    path('demo/woodcraft/', views.demo_woodcraft, name='demo_woodcraft'),
    path('demo/luxury-living/', views.demo_luxury_living, name='demo_luxury_living'),
    path('demo/luxury-living/delete/<int:pk>/', views.delete_furniture_product, name='delete_furniture_product'),
    path('demo/nordic-living/', views.nordic_living_demo, name='nordic_living_demo'),

    # --- PROPERTIES & TEMPLATES DB ---
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('template/<slug:slug>/', views.template_detail, name='template_detail'),  
    path('account/settings/', views.account_settings, name='account_settings'),
    path('checkout/<str:pack_type>/', views.checkout_pack, name='checkout_pack'),
    path('order/confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
]