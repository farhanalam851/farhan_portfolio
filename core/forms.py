from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    # Honeypot: real visitors never see or fill this; bots do.
    website = forms.CharField(required=False, widget=forms.TextInput(attrs={
        "tabindex": "-1", "autocomplete": "off"}))

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "topic", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your name", "class": "form-control"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@company.com", "class": "form-control"}),
            "topic": forms.Select(attrs={"class": "form-select"}),
            "message": forms.Textarea(attrs={
                "placeholder": "Tell me about your project or the role...",
                "rows": 5, "class": "form-control"}),
        }

    def clean_website(self):
        if self.cleaned_data.get("website"):
            raise forms.ValidationError("Spam detected.")
        return ""
