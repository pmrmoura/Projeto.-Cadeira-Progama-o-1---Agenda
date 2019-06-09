# -*- coding: utf-8 -*-
import sys

TODO_FILE = 'todo.txt'
ARCHIVE_FILE = 'done.txt'

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"
YELLOW = "\033[0;33m"

ADICIONAR = 'a'
REMOVER = 'r'
FAZER = 'f'
PRIORIZAR = 'p'
LISTAR = 'l'

# Imprime texto com cores. Por exemplo, para imprimir "Oi mundo!" em vermelho, basta usar
#
# printCores('Oi mundo!', RED)
# printCores('Texto amarelo e negrito', YELLOW + BOLD)

def printCores(*texto, cor) :
  print(cor + texto + RESET)
  

# Adiciona um compromisso aa agenda. Um compromisso tem no minimo
# uma descrição. Adicionalmente, pode ter, em caráter opcional, uma
# data (formato DDMMAAAA), um horário (formato HHMM), uma prioridade de A a Z, 
# um contexto onde a atividade será realizada (precedido pelo caractere
# '@') e um projeto do qual faz parte (precedido pelo caractere '+'). Esses
# itens opcionais são os elementos da tupla "extras", o segundo parâmetro da
# função.
#
# extras ~ (data, hora, prioridade, contexto, projeto)
#
# Qualquer elemento da tupla que contenha um string vazio ('') não
# deve ser levado em consideração. 
def adicionar(descricao, extras):
  data = '' 
  hora = ''
  pri = ''
  desc = ''
  contexto = ''
  projeto = ''
  # não é possível adicionar uma atividade que não possui descrição. 
  if descricao  == '' :
    return False
  else:
    if dataValida(extras[0]):
      data = extras[0]
    if horaValida(extras[1]):
      hora = extras[1]
    if  prioridadeValida(extras[2]):
      pri = extras[2]
    if contextoValido(extras[3]):
      contexto = extras[3]
    if projetoValido(extras[4]):
      projeto = extras[4]
    novaAtividade = [data, hora, pri, descricao,contexto, projeto]
    novaAtividade = ' '.join(novaAtividade)
  # Escreve no TODO_FILE. 
  try: 
    fp = open(TODO_FILE, 'a')
    fp.write(novaAtividade + "\n")
    fp.close()
  except IOError as err:
    print("Não foi possível escrever para o arquivo " + TODO_FILE)
    print(err)
    return False

  return True


# Valida a prioridade.
def prioridadeValida(pri):

  if len(pri) >= 2 and pri[0] == '(' and pri[2] == ')' and ehLetra(pri[1]):
        return True
  else:
        return False
  
  return False


# Valida a hora. Consideramos que o dia tem 24 horas, como no Brasil, ao invés
# de dois blocos de 12 (AM e PM), como nos EUA.
def horaValida(horaMin) :
  if len(horaMin) != 4 or not soDigitos(horaMin):
    return False
  else:
    if int(horaMin[0] + horaMin[1]) >= 0 and int(horaMin[0] + horaMin[1]) <= 23:
      if int(horaMin[0] + horaMin[1]) >= 0 and int(horaMin[2] + horaMin[3]) < 60:
        return True
      else:
        return False
    else:
      return False

# Valida datas. Verificar inclusive se não estamos tentando
# colocar 31 dias em fevereiro. Não precisamos nos certificar, porém,
# de que um ano é bissexto. 
def dataValida(data) :
  if len(data)!= 8 or not soDigitos(data):
        return False
  else:
        mes = int(data[2] + data[3])
        ano = int(data[4] + data[5] + data[6] + data[7])
        dia = int(data[0] + data[1])
        if mes <= 12 and  mes >= 1:
              if len(str(ano)) == 4:
                    if mes == 2 and dia  > 29:
                          return  False
                    elif mes == 4 or mes == 6 or mes == 8 or mes == 9 or mes == 11:
                          if dia > 30:
                                return False
                          else:
                                return True
                    else:
                          if dia > 0 and dia < 32:
                                return True
              else:
                    return False
        else:
              return False
  return False

