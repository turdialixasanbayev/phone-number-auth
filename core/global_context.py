def global_context(request):
    context = {
        'site_name': 'Phone Number Auth',
        'user': request.user
    }
    return context
