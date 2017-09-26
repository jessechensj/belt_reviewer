from __future__ import unicode_literals

from django.db import models

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

class UserManager(models.Manager):
    def validation(self, requestPost):
        string = ""
        if User.objects.filter(email=requestPost['email']):
            string += "Email already exists"
        if len(requestPost['first_name']) < 2:
            string += " First name is too short"
        if len(requestPost['last_name']) < 2: 
            string += " Last name is too short"
        if re.match(NAME_REGEX, requestPost['first_name']) == None or re.match(NAME_REGEX, requestPost['last_name']) == None:
            string += " Name may only contain letters"
        if re.match(EMAIL_REGEX, requestPost['email']) == None:
            string += " Invalid E-mail"
        if requestPost['password'] != requestPost['confirm_password']:
            string += " Password does not match confirm password"
        if len(requestPost['password']) < 8:
            string += " Password too short"
        return string

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Author(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name = "books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    

class Review(models.Model):
    rating = models.IntegerField()
    user = models.ForeignKey(User, related_name = "reviews")
    text = models.TextField()
    book = models.ForeignKey(Book, related_name = "reviews")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 