# Valida que o string do projeto está no formato correto. 
def projetoValido(proj):
  if len(proj) >= 2 and proj[0] == '+':
        return True
  else:
        return False
        

  return False

# Valida que o string do contexto está no formato correto. 
def contextoValido(cont):

  if len(cont) >= 2 and cont[0] == '@':
        return True
  else:
        return False

  return False

# Valida que a data ou a hora contém apenas dígitos, desprezando espaços
# extras no início e no fim.
def soDigitos(numero) :
  if type(numero) != str :
    return False
  for x in numero :
    if x < '0' or x > '9' :
      return False
  return True


# Dadas as linhas de texto obtidas a partir do arquivo texto todo.txt, devolve
# uma lista de tuplas contendo os pedaços de cada linha, conforme o seguinte
# formato:
#
# (descrição, prioridade, (data, hora, contexto, projeto))
#
# É importante lembrar que linhas do arquivo todo.txt devem estar organizadas de acordo com o
# seguinte formato:
#
# DDMMAAAA HHMM (P) DESC @CONTEXT +PROJ
#
# Todos os itens menos DESC são opcionais. Se qualquer um deles estiver fora do formato, por exemplo,
# data que não tem todos os componentes ou prioridade com mais de um caractere (além dos parênteses),
# tudo que vier depois será considerado parte da descrição.  
def organizar(linhas):
  itens = []

  for l in linhas:
    data = '' 
    hora = ''
    pri = ''
    desc = ''
    contexto = ''
    projeto = ''
  
    l = l.strip() # remove espaços em branco e quebras de linha do começo e do fim
    tokens = l.split() # quebra o string em palavras

    # Processa os tokens um a um, verificando se são as partes da atividade.
    # Por exemplo, se o primeiro token é uma data válida, deve ser guardado
    # na variável data e posteriormente removido a lista de tokens. Feito isso,
    # é só repetir o processo verificando se o primeiro token é uma hora. Depois,
    # faz-se o mesmo para prioridade. Neste ponto, verifica-se os últimos tokens
    # para saber se são contexto e/ou projeto. Quando isso terminar, o que sobrar
    # corresponde à descrição. É só transformar a lista de tokens em um string e
    # construir a tupla com as informações disponíveis. 
    for y in tokens:
      inicial = tokens[0]
      finais  = tokens[-1]
      if dataValida(inicial):
        data = inicial
        tokens.pop(0)
      elif horaValida(inicial):
        hora = inicial
        tokens.pop(0)
      elif prioridadeValida(inicial):
        pri = inicial
        tokens.pop(0)
      elif contextoValido(finais):
        contexto = finais
        tokens.pop()
      elif projetoValido(finais):
        projeto = finais
        tokens.pop()
      desc = ' '.join(tokens)
    itens.append((desc, (data, hora, pri, contexto, projeto)))

  return itens



# Datas e horas são armazenadas nos formatos DDMMAAAA e HHMM, mas são exibidas
# como se espera (com os separadores apropridados). 
#
# Uma extensão possível é listar com base em diversos critérios: (i) atividades com certa prioridade;
# (ii) atividades a ser realizadas em certo contexto; (iii) atividades associadas com
# determinado projeto; (vi) atividades de determinado dia (data específica, hoje ou amanhã). Isso não
# é uma das tarefas básicas do projeto, porém. 
def listar():
  lista = []
  tupla = ()
  fp = open(TODO_FILE, 'r')
  for x in fp:
    lista.append(x)
  fp.close()
  lista = organizar(lista)
  lista = ordenarPorPrioridade(lista)
  for x in range(len(lista)):
    data = lista[x][1][0]
    hora = lista[x][1][1]
    if dataValida(lista[x][1][0]):
      data = data[0] + data[1] + "/" + data[2] + data[3] + "/" + data[4] + data[5] + data[6] + data[7]
    if horaValida(lista[x][1][1]):
      hora = hora[0] + hora[1] + "h" + hora[2] + hora[3] + "m"
    palavraLista = [str(x), data ,  hora ,lista[x][1][2] ,lista[x][0] ,lista[x][1][3] , lista[x][1][4]]
    palavra = ' '.join(palavraLista)
    if lista[x][1][2] == "(A)":
      print(YELLOW + BOLD, palavra, RESET)
    else:
      print(GREEN, palavra , RESET)
    

