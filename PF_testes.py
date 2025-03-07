import sqlite3
import tkinter as tk
from tkinter import messagebox 
from tkinter import ttk


# Função para conectar ao banco de dados
def conectar():
    return sqlite3.connect('imc_usuarios.db')

# Criar a tabela no banco de dados
def criar_tabela():
    conn = conectar()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS usuarios(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            peso REAL NOT NULL,
            altura REAL NOT NULL,
            imc REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Função para calcular e salvar o IMC
def calcular_e_salvar():
        
        nome = entry_nome.get()
        peso = float(entry_peso.get())
        altura = float(entry_altura.get())
        imc = peso / (altura ** 2)
        resultado = ""

        if imc < 18.5:
            resultado = "Abaixo do peso"
        elif 18.5 <= imc < 24.9:
            resultado = "Peso normal"
        elif 25 <= imc < 29.9:
            resultado = "Sobrepeso"
        else:
            resultado = "Obesidade"

        # Salvar no banco de dados
        if nome:
            conn = conectar()
            c = conn.cursor()
            c.execute('INSERT INTO usuarios (nome, peso, altura, imc) VALUES (?, ?, ?, ?)', 
                      (nome, peso, altura, imc))
            conn.commit()
            conn.close()

            messagebox.showinfo("Resultado", f"Seu IMC é: {imc:.2f}\nClassificação: {resultado}")
            mostrar_usuarios()
        else:
            messagebox.showwarning("Aviso", "Por favor, insira o nome do usuário.")
            messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")

# Função para mostrar os usuários

def mostrar_usuarios():
    for row in tree.get_children():
        tree.delete(row)

    conn = conectar()
    c = conn.cursor()
    c.execute('SELECT * FROM usuarios')
    usuarios = c.fetchall()
    for usuario in usuarios:
        tree.insert("", "end", values=(usuario[0], usuario[1], usuario[2], usuario[3], f"{usuario[4]:.2f}"))
    conn.close()

# Função para deletar um usuário

def deletar_usuario():
    selecionado = tree.selection()
    if selecionado:
        user_id = tree.item(selecionado)['values'][0]
        conn = conectar()
        c = conn.cursor()
        c.execute('DELETE FROM usuarios WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
        mostrar_usuarios()
        messagebox.showinfo("Aviso", "Usuário deletado com sucesso!")
    else:
        messagebox.showwarning("Aviso", "Por favor, selecione um usuário para deletar.")

def editar():
     selecao = tree.selection()
     if selecao:
         user_id = tree.item(selecao)['values'][0]
         novo_nome = entry_nome.get()
         novo_peso = entry_peso.get()
         novo_altura = entry_altura.get()

         if novo_nome and novo_peso and novo_altura:
            conn = conectar()
            c = conn.cursor()    
            c.execute('UPDATE usuarios SET nome = ? , peso = ? , altura = ? WHERE id = ? ',(novo_nome,novo_peso,novo_altura,user_id))
            conn.commit()
            conn.close()  
            messagebox.showinfo('', 'DADOS ATUALIZADOS')
            mostrar_usuarios()

# Interface gráfica
root = tk.Tk()
root.title("Calculadora IMC")
root.configure(background='#3f5f5f')

# Labels e Entries
label_nome = tk.Label(root, text="Nome:")
label_nome.grid(row=0, column=0, padx=10, pady=10)

entry_nome = tk.Entry(root)
entry_nome.grid(row=0, column=1, padx=10, pady=10)

label_peso = tk.Label(root, text="Peso (kg):")
label_peso.grid(row=1, column=0, padx=10, pady=10)

entry_peso = tk.Entry(root)
entry_peso.grid(row=1, column=1, padx=10, pady=10)

label_altura = tk.Label(root, text="Altura (m):")
label_altura.grid(row=2, column=0, padx=10, pady=10)

entry_altura = tk.Entry(root)
entry_altura.grid(row=2, column=1, padx=10, pady=10)

# Button

btn_calcular = tk.Button(root, text="Calcular e Salvar", command=calcular_e_salvar)
btn_calcular.grid(row=4, column=0, columnspan=2, pady=10)

btn_deletar = tk.Button(root, text="Deletar", command=deletar_usuario)
btn_deletar.grid(row=5, column=0, columnspan=2, pady=10)

btn_atualizar = tk.Button(root, text='atualizar', command=editar)
btn_atualizar.grid(row=6, column=0, columnspan=2, pady=10)
# Exibir os usuários

columns = ("ID", "Nome", "Peso", "Altura", "IMC")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

for col in columns:
    tree.heading(col, text=col)

criar_tabela()
mostrar_usuarios()
root.mainloop()
