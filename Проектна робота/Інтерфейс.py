import tkinter as tk
from tkinter import messagebox, filedialog
import json
import math

def calculate():
    try:
        Fs = float(entry_fs.get().replace(",", "."))
        Vas = float(entry_vas.get().replace(",", "."))
        Qts_input = float(entry_qts.get().replace(",", "."))
        D = float(entry_d.get().replace(",", "."))

        # Перевірка чи Qts в межах від 1 до 100
        if not 1 <= Qts_input <= 100:
            raise ValueError("Qts має бути в межах від 1 до 100 (як відсоток).")

        # Перетворення Qts з відсотків у коефіцієнт
        Qts = Qts_input / 100

        # Визначення типу корпусу
        if Qts <= 0.4:
            box_type = "Закритий"
            volume = Vas * 0.7
        elif Qts <= 0.7:
            box_type = "Фазоінвертор"
            volume = Vas * 1.2
        else:
            box_type = "Не рекомендовано"
            result_volume.set("—")
            result_dimensions.set("—")
            result_type.set(box_type)
            messagebox.showwarning(
                "Qts занадто високе",
                "Цей динамік (Qts > 70%) не підходить для класичних оформлень (ЗЯ або ФІ)."
            )
            return

        # Обʼєм у м³
        volume_m3 = volume / 1000
        width_mm = math.ceil(D + 40)  # додаткові 40 мм на поле для динаміка
        height_mm = math.ceil(width_mm * 1.5)  # висота = 1.5 від ширини
        front_area_m2 = (width_mm / 1000) * (height_mm / 1000)  # площа переду в м²
        depth_m = volume_m3 / front_area_m2  # глибина, м
        depth_mm = math.ceil(depth_m * 1000)  # в мм

        # Виведення результатів
        result_volume.set(f"{volume:.2f}")
        result_dimensions.set(f"{height_mm} x {width_mm} x {depth_mm}")
        result_type.set(box_type)

    except ValueError as e:
        messagebox.showerror("Помилка", str(e))

def export_json():
    data = {
        "driver_parameters": {
            "Fs": entry_fs.get(),
            "Vas": entry_vas.get(),
            "Qts": entry_qts.get(),
            "D": entry_d.get()
        },
        "box_design": {
            "type": result_type.get(),
            "volume_liters": result_volume.get(),
            "dimensions_mm": result_dimensions.get()
        }
    }

    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Експорт", f"Результати збережено у файл:\n{file_path}")

# Інтерфейс
root = tk.Tk()
root.title("Розрахунок корпусу колонки")

# Введення
tk.Label(root, text="Fs (Гц):").grid(row=0, column=0, sticky="e")
entry_fs = tk.Entry(root)
entry_fs.grid(row=0, column=1)

tk.Label(root, text="Vas (л):").grid(row=1, column=0, sticky="e")
entry_vas = tk.Entry(root)
entry_vas.grid(row=1, column=1)

tk.Label(root, text="Qts (%) :").grid(row=2, column=0, sticky="e")
entry_qts = tk.Entry(root)
entry_qts.grid(row=2, column=1)

tk.Label(root, text="D (мм):").grid(row=3, column=0, sticky="e")
entry_d = tk.Entry(root)
entry_d.grid(row=3, column=1)

tk.Button(root, text="Розрахувати", command=calculate).grid(row=4, column=0, columnspan=2, pady=10)

# Результати
result_volume = tk.StringVar()
result_dimensions = tk.StringVar()
result_type = tk.StringVar()

tk.Label(root, text="Обʼєм корпусу (л):").grid(row=5, column=0, sticky="e")
tk.Label(root, textvariable=result_volume).grid(row=5, column=1)

tk.Label(root, text="Розміри H×W×D (мм):").grid(row=6, column=0, sticky="e")
tk.Label(root, textvariable=result_dimensions).grid(row=6, column=1)

tk.Label(root, text="Тип корпусу:").grid(row=7, column=0, sticky="e")
tk.Label(root, textvariable=result_type).grid(row=7, column=1)

tk.Button(root, text="Експортувати .json", command=export_json).grid(row=8, column=0, columnspan=2, pady=10)

root.mainloop()