def ordenarPorDataHora(lista):
  for x in range(len(lista) - 1):
    data = lista[x][1][0]
    data2 = lista[x + 1][1][0]
    mes = int(data[2] + data[3])
    ano = int(data[4] + data[5] + data[6] + data[7])
    dia = int(data[0] + data[1])
    mes2 = int(data2[2] + data2[3])
    ano2 = int(data2[4] + data2[5] + data2[6] + data2[7])
    dia2 = int(data2[0] + data2[1])
    if ano > ano2 or ano2 > ano:
      lista[x], lista[x + 1] = lista[x + 1], lista[x]
    elif mes > mes2 or mes2 > mes:
      lista[x], lista[x + 1] = lista[x + 1], lista[x]
    elif dia > dia2 or dia2 > dia:
      lista[x], lista[x + 1] = lista[x + 1], lista[x]
      
  return lista
   
def ordenarPorPrioridade(lista):
  n = 0
  while n < len(lista) * len(lista):
    for x in range(len(lista) - 1):
      if lista[x][1][2] > lista[x + 1][1][2] and x + 1 != len(lista):
        lista[x], lista[x + 1] = lista[x + 1], lista[x]
      n += 1
  lista = verificaPrioridadeEmBranco(lista)
  return lista

def verificaPrioridadeEmBranco(lista):
  n = 0
  while n < len(lista) * len(lista):
    for x in range(len(lista) - 1):
      if lista[x][1][2] == '':
        lista.insert(len(lista), lista[x])
        lista.remove(lista[x])
    n += 1
  return lista


def fazer(num):

  ################ COMPLETAR

  return 

def remover():

  ################ COMPLETAR

  return

# prioridade é uma letra entre A a Z, onde A é a mais alta e Z a mais baixa.
# num é o número da atividade cuja prioridade se planeja modificar, conforme
# exibido pelo comando 'l'. 
def priorizar(num, prioridade):

  ################ COMPLETAR

  return 



# Esta função processa os comandos e informações passados através da linha de comando e identifica
# que função do programa deve ser invocada. Por exemplo, se o comando 'adicionar' foi usado,
# isso significa que a função adicionar() deve ser invocada para registrar a nova atividade.
# O bloco principal fica responsável também por tirar espaços em branco no início e fim dos strings
# usando o método strip(). Além disso, realiza a validação de horas, datas, prioridades, contextos e
# projetos.  

def processarComandos(comandos) :
  if comandos[1] == ADICIONAR:
    comandos.pop(0) # remove 'agenda.py'
    comandos.pop(0) # remove 'adicionar'
    itemParaAdicionar = organizar([' '.join(comandos)])[0]
    # itemParaAdicionar = (descricao, (prioridade, data, hora, contexto, projeto))
    adicionar(itemParaAdicionar[0], itemParaAdicionar[1]) # novos itens não têm prioridade
  elif comandos[1] == LISTAR:
    listar()    
    ################ COMPLETAR

  elif comandos[1] == REMOVER:
    return    

    ################ COMPLETAR    

  elif comandos[1] == FAZER:
    return    

    ################ COMPLETAR

  elif comandos[1] == PRIORIZAR:
    return    

    ################ COMPLETAR

  else :
    print("Comando inválido.")

def ehLetra(strr):
    strr = strr.upper()
    if strr < 'A' or strr > 'Z':
        return False
    return True
  

    
  
# sys.argv é uma lista de strings onde o primeiro elemento é o nome do programa
# invocado a partir da linha de comando e os elementos restantes são tudo que
# foi fornecido em sequência. Por exemplo, se o programa foi invocado como
#
# python3 agenda.py a Mudar de nome.
#
# sys.argv terá como conteúdo
#
# ['agenda.py', 'a', 'Mudar', 'de', 'nome']
processarComandos(sys.argv)
