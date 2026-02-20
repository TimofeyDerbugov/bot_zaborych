import csv
import math
import os
import time
import os
import asyncio
from tkinter import Image
import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

from aiogram.types import FSInputFile
# --- Загрузка цен из CSV ---
def load_prices(filename="prices.csv"):
    prices = {}
    with open(filename, newline='', encoding="utf-8") as f:
        # Попробуем autodetect разделитель
        first_line = f.readline()
        delimiter = ';' if ';' in first_line else ','
        f.seek(0)

        reader = csv.DictReader(f, delimiter=delimiter)
        # Убираем случайные пробелы в заголовках
        reader.fieldnames = [name.strip() for name in reader.fieldnames]

        if "key" not in reader.fieldnames or "price" not in reader.fieldnames:
            raise ValueError(f"CSV должен содержать столбцы 'key' и 'price'. Найдено: {reader.fieldnames}")

        for row in reader:
            prices[row["key"].strip()] = float(row["price"].strip())
    return prices

# --- Основная функция расчёта ---
# def calculate(perimeter, material, zazor, kalitka, vorota, demontazh, distance):
#     prices = load_prices()
#
#     # Имена и цены
#     zabor_name = ""
#     zazor_name = "Без зазора"
#     kalitka_name = "Без калитки"
#     vorota_name = "Без ворот"
#
#     zena_kalitka = 0
#     vorota_zena = 0
#     zena = 0
#     kolvo = 0
#     obsh_krepezh = 0
#
#     # --- Калитка ---
#     if kalitka == 1:
#         kalitka_name = "Калитка эконом"
#         zena_kalitka = prices["kalitka_eco"]
#     elif kalitka == 2:
#         kalitka_name = "Калитка с замком"
#         zena_kalitka = prices["kalitka_lock"]
#
#     # --- Ворота ---
#     if f"vorota_{vorota}" in prices:
#         vorota_name = f"Ворота вариант {vorota}"
#         if vorota == 1:
#             vorota_zena = prices["vorota_1"]
#         elif vorota == 2:
#             vorota_zena = prices["vorota_2"]
#         elif vorota == 3:
#             vorota_zena = prices["vorota_3"]
#         elif vorota == 14:
#             vorota_zena = prices["vorota_14"]
#         elif vorota == 24:
#             vorota_zena = prices["vorota_24"]
#         elif vorota == 34:
#             vorota_zena = prices["vorota_34"]
#     # --- Столбы ---
#     kolvo_stolbov = math.floor(perimeter / 2.5) + 1
#     if material in [1, 2]:
#         zena_stolbov = kolvo_stolbov * prices["stolb_3d"]
#     else:
#         zena_stolbov = kolvo_stolbov * prices["stolb_shtaket"]
#
#     # --- Общие расходы ---
#     sheben_zena = perimeter * prices["sheben_per_m"]
#     montage_zena = perimeter * prices["montage_per_m"]
#     dem_zena = perimeter * prices["demontazh_per_m"] if demontazh else 0
#     dostavka_zena = distance * prices["dostavka_km"]
#
#     # --- Материал ---
#     if material in [1, 2]:
#         zabor_name = "3D сетка"
#         kolvo = perimeter / 2.5
#         zena = kolvo * (prices["setka_3d_eco"] if material == 1 else prices["setka_3d_premium"])
#         krepezh = 6 * kolvo
#         obsh_krepezh = krepezh * prices["krepezh_setka"]
#
#     elif material == 3:
#         zabor_name = "Профлист"
#         kolvo = perimeter / 1.1
#         zena = kolvo * prices["proflist"]
#         krepezh = 8 * kolvo
#         obsh_krepezh = krepezh * prices["krepezh_proflist"]
#
#     else:
#         zabor_name = "Штакетник"
#         zazor_map = {
#             1: (7.6, "2 см"),
#             2: (7.6, "2 см"),
#             3: (6.6, "4 см"),
#             4: (6.6, "4 см"),
#             5: (11, "6 см"),
#             6: (10, "8 см")
#         }
#         if zazor in zazor_map:
#             koef, name = zazor_map[zazor]
#             kolvo = perimeter * koef
#             zazor_name = name
#
#         if zazor in [1, 3] and material == 4:
#             zena = kolvo * prices["shtaket_175"]
#         elif zazor in [2, 4, 5, 6] and material == 4:
#             zena = kolvo * prices["shtaket_185"]
#         elif zazor in [2, 4, 5, 6] and material == 5:
#             zena = kolvo * prices["shtaket_200"]
#         else:
#             zena = kolvo * prices["shtaket_190"]
#
#         krepezh = (kolvo * 2) + (kolvo * 4)
#         obsh_krepezh = krepezh * prices["krepezh_shtaket"]
#
#     # --- Итог ---
#     obshaya_zena = zena + zena_kalitka + vorota_zena + sheben_zena + dem_zena + montage_zena + obsh_krepezh
#
#     return f"""
# Забор: {zabor_name}, {round(kolvo)} шт., {round(zena)} руб.
# Зазор: {zazor_name}
# Калитка: {kalitka_name},
# Ворота: {vorota_name},
# Щебень: {round(sheben_zena)} руб.
# Работа: {round(dem_zena)} руб. - демонтаж, {round(montage_zena)} руб. - монтаж
#
# ИТОГО: {round(obshaya_zena)} руб. + {round(dostavka_zena)} руб. - доставка
# """


