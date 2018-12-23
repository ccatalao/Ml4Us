from django import forms

from .models import Project, Label, Doc


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('title','description',)


class LabelForm(forms.ModelForm):

    class Meta:
        model = Label
        fields = ('text',)


class DocForm(forms.ModelForm):

    class Meta:
        model = Doc
        fields = ('text',)

