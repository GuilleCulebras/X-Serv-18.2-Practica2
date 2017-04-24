from django.shortcuts import render
from models import Pages
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt

def barra(request):

	if request.method == "GET":
		respuesta = "Introduce una URL <br>"
		respuesta += "<form action='' method='POST'>"
		respuesta += "URL: <input type='text' name='contenido'>"
		respuesta += "<input type='submit' value='Enviar'>"
		respuesta += "</form>"

		pages = Pages.objects.all()
		for page in pages:
			respuesta += "<br>" + str(page.id) + " : " + page.page
		return HttpResponse(respuesta)


	if request.method == "POST":
		url = request.POST['contenido']

		if url == "":
			respuesta = "Not Found. POST method without QS"
			return HttpResponse(respuesta, status = 404)
		else:

			if not (url[0:7] == "http://" or url[0:8] == "https://"):
				url = "http://" + url 
			
			try:
				pagina = Pages.objects.get(page=url)
				respuesta = "La url ya esta asignada <br>"
				respuesta += ("<html><body><a href='" + pagina.page + "'>" + str(pagina.id) + "</a>" +
                                    " : " +
                                    "<a href='" + pagina.page + "'>" + pagina.page + "</a>" +
                                    "</body></html>")

				return HttpResponse(respuesta)

			except Pages.DoesNotExist:
				pagina = Pages(page=url)
				pagina.save()

				respuesta = ("<html><body><a href='" + pagina.page + "'>" + str(pagina.id) + "</a>" +
                                    " : " +
                                    "<a href='" + pagina.page + "'>" + pagina.page + "</a>" +
                                    "</body></html>")
				
				return HttpResponse(respuesta)

def redirect(request, identificador):

	if identificador.isdigit():

		try:
			pagina = Pages.objects.get(id = int(identificador))
			respuesta = "<html><head><meta http-equiv='refresh' content='0; " + "url=" + pagina.page +"'></head>"
			return HttpResponse(respuesta, status = 302)

		except Pages.DoesNotExist:
			respuesta = "ERROR. Recurso no disponible"
			return HttpResponse(respuesta, status = 404)

	else:

		respuesta = "Error, no has introducido un numero"
		return HttpResponse(respuesta)