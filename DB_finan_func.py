# ___ FUNCÕES E BANCO DE DADOS

import re
import sqlite3
from tkinter import messagebox
from datetime import date
import calendar
from datetime import datetime
import pandas as pd

# ___ CONEXÃO E CURSOR DO SQLite
conexao = sqlite3.connect('DB-finan.db')
cursor = conexao.cursor()


def salvar_conta(titular, num, banco, saldo_atual):  # -> EXITO = 'ok' + messagebox / FALHA = 'erro' + messagebox
    if titular and num and banco and saldo_atual:  # -> VERIFICA SE TODOS OS DADOS EXISTEM, SE NÃO RETORNA 'erro'
        try:  # -> TENTA CRIAR TABELA E INSERIR VALORES

            # ___ CRIANDO A TABELA contas
            cursor.execute('''
                    CREATE TABLE IF NOT EXISTS contas (
                        titular TEXT NOT NULL,
                        num INTEGER NOT NULL,
                        banco TEXT NOT NULL,
                        saldo REAL NOT NULL)''')

            # ___ INSERINDO VALORES DA CONTA
            cursor.execute('''INSERT INTO contas (titular, num, banco, saldo) 
                                    VALUES (?,?,?,?)''', (titular, num, banco, saldo_atual))

            conexao.commit()  # -> CONFIRMA AS ALTERAÇÕES NO BANCO DE DADOS
            messagebox.showinfo('Sucesso!', f'Conta {num} foi adicionada')  # -> MSG DE SUCESSO
            return 'ok'  # -> EXITO = RETURN 'ok'
        except Exception as e:  # -> CAPTURA ERROS DE SQL OU EXCEÇÃO GERAL
            messagebox.showerror("Oops", f'Erro ao criar tabela: {e}')  # -> MSG DE ERRO
            return 'erro'  # -> FALHA = RETURN 'erro'
    else:  # -> SE ALGUM CAMPO ESTIVER VAZIO
        messagebox.showerror("Oops!", 'Erro de campo vazio')  # -> MSG DE ERRO DE CAMPO VAZIO
        return 'erro'  # -> FALHA = RETURN 'erro'


