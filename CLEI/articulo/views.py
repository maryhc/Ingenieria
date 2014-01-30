from django.http      import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response

from articulo.forms   import ArticuloForm, AutorForm
from articulo.models  import Articulo, Autor, Palabra_Clave_Articulo
from clei.models      import Topico
from reportlab.pdfgen import canvas

def articulo_index(request):
    num_articulos = Articulo.objects.count()
    return render_to_response('articulo/articulo_index.html', 
                              {'objeto_int' : num_articulos})

def articulo_mostrar_autor(request):
    articulos = Articulo.objects.all()
    return render_to_response('articulo/articulo_lista.html',
                              {'objeto_lista' : articulos})

def articulo_mostrar_topicos(request):
    topicos = Topico.objects.all()
    return render_to_response('articulo/articulo_topicos.html',
                              {'objeto_lista' : topicos})

def articulo_detalles(request, pk):
    try:
        articulo = Articulo.objects.get(pk=pk)
    except Articulo.DoesNotExist:
        raise Http404

    return render_to_response('articulo/articulo_detalles.html',
                              {'objeto' : articulo})

def articulo_agregar(request):
    if request.POST:
        articulo_instancia = Articulo()
        crear_form = ArticuloForm(instance=articulo_instancia, data=request.POST)
        if crear_form.is_valid():
            palabras_clave = crear_form.cleaned_data['palabras_clave']
            lista = palabras_clave.split(',')
            crear_form.save()
            for p in lista:
                p_clave = Palabra_Clave_Articulo(palabra=p)
                p_clave.save()
                p_clave.articulo.add(articulo_instancia)
                p_clave.save()
            return HttpResponseRedirect('exito')
    else:
        crear_form = ArticuloForm()

    return render(request, 'articulo/articulo_agregar.html', {
        'form': crear_form,
    })

def autor_registrar(request):
    if request.POST:
        crear_form = AutorForm(request.POST)
        if crear_form.is_valid():
            crear_form.save()
            return HttpResponseRedirect('exito')
    else:
        crear_form = AutorForm()

    return render(request, 'articulo/autor_agregar.html', {
        'form' : crear_form,
    })

def autor_listar(request):
    autores = Autor.objects.all()
    return render_to_response('articulo/autor_lista.html',
                              {'objeto_lista' : autores})

def autor_detalles(request, pk):
    try:
        autor = Autor.objects.get(pk=pk)
    except Autor.DoesNotExist:
        raise Http404

    return render_to_response('articulo/autor_detalles.html',
                              {'objeto' : autor})

def to_pdf(request):

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="download.pdf"'
    
    articulo_list = Articulo.objects.all().order_by('titulo')

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)
    i = 740
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    if articulo_list:
        for a in articulo_list:
            if i>=100:
                p.drawString(100, i, a.titulo)
            i = i-20
    else:
        p.drawString(100, 740, "No hay articulos")
    
    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response
