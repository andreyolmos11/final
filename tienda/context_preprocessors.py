from .models import Categoria, Carrito


def tienda_menu(request):
    categorias = Categoria.objects.filter(is_active=True)
    context = {
        'categorias_menu': categorias,
    }
    return context

def carrito_menu(request):
    if request.user.is_authenticated:
        carrito_items= Carrito.objects.filter(user=request.user)
        context = {
            'carrito_items': carrito_items,
        }
    else:
        context = {}
    return context