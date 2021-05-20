"""
Cadastro de produtos:

    O Cadastro de Produtos é um software com a finalidade de cadastrar apenas o
produto e seu preço em banco de dados usando o sqlite3.
    Inclui-se também além de visualizar os produtos cadastrados a função de
editar, e excluir cada produto individualmente.
    O programa inteiro foi construido usando a linguagem Python e o Tkinter
"""
from tkinter import ttk as tk
from tkinter import *
from ttkthemes import ThemedTk
from tkinter import messagebox as mb
import sqlite3
from sqlite3 import Error

class Cadastro_Produtos():
    """ Classe principal - chama a janela window com todos os widgets. """
    db_name = 'database.db'
    def __init__(self):
        """ Inicializador da janela principal. """
        self.window = ThemedTk(theme='plastik')
        self.window.title("Cadastro de Produtos em Tkinter")
        self.window.resizable(0, 0)
        self.window.geometry(self.centraliza_window(568, 500))

        self.frame_principal = tk.Frame(self.window)
        self.frame_principal.pack(fill=BOTH)

        self.label_espaco = tk.Label(self.frame_principal)
        self.label_espaco.grid(row=0, column=1, pady=4)

        self.label_nome = tk.Label(self.frame_principal, text='Nome do produto:')
        self.label_nome.grid(row=1, column=1, padx=10)

        self.entry_nome = tk.Entry(self.frame_principal, width=45)
        self.entry_nome.grid(row=1, column=2, pady=4)
        self.entry_nome.focus()

        self.label_preco = tk.Label(self.frame_principal, text='Preço do produto:')
        self.label_preco.grid(row=2, column=1, padx=10)

        self.entry_preco = tk.Entry(self.frame_principal, width=10)
        self.entry_preco.grid(row=2, column=2, pady=4, sticky=W)

        self.button_cadastrar = tk.Button(self.frame_principal, text='CADASTRAR', width=15, command=lambda:self.adicionar(self))
        self.button_cadastrar.grid(row=2, column=2, padx=5, pady=15, sticky=E)
        self.button_cadastrar.bind('<Return>', self.adicionar)

        self.separator = tk.Separator(self.window, orient='horizontal')
        self.separator.pack(fill='x')

        self.frame_pesquisar = tk.Frame(self.window)
        self.frame_pesquisar.pack(fill='x')

        self.frame_espaco = tk.Frame(self.frame_pesquisar)
        self.frame_espaco.pack(pady=30)

        self.label_pesquisar = tk.Label(self.frame_pesquisar, text='Pesquisar:').pack(side=LEFT, padx=20)

        self.entry_pesquisar = tk.Entry(self.frame_pesquisar, width=30)
        self.entry_pesquisar.pack(pady=10, side=LEFT)

        self.button_pesquisar = tk.Button(self.frame_pesquisar, text='Ok', command=self.pesquisar)
        self.button_pesquisar.pack(side=LEFT, padx=5)

        self.button_limpar = tk.Button(self.frame_pesquisar, text='Limpar', command=self.limpar)
        self.button_limpar.pack(side=LEFT, padx=5)

        self.frame_treeview = tk.Frame(self.window)
        self.frame_treeview.pack(fill='x')

        self.treeview = tk.Treeview(self.frame_treeview, columns=('id', "produto", 'preco'), show='headings')
        self.treeview.column('id', minwidth=0, width=30)
        self.treeview.column('produto', minwidth=0, width=250)
        self.treeview.column('id', minwidth=0, width=100)
        self.treeview.heading('id', text='ID')
        self.treeview.heading('produto', text='PRODUTO')
        self.treeview.heading('preco', text='PREÇO')
        self.treeview.grid(row=1, column=1)

        # scrollbar
        self.scrollbar = tk.Scrollbar(self.frame_treeview, orient="vertical", command=self.treeview.yview)
        self.scrollbar.grid(row=1, column=2, ipady=76)

        self.treeview.configure(yscrollcommand=self.scrollbar.set)

        self.frame_botoes = tk.Frame(self.window)
        self.frame_botoes.pack(side=BOTTOM, pady=10)

        self.button_excluir = tk.Button(self.frame_botoes, text='EXCLUIR', width=15, command=self.deletar)
        self.button_excluir.pack(side=LEFT)

        self.button_editar = tk.Button(self.frame_botoes, text='EDITAR', width=15, command=self.window_editar)
        self.button_editar.pack(side=LEFT, padx=5)

        self.button_sair = tk.Button(self.frame_botoes, text='SAIR', width=15, command=lambda:self.window.destroy())
        self.button_sair.pack(side=LEFT)

        self.visualizar_registros()

        self.window.mainloop()


    def executa_banco(self, query, parameters=()):
        """
        Executa o banco de dados, o mesmo leva duas variáveis.

        query - instrução para executar o banco de dados,
        ex.: 'SELECT * FROM product ORDER BY id'.
        parameters - recebe os parametros para a execução da query; parameters
        é uma tupla.
        """
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            query_result = cursor.execute(query, parameters)
            conn.commit()
            return query_result

    def visualizar_registros(self):
        """ Pega todos os registros e coloca dentro da Treeview """
        records = self.treeview.get_children()
        for element in records:
            self.treeview.delete(element)
        query = 'SELECT * FROM product ORDER BY id'
        db_rows = self.executa_banco(query)
        for row in db_rows:
            self.treeview.insert('', 'end', text=row[0], values=(row[0], row[1], row[2]))
        self.entry_pesquisar.delete(0, END)

    def validar(self):
        """ Verifica se as duas entradas não estão vazias """
        return len(self.entry_nome.get()) != 0 and len(self.entry_preco.get()) != 0

    def pesquisar(self):
        """ Realiza a pesquisa usando o método LIKE do SQL """
        parameters = (self.entry_pesquisar.get() + '%',)
        query = 'SELECT * FROM product WHERE name LIKE ?'
        db_rows = self.executa_banco(query, parameters)
        records = self.treeview.get_children()
        for element in records:
            self.treeview.delete(element)
        for row in db_rows:
            self.treeview.insert('', 'end', text=row[0], values=(row[0], row[1], row[2]))

    def limpar(self):
        """ Limpa a entry pesquisar. """
        self.entry_pesquisar.delete(0, END)
        self.visualizar_registros()

    def adicionar(self, event):
        """ Adiciona nova entrada no banco de dados. """
        if self.validar():
            query = 'INSERT INTO product VALUES(NULL, ?, ?)'
            name = self.entry_nome.get().title()
            price = self.entry_preco.get()
            parameters = (name, price)
            self.executa_banco(query, parameters)
            self.entry_nome.delete(0, END)
            self.entry_preco.delete(0, END)
            self.mensagem('info', 'Atenção', 'Produto {} cadastrado:'.format(self.entry_nome.get()))
        else:
            self.mensagem('erro', 'Atenção', 'Favor preencher todos os campos.')
            self.entry_nome.focus()
        self.entry_nome.focus()
        self.visualizar_registros()

    def deletar(self):
        """ Deleta o item selecionado na Treeview. """
        if not self.treeview.item(self.treeview.selection())['text']:
            self.mensagem('erro', 'Atenção', 'Selecione um item para excluir.')
        else:
            name_item = self.treeview.item(self.treeview.selection())['values']
            msgBox = mb.askquestion('Atenção', 'Tem certeza que deseja excluir "{}"? Este processo é irreversível.'.format(name_item[1]))
            if msgBox == 'no':
                pass
            else:
                id = self.treeview.item(self.treeview.selection())['text']
                query = 'DELETE FROM product WHERE id = ?'
                self.executa_banco(query, (id,))
                self.visualizar_registros()
                self.mensagem('info', 'Atenção', '{} deletado.'.format(name_item[1]))


    def window_editar(self):
        """ Chama a janela de edição. """
        if not self.treeview.item(self.treeview.selection())['text']:
            self.mensagem('erro', 'Atenção', 'Selecione um item para editar.')
        else:
            selecao = self.treeview.item(self.treeview.selection())['values']
            id = selecao[0]
            name = selecao[1]
            price = selecao[2]
            self.edit_wind = Toplevel()
            self.edit_wind.title('Editando "{}"'.format(name))
            self.edit_wind.geometry('550x170')
            self.edit_wind.transient(self.window)
            self.edit_wind.focus_force()
            self.edit_wind.grab_set()

            self.frame_principal = tk.Frame(self.edit_wind)
            self.frame_principal.pack(fill=BOTH)

            self.label_espaco = tk.Label(self.frame_principal)
            self.label_espaco.grid(row=0, column=1, pady=4)

            self.label_nome = tk.Label(self.frame_principal, text='Nome do produto:')
            self.label_nome.grid(row=1, column=1, padx=10)

            self.entry_nome = tk.Entry(self.frame_principal, width=45)
            self.entry_nome.grid(row=1, column=2, pady=4)
            self.entry_nome.focus()

            self.label_preco = tk.Label(self.frame_principal, text='Preço do produto:')
            self.label_preco.grid(row=2, column=1, padx=10)

            self.entry_preco = tk.Entry(self.frame_principal, width=10)
            self.entry_preco.grid(row=2, column=2, pady=4, sticky=W)

            self.button_salvar = tk.Button(self.frame_principal, text='SALVAR', width=15, command=self.editar_registros)
            self.button_salvar.grid(row=5, column=1)
            #self.button_salvar.bind('<Return>', self.editar_registros)

            self.button_cancelar = tk.Button(self.frame_principal, text='CANCELAR', width=15, command=lambda:self.edit_wind.destroy())
            self.button_cancelar.grid(row=5, column=2, pady=30, sticky=W)

            self.entry_nome.insert(0, name)
            self.entry_preco.insert(0, price)

    def editar_registros(self):
        """ Substitui no banco de dados o registro anterior selecionado pelo registro editado. """
        selecao = self.treeview.item(self.treeview.selection())['values']
        id = selecao[0]
        name = selecao[1]
        old_price = selecao[2]
        new_name = self.entry_nome.get().title()
        new_price = self.entry_preco.get()
        parameters = (new_name, new_price, name, old_price)
        query = 'UPDATE product SET name=?, price=? WHERE name=? AND price=?'
        self.executa_banco(query, parameters)
        self.edit_wind.destroy()
        self.mensagem('info', 'Atenção', 'Cadastro "{}" editado com sucesso!'.format(name))
        self.visualizar_registros()

    def mensagem(self, tipoMsg, title, msg):
        """ Exibe mensagens de alerta ao usuário, o mesmo pode ser de erro ou atenção. """
        if tipoMsg == "erro":
            mb.showerror(title, msg)
        else:
            mb.showinfo(title, msg)

    def centraliza_window(self, comprimento, altura):
        """
        Dimensiona e centraliza a janela.

        recebe duas variáveis:
        comprimento - a largura da janela
        altura - a altura da janela
        """
        # Dimensões da janela
        self.comprimento = comprimento
        self.altura = altura
        # Resolução da tela
        self.comprimento_screen = self.window.winfo_screenwidth()
        self.altura_screen = self.window.winfo_screenheight()
        # Posição da janela
        self.pos_x = (self.comprimento_screen / 2) - (self.comprimento / 2)
        self.pos_y = (self.altura_screen / 2) - (self.altura / 2) - 10

        self.window.geometry(
            "{}x{}+{}+{}".format(
                int(self.comprimento),
                int(self.altura),
                int(self.pos_x),
                int(self.pos_y),
            )
        )

Cadastro_Produtos()
