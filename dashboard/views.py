import json
from functools import wraps
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ReportForm
from .models import Report, ActionAlert


def officer_required(view_func):
    """Decorator: only government officers can access the view."""
    @wraps(view_func)
    @login_required
    def _wrapped(request, *args, **kwargs):
        user = request.user
        if hasattr(user, 'profile') and user.profile.is_officer:
            return view_func(request, *args, **kwargs)
        messages.error(request, 'Access denied. Only government officers can view the dashboard.')
        return redirect('dashboard:index')
    return _wrapped


@login_required
def index(request):
    return render(request, 'index.html')


@login_required
@officer_required
def dashboard_home(request):
    reports = Report.objects.all().order_by('-created_at')
    high_risk_count = reports.filter(risk_level='high').count()
    medium_risk_count = reports.filter(risk_level='medium').count()
    low_risk_count = reports.filter(risk_level='low').count()
    pending_count = reports.filter(status='pending').count()
    in_progress_count = reports.filter(status='in_progress').count()
    resolved_count = reports.filter(status='resolved').count()

    # Status update from POST
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'update_status':
            report_id = request.POST.get('report_id')
            new_status = request.POST.get('new_status')
            if report_id and new_status in dict(Report.STATUS_CHOICES):
                report = Report.objects.filter(id=report_id).first()
                if report:
                    report.status = new_status
                    report.save()
                    messages.success(request, f'Status updated for "{report.title}" → {new_status.replace("_", " ").title()}.')
        elif action == 'issue_alert':
            alert_title = request.POST.get('alert_title')
            alert_message = request.POST.get('alert_message')
            priority = request.POST.get('priority', 'normal')
            report_id = request.POST.get('alert_report')
            report = Report.objects.filter(id=report_id).first() if report_id else None
            if alert_title and alert_message:
                ActionAlert.objects.create(
                    title=alert_title,
                    message=alert_message,
                    priority=priority,
                    issued_by=request.user,
                    report=report,
                )
                messages.success(request, 'Immediate action instruction issued successfully.')
        return redirect('dashboard:dashboard-home')

    alerts = ActionAlert.objects.all().order_by('-created_at')
    latest_report = reports.first()

    return render(request, 'dashboard/dashboard_home.html', {
        'total_reports': reports.count(),
        'high_risk_count': high_risk_count,
        'medium_risk_count': medium_risk_count,
        'low_risk_count': low_risk_count,
        'pending_count': pending_count,
        'in_progress_count': in_progress_count,
        'resolved_count': resolved_count,
        'latest_report': latest_report,
        'reports': reports,
        'alerts': alerts,
        'status_choices': Report.STATUS_CHOICES,
    })


@login_required
def risk_map(request):
    reports = Report.objects.all()
    report_data = [
        {
            'title': report.title,
            'description': report.description,
            'risk_level': report.risk_level,
            'status': report.status,
            'latitude': report.latitude,
            'longitude': report.longitude,
            'created_at': report.created_at.strftime('%b %d, %Y %H:%M') if report.created_at else '',
            'image': report.image.url if report.image else '',
        }
        for report in reports
    ]
    reports_json = json.dumps(report_data)
    return render(request, 'dashboard/risk_map.html', {
        'reports_json': reports_json,
        'report_list': reports.order_by('-created_at'),
        'total_reports': reports.count(),
        'high_risk_count': reports.filter(risk_level='high').count(),
        'medium_risk_count': reports.filter(risk_level='medium').count(),
        'low_risk_count': reports.filter(risk_level='low').count(),
    })


@login_required
def report_breeding_spot(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.reported_by = request.user
            report.save()
            messages.success(request, 'Your breeding spot report was submitted successfully.')
            return redirect('dashboard:report-breeding-spot')
    else:
        form = ReportForm()
    return render(request, 'dashboard/report_form.html', {'form': form})
