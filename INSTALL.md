Installation instructions
=========================
Development and production setup instructions.

Development setup
-----------------
Create and activate a Python 3 virtual environment with the requirements listed
in `gamenightplanner/__init__.py`. Create a new Django project and add these
settings:

    import sys

    # Include the Game Night Planner path
    sys.path.append("path_to_directory_of_gamenightplanner")

    SITE_ID = 1

    INSTALLED_APPS = [
        ...
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'social_django',
        'invitations',
        'gamenightplanner',
    ]

    MIDDLEWARE = [
        ...
        'social_django.middleware.SocialAuthExceptionMiddleware',
    ]

    ROOT_URLCONF = 'gamenightplanner.urls'

    AUTHENTICATION_BACKENDS = [
        # Add whichever backends you like, here there is just OpenID
        'social_core.backends.open_id.OpenIdAuth',
        ...
        # If you require password login, include this as well. You
        # might need it for admin interface for example.
        'django.contrib.auth.backends.ModelBackend',
    ]

    LOGIN_URL = 'account:login'
    LOGOUT_REDIRECT_URL = 'main'

    # Social auth
    SOCIAL_AUTH_PIPELINE = (
        'gamenightplanner.account.is_signup',
        'gamenightplanner.account.check_verified_email',
        'social_core.pipeline.social_auth.social_details',
        'social_core.pipeline.social_auth.social_uid',
        'social_core.pipeline.social_auth.auth_allowed',
        'social_core.pipeline.social_auth.social_user',
        'gamenightplanner.account.signup',
        'social_core.pipeline.social_auth.associate_user',
        'social_core.pipeline.social_auth.load_extra_data',
        'social_core.pipeline.user.user_details',
    )

    SOCIAL_AUTH_LOGIN_ERROR_URL = 'main'
    SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'main'
    SOCIAL_AUTH_RAISE_EXCEPTIONS = False

    # Invitations
    INVITATIONS_SIGNUP_REDIRECT = 'account:signup'
    INVITATIONS_LOGIN_REDIRECT = 'main'
    INVITATIONS_INVITATION_ONLY = True
    INVITATIONS_ACCEPT_INVITE_AFTER_SIGNUP = True
    INVITATIONS_GONE_ON_ACCEPT_ERROR = False
    INVITATIONS_ADAPTER = 'gamenightplanner.account.InvitationAdapter'

In addition, you may want to include some email settings, if you are testing
invitations. You may modify these settings however you think is best.

Production setup
----------------
To be done.
