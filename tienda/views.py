import django
from django.contrib.auth.models import User
from tienda.models import Direccion, Carrito, Categoria, Orden, Producto
from django.shortcuts import redirect, render, get_object_or_404
from .forms import RegistrationForm, AddressForm
from django.contrib import messages
from django.views import View
import decimal
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator 



# Create your views here.
def home(request):
    categorias = Categoria.objects.filter(activo=True, destacado=True)[:4]
    productos = Producto.objects.filter(activo=True, destacado=True)[:12]
    context = {
        'categorias': categorias,
        'productos': productos,
    }
    return render(request, 'tienda/index.html', context)

def detalle(request, slug):
    producto = get_object_or_404(Producto, slug=slug)
    productos_relacionados = Producto.objects.exclude(id=producto.id).filter(activo=True, categoria=producto.categoria)
    context = {
        'producto': producto,
        'productos_relacionados': productos_relacionados,        
    }
    return render(request, 'tienda/detalle.html', context)

def todas_categorias(request):
    categorias = Categoria.objects.filter(activo=True)
    return render(request, 'tienda/categorias.html', {'categorias':categorias})


def categoria_productos(request, slug):
    categoria = get_object_or_404(Categoria, slug=slug)
    productos = Producto.objects.filter(activo=True, categoria=categoria)
    categorias = Categoria.objects.filter(activo=True)
    context = {
        'categoria' : categoria,
        'productos' : productos,
        'categorias' : categorias,
    }
    return render(request, 'tienda/categoria_productos.html', context)


#AUTENTIFICACIONES DE LAS VISTAS 

class RegistrarView(View):
    def get(self, request):
        form = RegistrationForm()
        return render (request, 'cuenta/registrar.html',{'form': form})
    
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, "Felicidades, Registro Completo Correctamente")
            form.save()
        return render(request, 'cuenta/registrar.html', {'form':form})
    

@login_required
def perfil(request):
    direcciones = Direccion.objects.filter(user=request.user)
    ordenes = Orden.objects.filter(user=request.user)
    return render(request, 'cuenta/perfil.html', {'direcciones': direcciones,  'ordenes': ordenes})


@method_decorator(login_required, name='dispatch')
class AddressView(View):
    def get(self, request):
        form = AddressForm()
        return render(request, 'cuenta/agregar_direccion.html', {'form': form})

    def post(self, request):
        form = AddressForm(request.POST)
        if form.is_valid():
            user=request.user
            localidad = form.cleaned_data['localidad']
            municipio = form.cleaned_data['municipio']
            departamento = form.cleaned_data['departamento']
            reg = Direccion(user=user, localidad=localidad, municipio=municipio, departamento=departamento)
            reg.save()
            messages.success(request, "La Nueva Dirreción ha sido agragada correctamente.")
        return redirect('tienda:perfil')


@login_required
def quitar_direccion(request, id):
    a = get_object_or_404(Direccion, user=request.user, id=id)
    a.delete()
    messages.success(request, "Direccion Removida.")
    return redirect('tienda:perfil')

@login_required
def agregar_al_carrito(request):
    user = request.user
    producto_id = request.GET.get('prod_id')
    producto = get_object_or_404(Producto, id=producto_id)


    item_en_carrito = Carrito.objects.filter(producto=producto_id, user=user)
    if item_en_carrito:
        cp = get_object_or_404(Carrito, producto=producto_id, user=user)
        cp.cantidad += 1
        cp.save()
    else:
        Carrito(user=user, producto=producto).save()
    
    return redirect('tienda:carrito')

@login_required
def carrito(request):
    user = request.user
    carrito_productos = Carrito.objects.filter(user=user)
    cantidad = decimal.Decimal(0)
    cantidad_envio = decimal.Decimal(10)
    cp = [p for p in Carrito.objects.all() if p.user==user]
    if cp:
        for p in cp:
            cantidad_temporal = (p.cantidad * p.producto.precio)
            cantidad += cantidad_temporal



    direcciones = Direccion.objects.filter(user=user)

    context = {
        'carrito_productos': carrito_productos,
        'cantidad': cantidad,
        'cantidad_envio': cantidad_envio,
        'total_cantidad': cantidad + cantidad_envio,
        'direcciones': direcciones,
    }
    return render(request, 'tienda/carrito.html', context)


@login_required
def remover_carrito(request, carrito_id):
    if request.method == 'GET':
        c = get_object_or_404(Carrito, id=carrito_id)
        c.delete()
        messages.success(request, "Producto Removido del Carrito.")
    return redirect('tienda:carrito')


@login_required
def plus_carrito(request, carrito_id):
    if request.method == 'GET':
        cp = get_object_or_404(Carrito, id=carrito_id)
        cp.cantidad += 1
        cp.save()
    return redirect('tienda:carrito')


@login_required
def menos_carrito(request, carrito_id):
    if request.method == 'GET':
        cp = get_object_or_404(Carrito, id=carrito_id)
        #REMUEVE LOS PRODUCTOS SI LA CANTIDAD ES MENOR A 1.
        if cp.cantidad == 1:
            cp.delete()
        else:
            cp.cantidad -= 1
            cp.save()
    return redirect('tienda:carrito')


@login_required
def checkout(request):
    user = request.user
    direccion_id = request.GET.get('direccion')
    
    direccion = get_object_or_404(Direccion, id=direccion_id)
    #OBTIENE TODOS LOS PRODUCTOS QUE EL USUARIO TIENE EN EL CARRITO DE COMPRAS
    carrito = Carrito.objects.filter(user=user)
    for c in carrito:
        #GUARDA TODOS LOS PRODUCTOS QUE ESTAN EN EL PEDIDO
        Orden(user=user, direccion=direccion, producto=c.producto, cantidad=c.cantidad).save()
        #BORRA LOS PRODUCTOS DESDE EL CARRITO
        c.delete()
    return redirect('tienda:ordenes')


@login_required
def ordenes(request):
    todas_ordenes = Orden.objects.filter(user=request.user).orden_por('-fecha_pedido')
    return render(request, 'tienda/ordenes.html', {'ordenes': todas_ordenes})





def tienda(request):
    return render(request, 'tienda/tienda.html')





def prueba(request):
    return render(request, 'tienda/prueba.html')


    
    

    




