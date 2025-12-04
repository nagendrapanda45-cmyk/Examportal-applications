from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime, timedelta
from django.http import HttpResponse
from home.users.models import Question, Configuration
from .forms import QuestionForm, SearchForm
import pandas as pd
import io
import os
from django.conf import settings
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Font, Alignment

current_year = datetime.now().year

# @login_required
def question_list(request):
    form = SearchForm(request.GET or None)
    questions = Question.objects.filter(deleted=False).order_by('-question_id')  # Filter out deleted questions


    if request.GET and form.is_valid():
        search_query = form.cleaned_data.get('search_query')
        difficulty = form.cleaned_data.get('difficulty')
        test_type = form.cleaned_data.get('test_type')
        category_type = form.cleaned_data.get('category_type')
        specialisation_name = form.cleaned_data.get('specialisation_name')

        # Apply general search query filter
        if search_query:
            questions = questions.filter(
                Q(question_id__exact=search_query) if search_query.isdigit() else
                Q(question_text__icontains=search_query)
            )

        # Apply dropdown filters
        if difficulty:
            questions = questions.filter(difficulty__iexact=difficulty)
        if test_type:
            questions = questions.filter(test_type__iexact=test_type)
        if category_type:
            questions = questions.filter(category_type__iexact=category_type)
        if specialisation_name:
            questions = questions.filter(specialisation_name__iexact=specialisation_name)

    # Paginate the questions
    paginator = Paginator(questions, 10)  # 10 questions per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'questions': page_obj,
        'form': form,
        'page_obj': page_obj,
    }
    return render(request, 'questions/question_list.html', context)

