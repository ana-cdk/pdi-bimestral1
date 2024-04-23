import cv2 as cv
from tkinter import *
from tkinter import filedialog 
from PIL import Image, ImageTk
from tkinter import messagebox
import numpy as np

tela = Tk()
tela.title("Trabalho Bimestral PDI")
tela.config(bg='#ffdbd7')
tela.resizable(False, False) 
fonte = ("Verdana", 9)

imagem_atual = None
transformacoes_realizadas = []

#Definir o tamanho da janela
largura_tela = tela.winfo_screenwidth() - 100
altura_tela = tela.winfo_screenheight() - 150

largura_frame = largura_tela // 2
altura_frame = altura_tela // 2

# Dividir a tela em quatro partes
frame_superior_esquerdo = Frame(tela, width=largura_frame-1, height=altura_frame-3, bg="#ffffff")
frame_superior_esquerdo.grid(row=0, column=0, sticky="nw", padx=(0, 1), pady=(0, 3))

frame_superior_direito = Frame(tela, width=largura_frame-1, height=altura_frame-3, bg="#ffffff")
frame_superior_direito.grid(row=0, column=1, sticky="ne", padx=(1, 0), pady=(0, 3))

frame_inferior_esquerdo = Frame(tela, width=largura_frame, height=altura_frame, bg="#f7f1e1")
frame_inferior_esquerdo.grid(row=1, column=0, sticky="sw")

frame_inferior_direito = Frame(tela, width=largura_frame, height=altura_frame, bg="#f7f1e1")
frame_inferior_direito.grid(row=1, column=1)

imagem_original = frame_superior_esquerdo

# Novo frame para conter a lista e o botão
frame_lista_e_botao = Frame(frame_inferior_direito, bg="#f7f1e1")
frame_lista_e_botao.pack(side="top", expand=True, fill="both")

# Lista de transformações
lista_transformacoes = Listbox(frame_lista_e_botao, width=83, height=23, font=fonte)
lista_transformacoes.pack(side="left", expand=True, fill="both")

def adicionar_transformacao(transformacao):
    transformacoes_realizadas.append(transformacao)
    atualizar_lista_transformacoes()

def atualizar_lista_transformacoes():
    lista_transformacoes.delete(0, END)
    for transformacao in transformacoes_realizadas:
        lista_transformacoes.insert(END, transformacao)

def atualizar_imagem_atual():
    global imagem_atual
    imagem_atual = imagem_cv.copy()
    for transformacao in transformacoes_realizadas:
        if transformacao == "Conversão de cores BGR -> GRAY":
            if len(imagem_atual.shape) > 2 and imagem_atual.shape[2] > 1:
                imagem_atual = cv.cvtColor(imagem_atual, cv.COLOR_BGR2GRAY)
        elif transformacao == "Filtro gaussiano - Blur":
            if len(imagem_atual.shape) > 2 and imagem_atual.shape[2] > 1:
                imagem_atual = cv.GaussianBlur(imagem_atual, (5, 5), 0)
        elif transformacao == "Detector de borda - Canny":
            imagem_atual = cv.Canny(imagem_atual, 50, 200)
        elif transformacao == "Binarização":
            _, imagem_atual = cv.threshold(imagem_atual, 127, 255, cv.THRESH_BINARY)
        elif transformacao == "Morfologia matemática - Erosão":
            kernel = np.ones((5, 5), np.uint8)
            imagem_atual = cv.erode(imagem_atual, kernel, iterations=1)

def excluir_transformacao():
    global imagem_original
    indices_selecionados = lista_transformacoes.curselection()
    for i in reversed(indices_selecionados):
        del transformacoes_realizadas[i]
    atualizar_lista_transformacoes()
    atualizar_imagem_atual()
    imagem_pil = Image.fromarray(imagem_atual)
    redimensionar_imagem_para_frame(imagem_pil, frame_superior_direito, largura_frame, altura_frame)


