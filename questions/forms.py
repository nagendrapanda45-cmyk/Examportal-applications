from django import forms
from home.users.models import Question

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            'test_type', 'question_text', 'option_a', 'option_b', 'option_c', 'option_d',
            'technical_question_answer', 'correct_answer', 'difficulty',
            'category_type', 'specialisation_name', 'is_multichoice', 'is_active', 'deleted'
        ]
        widgets = {
            'question_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'option_a': forms.TextInput(attrs={'class': 'form-control'}),
            'option_b': forms.TextInput(attrs={'class': 'form-control'}),
            'option_c': forms.TextInput(attrs={'class': 'form-control'}),
            'option_d': forms.TextInput(attrs={'class': 'form-control'}),
            'technical_question_answer': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'correct_answer': forms.Select(attrs={'class': 'form-control'}),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
            'test_type': forms.Select(attrs={'class': 'form-control'}),
            'category_type': forms.TextInput(attrs={'class': 'form-control'}),
            'specialisation_name': forms.Select(attrs={'class': 'form-control'}),
            'is_multichoice': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'deleted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        test_type = cleaned_data.get('test_type')
        option_a = cleaned_data.get('option_a')
        option_b = cleaned_data.get('option_b')
        option_c = cleaned_data.get('option_c')
        option_d = cleaned_data.get('option_d')
        technical_question_answer = cleaned_data.get('technical_question_answer')
        specialisation_name = cleaned_data.get('specialisation_name')
        correct_answer = cleaned_data.get('correct_answer')
        is_multichoice = cleaned_data.get('is_multichoice')

        if test_type == 'GT':
            # For General Test, is_multichoice must be True
            cleaned_data['is_multichoice'] = True
            if not option_a:
                self.add_error('option_a', 'Option A is required for General Test.')
            if not option_b:
                self.add_error('option_b', 'Option B is required for General Test.')
            if not option_c:
                self.add_error('option_c', 'Option C is required for General Test.')
            if not option_d:
                self.add_error('option_d', 'Option D is required for General Test.')
            if not correct_answer:
                self.add_error('correct_answer', 'Correct answer is required for General Test.')
            if technical_question_answer:
                self.add_error('technical_question_answer', 'Technical answer is not allowed for General Test.')
        elif test_type == 'TT':
            # For Technical Test, is_multichoice can be True or False
            if is_multichoice:
                # If is_multichoice is True, require options A-D and correct_answer
                if not option_a:
                    self.add_error('option_a', 'Option A is required for multiple-choice Technical Test.')
                if not option_b:
                    self.add_error('option_b', 'Option B is required for multiple-choice Technical Test.')
                if not option_c:
                    self.add_error('option_c', 'Option C is required for multiple-choice Technical Test.')
                if not option_d:
                    self.add_error('option_d', 'Option D is required for multiple-choice Technical Test.')
                if not correct_answer:
                    self.add_error('correct_answer', 'Correct answer is required for multiple-choice Technical Test.')
            else:
                # If is_multichoice is False, require technical_question_answer
                if not technical_question_answer:
                    self.add_error('technical_question_answer', 'Technical answer is required for non-multiple-choice Technical Test.')
                if option_a or option_b or option_c or option_d:
                    self.add_error(None, 'Options A-D are not allowed for non-multiple-choice Technical Test.')
                if correct_answer:
                    self.add_error('correct_answer', 'Correct answer is not allowed for non-multiple-choice Technical Test.')
            if specialisation_name == 'Not Applicable':
                self.add_error('specialisation_name', "Specialisation name cannot be 'Not Applicable' for Technical Test.")
            if not specialisation_name:
                self.add_error('specialisation_name', 'Specialisation name is required for Technical Test.')

        return cleaned_data

class SearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically set choices for specialisation_name
        self.fields['specialisation_name'].choices = [('', 'All Specialisations')] + Question.get_specialisation_choices()

    search_query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search by ID or question text'})
    )
    difficulty = forms.ChoiceField(
        choices=[('', 'All Difficulties'), ('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    test_type = forms.ChoiceField(
        choices=[('', 'All Test Types'), ('GT', 'General Test'), ('TT', 'Technical Test')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    category_type = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category'})
    )
    specialisation_name = forms.ChoiceField(
        choices=[],  # Choices set dynamically in __init__
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )