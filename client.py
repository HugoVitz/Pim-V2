import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog, ttk
import os
from PIL import Image, ImageTk
from database import Database

class App:
    def __init__(self):
        self.db = Database()
        self.user = None
        self.root = tk.Tk()
        self.root.title("Sistema de Gerenciamento Escolar")
        self.root.geometry("800x600")
        self.root.configure(bg="#FFFFFF")

        # base_dir para caminhos relativos robustos (funciona também com PyInstaller)
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

        # ícone da janela (braintech.ico) — tenta carregar e não quebra se falhar
        icon_path = os.path.join(self.base_dir, "imagens", "braintech.ico")
        try:
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"⚠️ Erro ao carregar ícone: {e}")

        # carrega imagens comuns (mas não exige que existam)
        self._load_common_images()

        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 12), padding=10)
        self.style.configure("TLabel", font=("Arial", 12), background="#FFFFFF")
        self.create_login_screen()

    def _load_common_images(self):
        """Tenta carregar as imagens que serão usadas pelo app.
           Se alguma não existir, define None para a imagem correspondente."""
        imgs_dir = os.path.join(self.base_dir, "imagens")

       

        # fundo do professor e do aluno (principal)
        self.bg_prof_image = None
        bg_prof_path = os.path.join(imgs_dir, "bg-professor.png")
        if os.path.exists(bg_prof_path):
            try:
                pimg = Image.open(bg_prof_path)
                pimg = pimg.resize((800, 600), Image.Resampling.LANCZOS)
                self.bg_prof_image = ImageTk.PhotoImage(pimg)
            except Exception as e:
                print(f"⚠️ Erro ao carregar bg-professor.png: {e}")

        self.bg_aluno_image = None
        bg_aluno_path = os.path.join(imgs_dir, "bg-aluno.png")
        if os.path.exists(bg_aluno_path):
            try:
                aimg = Image.open(bg_aluno_path)
                aimg = aimg.resize((800, 600), Image.Resampling.LANCZOS)
                self.bg_aluno_image = ImageTk.PhotoImage(aimg)
            except Exception as e:
                print(f"⚠️ Erro ao carregar bg-aluno.png: {e}")

    # ---------------------- TELA DE LOGIN ----------------------
    def create_login_screen(self):
        
        self.clear_screen()

        # usaremos um Canvas para facilitar colocar background + widgets por cima
        self.login_canvas = tk.Canvas(self.root, width=800, height=600, highlightthickness=0)
        self.login_canvas.pack(expand=True, fill=tk.BOTH)

        # Fundo: cor sólida sem imagem
        self.login_canvas.configure(bg="#FFFFFF")

        # Centralização: colocaremos os elementos próximos do centro (x=400)
        center_x = 400
        title_y = 110
        subtitle_y = 150
        form_start_y = 210
        spacing = 50
        entry_width = 300

        # Título e subtítulo: desenhados como textos sobre o canvas (branco, sem fundo)
        self.login_canvas.create_text(center_x, title_y, text="Seja Bem Vindo ao BrainTech!\n",
                                      font=("Arial", 25, "bold"), fill="#000000")
        self.login_canvas.create_text(center_x, subtitle_y, text="Login", font=("Arial,", 20, "bold" ), fill="#000000")

        # Para garantir legibilidade mínima sobre imagens muito claras, desenhamos
        # um leve retângulo semitransparente atrás dos campos usando stipple.
        # Se preferir sem essa "camada", mude draw_shade = False.
        draw_shade = False
        if draw_shade:
            shade_left = center_x - (entry_width // 2) - 20
            shade_right = center_x + (entry_width // 2) + 20
            shade_top = form_start_y - 30
            shade_bottom = form_start_y + spacing * 1.6 + 10
            # usa stipple para simular transparência (padrão Tk)
            self.login_canvas.create_rectangle(shade_left, shade_top, shade_right, shade_bottom,
                                               fill="#000000", outline="", stipple="gray25")

        # Labels: criados como canvas text (branco, sem fundo) para ficar "apenas letras"
        user_label_y = form_start_y
        pass_label_y = form_start_y + spacing

        self.login_canvas.create_text(center_x - (entry_width // 2) + 40, user_label_y - 10,
                                      text="Usuário:", anchor="w", font=("Arial", 15, "bold" ), fill="#07033F")
        self.login_canvas.create_text(center_x - (entry_width // 2) + 40, pass_label_y - 10,
                                      text="Senha:", anchor="w", font=("Arial", 15,"bold"  ), fill="#07033F")

        # Entradas: widgets Entry (colocados sobre o canvas). Estilizadas para serem discretas:
        # bd=0, relief='flat', highlightthickness=0, fg=white, insertbackground=white
        entry_x = center_x + (entry_width // 2) - (entry_width // 2) + 0  # lógica de alinhamento central
        # Entrada de Nome de Usuário
        self.username_entry = tk.Entry(self.root, font=("Arial", 12), bd=0, relief='flat', highlightthickness=0,
                                       fg="black", insertbackground="black", bg="#D3D3D3")
        # Entrada de Senha
        self.password_entry = tk.Entry(self.root, show="*", font=("Arial", 12), bd=0, relief='flat',
                                       highlightthickness=0, fg="black", insertbackground="black", bg="#D3D3D3")

        # NOTA: Tkinter Entry não suporta transparência verdadeira. Para minimizar a borda,
        # definimos bd=0 e relief='flat'. Se a sua imagem torna difícil ver onde digitar,
        
        # Abaixo posicionamos as entradas (width em pixels via create_window width).
        self.login_canvas.create_window(center_x, user_label_y + 12, window=self.username_entry, width=entry_width)
        self.login_canvas.create_window(center_x, pass_label_y + 12, window=self.password_entry, width=entry_width)

        # Opcional: desenhar linhas sutis abaixo das entradas para indicar campo (opcional)
        draw_underline = True
        if draw_underline:
            underline_offset = 18
            u_left = center_x - (entry_width // 2)
            u_right = center_x + (entry_width // 2)
            # linha branca sutil para indicar campo
            self.login_canvas.create_line(u_left, user_label_y + underline_offset, u_right, user_label_y + underline_offset,
                                          fill="#575757", width=1)
            self.login_canvas.create_line(u_left, pass_label_y + underline_offset, u_right, pass_label_y + underline_offset,
                                          fill="#575757", width=1)

        # Botão Entrar - centralizado
        login_btn = ttk.Button(self.root, text="Entrar", command=self.login)
        self.login_canvas.create_window(center_x, form_start_y + spacing * 1.9, window=login_btn)

    # ---------------------- LOGIN / AUTENTICAÇÃO ----------------------
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        request = {'action': 'login', 'username': username, 'password': password}
        response = self.send_request(request)
        if response['status'] == 'success':
            self.user = response['user']
            self.create_main_screen()
        else:
            messagebox.showerror("Erro", response['message'])
            

    # ---------------------- TELA PRINCIPAL (APÓS LOGIN) ----------------------
    def create_main_screen(self):
        self.clear_screen()

        # Canvas principal para facilitar desenho do fundo e topbar
        self.canvas = tk.Canvas(self.root, width=800, height=600, highlightthickness=0)
        self.canvas.pack(expand=True, fill=tk.BOTH)

        # escolhe fundo por papel (alternativa para cor se imagens não existirem)
        if self.user['role'] == 'Professor' and self.bg_prof_image:
            self.canvas.create_image(0, 0, anchor='nw', image=self.bg_prof_image)
            self.canvas.bg_ref = self.bg_prof_image
        elif self.user['role'] != 'Professor' and self.bg_aluno_image:
            self.canvas.create_image(0, 0, anchor='nw', image=self.bg_aluno_image)
            self.canvas.bg_ref = self.bg_aluno_image
        else:
            self.canvas.configure(bg="#f0f0f0")

        # imagem da barra superior (se existir) — fixa no topo
        if self.topbar_image:
            pass
        else:
            self.canvas.create_rectangle(0, 0, 800, 60, fill="#0b63b8", outline="")

        # Texto de boas-vindas (com sombra simulada)
        welcome_text = f"Bem-vindo, {self.user['username']}"
        # sombra
        self.canvas.create_text(402, 85, text=welcome_text, font=("Arial", 18, "bold"), fill="#000000")
        # texto branco por cima
        self.canvas.create_text(400, 82, text=welcome_text, font=("Arial", 18, "bold"), fill="white")

        # Botões (criados como widgets dentro do canvas)
        button_y = 150
        button_width = 220

        def make_button(text, cmd, y):
            btn = ttk.Button(self.canvas, text=text, command=cmd)
            self.canvas.create_window(400, y, window=btn, width=button_width)

        current_y = button_y

        if self.user['role'] == 'Professor':
            # Parte do Professor: Gerenciamento completo
            make_button("Gerenciar Turmas", self.manage_classes, current_y); current_y += 50
            make_button("Registrar Aula", self.manage_lessons, current_y); current_y += 50
            make_button("Marcar Presença", self.manage_attendance, current_y); current_y += 50
            make_button("Gerenciar Atividades", self.manage_activities, current_y); current_y += 50
        else:
            # Parte do Aluno: Visualização apenas
            make_button("Ver Turmas", self.view_classes, current_y); current_y += 50
            make_button("Ver Aulas", self.view_lessons, current_y); current_y += 50
            make_button("Ver Atividades", self.view_activities, current_y); current_y += 50

        # botão sair (última posição)
        make_button("Sair", self.logout, current_y)

    # ---------------------- DEMAIS TELAS E FUNÇÕES (mantive as funções originais) ----------------------
    def manage_classes(self):
        self.clear_screen()
        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        tk.Label(frame, text="Gerenciar Turmas", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=20)

        button_frame = tk.Frame(frame, bg="#f0f0f0")
        button_frame.pack(expand=True)

        ttk.Button(button_frame, text="Criar Turma", command=self.create_class).pack(pady=10, fill=tk.X)
        ttk.Button(button_frame, text="Adicionar Aluno", command=self.add_student).pack(pady=10, fill=tk.X)
        ttk.Button(button_frame, text="Voltar", command=self.create_main_screen).pack(pady=20, fill=tk.X)

    def create_class(self):
        name = simpledialog.askstring("Criar Turma", "Nome da Turma:")
        if name:
            request = {'action': 'add_class', 'name': name, 'teacher_id': self.user['id']}
            response = self.send_request(request)
            if response['status'] == 'success':
                messagebox.showinfo("Sucesso", "Turma criada!")
            else:
                messagebox.showerror("Erro", response['message'])

    def add_student(self):
        request = {'action': 'get_classes', 'teacher_id': self.user['id']}
        response = self.send_request(request)
        if response['status'] == 'success':
            classes = response['classes']
            if classes:
                class_names = [cls[1] for cls in classes]
                class_choice = simpledialog.askstring("Adicionar Aluno", f"Escolha a turma: {', '.join(class_names)}")
                class_id = next((cls[0] for cls in classes if cls[1] == class_choice), None)
                if class_id:
                    name = simpledialog.askstring("Adicionar Aluno", "Nome do Aluno:")
                    if name:
                        request = {'action': 'add_student', 'name': name, 'class_id': class_id}
                        response = self.send_request(request)
                        if response['status'] == 'success':
                            messagebox.showinfo("Sucesso", "Aluno adicionado!")
                        else:
                            messagebox.showerror("Erro", response['message'])
            else:
                messagebox.showinfo("Info", "Nenhuma turma encontrada.")
        else:
            messagebox.showerror("Erro", response['message'])

    def manage_lessons(self):
        self.clear_screen()
        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        tk.Label(frame, text="Registrar Aula", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=20)

        button_frame = tk.Frame(frame, bg="#f0f0f0")
        button_frame.pack(expand=True)

        ttk.Button(button_frame, text="Registrar Nova Aula", command=self.register_lesson).pack(pady=10, fill=tk.X)
        ttk.Button(button_frame, text="Voltar", command=self.create_main_screen).pack(pady=20, fill=tk.X)

    def register_lesson(self):
        request = {'action': 'get_classes', 'teacher_id': self.user['id']}
        response = self.send_request(request)
        if response['status'] == 'success':
            classes = response['classes']
            if classes:
                class_names = [cls[1] for cls in classes]
                class_choice = simpledialog.askstring("Registrar Aula", f"Escolha a turma: {', '.join(class_names)}")
                class_id = next((cls[0] for cls in classes if cls[1] == class_choice), None)
                if class_id:
                    date = simpledialog.askstring("Registrar Aula", "Data (dd/mm/aaaa):")
                    topic = simpledialog.askstring("Registrar Aula", "Tópico:")
                    if date and topic:
                        request = {'action': 'add_lesson', 'class_id': class_id, 'date': date, 'topic': topic}
                        response = self.send_request(request)
                        if response['status'] == 'success':
                            messagebox.showinfo("Sucesso", "Aula registrada!")
                        else:
                            messagebox.showerror("Erro", response['message'])
            else:
                messagebox.showinfo("Info", "Nenhuma turma encontrada.")

    def manage_attendance(self):
        self.clear_screen()
        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        tk.Label(frame, text="Marcar Presença", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=20)

        button_frame = tk.Frame(frame, bg="#f0f0f0")
        button_frame.pack(expand=True)

        ttk.Button(button_frame, text="Marcar Presença em Aula", command=self.mark_attendance).pack(pady=10, fill=tk.X)
        ttk.Button(button_frame, text="Voltar", command=self.create_main_screen).pack(pady=20, fill=tk.X)

    def mark_attendance(self):
        request = {'action': 'get_classes', 'teacher_id': self.user['id']}
        response = self.send_request(request)
        if response['status'] == 'success':
            classes = response['classes']
            if classes:
                class_names = [cls[1] for cls in classes]
                class_choice = simpledialog.askstring("Marcar Presença", f"Escolha a turma: {', '.join(class_names)}")
                class_id = next((cls[0] for cls in classes if cls[1] == class_choice), None)
                if class_id:
                    request = {'action': 'get_lessons', 'class_id': class_id}
                    response = self.send_request(request)
                    if response['status'] == 'success':
                        lessons = response['lessons']
                        if lessons:
                            lesson_topics = [f"{lesson[2]} - {lesson[3]}" for lesson in lessons]
                            lesson_choice = simpledialog.askstring("Marcar Presença", f"Escolha a aula: {', '.join(lesson_topics)}")
                            lesson_id = next((lesson[0] for lesson in lessons if f"{lesson[2]} - {lesson[3]}" == lesson_choice), None)
                            if lesson_id:
                                request = {'action': 'get_students', 'class_id': class_id}
                                response = self.send_request(request)
                                if response['status'] == 'success':
                                    students = response['students']
                                    attendances = []
                                    for student in students:
                                        present = messagebox.askyesno("Presença", f"{student[1]} presente?")
                                        attendances.append((student[0], 1 if present else 0))
                                    request = {'action': 'add_attendance', 'lesson_id': lesson_id, 'attendances': attendances}
                                    response = self.send_request(request)
                                    if response['status'] == 'success':
                                        messagebox.showinfo("Sucesso", "Presença marcada!")
                                    else:
                                        messagebox.showerror("Erro", response['message'])
                        else:
                            messagebox.showinfo("Info", "Nenhuma aula encontrada.")
            else:
                messagebox.showinfo("Info", "Nenhuma turma encontrada.")

    def manage_activities(self):
        self.clear_screen()
        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        tk.Label(frame, text="Gerenciar Atividades", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=20)

        button_frame = tk.Frame(frame, bg="#f0f0f0")
        button_frame.pack(expand=True)

        ttk.Button(button_frame, text="Upload Atividade", command=self.upload_activity).pack(pady=10, fill=tk.X)
        ttk.Button(button_frame, text="Voltar", command=self.create_main_screen).pack(pady=20, fill=tk.X)

    def upload_activity(self):
        request = {'action': 'get_classes', 'teacher_id': self.user['id']}
        response = self.send_request(request)
        if response['status'] == 'success':
            classes = response['classes']
            if classes:
                class_names = [cls[1] for cls in classes]
                class_choice = simpledialog.askstring("Upload Atividade", f"Escolha a turma: {', '.join(class_names)}")
                class_id = next((cls[0] for cls in classes if cls[1] == class_choice), None)
                if class_id:
                    file_path = filedialog.askopenfilename(title="Selecionar Arquivo")
                    if file_path:
                        name = simpledialog.askstring("Upload Atividade", "Nome da Atividade:")
                        if name:
                            dest_dir = "atividades"
                            os.makedirs(dest_dir, exist_ok=True)
                            dest_path = os.path.join(dest_dir, os.path.basename(file_path))
                            with open(file_path, 'rb') as src, open(dest_path, 'wb') as dst:
                                dst.write(src.read())
                            request = {'action': 'add_atividade', 'class_id': class_id, 'name': name, 'file_path': dest_path}
                            response = self.send_request(request)
                            if response['status'] == 'success':
                                messagebox.showinfo("Sucesso", "Atividade enviada!")
                            else:
                                messagebox.showerror("Erro", response['message'])
            else:
                messagebox.showinfo("Info", "Nenhuma turma encontrada.")

    def view_classes(self):
        request = {'action': 'get_classes'}
        response = self.send_request(request)
        if response['status'] == 'success':
            classes = response['classes']
            class_list = "\n".join([cls[1] for cls in classes])
            messagebox.showinfo("Turmas", class_list if class_list else "Nenhuma turma encontrada.")
        else:
            messagebox.showerror("Erro", response['message'])

    def view_lessons(self):
        request = {'action': 'get_classes'}
        response = self.send_request(request)
        if response['status'] == 'success':
            classes = response['classes']
            if classes:
                class_names = [cls[1] for cls in classes]
                class_choice = simpledialog.askstring("Ver Aulas", f"Escolha a turma: {', '.join(class_names)}")
                class_id = next((cls[0] for cls in classes if cls[1] == class_choice), None)
                if class_id:
                    request = {'action': 'get_lessons', 'class_id': class_id}
                    response = self.send_request(request)
                    if response['status'] == 'success':
                        lessons = response['lessons']
                        lesson_list = "\n".join([f"{lesson[2]} - {lesson[3]}" for lesson in lessons])
                        messagebox.showinfo("Aulas", lesson_list if lesson_list else "Nenhuma aula encontrada.")
                    else:
                        messagebox.showerror("Erro", response['message'])
            else:
                messagebox.showinfo("Info", "Nenhuma turma encontrada.")

    def view_activities(self):
        request = {'action': 'get_classes'}
        response = self.send_request(request)
        if response['status'] == 'success':
            classes = response['classes']
            if classes:
                class_names = [cls[1] for cls in classes]
                class_choice = simpledialog.askstring("Ver Atividades", f"Escolha a turma: {', '.join(class_names)}")
                class_id = next((cls[0] for cls in classes if cls[1] == class_choice), None)
                if class_id:
                    request = {'action': 'get_atividades', 'class_id': class_id}
                    response = self.send_request(request)
                    if response['status'] == 'success':
                        atividades = response['atividades']
                        activity_list = "\n".join([atividade[2] for atividade in atividades])
                        messagebox.showinfo("Atividades", activity_list if activity_list else "Nenhuma atividade encontrada.")
                    else:
                        messagebox.showerror("Erro", response['message'])
            else:
                messagebox.showinfo("Info", "Nenhuma turma encontrada.")

    def logout(self):
        self.user = None
        self.create_login_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def send_request(self, request):
        action = request.get('action')
        if action == 'login':
            username = request.get('username')
            password = request.get('password')
            if not username or not password:
                return {'status': 'error', 'message': 'Nome de usuário e senha obrigatórios'}
            user = self.db.get_user(username)
            if user and user[2] == password:
                return {'status': 'success', 'user': {'id': user[0], 'username': user[1], 'role': user[3], 'email': user[4]}}
            else:
                return {'status': 'error', 'message': 'Credenciais inválidas'}
        elif action == 'add_class':
            name = request.get('name')
            teacher_id = request.get('teacher_id')
            if not name or not teacher_id:
                return {'status': 'error', 'message': 'Nome e ID do professor obrigatórios'}
            self.db.add_class(name, teacher_id)
            return {'status': 'success'}
        elif action == 'get_classes':
            teacher_id = request.get('teacher_id')
            if teacher_id:
                classes = self.db.get_classes_by_teacher(teacher_id)
            else:
                classes = self.db.get_all_classes()
            return {'status': 'success', 'classes': classes}
        elif action == 'add_student':
            name = request.get('name')
            class_id = request.get('class_id')
            if not name or not class_id:
                return {'status': 'error', 'message': 'Nome e ID da turma obrigatórios'}
            self.db.add_student(name, class_id)
            return {'status': 'success'}
        elif action == 'get_students':
            class_id = request.get('class_id')
            if not class_id:
                return {'status': 'error', 'message': 'ID da turma obrigatório'}
            students = self.db.get_students_by_class(class_id)
            return {'status': 'success', 'students': students}
        elif action == 'add_lesson':
            class_id = request.get('class_id')
            date = request.get('date')
            topic = request.get('topic')
            if not class_id or not date or not topic:
                return {'status': 'error', 'message': 'ID da turma, data e tópico obrigatórios'}
            self.db.add_lesson(class_id, date, topic)
            return {'status': 'success'}
        elif action == 'get_lessons':
            class_id = request.get('class_id')
            if not class_id:
                return {'status': 'error', 'message': 'ID da turma obrigatório'}
            lessons = self.db.get_lessons_by_class(class_id)
            return {'status': 'success', 'lessons': lessons}
        elif action == 'add_attendance':
            lesson_id = request.get('lesson_id')
            attendances = request.get('attendances')  # lista de (id_aluno, presente)
            if not lesson_id or not attendances:
                return {'status': 'error', 'message': 'ID da aula e presenças obrigatórios'}
            for student_id, present in attendances:
                self.db.add_attendance(lesson_id, student_id, present)
            return {'status': 'success'}
        elif action == 'get_attendance':
            lesson_id = request.get('lesson_id')
            if not lesson_id:
                return {'status': 'error', 'message': 'ID da aula obrigatório'}
            attendance = self.db.get_attendance_by_lesson(lesson_id)
            return {'status': 'success', 'attendance': attendance}
        elif action == 'add_atividade':
            class_id = request.get('class_id')
            name = request.get('name')
            file_path = request.get('file_path')
            if not class_id or not name or not file_path:
                return {'status': 'error', 'message': 'ID da turma, nome e caminho do arquivo obrigatórios'}
            self.db.add_atividade(class_id, name, file_path)
            return {'status': 'success'}
        elif action == 'get_atividades':
            class_id = request.get('class_id')
            if not class_id:
                return {'status': 'error', 'message': 'ID da turma obrigatório'}
            atividades = self.db.get_atividades_by_class(class_id)
            return {'status': 'success', 'atividades': atividades}
        else:
            return {'status': 'error', 'message': 'Ação desconhecida'}

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()
