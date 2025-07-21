# core/forms.py

from django import forms
from core.models import Book

GENRE_CHOICES = [
    ('', 'Select'),
    ('Classics', 'Classics'),
    ('Crime', 'Crime'),
    ('Fiction', 'Fiction'),
    ('Historical Fiction', 'Historical Fiction'),
    ('History', 'History'),
    ('Horror', 'Horror'),
    ('Mystery', 'Mystery'),
    ('Philosophy', 'Philosophy'),
    ('Psychology', 'Psychology'),
    ('Religion', 'Religion'),
    ('Science', 'Science'),
    ('Science Fiction', 'Science Fiction'),
    ('Thriller', 'Thriller'),
    ('Art', 'Art'),
    ('Biography', 'Biography'),
    ('Business', 'Business'),
    ("Children's", "Children's"),
    ('Christian', 'Christian'),
    ('Comics', 'Comics'),
    ('Contemporary', 'Contemporary'),
    ('Cookbooks', 'Cookbooks'),
    ('Ebooks', 'Ebooks'),
    ('Fantasy', 'Fantasy'),
    ('Graphic Novels', 'Graphic Novels'),
    ('Humor and Comedy', 'Humor and Comedy'),
    ('Manga', 'Manga'),
    ('Memoir', 'Memoir'),
    ('Music', 'Music'),
    ('Nonfiction', 'Nonfiction'),
    ('Paranormal', 'Paranormal'),
    ('Poetry', 'Poetry'),
    ('Romance', 'Romance'),
    ('Self Help', 'Self Help'),
    ('Suspense', 'Suspense'),
    ('Spirituality', 'Spirituality'),
    ('Sports', 'Sports'),
    ('Travel', 'Travel'),
    ('Young Adult', 'Young Adult'),
]

SORT_CHOICES = [
    ('-average_rating', 'Rating (High → Low)'),
    ('-ratings_count',   'Popularity (High → Low)'),
    ('title',            'Title (A → Z)'),
    ('-title',           'Title (Z → A)'),
    ('num_pages',        'Pages (Few → Many)'),
    ('-num_pages',       'Pages (Many → Few)'),
    ('publication_year', 'Publication Year (Old → New)'),
    ('-publication_year','Publication Year (New → Old)'),
]

class SearchForm(forms.Form):
    title = forms.CharField(label='Title', required=False)
    author = forms.CharField(label='Author', required=False)
    genre1 = forms.ChoiceField(label='Genre 1', choices=GENRE_CHOICES, required=False,
                               widget=forms.Select(attrs={'class':'form-select'}))
    genre2 = forms.ChoiceField(label='Genre 2', choices=GENRE_CHOICES, required=False,
                               widget=forms.Select(attrs={'class':'form-select'}))
    rating_min = forms.FloatField(label='Min. Rating', required=False, min_value=0, max_value=5)
    rating_max = forms.FloatField(label='Max. Rating', required=False, min_value=0, max_value=5)
    year_min = forms.IntegerField(label='Min. Publication Year', required=False)
    year_max = forms.IntegerField(label='Max. Publication Year', required=False)
    pages_min = forms.IntegerField(label='Min. Pages', required=False, min_value=1)
    pages_max = forms.IntegerField(label='Max. Pages', required=False, min_value=1)
    sort_by = forms.ChoiceField(label='Sort by', choices=SORT_CHOICES, required=False,
                                widget=forms.Select(attrs={'class':'form-select'}))

class FavoriteBooksForm(forms.Form):
    book1 = forms.CharField(
        label='First Book',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'list': 'book1_list',
            'autocomplete': 'off',
            'id': 'id_book1',
            'placeholder': 'Type book name...'
        })
    )
    book2 = forms.CharField(
        label='Second Book',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'list': 'book2_list',
            'autocomplete': 'off',
            'id': 'id_book2',
            'placeholder': 'Type book name...'
        })
    )
    book3 = forms.CharField(
        label='Third Book',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'list': 'book3_list',
            'autocomplete': 'off',
            'id': 'id_book3',
            'placeholder': 'Type book name...'
        })
    )

    def _resolve_book(self, text):
        qs = Book.objects.filter(title__icontains=text)
        if not qs.exists():
            return None
        return qs.order_by('-average_rating', '-ratings_count').first()

    def clean_book1(self):
        text = self.cleaned_data.get('book1', '').strip()
        book = self._resolve_book(text)
        if not book:
            raise forms.ValidationError("No match found for the first book.")
        return book

    def clean_book2(self):
        text = self.cleaned_data.get('book2', '').strip()
        book = self._resolve_book(text)
        if not book:
            raise forms.ValidationError("No match found for the second book.")
        return book

    def clean_book3(self):
        text = self.cleaned_data.get('book3', '').strip()
        book = self._resolve_book(text)
        if not book:
            raise forms.ValidationError("No match found for the third book.")
        return book

    def clean(self):
        cleaned = super().clean()
        b1 = cleaned.get('book1')
        b2 = cleaned.get('book2')
        b3 = cleaned.get('book3')
        if b1 and b2 and b1.pk == b2.pk or \
           b1 and b3 and b1.pk == b3.pk or \
           b2 and b3 and b2.pk == b3.pk:
            raise forms.ValidationError("You cannot select the same book more than once.")
        return cleaned
