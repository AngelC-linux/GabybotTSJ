import telebot
import sqlite3
import hashlib
from decouple import config
from io import BytesIO
from telebot import types

bot = telebot.TeleBot(config('TG_TOKEN_02'))

route_db = config('DB')
csv = {}


def tabla_admin():
    with sqlite3.connect(route_db) as conexion:
        table = conexion.cursor()
        table.execute(config('SENTENCE_01'))
        conexion.commit()


tabla_admin()


def registrar_correo(message, correo_admin, contrasena):
    try:
        with sqlite3.connect(route_db) as conexion:
            table = conexion.cursor()
            hash_contrasena = hashlib.sha256(contrasena.encode()).hexdigest()
            table.execute(config("SENTENCE_02"), (correo_admin, hash_contrasena))
            conexion.commit()
        return True
    except sqlite3.IntegrityError as e:
        bot.send_message(message.chat.id, config("MESSAGE_06"))
        return False


def verificacion(message, correo_admin, contrasena):
    try:
        hash_contrasena = hashlib.sha256(contrasena.encode()).hexdigest()
        with sqlite3.connect(route_db) as conexion:
            table = conexion.cursor()
            table.execute(config("SENTENCE_03"), (correo_admin,))
            resultado = table.fetchone()
        if resultado:
            almacenar_contrasena = resultado[0]
            return hash_contrasena == almacenar_contrasena
        return False
    except Exception as e:
        bot.send_message(message.chat.id, config("MESSAGE_07"))
        return False


# Logica para los archivos CSV
def archivo_csv(modalidad):
    with sqlite3.connect(route_db) as conn:
        cursor = conn.cursor()
        cursor.execute(config("SENTENCE_08"), (modalidad,))
        alumnos = cursor.fetchall()
        csv_dato = BytesIO()
        nombre_columna = [i[0] for i in cursor.description]
        csv_dato.write(','.join(nombre_columna).encode(config('FORMAT_CODING_01')) + b'\n')
        for alumno in alumnos:
            csv_dato.write(','.join(map(str, alumno)).encode(config('FORMAT_CODING_02')) + b'\n')
        csv_dato.seek(0)
    return csv_dato


# Registrar.
@bot.message_handler(commands=[config("COMMAND_01")])
def validar_correo_admin_registrar(message):
    bot.send_message(message.chat.id, config("MESSAGE_08"))
    bot.register_next_step_handler(message, validar_contrasena_admin_registrar)


def validar_contrasena_admin_registrar(message):
    correo_admin = message.text
    bot.send_message(message.chat.id, config("MESSAGE_09"))
    bot.register_next_step_handler(message, validar_usuario_admin_registrar, correo_admin)


def validar_usuario_admin_registrar(message, correo_admin):
    contrasena = message.text
    if verificacion(message, correo_admin, contrasena):
        registro(message)
    else:
        bot.send_message(message.chat.id, config("MESSAGE_10"))


def registro(message):
    bot.send_message(message.chat.id,
                     config("MESSAGE_11"))
    bot.send_message(message.chat.id, config("MESSAGE_12"))
    bot.register_next_step_handler(message, mensaje_contrasena)


def mensaje_contrasena(message):
    correo_admin = message.text
    bot.send_message(message.chat.id, config("MESSAGE_13"))
    bot.register_next_step_handler(message, registrar_contrasena, correo_admin)


def registrar_contrasena(message, correo_admin):
    contrasena = message.text
    if verificacion(message, correo_admin, contrasena):
        bot.send_message(message.chat.id, config("MESSAGE_01"))
    else:
        if registrar_correo(message, correo_admin, contrasena):
            bot.send_message(message.chat.id, config("MESSAGE_02"))
        else:
            bot.send_message(message.chat.id, config("MESSAGE_03"))


# Iniciar sesion.
@bot.message_handler(commands=[config("COMMAND_02")])
def iniciar_sesion(message):
    bot.send_message(message.chat.id, config("MESSAGE_14"))
    bot.send_message(message.chat.id, config("MESSAGE_15"))
    bot.register_next_step_handler(message, contrasena)


