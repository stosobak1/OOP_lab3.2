import tkinter as tk
import json
import os

# ===== МОДЕЛЬ (Model) =====
class NumbersModel:
    def __init__(self):
        self._a = 0
        self._b = 50
        self._c = 100
        self._observers = []
        self._filename = "data.json"
        self.load()

    def add_observer(self, observer):
        self._observers.append(observer)
        self.notify_observers()

    def notify_observers(self):
        # Атомарное уведомление всех подписчиков
        for observer in self._observers:
            observer(self._a, self._b, self._c)

    # --- Логика изменения значений ---

    def set_a(self, val):
        val = self._clamp(val)
        if val == self._a: return
        self._a = val
        # Разрешающее поведение: A двигает B и C вперед
        if self._a > self._b: self._b = self._a
        if self._b > self._c: self._c = self._b
        self._finalize()

    def set_b(self, val):
        val = self._clamp(val)
        # Ограничивающее поведение: B зажат между A и C
        new_b = max(self._a, min(self._c, val))
        # Если значение не изменилось (попытка выйти за границы), 
        # все равно уведомляем, чтобы UI сбросил некорректный ввод
        if new_b == self._b:
            self.notify_observers()
            return
        self._b = new_b
        self._finalize()

    def set_c(self, val):
        val = self._clamp(val)
        if val == self._c: return
        self._c = val
        # Разрешающее поведение: C тянет B и A назад
        if self._c < self._b: self._b = self._c
        if self._b < self._a: self._a = self._b
        self._finalize()

    def _clamp(self, val):
        return max(0, min(100, val))

    def _finalize(self):
        self.save()
        self.notify_observers()

    def save(self):
        try:
            with open(self._filename, "w") as f:
                json.dump({"a": self._a, "b": self._b, "c": self._c}, f)
        except: pass

    def load(self):
        if os.path.exists(self._filename):
            try:
                with open(self._filename, "r") as f:
                    d = json.load(f)
                    self._a = self._clamp(d.get("a", 0))
                    self._b = self._clamp(d.get("b", 50))
                    self._c = self._clamp(d.get("c", 100))
                    # Проверка правил на случай ручного редактирования JSON
                    if self._a > self._b: self._b = self._a
                    if self._b > self._c: self._c = self._b
            except: pass


# ===== ПРЕДСТАВЛЕНИЕ (View) И КОНТРОЛЛЕР (Controller) =====
class App:
    def __init__(self, root, model):
        self.root = root
        self.model = model
        self.root.title("MVC Lab 3")
        self.root.geometry("500x300")
        self.root.minsize(400, 250)

        self._lock = False # Блокировка рекурсии при обновлении

        # Настройка сетки для адаптивности
        for i in range(3): self.root.columnconfigure(i, weight=1)
        for i in range(4): self.root.rowconfigure(i, weight=1)

        # Функция валидации: разрешает только цифры (P - новое значение поля)
        self.vcmd = (self.root.register(lambda P: P == "" or P.isdigit()), '%P')

        self._init_ui()
        self.model.add_observer(self.update_view)

    def _init_ui(self):
        self.widgets = {'a': {}, 'b': {}, 'c': {}}
        
        headers = ["A", "B", "C"]
        for i, h in enumerate(headers):
            tk.Label(self.root, text=h, font=("Arial", 12, "bold")).grid(row=0, column=i)

        for i, key in enumerate(['a', 'b', 'c']):
            # 1. Текстовое поле (Entry)
            e = tk.Entry(self.root, validate="key", validatecommand=self.vcmd, justify='center')
            e.grid(row=1, column=i, padx=10, sticky="ew")
            e.bind("<FocusOut>", lambda ev, k=key: self._send_to_model(k, ev.widget.get()))
            e.bind("<Return>", lambda ev, k=key: self._send_to_model(k, ev.widget.get()))
            self.widgets[key]['ent'] = e

            # 2. Спинбокс (Spinbox)
            s = tk.Spinbox(self.root, from_=0, to=100, justify='center',
                           validate="key", validatecommand=self.vcmd,
                           command=lambda k=key: self._send_to_model(k, self.widgets[k]['spn'].get()))
            s.grid(row=2, column=i, padx=10, sticky="ew")
            s.bind("<FocusOut>", lambda ev, k=key: self._send_to_model(k, ev.widget.get()))
            self.widgets[key]['spn'] = s

            # 3. Ползунок (Scale)
            sc = tk.Scale(self.root, from_=0, to=100, orient="horizontal", showvalue=False,
                          command=lambda val, k=key: self._send_to_model(k, val))
            sc.grid(row=3, column=i, padx=10, sticky="ew")
            self.widgets[key]['scl'] = sc

    def _send_to_model(self, key, value):
        if self._lock or value == "": return
        try:
            val = int(value)
            setter = getattr(self.model, f"set_{key}")
            setter(val)
        except ValueError:
            self.model.notify_observers() # Откат при ошибке

    def update_view(self, a, b, c):
        if self._lock: return
        self._lock = True
        
        data = {'a': a, 'b': b, 'c': c}
        for key, val in data.items():
            # Обновление Entry
            self.widgets[key]['ent'].delete(0, tk.END)
            self.widgets[key]['ent'].insert(0, str(val))
            
            # Обновление Spinbox
            self.widgets[key]['spn'].delete(0, tk.END)
            self.widgets[key]['spn'].insert(0, str(val))
            
            # Обновление Scale
            self.widgets[key]['scl'].set(val)
            
        self._lock = False

if __name__ == "__main__":
    root = tk.Tk()
    model = NumbersModel()
    app = App(root, model)
    root.mainloop()
