import window
import objetos
import viewport
from tkinter import *
from tkinter import ttk
import re
import numpy


#----------------------------------------------Janela Pricipal--------------------------------------------------------------#
#Cria a janela principal
janelaPrincipal = Tk()
janelaPrincipal.title("SGI - Arthur Lisboa e Igor May")
janelaPrincipal.geometry("730x630")
#----------------------------------------------Lado Esquerdo----------------------------------------------------------------#

#Frame do lado esquerdo (janelaPrincipal de funções)
ladoEsquerdo = Frame(janelaPrincipal)
ladoEsquerdo.grid(row=0, column=0)

#Menu de Funções
labelMenu = LabelFrame(ladoEsquerdo, text="Menu de funções", font="Helvetica 10", height = 700, width=200)
labelMenu.grid(row=0, column=0, pady = 0, padx=2)
labelObjetos = LabelFrame(labelMenu, text="Objetos", font="Helvetica 10", height = 600, width=300)
labelObjetos.grid(row=0, column=1)

#Lista de objetos com scrollbar
yScroll = Scrollbar(labelObjetos, orient=VERTICAL)
yScroll.grid(row=0, column=1)
listbox = Listbox(labelObjetos, bg="white", width="25", yscrollcommand=yScroll.set)
listbox.grid(row=0, column=0)
yScroll.config(command=listbox.yview)

#window com suas funcionalidades
labelWindow = LabelFrame(labelObjetos, text="Window", font="Helvetica 10", height = 450, width=200)
labelWindow.grid(row=1, column=0)

#Passo
passo = Label(labelWindow, text="Passo:")
entradaPasso = Entry(labelWindow)
porcentagemPasso = Label(labelWindow, text="%")
passo.place(relx=0.1, rely=0.01)
entradaPasso.place(relx=0.33, rely=0.01,relheight=0.035, relwidth=0.25)
porcentagemPasso.place(relx=0.6, rely=0.01)

#funções dos botões
def moverWindowCima():
    window.y_min += 5
    window.y_max += 5
    desenhar()

def moverWindowBaixo():
    window.y_min -= 5
    window.y_max -= 5
    desenhar()

def moverWindowDireita():
    window.x_min += 5
    window.x_max += 5
    desenhar()

def moverWindowEsquerda():
    window.x_min -= 5
    window.x_max -= 5
    desenhar()

def zoomIn():
    x_max_old = window.x_max 
    y_max_old = window.y_max 
    
    window.x_min /= window.zoom_value
    window.x_max /= window.zoom_value
    window.y_min /= window.zoom_value
    window.y_max /= window.zoom_value

    window.x_min += (x_max_old - window.x_max)/2
    window.x_max += (x_max_old - window.x_max)/2
    window.y_min += (y_max_old - window.y_max)/2
    window.y_max += (y_max_old - window.y_max)/2
    desenhar()

def zoomOut():
    x_min_old = window.x_min 
    x_max_old = window.x_max 
    y_min_old = window.y_min 
    y_max_old = window.y_max 
    
    window.x_min *= window.zoom_value
    window.x_max *= window.zoom_value
    window.y_min *= window.zoom_value
    window.y_max *= window.zoom_value

    window.x_min -= (window.x_max - x_max_old)/2
    window.x_max -= (window.x_max - x_max_old)/2
    window.y_min -= (window.y_max - y_max_old)/2
    window.y_max -= (window.y_max - y_max_old)/2
    desenhar()

def calcularCentroXwindow(pontos):
    soma = 0
    n = 0
    for iterador in range(len(pontos)):
        if iterador % 2 == 0:
            soma += pontos[iterador]
            n+=1
    return soma/n

def calcularCentroYwindow(pontos):
    soma = 0
    n = 0
    for iterador in range(len(pontos)):
        if iterador % 2 != 0:
            soma += pontos[iterador]
            n+=1
    return soma/n

