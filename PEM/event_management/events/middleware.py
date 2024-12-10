from django.shortcuts import render, redirect


def auth_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        if (request.path == '/index/') and (request.session.get('id') is None) :
                return redirect('/login/')
        
        if (request.path == '/login/' or request.path == 'signup/') and (request.session.get('id') is not None) :
                return redirect('/')
        

        response = get_response(request)

        return response

    return middleware