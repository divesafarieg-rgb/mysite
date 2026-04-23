from django import forms


class OrderImportForm(forms.Form):
    csv_file = forms.FileField(
        label="CSV файл с заказами",
        help_text="Файл должен содержать колонки: delivery_address, promocode, user_id, product_ids (через запятую)",
        widget=forms.FileInput(attrs={'accept': '.csv'})
    )

    def clean_csv_file(self):
        csv_file = self.cleaned_data['csv_file']

        if not csv_file.name.endswith('.csv'):
            raise forms.ValidationError('Пожалуйста, загрузите файл в формате CSV')

        if csv_file.size > 5 * 1024 * 1024:
            raise forms.ValidationError('Файл слишком большой (максимум 5MB)')

        return csv_file