def rotacionarWindow():
    atualizaCoordsWindow()
    #rotacionar os pontos da window para o lado esquerdo em 30 graus
    angulo = -(float(30))

    #Transladar o mundo de [-Wcx, -Wcy], Rotacionar o mundo, Escalonar o mundo
    angulo = angulo*-1
    matrixEsquerda = [[1, 0, 0], [0, 1, 0], [-(calcularCentroXwindow(copiaCoordsWindow)),-(calcularCentroYwindow(copiaCoordsWindow)), 1]]
    matrixRotacionar= [[numpy.cos(angulo* numpy.pi/180), -(numpy.sin(angulo* numpy.pi/180)), 0], [numpy.sin(angulo* numpy.pi/180), numpy.cos(angulo* numpy.pi/180), 0], [0, 0, 1]]
    matrixDireita= [[1, 0, 0], [0, 1, 0], [(calcularCentroXwindow(copiaCoordsWindow)),(calcularCentroYwindow(copiaCoordsWindow)), 1]]
    
    for i in range(len(objetosCriados)):   
        for z in range(0,len(objetosCriados[i].pontos),2):
            arrayAuxiliar = [[objetosCriados[i].pontos[z], objetosCriados[i].pontos[z+1], 1]]
            mult = numpy.matmul(arrayAuxiliar, matrixEsquerda)
            mult = numpy.matmul(mult, matrixRotacionar)
            mult = numpy.matmul(mult, matrixDireita)
            objetosCriados[i].pontos[z] = mult[0][0]
            objetosCriados[i].pontos[z+1] = mult[0][1] 

    desenhar()
            
def calcularCentroXobj(objeto):
    soma = 0
    n = 0
    for iterador in range(len(objeto.pontos)):
        if iterador % 2 == 0:
            soma += objeto.pontos[iterador]
            n+=1
    return soma/n

def calcularCentroYobj(objeto):
    soma = 0
    n = 0
    for iterador in range(len(objeto.pontos)):
        if iterador % 2 != 0:
            soma += objeto.pontos[iterador]
            n+=1
    return soma/n
            
def abrirJanelaTranslacao():
    janelaTranslacao = Toplevel(janelaPrincipal, pady=20, padx=20, height="200",width="300")
    
    listaNomes = []
    for i in range(len(objetosCriados)):
        listaNomes.append(objetosCriados[i].nome)
        
    objeto = Label(janelaTranslacao, text="Objeto:", width = 6)
    objeto.place(relx=0.08, rely=0)
    entradaNomeObjeto = ttk.Combobox(janelaTranslacao, values =listaNomes, width = 26)
    entradaNomeObjeto.place(relx=0.3, rely=0)

    ponto = Label(janelaTranslacao, text="Ponto:")
    ponto.place(relx=0.1, rely = 0.15)
    entradaPonto=Entry(janelaTranslacao,width = 26)
    entradaPonto.place(relx = 0.3, rely=0.15)

    mensagem = Label(janelaTranslacao, text = "(x, y)")
    mensagem.place(relx = 0.3, rely = 0.3)
    
    def transladar(name, ponto):
        pontoTranslacao = re.findall(r'-?\d+', ponto)
        listaPontoTranslacao = list(map(int, pontoTranslacao))
    
        matrixTranslacao =[[1, 0, 0], [0, 1, 0], [listaPontoTranslacao[0], listaPontoTranslacao[1], 1]];
        for i in range(len(objetosCriados)):
            if objetosCriados[i].nome == name:
                for z in range(0,len(objetosCriados[i].pontos),2):
                    arrayAuxiliar = [[objetosCriados[i].pontos[z], objetosCriados[i].pontos[z+1], 1]]
                    mult = numpy.matmul(arrayAuxiliar, matrixTranslacao)
                    objetosCriados[i].pontos[z] = mult[0][0]
                    objetosCriados[i].pontos[z+1] = mult[0][1]
                break
        
        desenhar()
        janelaTranslacao.destroy()

    botaoTransladar = Button(janelaTranslacao, text="Transladar", command= lambda: transladar(entradaNomeObjeto.get(), entradaPonto.get()), width = 10, height = 1)
    botaoTransladar.place(relx = 0.3, rely = 0.5)

