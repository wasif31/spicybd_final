from decimal import Decimal
from django.conf import settings
from listings.models import Listing


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, listing, quantity=1, update_quantity=False):
        listing_id = str(listing.id)
        max_quantity = Listing.objects.get(id=listing.id).stock
        if listing_id not in self.cart:
            self.cart[listing_id] = {
                'quantity': 0, 'price': str(listing.price)}
        if update_quantity and self.cart[listing_id]['quantity'] <= max_quantity:
            self.cart[listing_id]['quantity'] = quantity

        elif int(self.cart[listing_id]['quantity']+quantity) <= max_quantity:
            self.cart[listing_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, listing):
        listing_id = str(listing.id)
        if listing_id in self.cart:
            del self.cart[listing_id]
            self.save()

    def __iter__(self):
        listing_ids = self.cart.keys()
        listings = Listing.objects.filter(id__in=listing_ids)
        for listing in listings:
            self.cart[str(listing.id)]['listing'] = listing

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
