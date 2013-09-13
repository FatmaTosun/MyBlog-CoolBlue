from django.contrib.auth.models import User, check_password

class EmailAuthBackend(object):
    """
    Email Authentication Backend
    
    """
    
    def authenticate(self, email, password):
        """ Authenticate a user based on email address as the user name. """
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None 


    def get_user(self, user_id):
        """Get a User object from the user_id. """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None