from django.db import migrations

# Estrutura oficial do gabinete GPIST: 4 departamentos + secção administrativa.
DEPARTAMENTOS = [
    "Obras Públicas",
    "Gestão Urbanística",
    "Conservação das Infraestruturas Urbanas",
    "Promoção Gestão e Reabilitação Urbana",
    "Administrativo",
]


def seed_departments(apps, schema_editor):
    Department = apps.get_model("accounts", "Department")
    for name in DEPARTAMENTOS:
        Department.objects.get_or_create(name=name)


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_department_alter_customuser_departamento"),
    ]

    operations = [
        migrations.RunPython(seed_departments, migrations.RunPython.noop),
    ]
