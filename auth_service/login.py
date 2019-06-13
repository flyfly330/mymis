from django.contrib import auth


class Login(object):

    @staticmethod
    def handle_login(request, user_name, password):
        user = auth.authenticate(username=user_name, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            data = {
                'user_name': user.username,
                'email': user.email,
                'is_authenticated': user.is_authenticated.value
            }
            return data
        else:
            raise Exception("Log in failed")

    @staticmethod
    def handle_logout(request):
        auth.logout(request)
        return True
