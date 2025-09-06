
from django.views.generic import TemplateView, ListView
from django.views import View 
from django.shortcuts import render, redirect, get_object_or_404 
from django.http import HttpResponseRedirect 
from django.urls import reverse 
from django import forms
from django.core.exceptions import ValidationError 
#from .models import Product 
 # Create your views here. 
class HomePageView(TemplateView): 

    template_name = 'pages/home.html' 

 
class Product: 

    products = [ 
        {"id":"1", "name":"TV", "description":"Best TV", "price": "5000"}, 
        {"id":"2", "name":"iPhone", "description":"Best iPhone", "price": "10"}, 
        {"id":"3", "name":"Chromecast", "description":"Best Chromecast", "price": "9"}, 
        {"id":"4", "name":"Glasses", "description":"Best Glasses", "price": "40000000"} 
    ] 


class AboutPageView(TemplateView): 
    template_name = 'pages/about.html' 
 
     
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        context.update({ 
            "title": "About us - Online Store", 
            "subtitle": "About us", 
            "description": "This is an about page ...", 
            "author": "Developed by: María Acevedo", 
        }) 
 
        return context 
    

class ContactPageView(TemplateView):
    template_name = 'pages/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Contact",
            "subtitle": "Contact us",
            "description": "Email: onlineStore@gmail.com | Address: 128 Mapple St "
            "| Phone number: +98 12389012312 "

        })
        return context    

 
class ProductIndexView(View): 
    template_name = 'products/index.html' 
 
    def get(self, request): 
        viewData = {} 
        viewData["title"] = "Products - Online Store" 
        viewData["subtitle"] =  "List of products" 
        viewData["products"] = Product.products 
 
        return render(request, self.template_name, viewData) 
 
class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        try:
            product_id = int(id)
            if product_id < 1:
                raise ValueError("Product id must be 1 or greater")

            # Buscar el producto en la lista
            product = next((p for p in Product.products if int(p["id"]) == product_id), None)
            if not product:
                raise ValueError("Product not found")

            # ✅ Convertir precio a número
            product["price"] = float(product["price"])

        except (ValueError, IndexError):
            return HttpResponseRedirect(reverse('home'))

        viewData = {}
        viewData["title"] = product["name"] + " - Online Store"
        viewData["subtitle"] = product["name"] + " - Product information"
        viewData["product"] = product

        return render(request, self.template_name, viewData)
    


from django import forms 
from django.shortcuts import render, redirect 
 
from django import forms
from django.core.exceptions import ValidationError

class ProductForm(forms.Form):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is None or price <= 0:
            raise ValidationError("The price must be greater than zero.")
        return price
 
class ProductCreateView(View):
    template_name = 'products/create.html'

    def get(self, request):
        form = ProductForm()
        viewData = {}
        viewData["title"] = "Create product"
        viewData["form"] = form
        return render(request, self.template_name, viewData)

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
        # si quieres guardar el producto en tu lista (opcional):
            new_id = len(Product.products) + 1
            Product.products.append({
                "id": str(new_id),
                "name": form.cleaned_data["name"],
                "description": "New Product",
                "price": form.cleaned_data["price"],
         })

        # redirigir a un template de confirmación
            return render(request, "products/created.html", {
                "title": "Product Created",
        })
        else:
            viewData = {}
            viewData["title"] = "Create product"
            viewData["form"] = form
            return render(request, self.template_name, viewData)