def abrirJanelaEscalonamento():
    janelaEscalonamento = Toplevel(janelaPrincipal, pady=20, padx=20, height="200",width="300")
    
    listaNomes = []
    for i in range(len(objetosCriados)):
        listaNomes.append(objetosCriados[i].nome)
        
    objeto = Label(janelaEscalonamento, text="Objeto:", width = 6)
    objeto.place(relx=0.08, rely=0)
    entradaNomeObjeto = ttk.Combobox(janelaEscalonamento, values =listaNomes, width = 26)
    entradaNomeObjeto.place(relx=0.3, rely=0)

    fatorX = Label(janelaEscalonamento, text="Fator x:")
    fatorX.place(relx=0.1, rely = 0.15)
    entradaFatorX=Entry(janelaEscalonamento,width = 26)
    entradaFatorX.place(relx = 0.3, rely=0.15)

    fatorY = Label(janelaEscalonamento, text="Fator y:")
    fatorY.place(relx=0.1, rely = 0.3)
    entradaFatorY=Entry(janelaEscalonamento,width = 26)
    entradaFatorY.place(relx = 0.3, rely=0.3)
    
    def Escalonar(name, fatorX, fatorY):
        entradaFatorX = float(fatorX)
        entradaFatorY = float(fatorY)

        matrixEscalonamento =[[entradaFatorX, 0, 0], [0, entradaFatorY, 0], [0, 0, 1]];
        for i in range(len(objetosCriados)):
            if objetosCriados[i].nome == name:
                matrixEsquerda = [[1, 0, 0], [0, 1, 0], [-(calcularCentroXobj(objetosCriados[i])),-(calcularCentroYobj(objetosCriados[i])), 1]];
                matrixDireita = [[1, 0, 0], [0, 1, 0], [(calcularCentroXobj(objetosCriados[i])),(calcularCentroYobj(objetosCriados[i])), 1]];
                for z in range(0,len(objetosCriados[i].pontos),2):
                    arrayAuxiliar = [[objetosCriados[i].pontos[z], objetosCriados[i].pontos[z+1], 1]]
                    mult = numpy.matmul(arrayAuxiliar, matrixEsquerda)
                    mult = numpy.matmul(mult, matrixEscalonamento)
                    mult = numpy.matmul(mult, matrixDireita)
                    objetosCriados[i].pontos[z] = mult[0][0]
                    objetosCriados[i].pontos[z+1] = mult[0][1]
                break
        desenhar()
        janelaEscalonamento.destroy()

    botaoTransladar = Button(janelaEscalonamento, text="Escalonar", command= lambda: Escalonar(entradaNomeObjeto.get(), entradaFatorX.get(), entradaFatorY.get()), width = 10, height = 1)
    botaoTransladar.place(relx = 0.3, rely = 0.5)

