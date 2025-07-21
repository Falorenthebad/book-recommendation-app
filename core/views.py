# core/views.py

from collections import Counter
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from core.forms import FavoriteBooksForm, SearchForm
from core.models import Book
from django.db.models import Q
from django.core.paginator import Paginator

def home(request):
    return render(request, 'core/home.html')

def search_books(request):
    form = SearchForm(request.GET or None)
    qs = Book.objects.all()

    if form.is_valid():
        cd = form.cleaned_data

        if cd['title']:
            qs = qs.filter(title__icontains=cd['title'].strip())
        if cd['author']:
            qs = qs.filter(author_names__icontains=cd['author'].strip())

        for key in ('genre1','genre2'):
            genre = cd.get(key)
            if genre:
                qs = qs.filter(
                    Q(genre_1=genre)|Q(genre_2=genre)|
                    Q(genre_3=genre)|Q(genre_4=genre)|Q(genre_5=genre)
                )

        if cd['rating_min'] is not None:
            qs = qs.filter(average_rating__gte=cd['rating_min'])
        if cd['rating_max'] is not None:
            qs = qs.filter(average_rating__lte=cd['rating_max'])
        if cd['year_min'] is not None:
            qs = qs.filter(publication_year__gte=cd['year_min'])
        if cd['year_max'] is not None:
            qs = qs.filter(publication_year__lte=cd['year_max'])
        if cd['pages_min'] is not None:
            qs = qs.filter(num_pages__gte=cd['pages_min'])
        if cd['pages_max'] is not None:
            qs = qs.filter(num_pages__lte=cd['pages_max'])

        sort = cd.get('sort_by')
        if sort:
            qs = qs.order_by(sort)
        else:
            qs = qs.order_by('-average_rating', '-ratings_count')
    else:
        qs = Book.objects.none()

    paginator = Paginator(qs, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'core/search.html', {
        'form': form,
        'page_obj': page_obj,
    })

def recommend_by_favorites(request):
    """
    Kullanıcı POST ile üç favori kitabı gönderdiğinde
    onlara benzer diğer kitapları önersin (şimdi 15 kitap).
    """
    if request.method == 'POST':
        form = FavoriteBooksForm(request.POST)
        if form.is_valid():
            selected = [
                form.cleaned_data['book1'],
                form.cleaned_data['book2'],
                form.cleaned_data['book3'],
            ]

            genre_counts = Counter(
                g
                for book in selected
                for g in (getattr(book, f'genre_{i}') for i in range(1,6))
                if g
            )

            recommendations = []
            excluded = [b.pk for b in selected]
            for book in Book.objects.exclude(pk__in=excluded):
                common = sum(
                    genre_counts.get(getattr(book, f'genre_{i}'), 0)
                    for i in range(1,6)
                )
                score = common + book.average_rating * 0.1
                recommendations.append((score, book))

            recommendations.sort(key=lambda x: x[0], reverse=True)
            top15 = [bk for _, bk in recommendations[:15]]

            return render(request, 'core/recommend_results.html', {
                'selected': selected,
                'recommendations': top15,
            })
    else:
        form = FavoriteBooksForm()

    return render(request, 'core/recommend_form.html', {
        'form': form,
    })

def book_suggest(request):
    q = request.GET.get('q', '').strip()
    results = []
    if len(q) >= 2:
        qs = (Book.objects
                 .filter(title__icontains=q)
                 .order_by('-average_rating', '-ratings_count')[:10])
        for b in qs:
            results.append({
                'title': b.title,
                'first_author': b.first_author,
            })
    return JsonResponse({'results': results})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    genres = [
        getattr(book, f'genre_{i}')
        for i in range(1, 6)
        if getattr(book, f'genre_{i}')
    ]
    return render(request, 'core/book_detail.html', {
        'book': book,
        'genres': genres,
    })

def random_book(request):
    book = Book.objects.filter(average_rating__gt=3.7).order_by('?').first()
    return render(request, 'core/random_book.html', {
        'book': book,
    })
