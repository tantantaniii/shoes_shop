from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    slug = models.SlugField(unique=True, verbose_name="URL-метка")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name="Бренд")
    country = models.CharField(max_length=100, blank=True, verbose_name="Страна происхождения")

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"

    def __str__(self):
        return self.name


class Shoe(models.Model):
    GENDER_CHOICES = [
        ('M', 'Мужская'),
        ('F', 'Женская'),
        ('U', 'Унисекс'),
    ]

    SEASON_CHOICES = [
        ('W', 'Зима'),
        ('S', 'Лето'),
        ('D', 'Демисезон'),
        ('A', 'Всесезон'),
    ]

    name = models.CharField(max_length=200, verbose_name="Название модели")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name="Бренд")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Пол")
    season = models.CharField(max_length=1, choices=SEASON_CHOICES, verbose_name="Сезон")
    material_upper = models.CharField(max_length=100, verbose_name="Материал верха")
    material_insole = models.CharField(max_length=100, verbose_name="Материал стельки")
    material_outsole = models.CharField(max_length=100, verbose_name="Материал подошвы")
    heel_height_cm = models.FloatField(null=True, blank=True, verbose_name="Высота каблука (см)")
    is_waterproof = models.BooleanField(default=False, verbose_name="Водонепроницаемость")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = "Обувь"
        verbose_name_plural = "Обувь"

    def __str__(self):
        return f"{self.brand.name} {self.name}"


class ShoeSize(models.Model):
    shoe = models.ForeignKey(Shoe, related_name='sizes', on_delete=models.CASCADE, verbose_name="Модель обуви")
    size = models.FloatField(verbose_name="Размер (RU)")
    stock = models.PositiveIntegerField(default=0, verbose_name="Остаток на складе")

    class Meta:
        verbose_name = "Размер обуви"
        verbose_name_plural = "Размеры обуви"
        unique_together = ('shoe', 'size')

    def __str__(self):
        return f"{self.shoe} — размер {self.size} (остаток: {self.stock}"


class ShoeQuerySet(models.QuerySet):
    def by_gender(self, gender_code):
        """Фильтрация обуви по полу"""
        return self.filter(gender=gender_code)

    def by_season(self, season_code):
        """Фильтрация обуви по сезону"""
        return self.filter(season=season_code)

    def available_in_size(self, size):
        """Возвращает обувь, доступную в указанном размере с остатком > 0"""
        return self.filter(sizes__size=size, sizes__stock__gt=0).distinct()


class ShoeManager(models.Manager):
    def get_queryset(self):
        return ShoeQuerySet(self.model, using=self._db)

    def men_shoes(self):

        return self.get_queryset().by_gender('M')

    def women_shoes(self):

        return self.get_queryset().by_gender('F')

    def summer_shoes(self):

        return self.get_queryset().by_season('S')

    def available_in_size(self, size):

        return self.get_queryset().available_in_size(size)


Shoe.add_to_class('objects', ShoeManager())