# --- Тестовый запуск ---
# if __name__ == "__main__":
#     perimeter = float(input("Периметр (м): "))
#     material = int(input("Материал (1-5): "))
#     zazor = int(input("Зазор (1-6): "))
#     kalitka = int(input("Калитка (0-2): "))
#     vorota = int(input("Ворота (код): "))
#     demontazh = int(input("Демонтаж (0/1): "))
#     distance = float(input("Расстояние (км): "))
#
    # print(calculate(perimeter, material, zazor, kalitka, vorota, demontazh, distance))
#



per = 0
zab = 0
kal = 0
dem = 0
vor = 0
rust = 0
zaz = 0
API_TOKEN = '8360048034:AAFhMutaAqRBCElG4blTcIc2fU73qPxOgSI'
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
import asyncio
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

user_numbers = {}

# Команда /mech — бот просит ввести число
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("""
Приветствую!
Это бот для создания сметы
/inf - дополнительная информация
/mech - создание сметы
Приятного использования
    """)

@dp.message(Command("inf"))
async def cmd_start(message: types.Message):
    await message.answer("""
Тип заборов:
0: без забора
1: ворота эконом
2: ворота до 4 метров
3: ворота до 5 метров
14: ворота эконом + автоматика
24: ворота до 4 метров + автоматика
34: ворота до 5 метров + автоматика

Расчет доставки не предоставляется. 
Выбор зазора штакетника будет в любом случае. Если был выбран НЕ Штакетник, выбираем любой пункт, он не будет учитываться
    """)


@dp.message(Command("mech"))
async def cmd_number(message: types.Message):
    await message.answer("Введи периметр")


@dp.message(F.text)
async def get_number(message: types.Message):
    try:
        num = int(message.text)
        user_numbers[message.from_user.id] = num
        global per
        per = user_numbers[message.from_user.id]

        # Создаём inline-кнопки
        kb = InlineKeyboardBuilder()
        kb.button(text="🔹 3D Сетка 1.5м", callback_data="0")
        kb.button(text="🔹 3D сетка 1.8м", callback_data="1")
        kb.button(text="🔹 Профлист", callback_data="2")
        kb.button(text="🔹 Штакетнк 1.8м", callback_data="3")
        kb.button(text="🔹 Штакетнк 2м", callback_data="4")
        kb.adjust(1)  # по 2 кнопки в ряд

        await message.answer(
            f"Периметр сохранён: {num}\nТеперь выбери тип забора",
            reply_markup=kb.as_markup()
        )
    except ValueError:
        await message.answer("Пожалуйста, введи число!")

