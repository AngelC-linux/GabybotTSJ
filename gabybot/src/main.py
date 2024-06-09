import os
import telebot
import sqlite3
from telebot import types
from decouple import config
from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

bot = telebot.TeleBot(config('TG_TOKEN_01'))

temp_data = {}
zapopan_selected = False


@bot.message_handler(commands=["start"])
def submenu_campus(message):
    try:

        markup2 = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup2.add("Zapopan", "Tequila", "Arandas", "La Huerta", "Pto. Vallarta",
                    "El Grullo", "Mascota", "Lagos", "Tala", "Chapala",
                    "Cocula", "Zapotlanejo", "Tamazula")

        msg = bot.send_message(message.chat.id,
                               "Hola, soy el chatbot personal del área de Servicio Social del Tecnológico Superior de Jalisco.\n"
                               "Por favor, elige un campus en el menú para continuar:",
                               reply_markup=markup2)
        bot.register_next_step_handler(msg, opciones)
    except Exception as e:
        bot.send_message(message.chat.id, f"Error al obtener información: {e}")


def opciones(message):
    try:

        global zapopan_selected

        if message.text == "Zapopan":
            zapopan_selected = True
            markup = types.ReplyKeyboardMarkup(row_width=2)
            item1 = types.KeyboardButton("1. Información")
            item2 = types.KeyboardButton("2. Realizar registro")
            item3 = types.KeyboardButton("3. Generar formatos PDF | Servicio Social")

            markup.add(item1, item2, item3)

            bot.send_message(message.chat.id,
                             "Bienvenido al campus Zapopan,\n"
                             "Tu menú se ha actualizado, elige la opción que desees:",
                             reply_markup=markup)
            bot.register_next_step_handler(message, menu_principal)

        elif message.text in ["Tequila", "Arandas", "La Huerta", "Pto. Vallarta",
                              "El Grullo", "Mascota", "Lagos", "Tala", "Chapala", "Cocula",
                              "Zapotlanejo", "Tamazula"]:
            bot.send_message(message.chat.id, f"Lo sentimos mucho, {message.text}, "
                                              "en este momento tu campus no está disponible")
            submenu_campus(message)

        else:
            bot.send_message(message.chat.id,
                             "¿Cuál? ese campus no lo encuentro, "
                             "selecciona 1 de los 13 campus que hay en las opciones")
            submenu_campus(message)
    except Exception as e:
        bot.send_message(message.chat.id, f"Error de opciones en la información al usuario: {e}")


@bot.message_handler(func=lambda message: True)
def menu_principal(message):
    try:
        if message.text == "1. Información":
            bot.send_message(message.chat.id, config('INFORMATION'))
        elif message.text == "2. Realizar registro":
            bot.send_message(message.chat.id,
                             "De acuerdo con los requerimientos necesitas:"
                             "\n1.- Avance del 70% y expedir la carta que lo acredite "
                             "en control escolar."
                             "\n2.- Cinco créditos complementarios preferentemente."
                             "\n3.- Kardex o historial académico actual.\n"
                             "\nLos puntos anteriores los puedes verificar "
                             "en tú cuenta de Edcore:"
                             "\nhttps://edcore.tecmm.mx/alum/login.jsp\n"
                             "\n4.- Puedes verificar tú expediente de Actividades\n"
                             "Complementarias en Control Escolar"
                             "\n(Edificio de Ciencias Básicas segundo nivel a mano derecha).\n"
                             "\n5.- Recuerda revisar el porcentaje de avance en la parte superior de tu Kardex.\n"
                             "\n6.- Si cumples con lo anterior, selecciona el botón:"
                             "\n➡️ 3. Generar formatos PDF | Servicio Social"
                             "\n\n AVISO: El proceso puede durar 15 min. con la información a la mano, "
                             "Te sugerimos que busques un lugar cómodo y agradable para empezar el proceso")

        elif message.text == "3. Generar formatos PDF | Servicio Social":
            msg = bot.send_message(message.chat.id, "Por favor, ingresa tu matrícula:")
            bot.register_next_step_handler(msg, mensaje_nombre)
        else:
            bot.send_message(message.chat.id, "Lo siento, no entendí tu respuesta."
                                              "\nPor favor, elige una opción del teclado.")
            submenu_campus(message)
    except Exception as e:
        bot.send_message(message.chat.id, f"Error del menú proporcionar información: {e}")


def mensaje_nombre(message):
    try:
        if message.text == "":
            bot.send_message(message.chat.id, "")
            submenu_campus(message)
        else:
            matricula = message.text
            msg = bot.send_message(message.chat.id,
                                   "\nPor favor, escribe tu nombre completo "
                                   "iniciando por apellidos:")
            bot.register_next_step_handler(msg, mensaje_edad, matricula)

            msg = bot.reply_to(message, "\n\nAVISO: Si te equivocas en el proceso "
                                        "al final tendrás la opción de reiniciar,  "
                                        "pero deberás finalizar todo el proceso. "
                                        "\nTienes que tener en cuenta que no se guardarán los datos. "
                                        "\n\nEl proceso constará de 15 minutos a partir de aquí.")

    except Exception as e:
        bot.send_message(message.chat.id, f"Error al registrar el nombre: {e}")


