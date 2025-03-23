import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import sqlite3
import datetime

# Banco de dados e suas tabelas
conn = sqlite3.connect('petshop.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS pets (
        id_pet INTEGER PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(30) NOT NULL,
        dono VARCHAR(30) NOT NULL,
        telefone INTEGER NOT NULL,
        cuidadosAlergias VARCHAR(200)
    )
''')
conn.commit()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS pacotes (
        id_pet INTEGER NOT NULL,
        dataInicio DATETIME NOT NULL,
        dataFim DATETIME NOT NULL
    )
''')
conn.commit()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS agendamentos (
        id_pet INTEGER NOT NULL,
        data DATETIME NOT NULL
    )
''')
conn.commit()

def cadastro_pets():
    def adicionar_pet():
        nome = entry_nome.get()
        fone = entry_fone.get()
        dono = entry_dono.get()
        cuidalerg = entry_cuidalerg.get()
        if nome and fone:
            cursor.execute('INSERT INTO pets (nome, dono, telefone, cuidadosAlergias) VALUES (?, ?, ?, ?)', (nome, dono, fone, cuidalerg))
            conn.commit()
            messagebox.showinfo('Sucesso', 'Pet adicionado!')
            entry_nome.delete(0, tk.END)
            entry_dono.delete(0, tk.END)
            entry_fone.delete(0, tk.END)
            entry_cuidalerg.delete(0, tk.END)
            listar_pets()
        else:
            messagebox.showwarning('Atenção', 'Preencha todos os campos!')

    def listar_pets():
        listbox_pets.delete(0, tk.END)
        cursor.execute('SELECT id_pet, nome, dono, telefone, cuidadosAlergias FROM pets')
        for row in cursor.fetchall():
            listbox_pets.insert(tk.END, f'ID: {row[0]} | Nome: {row[1]} | Fone: {row[2]} | Telefone: {row[3]} | Cuidados e alergias: {row[4]}')

    def deletar_pet():
        selecao = listbox_pets.curselection()
        if selecao:
            item = listbox_pets.get(selecao)
            id_pet = int(item.split('|')[0].split(':')[1].strip())
            cursor.execute('DELETE FROM pets WHERE id_pet = ?', (id_pet,))
            conn.commit()
            messagebox.showinfo('Sucesso', 'Pet deletado!')
            listar_pets()
        else:
            messagebox.showwarning('Atenção', 'Selecione um usuário para deletar.')

# Interface gráfica

    root = tk.Toplevel()
    root.title('Gerenciador de Pets')

    tk.Label(root, text='Nome:').grid(row=0, column=0)
    entry_nome = tk.Entry(root)
    entry_nome.grid(row=0, column=1)

    tk.Label(root, text='Dono:').grid(row=0, column=2)
    entry_dono = tk.Entry(root)
    entry_dono.grid(row=0, column=3)

    tk.Label(root, text='Telefone:').grid(row=0, column=4)
    entry_fone = tk.Entry(root)
    entry_fone.grid(row=0, column=5)

    tk.Label(root, text='Cuidados e Alergias:').grid(row=1, column=0)
    entry_cuidalerg = tk.Entry(root, width=75)
    entry_cuidalerg.grid(row=1, column=1, columnspan=5)

    btn_adicionar = tk.Button(root, text='Adicionar', command=adicionar_pet)
    btn_adicionar.grid(row=2, column=3, columnspan=2)

    listbox_pets = tk.Listbox(root, width=90)
    listbox_pets.grid(row=3, columnspan=6)

    btn_deletar = tk.Button(root, text='Deletar', command=deletar_pet)
    btn_deletar.grid(row=4, column=3, columnspan=2)

    listar_pets()

    root.mainloop()

def administrar_pacotes():
    def adicionar_pacote():
        id = entry_id.get()
        dataInicioNF = entry_dataInicioNF.get()
        dataInicio = datetime.datetime.strptime(dataInicioNF, '%d/%m/%Y').strftime('%Y-%m-%d')
        dataFimNF = entry_dataFimNF.get()
        dataFim = datetime.datetime.strptime(dataFimNF, '%d/%m/%Y').strftime('%Y-%m-%d')
        if id and dataInicio and dataFim:
            cursor.execute('INSERT INTO pacotes (id_pet, dataInicio, dataFim) VALUES (?, ?, ?)', (id, dataInicio, dataFim))
            conn.commit()
            messagebox.showinfo('Sucesso', 'Pacote adicionado!')
            entry_id.delete(0, tk.END)
            entry_dataInicioNF.delete(0, tk.END)
            entry_dataFimNF.delete(0, tk.END)
            listar_pacotes()
        else:
            messagebox.showwarning('Atenção', 'Preencha todos os campos!')

    def listar_pacotes():
        listbox_pacotes.delete(0, tk.END)
        cursor.execute('SELECT id_pet, dataInicio, dataFim FROM pacotes')
        for row in cursor.fetchall():
            listbox_pacotes.insert(tk.END, f'ID: {row[0]} | Data de Início: {row[1]} | Data do Fim: {row[2]}')

    def deletar_pacote():
        selecao = listbox_pacotes.curselection()
        if selecao:
            item = listbox_pacotes.get(selecao)
            id_pet = int(item.split('|')[0].split(':')[1].strip())
            cursor.execute('DELETE FROM pacotes WHERE id = ?', (id_pet,))
            conn.commit()
            messagebox.showinfo('Sucesso', 'Pacote deletado!')
            listar_pacotes()
        else:
            messagebox.showwarning('Atenção', 'Selecione um pacote para deletar.')

# Interface gráfica

    root = tk.Toplevel()
    root.title('Administração de Pacotes')

    tk.Label(root, text='ID:').grid(row=0, column=0)
    entry_id = tk.Entry(root)
    entry_id.grid(row=0, column=1)

    tk.Label(root, text='Data do Início:').grid(row=0, column=2)
    entry_dataInicioNF = tk.Entry(root)
    entry_dataInicioNF.grid(row=0, column=3)

    tk.Label(root, text='Fim do Pacote:').grid(row=0, column=4)
    entry_dataFimNF = tk.Entry(root)
    entry_dataFimNF.grid(row=0, column=5)

    btn_adicionar = tk.Button(root, text='Adicionar', command=adicionar_pacote)
    btn_adicionar.grid(row=2, column=3, columnspan=2)

    listbox_pacotes = tk.Listbox(root, width=90)
    listbox_pacotes.grid(row=3, columnspan=6)

    btn_deletar = tk.Button(root, text='Deletar', command=deletar_pacote)
    btn_deletar.grid(row=4, column=3, columnspan=2)

    listar_pacotes()

    root.mainloop()

def marcar_horarios():
    def adicionar_horario():
        id = entry_id.get()
        hora = spin_hora.get()
        minuto = spin_minuto.get()
        if id and hora and minuto:
            hora_formatada = f"{int(hora):02}:{int(minuto):02}:00"
            cursor.execute('INSERT INTO agendamentos (id_pet, data) VALUES (?, ?)', (id, hora_formatada))
            conn.commit()
            messagebox.showinfo('Sucesso', 'Horário Marcado!')
            entry_id.delete(0, tk.END)
            listar_horarios()
        else:
            messagebox.showwarning('Atenção', 'Preencha todos os campos!')

    def listar_horarios():
        listbox_horarios.delete(0, tk.END)
        cursor.execute('SELECT id_pet, data FROM agendamentos')
        for row in cursor.fetchall():
            listbox_horarios.insert(tk.END, f'ID: {row[0]} | Data de Início: {row[1]} | Data do Fim: {row[2]}')

    def deletar_horario():
        selecao = listbox_horarios.curselection()
        if selecao:
            item = listbox_horarios.get(selecao)
            id_pet = int(item.split('|')[0].split(':')[1].strip())
            cursor.execute('DELETE FROM agendamentos WHERE id = ?', (id_pet,))
            conn.commit()
            messagebox.showinfo('Sucesso', 'Horario Desmarcado!')
            listar_horarios()
        else:
            messagebox.showwarning('Atenção', 'Selecione um pacote para deletar.')
            
    root = tk.Toplevel()
    root.title('Agendamentos')
    
    tk.Label(root, text='ID:').grid(row=0, column=0)
    entry_id = tk.Entry(root)
    entry_id.grid(row=0, column=1)
    
    tk.Label(root, text='Escolha a Data:').grid(row=2, column=0)
    calendario = DateEntry(root, date_pattern='dd/mm/yyyy')
    calendario.grid(row=1, column=0)

    tk.Label(root, text='Hora:').grid(row=3, column=0)
    frame_hora = tk.Frame(root)
    frame_hora.grid(row=1, column=1)
    
    spin_hora = tk.Spinbox(frame_hora, from_=0, to=23, width=5, format='%02.0f')
    spin_hora.pack(side=tk.LEFT)
    tk.Label(frame_hora, text=':').pack(side=tk.LEFT)
    spin_minuto = tk.Spinbox(frame_hora, from_=0, to=59, width=5, format='%02.0f')
    spin_minuto.pack(side=tk.LEFT)
    
    btn_adicionar = tk.Button(root, text='Adicionar', command=adicionar_horario)
    btn_adicionar.grid(row=2, column=3, columnspan=2)

    listbox_horarios = tk.Listbox(root, width=90)
    listbox_horarios.grid(row=3, columnspan=6)

    btn_deletar = tk.Button(root, text='Deletar', command=deletar_horario)
    btn_deletar.grid(row=4, column=3, columnspan=2)

root = tk.Tk()
root.title('Gerenciamento de PetShop')

btn_adicionar = tk.Button(root, text='Adicionar/Remover Pet', command=cadastro_pets, width=50)
btn_adicionar.grid(row=0, column=0, columnspan=2)

btn_adicionar = tk.Button(root, text='Administar Pacotes', command=administrar_pacotes, width=50)
btn_adicionar.grid(row=1, column=0, columnspan=2)

btn_adicionar = tk.Button(root, text='Horários', command=marcar_horarios, width=50)
btn_adicionar.grid(row=2, column=0, columnspan=2)

root.mainloop()

conn.close()
