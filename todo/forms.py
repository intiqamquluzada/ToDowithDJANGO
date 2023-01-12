from django import forms
from .models import Todo


class TodoForm(forms.ModelForm):
    deadline = forms.CharField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Todo
        fields = ('task_name', 'deadline',)

    def __init__(self, *args, **kwargs):
        super(TodoForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