def mensaje_edad(message, matricula):
    try:
        if message.text == "":
            bot.send_message("")
        else:
            nombre = message.text
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add(*[types.KeyboardButton(str(i)) for i in range(18, 61)])
            msg = bot.send_message(message.chat.id, "\nPor favor, selecciona tu edad:",
                                   reply_markup=markup)
            bot.register_next_step_handler(msg, mensaje_sexo, matricula, nombre)

    except Exception as e:
        bot.send_message(message.chat.id, "Error al introducir la edad "
                                          f"vuelve a seleccionar los formatos\n: {e}")


def mensaje_sexo(message, matricula, nombre):
    try:
        if not message.text.isdigit():
            if message.text == "":
                submenu_campus(message)
            msg = bot.send_message(message.chat.id,
                                   "Incorrecto, debes introducir por número tu edad.")
            bot.register_next_step_handler(msg, mensaje_sexo, matricula, nombre)
        else:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add(types.KeyboardButton("H"), types.KeyboardButton("M"))
            msg = bot.send_message(message.chat.id, "Selecciona un género:\n"
                                                    "Sabemos respetuosamente la importancia del tema "
                                                    "de género no binario, pero por disposición "
                                                    "de la documentanción oficial y/o si deseas realizar el "
                                                    "servicio de forma externa es necesario indicarlo.\n\n"
                                                    "H para Hombre\n"
                                                    "M para Mujer", reply_markup=markup)
            bot.register_next_step_handler(msg, mensaje_domicilio,
                                           matricula, nombre, message.text)
    except Exception as e:
        bot.send_message(message.chat.id, f"Error al introcir el sexo: {e}")


def mensaje_domicilio(message, matricula, nombre, edad):
    try:
        if message.text in ["H", "M"]:
            sexo = message.text
            temp_data[message.chat.id] = {"matricula": matricula}

            msg = bot.send_message(message.chat.id, "Por favor, ingresa tu domicilio:")
            msg = bot.reply_to(message, "Ejemplo: C. (Calle) número, Col. (Colonia), CP, Municipio, Estado.")
            bot.register_next_step_handler(msg, lambda msg: mensaje_telefono(msg, matricula,
                                                                             nombre, edad, sexo))
        else:
            bot.send_message(message.chat.id, "Lo lamento, solo se permiten las opciones del teclado")
            mensaje_sexo(message, matricula, nombre)
    except Exception as e:
        bot.send_message(message.chat.id, f"Error en el domicilio: {e}")


def mensaje_telefono(message, matricula, nombre, edad, sexo):
    try:
        domicilio = message.text

        msg = bot.send_message(message.chat.id, "Por favor, ingresa tu número de teléfono:")
        bot.register_next_step_handler(msg, lambda msg: mensaje_carrera(msg, matricula,
                                                                        nombre, edad,
                                                                        sexo, domicilio))
    except Exception as e:
        bot.send_message(message.chat.id, f"Error al introducir el teléfono: {e}")


def mensaje_carrera(message, matricula, nombre, edad, sexo, domicilio):
    try:
        telefono = message.text

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(types.KeyboardButton("Sistemas Computacionales"),
                   types.KeyboardButton("Industrial"),
                   types.KeyboardButton("Civil"),
                   types.KeyboardButton("Gestión Empresarial"),
                   types.KeyboardButton("Electromecánica"),
                   types.KeyboardButton("Electrónica"),
                   types.KeyboardButton("Arquitectura"),
                   types.KeyboardButton("Gastronomía"))
        msg = bot.send_message(message.chat.id, "Por favor, selecciona tu carrera:",
                               reply_markup=markup)
        bot.register_next_step_handler(msg, lambda msg: mensaje_semestre(msg, matricula, nombre,
                                                                         edad, sexo, domicilio,
                                                                         telefono))
    except Exception as e:
        bot.send_message(message.chat.id, f"Error al introcir la carrera: {e}")


def mensaje_semestre(message, matricula, nombre, edad, sexo, domicilio, telefono):
    try:
        carrera = message.text

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(types.KeyboardButton("1"), types.KeyboardButton("2"),
                   types.KeyboardButton("3"), types.KeyboardButton("4"),
                   types.KeyboardButton("5"), types.KeyboardButton("6"),
                   types.KeyboardButton("7"), types.KeyboardButton("8"),
                   types.KeyboardButton("9"), types.KeyboardButton("10"),
                   types.KeyboardButton("11"), types.KeyboardButton("12"),
                   types.KeyboardButton("13"), types.KeyboardButton("14"))
        msg = bot.send_message(message.chat.id, "Por favor, selecciona tu número de semestre:",
                               reply_markup=markup)
        bot.register_next_step_handler(msg, lambda msg: mensaje_periodo(msg, matricula,
                                                                        nombre, edad, sexo,
                                                                        domicilio, telefono,
                                                                        carrera))
    except Exception as e:
        bot.send_message(message.chat.id, f"Error al introducir el semestre: {e}")


