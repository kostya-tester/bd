import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import sqlite3
import os
import sys
from datetime import datetime


class DefectDatabase:
    """Класс для работы с базой данных дефектов"""

    def __init__(self, db_name=None):
        # Путь к базе данных в папке с программой
        if db_name is None:
            if getattr(sys, 'frozen', False):
                # Если запущено как EXE
                app_dir = os.path.dirname(sys.executable)
            else:
                # Если запущено как скрипт
                app_dir = os.path.dirname(os.path.abspath(__file__))
            db_name = os.path.join(app_dir, "defects.db")

        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.insert_default_data()

    def create_tables(self):
        """Создание таблиц базы данных"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS defects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                causes TEXT NOT NULL,
                ndt_methods TEXT NOT NULL,
                color TEXT DEFAULT '#8e44ad',
                created_date TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def insert_default_data(self):
        """Вставка стандартных 19 типов дефектов"""
        # Проверяем, есть ли уже данные
        self.cursor.execute("SELECT COUNT(*) FROM defects")
        if self.cursor.fetchone()[0] > 0:
            return

        default_defects = [
            ("Поры",
             "• Недостаточное газовыделение из сварочной ванны\n• Высокая скорость сварки\n• Загрязнение сварочных материалов\n• Повышенная влажность электродов\n• Наличие ржавчины на свариваемых кромках",
             "• Рентгенографический контроль\n• Гамма-дефектоскопия\n• Ультразвуковой контроль\n• Визуально-измерительный контроль\n• Компьютерная томография"),

            ("Трещины",
             "• Высокие термические напряжения\n• Неправильный выбор сварочных материалов\n• Дефекты основного металла\n• Нарушение технологии сварки\n• Повышенная скорость охлаждения",
             "• Ультразвуковой контроль\n• Магнитопорошковый контроль\n• Капиллярный контроль\n• Рентгенографический контроль\n• Вихретоковый контроль"),

            ("Включения",
             "• Плохая очистка свариваемых кромок\n• Низкое качество электродов\n• Неправильный режим сварки\n• Загрязнение защитного газа\n• Эрозия вольфрамового электрода",
             "• Рентгенографический контроль\n• Ультразвуковой контроль\n• Визуально-измерительный контроль\n• Компьютерная томография\n• Гамма-дефектоскопия"),

            ("Непровар",
             "• Недостаточная сила сварочного тока\n• Неправильная разделка кромок\n• Высокая скорость сварки\n• Неправильный угол наклона электрода\n• Чрезмерное смещение электрода",
             "• Ультразвуковой контроль\n• Рентгенографический контроль\n• Гамма-дефектоскопия\n• Визуально-измерительный контроль\n• Тепловой контроль"),

            ("Подрез",
             "• Повышенная сила сварочного тока\n• Неправильная техника сварки\n• Большая скорость сварки\n• Неправильное положение электрода\n• Несоответствие диаметра электрода",
             "• Визуально-измерительный контроль\n• Капиллярный контроль\n• Магнитопорошковый контроль\n• Ультразвуковой контроль\n• Вихретоковый контроль"),

            ("Наплыв",
             "• Избыточное количество наплавленного металла\n• Низкая скорость сварки\n• Неправильный угол наклона электрода\n• Повышенная сила тока\n• Неправильное положение шва в пространстве",
             "• Визуально-измерительный контроль\n• Измерение геометрических параметров\n• Лазерное сканирование\n• Ультразвуковой контроль\n• Профилометрия"),

            ("Прожог",
             "• Чрезмерная сила сварочного тока\n• Большой зазор между кромками\n• Малая толщина основного металла\n• Медленная скорость сварки\n• Недостаточное притупление кромок",
             "• Визуально-измерительный контроль\n• Рентгенографический контроль\n• Ультразвуковой контроль\n• Тепловизионный контроль\n• Компьютерная томография"),

            ("Утяжина",
             "• Усадка металла при кристаллизации\n• Неправильная форма разделки\n• Недостаточное заполнение кратера\n• Резкое прерывание дуги\n• Неправильный режим сварки",
             "• Визуально-измерительный контроль\n• Ультразвуковой контроль\n• Капиллярный контроль\n• Рентгенографический контроль\n• Компьютерная томография"),

            ("Расслоение",
             "• Дефекты прокатки металла\n• Наличие неметаллических включений\n• Внутренние напряжения в металле\n• Нарушение технологии выплавки\n• Водородное охрупчивание",
             "• Ультразвуковой контроль\n• Рентгенографический контроль\n• Акустическая эмиссия\n• Вихретоковый контроль\n• Компьютерная томография"),

            ("Зашлаковка",
             "• Нарушение режима шлакоотделения\n• Недостаточная очистка предыдущего слоя\n• Использование некачественного флюса\n• Неправильный угол наклона электрода\n• Слишком быстрая кристаллизация",
             "• Рентгенографический контроль\n• Ультразвуковой контроль\n• Компьютерная томография\n• Визуально-измерительный контроль\n• Гамма-дефектоскопия"),

            ("Смещение кромок",
             "• Неправильная сборка стыка\n• Некачественное закрепление деталей\n• Деформация свариваемых элементов\n• Неточности в подготовке кромок\n• Отсутствие приспособлений для сборки",
             "• Визуально-измерительный контроль\n• Шаблонный контроль\n• Лазерное 3D-сканирование\n• Ультразвуковой контроль\n• Координатно-измерительные машины"),

            ("Непроплавление",
             "• Недостаточная температура сварочной ванны\n• Наличие окисных пленок\n• Высокая теплопроводность основного металла\n• Неправильный угол сварки\n• Загрязнение свариваемых поверхностей",
             "• Ультразвуковой контроль\n• Рентгенографический контроль\n• Тепловой контроль\n• Вихретоковый контроль\n• Компьютерная томография"),

            ("Брызги металла",
             "• Повышенная сила сварочного тока\n• Неправильный угол наклона электрода\n• Избыточная длина дуги\n• Повышенное напряжение дуги\n• Некачественные сварочные материалы",
             "• Визуально-измерительный контроль\n• Контроль чистоты поверхности\n• Оптическая микроскопия\n• Капиллярный контроль\n• Магнитопорошковый контроль"),

            ("Свищ",
             "• Интенсивное газовыделение из сварочной ванны\n• Загрязнение сварочных материалов\n• Неправильный режим сварки\n• Влажность защитных газов\n• Нарушение герметичности шва",
             "• Капиллярный контроль\n• Гидравлические испытания\n• Вакуумный контроль\n• Гелиевый течеискатель\n• Ультразвуковой контроль"),

            ("Оксидная пленка",
             "• Окисление поверхности при сварке\n• Недостаточная защита сварочной ванны\n• Высокая температура сварки\n• Загрязнение защитного газа\n• Нарушение газовой защиты",
             "• Визуально-измерительный контроль\n• Металлографический анализ\n• Спектральный анализ\n• Рентгеновская спектроскопия\n• Ультразвуковой контроль"),

            ("Межкристаллитная коррозия",
             "• Обеднение границ зерен хромом\n• Неправильная термообработка\n• Чувствительность к межкристаллитной коррозии\n• Длительное воздействие высоких температур\n• Агрессивная среда эксплуатации",
             "• Ультразвуковой контроль\n• Вихретоковый контроль\n• Рентгенографический контроль\n• Акустическая эмиссия\n• Металлография реплик"),

            ("Вмятина",
             "• Механическое воздействие на поверхность\n• Ударные нагрузки при транспортировке\n• Падение посторонних предметов\n• Неправильное складирование\n• Деформация при монтаже",
             "• Визуально-измерительный контроль\n• Лазерное 3D-сканирование\n• Ультразвуковой контроль\n• Профилометрия\n• Голографическая интерферометрия"),

            ("Закат",
             "• Дефект прокатки металла\n• Закатывание окалины в металл\n• Нарушение технологии прокатки\n• Износ прокатных валков\n• Попадание посторонних частиц",
             "• Ультразвуковой контроль\n• Рентгенографический контроль\n• Вихретоковый контроль\n• Магнитопорошковый контроль\n• Капиллярный контроль"),

            ("Волосовина",
             "• Наличие неметаллических включений\n• Газовые пузыри при кристаллизации\n• Деформация металла при прокатке\n• Нарушение технологии выплавки\n• Загрязнение жидкого металла",
             "• Ультразвуковой контроль\n• Магнитопорошковый контроль\n• Капиллярный контроль\n• Вихретоковый контроль\n• Рентгенографический контроль")
        ]

        for name, causes, methods in default_defects:
            try:
                self.cursor.execute(
                    "INSERT INTO defects (name, causes, ndt_methods) VALUES (?, ?, ?)",
                    (name, causes, methods)
                )
            except sqlite3.IntegrityError:
                pass

        self.conn.commit()

    def get_all_defects(self):
        """Получение всех дефектов"""
        self.cursor.execute("SELECT id, name, causes, ndt_methods, color FROM defects ORDER BY id")
        return self.cursor.fetchall()

    def add_defect(self, name, causes, methods, color='#8e44ad'):
        """Добавление нового дефекта"""
        try:
            self.cursor.execute(
                "INSERT INTO defects (name, causes, ndt_methods, color) VALUES (?, ?, ?, ?)",
                (name, causes, methods, color)
            )
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            return None

    def update_defect(self, defect_id, name=None, causes=None, methods=None, color=None):
        """Обновление дефекта"""
        updates = []
        params = []

        if name:
            updates.append("name=?")
            params.append(name)
        if causes is not None:
            updates.append("causes=?")
            params.append(causes)
        if methods is not None:
            updates.append("ndt_methods=?")
            params.append(methods)
        if color:
            updates.append("color=?")
            params.append(color)

        if updates:
            params.append(defect_id)
            self.cursor.execute(
                f"UPDATE defects SET {', '.join(updates)} WHERE id=?",
                params
            )
            self.conn.commit()
            return True
        return False

    def delete_defect(self, defect_id):
        """Удаление дефекта"""
        self.cursor.execute("DELETE FROM defects WHERE id=?", (defect_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def search_defects(self, query):
        """Поиск дефектов"""
        self.cursor.execute(
            "SELECT id, name, causes, ndt_methods, color FROM defects WHERE name LIKE ? OR causes LIKE ? OR ndt_methods LIKE ?",
            (f'%{query}%', f'%{query}%', f'%{query}%')
        )
        return self.cursor.fetchall()


class DefectManagerApp:
    """Основное приложение управления дефектами"""

    def __init__(self, root):
        self.root = root
        self.root.title("База данных дефектов сварных соединений")
        self.root.geometry("1200x800")

        # Фиолетовая цветовая схема
        self.colors = {
            'bg': '#1a0033',  # Темно-фиолетовый фон
            'fg': '#ffffff',  # Белый текст
            'primary': '#8e44ad',  # Основной фиолетовый
            'success': '#9b59b6',  # Светло-фиолетовый
            'warning': '#a569bd',  # Пастельный фиолетовый
            'danger': '#6c3483',  # Темно-фиолетовый
            'dark': '#2c0a4a',  # Очень темный фиолетовый
            'light': '#e8daef',  # Светло-фиолетовый текст
            'button_bg': '#4a0072',  # Фиолетовый для кнопок
            'button_hover': '#6a1b9a',  # Фиолетовый при наведении
            'button_select': '#9c27b0',  # Выбранный фиолетовый
            'accent': '#ce93d8'  # Акцентный фиолетовый
        }

        self.root.configure(bg=self.colors['bg'])

        # Инициализация базы данных
        self.db = DefectDatabase()

        # Создание интерфейса
        self.create_menu()
        self.create_widgets()

        # Загрузка данных
        self.load_defects()

    def create_menu(self):
        """Создание меню приложения"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Меню "Файл"
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Новый дефект", command=self.add_new_defect)
        file_menu.add_command(label="Поиск", command=self.show_search)
        file_menu.add_separator()
        file_menu.add_command(label="Экспорт данных", command=self.export_data)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)

        # Меню "Правка"
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Правка", menu=edit_menu)
        edit_menu.add_command(label="Редактировать выбранный", command=self.edit_selected)
        edit_menu.add_command(label="Удалить выбранный", command=self.delete_selected)

        # Меню "Вид"
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Вид", menu=view_menu)
        view_menu.add_command(label="Обновить", command=self.refresh_data)
        view_menu.add_command(label="Статистика", command=self.show_statistics)

        # Меню "Справка"
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.show_about)

    def create_widgets(self):
        """Создание основных виджетов"""
        # Главный контейнер
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Верхняя панель с заголовком и поиском
        self.create_header(main_frame)

        # Панель с кнопками дефектов
        self.create_defects_grid(main_frame)

        # Информационная панель
        self.create_info_panel(main_frame)

        # Строка состояния
        self.create_status_bar()

    def create_header(self, parent):
        """Создание верхней панели"""
        header_frame = tk.Frame(parent, bg=self.colors['bg'])
        header_frame.pack(fill=tk.X, pady=(0, 10))

        # Заголовок
        title = tk.Label(
            header_frame,
            text="ДЕФЕКТЫ СВАРНЫХ СОЕДИНЕНИЙ",
            font=('Arial', 18, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['primary']
        )
        title.pack(side=tk.LEFT)

        # Кнопки управления
        controls = tk.Frame(header_frame, bg=self.colors['bg'])
        controls.pack(side=tk.RIGHT)

        buttons = [
            ("➕ Новый", self.add_new_defect, self.colors['success']),
            ("🔍 Поиск", self.show_search, self.colors['warning']),
            ("🔄 Обновить", self.refresh_data, self.colors['primary'])
        ]

        for text, command, color in buttons:
            btn = tk.Button(
                controls,
                text=text,
                command=command,
                bg=color,
                fg='white',
                font=('Arial', 10, 'bold'),
                relief=tk.FLAT,
                bd=1,
                padx=15,
                pady=5,
                cursor='hand2',
                activebackground=self.colors['button_hover'],
                activeforeground='white'
            )
            btn.pack(side=tk.LEFT, padx=2)
            self.button_hover_effect(btn, color)

    def create_defects_grid(self, parent):
        """Создание сетки с кнопками дефектов"""
        self.defects_frame = tk.Frame(parent, bg=self.colors['bg'])
        self.defects_frame.pack(fill=tk.X, pady=10)

        tk.Label(
            self.defects_frame,
            text="Выберите тип дефекта для просмотра информации:",
            font=('Arial', 11),
            bg=self.colors['bg'],
            fg=self.colors['light']
        ).pack(anchor=tk.W)

        # Контейнер для кнопок дефектов
        self.buttons_container = tk.Frame(self.defects_frame, bg=self.colors['bg'])
        self.buttons_container.pack(fill=tk.X, pady=10)

        self.defect_buttons = {}
        self.selected_defect_id = None

    def create_info_panel(self, parent):
        """Создание информационной панели"""
        info_frame = tk.Frame(parent, bg=self.colors['bg'])
        info_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Заголовок информационной панели
        info_header = tk.Frame(info_frame, bg=self.colors['primary'])
        info_header.pack(fill=tk.X, pady=(0, 10))

        tk.Label(
            info_header,
            text="ИНФОРМАЦИЯ О ДЕФЕКТЕ",
            font=('Arial', 12, 'bold'),
            bg=self.colors['primary'],
            fg='white',
            padx=20,
            pady=10
        ).pack()

        # Основной контейнер для информации
        content_frame = tk.Frame(info_frame, bg=self.colors['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Панель с основной информацией
        main_info = tk.Frame(content_frame, bg=self.colors['bg'])
        main_info.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        # Название дефекта
        self.name_label = tk.Label(
            main_info,
            text="",
            font=('Arial', 14, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['primary'],
            wraplength=500
        )
        self.name_label.pack(anchor=tk.W, pady=10)

        # Причины возникновения
        tk.Label(
            main_info,
            text="ПРИЧИНЫ ВОЗНИКНОВЕНИЯ:",
            font=('Arial', 11, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['warning']
        ).pack(anchor=tk.W)

        self.causes_text = scrolledtext.ScrolledText(
            main_info,
            height=8,
            bg=self.colors['dark'],
            fg=self.colors['light'],
            font=('Arial', 10),
            wrap=tk.WORD,
            relief=tk.FLAT,
            state=tk.DISABLED
        )
        self.causes_text.pack(fill=tk.BOTH, expand=True, pady=(5, 10))

        # Методы неразрушающего контроля
        tk.Label(
            main_info,
            text="МЕТОДЫ НЕРАЗРУШАЮЩЕГО КОНТРОЛЯ:",
            font=('Arial', 11, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['success']
        ).pack(anchor=tk.W)

        self.methods_text = scrolledtext.ScrolledText(
            main_info,
            height=8,
            bg=self.colors['dark'],
            fg=self.colors['light'],
            font=('Arial', 10),
            wrap=tk.WORD,
            relief=tk.FLAT,
            state=tk.DISABLED
        )
        self.methods_text.pack(fill=tk.BOTH, expand=True, pady=(5, 10))

        # Боковая панель с кнопками управления
        control_panel = tk.Frame(content_frame, bg=self.colors['bg'], width=150)
        control_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))

        control_buttons = [
            ("✏️ Редактировать", self.edit_selected, self.colors['primary']),
            ("🗑️ Удалить", self.delete_selected, self.colors['danger']),
            ("", None, None),  # Разделитель
            ("📊 Статистика", self.show_statistics, self.colors['warning']),
            ("💾 Экспорт", self.export_data, self.colors['success'])
        ]

        for text, command, color in control_buttons:
            if text:  # Пропускаем разделители
                btn = tk.Button(
                    control_panel,
                    text=text,
                    command=command,
                    bg=color,
                    fg='white',
                    font=('Arial', 10, 'bold'),
                    relief=tk.FLAT,
                    bd=1,
                    padx=15,
                    pady=8,
                    cursor='hand2',
                    width=20,
                    activebackground=self.colors['button_hover'],
                    activeforeground='white'
                )
                btn.pack(fill=tk.X, pady=2)
                self.button_hover_effect(btn, color)
            else:
                tk.Frame(control_panel, height=10, bg=self.colors['bg']).pack()

    def create_status_bar(self):
        """Создание строки состояния"""
        self.status_frame = tk.Frame(self.root, bg=self.colors['primary'])
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.status_label = tk.Label(
            self.status_frame,
            text="Готов к работе | Выберите дефект для просмотра информации",
            bg=self.colors['primary'],
            fg='white',
            font=('Arial', 9),
            padx=10,
            pady=5
        )
        self.status_label.pack(side=tk.LEFT)

        # Количество записей в базе
        self.count_label = tk.Label(
            self.status_frame,
            text="",
            bg=self.colors['primary'],
            fg='white',
            font=('Arial', 9),
            padx=10,
            pady=5
        )
        self.count_label.pack(side=tk.RIGHT)

    def button_hover_effect(self, button, original_color):
        """Добавление эффекта при наведении на кнопку"""

        def on_enter(e):
            button.configure(bg=self.colors['button_hover'])

        def on_leave(e):
            button.configure(bg=original_color)

        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)

    def load_defects(self, defects=None):
        """Загрузка и отображение дефектов"""
        # Очистка существующих кнопок
        for widget in self.buttons_container.winfo_children():
            widget.destroy()

        self.defect_buttons.clear()

        if defects is None:
            defects = self.db.get_all_defects()

        # Создание сетки кнопок (максимум 5 в ряд)
        row_frame = None
        for i, defect in enumerate(defects):
            if i % 5 == 0:
                row_frame = tk.Frame(self.buttons_container, bg=self.colors['bg'])
                row_frame.pack(fill=tk.X, pady=2)

            defect_id = defect[0]
            name = defect[1]

            btn = tk.Button(
                row_frame,
                text=name,
                bg=self.colors['button_bg'],
                fg='white',
                font=('Arial', 9, 'bold'),
                relief=tk.FLAT,
                bd=2,
                padx=10,
                pady=8,
                cursor='hand2',
                wraplength=150,
                height=2,
                width=18,
                activebackground=self.colors['button_hover'],
                activeforeground='white'
            )
            btn.pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)

            # Привязываем обработчики
            btn.bind('<Button-1>', lambda e, did=defect_id, b=btn: self.select_defect(did, b))
            btn.bind('<Enter>', lambda e, b=btn: b.configure(bg=self.colors['button_hover']))
            btn.bind('<Leave>', lambda e, b=btn, did=defect_id: b.configure(
                bg=self.colors['button_select'] if did == self.selected_defect_id else self.colors['button_bg']
            ))

            self.defect_buttons[defect_id] = btn

            # Выделяем выбранный дефект
            if defect_id == self.selected_defect_id:
                btn.configure(bg=self.colors['button_select'])

        # Обновление счетчика
        self.count_label.configure(text=f"Всего записей: {len(defects)}")

    def select_defect(self, defect_id, button):
        """Выбор дефекта и отображение информации"""
        # Сброс предыдущего выделения
        if self.selected_defect_id and self.selected_defect_id in self.defect_buttons:
            old_btn = self.defect_buttons[self.selected_defect_id]
            old_btn.configure(bg=self.colors['button_bg'])

        # Выделение нового
        self.selected_defect_id = defect_id
        button.configure(bg=self.colors['button_select'])

        # Отображение информации
        self.show_defect_info(defect_id)

    def show_defect_info(self, defect_id):
        """Отображение информации о выбранном дефекте"""
        defects = self.db.get_all_defects()

        for defect in defects:
            if defect[0] == defect_id:
                name = defect[1]
                causes = defect[2]
                methods = defect[3]

                # Обновление названия
                self.name_label.configure(text=name)

                # Обновление причин
                self.causes_text.configure(state=tk.NORMAL)
                self.causes_text.delete(1.0, tk.END)
                self.causes_text.insert(1.0, causes)
                self.causes_text.configure(state=tk.DISABLED)

                # Обновление методов
                self.methods_text.configure(state=tk.NORMAL)
                self.methods_text.delete(1.0, tk.END)
                self.methods_text.insert(1.0, methods)
                self.methods_text.configure(state=tk.DISABLED)

                # Обновление строки состояния
                self.status_label.configure(text=f"Выбран дефект: {name}")
                break

    def add_new_defect(self):
        """Добавление нового дефекта"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавление нового дефекта")
        dialog.geometry("600x500")
        dialog.configure(bg=self.colors['bg'])

        # Делаем диалог модальным
        dialog.transient(self.root)
        dialog.grab_set()

        # Заголовок
        tk.Label(
            dialog,
            text="ДОБАВЛЕНИЕ НОВОГО ДЕФЕКТА",
            font=('Arial', 14, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['primary']
        ).pack(pady=20)

        # Название
        tk.Label(
            dialog,
            text="Название дефекта:",
            font=('Arial', 11),
            bg=self.colors['bg'],
            fg=self.colors['light']
        ).pack(anchor=tk.W, padx=20)

        name_entry = tk.Entry(
            dialog,
            font=('Arial', 11),
            bg=self.colors['dark'],
            fg=self.colors['light'],
            insertbackground='white'
        )
        name_entry.pack(fill=tk.X, padx=20, pady=5)

        # Причины
        tk.Label(
            dialog,
            text="Причины возникновения:",
            font=('Arial', 11),
            bg=self.colors['bg'],
            fg=self.colors['light']
        ).pack(anchor=tk.W, padx=20)

        causes_text = scrolledtext.ScrolledText(
            dialog,
            height=6,
            font=('Arial', 10),
            bg=self.colors['dark'],
            fg=self.colors['light'],
            wrap=tk.WORD
        )
        causes_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)

        # Методы НК
        tk.Label(
            dialog,
            text="Методы неразрушающего контроля:",
            font=('Arial', 11),
            bg=self.colors['bg'],
            fg=self.colors['light']
        ).pack(anchor=tk.W, padx=20)

        methods_text = scrolledtext.ScrolledText(
            dialog,
            height=6,
            font=('Arial', 10),
            bg=self.colors['dark'],
            fg=self.colors['light'],
            wrap=tk.WORD
        )
        methods_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)

        def save_new_defect():
            name = name_entry.get().strip()
            causes = causes_text.get(1.0, tk.END).strip()
            methods = methods_text.get(1.0, tk.END).strip()

            if not name:
                messagebox.showerror("Ошибка", "Введите название дефекта")
                return

            if not causes:
                messagebox.showerror("Ошибка", "Введите причины возникновения")
                return

            if not methods:
                messagebox.showerror("Ошибка", "Введите методы неразрушающего контроля")
                return

            if self.db.add_defect(name, causes, methods):
                messagebox.showinfo("Успех", f"Дефект '{name}' успешно добавлен")
                self.refresh_data()
                dialog.destroy()
            else:
                messagebox.showerror("Ошибка", "Дефект с таким названием уже существует")

        # Кнопки
        buttons_frame = tk.Frame(dialog, bg=self.colors['bg'])
        buttons_frame.pack(fill=tk.X, pady=20, padx=20)

        tk.Button(
            buttons_frame,
            text="Сохранить",
            command=save_new_defect,
            bg=self.colors['success'],
            fg='white',
            font=('Arial', 11, 'bold'),
            relief=tk.FLAT,
            padx=20,
            pady=10,
            activebackground=self.colors['button_hover'],
            activeforeground='white'
        ).pack(side=tk.LEFT)

        tk.Button(
            buttons_frame,
            text="Отмена",
            command=dialog.destroy,
            bg=self.colors['danger'],
            fg='white',
            font=('Arial', 11),
            relief=tk.FLAT,
            padx=20,
            pady=10,
            activebackground=self.colors['button_hover'],
            activeforeground='white'
        ).pack(side=tk.RIGHT)

    def edit_selected(self):
        """Редактирование выбранного дефекта"""
        if not self.selected_defect_id:
            messagebox.showwarning("Предупреждение", "Выберите дефект для редактирования")
            return

        # Получаем данные текущего дефекта
        defects = self.db.get_all_defects()
        current_defect = None

        for defect in defects:
            if defect[0] == self.selected_defect_id:
                current_defect = defect
                break

        if not current_defect:
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Редактирование дефекта")
        dialog.geometry("600x500")
        dialog.configure(bg=self.colors['bg'])
        dialog.transient(self.root)
        dialog.grab_set()

        # Заголовок
        tk.Label(
            dialog,
            text="РЕДАКТИРОВАНИЕ ДЕФЕКТА",
            font=('Arial', 14, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['warning']
        ).pack(pady=20)

        # Название
        tk.Label(
            dialog,
            text="Название дефекта:",
            font=('Arial', 11),
            bg=self.colors['bg'],
            fg=self.colors['light']
        ).pack(anchor=tk.W, padx=20)

        name_entry = tk.Entry(
            dialog,
            font=('Arial', 11),
            bg=self.colors['dark'],
            fg=self.colors['light'],
            insertbackground='white'
        )
        name_entry.insert(0, current_defect[1])
        name_entry.pack(fill=tk.X, padx=20, pady=5)

        # Причины
        tk.Label(
            dialog,
            text="Причины возникновения:",
            font=('Arial', 11),
            bg=self.colors['bg'],
            fg=self.colors['light']
        ).pack(anchor=tk.W, padx=20)

        causes_text = scrolledtext.ScrolledText(
            dialog,
            height=6,
            font=('Arial', 10),
            bg=self.colors['dark'],
            fg=self.colors['light'],
            wrap=tk.WORD
        )
        causes_text.insert(1.0, current_defect[2])
        causes_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)

        # Методы НК
        tk.Label(
            dialog,
            text="Методы неразрушающего контроля:",
            font=('Arial', 11),
            bg=self.colors['bg'],
            fg=self.colors['light']
        ).pack(anchor=tk.W, padx=20)

        methods_text = scrolledtext.ScrolledText(
            dialog,
            height=6,
            font=('Arial', 10),
            bg=self.colors['dark'],
            fg=self.colors['light'],
            wrap=tk.WORD
        )
        methods_text.insert(1.0, current_defect[3])
        methods_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)

        def save_changes():
            name = name_entry.get().strip()
            causes = causes_text.get(1.0, tk.END).strip()
            methods = methods_text.get(1.0, tk.END).strip()

            if not name or not causes or not methods:
                messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
                return

            if self.db.update_defect(self.selected_defect_id, name, causes, methods):
                messagebox.showinfo("Успех", "Изменения сохранены")
                self.refresh_data()
                dialog.destroy()
            else:
                messagebox.showerror("Ошибка", "Не удалось сохранить изменения")

        # Кнопки
        buttons_frame = tk.Frame(dialog, bg=self.colors['bg'])
        buttons_frame.pack(fill=tk.X, pady=20, padx=20)

        tk.Button(
            buttons_frame,
            text="Сохранить",
            command=save_changes,
            bg=self.colors['success'],
            fg='white',
            font=('Arial', 11, 'bold'),
            relief=tk.FLAT,
            padx=20,
            pady=10,
            activebackground=self.colors['button_hover'],
            activeforeground='white'
        ).pack(side=tk.LEFT)

        tk.Button(
            buttons_frame,
            text="Отмена",
            command=dialog.destroy,
            bg=self.colors['danger'],
            fg='white',
            font=('Arial', 11),
            relief=tk.FLAT,
            padx=20,
            pady=10,
            activebackground=self.colors['button_hover'],
            activeforeground='white'
        ).pack(side=tk.RIGHT)

    def delete_selected(self):
        """Удаление выбранного дефекта"""
        if not self.selected_defect_id:
            messagebox.showwarning("Предупреждение", "Выберите дефект для удаления")
            return

        result = messagebox.askyesno(
            "Подтверждение",
            "Вы действительно хотите удалить выбранный дефект? Это действие нельзя отменить."
        )

        if result:
            if self.db.delete_defect(self.selected_defect_id):
                self.selected_defect_id = None
                self.refresh_data()
                self.clear_info()
                messagebox.showinfo("Успех", "Дефект успешно удален")
            else:
                messagebox.showerror("Ошибка", "Не удалось удалить дефект")

    def clear_info(self):
        """Очистка информационной панели"""
        self.name_label.configure(text="")

        self.causes_text.configure(state=tk.NORMAL)
        self.causes_text.delete(1.0, tk.END)
        self.causes_text.configure(state=tk.DISABLED)

        self.methods_text.configure(state=tk.NORMAL)
        self.methods_text.delete(1.0, tk.END)
        self.methods_text.configure(state=tk.DISABLED)

        self.status_label.configure(text="Готов к работе | Выберите дефект для просмотра информации")

    def show_search(self):
        """Показать окно поиска"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Поиск дефектов")
        dialog.geometry("500x150")
        dialog.configure(bg=self.colors['bg'])
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(
            dialog,
            text="Введите поисковый запрос:",
            font=('Arial', 11),
            bg=self.colors['bg'],
            fg=self.colors['light']
        ).pack(pady=20)

        search_frame = tk.Frame(dialog, bg=self.colors['bg'])
        search_frame.pack(fill=tk.X, padx=20)

        search_entry = tk.Entry(
            search_frame,
            font=('Arial', 11),
            bg=self.colors['dark'],
            fg=self.colors['light'],
            insertbackground='white'
        )
        search_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        def perform_search():
            query = search_entry.get().strip()
            if query:
                results = self.db.search_defects(query)
                if results:
                    self.load_defects(results)
                    if results:
                        self.select_defect(results[0][0], self.defect_buttons[results[0][0]])
                    self.status_label.configure(text=f"Найдено: {len(results)}")
                else:
                    messagebox.showinfo("Поиск", "Ничего не найдено")
                dialog.destroy()

        tk.Button(
            search_frame,
            text="Найти",
            command=perform_search,
            bg=self.colors['primary'],
            fg='white',
            font=('Arial', 10, 'bold'),
            relief=tk.FLAT,
            padx=15,
            pady=5,
            activebackground=self.colors['button_hover'],
            activeforeground='white'
        ).pack(side=tk.RIGHT)

    def refresh_data(self):
        """Обновление данных"""
        self.load_defects()
        if self.selected_defect_id:
            self.show_defect_info(self.selected_defect_id)
        self.status_label.configure(text="Данные обновлены | Готов к работе")

    def show_statistics(self):
        """Показать статистику"""
        defects = self.db.get_all_defects()

        dialog = tk.Toplevel(self.root)
        dialog.title("Статистика базы данных")
        dialog.geometry("400x300")
        dialog.configure(bg=self.colors['bg'])
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(
            dialog,
            text="СТАТИСТИКА",
            font=('Arial', 14, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['primary']
        ).pack(pady=20)

        stats_text = f"""
        Общее количество дефектов: {len(defects)}

        Самые распространенные методы НК:
        • Рентгенографический контроль: {sum(1 for d in defects if 'Рентгенографический' in d[3])} дефектов
        • Ультразвуковой контроль: {sum(1 for d in defects if 'Ультразвуковой' in d[3])} дефектов
        • Визуально-измерительный контроль: {sum(1 for d in defects if 'Визуально-измерительный' in d[3])} дефектов
        """

        stats_label = tk.Label(
            dialog,
            text=stats_text,
            font=('Arial', 11),
            bg=self.colors['bg'],
            fg=self.colors['light'],
            justify=tk.LEFT
        )
        stats_label.pack(pady=20)

        tk.Button(
            dialog,
            text="Закрыть",
            command=dialog.destroy,
            bg=self.colors['primary'],
            fg='white',
            font=('Arial', 10),
            relief=tk.FLAT,
            padx=20,
            pady=10,
            activebackground=self.colors['button_hover'],
            activeforeground='white'
        ).pack()

    def export_data(self):
        """Экспорт данных в текстовый файл"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )

        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("БАЗА ДАННЫХ ДЕФЕКТОВ СВАРНЫХ СОЕДИНЕНИЙ\n")
                f.write("=" * 50 + "\n\n")

                defects = self.db.get_all_defects()
                for defect in defects:
                    f.write(f"Название: {defect[1]}\n")
                    f.write("-" * 30 + "\n")
                    f.write("Причины возникновения:\n")
                    f.write(defect[2] + "\n\n")
                    f.write("Методы неразрушающего контроля:\n")
                    f.write(defect[3] + "\n")
                    f.write("=" * 50 + "\n\n")

            messagebox.showinfo("Успех", f"Данные экспортированы в файл:\n{filename}")

    def show_about(self):
        """Показать информацию о программе"""
        messagebox.showinfo(
            "О программе",
            "База данных дефектов сварных соединений\n\n"
            "Версия 2.0 (Фиолетовая тема)\n\n"
            "Программа для управления базой данных типов дефектов,\n"
            "их причинами и методами неразрушающего контроля.\n\n"
            "© 2024. Все права защищены.\n\n"
            "Для запуска не требуется установка Python или дополнительных библиотек."
        )


def main():
    """Главная функция запуска приложения"""
    root = tk.Tk()
    app = DefectManagerApp(root)

    # Центрирование окна на экране
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'1200x800+{x}+{y}')

    root.mainloop()


if __name__ == "__main__":
    main()
