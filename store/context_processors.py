from django.conf import settings

def isp_branding(request):
	return {'isp_name': settings.ISP_NAME}

