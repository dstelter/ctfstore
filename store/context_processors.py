

# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.urlresolvers import resolve


def isp_branding(request):
	return {'isp_name': settings.ISP_NAME}

def navigation(request):
	return {'nav_active': resolve(request.path_info).url_name,
	        'nav_items': [
	            ('home', 'Übersicht'),
	            ('achievements', 'Bonusprogramm'),
	            ('upgrades', 'Tarifoptionen'),
	            ('contact', 'Kontakt'),
	            ('career', 'Karriere')
	        ]
	}