def mensaje_periodo(message, matricula, nombre, edad, sexo, domicilio, telefono, carrera):
    try:
        if not message.text.isdigit():
            msg = bot.send_message(message.chat.id,
                                   "Incorrecto, debes introducir solo el número de semestre.")
            bot.register_next_step_handler(msg, mensaje_sexo, matricula, nombre)
        else:
            semestre = message.text

            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add(types.KeyboardButton("Enero - Julio"),
                       types.KeyboardButton("Julio - Enero"))
            msg = bot.send_message(message.chat.id, "Por favor, selecciona un periodo escolar:",
                                   reply_markup=markup)
            bot.register_next_step_handler(message, lambda msg: mensaje_creditos(msg, matricula,
                                                                                 nombre, edad, sexo,
                                                                                 domicilio, telefono,
                                                                                 carrera, semestre))
    except Exception as e:
        bot.send_message(message.chat.id, f"Error al introducir el periodo escolar: {e}")


def mensaje_creditos(message, matricula, nombre, edad, sexo, domicilio,
                     telefono, carrera, semestre):
    try:
        photo_path = config('PHOTO_01')
        periodo = message.text
        with open(photo_path, 'rb') as photo_file:
            photo_msg = types.InputMediaPhoto(photo_file)
            bot.send_media_group(message.chat.id, [photo_msg])

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(*[types.KeyboardButton(str(i)) for i in range(70, 101)])

        msg = bot.send_message(message.chat.id,
                               "Por favor, ingresa el avance de tu kardex, SOLO el número."
                               "\nrecuerda tener el mínimo del 70% de creditos aprobados:",
                               reply_markup=markup)
        bot.register_next_step_handler(msg, lambda msg: mensaje_correo(msg, matricula, nombre,
                                                                       edad, sexo, domicilio, telefono,
                                                                       carrera, semestre, periodo))
    except Exception as e:
        bot.send_message(message.chat.id, f"Error de imagen ejemplo créditos: {e}")


def mensaje_correo(message, matricula, nombre, edad, sexo, domicilio, telefono,
                   carrera, semestre, periodo):
    try:
        correo = message.text

        msg = bot.send_message(message.chat.id, "Por favor, ingresa tu correo institucional:")
        bot.register_next_step_handler(msg, lambda msg: mensaje_dependencia_oficial(msg, matricula,
                                                                                    nombre, edad, sexo, domicilio,
                                                                                    telefono, carrera, semestre,
                                                                                    periodo, correo))
    except Exception as e:
        bot.send_message(message.chat.id, f"Error al ingresar el correo institucional: {e}")


def mensaje_dependencia_oficial(message, matricula, nombre, edad, sexo, domicilio,
                                telefono, carrera, semestre, periodo, correo):
    try:
        photo_path = config('PHOTO_02')
        with open(photo_path, 'rb') as photo_file:
            photo_msg = types.InputMediaPhoto(photo_file)
            bot.send_media_group(message.chat.id, [photo_msg])
        dependencia = message.text

        msg = bot.send_message(message.chat.id, "Por favor, ingresa tu dependencia oficial de Servicio Social:"
                               "\nEn caso de ser interno, debes poner el nombre completo como viene en la imagen "
                               "incluyendo el campus")
        bot.register_next_step_handler(msg, lambda msg: mensaje_titular_dependencia(msg, matricula, nombre,
                                                                                    edad, sexo, domicilio, telefono,
                                                                                    carrera,
                                                                                    semestre, periodo, correo,
                                                                                    dependencia))
    except Exception as e:
        bot.send_message(message.chat.id, f"Error al ingresar la dependencia oficial de servicio social: {e}")


def mensaje_titular_dependencia(message, matricula, nombre, edad, sexo, domicilio,
                                telefono, carrera, semestre, periodo, correo, dependencia):
    try:
        titular = message.text

        msg = bot.send_message(message.chat.id, "Por favor, ingresa el nombre completo del titular de la dependencia:")
        bot.register_next_step_handler(msg,
                                       lambda msg: mensaje_domicilio_dependencia(msg, matricula, nombre, edad, sexo,
                                                                                 domicilio, telefono, carrera, semestre,
                                                                                 periodo,
                                                                                 correo,
                                                                                 dependencia, titular))
    except Exception as e:
        bot.send_message(message.chat.id, f"Error al ingresar el titular de la dependencia: {e}")


def mensaje_domicilio_dependencia(message, matricula, nombre, edad, sexo, domicilio,
                                  telefono, carrera, semestre, periodo, correo, dependencia, titular):
    try:
        photo_path = config('PHOTO_03')
        with open(photo_path, 'rb') as photo_file:
            photo_msg = types.InputMediaPhoto(photo_file)
            bot.send_media_group(message.chat.id, [photo_msg])
        domicilio_dependencia = message.text

        msg = bot.send_message(message.chat.id, "Por favor, ingresa el domicilio de la dependencia:")
        bot.register_next_step_handler(msg, lambda msg: mensaje_responsable_programa(msg, matricula, nombre, edad, sexo,
                                                                                     domicilio, telefono, carrera,
                                                                                     semestre,
                                                                                     periodo,
                                                                                     correo,
                                                                                     dependencia, titular,
                                                                                     domicilio_dependencia))
    except Exception as e:
        bot.send_message(message.chat.id, f"Error al ingresar el domicilio de la dependencia: {e}")