def abrirJanelaRotacao():
    janelaRotacao = Toplevel(janelaPrincipal, pady=20, padx=20, height="200",width="300")
    
    listaNomes = []
    for i in range(len(objetosCriados)):
        listaNomes.append(objetosCriados[i].nome)
        
    objeto = Label(janelaRotacao, text="Objeto:", width = 6)
    objeto.place(relx=0.08, rely=0)
    entradaNomeObjeto = ttk.Combobox(janelaRotacao, values =listaNomes, width = 26)
    entradaNomeObjeto.place(relx=0.3, rely=0)

    angulo = Label(janelaRotacao, text="Ângulo:")
    angulo.place(relx=0.1, rely = 0.15)
    entradaAngulo=Entry(janelaRotacao,width = 5)
    entradaAngulo.place(relx = 0.3, rely=0.15)

    graus = Label(janelaRotacao, text="°")
    graus.place(relx=0.45, rely = 0.15)

    tipo = Label(janelaRotacao, text="Tipo:")
    tipo.place(relx=0.1, rely = 0.3)
    listaTipos = ['Em torno do centro do objeto', 'Em torno do centro do mundo', 'Em torno de um ponto']
    entradaTipo=ttk.Combobox(janelaRotacao, values =listaTipos, width = 26)
    entradaTipo.place(relx = 0.3, rely=0.3)

    mensagem = Label(janelaRotacao, text = "Se o tipo escolhido for Em torno de um")
    mensagem.place(relx = 0.3, rely = 0.4)

    mensagem1 = Label(janelaRotacao, text = "ponto, ao clicar em Rotacionar, uma")
    mensagem1.place(relx = 0.3, rely = 0.5)

    mensagem2 = Label(janelaRotacao, text = "nova janela será aberta para digitar")
    mensagem2.place(relx = 0.3, rely = 0.6)
    
    mensagem3 = Label(janelaRotacao, text = "o ponto.")
    mensagem3.place(relx = 0.3, rely = 0.7)
    
    
    def Rotacionar(name, angulo, tipo):
        angulo = -(float(angulo))
        
        matrixRotacao =[[numpy.cos(angulo* numpy.pi/180), -(numpy.sin(angulo* numpy.pi/180)), 0], [numpy.sin(angulo* numpy.pi/180), numpy.cos(angulo* numpy.pi/180), 0], [0, 0, 1]];
        
        if tipo == 'Em torno do centro do objeto':
            for i in range(len(objetosCriados)):
                if objetosCriados[i].nome == name:
                    matrixEsquerda = [[1, 0, 0], [0, 1, 0], [-(calcularCentroXobj(objetosCriados[i])),-(calcularCentroYobj(objetosCriados[i])), 1]];
                    matrixDireita = [[1, 0, 0], [0, 1, 0], [(calcularCentroXobj(objetosCriados[i])),(calcularCentroYobj(objetosCriados[i])), 1]];
                    for z in range(0,len(objetosCriados[i].pontos),2):
                        arrayAuxiliar = [[objetosCriados[i].pontos[z], objetosCriados[i].pontos[z+1], 1]]
                        mult = numpy.matmul(arrayAuxiliar, matrixEsquerda)
                        mult = numpy.matmul(mult, matrixRotacao)
                        mult = numpy.matmul(mult, matrixDireita)
                        objetosCriados[i].pontos[z] = mult[0][0]
                        objetosCriados[i].pontos[z+1] = mult[0][1]
                    break

        elif tipo == 'Em torno do centro do mundo':
            for i in range(len(objetosCriados)):
                if objetosCriados[i].nome == name:
                    for z in range(0,len(objetosCriados[i].pontos),2):
                        arrayAuxiliar = [[objetosCriados[i].pontos[z], objetosCriados[i].pontos[z+1], 1]]
                        mult = numpy.matmul(arrayAuxiliar, matrixRotacao)
                        objetosCriados[i].pontos[z] = mult[0][0]
                        objetosCriados[i].pontos[z+1] = mult[0][1]
                    break
        
        elif tipo == 'Em torno de um ponto':
            janelaPonto = Toplevel(janelaPrincipal, pady=20, padx=20, height="200",width="300")
            
            pontoX = Label(janelaPonto, text="Ponto x:")
            pontoX.place(relx=0.1, rely=0)
            entradaPontoX = Entry(janelaPonto, width=26)
            entradaPontoX.place(relx=0.3, rely=0)

            pontoY = Label(janelaPonto, text="Ponto y:")
            pontoY.place(relx=0.1, rely = 0.15)
            entradaPontoY=Entry(janelaPonto,width = 26)
            entradaPontoY.place(relx = 0.3, rely=0.15)

            def rotacionarPeloPonto(pontox, pontoy):
                
                for i in range(len(objetosCriados)):
                    if objetosCriados[i].nome == name:
                        matrixEsquerda = [[1, 0, 0], [0, 1, 0], [-float(pontox),-float(pontoy), 1]];
                        matrixDireita = [[1, 0, 0], [0, 1, 0], [float(pontox),float(pontoy), 1]];
                        for z in range(0,len(objetosCriados[i].pontos),2):
                            arrayAuxiliar = [[objetosCriados[i].pontos[z], objetosCriados[i].pontos[z+1], 1]]
                            mult = numpy.matmul(arrayAuxiliar, matrixEsquerda)
                            mult = numpy.matmul(mult, matrixRotacao)
                            mult = numpy.matmul(mult, matrixDireita)
                            objetosCriados[i].pontos[z] = mult[0][0]
                            objetosCriados[i].pontos[z+1] = mult[0][1]
                        break
                janelaPonto.destroy()
                desenhar()
            
            botaoRotacionar = Button(janelaPonto, text="Rotacionar", command= lambda: rotacionarPeloPonto(entradaPontoX.get(), entradaPontoY.get()), width = 10, height = 1)
            botaoRotacionar.place(relx = 0.3, rely = 0.5)
        
        desenhar()
        janelaRotacao.destroy()

    botaoRotacionar = Button(janelaRotacao, text="Rotacionar", command= lambda: Rotacionar(entradaNomeObjeto.get(), entradaAngulo.get(), entradaTipo.get()), width = 10, height = 1)
    botaoRotacionar.place(relx = 0.3, rely = 0.9)
    
