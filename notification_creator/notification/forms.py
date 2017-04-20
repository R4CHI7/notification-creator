from django import forms

from notification.models import Notification


class NotificationForm(forms.ModelForm):
    send_at = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])

    class Meta:
        model = Notification
        fields = ['header', 'content', 'image_url', 'user_query', 'send_at']
