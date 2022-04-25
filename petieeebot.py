import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from dbhelper import DBHelper
from buttons import *

#Ligação com o banco de dados
db = DBHelper()
db.setup()

chave_api = "hidden"

bot = telebot.TeleBot(chave_api)

data = {'horario':"", 'descricao': ""}

#Querys para habilitar a navegação por botões dentro do bot
@bot.callback_query_handler(func = lambda call:True)
def callback_query(call):
    #Menu
    if call.data == "cb_alarme":
        alarme1(call.message)

    elif call.data == "cb_checagem":
        checagem1(call.message)
    
    #Menu -> Alarme
    elif call.data == "cb_alarme_r1":
        remedios1(call.message)
    
    elif call.data == "cb_alarme_d1":
        dentes1(call.message)

    elif call.data == "cb_alarme_b1":
        banho1(call.message)
    
    elif call.data == "cb_menu_voltar":
        menu(call.message)
    
    #Alarme -> Remedio
    elif call.data == "cb_remedio_lst":
        listarremedios(call.message)

    elif call.data == "cb_remedio_rmv":
        removerremedios(call.message)

    elif call.data == "cb_remedio_add":
        addremedios(call.message)
    
    elif call.data == "cb_alarme_voltar":
        alarme1(call.message)

    #Alarme -> Dentes
    elif call.data == "cb_dentes_lst":
        listardentes(call.message)

    elif call.data == "cb_dentes_rmv":
        removerdentes(call.message)

    elif call.data == "cb_dentes_add":
        adddentes(call.message)

    #Alarme -> Remedio
    elif call.data == "cb_banho_lst":
        listarbanhos(call.message)

    elif call.data == "cb_banho_rmv":
        removerbanho(call.message)

    elif call.data == "cb_banho_add":
        addbanho(call.message)

    #List -> Voltar
    elif call.data == "cb_r_list_voltar":
        remedios1(call.message)

    elif call.data == "cb_d_list_voltar":
        dentes1(call.message)

    elif call.data == "cb_b_list_voltar":
        banho1(call.message)
    

#########        
#Alarmes#
#########



@bot.message_handler(commands=["alarme"])
def alarme1(mensagem):
    texto = """
Que tipo de alarme deseja configurar?

/remedios - Alarme dos remédios
/dentes - Alarme para escovação dental
/banho - Alarme para horários de banho

Caso o bot não entenda o comando, o menu será reenviado
"""
    bot.send_message(mensagem.chat.id, texto, reply_markup=botoes_alarme())



########## 
#Remedios#
########## 

#Menu Remédios
@bot.message_handler(commands=["remedios"])
def remedios1(mensagem):
    texto = """
Que ação deseja realizar?

/addrem - Adicionar alarme para remédios.
/rmvrem - Remover um alarme já configurado para remédios.
/listrem - Listar os horários já configurados para remédios.
"""
    bot.send_message(mensagem.chat.id, texto, reply_markup=botoes_remedio())

#Listar
@bot.message_handler(commands=["listrem"])
def listarremedios(mensagem):
    tabela = db.get_items("remedio", mensagem.chat.id)
    tabela.sort()

    tabela_formato = ["Alarme %i: %s" % (index+1, value) for index, value in enumerate(tabela)]
    tabela_formatada = "\n".join(tabela_formato)

    if not tabela:
        bot.send_message(mensagem.chat.id, "Você não possui nenhum alarme definido. Selecione /remedios para criar um.", reply_markup=botoes_r_list())
    else:
        bot.send_message(mensagem.chat.id, f"{tabela_formatada}\n\nSelecione /remedios para criar ou remover um alarme.", reply_markup=botoes_r_list())

#Adicionar
@bot.message_handler(commands=["addrem"])
def addremedios(mensagem):
    global data
    env = bot.send_message(mensagem.chat.id, "Digite o horário que quer adicionar para remédios (Horas:Minutos)")
    bot.register_next_step_handler(env, respremediosadd)

