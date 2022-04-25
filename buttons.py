from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

#Criação dos botões inline disponíveis no menu
def botoes_menu():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("⏰", callback_data="cb_alarme"),
                               InlineKeyboardButton("❓", callback_data="cb_checagem"))
    return markup

#Criação dos botões inline disponíveis na aba de alarmes
def botoes_alarme():
    markup = InlineKeyboardMarkup()
    markup.row_width = 4
    markup.add(InlineKeyboardButton("💊", callback_data="cb_alarme_r1"),
                               InlineKeyboardButton("🦷", callback_data="cb_alarme_d1"),
                               InlineKeyboardButton("🚿", callback_data="cb_alarme_b1"),
                               InlineKeyboardButton("🔙", callback_data="cb_menu_voltar"))
    return markup

#Criação dos botões inline disponíveis na aba de alarmes de remédios
def botoes_remedio():
    markup = InlineKeyboardMarkup()
    markup.row_width = 4
    markup.add(InlineKeyboardButton("➕", callback_data="cb_remedio_add"), 
                                InlineKeyboardButton("❌", callback_data="cb_remedio_rmv"),
                                InlineKeyboardButton("📝", callback_data="cb_remedio_lst"),
                                InlineKeyboardButton("🔙", callback_data="cb_alarme_voltar"))
    return markup

#Criação dos botões inline disponíveis na aba de alarmes de escovar os dentes
def botoes_dente():
    markup = InlineKeyboardMarkup()
    markup.row_width = 4
    markup.add(InlineKeyboardButton("➕", callback_data="cb_dentes_add"), 
                                InlineKeyboardButton("❌", callback_data="cb_dentes_rmv"),
                                InlineKeyboardButton("📝", callback_data="cb_dentes_lst"),
                                InlineKeyboardButton("🔙", callback_data="cb_alarme_voltar"))
    return markup

#Criação dos botões inline disponíveis na aba de alarmes de banho
def botoes_banho():
    markup = InlineKeyboardMarkup()
    markup.row_width = 4
    markup.add(InlineKeyboardButton("➕", callback_data="cb_banho_add"), 
                                InlineKeyboardButton("❌", callback_data="cb_banho_rmv"),
                                InlineKeyboardButton("📝", callback_data="cb_banho_lst"),
                                InlineKeyboardButton("🔙", callback_data="cb_alarme_voltar"))
    return markup

#Criação dos botões para retornar a listagem
def botoes_r_list():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("🔙", callback_data=f"cb_r_list_voltar"))
    return markup

def botoes_d_list():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("🔙", callback_data=f"cb_d_list_voltar"))
    return markup

def botoes_b_list():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("🔙", callback_data=f"cb_b_list_voltar"))
    return markup