@dp.callback_query(lambda c: c.data in ["0","1","2","3","4"])
async def handle_button(callback: types.CallbackQuery):
    index = int(callback.data)  # индекс кнопки
    user_numbers[callback.from_user.id] = user_numbers.get(callback.from_user.id, 0)  # если нужен периметр
    # Сохраняем индекс выбора
    user_numbers[f"{callback.from_user.id}_type"] = index

    # Можно вывести выбор
    await callback.answer()  # убрать "часики"
    global zab
    zab = index
    kb2 = InlineKeyboardBuilder()
    kb2.button(text="🔹 Без калитки", callback_data="5")
    kb2.button(text="🔹 Калитка без замка", callback_data="6")
    kb2.button(text="🔹 Калитка с замком", callback_data="7")
    kb2.adjust(1)  # две кнопки в ряд

    await callback.message.answer(
        "Выберите модификацию калитки",
        reply_markup=kb2.as_markup()
    )

@dp.callback_query(lambda c: c.data in ["5","6","7"])
async def handle_gate(callback: types.CallbackQuery):
    global kal
    kal = int(callback.data)
    user_id = callback.from_user.id
    user_numbers[f"{user_id}_kalitka"] = kal

    await callback.answer()
    kb3 = InlineKeyboardBuilder()
    kb3.button(text="🔹 Без ворот", callback_data="8")
    kb3.button(text="🔹 Ворота до 4м", callback_data="9")
    kb3.button(text="🔹 Ворота до 5 м", callback_data="10")
    kb3.button(text="🔹 Эконом", callback_data="11")
    kb3.button(text="🔹 Ворота до 4м + автоматика", callback_data="12")
    kb3.button(text="🔹 Ворота до 5м + автоматика", callback_data="13")
    kb3.button(text="🔹 Ворота эконом + автоматика", callback_data="14")
    kb3.adjust(1)  # две кнопки в ряд

    await callback.message.answer(
        "Выберите модификацию ворот",
        reply_markup=kb3.as_markup()
    )

@dp.callback_query(lambda c: c.data in ["8","9","10","11","12","13","14"])
async def handle_gates(callback: types.CallbackQuery):
    global vor
    vor = int(callback.data)
    user_id = callback.from_user.id
    user_numbers[f"{user_id}_kalitka"] = vor

    await callback.answer()
    kb5 = InlineKeyboardBuilder()
    kb5.button(text="🔹 2", callback_data="17")
    kb5.button(text="🔹 2 двустр", callback_data="18")
    kb5.button(text="🔹 4", callback_data="19")
    kb5.button(text="🔹 4 двустр", callback_data="20")
    kb5.button(text="🔹 6 шахм", callback_data="21")
    kb5.button(text="🔹 8 шахм", callback_data="22")

    kb5.adjust(1)  # две кнопки в ряд

    await callback.message.answer(
        "Выберите модификацию штакетника.\nЕсли выбрали не штакетник выбирайте любой",
        reply_markup=kb5.as_markup()
    )

@dp.callback_query(lambda c: c.data in ["17", "18","19","20","21","22"])
async def handle_gatesss(callback: types.CallbackQuery):
    global zaz
    zaz = int(callback.data)

    user_id = callback.from_user.id
    user_numbers[f"{user_id}_dem"] = zaz

    await callback.answer()

    kb4 = InlineKeyboardBuilder()
    kb4.button(text="🔹 Демонтаж", callback_data="15")
    kb4.button(text="🔹 Без демонтажа", callback_data="16")

    kb4.adjust(1)  # две кнопки в ряд

    await callback.message.answer(
        "Выберите модификацию демонтажа",
        reply_markup=kb4.as_markup()
    )