#Segunda etapa ao adicionar remédio, registra a resposta da mensagem a ação de adicionar
def respremediosadd(mensagem):
    horariotd = mensagem.text
    temphoras = horariotd
    checagem = db.get_horarioexiste("remedio", mensagem.chat.id, f"{horariotd}")

    try:
        horas, minutos = temphoras.split(":")
    except ValueError:
        bot.send_message(mensagem.chat.id, f'Entrada não esperada, selecione /addrem para tentar novamente.', reply_markup=botoes_r_list())
    else:
        if (horas.isnumeric() == False or minutos.isnumeric() == False or len(horas) != 2 or len(minutos) != 2):
            bot.send_message(mensagem.chat.id, f'Horário inválido. Selecione /addrem para tentar novamente.', reply_markup=botoes_r_list())

        elif (int(horas) > 23 or int(horas) < 0) or (int(minutos) > 59 or int(minutos) < 0):
            bot.send_message(mensagem.chat.id, f'Horário inválido. Selecione /addrem para tentar novamente.', reply_markup=botoes_r_list())
        
        elif checagem:
            bot.send_message(mensagem.chat.id, f'Horário já possui um alarme configurado. Selecione /addrem para tentar novamente ou /listrem para listar os alarmes.', reply_markup=botoes_r_list())   
        
        else:
            data['horario'] = horariotd
            env = bot.send_message(mensagem.chat.id, f'Agora, digite a descrição do horário, caso não deseje uma, digite "N"')
            bot.register_next_step_handler(env, respremediosadd2)

#Terceira etapa ao adicionar remédio, verifica se a resposta foi válida ou não e da prosseguimento ao armazenamento no banco
def respremediosadd2(mensagem):
    if mensagem.text[0] == '/':
        bot.send_message(mensagem.chat.id, f"Descrição inválida. Selecione /addrem para tentar novamente.", reply_markup=botoes_r_list())
    else:
        if (mensagem.text).upper() == "N":
            data['descricao'] = "Alarme" 
        else:  
            data['descricao'] = mensagem.text

        horario = f"'{data['horario']}'"
        descricao = f"'{data['descricao']}'"

        bot.send_message(mensagem.chat.id, f"Alarme de remédio definido para {horario} com a descrição: {descricao}.", reply_markup=botoes_r_list())
        db.add_item(mensagem.chat.id, "'remedio'", 'NULL', horario, descricao)

#Remover
@bot.message_handler(commands=["rmvrem"])
def removerremedios(mensagem):
    env = bot.send_message(mensagem.chat.id, "Digite o horário do alarme de remédios que deseja remover. (Horas:Minutos)")
    bot.register_next_step_handler(env, respremediosrmv)

#Segunda etapa ao remover remédio, registra a resposta da mensagem a ação de remover
def respremediosrmv(mensagem):
    horario = mensagem.text
    tem = db.check_item(horario, 'remedio',  mensagem.chat.id)
    horario = f"'{horario}'"
    temphoras = f"{horario}"
    temphoras = temphoras.replace("'", "")

    try:
        horas, minutos = temphoras.split(":")
    except ValueError:
        bot.send_message(mensagem.chat.id, f'Entrada não esperada, selecione /rmvrem para tentar novamente.', reply_markup=botoes_r_list())
    else:
        if horas.isnumeric() == False or minutos.isnumeric == False:
            bot.send_message(mensagem.chat.id, f"Horário digitado inválido. Selecione /rmvrem para tentar novamente ou /listrem para listar os horários.", reply_markup=botoes_r_list())
        else:
            if tem != None:
                db.delete_item("'remedio'", horario, mensagem.chat.id)
                bot.send_message(mensagem.chat.id, f"Alarme no horário {horario} removido.", reply_markup=botoes_r_list())
            else:
                bot.send_message(mensagem.chat.id, f"Não existe um alarme programado neste horário.", reply_markup=botoes_r_list())



########
#Dentes#
########

#Menu Dentes
@bot.message_handler(commands=["dentes"])
def dentes1(mensagem):
    texto = """
Que ação deseja realizar?

/addden - Adicionar alarme para escovar os dentes.
/rmvden - Remover um alarme já configurado para escovar os dentes.
/listden - Listar os horários já configurados para escovar os dentes.
"""
    bot.send_message(mensagem.chat.id, texto, reply_markup=botoes_dente())

#Listar
@bot.message_handler(commands=["listden"])
def listardentes(mensagem):
    tabela = db.get_items("dentes", mensagem.chat.id)
    tabela.sort()

    tabela_formato = ["Alarme %i: %s" % (index+1, value) for index, value in enumerate(tabela)]
    tabela_formatada = "\n".join(tabela_formato)

    if not tabela:
        bot.send_message(mensagem.chat.id, "Você não possui nenhum alarme definido. Selecione /dentes para criar um.", reply_markup=botoes_d_list())
    else:
        bot.send_message(mensagem.chat.id, f"{tabela_formatada}\n\nSelecione /dentes para criar ou remover um alarme.", reply_markup=botoes_d_list())

