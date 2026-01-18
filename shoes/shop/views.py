# shop/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Shoe, Category, Brand, ShoeSize
from .cart import Cart
from .forms import UserRegisterForm


def home(request):
    new_shoes = Shoe.objects.order_by('-created_at')[:6]
    winter_shoes = Shoe.objects.by_season('W')[:4]
    summer_shoes = Shoe.objects.by_season('S')[:4]
    return render(request, 'shop/home.html', {
        'new_shoes': new_shoes,
        'winter_shoes': winter_shoes,
        'summer_shoes': summer_shoes,
    })


def shoe_list(request):
    shoes = Shoe.objects.all()
    
    # Поиск
    query = request.GET.get('q')
    if query:
        shoes = shoes.filter(
            Q(name__icontains=query) |
            Q(brand__name__icontains=query)
        )

    # Фильтры
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
            pass
    if category_id:
        shoes = shoes.filter(category_id=category_id)
    if brand_id:
        shoes = shoes.filter(brand_id=brand_id)

    paginator = Paginator(shoes, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    brands = Brand.objects.all()

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'brands': brands,
        'selected_gender': gender,
        'selected_season': season,
        'selected_size': size,
        'selected_category': category_id,
        'selected_brand': brand_id,
        'search_query': query,
    }
    return render(request, 'shop/shoe_list.html', context)


def shoe_detail(request, pk):
    shoe = get_object_or_404(Shoe, pk=pk)
    return render(request, 'shop/shoe_detail.html', {'shoe': shoe})


# === Корзина ===

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'shop/cart_detail.html', {'cart': cart})


def cart_add(request, shoe_id):
    cart = Cart(request)
    shoe = get_object_or_404(Shoe, id=shoe_id)
    size = request.POST.get('size')
    quantity = int(request.POST.get('quantity', 1))

    if not size:
        messages.error(request, "Выберите размер!")
        return redirect('shop:shoe_detail', pk=shoe_id)

    try:
        shoe.sizes.get(size=float(size), stock__gt=0)
        cart.add(shoe_id=shoe_id, size=float(size), quantity=quantity)
        messages.success(request, f"{shoe.name} (размер {size}) добавлен в корзину!")
    except ShoeSize.DoesNotExist:
        messages.error(request, "Товара нет в наличии в выбранном размере!")

    return redirect('shop:cart_detail')


def cart_remove(request, shoe_id, size):
    cart = Cart(request)
    cart.remove(shoe_id=shoe_id, size=float(size))
    messages.info(request, "Товар удалён из корзины")
    return redirect('shop:cart_detail')


# === Аутентификация ===

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт {username} создан! Вы можете войти.')
            return redirect('shop:login')
    else:
        form = UserRegisterForm()
    return render(request, 'shop/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Вы вошли как {username}.")
                return redirect('shop:home')
            else:
                messages.error(request, "Неверный логин или пароль.")
        else:
            messages.error(request, "Неверный логин или пароль.")
    else:
        form = AuthenticationForm()
    return render(request, 'shop/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.info(request, "Вы вышли из аккаунта.")
    return redirect('shop:home')