def redimensionar_imagem_para_frame(imagem_pil, frame, largura_frame, altura_frame):
    proporcao = min(largura_frame / imagem_pil.width, altura_frame / imagem_pil.height)
    nova_largura = int(imagem_pil.width * proporcao)
    nova_altura = int(imagem_pil.height * proporcao)
    imagem_redimensionada = imagem_pil.resize((nova_largura, nova_altura))

    imagem_tk = ImageTk.PhotoImage(imagem_redimensionada)

    label_imagem = Label(frame, image=imagem_tk)
    label_imagem.imagem_tk = imagem_tk
    x = (largura_frame - nova_largura) // 2
    y = (altura_frame - nova_altura) // 2
    label_imagem.place(x=x, y=y)

    return label_imagem

def abrir_arquivo():
    global label_imagem_anterior
    global imagem_cv
    global imagem_atual

    # Limpar os frames antes de abrir uma nova imagem
    for widget in frame_superior_esquerdo.winfo_children():
        widget.destroy()
    for widget in frame_superior_direito.winfo_children():
        widget.destroy()

    transformacoes_realizadas.clear()
    atualizar_lista_transformacoes()

    filename = filedialog.askopenfilename(title="Abrir Imagem", filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
    if filename:
        imagem_cv = cv.imread(filename)
        imagem_cv = cv.cvtColor(imagem_cv, cv.COLOR_RGB2BGR)
        imagem_atual = imagem_cv
        imagem_pil = Image.fromarray(imagem_cv)

        label_imagem_esquerda = redimensionar_imagem_para_frame(imagem_pil, frame_superior_esquerdo, largura_frame, altura_frame)
        label_imagem_direita = redimensionar_imagem_para_frame(imagem_pil, frame_superior_direito, largura_frame, altura_frame)

        # Atualizar a referência da imagem anterior
        label_imagem_anterior = label_imagem_esquerda
    return filename


def salvar_arquivo():
    if imagem_atual is not None:
        filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if filename:
            cv.imwrite(filename, cv.cvtColor(imagem_atual, cv.COLOR_RGB2BGR))
            messagebox.showinfo("Sucesso", "Imagem salva com sucesso!")

def converter_img():
    global imagem_atual
    if imagem_atual is None:
        messagebox.showinfo("Erro", "Escolha uma imagem primeiro")
    else:
        if len(imagem_atual.shape) > 2 and imagem_atual.shape[2] > 1:
            imagem_atual = cv.cvtColor(imagem_atual, cv.COLOR_BGR2GRAY)
            edit_pil = Image.fromarray(imagem_atual)
            redimensionar_imagem_para_frame(edit_pil, frame_superior_direito, largura_frame, altura_frame)
            adicionar_transformacao("Conversão de cores BGR -> GRAY")
        else:
            messagebox.showinfo("Erro", "A imagem atual não pode ser convertida para escala de cinza pois já está convertida.")

def filtro_img():
    global imagem_atual
    if imagem_atual is None:
        messagebox.showinfo("Erro", "Escolha uma imagem primeiro")
    else:
        edit = cv.GaussianBlur(imagem_atual, (5, 5), 0)
        imagem_atual = edit  # Atualiza a imagem atual para a imagem filtrada
        edit_pil = Image.fromarray(edit)
        redimensionar_imagem_para_frame(edit_pil, frame_superior_direito, largura_frame, altura_frame)
        adicionar_transformacao("Filtro gaussiano - Blur")

def detector_borda():
    global imagem_atual
    if imagem_atual is None:
        messagebox.showinfo("Erro", "Escolha uma imagem primeiro")
    else:
        edit = cv.Canny(imagem_atual, 50, 200)
        imagem_atual = edit  # Atualiza a imagem atual para a imagem filtrada
        edit_pil = Image.fromarray(edit)
        redimensionar_imagem_para_frame(edit_pil, frame_superior_direito, largura_frame, altura_frame)
        adicionar_transformacao("Detector de borda - Canny")

def binarizar_img():
    global imagem_atual
    if imagem_atual is None:
        messagebox.showinfo("Erro", "Escolha uma imagem primeiro")
    else:
        _, edit = cv.threshold(imagem_atual, 127, 255, cv.THRESH_BINARY)
        imagem_atual = edit  # Atualiza a imagem atual para a imagem binarizada
        edit_pil = Image.fromarray(edit)
        redimensionar_imagem_para_frame(edit_pil, frame_superior_direito, largura_frame, altura_frame)
        adicionar_transformacao("Binarização")

def morfologia():
    global imagem_atual
    if imagem_atual is None:
        messagebox.showinfo("Erro", "Escolha uma imagem primeiro")
    else:
        kernel = np.ones((5,5), np.uint8)
        edit = cv.erode(imagem_atual, kernel, iterations=1)
        imagem_atual = edit  # Atualiza a imagem atual para a imagem binarizada
        edit_pil = Image.fromarray(edit)
        redimensionar_imagem_para_frame(edit_pil, frame_superior_direito, largura_frame, altura_frame)
        adicionar_transformacao("Morfologia matemática - Erosão")

def barra_de_ferramentas():
    toolbar = Menu(tela)

    submenu_arquivo = Menu(toolbar, tearoff=0, font=fonte)
    submenu_arquivo.add_command(label="Abrir", command=abrir_arquivo)
    submenu_arquivo.add_command(label="Salvar", command=salvar_arquivo)

    toolbar.add_cascade(label="Arquivo", menu=submenu_arquivo)
    btnSair = toolbar.add_command(label="Sair", command=tela.quit)

    tela.config(menu=toolbar)

def botoes_pdi():

    # Adicionar botões no frame inferior esquerdo
    btnConv = Button(frame_inferior_esquerdo, text="Conversão de cores BGR -> GRAY", bg='#ffdbd7', width=35, height=2, font=fonte, command=converter_img)
    btnConv.place(relx=0.5, rely=0.2, anchor=CENTER)  # Coloca o botão no centro horizontal, 20% do topo

    btnFilt = Button(frame_inferior_esquerdo, text="Filtro Blur", bg='#ffb2c1', width=35, height=2, font=fonte, command=filtro_img)
    btnFilt.place(relx=0.5, rely=0.35, anchor=CENTER)  # Coloca o botão no centro horizontal, 35% do topo

    btnDetec = Button(frame_inferior_esquerdo, text="Detector de borda", bg='#ce7095', width=35, height=2, font=fonte, command=detector_borda)
    btnDetec.place(relx=0.5, rely=0.50, anchor=CENTER)  # Coloca o botão no centro horizontal, 50% do topo

    btnBin = Button(frame_inferior_esquerdo, text="Binarização", bg='#906f8d', width=35, height=2, font=fonte, command=binarizar_img)
    btnBin.place(relx=0.5, rely=0.65, anchor=CENTER)  # Coloca o botão no centro horizontal, 65% do topo

    btnMorf = Button(frame_inferior_esquerdo, text="Morfologia matemática", bg='#744c71', width=35, height=2, font=fonte, command=morfologia)
    btnMorf.place(relx=0.5, rely=0.8, anchor=CENTER)  # Coloca o botão no centro horizontal, 80% do topo


def botoes_lista():

    # Carregar a imagem do ícone
    icone = Image.open("D:/Faculdade/PDI/Trabalho bimestral 1/icons/trash.png")
    icone = icone.resize((25, 25))  # Redimensionar o ícone se necessário
    icone = ImageTk.PhotoImage(icone)
    # Botão de excluir
    btnExcluir = Button(frame_lista_e_botao, bg='#ffb2c1', width=25, height=25, font=fonte, command=excluir_transformacao, image=icone, compound=LEFT)
    btnExcluir.image = icone
    btnExcluir.pack(side="left", padx=10, pady=10)
    

barra_de_ferramentas()
botoes_pdi()
botoes_lista()

#imagem_original = frame_superior_esquerdo

tela.mainloop()