#Adicionar
@bot.message_handler(commands=["addden"])
def adddentes(mensagem):
    global data
    env = bot.send_message(mensagem.chat.id, "Digite o horário que quer adicionar para escovar os dentes (Horas:Minutos)")
    bot.register_next_step_handler(env, respdentesadd)

#Segunda etapa ao adicionar dentes, registra a resposta da mensagem a ação de adicionar
def respdentesadd(mensagem):
    horariotd = mensagem.text
    temphoras = horariotd
    checagem = db.get_horarioexiste("dentes", mensagem.chat.id, f"{horariotd}")
    
    try:
        horas, minutos = temphoras.split(":")
    except ValueError:
        bot.send_message(mensagem.chat.id, f'Entrada não esperada, selecione /addden para tentar novamente.', reply_markup=botoes_d_list())
    else:
        if (horas.isnumeric() == False or minutos.isnumeric() == False or len(horas) != 2 or len(minutos) != 2):
            bot.send_message(mensagem.chat.id, f'Horário inválido. Selecione /addden para tentar novamente.', reply_markup=botoes_d_list())

        elif (int(horas) > 23 or int(horas) < 0) or (int(minutos) > 59 or int(minutos) < 0):
            bot.send_message(mensagem.chat.id, f'Horário inválido. Selecione /addden para tentar novamente.', reply_markup=botoes_d_list())

        elif checagem:
            bot.send_message(mensagem.chat.id, f'Horário já possui um alarme configurado. Selecione /addden para tentar novamente ou /listden para listar os alarmes.', reply_markup=botoes_d_list())

        else:
            data['horario'] = horariotd
            env = bot.send_message(mensagem.chat.id, f'Agora, digite a descrição do horário, caso não deseje uma, digite "N"')
            bot.register_next_step_handler(env, respdentesadd2)

#Terceira etapa ao adicionar remédio, verifica se a resposta foi válida ou não e da prosseguimento ao armazenamento no banco
def respdentesadd2(mensagem):
    if mensagem.text[0] == '/':
        bot.send_message(mensagem.chat.id, f"Descrição inválida. Selecione /addden para tentar novamente.", reply_markup=botoes_d_list())
    else:
        if (mensagem.text).upper() == "N":
            data['descricao'] = "Alarme" 
        else:  
            data['descricao'] = mensagem.text

        horario = f"'{data['horario']}'"
        descricao = f"'{data['descricao']}'"

        bot.send_message(mensagem.chat.id, f"Alarme para escovar os dentes definido para {horario} com a descrição: {descricao}.", reply_markup=botoes_d_list())
        db.add_item(mensagem.chat.id, "'dentes'", 'NULL', horario, descricao)


#Remover
@bot.message_handler(commands=["rmvden"])
def removerdentes(mensagem):
    env = bot.send_message(mensagem.chat.id, "Digite o horário do alarme para escovar os dentes que deseja remover. (Horas:Minutos)")
    bot.register_next_step_handler(env, respdentesrmv)

#Segunda etapa ao remover dentes, registra a resposta da mensagem a ação de remover
def respdentesrmv(mensagem):
    horario = mensagem.text
    tem = db.check_item(horario, 'dentes',  mensagem.chat.id)
    horario = f"'{horario}'"
    temphoras = f"{horario}"
    temphoras = temphoras.replace("'", "")

    try:
        horas, minutos = temphoras.split(":")
    except ValueError:
        bot.send_message(mensagem.chat.id, f'Entrada não esperada, selecione /rmvden para tentar novamente.', reply_markup=botoes_d_list())
    else:
        if horas.isnumeric() == False or minutos.isnumeric == False:
            bot.send_message(mensagem.chat.id, f"Horário digitado inválido. Selecione /rmvden para tentar novamente ou /listrem para listar os horários.", reply_markup=botoes_d_list())
        else:
            if tem != None:
                db.delete_item("'dentes'", horario, mensagem.chat.id)
                bot.send_message(mensagem.chat.id, f"Alarme no horário {horario} removido.", reply_markup=botoes_d_list())
            else:
                bot.send_message(mensagem.chat.id, f"Não existe um alarme programado neste horário.", reply_markup=botoes_d_list())



#######
#Banho#
#######