def mensaje_responsable_programa(message, matricula, nombre, edad, sexo, domicilio,
                                 telefono, carrera, semestre, periodo, correo, dependencia, titular,
                                 domicilio_dependencia):
    try:
        responsable = message.text

        msg = bot.send_message(message.chat.id, "Por favor, ingresa el nombre completo del responsable del programa:")
        bot.register_next_step_handler(msg, lambda msg: mensaje_jefe_inmediato(msg, matricula, nombre, edad, sexo,
                                                                               domicilio, telefono, carrera, semestre,
                                                                               periodo,
                                                                               correo,
                                                                               dependencia, titular,
                                                                               domicilio_dependencia,
                                                                               responsable))
    except Exception as e:
        bot.send_message(message.chat.id, f"Error al ingresar el nombre del responsable del programa: {e}")


def mensaje_jefe_inmediato(message, matricula, nombre, edad, sexo, domicilio,
                           telefono, carrera, semestre, periodo, correo, dependencia, titular, domicilio_dependencia,
                           responsable):
    try:
        jefe = message.text

        msg = bot.send_message(message.chat.id, "Por favor, ingresa el puesto y nombre del jefe inmediato:")
        msg = bot.send_message(message.chat.id, "Ejemplo: Puesto, Nombre")
        bot.register_next_step_handler(msg, lambda msg: mensaje_nombre_programa(msg, matricula, nombre, edad, sexo,
                                                                                domicilio, telefono, carrera, semestre,
                                                                                periodo,
                                                                                correo,
                                                                                dependencia, titular,
                                                                                domicilio_dependencia, responsable,
                                                                                jefe))
    except Exception as e:
        bot.send_message(message.chat.id, f"Error al ingresar el puesto y nombre  del jefe inmediato: {e}")


def mensaje_nombre_programa(message, matricula, nombre, edad, sexo, domicilio,
                            telefono, carrera, semestre, periodo, correo, dependencia, titular, domicilio_dependencia,
                            responsable, jefe):
    try:
        photo_path = config('PHOTO_04')
        with open(photo_path, 'rb') as photo_file:
            photo_msg = types.InputMediaPhoto(photo_file)
            bot.send_media_group(message.chat.id, [photo_msg])
        programa = message.text

        msg = bot.send_message(message.chat.id, "Por favor, ingresa el nombre del programa:")
        msg = bot.send_message(message.chat.id, "Ejemplo: Apoyo administrativo")
        bot.register_next_step_handler(msg, lambda msg: mensaje_modalidad(msg, matricula, nombre, edad, sexo,
                                                                          domicilio, telefono, carrera, semestre,
                                                                          periodo,
                                                                          correo,
                                                                          dependencia, titular, domicilio_dependencia,
                                                                          responsable, jefe, programa))
    except Exception as e:
        bot.send_message(message.chat.id, f"Error al ingresar el nombre del programa: {e}")


def mensaje_modalidad(message, matricula, nombre, edad, sexo, domicilio,
                      telefono, carrera, semestre, periodo, correo, dependencia, titular, domicilio_dependencia,
                      responsable, jefe, programa):
    try:
        modalidad = message.text

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(types.KeyboardButton("Interno"),
                   types.KeyboardButton("Externo"))
        msg = bot.send_message(message.chat.id, "Por favor, selecciona una modalidad:", reply_markup=markup)
        bot.register_next_step_handler(msg, lambda msg: mensaje_fecha_inicio(msg, matricula, nombre, edad, sexo,
                                                                             domicilio, telefono, carrera, semestre,
                                                                             periodo,
                                                                             correo,
                                                                             dependencia, titular,
                                                                             domicilio_dependencia, responsable,
                                                                             jefe, programa,
                                                                             modalidad))
    except Exception as e:
        bot.send_message(message.chat.id, f"Error al seleccionar la modalidad: {e}")


def mensaje_fecha_inicio(message, matricula, nombre, edad, sexo, domicilio,
                         telefono, carrera, semestre, periodo, correo, dependencia, titular, domicilio_dependencia,
                         responsable, jefe, programa, modalidad):
    try:
        fecha_inicio = message.text

        msg = bot.send_message(message.chat.id, "Por favor, ingresa la fecha de inicio del Servicio Social:")
        msg = bot.send_message(message.chat.id, "Ejemplo: DD/MM/AA")
        bot.register_next_step_handler(msg, lambda msg: mensaje_actividades(msg, matricula, nombre, edad, sexo,
                                                                            domicilio, telefono, carrera,
                                                                            semestre,
                                                                            periodo,
                                                                            correo,
                                                                            dependencia, titular,
                                                                            domicilio_dependencia,
                                                                            responsable,
                                                                            jefe, programa,
                                                                            modalidad,
                                                                            fecha_inicio))
    except Exception as e:
        bot.send_message(message.chat.id, f"Error al ingresar la fecha de inicio de Servicio Social: {e}")


