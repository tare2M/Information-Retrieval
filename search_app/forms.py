from django import forms

class SearchForm(forms.Form):
    search_query = forms.CharField(label='Search Query', max_length=100, required=True)
    search_model = forms.ChoiceField(label='Search Model', choices=[
        ('boolean', 'Boolean Model'),
        ('extended boolean', 'Extended Boolean Model'),
        ('vector space model', 'Vector Space Model'),
    ], required=True)