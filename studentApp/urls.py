from django.urls import path
from studentApp import views

urlpatterns=[
    path('',views.home,name="home"),
    path('notes',views.notes,name="notes"),
    path('delete_note/<int:pk>',views.delete_note,name="delete-note"),
    path('notes_detail/<int:pk>',views.note_details.as_view(),name="notes-detail"),

    path('homework',views.homework,name="homework"),
    path('update_homework/<int:pk>',views.update_homework,name="update-homework"),
    path('delete_homework/<int:pk>',views.delete_homework,name="delete-homework"),
    path('youtube',views.youtubeview,name='youtube'),

    path('books',views.booksview,name='books'),

     path('dictionary',views.dictionaryview,name='dictionary'),

     path('wiki',views.wikiview,name='wiki'),
]