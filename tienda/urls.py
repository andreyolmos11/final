from tienda.forms import LoginForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'tienda'


urlpatterns = [
    path('', views.home, name="home"),
    # CARRITO Y CHECKOUT
    path('agregar-al-carrito/', views.agregar_al_carrito, name="agregar-al-carrito"),
    path('remover-carrito/<int:carrito_id>/', views.remover_carrito, name="remover-carrito"),
    path('plus-carrito/<int:carrito_id>/', views.plus_carrito, name="plus-carrito"),
    path('menos-carrito/<int:carrito_id>/', views.menos_carrito, name="menos-carrito"),
    path('carrito/', views.carrito, name="carrito"),
    path('checkout/', views.checkout, name="checkout"),
    path('ordenes/', views.ordenes, name="ordenes"),

    #PRODUCTOS
    path('producto/<slug:slug>/', views.detalle, name="producto-detalle"),
    path('categorias/', views.todas_categorias, name="todas-categorias"),
    path('<slug:slug>/', views.categoria_productos, name="categoria-productos"),

    path('tienda/', views.tienda, name="tienda"),

    #AUTENTIFICACION
    path('cuenta/registrar/', views.RegistrationView.as_view(), name="registrar"),
    path('cuenta/login/', auth_views.LoginView.as_view(template_name='cuenta/login.html', authentication_form=LoginForm), name="login"),
    path('cuenta/perfil/', views.profile, name="profile"),
    path('cuenta/agregar-direccion/', views.AddressView.as_view(), name="add-address"),
    path('cuenta/remover-direccion/<int:id>/', views.remove_address, name="remove-address"),
    path('cuenta/logout/', auth_views.LogoutView.as_view(next_page='store:login'), name="logout"),

    path('cuenta/password-change/', auth_views.PasswordChangeView.as_view(template_name='cuenta/password_change.html', form_class=PasswordChangeForm, success_url='/cuenta/password-change-done/'), name="password-change"),
    path('cuenta/password-change-done/', auth_views.PasswordChangeDoneView.as_view(template_name='cuenta/password_change_done.html'), name="password-change-done"),

    path('cuenta/password-reset/', auth_views.PasswordResetView.as_view(template_name='cuenta/password_reset.html', form_class=PasswordResetForm, success_url='/cuenta/password-reset/done/'), name="password-reset"), # Passing Success URL to Override default URL, also created password_reset_email.html due to error from our app_name in URL
    path('cuenta/password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='cuenta/password_reset_done.html'), name="password_reset_done"),
    path('cuenta/password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='cuenta/password_reset_confirm.html', form_class=SetPasswordForm, success_url='/cuenta/password-reset-complete/'), name="password_reset_confirm"), # Passing Success URL to Override default URL
    path('cuenta/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='cuenta/password_reset_complete.html'), name="password_reset_complete"),

    path('producto/prueba/', views.test, name="prueba"),

    
]
