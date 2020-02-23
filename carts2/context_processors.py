from .carts2 import Cart


def carts2(request):
    return {'carts2': Cart(request)}
