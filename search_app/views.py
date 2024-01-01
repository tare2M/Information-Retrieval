import os
from django.shortcuts import render, redirect
from .utils import boolean_search, extended_boolean_search, vector_space_model_search, build_boolean_index, read_doc, extract_text_from_doc
from .forms import SearchForm

def home(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            search_query = form.cleaned_data['search_query']
            search_model = form.cleaned_data['search_model']
            print("Search Query (home):", search_query)
            print("Search Model (home):", search_model)

            # Redirect to the search_results view with search parameters as query parameters
            return redirect('search_results', search_query=search_query, search_model=search_model)
    else:
        form = SearchForm()

    return render(request, 'home.html', {'form': form})

def search_results(request):
    try:
        doc_folder_path = ".\search_app\doc"
        documents = [read_doc(os.path.join(doc_folder_path, filename)) for filename in os.listdir(doc_folder_path) if filename.endswith(".doc")]
        inverted_index = build_boolean_index(documents)

        if not documents:
            return render(request, 'search_results.html', {'error': "No documents available for searching."})

        search_query = request.GET.get('search_query')
        search_model = request.GET.get('search_model')
        print("Search Query:", search_query)
        print("Search Model:", search_model)
        print("Search Query and Model Type:")
        print(type(search_query), type(search_model))

        if search_query and search_model:
            search_models = {
                'boolean': boolean_search,
                'extended boolean': extended_boolean_search,
                'vector space model': vector_space_model_search,
            }

            search_function = search_models.get(search_model.lower())
            if search_function:
                # Using the selected search function from utils.py
                search_results = search_function(search_query, inverted_index, documents)
                return render(request, 'search_results.html', {'search_results': search_results, 'query': search_query})
            else:

                return render(request, 'search_results.html', {'error': "Invalid model selection. Choose between 'Boolean', 'Extended Boolean', or 'Vector Space Model.'"})
        else:
            return render(request, 'search_results.html', {'error': "Invalid search query or model."})
    except Exception as e:
        return render(request, 'search_results.html', {'error': f"An error occurred: {e}"})
