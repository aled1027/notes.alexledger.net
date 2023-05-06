---
date: 2023-04-02
tags:
    - til
    - python
    - django
title: TIL How to customize the Django admin UI
---

# TIL How to customize the Django admin UI

https://docs.djangoproject.com/en/4.1/ref/contrib/admin/#django.contrib.admin

Today I learned how to customize a few pieces of the Django Admin UI. Namely: choosing the columns that are shown and adding search.

Suppose we have the following `Neighborhood` and `Person` models.

```
# models.py

from django.db import models

class Neighborhood(models.Model):
    location = models.CharField(max_length=64, null=False, blank=True)

    def __str__(self) -> str:
        return self.location


class Person(models.Model):
    name = models.CharField(max_length=64, null=False, blank=True)
    age = models.IntegerField()
    Neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE, null=True)
```

Then we can set up a Person Admin where we show all the fields and can search on name and neighborhood location.

```
# admin.py

from django.contrib import admin

from .models import Person, Neighborhood


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "age",
        "neighborhood",
    ]

    # Here's a convenient way to grab everything:
    # list_display = ["__str__"] + [fld.get_attname() for fld in Person._meta.fields]

    search_fields = ["name", "neighborhood__location"]
```

## Other Tips

- If you have a custom `__str__` for the model, then include `__str__` under the `list_display`. If it's the first option, then it's clickable.
- Reference attributes on related objects with this formula containing two underscores: `<object>__<obj_attribute>`.