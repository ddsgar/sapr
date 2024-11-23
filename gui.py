import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from preprocessor import Preprocessor
from processor import Processor

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("САПР для стержневых конструкций")

        # Адаптация размера окна под размер монитора
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        self.root.geometry(f"{window_width}x{window_height}")

        self.preprocessor = Preprocessor()
        self.processor = None

        self.create_widgets()

    def create_widgets(self):
        self.input_frame = ttk.Frame(self.root)
        self.input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.node_frame = ttk.LabelFrame(self.input_frame, text="Узлы")
        self.node_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.element_frame = ttk.LabelFrame(self.input_frame, text="Элементы")
        self.element_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.load_frame = ttk.LabelFrame(self.input_frame, text="Нагрузки")
        self.load_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.bc_frame = ttk.LabelFrame(self.input_frame, text="Граничные условия")
        self.bc_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        self.control_frame = ttk.Frame(self.input_frame)
        self.control_frame.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        self.create_node_widgets()
        self.create_element_widgets()
        self.create_load_widgets()
        self.create_bc_widgets()
        self.create_control_widgets()

        self.canvas_frame = ttk.Frame(self.root)
        self.canvas_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.load_list_frame = ttk.LabelFrame(self.input_frame, text="Сохраненные нагрузки")
        self.load_list_frame.grid(row=5, column=0, padx=10, pady=10, sticky="ew")
        self.load_listbox = tk.Listbox(self.load_list_frame, height=5)
        self.load_listbox.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

    def create_node_widgets(self):
        ttk.Label(self.node_frame, text="X:").grid(row=0, column=0, padx=5, pady=5)
        self.node_x_entry = ttk.Entry(self.node_frame)
        self.node_x_entry.grid(row=0, column=1, padx=5, pady=5)

        self.add_node_button = ttk.Button(self.node_frame, text="Добавить узел", command=self.add_node)
        self.add_node_button.grid(row=0, column=2, padx=5, pady=5)

        self.node_listbox = tk.Listbox(self.node_frame, height=5)
        self.node_listbox.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

    def create_element_widgets(self):
        ttk.Label(self.element_frame, text="Узел 1:").grid(row=0, column=0, padx=5, pady=5)
        self.element_node1_entry = ttk.Entry(self.element_frame)
        self.element_node1_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.element_frame, text="Узел 2:").grid(row=0, column=2, padx=5, pady=5)
        self.element_node2_entry = ttk.Entry(self.element_frame)
        self.element_node2_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(self.element_frame, text="E:").grid(row=0, column=4, padx=5, pady=5)
        self.element_E_entry = ttk.Entry(self.element_frame)
        self.element_E_entry.grid(row=0, column=5, padx=5, pady=5)

        ttk.Label(self.element_frame, text="σ_max:").grid(row=0, column=6, padx=5, pady=5)
        self.element_sigma_max_entry = ttk.Entry(self.element_frame)
        self.element_sigma_max_entry.grid(row=0, column=7, padx=5, pady=5)

        ttk.Label(self.element_frame, text="Тип сечения:").grid(row=1, column=0, padx=5, pady=5)
        self.element_section_type_var = tk.StringVar(value="Прямоугольное")
        self.element_section_type_menu = ttk.OptionMenu(self.element_frame, self.element_section_type_var, "Прямоугольное", "Прямоугольное", "Треугольное", "Круглое")
        self.element_section_type_menu.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.element_frame, text="k:").grid(row=1, column=2, padx=5, pady=5)
        self.element_k_entry = ttk.Entry(self.element_frame)
        self.element_k_entry.grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(self.element_frame, text="b:").grid(row=1, column=4, padx=5, pady=5)
        self.element_b_entry = ttk.Entry(self.element_frame)
        self.element_b_entry.grid(row=1, column=5, padx=5, pady=5)

        ttk.Label(self.element_frame, text="r:").grid(row=1, column=6, padx=5, pady=5)
        self.element_r_entry = ttk.Entry(self.element_frame)
        self.element_r_entry.grid(row=1, column=7, padx=5, pady=5)

        self.add_element_button = ttk.Button(self.element_frame, text="Добавить элемент", command=self.add_element)
        self.add_element_button.grid(row=0, column=8, padx=5, pady=5)

        self.element_listbox = tk.Listbox(self.element_frame, height=5)
        self.element_listbox.grid(row=2, column=0, columnspan=9, padx=5, pady=5, sticky="ew")

    def create_load_widgets(self):
        ttk.Label(self.load_frame, text="Тип нагрузки:").grid(row=0, column=0, padx=5, pady=5)
        self.load_type_var = tk.StringVar(value="Сосредоточенная")
        self.load_type_menu = ttk.OptionMenu(self.load_frame, self.load_type_var, "Сосредоточенная", "Сосредоточенная", "Распределенная")
        self.load_type_menu.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.load_frame, text="Узел:").grid(row=0, column=2, padx=5, pady=5)
        self.load_node_entry = ttk.Entry(self.load_frame)
        self.load_node_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(self.load_frame, text="F:").grid(row=0, column=4, padx=5, pady=5)
        self.load_F_entry = ttk.Entry(self.load_frame)
        self.load_F_entry.grid(row=0, column=5, padx=5, pady=5)

        ttk.Label(self.load_frame, text="Узел 2:").grid(row=1, column=2, padx=5, pady=5)
        self.load_node2_entry = ttk.Entry(self.load_frame)
        self.load_node2_entry.grid(row=1, column=3, padx=5, pady=5)

        self.add_load_button = ttk.Button(self.load_frame, text="Добавить нагрузку", command=self.add_load)
        self.add_load_button.grid(row=0, column=6, padx=5, pady=5)

    def create_bc_widgets(self):
        ttk.Label(self.bc_frame, text="Узел:").grid(row=0, column=0, padx=5, pady=5)
        self.bc_node_entry = ttk.Entry(self.bc_frame)
        self.bc_node_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.bc_frame, text="u:").grid(row=0, column=2, padx=5, pady=5)
        self.bc_u_entry = ttk.Entry(self.bc_frame)
        self.bc_u_entry.grid(row=0, column=3, padx=5, pady=5)

        self.add_bc_button = ttk.Button(self.bc_frame, text="Добавить граничное условие", command=self.add_bc)
        self.add_bc_button.grid(row=0, column=4, padx=5, pady=5)

        ttk.Label(self.bc_frame, text="Тип заделки:").grid(row=1, column=0, padx=5, pady=5)
        self.bc_type_var = tk.StringVar(value="Заделка")
        self.bc_type_menu = ttk.OptionMenu(self.bc_frame, self.bc_type_var, "Заделка", "Заделка", "Шарнир")
        self.bc_type_menu.grid(row=1, column=1, padx=5, pady=5)

    def create_control_widgets(self):
        self.visualize_button = ttk.Button(self.control_frame, text="Визуализировать", command=self.visualize)
        self.visualize_button.grid(row=0, column=0, padx=5, pady=5)

        self.solve_button = ttk.Button(self.control_frame, text="Рассчитать", command=self.solve)
        self.solve_button.grid(row=0, column=1, padx=5, pady=5)

        self.save_button = ttk.Button(self.control_frame, text="Сохранить проект", command=self.save_project)
        self.save_button.grid(row=0, column=2, padx=5, pady=5)

        self.load_button = ttk.Button(self.control_frame, text="Загрузить проект", command=self.load_project)
        self.load_button.grid(row=0, column=3, padx=5, pady=5)

    def add_node(self):
        x = float(self.node_x_entry.get())
        self.preprocessor.add_node(x, 5)  # Y координата всегда 5
        self.update_node_listbox()

    def add_element(self):
        node1 = int(self.element_node1_entry.get())
        node2 = int(self.element_node2_entry.get())
        E = float(self.element_E_entry.get())
        sigma_max = float(self.element_sigma_max_entry.get())
        section_type = self.element_section_type_var.get()
        k = float(self.element_k_entry.get())
        b = float(self.element_b_entry.get())
        r = float(self.element_r_entry.get())

        if section_type == "Прямоугольное":
            A = k * b
        elif section_type == "Треугольное":
            A = 0.5 * k * b
        elif section_type == "Круглое":
            A = 3.14159 * r * r

        self.preprocessor.add_element(node1, node2, A, E, sigma_max, section_type, k, b, r)
        self.update_element_listbox()

    def add_load(self):
        load_type = self.load_type_var.get()
        node1 = int(self.load_node_entry.get())
        F = float(self.load_F_entry.get())
        if load_type == "Распределенная":
            node2 = int(self.load_node2_entry.get())
            self.preprocessor.add_load(load_type, node1, node2, F)
        else:
            self.preprocessor.add_load(load_type, node1, F)
        self.update_load_listbox()

    def add_bc(self):
        node = int(self.bc_node_entry.get())
        u = float(self.bc_u_entry.get())
        self.preprocessor.add_boundary_condition(node, u, 0)  # v всегда 0

    def update_node_listbox(self):
        self.node_listbox.delete(0, tk.END)
        for i, node in enumerate(self.preprocessor.nodes):
            self.node_listbox.insert(tk.END, f"Узел {i}: ({node[0]}, 5)")

    def update_element_listbox(self):
        self.element_listbox.delete(0, tk.END)
        for i, elem in enumerate(self.preprocessor.elements):
            self.element_listbox.insert(tk.END, f"Элемент {i}: Узел 1={elem['node1']}, Узел 2={elem['node2']}, E={elem['E']}, σ_max={elem['sigma_max']}, Тип сечения={elem['section_type']}, k={elem['k']}, b={elem['b']}, r={elem['r']}")

    def update_load_listbox(self):
        self.load_listbox.delete(0, tk.END)
        for i, load in enumerate(self.preprocessor.loads):
            if load['type'] == "Сосредоточенная":
                self.load_listbox.insert(tk.END, f"Нагрузка {i}: Тип={load['type']}, Узел={load['node']}, F={load['F']}")
            else:
                self.load_listbox.insert(tk.END, f"Нагрузка {i}: Тип={load['type']}, Узел 1={load['node1']}, Узел 2={load['node2']}, F={load['F']}")

    def visualize(self):
        fig, ax = plt.subplots()
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 15)

        for elem in self.preprocessor.elements:
            if elem['node1'] < len(self.preprocessor.nodes) and elem['node2'] < len(self.preprocessor.nodes):
                node1 = self.preprocessor.nodes[elem['node1']]
                node2 = self.preprocessor.nodes[elem['node2']]
                k = elem['k']
                b = elem['b']
                section_type = elem['section_type']

                # Центр стержня на координате 5 по Y
                center_y = 5

                if section_type == "Прямоугольное":
                    ax.plot([node1[0], node2[0]], [center_y - k / 2, center_y - k / 2], 'k-', linewidth=b)
                    ax.plot([node1[0], node2[0]], [center_y + k / 2, center_y + k / 2], 'k-', linewidth=b)
                    ax.plot([node1[0], node1[0]], [center_y - k / 2, center_y + k / 2], 'k-', linewidth=b)
                    ax.plot([node2[0], node2[0]], [center_y - k / 2, center_y + k / 2], 'k-', linewidth=b)
                elif section_type == "Треугольное":
                    ax.plot([node1[0], node2[0]], [center_y, center_y], 'k-', linewidth=b)
                    ax.plot([node1[0], node1[0] + b / 2], [center_y, center_y + k], 'k-', linewidth=b)
                    ax.plot([node1[0] + b / 2, node2[0]], [center_y + k, center_y], 'k-', linewidth=b)
                elif section_type == "Круглое":
                    ax.plot([node1[0], node2[0]], [center_y, center_y], 'k-', linewidth=b)
                    ax.add_patch(plt.Circle((node1[0], center_y), k / 2, color='k'))
                    ax.add_patch(plt.Circle((node2[0], center_y), k / 2, color='k'))
            else:
                print(f"Ошибка: Узел {elem['node1']} или {elem['node2']} не существует.")

        for load in self.preprocessor.loads:
            if load['type'] == "Сосредоточенная":
                node = self.preprocessor.nodes[load['node']]
                if load['F'] is not None:
                    arrow_color = 'r' if load['F'] > 0 else 'b'
                    ax.arrow(node[0], 5, 0, load['F'] / 10, head_width=0.1, head_length=0.1, fc=arrow_color, ec=arrow_color)
                    ax.annotate(f'F={load["F"]}', (node[0], 5))
                else:
                    print(f"Ошибка: Значение F для узла {load['node']} не определено.")
            elif load['type'] == "Распределенная":
                node1 = self.preprocessor.nodes[load['node1']]
                node2 = self.preprocessor.nodes[load['node2']]
                if load['F'] is not None:
                    arrow_color = 'r' if load['F'] > 0 else 'b'
                    num_arrows = 10  # Количество маленьких стрелок
                    for i in range(num_arrows):
                        x_pos = node1[0] + (node2[0] - node1[0]) * (i + 1) / (num_arrows + 1)
                        ax.arrow(x_pos, 5, 0, load['F'] / 100, head_width=0.05, head_length=0.05, fc=arrow_color, ec=arrow_color)
                    ax.annotate(f'q={load["F"]}', ((node1[0] + node2[0]) / 2, 5))
                else:
                    print(f"Ошибка: Значение F для узлов {load['node1']} и {load['node2']} не определено.")
            else:
                print(f"Ошибка: Узел {load['node']} не существует.")

        for bc in self.preprocessor.boundary_conditions:
            if bc['node'] < len(self.preprocessor.nodes):
                node = self.preprocessor.nodes[bc['node']]
                ax.plot(node[0], 5, 'go')
                ax.annotate(f'u={bc["u"]}', (node[0], 5))
            else:
                print(f"Ошибка: Узел {bc['node']} не существует.")

        # Отображение типа заделки
        bc_type = self.bc_type_var.get()
        if bc_type == "Шарнир":
            ax.plot(0, 5, 'ko')  # Шарнир
            ax.plot([-0.1, 0.1], [5, 5], 'k-')
            ax.plot([0, 0], [4.9, 5.1], 'k-')
        else:
            ax.plot([-0.1, 0.1], [5, 5], 'k-')  # Заделка

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    def solve(self):
        self.processor = Processor(self.preprocessor.nodes, self.preprocessor.elements, self.preprocessor.loads, self.preprocessor.boundary_conditions)
        u = self.processor.solve()
        stresses = self.processor.calculate_stresses(u)

        result_window = tk.Toplevel(self.root)
        result_window.title("Результаты")

        tk.Label(result_window, text="Перемещения:").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(result_window, text=str(u)).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(result_window, text="Напряжения:").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(result_window, text=str(stresses)).grid(row=1, column=1, padx=5, pady=5)

    def save_project(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            project_data = {
                "nodes": self.preprocessor.nodes,
                "elements": self.preprocessor.elements,
                "loads": self.preprocessor.loads,
                "boundary_conditions": self.preprocessor.boundary_conditions
            }
            with open(file_path, 'w') as f:
                json.dump(project_data, f, indent=4)
            messagebox.showinfo("Сохранение проекта", "Проект успешно сохранен.")

    def load_project(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as f:
                project_data = json.load(f)
                self.preprocessor.nodes = project_data["nodes"]
                self.preprocessor.elements = project_data["elements"]
                self.preprocessor.loads = project_data["loads"]
                self.preprocessor.boundary_conditions = project_data["boundary_conditions"]
            self.update_node_listbox()
            self.update_element_listbox()
            self.update_load_listbox()
            self.visualize()
            messagebox.showinfo("Загрузка проекта", "Проект успешно загружен.")
