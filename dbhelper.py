import sqlite3


class DBHelper:
    #Iniciar o banco de dados
    def __init__(self, dbname="petieee.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname, check_same_thread=False)

    #Criar uma table alarme caso não exista
    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS tb_alarme (description text)"
        self.conn.execute(stmt)
        self.conn.commit()

    #Adicionar item na tabela de alarme
    def add_item(self, id_user, id_tipo, id_alarme, horario, descricao):
        stmt = f"INSERT INTO tb_alarme (id_user, id_tipo, id_alarme, horario, descricao) VALUES ({id_user}, {id_tipo}, {id_alarme}, {horario}, {descricao})"
        self.conn.execute(stmt)
        self.conn.commit()

    #Realiza a checagem de um item na tabela de checagem
    def add_checagem(self, id_user, id_checagem, checagem_minutos):
        stmt = f"INSERT INTO tb_checagem (id_user, id_checagem, checagem_minutos) VALUES ({id_user}, {id_checagem}, {checagem_minutos})"
        self.conn.execute(stmt)
        self.conn.commit()

    #Deleta um item da tabela de alarme
    def delete_item(self, id_tipo, horario, id_user):
        stmt = f"DELETE FROM tb_alarme WHERE id_tipo = {id_tipo} and horario = {horario} and id_user = {id_user}"
        self.conn.execute(stmt)
        self.conn.commit()

    #Deleta um item da tabela de checagem
    def delete_checagem(self, id_user):
        stmt = f"DELETE FROM tb_checagem WHERE id_user = {id_user}"
        self.conn.execute(stmt)
        self.conn.commit()

    #Recebe um item da tabela de checagem
    def get_checagem(self, id_user):
        stmt = f"SELECT checagem_minutos FROM tb_checagem where id_user = {id_user}"
        return [x[0] for x in self.conn.execute(stmt)]

    #Recebe um horario + descrição da tabela de alarme
    def get_items(self, id_tipo, id_user):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT horario, descricao FROM tb_alarme WHERE id_tipo = '{id_tipo}' and id_user = {id_user}")
        ans= cursor.fetchall()
        return ans

    #Verifica se o horário existe na tabela de alarme
    def get_horarioexiste(self, id_tipo, id_user, horario):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT horario FROM tb_alarme WHERE id_tipo = '{id_tipo}' and id_user = {id_user} and horario = '{horario}'")
        ans= cursor.fetchall()
        return ans    

    #Recebe o valor de checagem da tablea de checagem
    def get_checagem2(self, id_user):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT checagem_minutos FROM tb_checagem WHERE id_user = '{id_user}'")
        ans= cursor.fetchone()
        return ans

    #Recebe um horário da tabela de alarme
    def check_item(self, horario, id_tipo, id_user):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT horario FROM tb_alarme WHERE id_tipo = '{id_tipo}' AND horario = '{horario}' AND id_user = '{id_user}'")
        result = cursor.fetchone()
        return result