def mensaje_actividades(message, matricula, nombre, edad, sexo, domicilio,
                        telefono, carrera, semestre, periodo, correo, dependencia, titular, domicilio_dependencia,
                        responsable, jefe, programa, modalidad, fecha_inicio):
    try:
        actividades = message.text

        msg = bot.send_message(message.chat.id, "Por favor, ingresa la actividad de Servicio Social:")
        msg = bot.send_message(message.chat.id, "Ejemplo: Captura de datos y organizar documentos del departamento.")
        bot.register_next_step_handler(msg, lambda msg: reglamento_uno(msg, matricula, nombre, edad, sexo,
                                                                       domicilio, telefono, carrera, semestre,
                                                                       periodo,
                                                                       correo,
                                                                       dependencia, titular, domicilio_dependencia,
                                                                       responsable, jefe, programa,
                                                                       modalidad,
                                                                       fecha_inicio, actividades))
    except Exception as e:
        bot.send_message(message.chat.id, f"Error al ingresar las actividades de Servicio Social: {e}")


def reglamento_uno(message, matricula, nombre, edad, sexo, domicilio,
                   telefono, carrera, semestre, periodo, correo, dependencia, titular, domicilio_dependencia,
                   responsable, jefe, programa, modalidad, fecha_inicio, actividades):
    try:
        ciudad = message.text

        msg = bot.send_message(message.chat.id, "Me comprometo a realizar el Servicio Social "
                                                "acatando el reglamento emitido por el Instituto Tecnológico Superior de Jalisco "
                                                "y llevarlo a cabo en el lugar y periodos manifestados, así como a participar "
                                                "con mis conocimientos iniciativa en las actividades que desempeñe, procurando "
                                                "dar una imagen positiva del Instituto Tecnológico Superior de Jalisco en el organismo "
                                                "o dependencia oficial. De no hacerlo así, quedo enterado (a) de la cancelación respectiva, la cual "
                                                "procederá automáticamente.")
        msg = bot.send_message(message.chat.id, "En la CIUDAD de:")
        msg = bot.send_message(message.chat.id, "Ejemplo: Zapopan, Jalisco")
        bot.register_next_step_handler(msg, lambda msg: reglamento_dos(msg, matricula, nombre, edad, sexo,
                                                                       domicilio, telefono, carrera, semestre,
                                                                       periodo,
                                                                       correo,
                                                                       dependencia, titular, domicilio_dependencia,
                                                                       responsable, jefe, programa,
                                                                       modalidad,
                                                                       fecha_inicio, actividades, ciudad))
    except Exception as e:
        bot.send_message(message.chat.id, f"Error al ingresar la ciudad(reglamento): {e}")


def reglamento_dos(message, matricula, nombre, edad, sexo, domicilio,
                   telefono, carrera, semestre, periodo, correo, dependencia, titular, domicilio_dependencia,
                   responsable, jefe, programa, modalidad, fecha_inicio, actividades, ciudad):
    try:
        dia = message.text

        msg = bot.send_message(message.chat.id, "Del DIA:")
        bot.register_next_step_handler(msg, lambda msg: reglamento_tres(msg, matricula, nombre, edad, sexo,
                                                                        domicilio, telefono, carrera, semestre,
                                                                        periodo,
                                                                        correo,
                                                                        dependencia, titular, domicilio_dependencia,
                                                                        responsable, jefe, programa,
                                                                        modalidad,
                                                                        fecha_inicio, actividades, ciudad, dia))
    except Exception as e:
        bot.send_message(message.chat.id, f"Error al ingresar el día(reglamento): {e}")


def reglamento_tres(message, matricula, nombre, edad, sexo, domicilio,
                    telefono, carrera, semestre, periodo, correo, dependencia, titular, domicilio_dependencia,
                    responsable, jefe, programa, modalidad, fecha_inicio, actividades, ciudad, dia):
    try:
        mes = message.text

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(types.KeyboardButton("Enero"),
                   types.KeyboardButton("Febrero"),
                   types.KeyboardButton("Marzo"),
                   types.KeyboardButton("Abril"),
                   types.KeyboardButton("Mayo"),
                   types.KeyboardButton("Junio"),
                   types.KeyboardButton("Julio"),
                   types.KeyboardButton("Agosto"),
                   types.KeyboardButton("Septiembre"),
                   types.KeyboardButton("Octubre"),
                   types.KeyboardButton("Noviembre"),
                   types.KeyboardButton("Diciembre"))
        msg = bot.send_message(message.chat.id, "Del MES:", reply_markup=markup)
        bot.register_next_step_handler(msg, lambda msg: reglamento_cuatro(msg, matricula, nombre, edad, sexo,
                                                                          domicilio, telefono, carrera, semestre,
                                                                          periodo,
                                                                          correo,
                                                                          dependencia, titular, domicilio_dependencia,
                                                                          responsable, jefe, programa,
                                                                          modalidad,
                                                                          fecha_inicio, actividades, ciudad, dia, mes))
    except Exception as e:
        bot.send_message(message.chat.id, f"Error al ingresar el mes(reglamento): {e}")


def reglamento_cuatro(message, matricula, nombre, edad, sexo, domicilio,
                      telefono, carrera, semestre, periodo, correo, dependencia, titular, domicilio_dependencia,
                      responsable, jefe, programa, modalidad, fecha_inicio, actividades,
                      ciudad, dia, mes):
    try:
        año = message.text

        msg = bot.send_message(message.chat.id, "Del AÑO:")
        bot.register_next_step_handler(msg, lambda msg: objetivo(msg, matricula, nombre, edad, sexo,
                                                                 domicilio, telefono, carrera, semestre,
                                                                 periodo,
                                                                 correo,
                                                                 dependencia, titular, domicilio_dependencia,
                                                                 responsable, jefe, programa,
                                                                 modalidad,
                                                                 fecha_inicio, actividades, ciudad, dia, mes, año))
    except Exception as e:
        bot.send_message(message.chat.id, f"Error al ingresar el año(reglamento): {e}")


