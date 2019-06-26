"""
WSGI config for emt7ank project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
import sys


path = "/home/elshafeay/emt7ank/backend"

if path not in sys.path:
	sys.path.append(path)


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emt7ank.deploy_settings')

application = get_wsgi_application()
