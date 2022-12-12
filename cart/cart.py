from products.models import Product
from django.contrib import messages


class Cart:
    def __init__(self, request):
        """
        initialize the cart
        """
        self.request = request

        self.session = request.session

        cart = self.session.get('cart')

        if not cart:
            self.session['cart'] = {}
            cart = self.session['cart']

        self.cart = cart

    def add(self, product, quantity=1, replace_current_quantity=False):
        """
        adding product to cart with specified quantity
        """
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0}

        if replace_current_quantity:
            self.cart[product_id]['quantity'] = quantity
            messages.success(self.request, 'cart updated successfully')

        else:
            self.cart[product_id]['quantity'] += quantity
            messages.success(self.request, 'Product added successfully')

        self.save()

    def remove(self, product):
        """
        remove a product from the cart
        """
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            messages.success(self.request, 'product removed successfully')
            self.save()

    def save(self):
        """
        mark session as modified to save changes
        """
        self.session.modified = True

    def __iter__(self):
        """
        to make it possible to iterate on cart
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product_obj'] = product

        for item in cart.values():
            item['total_price'] = item['product_obj'].price * item['quantity']
            yield item

    def __len__(self):
        """
        this is for knowing how many products are there in the cart
        """
        return sum(item['quantity'] for item in self.cart.values())

    def clear(self):
        """
        for clearing the cart totally
        """
        del self.session['cart']
        messages.success(self.request, 'cart cleared successfully')
        self.save()

    def get_total_price(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        return sum(item['product_obj'].price * item['quantity'] for item in self.cart.values())
