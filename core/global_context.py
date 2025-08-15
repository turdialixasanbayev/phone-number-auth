from datetime import datetime


def global_context(request):
    context = {
        'site_name': 'Phone Number Auth',
        'user': request.user,
        'current_year': datetime.now().year
    }
    return context
