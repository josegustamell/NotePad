from django.shortcuts import render, redirect
from .models import Notes, Notebook
from .forms import CreateUserForm
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def registerUser(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    context = {'form': form}
    return render(request, 'base/register.html', context)


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('tasks')
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, username=email, password=password)
            login(request, user)
            return redirect('home')
            
    return render(request, 'base/login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')


def notebooks(request):
    if request.user.is_authenticated:
        return {'notebooks_main': Notebook.objects.filter(user=request.user)}
    else:
        return {}


@login_required(login_url='login')
def home(request):  # Show all the notes
    notes = Notes.objects.filter(user=request.user)
    number_notes = notes.count()
    number_notebooks = Notebook.objects.filter(user=request.user).count()
    context = {
        'notes': notes,
        'number_notes': number_notes,
        'number_notebooks': number_notebooks
    }
    return render(request, 'base/home.html', context)


@login_required(login_url='login')
def addNote(request):
    number_notebooks = len(Notebook.objects.filter(user=request.user))

    if request.method == 'POST':
        data = request.POST
        note = request.POST.get('content')  
        title = request.POST.get('title_note')  

        if data['notebook'] != 'none':  
            notebook = Notebook.objects.get(id=data['notebook'])
        elif data['notebook_new'] != '':  
            notebook, created = Notebook.objects.get_or_create(name=data['notebook_new'], user=request.user)  
        else:                                                                      
            notebook = None

        Notes.objects.create(
            notebook=notebook,
            title=title,
            content=note,
            user=request.user
        )

        return redirect('home')

    context = {'number_notebooks': number_notebooks}
    return render(request, 'base/add_note.html', context)


@login_required(login_url='login')
def editNote(request, pk):
    notebooks = Notebook.objects.filter(user=request.user)
    note = Notes.objects.get(id=pk)

    if note.notebook == None:
        notebooks_select = notebooks
    else:
        notebooks_select = notebooks.exclude(name__icontains=note.notebook)

    if request.method == 'POST':
        data = request.POST
        if data['notebook'] != '':
            notebook = Notebook.objects.get(id=data['notebook'])
            note.notebook = notebook
        else:
            note.notebook = note.notebook
        note.title = data['title_note']
        note.content = data['content']
        note.save()
        return redirect('home')

    context = {'note': note,'notebooks_select': notebooks_select}
    return render(request, 'base/edit_note.html', context)


@login_required(login_url='login')
def addNotebook(request):
    if request.method == 'POST':
        data = request.POST
        Notebook.objects.create(
            user=request.user,
            name=data['name-notebook']
        )
        return redirect('home')
    return render(request, 'base/add_notebook.html')


@login_required(login_url='login')
def notebookNotes(request, pk):  # Show the notes of a specific notebook.
    notebook = Notebook.objects.filter(user=request.user).get(id=pk)
    notes = Notes.objects.filter(notebook=notebook)
    number_notes = notes.count()

    context = {
        'notebook': notebook,
        'notes': notes,
        'number_notes': number_notes
    }
    return render(request, 'base/notebook_notes.html', context)


@login_required(login_url='login')
def addNoteInNotebook(request, pk):  # Allow the user to create a note automatically inside the notebook that he is
    notebook = Notebook.objects.get(id=pk)  # looking
    notebooks = Notebook.objects.filter(user=request.user).exclude(name__icontains=notebook.name)

    if request.method == 'POST':
        data = request.POST
        note = request.POST.get('content')
        title = request.POST.get('title_note')

        if data['notebook'] == notebook.id:
            notebook = Notebook.objects.get(id=data['notebook'])

        Notes.objects.create(
            notebook=notebook,
            title=title,
            content=note,
            user=request.user
        )

        return redirect('home')

    context = {'notebook': notebook, 'notebooks': notebooks}
    return render(request, 'base/add_note_in_notebook.html', context)


@login_required(login_url='login')
def editNotebook(request, pk):
    notebook = Notebook.objects.get(id=pk)

    if request.method == 'POST':
        notebook.name = request.POST.get('name')
        notebook.save()
        return redirect('notebook', pk=notebook.id)

    context = {'notebook': notebook}
    return render(request, 'base/edit_notebook.html', context)


@login_required(login_url='login')
def deleteNote(request, pk):
    note = Notes.objects.get(id=pk)
    notebook = note.notebook

    if request.method == 'POST':
        note.delete()
        return redirect('home')

    context = {'note': note, 'notebook': notebook}
    return render(request, 'base/delete_note.html', context)


@login_required(login_url='login')
def deleteNotebook(request, pk):
    notebook = Notebook.objects.get(id=pk)

    if request.method == 'POST':
        notebook.delete()
        return redirect('home')

    context = {'notebook': notebook}
    return render(request, 'base/delete_notebook.html', context)


@login_required(login_url='login')
def searchNote(request):
    query = request.GET.get('q')
    query_set = Notes.objects.filter(user=request.user)

    if query is not None:
        lookups = Q(title__icontains=query) | Q(content__icontains=query)
        query_set = Notes.objects.filter(lookups)

    context = {'note': query_set, 'query': query}
    return render(request, 'base/search.html', context)
