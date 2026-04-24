import tkinter as tk

# ===== МОДЕЛЬ =====
class Model:
    def __init__(self):
        self.a = 10
        self.b = 50
        self.c = 90

    def set_values(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

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

        # ===== ENTRY =====
        self.entry_a = tk.Entry(root, width=10)
        self.entry_b = tk.Entry(root, width=10)
        self.entry_c = tk.Entry(root, width=10)

        self.entry_a.grid(row=1, column=0)
        self.entry_b.grid(row=1, column=1)
        self.entry_c.grid(row=1, column=2)

        # ===== SPINBOX =====
        self.spin_a = tk.Spinbox(root, from_=0, to=100, width=8)
        self.spin_b = tk.Spinbox(root, from_=0, to=100, width=8)
        self.spin_c = tk.Spinbox(root, from_=0, to=100, width=8)

        self.spin_a.grid(row=2, column=0)
        self.spin_b.grid(row=2, column=1)
        self.spin_c.grid(row=2, column=2)

        # ===== SCALE =====
        self.scale_a = tk.Scale(root, from_=0, to=100, orient="horizontal")
        self.scale_b = tk.Scale(root, from_=0, to=100, orient="horizontal")
        self.scale_c = tk.Scale(root, from_=0, to=100, orient="horizontal")

        self.scale_a.grid(row=3, column=0)
        self.scale_b.grid(row=3, column=1)
        self.scale_c.grid(row=3, column=2)

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

        # начальное обновление
        self.update_view()

    # ===== ОБНОВЛЕНИЕ ИЗ ENTRY =====
    def update_from_entry(self, event):
        try:
            a = int(self.entry_a.get())
            b = int(self.entry_b.get())
            c = int(self.entry_c.get())
            self.model.set_values(a, b, c)
            self.update_view()
        except:
            pass

    # ===== ОБНОВЛЕНИЕ ИЗ SPINBOX =====
    def update_from_spin(self, event):
        try:
            a = int(self.spin_a.get())
            b = int(self.spin_b.get())
            c = int(self.spin_c.get())
            self.model.set_values(a, b, c)
            self.update_view()
        except:
            pass

    # ===== ОБНОВЛЕНИЕ ИЗ SCALE =====
    def update_from_scale(self, value):
        a = self.scale_a.get()
        b = self.scale_b.get()
        c = self.scale_c.get()
        self.model.set_values(a, b, c)
        self.update_view()

    # ===== ОБНОВЛЕНИЕ VIEW =====
    def update_view(self):
        a, b, c = self.model.get_values()

        # Entry
        self.entry_a.delete(0, tk.END)
        self.entry_a.insert(0, str(a))

        self.entry_b.delete(0, tk.END)
        self.entry_b.insert(0, str(b))

        self.entry_c.delete(0, tk.END)
        self.entry_c.insert(0, str(c))

        # Spinbox
        self.spin_a.delete(0, tk.END)
        self.spin_a.insert(0, str(a))

        self.spin_b.delete(0, tk.END)
        self.spin_b.insert(0, str(b))

        self.spin_c.delete(0, tk.END)
        self.spin_c.insert(0, str(c))

        # Scale
        self.scale_a.set(a)
        self.scale_b.set(b)
        self.scale_c.set(c)


# ===== ЗАПУСК =====
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
