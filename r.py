from tkinter import *

janela = Tk()

def __init__():
    pass

def ok():
    nick = str(CaixaDeEntrada1.get())
    patente = str(CaixaDeEntrada2.get())
    pagpromocao = str(CaixaDeEntrada3.get())
    Linha_Entry_1 = nick
    Linha_Entry_2 = patente
    Linha_Entry_3 = pagpromocao
    print (Linha_Entry_1)
    print (Linha_Entry_2)
    print (Linha_Entry_3)
    CaixaDeEntrada3['bg'] = 'white'
    if nick in ' ':
        CaixaDeEntrada1['bg'] = 'pink'
        erro['text'] = 'Preencha todos os campos!'
    else:
        CaixaDeEntrada1['bg'] = 'white'
    if patente in ' ':
        CaixaDeEntrada2['bg'] = 'pink'
        erro['text'] = 'Preencha todos os campos!'
    else:
        CaixaDeEntrada2['bg'] = 'white'
    if pagpromocao in ' ':
        CaixaDeEntrada3['bg'] = 'pink'
        erro['text'] = 'Preencha todos os campos!'
    else:
        CaixaDeEntrada3['bg'] = 'white'
    if nick != '' and patente != '' and pagpromocao != '':
        janela.destroy()


#==========================================Janela Inicial:

titulo1 = Label(bg='#191970', font=('Arial', '14', 'bold'), fg='white', text='BEM VINDO ao RELATÓRIOS DIC')
titulo1.place(x='13', y='10')

CaixaDeEntrada1 = Entry(width=25, bg='white', font=('Comic Sans MS', '10'))
CaixaDeEntrada1.place(x=130, y=50)
Info1 = Label(font=('Arial', '11', 'bold'), fg='white', bg='#191970', text='Nick:')
Info1.place(x=10, y=50)

CaixaDeEntrada2 = Entry(width=25, bg='white', font=('Comic Sans MS', '10'))
CaixaDeEntrada2.place(x=130, y=75)
Info2 = Label(font=('Arial', '11', 'bold'), fg='white', bg='#191970', text='Patente:')
Info2.place(x=10, y=75)

CaixaDeEntrada3 = Entry(width=25, bg='white', font=('Comic Sans MS', '10'))
CaixaDeEntrada3.place(x=130, y=100)
Info3 = Label(font=('Arial', '11', 'bold'), fg='white', bg='#191970', text='Pág. Promoção:')
Info3.place(x=10, y=100)

erro = Label(bg='#191970', fg='red', font=('Arial', '11'), text='')
erro.place(x=135, y=125)

proximo = Button(width='39', text='Próximo', font=('Arial','10'), command=ok)
proximo.place(x=15, y=150)


#=======================================FimDaJanelaInicial

#Propriedades da janela:
janela.resizable(width=False, height=False)
janela.configure(bg='#191970')
#janela.wm_iconbitmap('ICO.ico')
janela.title('Relatórios DIC - Por WellersonOP')
janela.geometry('350x190+450+300')
janela.mainloop()