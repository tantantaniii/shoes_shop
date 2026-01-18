# shop/cart.py
class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, shoe_id, size, quantity=1):
        key = f"{shoe_id}_{size}"
        if key not in self.cart:
            self.cart[key] = {
                'shoe_id': shoe_id,
                'size': size,
                'quantity': 0,
                'price': 0
            }
        self.cart[key]['quantity'] += quantity
        self.save()

    def remove(self, shoe_id, size):
        key = f"{shoe_id}_{size}"
        if key in self.cart:
            del self.cart[key]
            self.save()

    def get_items(self):
        from .models import Shoe, ShoeSize
        items = []
        for item in self.cart.values():
            try:
                shoe = Shoe.objects.get(id=item['shoe_id'])
                size_obj = shoe.sizes.get(size=item['size'])
                item['shoe'] = shoe
                item['size_obj'] = size_obj
                item['price'] = float(shoe.price)
                item['total_price'] = item['price'] * item['quantity']
                items.append(item)
            except (Shoe.DoesNotExist, ShoeSize.DoesNotExist):
                continue
        return items

    def get_total_price(self):
        return sum(item['total_price'] for item in self.get_items())

    def clear(self):
        self.session['cart'] = {}
        self.save()

    def save(self):
        self.session.modified = True