#Menu Banho
@bot.message_handler(commands=["banho"])
def banho1(mensagem):
    texto = """
Que ação deseja realizar?

/addbnh - Adicionar alarme para banho.
/rmvbnh - Remover um alarme já configurado para banho.
/listbnh - Listar os horários já configurados para banho.
"""
    bot.send_message(mensagem.chat.id, texto, reply_markup=botoes_banho())

#Listar
@bot.message_handler(commands=["listbnh"])
def listarbanhos(mensagem):
    tabela = db.get_items("banho", mensagem.chat.id)
    tabela.sort()

    tabela_formato = ["Alarme %i: %s" % (index+1, value) for index, value in enumerate(tabela)]
    tabela_formatada = "\n".join(tabela_formato)

    if not tabela:
        bot.send_message(mensagem.chat.id, "Você não possui nenhum alarme definido. Selecione /banho para criar um.", reply_markup=botoes_b_list())
    else:
        bot.send_message(mensagem.chat.id, f"{tabela_formatada}\n\nSelecione /banho para criar ou remover um alarme.", reply_markup=botoes_b_list())

#Adicionar
@bot.message_handler(commands=["addbnh"])
def addbanho(mensagem):
    global data
    env = bot.send_message(mensagem.chat.id, "Digite o horário que quer adicionar para tomar banho (Horas:Minutos)")
    bot.register_next_step_handler(env, respbanhoadd)

#Segunda etapa ao adicionar banho, registra a resposta da mensagem a ação de adicionar
def respbanhoadd(mensagem):
    horariotd = mensagem.text
    temphoras = horariotd
    checagem = db.get_horarioexiste("remedio", mensagem.chat.id, f"{horariotd}")

    try:
        horas, minutos = temphoras.split(":")
    except ValueError:
        bot.send_message(mensagem.chat.id, f'Entrada não esperada, selecione /addbnh para tentar novamente.', reply_markup=botoes_b_list())
    else:
        if (horas.isnumeric() == False or minutos.isnumeric() == False or len(horas) != 2 or len(minutos) != 2):
            bot.send_message(mensagem.chat.id, f'Horário inválido. Selecione /addbnh para tentar novamente.', reply_markup=botoes_b_list())

        elif (int(horas) > 23 or int(horas) < 0) or (int(minutos) > 59 or int(minutos) < 0):
            bot.send_message(mensagem.chat.id, f'Horário inválido. Selecione /addbnh para tentar novamente.', reply_markup=botoes_b_list())

        elif checagem:
                    bot.send_message(mensagem.chat.id, f'Horário já possui um alarme configurado. Selecione /addbnh para tentar novamente ou /listbnh para listar os alarmes.', reply_markup=botoes_b_list())
        
        else:
            data['horario'] = horariotd
            env = bot.send_message(mensagem.chat.id, f'Agora, digite a descrição do horário, caso não deseje uma, digite "N"')
            bot.register_next_step_handler(env, respbanhoadd2)

#Terceira etapa ao adicionar dentes, verifica se a resposta foi válida ou não e da prosseguimento ao armazenamento no banco
def respbanhoadd2(mensagem):
    if mensagem.text[0] == '/':
        bot.send_message(mensagem.chat.id, f"Descrição inválida. Selecione /addbnh para tentar novamente.", reply_markup=botoes_b_list())
    else:
        if (mensagem.text).upper() == "N":
            data['descricao'] = "Alarme" 
        else:  
            data['descricao'] = mensagem.text

        horario = f"'{data['horario']}'"
        descricao = f"'{data['descricao']}'"

        bot.send_message(mensagem.chat.id, f"Alarme para banho definido para {horario} com a descrição: {descricao}.", reply_markup=botoes_b_list())
        db.add_item(mensagem.chat.id, "'banho'", 'NULL', horario, descricao)


#Remover
@bot.message_handler(commands=["rmvbnh"])
def removerbanho(mensagem):
    env = bot.send_message(mensagem.chat.id, "Digite o horário do alarme de banho que deseja remover. (Horas:Minutos)")
    bot.register_next_step_handler(env, respbanhormv)

