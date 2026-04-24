import tkinter as tk

# ===== МОДЕЛЬ =====
class Model:
    def __init__(self):
        self.a = 10
        self.b = 50
        self.c = 90

    def set_a(self, value):
        self.a = value

    def set_b(self, value):
        self.b = value

    def set_c(self, value):
        self.c = value

    def get_values(self):
        return self.a, self.b, self.c


# ===== ПРИЛОЖЕНИЕ =====
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("MVC Lab")

        self.model = Model()

        # ===== ПОДПИСИ =====
        tk.Label(root, text="A").grid(row=0, column=0)
        tk.Label(root, text="B").grid(row=0, column=1)
        tk.Label(root, text="C").grid(row=0, column=2)

        # ===== ПОЛЯ ВВОДА =====
        self.entry_a = tk.Entry(root)
        self.entry_b = tk.Entry(root)
        self.entry_c = tk.Entry(root)

        self.entry_a.grid(row=1, column=0)
        self.entry_b.grid(row=1, column=1)
        self.entry_c.grid(row=1, column=2)

        # начальные значения
        self.update_view()

        # события
        self.entry_a.bind("<KeyRelease>", self.on_change)
        self.entry_b.bind("<KeyRelease>", self.on_change)
        self.entry_c.bind("<KeyRelease>", self.on_change)

    def on_change(self, event):
        try:
            a = int(self.entry_a.get())
            b = int(self.entry_b.get())
            c = int(self.entry_c.get())

            self.model.set_a(a)
            self.model.set_b(b)
            self.model.set_c(c)

        except:
            pass

    def update_view(self):
        a, b, c = self.model.get_values()

        self.entry_a.delete(0, tk.END)
        self.entry_a.insert(0, str(a))

        self.entry_b.delete(0, tk.END)
        self.entry_b.insert(0, str(b))

        self.entry_c.delete(0, tk.END)
        self.entry_c.insert(0, str(c))


# ===== ЗАПУСК =====
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