#Botões
botaoCima = Button(labelWindow, text="↑",command=moverWindowCima, width=1, height=1)
botaoCima.place(relx=0.16, rely=0.07) 

botaoEsqeurda = Button(labelWindow, text="←", command=moverWindowEsquerda, width=1, height=1)
botaoEsqeurda.place(relx=0.07, rely=0.13) 

botaoDireita = Button(labelWindow, text="→", command=moverWindowDireita, width=1, height=1)
botaoDireita.place(relx=0.23, rely=0.13) 

botaoBaixo = Button(labelWindow, text="↓", command=moverWindowBaixo, width=1, height=1)
botaoBaixo.place(relx=0.16, rely=0.19) 

botaoRotacionarWindowEsquerda = Button(labelWindow, text="↶", command=rotacionarWindow, width=1, height=1)
botaoRotacionarWindowEsquerda.place(relx = 0.5, rely=0.07)

# botaoRotacionarWindowDireita = Button(labelWindow, text="↷", command= lambda: rotacionarWindow('direito'), width=1, height=1)
# botaoRotacionarWindowDireita.place(relx = 0.5, rely=0.19)

botaoZoomIn = Button(labelWindow, text="IN", command=zoomIn, width=1, height=1)
botaoZoomIn.place(relx=0.7, rely=0.07) 

botaoZoomOut = Button(labelWindow, text="OUT", command=zoomOut, width=1, height=1)
botaoZoomOut.place( relx=0.7, rely=0.19)

botaoAbrirTranslacao = Button(labelWindow, text="Translação", command=abrirJanelaTranslacao, width = 10, height = 1)
botaoAbrirTranslacao.place(relx=0.25, rely =0.35)

botaoAbrirTranslacao = Button(labelWindow, text="Escalonamento", command=abrirJanelaEscalonamento, width = 10, height = 1)
botaoAbrirTranslacao.place(relx=0.25, rely =0.42)

botaoAbrirRotacao = Button(labelWindow, text="Rotação", command=abrirJanelaRotacao, width = 10, height = 1)
botaoAbrirRotacao.place(relx=0.25, rely =0.49)

#----------------------------------------------Lado Direito----------------------------------------------------------------#

#Frame do lado direito (canvas + espaço para comentários)
ladoDireito = Frame(janelaPrincipal)
ladoDireito.grid(row=0, column=1)

#Criando canvas
canvasWidth = 500
canvasHeight = 510
canvas = Canvas(ladoDireito, bg="white", width=canvasWidth, height=canvasHeight)
canvas.grid(row=0, column=1)

#Espaço para comentários abaixo do canvas
espacoComentarios = LabelFrame(ladoDireito, height=100, width=500)
espacoComentarios.grid(row=1, column=1, pady = 2)

#Criando window e viewport
window = window.Window(0,canvasWidth,0,canvasHeight)
viewport = viewport.Viewport(0, canvasWidth, 0, canvasHeight)

#---------------------------------------Janela para adicionar objeto-----------------------------------------------------------#

objetosCriados = []

