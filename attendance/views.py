import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StudentImportForm
from .models import Student

def import_students(request):
    if request.method == "POST":
        form = StudentImportForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data["file"]
            try:
                if file.name.endswith(".csv"):
                    df = pd.read_csv(file)
                elif file.name.endswith((".xls", ".xlsx")):
                    df = pd.read_excel(file)
                else:
                    messages.error(request, "Unsupported file format.")
                    return redirect("import_students")

                required_columns = {"admission_number", "full_name", "parent_phone"}
                if not required_columns.issubset(set(df.columns)):
                    messages.error(request, f"Missing required columns: {required_columns}")
                    return redirect("import_students")

                added, skipped = 0, 0
                for _, row in df.iterrows():
                    admission_number = str(row["admission_number"]).strip()
                    full_name = str(row["full_name"]).strip()
                    parent_phone = str(row["parent_phone"]).strip()

                    if not Student.objects.filter(admission_number=admission_number).exists():
                        Student.objects.create(
                            admission_number=admission_number,
                            full_name=full_name,
                            parent_phone=parent_phone,
                            class_name=row.get("class_name", ""),
                            entry_year=row.get("entry_year"),
                            education_cycle=row.get("education_cycle", 4),
                            is_active=True
                        )
                        added += 1
                    else:
                        skipped += 1

                messages.success(request, f"{added} students added. {skipped} were skipped (already exist).")
                return redirect("import_students")

            except Exception as e:
                messages.error(request, f"Error processing file: {e}")
    else:
        form = StudentImportForm()

    return render(request, "attendance/import_students.html", {"form": form})