def objetivo(message, matricula, nombre, edad, sexo, domicilio,
             telefono, carrera, semestre, periodo, correo, dependencia, titular, domicilio_dependencia,
             responsable, jefe, programa, modalidad, fecha_inicio, actividades,
             ciudad, dia, mes, año):
    try:
        objetivo_programa = message.text

        msg = bot.send_message(message.chat.id, "Por favor, ingresa el objetivo del programa:")
        msg = bot.send_message(message.chat.id, "Ejemplo: Tener en orden la documentación del departamento.")
        bot.register_next_step_handler(msg, lambda msg: tipo_programa(msg, matricula, nombre, edad, sexo,
                                                                      domicilio, telefono, carrera, semestre,
                                                                      periodo,
                                                                      correo,
                                                                      dependencia, titular, domicilio_dependencia,
                                                                      responsable, jefe, programa,
                                                                      modalidad,
                                                                      fecha_inicio, actividades, ciudad, dia, mes, año,
                                                                      objetivo_programa))
    except Exception as e:
        bot.send_message(message.chat.id, f"Error al ingresar el objetivo del programa: {e}")


def tipo_programa(message, matricula, nombre, edad, sexo, domicilio,
                  telefono, carrera, semestre, periodo, correo, dependencia, titular, domicilio_dependencia,
                  responsable, jefe, programa, modalidad, fecha_inicio, actividades,
                  ciudad, dia, mes, año, objetivo_programa):
    try:
        tipo_programa_seleccion = message.text
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(types.KeyboardButton("Educación para adultos (X)"),
                   types.KeyboardButton("Actividades deportivas (X)"),
                   types.KeyboardButton("Actividades cívicas (X)"),
                   types.KeyboardButton("Apoyo a la salud (X)"),
                   types.KeyboardButton("Actividades culturales (X)"),
                   types.KeyboardButton("Desarrollo sustentable (X)"),
                   types.KeyboardButton("Desarrollo de comunidad (X)"),
                   types.KeyboardButton("Otros (X)"))
        msg = bot.send_message(message.chat.id, "Por favor, selecciona el tipo de programa:", reply_markup=markup)
        bot.register_next_step_handler(msg, lambda msg: tipo_actividad(msg, matricula, nombre, edad, sexo,
                                                                       domicilio, telefono, carrera, semestre,
                                                                       periodo, correo, dependencia, titular,
                                                                       domicilio_dependencia, responsable, jefe,
                                                                       programa, modalidad, fecha_inicio,
                                                                       actividades,
                                                                       ciudad, dia, mes, año, objetivo_programa,
                                                                       tipo_programa_seleccion))
    except Exception as e:
        bot.send_message(message.chat.id, f"Error al seleccionar el tipo de programa: {e}")


def tipo_actividad(message, matricula, nombre, edad, sexo, domicilio,
                   telefono, carrera, semestre, periodo, correo, dependencia, titular, domicilio_dependencia,
                   responsable, jefe, programa, modalidad, fecha_inicio, actividades,
                   ciudad, dia, mes, año, objetivo_programa, tipo_programa_seleccion):
    try:
        actividad_seleccionada = message.text
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(types.KeyboardButton("ADMINISTRATIVAS (X)"),
                   types.KeyboardButton("TÉCNICAS (X)"),
                   types.KeyboardButton("ASESORIA (X)"),
                   types.KeyboardButton("INVESTIGACIÓN (X)"),
                   types.KeyboardButton("DOCENTES (X)"),
                   types.KeyboardButton("OTRAS"))
        msg = bot.send_message(message.chat.id, "Por favor, selecciona el tipo de actividad:", reply_markup=markup)
        bot.register_next_step_handler(msg, lambda msg: dependencia_validacion(msg, matricula, nombre, edad, sexo,
                                                                               domicilio, telefono, carrera, semestre,
                                                                               periodo, correo, dependencia, titular,
                                                                               domicilio_dependencia, responsable, jefe,
                                                                               programa, modalidad, fecha_inicio,
                                                                               actividades,
                                                                               ciudad, dia, mes, año, objetivo_programa,
                                                                               tipo_programa_seleccion,
                                                                               actividad_seleccionada))
    except Exception as e:
        bot.send_message(message.chat.id, f"Error al seleccionar el tipo de actividad: {e}")


