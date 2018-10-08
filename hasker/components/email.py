# E-mail settings

EMAIL_HOST = ''
EMAIL_PORT = 465
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_SSL = True

EMAIL_FROM = ''
EMAIL_MESSAGES = {
    'sign_up': [
        'Hasker - registration',
        'Hello!<br>You are now signed up. Your login: <%LOGIN%> <br><br>'
    ],
    'new_answer': [
        'Hasker - added new answer to your question',
        'Hello!<br>New answer to your question has been added. You can find it on this page: <%LINK%> <br><br>'
    ]
}

EMAIL_SIGN = 'With best wishes,<br>Hasker'