@dp.callback_query(lambda c: c.data in ["15", "16"])
async def handle_gatess(callback: types.CallbackQuery, reportlab=None):
    global dem
    global vor
    global zaz
    dem = int(callback.data)

    user_id = callback.from_user.id
    user_numbers[f"{user_id}_dem"] = dem

    await callback.answer()

# 01234
# zab

# 567
# kal

# 891011121314
# vor
    zaz = zaz - 16
    if vor == 8:
        vor = 0
    elif vor == 9:
        vor = 2
    elif vor == 10:
        vor = 3
    elif vor == 11:
        vor = 1
    elif vor == 12:
        vor = 24
    elif vor == 13:
        vor = 34
    elif vor == 14:
        vor =14

    if dem == 15:
        dem = 1
    elif dem == 16:
        dem = 0
# 1516
# dem

    def calculate(perimeter, material, zazor, kalitka, vorota, demontazh, distance):
        prices = load_prices()

        # Имена и цены
        zabor_name = ""
        zazor_name = "Без зазора"
        kalitka_name = "Без калитки"
        vorota_name = "Без ворот"

        zena_kalitka = 0
        vorota_zena = 0
        zena = 0
        kolvo = 0
        obsh_krepezh = 0

        # --- Калитка ---
        if kalitka == 1:
            kalitka_name = "Калитка эконом"
            zena_kalitka = prices["kalitka_eco"]
        elif kalitka == 2:
            kalitka_name = "Калитка с замком"
            zena_kalitka = prices["kalitka_lock"]

        # --- Ворота ---
        if f"vorota_{vorota}" in prices:
            vorota_name = f"Ворота вариант {vorota}"
            if vorota == 1:
                vorota_zena = prices["vorota_1"]
            elif vorota == 2:
                vorota_zena = prices["vorota_2"]
            elif vorota == 3:
                vorota_zena = prices["vorota_3"]
            elif vorota == 14:
                vorota_zena = prices["vorota_14"]
            elif vorota == 24:
                vorota_zena = prices["vorota_24"]
            elif vorota == 34:
                vorota_zena = prices["vorota_34"]
        # --- Столбы ---
        kolvo_stolbov = math.floor(perimeter / 2.5) + 1
        if material in [1, 2]:
            zena_stolbov = kolvo_stolbov * prices["stolb_3d"]
        else:
            zena_stolbov = kolvo_stolbov * prices["stolb_shtaket"]

        # --- Общие расходы ---
        sheben_zena = perimeter * prices["sheben_per_m"]
        montage_zena = perimeter * prices["montage_per_m"]
        dem_zena = perimeter * prices["demontazh_per_m"] if demontazh else 0
        dostavka_zena = distance * prices["dostavka_km"]

        # --- Материал ---
        if material in [1, 2]:
            zabor_name = "3D сетка"
            kolvo = perimeter / 2.5
            zena = kolvo * (prices["setka_3d_eco"] if material == 1 else prices["setka_3d_premium"])
            krepezh = 6 * kolvo
            obsh_krepezh = krepezh * prices["krepezh_setka"]

        elif material == 3:
            zabor_name = "Профлист"
            kolvo = perimeter / 1.1
            zena = kolvo * prices["proflist"]
            krepezh = 8 * kolvo
            obsh_krepezh = krepezh * prices["krepezh_proflist"]

        else:
            zabor_name = "Штакетник"
            zazor_map = {
                1: (7.6, "2 см"),
                2: (7.6, "2 см"),
                3: (6.6, "4 см"),
                4: (6.6, "4 см"),
                5: (11, "6 см"),
                6: (10, "8 см")
            }
            if zazor in zazor_map:
                koef, name = zazor_map[zazor]
                kolvo = perimeter * koef
                zazor_name = name

            if zazor in [1, 3] and material == 4:
                zena = kolvo * prices["shtaket_175"]
            elif zazor in [2, 4, 5, 6] and material == 4:
                zena = kolvo * prices["shtaket_185"]
            elif zazor in [2, 4, 5, 6] and material == 5:
                zena = kolvo * prices["shtaket_200"]
            else:
                zena = kolvo * prices["shtaket_190"]

            krepezh = (kolvo * 2) + (kolvo * 4)
            obsh_krepezh = krepezh * prices["krepezh_shtaket"]

        # --- Итог ---
        obshaya_zena = zena + zena_kalitka + vorota_zena + sheben_zena + dem_zena + montage_zena + obsh_krepezh
        alkj = [zabor_name, kolvo, zena, zazor_name, kalitka_name, zena_kalitka, vorota_name, vorota_zena, sheben_zena, dem_zena, montage_zena, obshaya_zena]
        return alkj
