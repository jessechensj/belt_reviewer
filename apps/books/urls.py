from django.conf.urls import url
from . import views           
urlpatterns = [
  url(r'^$', views.user_index),
  url(r'^login$', views.login),
  url(r'^register$', views.register),
  url(r'^success$', views.success),
  url(r'^add$', views.add),
  url(r'^create$', views.create),
  url(r'^books$', views.books),
  url(r'^book/(?P<id>\d+)$', views.render_book),
  url(r'^book/add_review$', views.add_review),
  url(r'^user/(?P<id>\d+)$', views.user),
  url(r'^book/(?P<book_id>\d+)/delete_review/(?P<review_id>\d+)$', views.delete_review),
  url(r'^logout$', views.logout)
]