from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.db.models import Q

from .models import Product, Category, Like


class ProductListView(ListView):
    model = Product
    template_name = "products/index.html"
    paginate_by = 12
    ordering = ['-id']
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_list'] = Product.objects.all()
        context['category_list'] = Category.objects.all()
        return context

    def get_queryset(self):
        object_list = super().get_queryset()
        query = self.request.GET.get("search")
        if query:
            object_list = Product.objects.filter(
                Q(title__icontains=query) | Q(category__title__icontains=query
                                              )).distinct()
        return object_list


class SpecialListView(ListView):
    model = Product
    template_name = "products/special.html"
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_list'] = Product.objects.all()
        context['category_list'] = Category.objects.all()
        return context

    def get_queryset(self):
        object_list = super().get_queryset()
        query = self.request.GET.get("search")
        if query:
            object_list = Product.objects.filter(
                Q(title__icontains=query) | Q(category__title__icontains=query
                                              )).distinct()
        return object_list


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.likes.filter(
                product__slug=self.object.slug,
                user_id=self.request.user.id).exists():
            context['is_liked'] = True
        else:
            context['is_liked'] = False
        return context


class LikeListView(ListView):
    model = Like
    template_name = "products/like-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['like_list'] = Like.objects.filter(user=self.request.user)
        return context


def like(request, slug, pk):
    try:
        like = Like.objects.get(product__slug=slug, user_id=request.user.id)
        like.delete()
        return JsonResponse({"response": "unliked"})
    except Exception:
        Like.objects.create(product_id=pk, user_id=request.user.id)
        return JsonResponse({"response": "liked"})
