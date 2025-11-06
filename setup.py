import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from database import Database
from PIL import Image, ImageTk
import os

class SetupApp:
    def __init__(self):
        self.db = Database()
        self.root = tk.Tk()
        self.root.title("Configuração do BrainTech")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        # Caminhos automáticos
        base_dir = os.path.dirname(os.path.abspath(__file__))
        img_dir = os.path.join(base_dir, "imagens")
        icon_path = os.path.join(img_dir, "braintech.ico")
        bg_path = os.path.join(img_dir, "bg-login.png")
        logo_path = os.path.join(img_dir, "braintech.png")

        # Ícone da janela
        try:
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"⚠️ Erro ao carregar ícone: {e}")

        # Fundo com imagem
        try:
            bg_image = Image.open(bg_path)
            bg_image = bg_image.resize((600, 400))
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            self.bg_label = tk.Label(self.root, image=self.bg_photo)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"⚠️ Erro ao carregar fundo: {e}")
            self.root.configure(bg="#ffffff")

        # Estilos
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 11, "bold"), padding=6)
        style.configure("TLabel", background="black", foreground="white", font=("Arial", 12))
        
        # Logo superior
        try:
            logo_image = Image.open(logo_path)
            logo_image = logo_image.resize((130, 50))
            self.logo_photo = ImageTk.PhotoImage(logo_image)
            logo_label = tk.Label(self.root, image=self.logo_photo, bg="black")
            logo_label.place(relx=0.5, rely=0.05, anchor="n")
        except Exception as e:
            print(f"⚠️ Erro ao carregar logo: {e}")

        # Criar tela inicial
        self.create_setup_screen()

    def create_setup_screen(self):
        self.clear_screen()

        # Frame semi-transparente para o conteúdo
        frame = tk.Frame(self.root, bg="white")  # transparência simulada
        frame.place(relx=0.5, rely=0.55, anchor="center")

        title = tk.Label(
            frame,
            text="Configuração do BrainTech",
            font=("Arial", 18, "bold"),
            bg="#FFFFFF",
            fg="black"
        )
        title.pack(pady=15)

        subtitle = tk.Label(
            frame,
            text="Gerenciar Usuários",
            font=("Arial", 13),
            bg="#FFFFFF",
            fg="black"
        )
        subtitle.pack(pady=5)

        # Botões
        ttk.Button(frame, text="Adicionar Usuário", command=self.add_user).pack(pady=5, fill=tk.X)
        ttk.Button(frame, text="Listar/Excluir Usuários", command=self.list_users).pack(pady=5, fill=tk.X)
        ttk.Button(frame, text="Concluir Configuração", command=self.finish_setup).pack(pady=10, fill=tk.X)

    def add_user(self):
        username = simpledialog.askstring("Adicionar Usuário", "Nome de usuário:")
        if username:
            password = simpledialog.askstring("Adicionar Usuário", "Senha:", show="*")
            if password:
                email = simpledialog.askstring("Adicionar Usuário", "Email:")
                if email:
                    role = simpledialog.askstring("Adicionar Usuário", "Função (Professor/aluno):").lower()
                    if role == 'professor':
                        role = 'Professor'
                    elif role == 'aluno':
                        role = 'aluno'
                    if role in ['Professor', 'aluno']:
                        try:
                            self.db.add_user(username, password, role, email)
                            messagebox.showinfo("Sucesso", f"Usuário {username} criado com sucesso.")
                        except Exception as e:
                            messagebox.showerror("Erro", f"Erro ao criar usuário: {e}")
                    else:
                        messagebox.showerror("Erro", "Função inválida. Use 'Professor' ou 'aluno'.")
            else:
                messagebox.showerror("Erro", "Senha obrigatória.")
        else:
            messagebox.showerror("Erro", "Nome de usuário obrigatório.")

    def list_users(self):
        users = self.db.get_all_users()
        if users:
            user_list = "\n".join([f"ID: {u[0]}, Usuário: {u[1]}, Email: {u[4]}, Função: {u[3]}" for u in users])
            user_choice = simpledialog.askstring(
                "Listar/Excluir Usuários",
                f"Usuários:\n{user_list}\n\nDigite o ID do usuário para excluir (ou deixe em branco para voltar):"
            )
            if user_choice and user_choice.isdigit():
                user_id = int(user_choice)
                if any(u[0] == user_id for u in users):
                    confirm = messagebox.askyesno("Confirmar Exclusão", f"Deseja excluir o usuário ID {user_id}?")
                    if confirm:
                        try:
                            self.db.delete_user(user_id)
                            messagebox.showinfo("Sucesso", "Usuário excluído com sucesso.")
                        except Exception as e:
                            messagebox.showerror("Erro", f"Erro ao excluir: {e}")
                else:
                    messagebox.showerror("Erro", "ID inválido.")
        else:
            messagebox.showinfo("Info", "Nenhum usuário encontrado.")

    def finish_setup(self):
        messagebox.showinfo("Configuração", "Configuração concluída.")
        self.root.quit()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            if not isinstance(widget, tk.Label) or not hasattr(widget, "image"):
                widget.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = SetupApp()
    app.run()
