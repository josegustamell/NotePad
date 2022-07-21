from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerUser, name='register'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('', views.home, name='home'),
    path('add/', views.addNote, name='add_note'),
    path('add-in-notebook/<str:pk>', views.addNoteInNotebook, name='add-in-notebook'),
    path('add-notebook/', views.addNotebook, name='add_notebook'),
    path('notebook/<str:pk>', views.notebookNotes, name='notebook'),
    path('note/', views.searchNote, name='search'),
    path('edit/<str:pk>', views.editNote, name='edit'),
    path('edit-notebook/<str:pk>', views.editNotebook, name='edit-notebook'),
    path('delete/<str:pk>', views.deleteNote, name='delete-note'),
    path('delete-notebook/<str:pk>', views.deleteNotebook, name='delete-notebook')

]

