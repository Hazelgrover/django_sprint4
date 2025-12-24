from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('rooms/create/', views.create_room, name='create_room'),
    path('rooms/<int:room_id>/', views.room_detail, name='room_detail'),
    path('rooms/<int:room_id>/edit/', views.edit_room, name='edit_room'),
    path('rooms/<int:room_id>/delete/', views.delete_room, name='delete_room'),
    path('rooms/<int:room_id>/review/', views.add_review, name='add_review'),
    path(
        'rooms/<int:room_id>/edit_review/<int:review_id>/',
        views.edit_review, name='edit_review'
    ),
    path(
        'rooms/<int:room_id>/delete_review/<int:review_id>/',
        views.delete_review, name='delete_review'
    ),
    path('category/<slug:slug>/', views.category_rooms, name='category_rooms'),
    path('location/<slug:slug>/', views.location_rooms, name='location_rooms'),
]
