from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.http import JsonResponse
from django.urls import resolve
from django.shortcuts import redirect

class JWTAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if resolve(request.path).url_name in ['login_page', 'send-otp', 'verify-otp']:
            return

        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')

        if access_token:
            try:
                AccessToken(access_token)
                request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
            except Exception:
                new_access_token = self.refresh_access_token(refresh_token)
                if new_access_token:
                    request.META['HTTP_AUTHORIZATION'] = f'Bearer {new_access_token}'
                    request._new_access_token = new_access_token
                else:
                    return redirect('login_page')
        elif refresh_token:
            new_access_token = self.refresh_access_token(refresh_token)
            if new_access_token:
                request.META['HTTP_AUTHORIZATION'] = f'Bearer {new_access_token}'
                request._new_access_token = new_access_token
            else:
                return redirect('login_page')
        else:
            return redirect('login_page')

    def process_response(self, request, response):
        new_access_token = getattr(request, '_new_access_token', None)
        if new_access_token:
            response.set_cookie('access_token', new_access_token, httponly=True, max_age=60 * 10)
        return response

    def refresh_access_token(self, refresh_token):
        if refresh_token:
            try:
                return str(RefreshToken(refresh_token).access_token)
            except Exception:
                return None
        return None
