# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django.contrib import admin
# Internal
from .models import Contact
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """
    Admin Class for Contact Model for contact registration in admin panel
    """
    list_display = (
        'contact_id',
        'name',
        'message',
        'phone',
        'email',
    )
    # Fields that will act as clickable links to edit page
    list_display_links = ('contact_id', 'name',)
    list_filter = ('name', 'email',)
    search_fields = ('name', 'email', 'phone', 'message',)
    ordering = ('-contact_id',)  # Order by descending contact_id

    readonly_fields = ('contact_id',)  # Make the contact_id field read-only

    fieldsets = (
        ('Contact Information', {
            'fields': ('contact_id', 'name', 'email', 'phone'),
        }),
        ('Message Information', {
            'fields': ('message',),
        }),
    )

    # Automatically populates the contact_id field with an incremental value
    def save_model(self, request, obj, form, change):
        if not obj.contact_id:
            last_contact = Contact.objects.all().order_by('contact_id').last()
            if last_contact is not None:
                obj.contact_id = last_contact.contact_id + 1
            else:
                obj.contact_id = 1
        super().save_model(request, obj, form, change)