def dependencia_validacion(message, matricula, nombre, edad, sexo, domicilio,
                           telefono, carrera, semestre, periodo, correo, dependencia, titular, domicilio_dependencia,
                           responsable, jefe, programa, modalidad, fecha_inicio, actividades,
                           ciudad, dia, mes, año, objetivo_programa, tipo_programa_seleccion,
                           actividad_seleccionada):
    try:
        dependencia_validacion = message.text
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(types.KeyboardButton("Si"),
                   types.KeyboardButton("No"))
        msg = bot.send_message(message.chat.id,
                               "¿El Servicio Social lo realizará dentro de las instalaciones de la dependencia?",
                               reply_markup=markup)
        bot.register_next_step_handler(msg, lambda msg: aviso_pdf(msg, matricula, nombre, edad, sexo,
                                                                  domicilio, telefono, carrera, semestre,
                                                                  periodo, correo, dependencia, titular,
                                                                  domicilio_dependencia, responsable, jefe,
                                                                  programa, modalidad, fecha_inicio,
                                                                  actividades, ciudad, dia, mes, año,
                                                                  objetivo_programa, tipo_programa_seleccion,
                                                                  actividad_seleccionada,
                                                                  dependencia_validacion))
    except Exception as e:
        bot.send_message(message.chat.id, f"Error en validar la dependencia: {e}")


def aviso_pdf(message, matricula, nombre, edad, sexo, domicilio,
              telefono, carrera, semestre, periodo, correo, dependencia, titular, domicilio_dependencia, responsable,
              jefe, programa, modalidad, fecha_inicio, actividades, ciudad, dia, mes, año,
              objetivo_programa, tipo_programa_seleccion, actividad_seleccionada, dependencia_validacion):
    try:
        bot.send_message(message.chat.id, "Espera, tu archivo PDF está siendo generado 😁"
                                          "\nSi presentas algún problema, reinicia el proceso.")
        pdf(message, matricula, nombre, edad, sexo, domicilio, telefono, carrera, semestre, periodo, correo,
            dependencia, titular, domicilio_dependencia, responsable, jefe, programa, modalidad, fecha_inicio,
            actividades, ciudad, dia, mes, año, objetivo_programa, tipo_programa_seleccion, actividad_seleccionada,
            dependencia_validacion)

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(types.KeyboardButton("Regresar al menú principal"))
        bot.send_message(message.chat.id, "NOTA: Recuerda imprimir tus formatos generados.")
        bot.send_message(message.chat.id, "¿Quieres volver al menú principal?", reply_markup=markup)
        bot.register_next_step_handler(message, regresar_menu_principal)
    except Exception as e:
        bot.send_message(message.chat.id, f"Error en aviso PDF: {e}")


@bot.message_handler(func=lambda message: True)
def regresar_menu_principal(message):
    try:
        if message.text == "Regresar al menú principal":
            markup = types.ReplyKeyboardMarkup(row_width=2)
            item1 = types.KeyboardButton("1. Información")
            item2 = types.KeyboardButton("2. Realizar registro")
            item3 = types.KeyboardButton("3. Generar formatos PDF | Servicio Social")
            markup.add(item1, item2, item3)

            bot.send_message(message.chat.id, "Selecciona una opción del teclado para continuar:")
            bot.send_message(message.chat.id,
                             "Aviso: Puedes hacer uso del comando /start para cambiar de campus en el caso "
                             "que sea disponible.", reply_markup=markup)
    except Exception as e:
        bot.send_message(message.chat.id, f"Error al regresar al menú principal: {e}")


