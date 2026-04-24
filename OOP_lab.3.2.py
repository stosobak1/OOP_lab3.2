import tkinter as tk
import json
import os

# ===== МОДЕЛЬ =====
class Model:
    def __init__(self):
        self._a = 10
        self._b = 50
        self._c = 90
        self._observers = []

        self.load()

    # ===== ПОДПИСКА =====
    def subscribe(self, callback):
        self._observers.append(callback)

    def notify(self):
        for callback in self._observers:
            callback()

    # ===== ЛОГИКА =====
    def set_values(self, a, b, c):
        old = (self._a, self._b, self._c)

        # ограничения
        if a > b:
            b = a
        if b > c:
            c = b
        if b < a:
            a = b

        a = max(0, min(100, a))
        b = max(0, min(100, b))
        c = max(0, min(100, c))

        new = (a, b, c)

        # если ничего не изменилось — не уведомляем
        if old == new:
            return

        self._a, self._b, self._c = new

        self.save()
        self.notify()

    def get_values(self):
        return self._a, self._b, self._c

    # ===== СОХРАНЕНИЕ =====
    def save(self):
        data = {"a": self._a, "b": self._b, "c": self._c}
        with open("data.json", "w") as f:
            json.dump(data, f)

    def load(self):
        if os.path.exists("data.json"):
            try:
                with open("data.json", "r") as f:
                    data = json.load(f)
                    self._a = data["a"]
                    self._b = data["b"]
                    self._c = data["c"]
            except:
                pass


# ===== VIEW =====
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("MVC Lab")

        self.model = Model()
        self.model.subscribe(self.update_view)

        # ===== UI =====
        tk.Label(root, text="A", font=("Arial", 16)).grid(row=0, column=0)
        tk.Label(root, text="<=", font=("Arial", 16)).grid(row=0, column=1)
        tk.Label(root, text="B", font=("Arial", 16)).grid(row=0, column=2)
        tk.Label(root, text="<=", font=("Arial", 16)).grid(row=0, column=3)
        tk.Label(root, text="C", font=("Arial", 16)).grid(row=0, column=4)

        # ENTRY
        self.entry_a = tk.Entry(root, width=10)
        self.entry_b = tk.Entry(root, width=10)
        self.entry_c = tk.Entry(root, width=10)

        self.entry_a.grid(row=1, column=0)
        self.entry_b.grid(row=1, column=2)
        self.entry_c.grid(row=1, column=4)

        # SPINBOX
        self.spin_a = tk.Spinbox(root, from_=0, to=100, width=8)
        self.spin_b = tk.Spinbox(root, from_=0, to=100, width=8)
        self.spin_c = tk.Spinbox(root, from_=0, to=100, width=8)

        self.spin_a.grid(row=2, column=0)
        self.spin_b.grid(row=2, column=2)
        self.spin_c.grid(row=2, column=4)

        # SCALE
        self.scale_a = tk.Scale(root, from_=0, to=100, orient="horizontal")
        self.scale_b = tk.Scale(root, from_=0, to=100, orient="horizontal")
        self.scale_c = tk.Scale(root, from_=0, to=100, orient="horizontal")

        self.scale_a.grid(row=3, column=0)
        self.scale_b.grid(row=3, column=2)
        self.scale_c.grid(row=3, column=4)

        # ===== СОБЫТИЯ =====
        self.entry_a.bind("<KeyRelease>", self.update_from_entry)
        self.entry_b.bind("<KeyRelease>", self.update_from_entry)
        self.entry_c.bind("<KeyRelease>", self.update_from_entry)

        self.spin_a.bind("<KeyRelease>", self.update_from_spin)
        self.spin_b.bind("<KeyRelease>", self.update_from_spin)
        self.spin_c.bind("<KeyRelease>", self.update_from_spin)

        self.scale_a.config(command=self.update_from_scale)
        self.scale_b.config(command=self.update_from_scale)
        self.scale_c.config(command=self.update_from_scale)

        # первый рендер
        self.update_view()

    # ===== ОБНОВЛЕНИЯ =====
    def update_from_entry(self, event):
        try:
            self.model.set_values(
                int(self.entry_a.get()),
                int(self.entry_b.get()),
                int(self.entry_c.get())
            )
        except:
            pass

    def update_from_spin(self, event):
        try:
            self.model.set_values(
                int(self.spin_a.get()),
                int(self.spin_b.get()),
                int(self.spin_c.get())
            )
        except:
            pass

    def update_from_scale(self, value):
        self.model.set_values(
            self.scale_a.get(),
            self.scale_b.get(),
            self.scale_c.get()
        )

    # ===== VIEW =====
    def update_view(self):
        a, b, c = self.model.get_values()

        self._set(self.entry_a, a)
        self._set(self.entry_b, b)
        self._set(self.entry_c, c)

        self._set(self.spin_a, a)
        self._set(self.spin_b, b)
        self._set(self.spin_c, c)

        self.scale_a.set(a)
        self.scale_b.set(b)
        self.scale_c.set(c)

    def _set(self, widget, value):
        widget.delete(0, tk.END)
        widget.insert(0, str(value))


# ===== ЗАПУСК =====
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
