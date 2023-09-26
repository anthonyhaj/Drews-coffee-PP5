from django.shortcuts import render, redirect
from django.views import View
from .forms import ContactForm
from .models import Contact


class ContactView(View):
    template_name = 'contact/contact.html'

    def get(self, request):
        form = ContactForm()
        if request.user.is_authenticated:
            # Pre-fill the email if the user is authenticated
            form.fields['email'].initial = request.user.email
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            new_contact = form.save(commit=False)
            if request.user.is_authenticated:
                new_contact.email = request.user.email 
            new_contact.save()
            # Redirect to a new page indicating success
            return redirect('contact_success')  
        return render(request, self.template_name, {'form': form})
