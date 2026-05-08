import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime


def get_connection():
    conn = sqlite3.connect('foodexpress.db')
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS customers (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        full_name TEXT NOT NULL,
                        phone TEXT UNIQUE,
                        address TEXT NOT NULL,
                        registration_date TEXT DEFAULT CURRENT_TIMESTAMP)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        category TEXT,
                        price REAL NOT NULL,
                        description TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        customer_id INTEGER,
                        order_date TEXT DEFAULT CURRENT_TIMESTAMP,
                        status TEXT DEFAULT 'Новый',
                        total_amount REAL DEFAULT 0.0,
                        delivery_address TEXT,
                        notes TEXT,
                        FOREIGN KEY (customer_id) REFERENCES customers (id))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS order_items (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        order_id INTEGER,
                        product_id INTEGER,
                        quantity INTEGER DEFAULT 1,
                        price REAL,
                        FOREIGN KEY (order_id) REFERENCES orders (id),
                        FOREIGN KEY (product_id) REFERENCES products (id))''')

    cursor.execute("SELECT COUNT(*) as count FROM products")
    if cursor.fetchone()['count'] < 80:
        menu_items = [
            ("Маргарита", "Пицца", 890, "Томатный соус, моцарелла, базилик"),
            ("Пепперони", "Пицца", 1090, "Острая колбаса пепперони, моцарелла"),
            ("Четыре сыра", "Пицца", 990, "Моцарелла, чеддер, дор-блю, пармезан"),
            ("Гавайская", "Пицца", 950, "Курица, ананас, моцарелла"),
            ("Мясная", "Пицца", 1190, "Говядина, ветчина, бекон, пепперони"),
            ("BBQ Чикен", "Пицца", 1150, "Курица, соус BBQ, красный лук"),
            ("Диабло", "Пицца", 1120, "Острая колбаса, халапеньо, острый соус"),
            ("Морская", "Пицца", 1250, "Креветки, тунец, мидии, кальмары"),
            ("Вегетарианская", "Пицца", 890, "Баклажаны, перец, томаты, шампиньоны"),
            ("Карбонара", "Пицца", 1050, "Бекон, пармезан, яйцо, сливочный соус"),
            ("Калифорния", "Роллы", 690, "Краб, авокадо, огурец, соус спайси"),
            ("Филадельфия", "Роллы", 790, "Лосось, сливочный сыр, авокадо"),
            ("Запечённый", "Роллы", 750, "Лосось, сыр, соус унаги, запечённый"),
            ("Дракон", "Роллы", 890, "Угорь, авокадо, соус унаги, кунжут"),
            ("Спайси тунец", "Роллы", 720, "Тунец, острый соус, огурец"),
            ("Филадельфия с угрём", "Роллы", 850, "Угорь, сливочный сыр, авокадо"),
            ("Цезарь ролл", "Роллы", 680, "Курица, салат, пармезан, соус цезарь"),
            ("Темпура", "Роллы", 780, "Креветка в темпуре, авокадо, огурец"),
            ("Окинава", "Роллы", 820, "Угорь, креветка, авокадо, огурец"),
            ("Самурай", "Роллы", 740, "Лосось, тунец, огурец, соус унаги"),
            ("Лосось", "Суши", 180, "Свежий лосось на рисе с васаби"),
            ("Тунец", "Суши", 190, "Тунец на рисе с васаби"),
            ("Угорь", "Суши", 200, "Копчёный угорь с соусом унаги"),
            ("Креветка", "Суши", 170, "Креветка на рисе с соусом"),
            ("Окунь", "Суши", 160, "Свежий окунь с лимоном"),
            ("Икура", "Суши", 250, "Икра лосося на рисе"),
            ("Классический", "Бургеры", 590, "Говяжья котлета, чеддер, овощи, соус гриль"),
            ("Чизбургер", "Бургеры", 620, "Двойной сыр, говяжья котлета, маринованные огурцы"),
            ("Куриный", "Бургеры", 550, "Куриная котлета, сыр, соус барбекю"),
            ("Двойной", "Бургеры", 890, "Две котлеты, двойной сыр, бекон"),
            ("Острый", "Бургеры", 650, "Острая котлета, халапеньо, острый соус"),
            ("BBQ бургер", "Бургеры", 680, "Бекон, карамелизированный лук, соус BBQ"),
            ("С грибами", "Бургеры", 610, "Шампиньоны, сыр гауда, луковые кольца"),
            ("Овощной", "Бургеры", 490, "Вегетарианский, овощная котлета, авокадо"),
            ("Цезарь с курицей", "Салаты", 490, "Курица, пармезан, сухарики, соус цезарь"),
            ("Греческий", "Салаты", 450, "Фета, оливки, томаты, огурцы, перец"),
            ("С тунцом", "Салаты", 520, "Тунец, авокадо, свежие овощи, оливковое масло"),
            ("Нисуаз", "Салаты", 560, "Тунец, яйцо, фасоль, томаты, анчоусы"),
            ("Оливье с курицей", "Салаты", 380, "Курица, горошек, яйца, огурцы, майонез"),
            ("Крабовый", "Салаты", 420, "Крабовые палочки, кукуруза, огурец, рис, майонез"),
            ("Картофель фри", "Закуски", 290, "Хрустящий картофель фри, порция"),
            ("Наггетсы", "Закуски", 390, "10 штук куриных наггетсов с соусом"),
            ("Крылышки BBQ", "Закуски", 650, "8 острых куриных крылышек с соусом BBQ"),
            ("Сырные палочки", "Закуски", 420, "8 штук палочек моцареллы с томатным соусом"),
            ("Луковые кольца", "Закуски", 320, "Хрустящие луковые кольца, порция 200 грамм"),
            ("Картофель по-деревенски", "Закуски", 310, "Картофель с пряностями и чесноком"),
            ("Креветки в кляре", "Закуски", 590, "8 штук креветок в хрустящем кляре"),
            ("Овощной микс", "Закуски", 350, "Свежие овощи с соусом ранч"),
            ("Томатный суп", "Первые блюда", 320, "Суп с томатами, базиликом и пармезаном"),
            ("Грибной суп", "Первые блюда", 340, "Суп из шампиньонов со сливками"),
            ("Солянка мясная", "Первые блюда", 390, "Сборная мясная солянка с лимоном"),
            ("Лапша куриная", "Первые блюда", 330, "Лапша с курицей и овощами"),
            ("Сырный суп", "Первые блюда", 350, "Сливочный суп с сыром и сухариками"),
            ("Мисо суп", "Первые блюда", 280, "Японский суп с тофу и водорослями"),
            ("Чизкейк Нью-Йорк", "Десерты", 380, "Классический нью-йоркский чизкейк"),
            ("Тирамису", "Десерты", 390, "Итальянский десерт с кофе и маскарпоне"),
            ("Брауни", "Десерты", 320, "Шоколадное пирожное с орехами"),
            ("Панна котта", "Десерты", 340, "Сливочный десерт с ягодным соусом"),
            ("Макарун", "Десерты", 180, "Французское миндальное печенье 1 штука"),
            ("Мороженое", "Десерты", 150, "Ванильное, шоколадное или клубничное 1 шарик"),
            ("Пирожное картошка", "Десерты", 120, "Классическое пирожное из печенья"),
            ("Пицца-роллы", "Выпечка", 290, "4 штуки роллов с начинкой из пиццы"),
            ("Сырные булочки", "Выпечка", 250, "Свежие булочки с моцареллой, 4 штуки"),
            ("Хлеб с чесноком", "Выпечка", 190, "Багет с чесночным маслом"),
            ("Лаваш", "Выпечка", 150, "Тонкий армянский лаваш"),
            ("Кола", "Напитки", 150, "Coca-Cola 0.5 литра"),
            ("Кола Zero", "Напитки", 150, "Coca-Cola Zero 0.5 литра"),
            ("Спрайт", "Напитки", 150, "Sprite 0.5 литра"),
            ("Фанта", "Напитки", 150, "Fanta 0.5 литра"),
            ("Морс клюквенный", "Напитки", 170, "Домашний клюквенный морс 0.3 литра"),
            ("Чай чёрный", "Напитки", 120, "Чёрный чай (горячий или холодный)"),
            ("Чай зелёный", "Напитки", 120, "Зелёный чай (горячий или холодный)"),
            ("Сок апельсиновый", "Соки", 180, "Натуральный апельсиновый сок 0.3 литра"),
            ("Сок яблочный", "Соки", 170, "Натуральный яблочный сок 0.3 литра"),
            ("Сок вишнёвый", "Соки", 180, "Натуральный вишнёвый сок 0.3 литра"),
            ("Лимонад", "Напитки", 210, "Домашний лимонад 0.5 литра"),
            ("Молочный коктейль", "Напитки", 250, "Шоколадный или клубничный 0.4 литра"),
            ("Кофе американо", "Кофе", 180, "Классический американо 0.3 литра"),
            ("Кофе латте", "Кофе", 220, "Латте с нежной пенкой 0.3 литра"),
            ("Капучино", "Кофе", 210, "Капучино с корицей 0.3 литра"),
            ("Глинтвейн", "Горячие напитки", 290, "Безалкогольный глинтвейн 0.3 литра"),
            ("Томатный соус", "Соусы", 50, "Классический томатный соус"),
            ("Сырный соус", "Соусы", 60, "Нежный сырный соус"),
            ("Чесночный соус", "Соусы", 50, "Ароматный чесночный соус"),
            ("Барбекю", "Соусы", 60, "Соус барбекю"),
            ("Острый соус", "Соусы", 50, "Острый перечный соус"),
        ]
        cursor.executemany("INSERT INTO products (name, category, price, description) VALUES (?,?,?,?)", menu_items)

    conn.commit()
    conn.close()


class FoodExpressApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FoodExpress — Доставка вкусной еды")
        self.root.geometry("1400x800")
        self.root.configure(bg='#f8f9fa')

        init_db()
        self.setup_styles()

        self.main_container = ttk.Frame(root, style='Main.TFrame')
        self.main_container.pack(fill='both', expand=True)

        self.create_header()
        self.create_main_content()

        self.cart = []

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        style.configure('Main.TFrame', background='#f8f9fa')
        style.configure('Header.TFrame', background='#2c3e50')
        style.configure('Card.TFrame', background='#ffffff', relief='raised', borderwidth=1)

        style.configure('Header.TLabel', background='#2c3e50', foreground='#ecf0f1',
                        font=('Segoe UI', 24, 'bold'))
        style.configure('Subtitle.TLabel', background='#f8f9fa', foreground='#7f8c8d',
                        font=('Segoe UI', 12))
        style.configure('Title.TLabel', background='#ffffff', foreground='#2c3e50',
                        font=('Segoe UI', 14, 'bold'))

        style.configure('Primary.TButton', background='#e74c3c', foreground='#ffffff',
                        font=('Segoe UI', 11, 'bold'), padding=10)
        style.map('Primary.TButton',
                  background=[('active', '#c0392b'), ('pressed', '#a93226')])

        style.configure('Secondary.TButton', background='#3498db', foreground='#ffffff',
                        font=('Segoe UI', 10), padding=10)
        style.map('Secondary.TButton',
                  background=[('active', '#2980b9')])

        style.configure('Treeview', background='#ffffff', foreground='#2c3e50',
                        font=('Segoe UI', 10), rowheight=30)
        style.configure('Treeview.Heading', background='#ecf0f1', foreground='#2c3e50',
                        font=('Segoe UI', 11, 'bold'))

        style.configure('TEntry', fieldbackground='#ffffff', foreground='#2c3e50',
                        font=('Segoe UI', 11), padding=8)

        style.configure('TNotebook', background='#f8f9fa', tabmargins=[2, 5, 2, 0])
        style.configure('TNotebook.Tab', background='#ecf0f1', foreground='#7f8c8d',
                        font=('Segoe UI', 11, 'bold'), padding=[15, 5])
        style.map('TNotebook.Tab',
                  background=[('selected', '#e74c3c')],
                  foreground=[('selected', '#ffffff')])

    def create_header(self):
        header = ttk.Frame(self.main_container, style='Header.TFrame', height=100)
        header.pack(fill='x', padx=0, pady=0)
        header.pack_propagate(False)

        left_frame = ttk.Frame(header, style='Header.TFrame')
        left_frame.pack(side='left', padx=30, pady=20)

        ttk.Label(left_frame, text="FoodExpress", style='Header.TLabel').pack(side='left')
        ttk.Label(left_frame, text="Доставка вкусной еды", style='Subtitle.TLabel',
                  background='#2c3e50', foreground='#bdc3c7').pack(side='left', padx=(15, 0))

        right_frame = ttk.Frame(header, style='Header.TFrame')
        right_frame.pack(side='right', padx=30, pady=20)

        info_text = "Работаем: 10:00 - 23:00\nГорячая линия: 8-800-123-45-67"
        ttk.Label(right_frame, text=info_text, style='Subtitle.TLabel',
                  background='#2c3e50', foreground='#bdc3c7', justify='right').pack()

    def create_main_content(self):
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=20)

        self.create_menu_tab()
        self.create_new_order_tab()
        self.create_all_orders_tab()
        self.create_statistics_tab()

    def create_menu_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Наше меню")

        categories_frame = ttk.LabelFrame(tab, text="Категории", padding=15)
        categories_frame.pack(side='left', fill='y', padx=10, pady=10)

        self.category_listbox = tk.Listbox(categories_frame, font=('Segoe UI', 12),
                                           bg='#ffffff', fg='#2c3e50',
                                           selectbackground='#e74c3c',
                                           selectforeground='#ffffff',
                                           height=22, width=20, relief='flat')
        self.category_listbox.pack(fill='both', expand=True)

        products_frame = ttk.LabelFrame(tab, text="Блюда", padding=15)
        products_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)

        search_frame = ttk.Frame(products_frame)
        search_frame.pack(fill='x', pady=(0, 10))

        ttk.Label(search_frame, text="Поиск:").pack(side='left', padx=5)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side='left', padx=5)
        ttk.Button(search_frame, text="Найти", command=self.search_products,
                   style='Secondary.TButton').pack(side='left', padx=5)

        tree_frame = ttk.Frame(products_frame)
        tree_frame.pack(fill='both', expand=True)

        scroll_y = ttk.Scrollbar(tree_frame, orient='vertical')
        scroll_x = ttk.Scrollbar(tree_frame, orient='horizontal')

        self.menu_tree = ttk.Treeview(tree_frame, columns=('name', 'price', 'description'),
                                      show='headings', height=18,
                                      yscrollcommand=scroll_y.set,
                                      xscrollcommand=scroll_x.set)

        scroll_y.config(command=self.menu_tree.yview)
        scroll_x.config(command=self.menu_tree.xview)

        self.menu_tree.heading('name', text='Название блюда')
        self.menu_tree.heading('price', text='Цена')
        self.menu_tree.heading('description', text='Описание')

        self.menu_tree.column('name', width=300)
        self.menu_tree.column('price', width=100, anchor='center')
        self.menu_tree.column('description', width=500)

        self.menu_tree.pack(side='left', fill='both', expand=True)
        scroll_y.pack(side='right', fill='y')
        scroll_x.pack(side='bottom', fill='x')

        btn_frame = ttk.Frame(products_frame)
        btn_frame.pack(fill='x', pady=(10, 0))

        qty_frame = ttk.Frame(btn_frame)
        qty_frame.pack(side='right', padx=5)

        ttk.Label(qty_frame, text="Количество:").pack(side='left', padx=5)
        self.spin_qty = tk.Spinbox(qty_frame, from_=1, to=99, width=5, font=('Segoe UI', 10))
        self.spin_qty.pack(side='left', padx=5)

        ttk.Button(btn_frame, text="Добавить в корзину",
                   command=self.add_to_cart_from_menu,
                   style='Primary.TButton').pack(side='right', padx=5)

        self.load_categories()
        self.category_listbox.bind('<<ListboxSelect>>', self.on_category_select)
        self.load_all_products()

    def search_products(self):
        search_text = self.search_entry.get().strip().lower()
        if not search_text:
            self.load_all_products()
            return

        for item in self.menu_tree.get_children():
            self.menu_tree.delete(item)

        conn = get_connection()
        products = conn.execute("SELECT * FROM products WHERE LOWER(name) LIKE ? OR LOWER(description) LIKE ?",
                                (f'%{search_text}%', f'%{search_text}%')).fetchall()

        for product in products:
            self.menu_tree.insert('', 'end', values=(
                product['name'],
                f"{product['price']} ₽",
                product['description']
            ), tags=(product['id'],))
        conn.close()

        if len(products) == 0:
            messagebox.showinfo("Результат поиска", "Ничего не найдено")

    def load_categories(self):
        categories = [
            "Все блюда", "Пицца", "Роллы", "Суши", "Бургеры",
            "Салаты", "Закуски", "Первые блюда", "Десерты",
            "Выпечка", "Напитки", "Соки", "Кофе", "Соусы"
        ]
        for cat in categories:
            self.category_listbox.insert(tk.END, cat)

    def on_category_select(self, event):
        selection = self.category_listbox.curselection()
        if selection:
            category = self.category_listbox.get(selection[0])
            if category == "Все блюда":
                self.load_all_products()
            else:
                self.load_products_by_category(category)

    def load_all_products(self):
        for item in self.menu_tree.get_children():
            self.menu_tree.delete(item)

        conn = get_connection()
        products = conn.execute("SELECT * FROM products ORDER BY category, name").fetchall()

        for product in products:
            self.menu_tree.insert('', 'end', values=(
                product['name'],
                f"{product['price']} ₽",
                product['description']
            ), tags=(product['id'],))
        conn.close()

    def load_products_by_category(self, category):
        for item in self.menu_tree.get_children():
            self.menu_tree.delete(item)

        conn = get_connection()
        products = conn.execute("SELECT * FROM products WHERE category = ? ORDER BY name",
                                (category,)).fetchall()

        for product in products:
            self.menu_tree.insert('', 'end', values=(
                product['name'],
                f"{product['price']} ₽",
                product['description']
            ), tags=(product['id'],))
        conn.close()

    def add_to_cart_from_menu(self):
        selection = self.menu_tree.selection()
        if not selection:
            messagebox.showwarning("Внимание", "Пожалуйста, выберите блюдо из меню")
            return

        try:
            quantity = int(self.spin_qty.get())
            if quantity < 1:
                quantity = 1
        except:
            quantity = 1

        item = self.menu_tree.item(selection[0])
        product_id = item['tags'][0]

        conn = get_connection()
        product = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
        conn.close()

        found = False
        for cart_item in self.cart:
            if cart_item[0] == product_id:
                cart_item[3] += quantity
                self.refresh_cart()
                messagebox.showinfo("Успех", f"Количество '{product['name']}' увеличено на {quantity}")
                found = True
                break

        if not found:
            self.cart.append([product_id, product['name'], product['price'], quantity])
            self.refresh_cart()
            messagebox.showinfo("Успех", f"'{product['name']}' добавлен в корзину в количестве {quantity} шт.")

    def create_new_order_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Оформление заказа")

        left_frame = ttk.LabelFrame(tab, text="Информация о клиенте", padding=20)
        left_frame.pack(side='left', fill='both', padx=10, pady=10, expand=True)

        info_label = ttk.Label(left_frame, text="Поля, отмеченные *, обязательны для заполнения",
                               font=('Segoe UI', 10), foreground='#e74c3c')
        info_label.grid(row=0, column=0, columnspan=2, sticky='w', pady=(0, 15))

        fields = [
            ("ФИО *", "entry_name", "Введите ваши фамилию, имя и отчество", 1),
            ("Телефон *", "entry_phone", "Например: +7 (999) 123-45-67", 2),
            ("Адрес доставки *", "entry_address", "Улица, дом, квартира, подъезд", 3),
            ("Примечание к заказу", "entry_notes", "Особые пожелания (опционально)", 4)
        ]

        self.order_entries = {}
        for label, key, placeholder, row in fields:
            ttk.Label(left_frame, text=label, font=('Segoe UI', 12, 'bold'),
                      foreground='#2c3e50').grid(row=row, column=0, sticky='w', pady=(0, 5))

            entry = ttk.Entry(left_frame, width=50, font=('Segoe UI', 11))
            entry.grid(row=row, column=0, columnspan=2, sticky='ew', pady=(0, 5))

            entry.insert(0, placeholder)
            entry.configure(foreground='#95a5a6')

            def on_focus(e, e_entry=entry, e_placeholder=placeholder):
                if e_entry.get() == e_placeholder:
                    e_entry.delete(0, tk.END)
                    e_entry.configure(foreground='#2c3e50')

            def on_blur(e, e_entry=entry, e_placeholder=placeholder):
                if e_entry.get() == "":
                    e_entry.insert(0, e_placeholder)
                    e_entry.configure(foreground='#95a5a6')

            entry.bind('<FocusIn>', on_focus)
            entry.bind('<FocusOut>', on_blur)

            self.order_entries[key] = entry

        example_frame = ttk.LabelFrame(left_frame, text="Пример заполнения", padding=10)
        example_frame.grid(row=5, column=0, columnspan=2, sticky='ew', pady=(20, 0))

        example_text = """ФИО: Иванов Иван Иванович
Телефон: +7 912 345-67-89
Адрес: ул. Ленина, д. 10, кв. 25
Примечание: Без лука, позвоньте за 5 минут"""

        ttk.Label(example_frame, text=example_text, font=('Segoe UI', 10),
                  foreground='#7f8c8d', justify='left').pack(anchor='w')

        right_frame = ttk.LabelFrame(tab, text="Корзина", padding=20)
        right_frame.pack(side='right', fill='both', padx=10, pady=10, expand=True)

        ttk.Label(right_frame, text="Добавляйте блюда из вкладки 'Меню'",
                  font=('Segoe UI', 10), foreground='#3498db').pack(anchor='w', pady=(0, 10))

        cart_scroll = ttk.Scrollbar(right_frame, orient='vertical')
        self.cart_tree = ttk.Treeview(right_frame, columns=('name', 'qty', 'price'),
                                      show='headings', height=15,
                                      yscrollcommand=cart_scroll.set)
        cart_scroll.config(command=self.cart_tree.yview)

        self.cart_tree.heading('name', text='Блюдо')
        self.cart_tree.heading('qty', text='Кол-во')
        self.cart_tree.heading('price', text='Сумма')

        self.cart_tree.column('name', width=300)
        self.cart_tree.column('qty', width=100, anchor='center')
        self.cart_tree.column('price', width=120, anchor='center')

        self.cart_tree.pack(fill='both', expand=True)
        cart_scroll.pack(side='right', fill='y')

        cart_buttons = ttk.Frame(right_frame)
        cart_buttons.pack(fill='x', pady=(10, 0))

        ttk.Button(cart_buttons, text="Удалить выбранное",
                   command=self.remove_from_cart, style='Secondary.TButton').pack(side='left', padx=5)

        ttk.Button(cart_buttons, text="Очистить корзину",
                   command=self.clear_cart, style='Secondary.TButton').pack(side='left', padx=5)

        self.total_label = ttk.Label(right_frame, text="Итого: 0 ₽",
                                     font=('Segoe UI', 16, 'bold'), foreground='#e74c3c')
        self.total_label.pack(pady=(10, 0))

        ttk.Button(right_frame, text="Оформить заказ",
                   command=self.create_order, style='Primary.TButton').pack(pady=(15, 0), fill='x', ipady=5)

    def clear_cart(self):
        if self.cart:
            if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить корзину?"):
                self.cart.clear()
                self.refresh_cart()
                messagebox.showinfo("Успех", "Корзина очищена")

    def refresh_cart(self):
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)

        total = 0
        for product_id, name, price, qty in self.cart:
            amount = price * qty
            total += amount
            self.cart_tree.insert('', 'end', values=(name, f"{qty} шт.", f"{amount} ₽"))

        self.total_label.config(text=f"Итого: {total} ₽")

    def remove_from_cart(self):
        selection = self.cart_tree.selection()
        if not selection:
            messagebox.showwarning("Внимание", "Выберите блюдо для удаления")
            return

        idx = self.cart_tree.index(selection[0])
        self.cart.pop(idx)
        self.refresh_cart()
        messagebox.showinfo("Успех", "Блюдо удалено из корзины")

    def create_order(self):
        if not self.cart:
            messagebox.showerror("Ошибка", "Корзина пуста! Добавьте блюда в корзину из вкладки 'Меню'")
            return

        name_entry = self.order_entries['entry_name']
        phone_entry = self.order_entries['entry_phone']
        address_entry = self.order_entries['entry_address']
        notes_entry = self.order_entries['entry_notes']

        name = name_entry.get().strip()
        phone = phone_entry.get().strip()
        address = address_entry.get().strip()
        notes = notes_entry.get().strip()

        if name == "Введите ваши фамилию, имя и отчество":
            name = ""
        if phone == "Например: +7 (999) 123-45-67":
            phone = ""
        if address == "Улица, дом, квартира, подъезд":
            address = ""
        if notes == "Особые пожелания (опционально)":
            notes = ""

        if not all([name, phone, address]):
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все обязательные поля!\n"
                                           "Обязательные поля: ФИО, Телефон, Адрес доставки")
            return

        conn = get_connection()
        cursor = conn.cursor()

        try:
            try:
                cursor.execute("INSERT INTO customers (full_name, phone, address) VALUES (?,?,?)",
                               (name, phone, address))
                customer_id = cursor.lastrowid
            except sqlite3.IntegrityError:
                cursor.execute("SELECT id FROM customers WHERE phone=?", (phone,))
                customer_id = cursor.fetchone()['id']

            cursor.execute("INSERT INTO orders (customer_id, delivery_address, notes, status) VALUES (?,?,?,?)",
                           (customer_id, address, notes, "Новый"))
            order_id = cursor.lastrowid

            total = 0
            for prod_id, _, price, qty in self.cart:
                cursor.execute("INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?,?,?,?)",
                               (order_id, prod_id, qty, price))
                total += price * qty

            cursor.execute("UPDATE orders SET total_amount = ? WHERE id = ?", (total, order_id))
            conn.commit()

            order_details = f"ЗАКАЗ №{order_id} УСПЕШНО ОФОРМЛЕН!\n\n"
            order_details += f"Информация о заказе:\n"
            order_details += f"----------------------------------------\n"
            order_details += f"Клиент: {name}\n"
            order_details += f"Телефон: {phone}\n"
            order_details += f"Адрес: {address}\n"
            if notes:
                order_details += f"Примечание: {notes}\n"
            order_details += f"Сумма: {total} ₽\n"
            order_details += f"----------------------------------------\n\n"
            order_details += f"Статус: Новый заказ\n"
            order_details += f"Ожидайте звонка курьера в ближайшее время!\n\n"
            order_details += f"Спасибо, что выбрали FoodExpress!"

            messagebox.showinfo("Заказ оформлен!", order_details)

            self.cart.clear()
            self.refresh_cart()

            for key, entry in self.order_entries.items():
                entry.delete(0, tk.END)
                if key == 'entry_name':
                    entry.insert(0, "Введите ваши фамилию, имя и отчество")
                elif key == 'entry_phone':
                    entry.insert(0, "Например: +7 (999) 123-45-67")
                elif key == 'entry_address':
                    entry.insert(0, "Улица, дом, квартира, подъезд")
                elif key == 'entry_notes':
                    entry.insert(0, "Особые пожелания (опционально)")
                entry.configure(foreground='#95a5a6')

        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при оформлении заказа:\n{str(e)}")
        finally:
            conn.close()

    def create_all_orders_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="История заказов")

        main_frame = ttk.Frame(tab, padding=20)
        main_frame.pack(fill='both', expand=True)

        ttk.Label(main_frame, text="История заказов", font=('Segoe UI', 18, 'bold'),
                  foreground='#2c3e50').pack(anchor='w', pady=(0, 20))

        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill='x', pady=(0, 10))

        buttons_frame = ttk.Frame(control_frame)
        buttons_frame.pack()

        btn_refresh = ttk.Button(buttons_frame, text="Обновить список заказов",
                                 command=self.load_orders, style='Secondary.TButton', width=25)
        btn_refresh.pack(side='left', padx=5)

        btn_change = ttk.Button(buttons_frame, text="Изменить статус заказа",
                                command=self.change_order_status, style='Primary.TButton', width=25)
        btn_change.pack(side='left', padx=5)

        table_frame = ttk.LabelFrame(main_frame, text="Список заказов", padding=10)
        table_frame.pack(fill='both', expand=True)

        container = ttk.Frame(table_frame)
        container.pack(fill='both', expand=True)

        scroll_y = ttk.Scrollbar(container, orient='vertical')
        scroll_x = ttk.Scrollbar(container, orient='horizontal')

        self.orders_tree = ttk.Treeview(container, columns=('id', 'date', 'customer', 'address', 'total', 'status'),
                                        show='headings',
                                        yscrollcommand=scroll_y.set,
                                        xscrollcommand=scroll_x.set)

        scroll_y.config(command=self.orders_tree.yview)
        scroll_x.config(command=self.orders_tree.xview)

        self.orders_tree.heading('id', text='Номер заказа')
        self.orders_tree.heading('date', text='Дата')
        self.orders_tree.heading('customer', text='Клиент')
        self.orders_tree.heading('address', text='Адрес доставки')
        self.orders_tree.heading('total', text='Сумма')
        self.orders_tree.heading('status', text='Статус')

        self.orders_tree.column('id', width=100, anchor='center')
        self.orders_tree.column('date', width=150, anchor='center')
        self.orders_tree.column('customer', width=200)
        self.orders_tree.column('address', width=400)
        self.orders_tree.column('total', width=120, anchor='center')
        self.orders_tree.column('status', width=120, anchor='center')

        self.orders_tree.pack(side='left', fill='both', expand=True)
        scroll_y.pack(side='right', fill='y')
        scroll_x.pack(side='bottom', fill='x')

        self.load_orders()

    def load_orders(self):
        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)

        conn = get_connection()
        query = """
        SELECT o.id, o.order_date, c.full_name, o.delivery_address, 
               o.total_amount, o.status
        FROM orders o
        JOIN customers c ON o.customer_id = c.id
        ORDER BY o.id DESC
        """

        orders = conn.execute(query).fetchall()

        for order in orders:
            self.orders_tree.insert('', 'end', values=(
                order['id'],
                order['order_date'][:16],
                order['full_name'],
                order['delivery_address'],
                f"{order['total_amount']} ₽",
                order['status']
            ))
        conn.close()

    def change_order_status(self):
        selection = self.orders_tree.selection()
        if not selection:
            messagebox.showwarning("Внимание", "Пожалуйста, выберите заказ для изменения статуса")
            return

        item = self.orders_tree.item(selection[0])
        order_id = item['values'][0]
        current_status = item['values'][5]

        status_window = tk.Toplevel(self.root)
        status_window.title("Изменение статуса заказа")
        status_window.geometry("400x350")
        status_window.configure(bg='#f8f9fa')

        status_window.transient(self.root)
        status_window.grab_set()

        main_frame = ttk.Frame(status_window, padding=20)
        main_frame.pack(fill='both', expand=True)

        ttk.Label(main_frame, text=f"Заказ №{order_id}",
                  font=('Segoe UI', 14, 'bold')).pack(pady=(0, 10))

        ttk.Label(main_frame, text=f"Текущий статус: {current_status}",
                  font=('Segoe UI', 11)).pack(pady=(0, 20))

        ttk.Label(main_frame, text="Выберите новый статус:",
                  font=('Segoe UI', 11)).pack(anchor='w', pady=(0, 5))

        statuses = ["Новый", "Готовится", "В пути", "Доставлен"]
        selected_status = tk.StringVar(value=current_status)

        for status in statuses:
            ttk.Radiobutton(main_frame, text=status, variable=selected_status,
                            value=status).pack(anchor='w', pady=5)

        def update_status():
            new_status = selected_status.get()
            if new_status == current_status:
                messagebox.showinfo("Информация", "Статус не изменен")
                status_window.destroy()
                return

            conn = get_connection()
            cursor = conn.cursor()
            try:
                cursor.execute("UPDATE orders SET status = ? WHERE id = ?", (new_status, order_id))
                conn.commit()
                messagebox.showinfo("Успех", f"Статус заказа №{order_id} изменен на '{new_status}'")
                self.load_orders()
                status_window.destroy()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось изменить статус:\n{str(e)}")
            finally:
                conn.close()

        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill='x', pady=(20, 0))

        ttk.Button(btn_frame, text="Сохранить", command=update_status,
                   style='Primary.TButton').pack(side='left', padx=5, expand=True, fill='x')

        ttk.Button(btn_frame, text="Отмена", command=status_window.destroy,
                   style='Secondary.TButton').pack(side='left', padx=5, expand=True, fill='x')

    def create_statistics_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Статистика")

        main_frame = ttk.Frame(tab, padding=20)
        main_frame.pack(fill='both', expand=True)

        canvas = tk.Canvas(main_frame, bg='#f8f9fa', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=canvas.winfo_width())

        def configure_canvas(event):
            canvas.itemconfig(1, width=event.width)

        canvas.bind("<Configure>", configure_canvas)

        conn = get_connection()

        total_orders = conn.execute("SELECT COUNT(*) as count FROM orders").fetchone()['count']
        total_revenue = conn.execute("SELECT SUM(total_amount) as total FROM orders").fetchone()['total'] or 0
        avg_check = total_revenue / total_orders if total_orders > 0 else 0

        today = datetime.now().strftime('%Y-%m-%d')
        today_orders = conn.execute(
            "SELECT COUNT(*) as count, SUM(total_amount) as total FROM orders WHERE DATE(order_date) = ?",
            (today,)).fetchone()
        today_count = today_orders['count'] or 0
        today_revenue = today_orders['total'] or 0

        ttk.Label(scrollable_frame, text="Статистика доставки",
                  font=('Segoe UI', 20), foreground='#2c3e50').pack(anchor='center', pady=(0, 20))

        stats_frame = ttk.Frame(scrollable_frame)
        stats_frame.pack(fill='x', pady=10)

        for i in range(4):
            stats_frame.columnconfigure(i, weight=1)

        card1 = ttk.Frame(stats_frame, style='Card.TFrame', padding=15)
        card1.grid(row=0, column=0, padx=5, sticky='nsew')
        ttk.Label(card1, text="Всего заказов", font=('Segoe UI', 12), foreground='#7f8c8d').pack()
        ttk.Label(card1, text=str(total_orders), font=('Segoe UI', 32), foreground='#e74c3c').pack()

        card2 = ttk.Frame(stats_frame, style='Card.TFrame', padding=15)
        card2.grid(row=0, column=1, padx=5, sticky='nsew')
        ttk.Label(card2, text="Общая выручка", font=('Segoe UI', 12), foreground='#7f8c8d').pack()
        ttk.Label(card2, text=f"{total_revenue:,.0f} ₽", font=('Segoe UI', 32), foreground='#27ae60').pack()

        card3 = ttk.Frame(stats_frame, style='Card.TFrame', padding=15)
        card3.grid(row=0, column=2, padx=5, sticky='nsew')
        ttk.Label(card3, text="Средний чек", font=('Segoe UI', 12), foreground='#7f8c8d').pack()
        ttk.Label(card3, text=f"{avg_check:,.0f} ₽", font=('Segoe UI', 32), foreground='#3498db').pack()

        card4 = ttk.Frame(stats_frame, style='Card.TFrame', padding=15)
        card4.grid(row=0, column=3, padx=5, sticky='nsew')
        ttk.Label(card4, text=f"Заказов сегодня", font=('Segoe UI', 12), foreground='#7f8c8d').pack()
        ttk.Label(card4, text=f"{today_count} / {today_revenue:,.0f} ₽", font=('Segoe UI', 24),
                  foreground='#f39c12').pack()

        new_orders = conn.execute("SELECT COUNT(*) as count FROM orders WHERE status = 'Новый'").fetchone()['count']
        cooking_orders = conn.execute("SELECT COUNT(*) as count FROM orders WHERE status = 'Готовится'").fetchone()[
            'count']
        delivering_orders = conn.execute("SELECT COUNT(*) as count FROM orders WHERE status = 'В пути'").fetchone()[
            'count']
        delivered_orders = conn.execute("SELECT COUNT(*) as count FROM orders WHERE status = 'Доставлен'").fetchone()[
            'count']

        status_frame = ttk.LabelFrame(scrollable_frame, text="Статусы заказов", padding=15)
        status_frame.pack(fill='x', pady=10)

        status_stats = ttk.Frame(status_frame)
        status_stats.pack(fill='x')

        for i in range(4):
            status_stats.columnconfigure(i, weight=1)

        status1 = ttk.Frame(status_stats, style='Card.TFrame', padding=10)
        status1.grid(row=0, column=0, padx=5, sticky='nsew')
        ttk.Label(status1, text="Новые", font=('Segoe UI', 11), foreground='#7f8c8d').pack()
        ttk.Label(status1, text=str(new_orders), font=('Segoe UI', 20), foreground='#2c3e50').pack()

        status2 = ttk.Frame(status_stats, style='Card.TFrame', padding=10)
        status2.grid(row=0, column=1, padx=5, sticky='nsew')
        ttk.Label(status2, text="Готовятся", font=('Segoe UI', 11), foreground='#7f8c8d').pack()
        ttk.Label(status2, text=str(cooking_orders), font=('Segoe UI', 20), foreground='#2c3e50').pack()

        status3 = ttk.Frame(status_stats, style='Card.TFrame', padding=10)
        status3.grid(row=0, column=2, padx=5, sticky='nsew')
        ttk.Label(status3, text="В пути", font=('Segoe UI', 11), foreground='#7f8c8d').pack()
        ttk.Label(status3, text=str(delivering_orders), font=('Segoe UI', 20), foreground='#2c3e50').pack()

        status4 = ttk.Frame(status_stats, style='Card.TFrame', padding=10)
        status4.grid(row=0, column=3, padx=5, sticky='nsew')
        ttk.Label(status4, text="Доставлены", font=('Segoe UI', 11), foreground='#7f8c8d').pack()
        ttk.Label(status4, text=str(delivered_orders), font=('Segoe UI', 20), foreground='#2c3e50').pack()

        popular_frame = ttk.LabelFrame(scrollable_frame, text="Популярные блюда", padding=15)
        popular_frame.pack(fill='x', pady=10)

        popular = conn.execute("""
        SELECT p.name, p.category, SUM(oi.quantity) as total_qty, SUM(oi.quantity * oi.price) as total_revenue
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        GROUP BY p.id
        ORDER BY total_qty DESC
        LIMIT 10
        """).fetchall()

        if len(popular) > 0:
            popular_tree = ttk.Treeview(popular_frame, columns=('rank', 'name', 'category', 'qty', 'revenue'),
                                        show='headings', height=10)
            popular_tree.heading('rank', text='Место')
            popular_tree.heading('name', text='Блюдо')
            popular_tree.heading('category', text='Категория')
            popular_tree.heading('qty', text='Продано, шт')
            popular_tree.heading('revenue', text='Выручка, ₽')

            popular_tree.column('rank', width=80, anchor='center')
            popular_tree.column('name', width=250)
            popular_tree.column('category', width=150)
            popular_tree.column('qty', width=120, anchor='center')
            popular_tree.column('revenue', width=150, anchor='center')

            for i, item in enumerate(popular, 1):
                popular_tree.insert('', 'end', values=(i, item['name'], item['category'],
                                                       item['total_qty'], f"{item['total_revenue']:,.0f}"))

            popular_tree.pack(fill='x', expand=True)
        else:
            ttk.Label(popular_frame, text="Пока нет заказов", font=('Segoe UI', 12),
                      foreground='#95a5a6').pack(anchor='w', pady=20)

        category_frame = ttk.LabelFrame(scrollable_frame, text="Продажи по категориям", padding=15)
        category_frame.pack(fill='x', pady=10)

        categories_stats = conn.execute("""
        SELECT p.category, SUM(oi.quantity) as total_qty, SUM(oi.quantity * oi.price) as total_revenue
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        GROUP BY p.category
        ORDER BY total_revenue DESC
        """).fetchall()

        if len(categories_stats) > 0:
            category_tree = ttk.Treeview(category_frame, columns=('category', 'qty', 'revenue', 'percent'),
                                         show='headings', height=8)
            category_tree.heading('category', text='Категория')
            category_tree.heading('qty', text='Продано, шт')
            category_tree.heading('revenue', text='Выручка, ₽')
            category_tree.heading('percent', text='Доля от оборота')

            category_tree.column('category', width=200)
            category_tree.column('qty', width=120, anchor='center')
            category_tree.column('revenue', width=150, anchor='center')
            category_tree.column('percent', width=150, anchor='center')

            for item in categories_stats:
                percent = (item['total_revenue'] / total_revenue * 100) if total_revenue > 0 else 0
                category_tree.insert('', 'end', values=(item['category'], item['total_qty'],
                                                        f"{item['total_revenue']:,.0f}", f"{percent:.1f}%"))

            category_tree.pack(fill='x', expand=True)
        else:
            ttk.Label(category_frame, text="Пока нет заказов", font=('Segoe UI', 12),
                      foreground='#95a5a6').pack(anchor='w', pady=20)

        conn.close()

        btn_frame = ttk.Frame(scrollable_frame)
        btn_frame.pack(fill='x', pady=10)
        ttk.Button(btn_frame, text="Обновить статистику",
                   command=self.refresh_statistics, style='Primary.TButton').pack()

    def refresh_statistics(self):
        for i, tab_id in enumerate(self.notebook.tabs()):
            if self.notebook.tab(tab_id, "text") == "Статистика":
                self.notebook.forget(tab_id)
                break
        self.create_statistics_tab()
        self.notebook.select(self.notebook.tabs()[3])


def main():
    root = tk.Tk()
    app = FoodExpressApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()