import pandas as pd
from django.shortcuts import render, redirect,get_object_or_404
from django.db.models import Q
from matching.models import DebtorExcelBase, ClaimerExcelBase
from compare.models import ComparisonResult
from compare.forms import ComparisonForm


def select_files(request):
    if request.method == 'POST':
        form = ComparisonForm(request.POST)
        if form.is_valid():
            key_columns = form.cleaned_data['key_columns']
            non_key_columns = form.cleaned_data['non_key_columns']

            # Fetch records from the database
            debtor_records = DebtorExcelBase.objects.all()
            claimer_records = ClaimerExcelBase.objects.all()

            # Perform comparison
            results = compare_data(debtor_records, claimer_records, key_columns, non_key_columns)

            # Save comparison results to the database
            for result in results:
                ComparisonResult.objects.create(
                    debtor_id=result.get('debtor_record_id'),
                    claimer_id=result.get('claimer_record_id'),
                    debtor_data=result.get('debtor_data', {}),
                    claimer_data=result.get('claimer_data', {}),
                    status=result.get('status', ''),
                    description=result.get('description', '')
                )

            return redirect('results')  # Redirect to the 'results' view

    else:
        form = ComparisonForm()

    return render(request, 'compare/select_files.html', {'form': form})

def compare_data(debtor_records, claimer_records, key_columns, non_key_columns):
    comparison_results = []

    # Convert the records to DataFrames for easier comparison
    debtor_df = pd.DataFrame(list(debtor_records.values(*key_columns, *non_key_columns)))
    claimer_df = pd.DataFrame(list(claimer_records.values(*key_columns, *non_key_columns)))

    # Perform the merge based on the selected key columns
    merged_df = pd.merge(debtor_df, claimer_df, on=key_columns, how='outer', suffixes=('_debtor', '_claimer'))

    for _, row in merged_df.iterrows():
        result = {
            'debtor_record_id': row.get('id_debtor'),
            'claimer_record_id': row.get('id_claimer'),
            'debtor_data': row.filter(like='_debtor').to_dict(),
            'claimer_data': row.filter(like='_claimer').to_dict(),
            'status': 'Green',
            'description': 'Everything matches.',
        }

        # Check for NaN values
        if row.isnull().any():
            result['status'] = 'Red'
            result['description'] = 'One or more columns contain NaN values.'

        # Check for mismatches in non-key columns
        else:
            for column in non_key_columns:
                debtor_value = row.get(f'{column}_debtor')
                claimer_value = row.get(f'{column}_claimer')

                if debtor_value != claimer_value:
                    result['status'] = 'Yellow'
                    result['description'] = f'Mismatch in column "{column}": Debtor="{debtor_value}", Claimer="{claimer_value}".'
                    break

        comparison_results.append(result)

    return comparison_results

def results(request):
    comparison_results = ComparisonResult.objects.all()
    context = {
        'results': comparison_results
    }
    return render(request, 'compare/results.html', context)


def delete_comparison_result(request, id):
    result = get_object_or_404(ComparisonResult, id=id)
    if request.method == 'POST':
        result.delete()
        return redirect('comparefiles:results')
    # Optionally, render a confirmation page
    return redirect('comparefiles:results')
