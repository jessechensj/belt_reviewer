from django.shortcuts import render, HttpResponse, redirect
from django.contrib.sessions.models import Session
from models import *
from django.contrib import messages
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
WHITESPACE_REGEX = re.compile(r'^\s+$')

def user_index(request):
  return render(request, 'user_index.html')

def login(request):
  if request.method == "POST":
    if re.match(EMAIL_REGEX, request.POST['email']) != None:
      user = User.objects.filter(email=request.POST['email'])
      if user:
        if user[0].password == request.POST["password"]:
          request.session['user_id'] = user[0].id
          return redirect('/success')
        else:
          messages.error(request, "Invalid E-mail or Password")
          return redirect('/')
      else:
        messages.error(request, "Invalid E-mail or Password")
        return redirect('/')
    else:
      messages.error(request, "Invalid E-mail or Password")
      return redirect('/')
  return redirect('/')

def register(request):
  if request.method == "POST":
    if len(User.objects.validation(request.POST)) > 0:
      messages.error(request, User.objects.validation(request.POST))
      return redirect('/')
    else:
      User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=request.POST['password'])
      messages.error(request, "successfully registered")
      return redirect('/')
  return redirect('/')

def success(request):
  request.session['first_name'] = User.objects.get(id=request.session['user_id']).first_name
  return redirect('/books')

def books(request):
    latest = {
        'reviews':Review.objects.all().order_by('-id')[:3][::-1],
        'books':Book.objects.all()
        }
    return render(request, 'book_index.html', latest)

def add(request):
    authors = {'authors':Author.objects.all().values()}
    return render(request, 'book_add.html', authors)

def create(request):
    if len(request.GET['author_text']) == 0 or re.match(WHITESPACE_REGEX, request.GET['author_text']):
        author_name = request.GET['author_dropdown']
    else:
        author_name = request.GET['author_text']
    if not Author.objects.filter(name=author_name):
        Author.objects.create(name=author_name)
    author = Author.objects.filter(name=author_name)
    Book.objects.create(title=request.GET['title'], author=author[0])
    Review.objects.create(text=request.GET['review'], rating=request.GET['rating'], user=User.objects.get(id=request.session['user_id']), book=Book.objects.last())
    return redirect('/books')

def render_book(request, id):
    book = {
        'book':Book.objects.get(id=id),
        'reviews':Review.objects.filter(book=id)
        }
    return render(request, "render_book.html", book)

def add_review(request):
    Review.objects.create(rating=request.GET['rating'], text=request.GET['text'], user=User.objects.get(id=request.session['user_id']), book=Book.objects.get(id=request.GET['book_id']))
    return redirect('/book/' + str(request.GET['book_id']))

def user(request, id):
    user = User.objects.get(id=id)
    reviews = user.reviews.all()
    book_ids = reviews.values("book_id").distinct()
    books = []
    for book in book_ids:
        books.append(Book.objects.get(id=book["book_id"]))
    user = {
        'user':user,
        'count':User.objects.get(id=id).reviews.count(),
        'books':books
    }
    print User.objects.get(id=id).reviews
    return render(request, "user.html", user)

def logout(request):
    request.session.flush()
    messages.error(request, "Successfully logged out")
    return redirect('/')

def delete_review(request, book_id, review_id):
    Review.objects.get(id=review_id).delete()
    return redirect('/book/' + str(book_id))