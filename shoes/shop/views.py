from django.shortcuts import render, get_object_or_404
from .models import Shoe, Category, Brand

def shoe_list(request):
    shoes = Shoe.objects.all()
    
    gender = request.GET.get('gender')
    season = request.GET.get('season')
    size = request.GET.get('size')
    category_id = request.GET.get('category')
    brand_id = request.GET.get('brand')

    if gender:
        shoes = shoes.by_gender(gender)
    if season:
        shoes = shoes.by_season(season)
    if size:
        try:
            shoes = shoes.available_in_size(float(size))
        except ValueError:
            pass  #игнор некорректного размера
    if category_id:
        shoes = shoes.filter(category_id=category_id)
    if brand_id:
        shoes = shoes.filter(brand_id=brand_id)

    categories = Category.objects.all()
    brands = Brand.objects.all()

    context = {
        'shoes': shoes,
        'categories': categories,
        'brands': brands,
        'selected_gender': gender,
        'selected_season': season,
        'selected_size': size,
        'selected_category': category_id,
        'selected_brand': brand_id,
    }
    return render(request, 'shop/shoe_list.html', context)


def shoe_detail(request, pk):
    shoe = get_object_or_404(Shoe, pk=pk)
    return render(request, 'shop/shoe_detail.html', {'shoe': shoe})