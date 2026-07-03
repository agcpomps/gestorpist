from datetime import date

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import Department

from .forms import ProjectForm
from .models import Project, Task


@login_required
def project_list(request):
    projects = (
        Project.objects.select_related("department", "manager")
        .prefetch_related("tasks")
    )
    return render(request, "projectos/projectos.html", {"projects": projects})


@login_required
def report(request):
    """Management report: projects by department and by individual."""
    today = date.today()
    nao_terminado = ~Q(status__in=[Project.Status.CONCLUIDO, Project.Status.CANCELADO])

    projects = Project.objects.all()
    kpis = {
        "total": projects.count(),
        "em_curso": projects.filter(status=Project.Status.EM_CURSO).count(),
        "concluidos": projects.filter(status=Project.Status.CONCLUIDO).count(),
        "atrasados": projects.filter(nao_terminado, end_date__lt=today).count(),
    }

    por_departamento = list(
        Department.objects.annotate(
            total=Count("projects", distinct=True),
            em_curso=Count(
                "projects",
                filter=Q(projects__status=Project.Status.EM_CURSO),
                distinct=True,
            ),
            concluidos=Count(
                "projects",
                filter=Q(projects__status=Project.Status.CONCLUIDO),
                distinct=True,
            ),
            atrasados=Count(
                "projects",
                filter=Q(projects__end_date__lt=today)
                & ~Q(projects__status__in=[Project.Status.CONCLUIDO, Project.Status.CANCELADO]),
                distinct=True,
            ),
            tarefas_total=Count("projects__tasks", distinct=True),
            tarefas_concluidas=Count(
                "projects__tasks",
                filter=Q(projects__tasks__status=Task.Status.CONCLUIDA),
                distinct=True,
            ),
        )
        .filter(total__gt=0)
        .order_by("-total", "name")
    )
    for dept in por_departamento:
        dept.progresso = (
            round(dept.tarefas_concluidas / dept.tarefas_total * 100)
            if dept.tarefas_total
            else 0
        )

    por_responsavel = list(
        get_user_model()
        .objects.annotate(
            total=Count("managed_projects", distinct=True),
            em_curso=Count(
                "managed_projects",
                filter=Q(managed_projects__status=Project.Status.EM_CURSO),
                distinct=True,
            ),
            concluidos=Count(
                "managed_projects",
                filter=Q(managed_projects__status=Project.Status.CONCLUIDO),
                distinct=True,
            ),
            tarefas_atribuidas=Count("tasks", distinct=True),
            tarefas_pendentes=Count(
                "tasks",
                filter=~Q(tasks__status=Task.Status.CONCLUIDA),
                distinct=True,
            ),
        )
        .filter(Q(total__gt=0) | Q(tarefas_atribuidas__gt=0))
        .select_related("departamento")
        .order_by("-total", "username")
    )

    context = {
        "kpis": kpis,
        "por_departamento": por_departamento,
        "por_responsavel": por_responsavel,
        "hoje": today,
    }
    return render(request, "projectos/report.html", context)


@login_required
def project_create(request):
    form = ProjectForm(request.POST or None, user=request.user)
    if request.method == "POST" and form.is_valid():
        project = form.save(commit=False)
        project.created_by = request.user
        project.save()
        form.save_m2m()
        messages.success(request, f"Projecto “{project.name}” criado com sucesso.")
        return redirect("projectos:list")
    return render(request, "projectos/form.html", {"form": form, "titulo": "Novo projecto"})


@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if not request.user.manages(project.department_id):
        return HttpResponseForbidden("Sem permissão para gerir projectos deste departamento.")
    form = ProjectForm(request.POST or None, instance=project, user=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"Projecto “{project.name}” actualizado.")
        return redirect("projectos:list")
    return render(request, "projectos/form.html", {"form": form, "titulo": "Editar projecto"})


@login_required
def project_delete(request, pk):
    if request.method == "DELETE":
        project = get_object_or_404(Project, pk=pk)
        if not request.user.manages(project.department_id):
            return HttpResponseForbidden("Sem permissão para gerir projectos deste departamento.")
        project.delete()
        return HttpResponse(status=200)
    return HttpResponse(status=405)