#Segunda etapa ao remover remédio, registra a resposta da mensagem a ação de remover
def respbanhormv(mensagem):
    horario = mensagem.text
    tem = db.check_item(horario, 'banho',  mensagem.chat.id)
    horario = f"'{horario}'"
    temphoras = f"{horario}"
    temphoras = temphoras.replace("'", "")

    try:
        horas, minutos = temphoras.split(":")
    except ValueError:
        bot.send_message(mensagem.chat.id, f'Entrada não esperada, selecione /rmvbnh para tentar novamente.', reply_markup=botoes_b_list())
    else:
        if horas.isnumeric() == False or minutos.isnumeric == False:
            bot.send_message(mensagem.chat.id, f"Horário digitado inválido. Selecione /rmvbnh para tentar novamente ou /listrem para listar os horários.", reply_markup=botoes_b_list())
        else:
            if tem != None:
                db.delete_item("'banho'", horario, mensagem.chat.id)
                bot.send_message(mensagem.chat.id, f"Alarme no horário {horario} removido.", reply_markup=botoes_b_list())
            else:
                bot.send_message(mensagem.chat.id, f"Não existe um alarme programado neste horário.", reply_markup=botoes_b_list())


##########
#Checagem#
##########

@bot.message_handler(commands=["checagem"])
def checagem1(mensagem): 
    texto = """
Que ação deseja realizar?

/addcheck - Adicionar temporizador para checagem.
/rmvcheck - Remover temporizador para checagem.
/listcheck - Listar de quanto em quanto tempo está sendo feita a checagem.
"""
    bot.send_message(mensagem.chat.id, texto)

#Adicionar
@bot.message_handler(commands=["addcheck"])
def addcheck(mensagem):
    checagem = db.get_checagem(mensagem.chat.id)

    if not checagem:
        env = bot.send_message(mensagem.chat.id, "De quanto em quanto tempo deseja realizar a checagem? (Minutos - Max = 1440)")
        bot.register_next_step_handler(env, respchecagem1)
    else:
        bot.send_message(mensagem.chat.id, "Você já possui uma checagem definida, selecione /listcheck para listá-la.")

#Checa a mensagem introduzida na ação de checagem, processando se é uma resposta válida
def respchecagem1(mensagem):
    horario = mensagem.text
    if horario.isnumeric() == False or int(horario) > 1440 or int(horario) < 0:
        bot.send_message(mensagem.chat.id, f"Horário inválido, selecione /addcheck para tentar novamente.")
    else:
        db.add_checagem(mensagem.chat.id, 'NULL', horario)
        bot.send_message(mensagem.chat.id, f"A checagem será realizada a cada {horario} minutos.")

#Listar
@bot.message_handler(commands=["listcheck"])
def listarchecagem(mensagem):
    check = db.get_checagem(mensagem.chat.id)
    check = str(check)[1:-1]

    if not check:
        bot.send_message(mensagem.chat.id, "Você não definiu um horário pra checagem. Selecione /addcheck para definir um.")
    else:
        bot.send_message(mensagem.chat.id, f"Checagem sendo realizada a cada {check} minutos.\n\nSelecione /checagem1 para voltar ao menu de checagem.")

#Remover
@bot.message_handler(commands=["rmvcheck"])
def deletarchecagem(mensagem):
    env = bot.send_message(mensagem.chat.id, "Deseja realmente deletar o horário de checagem? (Sim/Não)")
    bot.register_next_step_handler(env, respdeletecheck)

#Confirmação para deletar o timer atual da checagem
def respdeletecheck(mensagem):
    resposta = mensagem.text

    if resposta.upper() == "SIM":
        db.delete_checagem(mensagem.chat.id)
        bot.send_message(mensagem.chat.id, "Checagem deletada. Selecione /menu para retornar ao menu.")
    else:
        bot.send_message(mensagem.chat.id, "Operação abortada. Selecione /menu para retornar ao menu.")

#Impede o bot de crashar caso a mensagem recebida seja algo que ele não processe
def verificar(mensagem):
        msg = mensagem.text
        if msg != None:
            return True

#Mensagem padrão do bot ao iniciá-lo
@bot.message_handler(commands=["menu", "start"])
def menu(mensagem):
    texto = """
Olá, bem-vindo a interface de configuração do PetIEEE! Selecione uma das opções a seguir (Clicando):

/alarme - Configurar uma agenda de alarmes
/checagem - Temporizador para checagem do idoso

Caso o bot não entenda o comando, o menu será reenviado
"""
    bot.send_message(mensagem.chat.id, texto, reply_markup=botoes_menu())

#Verificação de comando inválido
@bot.message_handler(func=verificar)
def erro(mensagem):
    texto = """
Comando não reconhecido, digite /menu para voltar ao menu.
"""
    bot.send_message(mensagem.chat.id, texto)

#Manter o bot rodando
bot.polling()