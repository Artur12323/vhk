import tkinter as tk
from tkinter import messagebox, filedialog
import json

def calculate_box_volume(Vas, box_type="sealed", Qts_fixed=0.4, Qtc=0.707):
    """Обчислення об'єму корпусу в літрах без введення Qts"""
    if box_type == "sealed":
        if Qtc**2 / Qts_fixed**2 - 1 <= 0:
            raise ValueError("Некоректне співвідношення Qtc і Qts.")
        Vb = Vas / ((Qtc**2 / Qts_fixed**2) - 1)
    elif box_type == "bass_reflex":
        Vb = 20 * Vas * Qts_fixed**3.3
    elif box_type == "bandpass":
        sealed_part = Vas / ((Qtc**2 / Qts_fixed**2) - 1) if Qtc**2 / Qts_fixed**2 - 1 > 0 else Vas * 0.7
        reflex_part = 20 * Vas * Qts_fixed**3.3
        Vb = sealed_part + reflex_part
    else:
        raise ValueError("Невідомий тип корпусу.")
    return round(Vb, 2)

def calculate_dimensions(volume_liters, material_thickness_mm, woofer_diameter_mm):
    volume_m3 = volume_liters / 1000
    width = 0.25
    depth = 0.25
    height = volume_m3 / (width * depth)

    # Враховуємо розміри низькочастотного динаміка (вуфера)
    h_in = max(height * 1000, woofer_diameter_mm + 20)  # висота не може бути меншою за діаметр динаміка + запас
    w_in = width * 1000
    d_in = max(depth * 1000, woofer_diameter_mm * 0.4 + 30)  # глибина з запасом

    # Враховуємо товщину матеріалу
    t = material_thickness_mm
    h_out = h_in + 2 * t
    w_out = w_in + 2 * t
    d_out = d_in + 2 * t

    return {
        "internal": {"height": int(h_in), "width": int(w_in), "depth": int(d_in)},
        "external": {"height": int(h_out), "width": int(w_out), "depth": int(d_out)}
    }

def on_calculate():
    try:
        Fs = float(entry_fs.get())
        Vas = float(entry_vas.get())
        D = float(entry_d.get())
        Tweeter_D = float(entry_tweeter.get())  # діаметр твітера
        material_thickness = float(entry_thickness.get())
        Qts = 0.4  # фіксоване значення

        # Розрахунок для різних типів корпусів
        box_type_translation = {
            "Закритий": "sealed",
            "Фазоінвертор": "bass_reflex",
            "Бандпас": "bandpass"
        }
        box_type_key = box_type_translation.get(box_type_var.get(), "bass_reflex")  # за замовчуванням ФІ

        vol_sealed = calculate_box_volume(Vas, box_type_key, Qts)
        vol_br = calculate_box_volume(Vas, "bass_reflex", Qts)
        vol_bp = calculate_box_volume(Vas, "bandpass", Qts)

        dims_sealed = calculate_dimensions(vol_sealed, material_thickness, D)
        dims_br = calculate_dimensions(vol_br, material_thickness, D)
        dims_bp = calculate_dimensions(vol_bp, material_thickness, D)

        result_var.set(
            f"### Результати розрахунку:\n\n"
            f"1. Закритий корпус:\n"
            f"  Об'єм: {vol_sealed} л\n"
            f"  Розміри (внутрішні): {dims_sealed['internal']['height']}x{dims_sealed['internal']['width']}x{dims_sealed['internal']['depth']} мм\n"
            f"  Розміри (зовнішні): {dims_sealed['external']['height']}x{dims_sealed['external']['width']}x{dims_sealed['external']['depth']} мм\n\n"
            f"2. Фазоінвертор (Bass Reflex):\n"
            f"  Об'єм: {vol_br} л\n"
            f"  Розміри (внутрішні): {dims_br['internal']['height']}x{dims_br['internal']['width']}x{dims_br['internal']['depth']} мм\n"
            f"  Розміри (зовнішні): {dims_br['external']['height']}x{dims_br['external']['width']}x{dims_br['external']['depth']} мм\n\n"
            f"3. Бандпас:\n"
            f"  Об'єм: {vol_bp} л\n"
            f"  Розміри (внутрішні): {dims_bp['internal']['height']}x{dims_bp['internal']['width']}x{dims_bp['internal']['depth']} мм\n"
            f"  Розміри (зовнішні): {dims_bp['external']['height']}x{dims_bp['external']['width']}x{dims_bp['external']['depth']} мм"
        )

        global export_data
        export_data = {
            "driver_parameters": {
                "Fs": Fs,
                "Vas": Vas,
                "Qts (fixed)": Qts,
                "D (woofer diameter)": D,
                "D (tweeter diameter)": Tweeter_D
            },
            "sealed_box": {
                "volume_liters": vol_sealed,
                "dimensions_mm": dims_sealed
            },
            "bass_reflex": {
                "volume_liters": vol_br,
                "dimensions_mm": dims_br
            },
            "bandpass": {
                "volume_liters": vol_bp,
                "dimensions_mm": dims_bp
            }
        }

    except ValueError as e:
        messagebox.showerror("Помилка", f"Некоректні дані: {e}")

def on_export():
    if not export_data:
        messagebox.showinfo("Увага", "Спочатку зробіть розрахунок.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON файли", "*.json")])
    if file_path:
        with open(file_path, 'w') as f:
            json.dump(export_data, f, indent=4)
        messagebox.showinfo("Експорт", "Дані збережено успішно.")

# GUI
root = tk.Tk()
root.title("Розрахунок об’єму корпусу колонки")

# Введення параметрів
tk.Label(root, text="1. Fs (Гц) — резонансна частота динаміка:").grid(row=0, column=0)
tk.Label(root, text="2. Vas (л) — еквівалентний об'єм повітря динаміка:").grid(row=1, column=0)
tk.Label(root, text="3. Діаметр низькочастотного динаміка (мм):").grid(row=2, column=0)
tk.Label(root, text="4. Діаметр твітера (мм):").grid(row=3, column=0)
tk.Label(root, text="5. Товщина матеріалу (мм) для корпусу:").grid(row=4, column=0)

entry_fs = tk.Entry(root)
entry_vas = tk.Entry(root)
entry_d = tk.Entry(root)
entry_tweeter = tk.Entry(root)
entry_thickness = tk.Entry(root)
entry_thickness.insert(0, "18")  # стандартне значення товщини матеріалу

entry_fs.grid(row=0, column=1)
entry_vas.grid(row=1, column=1)
entry_d.grid(row=2, column=1)
entry_tweeter.grid(row=3, column=1)
entry_thickness.grid(row=4, column=1)

# Вибір типу корпусу
box_type_var = tk.StringVar(value="Фазоінвертор")
tk.Label(root, text="6. Тип корпусу:").grid(row=5, column=0)
tk.OptionMenu(root, box_type_var, "Закритий", "Фазоінвертор", "Бандпас").grid(row=5, column=1)

# Кнопка розрахунку
tk.Button(root, text="🔍 Розрахувати об'єм і розміри", command=on_calculate).grid(row=6, column=0, columnspan=2, pady=10)

# Виведення результатів
result_var = tk.StringVar()
tk.Label(root, textvariable=result_var, justify="left", wraplength=600).grid(row=7, column=0, columnspan=3, padx=10, sticky="w")

# Кнопка експорту
tk.Button(root, text="💾 Експортувати результат в .json", command=on_export).grid(row=8, column=0, columnspan=2, pady=10)

export_data = None
root.mainloop()