#Abrir janela para adicionar objeto
def abrirJanelaAdicionarObjeto():
    janelaParaAdicionarObjetos = Toplevel(janelaPrincipal, pady=20, padx=20, height="200",width="300")
    
    #Espaço para digitar o nome
    nome = Label(janelaParaAdicionarObjetos, text="Nome:", width = 4)
    entradaNome = Entry(janelaParaAdicionarObjetos, width=27)
    nome.place(relx=0.1, rely=0)
    entradaNome.place(relx=0.3, rely=0)
    entradaNome.insert(END, 'Test')

    #Espaço para selecionar o tipo do objeto
    tipo = Label(janelaParaAdicionarObjetos, text="Tipo:")
    tipo.place(relx=0.1, rely = 0.15)
    listaTipos = ["Ponto", "Reta", "Polígono"]
    tipoCb=ttk.Combobox(janelaParaAdicionarObjetos, values =listaTipos, width = 26)
    tipoCb.place(relx = 0.3, rely=0.15)
    tipoCb.current(2)
    
    #Espaço para selecionar a cor do objeto
    cor = Label(janelaParaAdicionarObjetos, text="Cor:")
    cor.place(relx=0.1, rely=0.3)
    listaCores = ["Amarelo", "Azul", "Verde", "Vermelho","Preto"]
    corCb=ttk.Combobox(janelaParaAdicionarObjetos, values=listaCores, width = 26)
    corCb.place(relx=0.3, rely=0.3)
    corCb.current(4)
    
    #Espaço para digitar as coordenadas
    coordenadas = Label(janelaParaAdicionarObjetos, text="Coordenadas:")
    entradaCoordenadas = Entry(janelaParaAdicionarObjetos, width=27)
    coordenadas.place(relx=0.017, rely =0.45)
    entradaCoordenadas.place(relx=0.3, rely = 0.45)
    exemploDeCoordenadas = Label(janelaParaAdicionarObjetos, text = "(x1, y1),(x2, y2)...")
    exemploDeCoordenadas.place(relx=0.3, rely=0.6)
    entradaCoordenadas.insert(END, '200,235,300,235,250,300')

    
    #Botão para gerar objetos
    botaoGerarObjeto = Button(janelaParaAdicionarObjetos, text="Gerar objeto", width = 15, command= lambda: gerarObjeto(tipoCb.get(), corCb.get()))
    botaoGerarObjeto.place(relx=0.25, rely=0.85)
    
    def gerarObjeto(tipo, cor):  
        #pega o nome digitado
        nomeEscolhido = entradaNome.get()
        
        #pega as coordenadas digitadas
        entrada_cords = entradaCoordenadas.get()
        
        coordsInicial = []
        coordsInt = []
        
        #tira os caracteres de entrada_cords
        coordsInicial = re.findall(r'-?\d+', entrada_cords)
        
        #Transforma o vetor coordsInicial em um vetor de inteiros
        coordsInt = list(map(int, coordsInicial))
        
        objetoCriado = None
        
        if tipo == 'Ponto':
            objetoCriado = objetos.Ponto(coordsInt, coordsInt, nomeEscolhido, tipo, cor)
        elif tipo == 'Reta':
            objetoCriado = objetos.Reta(coordsInt, coordsInt, nomeEscolhido, tipo, cor)
        elif tipo == 'Polígono':
            objetoCriado = objetos.Poligono(coordsInt, coordsInt, nomeEscolhido, tipo, cor) 
        
        #bota o nome do objeto criado na listbox
        listbox.insert(1, objetoCriado.nome)
        
        #bota o objeto criado na lista de objetos criados
        objetosCriados.append(objetoCriado)
        
        #desenha o objeto criado
        desenhar()
        
        #fecha a janela de adicionar objetos
        janelaParaAdicionarObjetos.destroy()

#Botão no frame Window para adicionar um objeto novo
botaoAdicionarObjeto = Button(labelWindow, text="Adicionar objeto", command=abrirJanelaAdicionarObjeto, width = 10, height = 1)
botaoAdicionarObjeto.place(relx=0.25, rely=0.28)

#------------------------------------------------------------------------------------------------------------------------------#

