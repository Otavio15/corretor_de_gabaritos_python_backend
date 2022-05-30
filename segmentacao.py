
import cv2
import os
import shutil

class Processamento():

    def __init__(self):
        pass

    def leituraImg(self, path_img, i, j):

        flag = False

        classificador = cv2.CascadeClassifier("cascade.xml")

        img = cv2.imread(path_img+".jpg")

        # amplia a imagem da placa em 4
        img = cv2.resize(img, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC);
        #cv2.imshow("ENTRADA", img)

        # Converte para escala de cinza
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("Escala Cinza", img)

        # Binariza imagem
        img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 91, 40)
        #cv2.imshow("Limiar", img)

        # Desfoque na Imagem
        img = cv2.GaussianBlur(img, (5, 5), 0)
        # cv2.imshow("Desfoque", img)

        faces_detectadas = classificador.detectMultiScale(img, scaleFactor=1.05)

        for (x, y, a, l) in faces_detectadas:
            # img_capturada retorna a região desenhada da face encontrada

            if (j != 1 and i != 0):
                global respostas, flag_resposta
                if (j == 2 and flag == False):
                    respostas[i] = "A"
                    flag = True
                    flag_resposta = True
                    cv2.rectangle(img, (x, y), (x + a, y + l), (0, 255, 0), 2)
                elif (j == 3 and flag == False):
                    respostas[i] = "B"
                    flag = True
                    flag_resposta = True
                    cv2.rectangle(img, (x, y), (x + a, y + l), (0, 255, 0), 2)
                elif (j == 4 and flag == False):
                    respostas[i] = "C"
                    flag = True
                    flag_resposta = True
                    cv2.rectangle(img, (x, y), (x + a, y + l), (0, 255, 0), 2)
                elif (j == 5 and flag == False):
                    respostas[i] = "D"
                    flag = True
                    flag_resposta = True
                    cv2.rectangle(img, (x, y), (x + a, y + l), (0, 255, 0), 2)
                elif (j == 6 and flag == False):
                    respostas[i] = "E"
                    flag = True
                    flag_resposta = True
                    cv2.rectangle(img, (x, y), (x + a, y + l), (0, 255, 0), 2)


        cv2.imwrite("saida/{}/{}.jpg".format(i,j), img)

class Ordem:
    def __init__(self, pasta, subpasta, valorx, imagem):
        print('Pasta {}, Subpasta {}, Valor X {}'.format(pasta, subpasta, valorx))
        self.pasta = pasta
        self.subpasta = subpasta
        self.valorx = valorx
        self.imagem = imagem

tamanho = len(os.listdir("imagens"))

if (tamanho > 0):
    for i in range(tamanho):
        shutil.rmtree('imagens/' + str(i))

conjunto_elementos = []

arquivo = "gabarito.png"

imagem = cv2.imread(arquivo)

imagem_aux = cv2.imread(arquivo)

#####################
height = imagem.shape[0]
width = imagem.shape[1]

if (height > width):
    while (width > 600):
        height -= int(height/5)
        width -= int(width/5)
        #print("Altura {}, largura {}".format(height,width))

imagem = cv2.resize(imagem, (width, height), interpolation = cv2.INTER_CUBIC)
imagem_aux = cv2.resize(imagem_aux, (width, height), interpolation = cv2.INTER_CUBIC)
#####################

imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
cv2.imwrite("Imagem-cinza.jpg", imagem_cinza)

thresh = cv2.adaptiveThreshold(imagem_cinza, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 91, 20)
thresh = cv2.medianBlur(thresh,5)

cv2.imwrite("Imagem-binaria.jpg", thresh)

contours,h = cv2.findContours(thresh,cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

contador = 0
contador_pastas = 0

aux_contador_pastas = False
aux_aux_contador_pasta = False

aux_y = -1
flag_cor = False

dados = 0

for cnt in contours:

    # captura o perímetro da imagem
    perimetro = cv2.arcLength(cnt, True)
    # aproxima os contornos da imagem, neste caso estou declarando a variável
    approx = 0

    if perimetro > 80 and perimetro < 300:
        # aproxima os contornos da forma correspondente
        approx = cv2.approxPolyDP(cnt, 0.04 * perimetro, True)
        # verifica a quantidade de vértices, caso seja igual a 4 pode ser um...
        # quadrado ou terângulo
        if len(approx) == 4:
            # boundingRect captura as coordenadas x,y e a altura e largura
            (x, y, a, l) = cv2.boundingRect(cnt)

            # A condição seguinte testa as seguintes propiedades:
            # A altura e largura é maior que 15px e altura e largura é menor que 300px;
            # O resultado da altura - largura é menor que 15, essa condicional serve...
            # para encontrar figuras geométricas próximas de um quadrado.
            if (a > 10 and l > 10 and a < 100 and l < 100 and a-l < 15):
                # cv2.rectangle é responsável por desenhar um retângulo na imagem

                elementos = len(os.listdir("imagens"))

                if (aux_y == -1):
                    contador_pastas += 1
                    cv2.rectangle(imagem_aux, (x, y), (x + a, y + l), (255, 255, 255), 2)
                    cv2.rectangle(imagem, (x, y), (x + a, y + l), (0, 255, 255), 2)
                else:
                    if (y in range(aux_y-5, aux_y+5)):
                        if (flag_cor == False):
                            if aux_contador_pastas == False:
                                contador_pastas += 1
                                aux_contador_pastas = True

                            cv2.rectangle(imagem_aux, (x, y), (x + a, y + l), (255, 255, 255), 2)
                            cv2.rectangle(imagem, (x, y), (x + a, y + l), (0, 255, 0), 2)

                        else:
                            if aux_contador_pastas == True:
                                contador_pastas += 1
                                aux_contador_pastas = False

                            cv2.rectangle(imagem_aux, (x, y), (x + a, y + l), (255, 255, 255), 2)
                            cv2.rectangle(imagem, (x, y), (x + a, y + l), (0, 0, 255), 2)

                    else:
                        if (flag_cor == False):
                            if aux_contador_pastas == True:
                                contador_pastas += 1
                                aux_contador_pastas = False

                            cv2.rectangle(imagem_aux, (x, y), (x + a, y + l), (255, 255, 255), 2)
                            cv2.rectangle(imagem, (x, y), (x + a, y + l), (0, 0, 255), 2)
                            flag_cor = True

                        else:
                            if aux_contador_pastas == False:
                                contador_pastas += 1
                                aux_contador_pastas = True

                            cv2.rectangle(imagem_aux, (x, y), (x + a, y + l), (255, 255, 255), 2)
                            cv2.rectangle(imagem, (x, y), (x + a, y + l), (0, 255, 0), 2)
                            flag_cor = False

                aux_y = y

                # variável roi captura a imagem "dentro" do retângulo
                roi = imagem_aux[y:y + l, x:x + a]

                #altera os valores dentro do diretório
                if aux_contador_pastas == aux_aux_contador_pasta:
                    contador += 1
                else:
                    contador = 1
                    aux_aux_contador_pasta = aux_contador_pastas
                # ++++++++++++++++++++++++++++++++++++++

                dados = Ordem(contador_pastas - 1, contador, x, roi)
                conjunto_elementos.append(dados)

cv2.imwrite("Imagem-reconhecida.jpg", imagem)

conjunto_elementos.sort(key=lambda x: x.valorx)
conjunto_elementos.sort(key=lambda x: x.pasta)

aux = 1
contador = 0
tamanho = len(os.listdir("imagens"))

del(conjunto_elementos[0])

