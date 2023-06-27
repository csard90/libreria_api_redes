from fastapi import FastAPI
import pandas as pd
import os

# BRUNAZO HACER CUALQUIER PRUEBA QUE QUIERAS DESDE http://localhost:8000/docs. Hay esta la opcion
# poniendo try out de probar todos los metodos. Mas que nada porque los put, post y remove
# no los podemos probar por url, o al menos no encontre como.


# CUANDO BRUNO DESCARGUES ALGUN .JSON QUE TE ENVIE EN EL CLIENTE Y LO IMPORTES COMO .json HACELE ANTES DE USARLO UN
# archivo.replace("\\", '' ) para borrarle unas barras inclinadas invertidas que pone pandas como caracter de escape

# En los return que devolvi texto despues vemos que devuelvo, no se como tenias pensado hacer el cliente. 

# Te deje comentarios de como hice los metodos. Es bastante simple.


app = FastAPI()
        
@app.get("/libreria_entera")
def libreria_entera():

    ''' Metodo GET que devuelve todos los libros de la libreria. '''

    libros = cargar_libreria()

    # Pasamos a formato .json para poder mandarlo en el return
    libros = libros.to_json(orient='records')


    
    return libros

@app.get("/buscar_libro")
def buscar_libro(columna: str, patron_busqueda : str):
    
    '''  
    Metodo GET para buscar un determinado libro por: Autor, Pais, Idioma, Titulo, Año.
    Busca si el patron esta contenido en la cadena.
    Recibe dos paremtros, columna es el atributo del .json, y patron_busqueda es el
    patron que se busca.
    Ej: http://localhost:8000/buscar_libro?columna=author&patron_busqueda=ch
    busca los autores que contengan en alguna parte de su nombre el patron 'ch'.
    '''

    libros = cargar_libreria()

    if columna == 'author':            
        return busqueda_por_patron(libros, patron_busqueda, columna)
    elif columna == 'country':    
        return busqueda_por_patron(libros, patron_busqueda, columna)    
    elif columna == 'language':
        return busqueda_por_patron(libros, patron_busqueda, columna)    
    elif columna == 'title':
        return busqueda_por_patron(libros, patron_busqueda, columna)    
    elif columna == 'year':
        return busqueda_por_patron(libros, patron_busqueda, columna)    
    else:        
        return 'Opcion no valida'


@app.post("/agregar_libro")
def agregar_libro(autor: str, pais : str, link_imagen: str, idioma: str, link: str, paginas: str, titulo: str,
                 año: str):  

    '''
    Metodo POST que sirve para agregar un nuevo libro. Recibe los datos de los atributos que tendra
    el nuevo libro y lo crea.
    '''
    
    libros = cargar_libreria()

    nuevo_libro = {'author': autor, 'country': pais, 'imageLink': link_imagen, 'language': idioma, 
                   'link': link, 'pages': paginas, 'title': titulo, 'year': año}

    # Coloca el nuevo libro en la ultima posicion del df.
    libros.loc[len(libros)] = nuevo_libro    
    
    # Sin esto no se porque no me guarda el archivo .json, no parece tener nada que ver, pero a partir de que lo 
    # puse funciono
    os.getcwd()

    # Exporta a .json sobreescribiendo la base de datos. orient='records' cada fila del df es un objeto JSON
    # independiente
    libros.to_json('books.json', orient='records') 

    return 'Libro agregado existosamente'