def contrasena(message):
    correo_admin = message.text
    bot.send_message(message.chat.id, config("MESSAGE_16"))
    bot.register_next_step_handler(message, validar_sesion, correo_admin)


def documentos_csv(message):
    csv_dato_interno = archivo_csv(config("FILTER_01"))
    archivo_interno = config("NAME_CSV_INTERNO")
    bot.send_document(message.chat.id, csv_dato_interno, visible_file_name=archivo_interno)
    csv_dato_externo = archivo_csv(config("FILTER_02"))
    archivo_externo = config("NAME_CSV_EXTERNO")
    bot.send_document(message.chat.id, csv_dato_externo, visible_file_name=archivo_externo)


def validar_sesion(message, correo_admin):
    contrasena = message.text
    if verificacion(message, correo_admin, contrasena):
        bot.send_message(message.chat.id, config("MESSAGE_17"))
        documentos_csv(message)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        boton_actualizar = types.KeyboardButton(config("NAME_BUTTON"))
        markup.add(boton_actualizar)
        bot.send_message(message.chat.id, config("MESSAGE_45"), reply_markup=markup)
    else:
        bot.send_message(message.chat.id, config("MESSAGE_04"))


@bot.message_handler(func=lambda message: message.text == config("NAME_BUTTON"))
def evento_boton_actualizar(message):
    documentos_csv(message)


# Eliminar administradores.
@bot.message_handler(commands=[config("COMMAND_03")])
def validar_correo_admin_administradores(message):
    bot.send_message(message.chat.id, config("MESSAGE_18"))
    bot.register_next_step_handler(message, validar_contrasena_admin_administradores)


def validar_contrasena_admin_administradores(message):
    correo_admin = message.text
    bot.send_message(message.chat.id, config("MESSAGE_19"))
    bot.register_next_step_handler(message, validar_usuario_admin_administradores, correo_admin)


def validar_usuario_admin_administradores(message, correo_admin):
    contrasena = message.text
    if verificacion(message, correo_admin, contrasena):
        lista_correos(message, correo_admin)
    else:
        bot.send_message(message.chat.id, config("MESSAGE_20"))


def lista_correos(message, correo_admin):
    correos_registrados = recuperar_correos_db()
    if correos_registrados:
        lista_correos = "\n".join(correos_registrados)
        bot.send_message(message.chat.id, f"Correos registrados en la base de datos:\n{lista_correos}")
        bot.send_message(message.chat.id, config("MESSAGE_22"))
        bot.register_next_step_handler(message, mensaje_confirmacion)
    else:
        bot.send_message(message.chat.id, config("MESSAGE_23"))


def mensaje_confirmacion(message):
    correo_eliminacion = message.text
    correos_registrados = recuperar_correos_db()
    if correo_eliminacion in correos_registrados:
        if eliminar_correo(correo_eliminacion):
            bot.send_message(message.chat.id, f"El usuario {correo_eliminacion} fue eliminado correctamente.")
        else:
            bot.send_message(message.chat.id, config("MESSAGE_05"))
    else:
        bot.send_message(message.chat.id, config("MESSAGE_25"))


def eliminar_correo(correo_admin):
    with sqlite3.connect(route_db) as conexion:
        table = conexion.cursor()
        table.execute(config("SENTENCE_06"), (correo_admin,))
        conexion.commit()
    return True


def recuperar_correos_db():
    with sqlite3.connect(route_db) as conexion:
        table = conexion.cursor()
        table.execute(config('SENTENCE_07'))
        correos = table.fetchall()
        return [correo[0] for correo in correos]


# Eliminar datos de los alumnos.
@bot.message_handler(commands=[config("COMMAND_04")])
def validar_correo_admin_alumnos(message):
    bot.send_message(message.chat.id, config("MESSAGE_26"))
    bot.register_next_step_handler(message, validar_contrasena_admin_alumnos)


def validar_contrasena_admin_alumnos(message):
    correo_admin = message.text
    bot.send_message(message.chat.id, config("MESSAGE_27"))
    bot.register_next_step_handler(message, validar_usuario_admin_alumnos, correo_admin)