def salvar_movimentacao_corriqueira(data, nome, valor, conta,
                                    tipo):  # -> EXITO = 'salvo' + messagebox / FALHA = 'erro' + messagebox
    # CHECAGEM DE PADRONIZAÇÃO DA DATA
    padrao_requirido = re.compile(r'\d{4}-\d{2}-\d{2}')  # -> CRIA O PADRÃO DE DATA PERMITIDO (YYYY-MM-DD)
    if not padrao_requirido.match(data):  # -> SE NÃO ESTIVER NO PADRÃO = RETURN ERRO
        messagebox.showerror("ops",
                             f'Insira a data no formmato correto\n"yyyy-mm-dd"')  # -> MSG DE FORMATO DE DATA INCORRETO
        return 'erro'  # -> FALHA = RETURN 'erro'
    else:  # -> SE ESTIVER NO PADRÃO

        try:  # -> TENTA TRANSFORMAR A STRING EM OBJETO DATE
            data_obj = datetime.strptime(data, '%Y-%m-%d').date()
            if data_obj < date.today():  # -> BLOQUEIO PARA DATAS PASSADAS
                messagebox.showerror('Oops!',
                                     'Você só pode colocar datas futuras')  # -> MSG DE BLOQUEIO DE DATA PASSADA
                return 'erro'  # -> FALHA = RETURN 'erro'
        except:  # -> SE FALHAR NA CONVERSÃO DA DATA
            messagebox.showerror('Ops', 'Você não inseriu uma data valida')  # -> MSG DE DATA INVÁLIDA
            return 'erro'  # -> FALHA = RETURN 'erro'

    # PROCESSO DE VERIFICAÇÃO E REGISTRO DAS INFORMAÇÕES
    if data and nome and valor and conta and tipo:  # -> CHECA INTEGRIDADE DOS DADOS
        try:  # -> TENTA CRIAR A TABELA movimentos E INSERIR OS DADOS
            nome = nome.strip().lower()  # -> FORMATA O NOME (SEM ESPAÇOS E EM MINÚSCULAS)
            valor = converter_valor(valor)
            if tipo == 'SAIDA':  # -> AJUSTA O SINAL DO VALOR CONFORME O TIPO SELECIONADO
                valor = -abs(valor)
            else:
                valor = abs(valor)

            # ___ CRIANDO A TABELA movimentos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS movimentos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data DATE NOT NULL,
                    nome TEXT NOT NULL,
                    valor REAL NOT NULL,
                    conta TEXT NOT NULL)''')

            # ___ INSERINDO OS DADOS NO BANCO
            cursor.execute('''INSERT INTO movimentos (data, nome, valor, conta) 
                    VALUES (?,?,?,?)''', (data, nome, valor, conta))
            conexao.commit()  # -> CONFIRMA A INSERÇÃO NO BANCO
            messagebox.showinfo("Sucesso!", f'Movimentação foi adicionada')  # -> MSG DE SUCESSO
            return 'salvo'  # -> EXITO = RETURN 'salvo'

        except sqlite3.Error as erro:  # -> CAPTURA ERROS ESPECÍFICOS DO SQLITE
            messagebox.showerror("ops", f'{erro}')  # -> MSG DE ERRO DO BANCO
            return 'erro'  # -> FALHA = RETURN 'erro'
        except Exception as e:  # -> CAPTURA ERROS GERAIS
            messagebox.showerror("ops", f'{e}')  # -> MSG DE ERRO GERAL
            return 'erro'  # -> FALHA = RETURN 'erro'
    else:  # -> CAMPOS FALTANTES
        messagebox.showerror("ops", 'Erro de campo vazio')  # -> MSG DE CAMPO VAZIO
        return 'erro'  # -> FALHA = RETURN 'erro'


def converter_valor(valor):  # -> EXITO = RETURN valor (float) / FALHA = RETURN None OU MSG DE ERRO
    if valor and valor != 0:
        try:  # -> TRATA STRING E CONVERTE PARA FLOAT
            valor = str(valor).replace(',', '.').replace("R$", "").replace("$", "").strip()
            return float(valor)  # -> EXITO = RETURN FLOAT CONVERTIDO
        except Exception as e:  # -> ERRO DE FORMATO INCORRETO
            messagebox.showerror("ops", f'Erro ao converter valor do tipo: {e}')
            return None  # -> FALHA = RETURN None
    else:  # -> SE VALOR FOR NULO/VAZIO
        messagebox.showerror('Ops','Erro de campo vazio "valor"')
        return None  # -> RETORNA None


def mostrar_nomes_num_contas():  # -> EXITO = RETURN list[(titular, num)] / FALHA = RETURN ['Registre...'] OU None
    try:
        cursor.execute('''SELECT titular, num, saldo FROM contas''')  # -> BUSCA TODAS AS CONTAS
        dados_fr_conta = cursor.fetchall()
        contas = []
        for dado in dados_fr_conta:
            contas.append((dado[0], dado[1]))  # -> MONTA LISTA DE TUPLAS COM TITULAR E NÚMERO DA CONTA
        return contas  # -> EXITO = RETURN LISTA DE CONTAS
    except sqlite3.OperationalError as e:
        if "no such table" in str(e):  # -> SE A TABELA AINDA NÃO EXISTIR
            return ['Registre uma conta antes']  # -> RETORNA AVISO EM LISTA
        else:
            messagebox.showerror("Erro SQL", f"Ocorreu um erro de execução: {e}")  # -> MSG DE ERRO SQL
            return None  # -> FALHA = RETURN None
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro inesperado: {e}")  # -> MSG DE ERRO GERAL
        return None  # -> FALHA = RETURN None


def buscar_conta_by_num(num):  # -> EXITO = RETURN list[titular, num, saldo_calculado, banco] / FALHA = RETURN messagebox
    hoje = date.today()
    try:
        cursor.execute('''SELECT titular, num, saldo, banco FROM contas WHERE num = ?''',
                       (num,))  # -> BUSCA DADOS DE UMA CONTA ESPECÍFICA
        resultado = cursor.fetchone()
        saldo = resultado[2]
        total_saldo = [0]

        try:  # -> TENTA SOMAR MOVIMENTAÇÕES REALIZADAS ATÉ A DATA DE HOJE
            cursor.execute('''SELECT SUM(valor)
            FROM movimentos
            WHERE data <= ?  AND conta = ? ''', (hoje, num))
            resposta1 = cursor.fetchone()[0]
            if resposta1:
                total_saldo.append(resposta1)

        except:
            pass

        resultado_final = [resultado[0], resultado[1], saldo + sum(total_saldo),
                           resultado[3]]  # -> CONSOLIDA OS DADOS E O SALDO ATUALIZADO DAH CONTA

        return resultado_final  # -> EXITO = RETURN LISTA COM DADOS DA CONTA E SALDO
    except sqlite3.OperationalError as e:
        messagebox.showerror('Ops', f'Erro : {e}')  # -> MSG DE ERRO DE BANCO


def pegar_movimentaçoes_do_mes_total(mes, ano,
                                     conta):  # -> EXITO = RETURN 'R$X.XX' / FALHA OU SEM DADOS = RETURN STRING AVISO
    mes = f'{mes:02d}'
    try:
        try:  # -> SOMA TODAS AS MOVIMENTAÇÕES DO MÊS ESPECIFICADO
            cursor.execute('''SELECT SUM(valor)
             FROM movimentos
              WHERE strftime('%Y-%m', data) = ? AND conta = ?''',
                           (f'{ano}-{mes}', conta))
            resultado = cursor.fetchone()[0]
            if not resultado:
                resultado = 0
        except:
            resultado = 0
        if resultado and resultado != 0:
            return f'R${resultado:.2f}'  # -> EXITO = RETURN VALOR FORMATADO 'R$X.XX'
        else:
            return 'Não tem\nmovimentação\ncadastrada(mês)'  # -> SEM DADOS = RETURN AVISO
    except:
        return 'Não tem\nmovimentação\ncadastrada(mês)'  # -> FALHA = RETURN AVISO


def calcular_saldo_ate_fim_do_mes(hoje, mes, ano, conta,
                                  scr=False):  # -> EXITO = RETURN STRING FORMATADA COM SALDO / FALHA = RETURN STRING AVISO
    mes = f'{mes:02d}'
    hoje = f'{hoje:02d}'
    try:
        final_do_mes = calendar.monthrange(int(ano), int(mes))[1]  # -> IDENTIFICA O ÚLTIMO DIA DO MÊS

        cursor.execute('''SELECT saldo FROM contas WHERE num = ?''', (conta,))  # -> PEGA O SALDO BASE DA CONTA
        resultado = cursor.fetchone()
        saldo = resultado[0]
        try:  # -> SOMA OS MOVIMENTOS FUTUROS DA DATA ATUAL ATÉ O FIM DO MÊS
            cursor.execute('''SELECT SUM(valor)
             FROM movimentos
             WHERE data >= ? AND data <= ? AND conta = ?''', (hoje, f'{ano}-{mes}-{final_do_mes}', conta))
            resultado = cursor.fetchone()[0]
            if not resultado:
                resultado = 0
        except:
            resultado = 0

        total = saldo + resultado  # -> CALCULA O SALDO TOTAL PROJETADO
        if scr:
            return f'R${total:.2f}'  # -> EXITO (FLAG SCR) = RETURN 'R$X.XX'
        else:
            return f'\n{ano}-{mes}-{final_do_mes}\nR$ {total:.2f}'  # -> EXITO = RETURN DATA FIM + SALDO FORMATADO
    except:
        return f'Não tem\nmovimentações\nno futuro'  # -> FALHA = RETURN STRING DE AVISO


def pegar_todas_as_mov_do_mes_ano(conta, mes, ano, margem,
                                  tudo=False):  # -> EXITO = RETURN (resultado_movs) / FALHA OU VAZIO = RETURN ['None']
    if tudo:
        query_movimentos = ''
    else:
        query_movimentos = 'LIMIT 600'  # -> DEFINE LIMITE DE REGISTROS POR PERFORMANCE NA SCROLLFRAME

    if margem == 'Ano':  # -> CONSULTA COM FILTRO ANUAL
        ano = str(ano)
        try:
            cursor.execute(f'''SELECT data, nome, valor, id
                 FROM movimentos WHERE strftime('%Y', data) = ? AND conta = ?
                 ORDER BY data ASC {query_movimentos}''', (ano, conta))
            resultado = cursor.fetchall()
            if not resultado:
                resultado = 0
        except sqlite3.OperationalError:
            resultado = 0

        if resultado == 0:
            return ['None']  # -> SEM REGISTROS NO ANO = RETURN ['None']
        else:
            return resultado  # -> EXITO ANUAL = RETURN LISTA_MOVS


    elif margem == 'Mes':
        mes = f'{mes:02d}'

    elif margem == 'Mes - passado':
        mes -= 1
        mes = f'{mes:02d}'

    try:  # -> CONSULTA COM FILTRO MENSAL
        cursor.execute(f'''SELECT data, nome, valor, id
             FROM movimentos WHERE strftime('%Y-%m', data) = ? AND conta = ?
             ORDER BY data ASC {query_movimentos}''', (f'{ano}-{mes}', conta))
        resultado = cursor.fetchall()
        if not resultado:
            resultado = 0
    except sqlite3.OperationalError:
        resultado = 0

    if resultado == 0:
        return ['None']  # -> SEM REGISTROS NO MÊS = RETURN ['None']
    else:
        return resultado  # -> EXITO MENSAL = RETURN LISTA_MOVS


def pegar_movimentacao_data_para_graficos(conta, mes, margem,
                                          tipo):  # -> EXITO = RETURN (datas, vendas_por_datas, nomes) / FALHA = RETURN (['None'], ['None'], ['None'])
    ano = str(date.today().year)

    if margem == 'Ano':  # -> BUSCA DADOS DO ANO TODO
        try:
            if tipo == 'Total':  # -> FILTRA TODAS AS MOVIMENTAÇÕES AGRUPADAS POR DATA E SOMADAS
                try:
                    cursor.execute('''SELECT data, GROUP_CONCAT(nome, '\n') AS nomes, SUM(valor) AS valor_total
                                    FROM movimentos
                                    WHERE strftime('%Y', data) = ? AND conta = ?
                                    GROUP BY data
                                    ORDER BY data ASC''', (ano, conta))
                    resultado = cursor.fetchall()
                    if not resultado:
                        resultado = None
                except:
                    resultado = None

            elif tipo == 'Entradas':  # -> FILTRA APENAS ENTRADAS (> 0) AGRUPADAS POR DATA
                try:
                    cursor.execute('''SELECT data, GROUP_CONCAT(nome, '\n') AS nomes, SUM(valor) AS valor_total 
                                    FROM movimentos
                                    WHERE valor > 0 AND strftime('%Y', data) = ? AND conta = ?
                                    GROUP BY data
                                    ORDER BY data ASC''', (ano, conta))
                    resultado = cursor.fetchall()
                    if not resultado:
                        resultado = None
                except:
                    resultado = None

            else:  # -> FILTRA APENAS SAÍDAS (< 0) AGRUPADAS POR DATA
                try:
                    cursor.execute('''SELECT data, GROUP_CONCAT(nome, '\n') AS nomes, SUM(valor) AS valor_total 
                                    FROM movimentos
                                    WHERE valor < 0 AND strftime('%Y', data) = ? AND conta = ?
                                    GROUP BY data
                                    ORDER BY data ASC''', (ano, conta))
                    resultado = cursor.fetchall()
                    if not resultado:
                        resultado = None
                except:
                    resultado = None

            if resultado:  # -> ORGANIZA LISTAS FINAIS PARA O GRÁFICO (EIXO X, VALORES, RÓTULOS)
                datas = [r[0] for r in resultado]
                nomes = [r[1] for r in resultado]
                vendas_por_datas = [r[2] for r in resultado]
            else:  # -> SE O BANCO ESTIVER VAZIO NO PERÍODO
                datas = ['Banco Vazio']
                nomes = ['Banco Vazio']
                vendas_por_datas = ['Banco Vazio']
            return datas, vendas_por_datas, nomes  # -> EXITO ANUAL = RETURN (LISTA_DATAS, LISTA_VALORES, LISTA_NOMES)
        except sqlite3.OperationalError as e:  # -> ERROS DE BANCO SQL
            messagebox.showerror('Ops', f'Erro com SQl : {e}')
            return ['None'], ['None'], ['None']  # -> FALHA = RETURN (['None'], ['None'], ['None'])
        except Exception as e:  # -> ERROS GERAIS
            messagebox.showerror('Ops', f'Erro inesperado : {e}')
            return ['None'], ['None'], ['None']  # -> FALHA = RETURN (['None'], ['None'], ['None'])

    elif margem == 'Mes':
        mes = f'{mes:02d}'

    elif margem == 'Mes - passado':
        if mes == 1:
            mes = 12
            ano = int(ano) - 1
        else:
            mes -= 1
        mes = f'{mes:02d}'

    try:  # -> BUSCA DADOS COM FILTRO MENSAL AGRUPANDO DATAS PARA EVITAR SOBREPOSIÇÃO NO MATPLOTLIB
        if tipo == 'Total':  # -> FILTRA TUDO DO MÊS
            try:
                cursor.execute('''SELECT data, GROUP_CONCAT(nome, '\n') AS nomes, SUM(valor) AS valor_total 
                                FROM movimentos
                                WHERE strftime('%Y-%m', data) = ? AND conta = ?
                                GROUP BY data
                                ORDER BY data ASC''', (f'{ano}-{mes}', conta))
                resultado = cursor.fetchall()
                if not resultado:
                    resultado = None
            except:
                resultado = None

        elif tipo == 'Entradas':  # -> FILTRA APENAS ENTRADAS (> 0) DO MÊS
            try:
                cursor.execute('''SELECT data, GROUP_CONCAT(nome, '\n') AS nomes, SUM(valor) AS valor_total
                                FROM movimentos
                                WHERE valor > 0 AND strftime('%Y-%m', data) = ? AND conta = ?
                                GROUP BY data
                                ORDER BY data ASC''', (f'{ano}-{mes}', conta))
                resultado = cursor.fetchall()
                if not resultado:
                    resultado = None
            except:
                resultado = None

        else:  # -> FILTRA APENAS SAÍDAS (< 0) DO MÊS
            try:
                cursor.execute('''SELECT data, GROUP_CONCAT(nome, '\n') AS nomes, SUM(valor) AS valor_total
                                FROM movimentos
                                WHERE valor < 0 AND strftime('%Y-%m', data) = ? AND conta = ?
                                GROUP BY data
                                ORDER BY data ASC''', (f'{ano}-{mes}', conta))
                resultado = cursor.fetchall()
                if not resultado:
                    resultado = None
            except:
                resultado = None

        if resultado:  # -> ORGANIZA LISTAS FINAIS DO MÊS
            datas = [r[0] for r in resultado]
            nomes = [r[1] for r in resultado]
            vendas_por_datas = [r[2] for r in resultado]
        else:  # -> BANCO VAZIO NO MÊS
            datas = ['Banco Vazio']
            nomes = ['Banco Vazio']
            vendas_por_datas = ['Banco Vazio']
        return datas, vendas_por_datas, nomes  # -> EXITO MENSAL = RETURN (LISTA_DATAS, LISTA_VALORES, LISTA_NOMES)

    except sqlite3.OperationalError as e:  # -> ERRO DE SQL
        messagebox.showerror('Ops', f'Erro com SQl : {e}')
        return ['None'], ['None'], ['None']  # -> FALHA = RETURN (['None'], ['None'], ['None'])
    except Exception as e:  # -> ERRO INESPERADO
        messagebox.showerror('Ops', f'Erro inesperado : {e}')
        return ['None'], ['None'], ['None']  # -> FALHA = RETURN (['None'], ['None'], ['None'])


def pegar_id_todas_movimentos(conta):  # -> EXITO = RETURN list[str_ids] / FALHA OU VAZIO = RETURN ['none'] OU ['None']
    try:
        cursor.execute('''SELECT id FROM movimentos
        WHERE conta = ?''', (conta,))  # -> BUSCA TODOS OS IDS DE MOVIMENTAÇÕES DE UMA CONTA
        resultado = cursor.fetchall()
        if not resultado:
            return ['none']  # -> SEM IDS = RETURN ['none']
        else:
            valores = [str(r[0]) for r in resultado]  # -> CONVERTE CADA ID PARA STRING PARA USAR NO CTKOPTIONMENU
            return valores  # -> EXITO = RETURN LISTA DE IDS EM STRING
    except:
        return ['None']  # -> FALHA = RETURN ['None']


def update_movimentos(ident, coluna, valor):  # -> EXITO = messagebox + RETURN messagebox / FALHA = RETURN None
    if coluna == 'valor':  # -> SE FOR EDITAR O VALOR, FAZ A TRATATIVA DE FLOAT
        valor = converter_valor(valor)
    if not valor:  # -> SE A CONVERSÃO RETORNAR NULA = CANCELA O UPDATE
        return None
    if coluna == 'data':  # -> SE FOR EDITAR A DATA, VALIDA O PADRÃO YYYY-MM-DD
        valor = checar_padrao(valor)
        if not valor:  # -> SE A DATA FOR INVÁLIDA = CANCELA O UPDATE
            return None
    try:  # -> EXECUTA A ATUALIZAÇÃO DINÂMICA DA COLUNA PELO ID
        cursor.execute(f'''UPDATE movimentos
        SET {coluna} = ?
        WHERE id = ?''', (valor, ident))
        conexao.commit()  # -> PERSISTE A ALTERAÇÃO NO BANCO DE DADOS
        return messagebox.showinfo('Sucesso', 'Update concluído com sucesso')  # -> EXITO = MSG SUCESSO
    except Exception as e:  # -> CAPTURA ERROS NO UPDATE
        messagebox.showerror('Ops', f'{e}')  # -> MSG DE ERRO
        return None  # -> FALHA = RETURN None


def checar_padrao(data):  # -> EXITO = RETURN data_obj (date) / FALHA = RETURN None + messagebox
    # CHECAGEM DE PADRONIZAÇÃO DA DATA
    padrao_requirido = re.compile(r'\d{4}-\d{2}-\d{2}')  # -> CRIA O PADRÃO DE DATA PERMITIDO
    if not padrao_requirido.match(data):  # -> SE NÃO ESTIVER NO PADRÃO = RETURN None
        messagebox.showerror("ops",
                             f'Insira a data no formmato correto\n"yyyy-mm-dd"')  # -> MSG DE FORMATO DE DATA INCORRETO
        return None  # -> FALHA = RETURN None
    else:  # -> SE ESTIVER NO PADRÃO

        try:  # -> TENTA TRANSFORMAR A STRING EM OBJETO DATE
            data_obj = datetime.strptime(data, '%Y-%m-%d').date()
            return data_obj  # -> EXITO = RETURN OBJETO DATE
        except:  # -> SE FALHAR NA CONVERSÃO
            return None  # -> FALHA = RETURN None

def calcular_saldo_ate(data, conta):
    data = checar_padrao(data)
    if not data: return None
    elif data <= date.today():
        messagebox.showerror('Ops','Só pode datas futuras')
        return None
    else:
        try:
            cursor.execute('''SELECT saldo FROM contas WHERE num = ?''', (conta,))
            saldo = cursor.fetchone()[0]
        except Exception as e:
            messagebox.showerror('Ops', f'{e}')
            return None
        try:
            cursor.execute('''SELECT SUM(valor) FROM movimentos
            WHERE conta = ? AND data <= ?''', (conta,data))
            movimentos = cursor.fetchone()[0]
        except:
            movimentos = 0
        if saldo:
            return saldo + movimentos
        else:
            return 'Sem saldo'

def sql_to_excel(conta):
    query = f'''SELECT id, data, nome, valor from movimentos
        WHERE conta = "{conta}"'''
    try:
        df = pd.read_sql_query(query, conexao, index_col='id')
        df.to_excel('relatorio.xlsx', index=True)
    except Exception as e: messagebox.showerror('Ops', f'{e}')



