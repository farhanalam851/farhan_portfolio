from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    # Honeypot: real visitors never see or fill this; bots do. The name is deliberately odd,
    # because browsers autofill fields called "website"/"url" and that blocked real visitors.
    contact_hp = forms.CharField(required=False, label="", widget=forms.TextInput(attrs={
        "tabindex": "-1", "autocomplete": "off", "data-lpignore": "true", "data-1p-ignore": "true"}))

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "topic", "message"]
        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Your name", "class": "form-control",
                "autocomplete": "name", "maxlength": 100}),
            "email": forms.EmailInput(attrs={
                "placeholder": "you@company.com", "class": "form-control",
                "autocomplete": "email", "inputmode": "email"}),
            "topic": forms.Select(attrs={"class": "form-select"}),
            "message": forms.Textarea(attrs={
                "placeholder": "Tell me about your project or the role...",
                "rows": 5, "class": "form-control", "maxlength": 3000}),
        }
        error_messages = {
            "name": {"required": "Please tell me your name."},
            "email": {"required": "Please enter your email so I can reply.",
                      "invalid": "That email address doesn't look right."},
            "message": {"required": "Please write a short message."},
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if len(name) < 2:
            raise forms.ValidationError("Please enter your full name.")
        return name

    def clean_message(self):
        message = self.cleaned_data["message"].strip()
        if len(message) < 10:
            raise forms.ValidationError("Please write at least a sentence (10+ characters).")
        return message

    def full_clean(self):
        """Mark every invalid field so the template and screen readers can flag it."""
        super().full_clean()
        for name in self.errors:
            if name in self.fields:
                widget = self.fields[name].widget
                widget.attrs["class"] = (widget.attrs.get("class", "") + " is-invalid").strip()
                widget.attrs["aria-invalid"] = "true"
                widget.attrs["aria-describedby"] = f"{name}-error"