def validar_usuario_admin_alumnos(message, correo_admin):
    contrasena = message.text
    if verificacion(message, correo_admin, contrasena):
        mensaje_confirmacion_alum(message)
    else:
        bot.send_message(message.chat.id, config("MESSAGE_28"))


def mensaje_confirmacion_alum(message):
    bot.send_message(message.chat.id,
                     config("MESSAGE_29"))
    bot.register_next_step_handler(message, mensaje_eliminacion_alum)


def mensaje_eliminacion_alum(message):
    respuesta = message.text.lower()
    if respuesta == config("MESSAGE_30"):
        if eliminar_alumnos():
            bot.send_message(message.chat.id, config("MESSAGE_32"))
        else:
            bot.send_message(message.chat.id, config("MESSAGE_33"))
    elif respuesta == config("MESSAGE_31"):
        bot.send_message(message.chat.id, config("MESSAGE_34"))
    else:
        bot.send_message(message.chat.id, config("MESSAGE_35"))


def eliminar_alumnos():
    with sqlite3.connect(route_db) as conexion:
        tabla = conexion.cursor()
        tabla.execute(config("SENTENCE_09"))
        conexion.commit()
    return True


# Eliminar a los alumnos de manera individual
@bot.message_handler(commands=[config("COMMAND_05")])
def validar_correo_admin_alumnos_individual(message):
    bot.send_message(message.chat.id, config("MESSAGE_26"))
    bot.register_next_step_handler(message, validar_contrasena_admin_alumnos_individual)


def validar_contrasena_admin_alumnos_individual(message):
    correo_admin = message.text
    bot.send_message(message.chat.id, config("MESSAGE_27"))
    bot.register_next_step_handler(message, validar_usuario_admin_alumnos_individual, correo_admin)


def validar_usuario_admin_alumnos_individual(message, correo_admin):
    contrasena = message.text
    if verificacion(message, correo_admin, contrasena):
        mostrar_alumnos(message)
    else:
        bot.send_message(message.chat.id, config("MESSAGE_28"))


def mostrar_alumnos(message):
    bot.send_message(message.chat.id, config("MESSAGE_36"))
    datos_alum = obtener_alumnos()
    if datos_alum:
        for alumno in datos_alum:
            bot.send_message(message.chat.id, f"Alumno:\n{alumno}")
        bot.send_message(message.chat.id, config("MESSAGE_37"))
        bot.register_next_step_handler(message, confirmacion_eliminacion_alumnos)
    else:
        bot.send_message(message.chat.id, config("MESSAGE_38"))


def confirmacion_eliminacion_alumnos(message):
    name_alum = message.text
    alumno = obtener_alumnos_nombre(name_alum)
    if alumno:
        bot.send_message(message.chat.id, f"¿Desea eliminar al alumno del sistema?\n{alumno} Escriba: (Si/No)")
        bot.register_next_step_handler(message, eliminar_alumno_db, name_alum)
    else:
        bot.send_message(message.chat.id, config("MESSAGE_39"))


def obtener_alumnos():
    with sqlite3.connect(route_db) as conexion:
        cursor = conexion.cursor()
        cursor.execute(config("SENTENCE_10"))
        alumnos = cursor.fetchall()
        return alumnos


def obtener_alumnos_nombre(name_alum):
    with sqlite3.connect(route_db) as conexion:
        cursor = conexion.cursor()
        cursor.execute(config("SENTENCE_11"), (name_alum,))
        alumno = cursor.fetchone()
        return alumno


def eliminar_alumno_db(message, name_alum):
    respuesta = message.text.lower()
    if respuesta == config("MESSAGE_40"):
        if eliminar_alumno(name_alum):
            bot.send_message(message.chat.id, config("MESSAGE_42"))
        else:
            bot.send_message(message.chat.id, config("MESSAGE_43"))
    else:
        bot.send_message(message.chat.id, config("MESSAGE_44"))


def eliminar_alumno(name_alum):
    with sqlite3.connect(route_db) as conexion:
        cursor = conexion.cursor()
        cursor.execute(config("SENTENCE_12"), (name_alum,))
        conexion.commit()
    return True


bot.polling()