#Método para desenhar o objeto no canvas
def desenhar():
    
    #Antes de desenhar apaga tudo q estava desenhado
    canvas.delete("all")
    
    for objeto in objetosCriados:
        if objeto.tipo == 'Ponto':
            listaAuxiliar = []
            for iterador in range(len(objeto.pontos)):
                if iterador % 2 == 0:
                    listaAuxiliar.append(transformadaParaX(objeto.pontos[iterador]))
                else:
                    listaAuxiliar.append(transformadaParaY(objeto.pontos[iterador]))
            if objeto.cor == 'Amarelo':
                canvas.create_oval((listaAuxiliar[0], listaAuxiliar[1]), (listaAuxiliar[0],listaAuxiliar[1]), fill='yellow', width=2)
            elif objeto.cor == 'Azul':
                canvas.create_oval((listaAuxiliar[0], listaAuxiliar[1]), (listaAuxiliar[0],listaAuxiliar[1]), fill='blue', width=2)
            elif objeto.cor == 'Verde':
                canvas.create_oval((listaAuxiliar[0], listaAuxiliar[1]), (listaAuxiliar[0],listaAuxiliar[1]), fill='green', width=2)
            elif objeto.cor == 'Vermelho':
                canvas.create_oval((listaAuxiliar[0], listaAuxiliar[1]), (listaAuxiliar[0],listaAuxiliar[1]), fill='red', width=2)
            elif objeto.cor == 'Preto':
                canvas.create_oval((listaAuxiliar[0], listaAuxiliar[1]), (listaAuxiliar[0],listaAuxiliar[1]), fill='black', width=2)
        
        elif objeto.tipo == 'Reta':   
            listaAuxiliar = []
            for iterador in range(len(objeto.pontos)):
                if iterador % 2 == 0:
                    listaAuxiliar.append(transformadaParaX(objeto.pontos[iterador]))
                else:
                    listaAuxiliar.append(transformadaParaY(objeto.pontos[iterador]))
            if objeto.cor == 'Amarelo':
                canvas.create_line(listaAuxiliar, fill='yellow')
            elif objeto.cor == 'Azul':
                canvas.create_line(listaAuxiliar, fill='blue')
            elif objeto.cor == 'Verde':
                canvas.create_line(listaAuxiliar, fill='green')
            elif objeto.cor == 'Vermelho':
                canvas.create_line(listaAuxiliar, fill='red')
            elif objeto.cor == 'Preto':
                canvas.create_line(listaAuxiliar, fill='black')
        
        elif objeto.tipo == 'Polígono':
            listaAuxiliar = []
            objeto.pontos.append(objeto.pontos[0])
            objeto.pontos.append(objeto.pontos[1])
            for iterador in range(len(objeto.pontos)):
                if iterador % 2 == 0:
                    listaAuxiliar.append(transformadaParaX(objeto.pontos[iterador]))
                else:
                    listaAuxiliar.append(transformadaParaY(objeto.pontos[iterador]))
            if objeto.cor == 'Amarelo':
                canvas.create_line(listaAuxiliar, fill='yellow')
            elif objeto.cor == 'Azul':
                canvas.create_line(listaAuxiliar, fill='blue')
            elif objeto.cor == 'Verde':
                canvas.create_line(listaAuxiliar, fill='green')
            elif objeto.cor == 'Vermelho':
                canvas.create_line(listaAuxiliar, fill='red')
            elif objeto.cor == 'Preto':
                canvas.create_line(listaAuxiliar, fill='black')
            
            objeto.pontos= objeto.pontos[:-2]
            

#Cáculo da transformada de viewport
def transformadaParaX(x):
    xw_min = window.x_min
    xw_max = window.x_max
    x_vp = (x - xw_min) / (xw_max - xw_min) * (viewport.x_max - viewport.x_min)
    return x_vp

def transformadaParaY(y):
    yw_min = window.y_min
    yw_max = window.y_max
    y_vp = (1 - (y - yw_min) / (yw_max - yw_min)) * (viewport.y_max - viewport.y_min)
    return y_vp

copiaCoordsWindow = []
copiaCoordsWindow.append(window.x_min)
copiaCoordsWindow.append(window.y_min)

copiaCoordsWindow.append(window.x_max)
copiaCoordsWindow.append(window.y_min)

copiaCoordsWindow.append(window.x_max)
copiaCoordsWindow.append(window.y_max)

copiaCoordsWindow.append(window.x_min)
copiaCoordsWindow.append(window.y_max)

def atualizaCoordsWindow():
    copiaCoordsWindow[0] = (window.x_min)
    copiaCoordsWindow[1] = (window.y_min)

    copiaCoordsWindow[2] = (window.x_max)
    copiaCoordsWindow[3] = (window.y_min)

    copiaCoordsWindow[4] = (window.x_max)
    copiaCoordsWindow[5] = (window.y_max)

    copiaCoordsWindow[6] = (window.x_min)
    copiaCoordsWindow[7] = (window.y_max)

print("copiaCoordsWindow:", copiaCoordsWindow)
print("centro da window:", calcularCentroXwindow(copiaCoordsWindow), calcularCentroYwindow(copiaCoordsWindow))
janelaPrincipal.mainloop()