# @login_required
def question_add(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            if question.test_type == 'GT':
                question.is_multichoice = True  # Enforce is_multichoice=True for GT
            question.save()
            return redirect('question_list')
    else:
        form = QuestionForm()
    return render(request, 'questions/question_form.html', {'form': form})

# @login_required
def question_edit(request, question_id):
    question = get_object_or_404(Question, question_id=question_id, deleted=False)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            if question.test_type == 'GT':
                question.is_multichoice = True  # Enforce is_multichoice=True for GT
            question.save()
            return redirect('question_list')
    else:
        form = QuestionForm(instance=question)
    return render(request, 'questions/question_edit.html', {'form': form})

# @login_required
def question_delete(request, question_id):
    question = get_object_or_404(Question, question_id=question_id, deleted=False)
    if request.method == 'POST':
        question.deleted = True  # Soft delete by setting deleted=True
        question.save()
        return redirect('question_list')
    return render(request, 'questions/question_confirm_delete.html', {'question': question})

# @login_required
def question_import(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        if not file:
            messages.error(request, 'No file uploaded.')
            return render(request, 'questions/question_import.html')

        try:
            # Expected columns
            expected_columns = [
                'question_text', 'option_a', 'option_b', 'option_c', 'option_d',
                'technical_question_answer', 'correct_answer', 'difficulty',
                'test_type', 'category_type', 'specialisation_name', 'is_multichoice', 'is_active', 'deleted'
            ]

            # Determine file type and read with pandas
            file_extension = file.name.split('.')[-1].lower()
            if file_extension == 'csv':
                df = pd.read_csv(file)
            elif file_extension in ['xlsx', 'xls']:
                df = pd.read_excel(file)
            else:
                messages.error(request, 'Unsupported file format. Please upload a CSV or Excel file.')
                return render(request, 'questions/question_import.html')

            # Validate columns
            missing_columns = [col for col in expected_columns if col not in df.columns]
            if missing_columns:
                messages.error(request, f'Missing columns in file: {", ".join(missing_columns)}')
                return render(request, 'questions/question_import.html')

            # Drop any unexpected columns
            df = df[expected_columns]

            # Get valid specialisation names (hardcoded + DB)
            hardcoded_specialisations = ['Python', 'Java', 'C', 'C++', '.NET', 'Java Script', 'Not Applicable']
            db_specialisations = list(Configuration.objects.filter(key=f'primary_skills_{current_year}', deleted=False).values_list('value', flat=True))
            valid_specialisations = hardcoded_specialisations + [s for s in db_specialisations if s not in hardcoded_specialisations]
            valid_specialisations_lower = [s.lower() for s in valid_specialisations]

            # Valid values
            valid_correct_answers = ['A', 'B', 'C', 'D']
            valid_test_types = ['GT', 'TT']
            valid_difficulties = ['easy', 'medium', 'hard']
            valid_category_types = ['Aptitude', 'Coding', 'Reasoning']

            # Process each row
            success_count = 0
            error_messages = []
            for index, row in df.iterrows():
                try:
                    # Skip rows with missing or invalid question_text
                    question_text = str(row['question_text']).strip() if pd.notna(row['question_text']) else ''
                    if not question_text or question_text.lower() in ['note', 'field', 'allowed values']:
                        continue

                    # Read test_type and is_multichoice first
                    test_type = str(row['test_type']).strip() if pd.notna(row['test_type']) else None
                    is_multichoice = bool(row['is_multichoice']) if pd.notna(row['is_multichoice']) else False

                    # Normalize and validate test_type
                    if test_type:
                        test_type = test_type.upper()
                        if test_type in ['TECHNICAL TEST', 'TECHNICAL', 'TT (TECHNICAL TEST)']:
                            test_type = 'TT'
                        elif test_type in ['GENERAL TEST', 'GENERAL', 'GT (GENERAL TEST)']:
                            test_type = 'GT'
                        if test_type not in valid_test_types:
                            raise ValueError(f"Invalid test_type: '{test_type}'. Must be one of {valid_test_types}.")
                    else:
                        raise ValueError("test_type is required.")

                    # Initialize data dictionary with default values
                    data = {
                        'question_text': question_text,
                        'option_a': None,
                        'option_b': None,
                        'option_c': None,
                        'option_d': None,
                        'technical_question_answer': None,
                        'correct_answer': None,
                        'difficulty': str(row['difficulty']).lower() if pd.notna(row['difficulty']) else None,
                        'test_type': test_type,
                        'category_type': str(row['category_type']).title() if pd.notna(row['category_type']) else None,
                        'specialisation_name': str(row['specialisation_name']).title() if pd.notna(row['specialisation_name']) else 'Not Applicable',
                        'is_multichoice': is_multichoice,
                        'is_active': bool(row['is_active']) if pd.notna(row['is_active']) else True,
                        'deleted': bool(row['deleted']) if pd.notna(row['deleted']) else False,
                    }

                    # Validate specialisation_name
                    if data['specialisation_name'].lower() not in valid_specialisations_lower:
                        raise ValueError(f"Invalid specialisation_name: '{data['specialisation_name']}'")

                    # Validate difficulty
                    if data['difficulty'] and data['difficulty'] not in valid_difficulties:
                        raise ValueError(f"Invalid difficulty: '{data['difficulty']}'. Must be one of {valid_difficulties}")

                    # Validate category_type
                    if data['category_type'] and data['category_type'] not in valid_category_types:
                        raise ValueError(f"Invalid category_type: '{data['category_type']}'. Must be one of {valid_category_types}")

                    if test_type == 'GT':
                        # Enforce is_multichoice=True for GT
                        data['is_multichoice'] = True
                        # Read multiple-choice fields
                        data['option_a'] = str(row['option_a']) if pd.notna(row['option_a']) else None
                        data['option_b'] = str(row['option_b']) if pd.notna(row['option_b']) else None
                        data['option_c'] = str(row['option_c']) if pd.notna(row['option_c']) else None
                        data['option_d'] = str(row['option_d']) if pd.notna(row['option_d']) else None
                        correct_answer = str(row['correct_answer']).strip() if pd.notna(row['correct_answer']) else None

                        # Validate multiple-choice fields
                        if not all([data['option_a'], data['option_b'], data['option_c'], data['option_d']]):
                            raise ValueError("All options (A-D) are required for General Test.")
                        if not correct_answer:
                            raise ValueError("Correct answer is required for General Test.")
                        # Normalize and validate correct_answer
                        correct_answer = correct_answer.upper()
                        if correct_answer.startswith('OPTION '):
                            correct_answer = correct_answer[7:8]
                        options = {
                            'A': data['option_a'],
                            'B': data['option_b'],
                            'C': data['option_c'],
                            'D': data['option_d'],
                        }
                        for key, value in options.items():
                            if value and correct_answer == value:
                                correct_answer = key
                                break
                        if correct_answer not in valid_correct_answers:
                            raise ValueError(f"Invalid correct_answer: '{correct_answer}'. Must be one of {valid_correct_answers} or match an option (A-D).")
                        data['correct_answer'] = correct_answer
                        # Check for technical_question_answer
                        if pd.notna(row['technical_question_answer']) and str(row['technical_question_answer']).strip():
                            raise ValueError("technical_question_answer is not allowed for General Test.")

                    elif test_type == 'TT':
                        if is_multichoice:
                            # Read multiple-choice fields
                            data['option_a'] = str(row['option_a']) if pd.notna(row['option_a']) else None
                            data['option_b'] = str(row['option_b']) if pd.notna(row['option_b']) else None
                            data['option_c'] = str(row['option_c']) if pd.notna(row['option_c']) else None
                            data['option_d'] = str(row['option_d']) if pd.notna(row['option_d']) else None
                            correct_answer = str(row['correct_answer']).strip() if pd.notna(row['correct_answer']) else None
                            # Validate multiple-choice fields
                            if not all([data['option_a'], data['option_b'], data['option_c'], data['option_d']]):
                                raise ValueError("All options (A-D) are required for multiple-choice Technical Test.")
                            if not correct_answer:
                                raise ValueError("Correct answer is required for multiple-choice Technical Test.")
                            # Normalize and validate correct_answer
                            correct_answer = correct_answer.upper()
                            if correct_answer.startswith('OPTION '):
                                correct_answer = correct_answer[7:8]
                            options = {
                                'A': data['option_a'],
                                'B': data['option_b'],
                                'C': data['option_c'],
                                'D': data['option_d'],
                            }
                            for key, value in options.items():
                                if value and correct_answer == value:
                                    correct_answer = key
                                    break
                            if correct_answer not in valid_correct_answers:
                                raise ValueError(f"Invalid correct_answer: '{correct_answer}'. Must be one of {valid_correct_answers} or match an option (A-D).")
                            data['correct_answer'] = correct_answer
                            # Check for technical_question_answer
                            if pd.notna(row['technical_question_answer']) and str(row['technical_question_answer']).strip():
                                raise ValueError("technical_question_answer is not allowed for multiple-choice Technical Test.")
                        else:
                            # Read technical_question_answer
                            data['technical_question_answer'] = str(row['technical_question_answer']) if pd.notna(row['technical_question_answer']) else None
                            # Validate technical_question_answer
                            # if not data['technical_question_answer']:
                            #     raise ValueError("technical_question_answer is required for non-multiple-choice Technical Test.")
                            # Check for options and correct_answer
                            if any([pd.notna(row[col]) and str(row[col]).strip() for col in ['option_a', 'option_b', 'option_c', 'option_d', 'correct_answer']]):
                                raise ValueError("Options A-D and correct_answer are not allowed for non-multiple-choice Technical Test.")
                        # Validate specialisation_name for TT
                        if data['specialisation_name'] == 'Not Applicable':
                            raise ValueError("specialisation_name cannot be 'Not Applicable' for Technical Test.")

                    # Save the question
                    question = Question(**data)
                    question.save()
                    success_count += 1

                except Exception as e:
                    error_messages.append(f"Row {index + 2}: {str(e)}")

            # Provide feedback
            if success_count > 0:
                messages.success(request, f'Successfully imported {success_count} questions.')
            if error_messages:
                messages.error(request, f'Errors in {len(error_messages)} rows: {" | ".join(error_messages)}')
            return redirect('question_list')

        except Exception as e:
            messages.error(request, f'Error processing file: {str(e)}')
            return render(request, 'questions/question_import.html')

    return render(request, 'questions/question_import.html')

# @login_required
def download_reference_excel(request):
    # Define the column headings based on the Question model
    columns = [
        'question_text', 'option_a', 'option_b', 'option_c', 'option_d',
        'technical_question_answer', 'correct_answer', 'difficulty',
        'test_type', 'category_type', 'specialisation_name', 'is_multichoice', 'is_active', 'deleted'
    ]

    main_df = pd.DataFrame(columns=columns)

    # Create data for the reference table
    reference_data = {
        'Field': ['difficulty', 'test_type', 'category_type', 'specialisation_name', 'correct_answer', 'is_multichoice', 'is_active', 'deleted'],
        'Allowed Values': [
            'easy, medium, hard',
            'GT (General Test), TT (Technical Test)',
            'Aptitude, Coding, Reasoning',
            'Python, Java, C, C++, .NET, Java Script, Not Applicable',
            'A, B, C, D (or the exact option value, e.g., "2" for option_a="2")',
            'True for GT, True/False for TT (True enables multiple-choice options)',
            'Default: True',
            'Default: False'
        ]
    }
    reference_df = pd.DataFrame(reference_data)

    # Create a new workbook and select the active sheet
    wb = Workbook()
    ws = wb.active
    ws.title = 'Question Reference'

    # Write the main table (headings + example row)
    for r_idx, row in enumerate(dataframe_to_rows(main_df, index=False, header=True), 1):
        for c_idx, value in enumerate(row, 1):
            ws.cell(row=r_idx, column=c_idx, value=value)

    # Write the reference table starting at Q1 (column 17, after 3-column gap: N, O, P)
    ws['Q1'] = 'Note: Use exact values from Allowed Values for the fields below'
    ws['Q1'].font = Font(bold=True)
    for r_idx, row in enumerate(dataframe_to_rows(reference_df, index=False, header=True), 2):
        for c_idx, value in enumerate(row, 1):
            ws.cell(row=r_idx, column=c_idx + 16, value=value)  # Offset by 16 columns (A-M for main, N-P gap, Q starts note)

    # Adjust column widths for better readability
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = max_length + 2
        ws.column_dimensions[column].width = adjusted_width

    # Create a buffer to store the Excel file
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    # Ensure the media/reference directory exists
    reference_dir = os.path.join(settings.MEDIA_ROOT, 'reference')
    os.makedirs(reference_dir, exist_ok=True)

    # Save the Excel file to media/reference
    file_path = os.path.join(reference_dir, 'question_reference.xlsx')
    with open(file_path, 'wb') as f:
        f.write(buffer.getvalue())

    # Serve the file for download
    response = HttpResponse(
        buffer,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="question_reference.xlsx"'
    return response