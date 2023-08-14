---
title: "Til How to Use Django-Import-Export to Import Data"
date: 2023-08-14T16:02:18-07:00
draft: false
tags: [til, python, django]
---


Today I learned how to import records into Django with [Django-Import-Export](https://django-import-export.readthedocs.io/). I've used the library for exporting and quite liked it, so I thought I'd give it a shot at importing.

Set up was easy since I already had export set up. I simply added `import_export.admin.ImportMixin` as a mixin to my admin model.

I've been using a dynamic model to register everything. Now that model looks like this:

```python
def register_admin_for_models(
    model: Type[Model],
    in_list_display: list[str] | None = None,
    in_list_filter: list[str] | None = None,
):
    """
    This function registers an admin model given the configuration.

    Args:
        model (models): The model
        in_list_display (list[str] | None): The list of fields to display in the admin UI. If None, then all
            fields provided by model._meta.fields are displayed.
        in_list_filter (list[str] | None): List of filters
    """
    # Convert everything to tuples to avoid mutation
    default_list_display = ("__str__",) + tuple(
        field.name for field in model._meta.fields
    )

    readonly_fields = []
    base_readonly_fields = ["id", "created_at", "updated_at", "version"]
    for field in base_readonly_fields:
        if field in default_list_display:
            readonly_fields.append(field)

    the_readonly_fields = tuple(readonly_fields)
    the_list_display = tuple(in_list_display or default_list_display)
    the_list_filter = tuple(in_list_filter or [])

    class DynamicAdmin(ImportMixin, ExportMixin, admin.ModelAdmin):
        list_display = the_list_display
        list_filter = the_list_filter
        readonly_fields = the_readonly_fields

    admin.site.register(model, DynamicAdmin)

models_for_admin: list[Any] = [
    (models.Tag, ()),
]

for values in models_for_admin:
    register_admin_for_models(*values)  # type: ignore
```

It's not the prettiest, but it works.

Now when I navigate to a model in the Django admin UI, there's an import button for importing a file. I used the CSV import but saw options for json, yaml, xls, xlsx, and tsv.

One strange thing I found was that I needed every field in the CSV. I was hoping that if a field was missing, then it'd use the default value the model. This wasn't a show-stopper, but it was annoying for the system-managed fields like created_at and updated_at (but as it turned out, those fields were overwritten at  import time.)

I also found that leaving `id` blank meant it was auto-incremented as expected, but it was interesting that it was needed as a header in the file.

I was then pleased that there was a neat workflow for evaluating errors before importing, a nice confirmation screen, and a generally great experience. I'll definitely keep using this.