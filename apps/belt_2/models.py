from __future__ import unicode_literals
from django.db import models
import bcrypt

class UserManager(models.Manager):
    def validateRegistration(self, form_data):
        errors = []

        if len(form_data['name']) < 3:
            errors.append("Name must be at least 3 characters.")

        if len(form_data['username']) < 3:
            errors.append("Username must be at least 3 characters.")

        if len(form_data['password']) < 8:
            errors.append("Password must be at least 8 characters.")

        if form_data['password'] != form_data['confirm_password']:
            errors.append("Passwords do not match")

        if len(form_data['hired']) == 0:
            errors.append("Hire date cannot be blank.")

        return errors

    def createUser(self, form_data):
        password = str(form_data['password'])
        hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt())

        user = User.objects.create(
            name = form_data['name'],
            username = form_data['username'],
            password = hashed_pw,
            date_hired = form_data['hired']
        )

        return user

    def validateLogin(self, form_data):
        errors = []

        if len(form_data['username']) == 0:
            errors.append("Username is required")

        if len(form_data['password']) == 0:
            errors.append("Password is required")

        return errors

class WishManager(models.Manager):
    def validateWish(self, form_data):
        errors = []

        if len(form_data['product']) < 3:
            errors.append("Product name must be at least 3 characters.")

        return errors

    def addWish(self, form_data, user):
        wish = Wish.objects.create(
            product = form_data['product'],
            user = user
        )

        user.wishers.add(wish)
        return wish

class User(models.Model):
    name = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    date_hired = models.DateField(auto_now=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Wish(models.Model):
    product = models.CharField(max_length=30)
    user = models.ForeignKey(User, related_name="wishes")
    wishers = models.ManyToManyField(User, related_name="wishers")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = WishManager()