#         f"""
# Забор: {zabor_name}, {round(kolvo)} шт., {round(zena)} руб.
# Зазор: {zazor_name}
# Калитка: {kalitka_name}, {zena_kalitka} руб.
# Ворота: {vorota_name}, {vorota_zena} руб.
# Щебень: {round(sheben_zena)} руб.
# Работа:
# {round(dem_zena)} руб. - демонтаж.
# {round(montage_zena)} руб. - монтаж
#
# ИТОГО: {round(obshaya_zena)} руб. + доставка рассчитывается индивидуально
#     """
    perimeter = per
    material = zab + 1
    zazor = zaz
    kalitka = kal - 5
    vorota = vor
    demontazh = dem - 15
    distance = 0
    srt = calculate(perimeter, material, zazor, kalitka, vorota, demontazh, distance)
    all_text = f"Забор: {srt[0]}, {round(srt[1])} шт., {round(srt[2])} руб.\nЗазор: {srt[3]}\nКалитка: {srt[4]}, {srt[5]} руб.\nВорота: {srt[6]}, {srt[7]} руб.\nЩебень: {round(srt[8])} руб.\nРабота:\n{round(srt[9])} руб. - демонтаж.\n{round(srt[10])} руб. - монтаж\n\nИТОГО: {round(srt[11])} руб. + доставка рассчитывается индивидуально"
    await callback.message.answer(all_text)


        # Путь к шрифту — лежит в той же папке, что и код
    print("Функция вызвана")

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    font_path = os.path.join(BASE_DIR, "DejaVuSans.ttf")
    logo_path = os.path.join(BASE_DIR, "logo.png")
    pdf_path = os.path.join(BASE_DIR, "example.pdf")

    # Проверка существования файлов


    # Регистрация шрифта
    if "DejaVu" not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont("DejaVu", font_path))

    # Создание PDF
    doc = SimpleDocTemplate(pdf_path)

    style = ParagraphStyle(
        name="Normal",
        fontName="DejaVu",
        fontSize=15,
        textColor=colors.black
    )

    # Создание элементов
    logo = Image(logo_path, width=400, height=200)
    logo.hAlign = 'CENTER'

    elements = [
        logo,
        Spacer(1, 20),  # отступ
        # Paragraph(all_text, style)
    ]
    for line in all_text.split("\n"):
        elements.append(Paragraph(line, style))
        elements.append(Spacer(1, 10))  # отступ между строками
    doc.build(elements)

    # Отправка PDF
    file = FSInputFile(pdf_path)
    await callback.message.answer_document(file, caption="Вот ваш PDF")
    print("send")
    # await message.answer_document(file, caption="Вот ваш PDF")

    # Удаление файла
    os.remove(pdf_path)

    # print(calculate(perimeter, material, zazor, kalitka, vorota, demontazh, distance))



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

# Код	Название ворот	Примечание/Цена
# 1	ВОРОТА эконом	21000 руб.
# 2	Ворота до 4 м	80000 руб.
# 3	Ворота до 5 м	90000 руб.
# 14 ВОРОТА эконом + автоматика	84000 руб.
# 24 Ворота до 4 м + автоматика	143000 руб.
# 34 Ворота до 5 м + автоматика	153000 руб.