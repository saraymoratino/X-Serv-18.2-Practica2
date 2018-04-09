from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import urls
import urllib

# Create your views here.

def htmlanswer():

	answer = "<html><body>"
	answer += "<form id='formulario' action='' method='POST'>"
	answer += "<fieldset><legend><b style= 'color:blue'>Acortador de url's</b></legend>"
	answer += "<label>URL: </label>"
	answer += "<input type='text' name='url' placeholder='Introduce la URL' value='' style='color:grey'/>"
	answer += "<input type='submit' value='Send' /></fieldset></form>"
	answer += '<p><h5 style =color:green> Lista de URLS </h5></p>'

	for url in urls.objects.all():
		identificador = url.id
		url = url.url_original
		short_url = 'localhost:8000/' + str(identificador)
		answer += '<a href=' + url + '>' + url + '</a>' + ' <---> ' + '<a href=' + url + '>' + short_url + '</a><br>'	 

	answer += "</body></html>"
	return answer
	
	
@csrf_exempt	
def pag_principal(request):
	recurso = request.method
	#print(str(recurso))
	if recurso == 'GET':
		html_answer = htmlanswer()
		return HttpResponse(html_answer)

	elif recurso == 'POST':
		original_url = urllib.parse.unquote (request.POST.get('url'))
		if not original_url.startswith("http://") and not original_url.startswith("https://"):
			original_url = "http://" + original_url

		try:
			url_BBDD = urls.objects.get(url_original = original_url)
		except urls.DoesNotExist:
			urls(url_original = original_url).save()

		html_answer = htmlanswer()
		return HttpResponse(html_answer)
		
	else:
		return HttpResponse("Recurso no valido")
	
	
def buscar_BBDD(request, recurso):
	identificador = recurso
	try:
		url = urls.objects.get(id = identificador).url_original
		html_answer = '<html><body><meta http-equiv="Refresh" content=' + "3;url=" + url + '>'
		html_answer += '<h2>Redirigiendo...</h2></body></html>'
	except urls.DoesNotExist:
		html_answer = '<html><body><meta http-equiv="Refresh" content=' + "2;url=" + 'http://localhost:8000' + '>'
		html_answer += '<h2><a style="color:red">404 Not Found.</a></h2>'
		html_answer += '<h4>Redirigiendo al formulario...</h4></body></html>'
		pass

	return HttpResponse(html_answer)
	
	
	