# Generar PDF con ReportLab Library.
def pdf(message, matricula, nombre, edad, sexo, domicilio, telefono, carrera, semestre, periodo, creditos_aprobados,
        correo, dependencia, titular, domicilio_dependencia, responsable, jefe, programa, modalidad, fecha_inicio,
        actividades, ciudad, dia, mes, año, objetivo_programa, tipo_programa_seleccion, actividad_seleccionada):
    try:
        dependencia_validacion = message.text
        guardar_datos(nombre, matricula, correo, carrera, telefono, programa, actividades, modalidad)

        # Formato 01
        packet_1 = BytesIO()
        can1 = canvas.Canvas(packet_1, pagesize=letter)

        can1.setFontSize(10)
        can1.drawString(x=330, y=580, text=str(edad))
        can1.drawString(x=394, y=578, text=str(sexo))
        can1.drawString(x=400, y=524, text=str(semestre))
        can1.drawString(x=462, y=552, text=str(telefono))
        can1.drawString(x=385, y=498, text=str(creditos_aprobados))
        can1.setFontSize(13)
        can1.drawString(x=195, y=453, text=str(periodo))
        can1.setFontSize(7)
        can1.drawString(x=136, y=554, text=str(domicilio))
        can1.drawString(x=122, y=580, text=str(nombre))
        can1.setFontSize(9)
        can1.drawString(x=171, y=496, text=str(matricula))
        can1.drawString(x=135, y=524, text=str(carrera))
        can1.save()

        packet_1.seek(0)
        new_pdf1 = PdfReader(packet_1)

        existing_pdf = PdfReader(config("PDF_PATH"))
        output = PdfWriter()

        first_page = existing_pdf.pages[0]  # Pagina 01.
        first_page.merge_page(new_pdf1.pages[0])
        output.add_page(first_page)

        # Formato 02
        packet_2 = BytesIO()
        can2 = canvas.Canvas(packet_2, pagesize=letter)

        can2.setFontSize(9)
        can2.drawString(x=170, y=572, text=str(nombre))
        can2.drawString(x=107, y=548, text=str(sexo))
        can2.drawString(x=186, y=548, text=str(telefono))
        can2.drawString(x=160, y=525, text=str(correo))
        can2.drawString(x=180, y=490, text=str(matricula))
        can2.drawString(x=370, y=491, text=str(carrera))
        can2.drawString(x=160, y=467, text=str(periodo))
        can2.drawString(x=450, y=467, text=str(semestre))
        can2.drawString(x=167, y=434, text=str(dependencia))
        can2.drawString(x=200, y=410, text=str(titular))
        can2.drawString(x=60, y=375, text=str(jefe))
        can2.drawString(x=185, y=358, text=str(programa))
        can2.drawString(x=147, y=335, text=str(modalidad))
        can2.drawString(x=295, y=334, text=str(fecha_inicio))
        can2.drawString(x=60, y=300, text=str(actividades))
        can2.setFontSize(12)
        can2.drawString(x=57, y=220, text=str(tipo_programa_seleccion))
        can2.setFontSize(7)
        can2.drawString(x=306, y=549, text=str(domicilio))
        can2.save()

        packet_2.seek(0)
        new_pdf2 = PdfReader(packet_2)

        second_page = existing_pdf.pages[1]  # Pagina 02.
        second_page.merge_page(new_pdf2.pages[0])
        output.add_page(second_page)

        # Formato 03
        packet_3 = BytesIO()
        can3 = canvas.Canvas(packet_3, pagesize=letter)

        can3.setFontSize(9)
        can3.drawString(x=125, y=522, text=str(nombre))
        can3.drawString(x=470, y=522, text=str(matricula))
        can3.drawString(x=480, y=496, text=str(telefono))
        can3.drawString(x=128, y=475, text=str(carrera))
        can3.drawString(x=425, y=475, text=str(semestre))
        can3.drawString(x=150, y=453, text=str(dependencia))
        can3.drawString(x=60, y=417, text=str(domicilio_dependencia))
        can3.drawString(x=60, y=388, text=str(responsable))
        can3.drawString(x=185, y=371, text=str(fecha_inicio))
        can3.drawString(x=190, y=281, text=str(ciudad))
        can3.drawString(x=495, y=281, text=str(dia))
        can3.drawString(x=130, y=268, text=str(mes))
        can3.drawString(x=285, y=268, text=str(año))
        can3.setFontSize(7)
        can3.drawString(x=130, y=498, text=str(domicilio))
        can3.save()

        packet_3.seek(0)
        new_pdf3 = PdfReader(packet_3)

        third_page = existing_pdf.pages[2]  # Pagina 03.
        third_page.merge_page(new_pdf3.pages[0])
        output.add_page(third_page)

        # Formato 04
        packet_4 = BytesIO()
        can4 = canvas.Canvas(packet_4, pagesize=letter)

        can4.setFontSize(7)
        can4.drawString(x=185, y=545, text=str(nombre))
        can4.drawString(x=135, y=520, text=str(domicilio))
        can4.drawString(x=50, y=380, text=str(programa))
        can4.drawString(x=245, y=380, text=str(objetivo_programa))
        can4.drawString(x=55, y=320, text=str(actividades))
        can4.drawString(x=55, y=270, text=str(actividad_seleccionada))
        can4.setFontSize(10)
        can4.drawString(x=80, y=222, text=str(dependencia_validacion))
        can4.setFontSize(9)
        can4.drawString(x=430, y=545, text=str(edad))
        can4.drawString(x=510, y=545, text=str(sexo))
        can4.drawString(x=480, y=520, text=str(telefono))
        can4.drawString(x=135, y=486, text=str(carrera))
        can4.drawString(x=440, y=486, text=str(semestre))
        can4.drawString(x=175, y=460, text=str(matricula))
        can4.drawString(x=450, y=460, text=str(creditos_aprobados))
        can4.setFontSize(10)
        can4.drawString(x=155, y=178, text=str(dia) + " de " + str(mes) + " del " + str(año))
        can4.save()

        packet_4.seek(0)
        new_pdf4 = PdfReader(packet_4)

        four_page = existing_pdf.pages[3]  # Pagina 04.
        four_page.merge_page(new_pdf4.pages[0])
        output.add_page(four_page)

        for page_number in range(4, len(existing_pdf.pages)):
            page = existing_pdf.pages[page_number]
            output.add_page(page)

        modified_pdf_filename = f"{matricula}.pdf"
        modified_pdf_path = os.path.join(config("MODIFIED_PDF_PATH"), modified_pdf_filename)
        with open(modified_pdf_path, "wb") as output_stream:
            output.write(output_stream)

        with open(modified_pdf_path, "rb") as modified_pdf_file:
            bot.send_document(message.chat.id, modified_pdf_file)

            os.remove(modified_pdf_path)

    except Exception as e:
        bot.send_message(message.chat.id, f"Error al proporcionar los formatos: {e}")


def crear_tabla():
    route_db = config('DB')
    with sqlite3.connect(route_db) as conn:
        conexion = conn.cursor()
        conexion.execute(config("SENTENCE_04"))
        conn.commit()


def guardar_datos(nombre, matricula, correo, carrera, telefono, programa, actividades, modalidad):
    route_db = config('DB')
    with sqlite3.connect(route_db) as conn:
        conexion = conn.cursor()
        conexion.execute(config("SENTENCE_05"),
                         (nombre, matricula, correo, carrera, telefono, programa, actividades, modalidad))
        conn.commit()


crear_tabla()
bot.polling()
