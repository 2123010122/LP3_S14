from django.shortcuts import render, HttpResponse, redirect
from miapp.models import Articulo,Autor
from miapp.forms import FormArticulo
from django.contrib import messages

# Create your views here.
layout = """
    <h1> Proyecto Web (LP3 - 2024) | Flor Cerdán </h1>
    <hr/>
    <ul>
        <li>
            <a href="/inicio"> Inicio</a>
        </li>
        <li>
            <a href="/saludo"> Mensaje de Saludo</a>
        </li>
        <li>
            <a href="/rango"> Mostrar Números [a,b]</a>
        </li>
         <li>
            <a href="/rango2/10/15"> Mostrar Números [10,15]</a>
        </li>

    </ul>
    <hr/>
"""

def index(request):
    estudiantes = [ 'Diego Caballero', 
                    'Jeampier Barrios',
                    'Javier Pablo',
                    'Yesenia Zuñiga']
    #estudiantes = [ ]
    return render(request,'index.html', {
        'titulo':'Inicio',
        #'mensaje':'Proyecto Web Con DJango',
        'estudiantes': estudiantes
    })
 
def saludo(request):
    return render(request,'saludo.html',{
        'titulo':'Saludo',
        'autor_saludo':'Mg. Flor Elizabeth Cerdán León'
    })

def rango(request):
    a = 10
    b = 20
    rango_numeros = range(a,b+1)
    return render(request,'rango.html',{
        'titulo':'Rango',
        'a':a,
        'b':b,
        'rango_numeros':rango_numeros
    })

def rango2(request,a=0,b=100):
    if a>b:
        return redirect('rango2',a=b, b=a)
    resultado = f"""
        <h2> Números de [{a},{b}] </h2>
        Resultado: <br>
        <ul> 
    """
    
    while a<=b:
        resultado +=  f"<li> {a} </li>"
        a+=1
    resultado += "</ul"
    return HttpResponse(layout + resultado)

def crear_articulo(request,titulo, contenido, publicado):
    articulo = Articulo(
        titulo = titulo,
        contenido = contenido,
        publicado = publicado
    )
    articulo.save()
    return HttpResponse(f"Articulo Creado: {articulo.titulo} - {articulo.contenido}")

def buscar_articulo(request):
    try:
        articulo = Articulo.objects.get(id=1)
        resultado = f"""Articulo: 
                        <br> <strong>ID:</strong> {articulo.id} 
                        <br> <strong>Título:</strong> {articulo.titulo} 
                        <br> <strong>Contenido:</strong> {articulo.contenido}
                        """
    except:
        resultado = "<h1> Artículo No Encontrado </h1>"
    return HttpResponse(resultado)

def leer_articulo(request):
    try:
        articulos = Articulo.objects.all()
        resultado = "<h1>Artículos:</h1>"
        for articulo in articulos:
            resultado += f"<p>{articulo.id} - {articulo.titulo}</p>"
    except Exception as e:
        resultado = "<h1> Artículos No Encontrados </h1>"
    return HttpResponse(resultado)

def leer_articulo2(request, a):
    try:
        articulo = Articulo.objects.get(id=a)
        resultado = f"""Articulo: 
                        <br> <strong>ID:</strong> {articulo.id} 
                        <br> <strong>Título:</strong> {articulo.titulo} 
                        <br> <strong>Contenido:</strong> {articulo.contenido}
                        """
    except Articulo.DoesNotExist:
        resultado = "<h1> Artículo No Encontrado </h1>"
    return HttpResponse(resultado)

def editar_articulo(request, id):
    articulo = Articulo.objects.get(pk=id)


    articulo.titulo = "Enseñanza onLine en la UNTELS"
    articulo.contenido = "Aula Virtual, Google Meet, Portal Académico, Google Classroom..."
    articulo.publicado = False


    articulo.save()
    return HttpResponse(f"Articulo Editado: {articulo.titulo} - {articulo.contenido}")

def listar_articulos(request):
    articulos = Articulo.objects.all();
    """articulos = Articulo.objects.filter(
        Q(titulo__contains="Py") |
        Q(titulo__contains="Hab")
    )"""
    return render(request, 'listar_articulos.html',{
        'articulos': articulos,
        'titulo': 'Listado de Artículos'
    })


def eliminar_articulo(request, id):
    articulo = Articulo.objects.get(pk=id)
    articulo.delete()
    return redirect('listar_articulos')

def save_articulo(request):
    if request.method == 'POST':
        titulo = request.POST['titulo']
        if len(titulo)<=5:
            return HttpResponse("<h2>El tamaño del título es pequeño, intente nuevamente</h2>")
        contenido = request.POST['contenido']
        publicado = request.POST['publicado']

        articulo = Articulo(
            titulo = titulo,
            contenido = contenido,
            publicado = publicado
        )
        articulo.save()
        # Crear un mensaje flash (Sesión que solo se muestra 1 vez)
        
        return HttpResponse(f"Articulo Creado: {articulo.titulo} - {articulo.contenido}")
    else:
        return HttpResponse("<h2>No se ha podido registrar el artículo</h2>")


def create_articulo(request):
    return render(request, 'create_articulo.html')

def listar_autores(request):
    autors = Autor.objects.all();
    """autores = Autor.objects.all()
    )"""
    return render(request, 'listar_autores.html',{
        'autores': autors,
        'titulo': 'Listado de Autores'
    })

def save_autor(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        sexo = request.POST['sexo']
        fecha_nac = request.POST['fecha_nac']
        pais = request.POST['pais']

        autor = Autor(
            nombre = nombre,
            apellido = apellido,
            sexo = sexo,
            fecha_nac = fecha_nac,
            pais = pais,
        )
        autor.save()
        return HttpResponse(f"Autor Creado:")
    else:
        return HttpResponse("<h2>No se ha podido registrar el autor</h2>")


def create_autor(request):
    return render(request, 'create_autor.html')

def eliminar_autor(request, id):
    autor = Autor.objects.get(pk=id)
    autor.delete()
    return redirect('listar_autores')

def create_full_articulo(request):
    if request.method == 'POST':
        formulario = FormArticulo(request.POST)
        if formulario.is_valid():
            data_form = formulario.cleaned_data
            # Hay 2 formar de recuperar la información
            titulo  = data_form.get('titulo')
            contenido = data_form['contenido']
            publicado = data_form['publicado']
            articulo = Articulo(
                titulo = titulo,
                contenido = contenido,
                publicado = publicado
            )
            articulo.save()
            messages.success(request, f'Se agregó correctamente el artículo {articulo.id}')
            return redirect('listar_articulos')
            #return HttpResponse(articulo.titulo + ' -  ' + articulo.contenido + ' - ' + str(articulo.publicado))
    else:
        formulario = FormArticulo()
        # Generamos un formulario vacío


    return render(request, 'create_full_articulo.html',{
        'form': formulario
    })


