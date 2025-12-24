from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone

from .models import Room, Category, Location, Review, User
from .forms import RoomForm, ReviewForm

def index(request):
    rooms = (
        Room.objects.select_related('author', 'category', 'location')
        .filter(is_published=True, pub_date__lte=timezone.now())
        .order_by('-pub_date')
    )
    paginator = Paginator(rooms, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'hotel/index.html', {'page_obj': page_obj})

def room_detail(request, room_id):
    rooms_by_id = {room.id: room for room in Room.objects.all()}
    room = rooms_by_id.get(room_id)
    if room is None:
        raise Http404(f'Номер с id={room_id} не найден!')
    reviews = room.reviews.select_related('author').order_by('created_at')
    review_count = reviews.count()
    return render(
        request,
        'hotel/room_detail.html',
        {'room': room, 'reviews': reviews, 'review_count': review_count}
    )

@login_required
def create_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            room = form.save(commit=False)
            room.author = request.user
            room.save()
            return redirect('profile', username=request.user.username)
    else:
        form = RoomForm()
    return render(request, 'hotel/create_room.html', {'form': form})

@login_required
def edit_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if room.author != request.user:
        return redirect('room_detail', room_id=room_id)
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()
            return redirect('room_detail', room_id=room.id)
    else:
        form = RoomForm(instance=room)
    return render(request, 'hotel/create_room.html', {'form': form, 'room': room})

@login_required
def delete_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if room.author != request.user:
        return redirect('room_detail', room_id=room.id)
    if request.method == 'POST':
        room.delete()
        return redirect('profile', username=request.user.username)
    return render(request, 'hotel/confirm_delete_room.html', {'object': room})

def category_rooms(request, slug):
    category = get_object_or_404(Category, slug=slug)
    rooms = (
        category.rooms.select_related('author', 'location')
        .filter(is_published=True, pub_date__lte=timezone.now())
        .order_by('-pub_date')
    )
    paginator = Paginator(rooms, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'hotel/category.html', {
        'category': category, 'page_obj': page_obj
    })

def location_rooms(request, slug):
    location = get_object_or_404(Location, slug=slug)
    rooms = (
        location.rooms.select_related('author', 'category')
        .filter(is_published=True, pub_date__lte=timezone.now())
        .order_by('-pub_date')
    )
    paginator = Paginator(rooms, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'hotel/location.html', {
        'location': location, 'page_obj': page_obj
    })

@login_required
def add_review(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.room = room
            review.author = request.user
            review.save()
            return redirect('room_detail', room_id=room.id)
    else:
        form = ReviewForm()
    return render(request, 'hotel/add_review.html', {'form': form, 'room': room})

@login_required
def edit_review(request, room_id, review_id):
    review = get_object_or_404(Review, id=review_id, room_id=room_id)
    if review.author != request.user:
        return redirect('room_detail', room_id=room_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.edited_at = timezone.now()
            review.save()
            return redirect('room_detail', room_id=room_id)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'hotel/edit_review.html', {'form': form, 'room': review.room})

@login_required
def delete_review(request, room_id, review_id):
    review = get_object_or_404(Review, id=review_id, room_id=room_id)
    if review.author != request.user:
        return redirect('room_detail', room_id=room_id)
    if request.method == 'POST':
        review.delete()
        return redirect('room_detail', room_id=room_id)
    return render(request, 'hotel/confirm_delete_review.html', {'object': review})