@app.put("/modificar_libro")
def modificar_libro(eleccion: str, autor: str, pais : str, link_imagen: str, idioma: str, link: str, 
                    paginas: str, titulo: str, año: str):  
    
    '''
    Metodo PUT que modifica un libro a partir de un titulo, el parametro eleccion. Este, debe coincidir 
    exactamente con el titulo del libro en cuestion.
    Tambien recibe los todos los nuevos valores de TODOS los atributos del libro, para ser modificados.
    '''

    libros = cargar_libreria()

    libro_modificado = {'author': autor, 'country': pais, 'imageLink': link_imagen, 'language': idioma, 
                   'link': link, 'pages': paginas, 'title': titulo, 'year': año}

    # Verifica si existe al menos una fila con ese titulo.
    if libros['title'][ libros['title'] == eleccion ].empty == False:

        # Me quedo con la primera fila (podrian existir mas de una)
        fila = libros[ libros['title'] == eleccion ].iloc[0]

        # Busco su indice. Como ya la tengo identificada, en formato series, lo paso a dataframe, 
        # cambio filas por columnas para que vuelva a tener el indice en donde va y elijo obtener 
        # el indice del elemento que esta en la posicion 0.
        indice = fila.to_frame().transpose().index[0]
    
        # Modifico a partir del indice los diferentes atributos del libro.
        libros.loc[indice, 'author'] = libro_modificado['author']
        libros.loc[indice, 'country'] = libro_modificado['country']
        libros.loc[indice, 'imageLink'] = libro_modificado['imageLink']
        libros.loc[indice, 'language'] = libro_modificado['language']
        libros.loc[indice, 'link'] = libro_modificado['link']
        libros.loc[indice, 'pages'] = libro_modificado['pages']
        libros.loc[indice, 'title'] = libro_modificado['title']
        libros.loc[indice, 'year'] = libro_modificado['year']

        # Esto es necesario para que guarde el archivo .json (sin esto no funcionaba)
        os.getcwd()

        # Sobreeescribo el archivo, una fila un objeto.
        libros.to_json('books.json', orient='records')    

        return 'Libro modificado existosamente'
    
    # Si no existe ninguna fila con ese titulo..
    else: 
        
        return 'El libro ' + str(eleccion) + ' no existe en la base de datos'

@app.delete("/eliminar_libro")
def eliminar_libro(eleccion: str):  
    
    '''
    Metodo DELETE que eliminar un libro a partir de un titulo, el parametro eleccion. Este, debe coincidir 
    exactamente con el titulo del libro en cuestion.
    '''

    libros = cargar_libreria()

    # Verifica si existe al menos una fila con ese titulo.
    if libros['title'][ libros['title'] == eleccion ].empty == False:

        # Me quedo con la primera fila (podrian existir mas de una)
        fila = libros[ libros['title'] == eleccion ].iloc[0]

        # Busco su indice. Como ya la tengo identificada, en formato series, lo paso a dataframe, 
        # cambio filas por columnas para que vuelva a tener el indice en donde va y elijo obtener 
        # el indice del elemento que esta en la posicion 0.
        indice = fila.to_frame().transpose().index[0]

        # Elimino el archivo en cuestion
        libros = libros.drop(indice)

        # Esto es necesario para que guarde el archivo .json (sin esto no funcionaba)
        os.getcwd()

        # Sobreeescribo el archivo, una fila un objeto.
        libros.to_json('books.json', orient='records')    

        return 'Libro eliminado existosamente'
    
    # Si no existe ninguna fila con ese titulo..
    else: 
        
        return 'El libro ' + str(eleccion) + ' no existe en la base de datos'




#----------------------------------------------------------------------------------------------------------------
# Funciones auxiliares:
#----------------------------------------------------------------------------------------------------------------

def cargar_libreria():

    ''' Funcion auxiliar utilizada para cargar la libreria cada vez que se llama algun metodo'''

    # Usamos pandas para leer el archivo .json
    libros = pd.read_json('books.json')

    # Limpieza del dataframe en la columna link que al final del mismo tenia la cadena "\n"
    libros['link'] = libros['link'].apply(lambda x : x.replace("\n", ''))
    # Conversion de tipos de datos
    libros['year'] = libros['year'].astype(str)
    libros['pages'] = libros['pages'].astype(str)
    return libros



def busqueda_por_patron(libros, patron_busqueda, columna):

    ''' Funcion auxiliar utilizada para buscar la/s fila/s del df que contenga/n un patron en determinada 
    columna. Es utilizada por el metodo GET /buscar libro  '''

    # Devuelve mascara booleana con valor True en las filas que contenga la cadena buscada
    mascara = libros[columna].str.contains(patron_busqueda, case=False) # Ignora may. y min.

    # Si al menos hay un True devuelve True, es decir hay resultados, sino False, no hay resultados
    resultado_mascara = mascara.any()

    # En caso de haber resultados
    if resultado_mascara == True:

        # Buscamos los resultados
        resultado_busqueda = libros[mascara]

        # Convertimos a .json para poder devolverlo
        resultado_busqueda = resultado_busqueda.to_json(orient='records')        

        return resultado_busqueda
    
    else:

        return 'No se encontro ningun resultado para el ' + columna + ' indicado'

