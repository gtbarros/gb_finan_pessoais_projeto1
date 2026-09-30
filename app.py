import customtkinter as ctk
import sys
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from DB_finan_func import *
from atributos_fixos import *
from datetime import date
import matplotlib.pyplot as plt

# DATA
hoje = date.today()
mes = hoje.month
ano = hoje.year
for m in meses:
    if m == mes:
        mes_texto = meses[m]

# IMAGENS DO APP


# APPARENCIA "DARK" (NÃO FIZ MODO LIGHT)
ctk.set_appearance_mode('dark')
tam_principal = f"{largura}x{altura}"
tam_principal_esticado = f"{largura+100}x{altura+100}"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        # CONFIGURAÇÕES VISUAIS

        self.geometry(tam_principal)
        self.title("Sistema Financeiro")
        self.attributes("-transparentcolor", "#000001")
        self.configure(fg_color=PRIMARIA)

        # FONTES PARA UTILIZAR
        self.fonte_titulo = ctk.CTkFont(family='Segoe UI', size=30, weight='bold',
                                        slant='italic')
        self.fonte_linhaM = ctk.CTkFont(family='Segoe UI', size=17, weight='bold',
                                        slant='italic')
        self.fonte_linham = ctk.CTkFont(family='Segoe UI', size=13, weight='bold',
                                        slant='italic')
        self.fonte_linhamin = ctk.CTkFont(family='Segoe UI', size=10, weight='bold',
                                        slant='italic')

        # CHAMA LOGIN PAGE
        self.inter_login()

    # FUNÇÃO PARA LIMPAR
    def limpar_janela(self):
        for janela in self.winfo_children():
            janela.destroy()
        def fechar_tudo():
            self.quit()
            self.destroy()
            sys.exit(0)
        self.protocol("WM_DELETE_WINDOW", fechar_tudo)






    # ___ INTERMEDIAÇÃO DE LOGIN___
    def inter_login(self):
        self.protocol("WM_DELETE_WINDOW", "")
        contas = mostrar_nomes_num_contas()
        if contas and contas[0] != 'Registre uma conta antes':
            self.limpar_janela()
            self.geometry('390x55')
            contas_p_visualizar = [f'{conta[0]}-{conta[1]}' for conta in contas]
            barra_selecao_tipo = ctk.CTkOptionMenu(
                master=self,
                values=contas_p_visualizar, width=50, height=30,
                corner_radius=10, fg_color=AZUL, text_color=BRANCO2,
                button_color=AZUL, font=self.fonte_linhaM)
            barra_selecao_tipo.pack(side='left', padx=(10, 0), pady=10)
            barra_selecao_tipo.pack_propagate(False)
            botao_avancar = ctk.CTkButton(self, text='AVANÇAR', width=125, height=50,
                                         corner_radius=0, fg_color=AZUL, border_color=CINZA,
                                         font=self.fonte_linham, text_color=BRANCO,
                                         hover_color=TERCIARIA, command=lambda: self.prox_pagina(buscar_conta_by_num(barra_selecao_tipo.get().split('-',1)[1])),
                                         border_width=0)
            botao_avancar.pack(pady=10, padx=(10,0), side='left')

        else:
            messagebox.showinfo('Atenção', '''Você não tem nenhuma conta registrada,
             vamos te redirecionar para aba de criação de contas''')
            self.withdraw()
            self.janela_add_conta(primeira_vez=True)






    # PROX_PAGINA
        # FROM FUNCOES
            # PRIMEIRO VERIFICA O LOGIN COM VERIFICAR_ENTRY
        # ELEMENTOS
            # 1 FRAME DATA
            # 1 FRAME GRAFICOS (3 GRAFICOS)
            # 1 FRAME
                # 3 BOTOES (ADD, ACCOUNTS, VIEW)
    def prox_pagina(self, conta):

                    verificar_integridade_dados(conta)

                    self.limpar_janela()
                    self.configure(fg_color=PRIMARIA)
                    self.geometry(tam_principal)
                    conta = buscar_conta_by_num(conta[1])


                                        # ___ FRAME DE DATAS ___
                    frame_back_data = ctk.CTkFrame(self, fg_color=AZUL, width=largura,
                                                   height= 100)
                    frame_back_data.pack(fill= 'x', side= 'top')


                                        # ___ TEXTO INDICANDO CONTA ___
                    ctk.CTkLabel(frame_back_data, text=f'{conta[0]}-{conta[1]}', height=20, width=100,
                                 fg_color=AZUL, corner_radius=30, text_color=BRANCO2,
                                 font=self.fonte_linham).place(x=largura/2-(100-13), y=0)


                                        # ___ BOTAO ESCOLHER CONTA ___
                    botao_mudar_conta = ctk.CTkButton(frame_back_data, text='Mudar Conta', width=65, height=1,
                                                  corner_radius=0, fg_color=BRANCO, border_color=CINZA,
                                                  font=self.fonte_linhamin, text_color=PRETO,
                                                  hover_color=TERCIARIA, command=lambda: self.inter_login(),
                                                  border_width=0)
                    botao_mudar_conta.place(x=largura -70, y=5)


                    ctk.CTkLabel(frame_back_data, text= f'{mes_texto.upper()}', height=50, width=150,
                                 fg_color=AZUL, corner_radius = 30, text_color= BRANCO2,
                                 font  = self.fonte_titulo).place(x= 10, y=40)

                    ctk.CTkLabel(frame_back_data, text=f'{ano}', height=50, width=150,
                                 fg_color=AZUL, corner_radius=30, text_color=BRANCO2,
                                 font=self.fonte_titulo).place(x=(largura//2)+50, y=40)

                                        # ___ FRAME GRAFICO (MAIS EM CIMA)
                    frame_grafico3 = ctk.CTkFrame(self, fg_color=TERCIARIA,
                                                  height=altura //3 -100, width=140,
                                                  border_width=0, border_color=CINZA, corner_radius=5)
                    frame_grafico3.pack(side='top', pady=(30,0))
                    frame_grafico3.pack_propagate(False)

                    ctk.CTkLabel(frame_grafico3, text=f'Saldo atual\nR${conta[2]:.2f}', height=altura//3-150, width=100,
                                 fg_color=TERCIARIA, corner_radius=10, text_color=BRANCO,
                                 font=self.fonte_linham).pack(expand= True, fill= 'both')

                    # ___CONTAINER INFERIOR ONDE POSSUI DOS FRAME COM INFORMAÇÃO___
                            #___MOVIMENTACOES & PREVISÃO DO SALDO FIM DO MES___
                    container_inferior = ctk.CTkFrame(self, fg_color=PRIMARIA, height=altura//3-100)
                    container_inferior.pack(side='top', fill='x', pady=(50,0))



                                            #___ FRAME 1 - GRAFICOS ___
                    frame_grafico1 = ctk.CTkFrame(container_inferior, fg_color=TERCIARIA,
                                                  height=altura//3-100, width=140,
                                                  border_width=0, border_color=CINZA)
                    frame_grafico1.pack(side= 'left', padx= (50,0))
                    frame_grafico1.pack_propagate(False)
                    ctk.CTkLabel(frame_grafico1, text=f'Movimentação',
                                 fg_color=TERCIARIA, corner_radius=0, text_color=BRANCO,
                                 height=1, width=1,
                                 font=self.fonte_linham).pack(pady=(20,0))
                    ctk.CTkLabel(frame_grafico1, text=f'(mes)',
                                 fg_color=TERCIARIA, corner_radius=5, text_color=BRANCO,
                                 height=1, width=1,
                                 font=self.fonte_linhamin).pack()
                    ctk.CTkLabel(frame_grafico1, text=f'{pegar_movimentaçoes_do_mes_total(mes,ano,conta[1])}',
                                 fg_color=TERCIARIA, corner_radius=0, text_color=BRANCO,
                                 height=1, width=1,
                                 font=self.fonte_linhamin).pack(pady= (10,0))



                                            #___ FRAME 2 - GRAFICOS ___
                    frame_grafico2 = ctk.CTkFrame(container_inferior, fg_color=TERCIARIA,
                                                  height=altura // 3 - 100, width=140,
                                                  border_width=0, border_color=CINZA)
                    frame_grafico2.pack(side= 'right', padx = (0,50))
                    frame_grafico2.pack_propagate(False)

                                            #___ CONTEUDO GRAFICO 2___
                    ctk.CTkLabel(frame_grafico2, text=f'Previsão Saldo',
                                 height=1, width=1,
                                 fg_color=TERCIARIA, corner_radius=0, text_color=BRANCO,
                                 font=self.fonte_linham).pack(pady=(20,0))

                    ctk.CTkLabel(frame_grafico2, text=f'{calcular_saldo_ate_fim_do_mes(hoje,mes,ano,conta[1])}',
                                 height=1, width=1,
                                 fg_color=TERCIARIA, corner_radius=0, text_color=BRANCO,
                                 font=self.fonte_linhamin).pack()


                                            #___ FRAME BOTOES ___
                    frame_botoes = ctk.CTkFrame(self, fg_color=PRIMARIA)
                    frame_botoes.pack(side= 'top', pady = 0, fill= 'both', expand= True)

                    botao_add_mov = ctk.CTkButton(frame_botoes, text='ADD', width=125, height=50,
                                                  corner_radius=0, fg_color=BRANCO, border_color=CINZA,
                                                  font = self.fonte_titulo, text_color= SECUNDARIA,
                                                  hover_color=TERCIARIA, command= lambda: self.janela_add_mov_corriqueira(conta),
                                                  border_width=0)
                    botao_add_mov.pack(pady=(50,0), padx=(50,0), side= 'left', anchor= 'n')
                    botao_view_mov = ctk.CTkButton(frame_botoes, text='VIEW', width=125, height=50,
                                                   corner_radius=0, fg_color=BRANCO, border_color=CINZA,
                                                   font=self.fonte_titulo, text_color=SECUNDARIA,
                                                   hover_color=TERCIARIA,
                                                   border_width=0, command=lambda: self.view_page(conta))
                    botao_view_mov.pack(pady=(50,0), padx=(0, 50), side='right', anchor= 'n')
                    botao_add_account= ctk.CTkButton(self, text='ACCOUNTS', width=250, height=50,
                                                     corner_radius=0, fg_color=BRANCO, border_color=CINZA,
                                                     font=self.fonte_titulo, text_color=SECUNDARIA,
                                                     hover_color=TERCIARIA, command=  self.janela_add_conta,
                                                     border_width=0)
                    botao_add_account.place(x=(largura-250)/2,y=altura-75)



    #JANELA ADD MOV
        # ABRE UMA JANELA A PARTE PARA ADD PRODUTO
    def janela_add_mov_corriqueira(self, conta):

        verificar_integridade_dados(conta)
        # ATRIBUTOS DA JANELA QUE ABRE

        janela_sobreposta = ctk.CTkToplevel(self,fg_color=PRETO)
        janela_sobreposta.geometry('580x100')
        janela_sobreposta.title('Add Movimentação')
        janela_sobreposta.attributes("-topmost", True)
        janela_sobreposta.grab_set()
        def ao_fechar():
            self.prox_pagina(conta)
            janela_sobreposta.destroy()



        janela_sobreposta.protocol("WM_DELETE_WINDOW", ao_fechar)
        #Frame de labels

        frame_textos = ctk.CTkFrame(janela_sobreposta, fg_color=PRETO,height=50)
        frame_textos.pack(side='top', fill='x')
        ctk.CTkLabel(frame_textos, text=f'DATA', height=30, width=100,
                     fg_color=PRIMARIA, corner_radius=10, text_color=BRANCO2,
                     font=self.fonte_linhaM).pack(pady= 10, padx=(10, 0), side='left')
        ctk.CTkLabel(frame_textos, text=f'NOME', height=30, width=200,
                     fg_color=PRIMARIA, corner_radius=10, text_color=BRANCO2,
                     font=self.fonte_linhaM).pack(pady=10, padx=(10, 0), side='left')
        ctk.CTkLabel(frame_textos, text=f'VAlOR', height=30, width=100,
                     fg_color=PRIMARIA, corner_radius=10, text_color=BRANCO2,
                     font=self.fonte_linhaM).pack(pady=10, padx=(10, 0), side='left')

        barra_selecao_tipo = ctk.CTkOptionMenu(
            master=frame_textos,
            values=["ENTRADA", "SAIDA"], width=125, height=30,
            corner_radius=10, fg_color=AZUL, text_color=BRANCO2,
            button_color=AZUL, font=self.fonte_linhaM)
        barra_selecao_tipo.pack(side='left', padx=(10, 0), pady=10)

        # Frame de Entrys

        frame_entrys = ctk.CTkFrame(janela_sobreposta, fg_color=PRETO,height=50)
        frame_entrys.pack(side='top', fill='x')

        entry_data = ctk.CTkEntry(frame_entrys, placeholder_text='aaaa-mm-dd', width=100, height=20,
                                  corner_radius=0,
                                  font=self.fonte_linham, placeholder_text_color=BRANCO2,
                                  border_width=0, fg_color=SECUNDARIA)
        entry_data.pack(side='left', padx=(10, 0))
        entry_nome = ctk.CTkEntry(frame_entrys, placeholder_text='Fornecedor/Devedor', width=200, height=20,
                                  corner_radius=0,
                                  font=self.fonte_linham, placeholder_text_color=BRANCO2,
                                  border_width=0, fg_color=SECUNDARIA)
        entry_nome.pack(side='left', padx=(10,0))
        entry_valor = ctk.CTkEntry(frame_entrys, placeholder_text='Ex: 2312.75', width=100, height=20,
                                   corner_radius=0,
                                   font=self.fonte_linham, placeholder_text_color=BRANCO2,
                                   border_width=0, fg_color=SECUNDARIA)
        entry_valor.pack(side='left', padx=(10, 0))

        botao_salvar = ctk.CTkButton(frame_entrys, text='SAVE', width=125, height=20,
                                     corner_radius=0, fg_color=VERDE,
                                     font=self.fonte_linham, text_color=BRANCO2,
                                     hover_color=TERCIARIA, command= lambda: salvar_e_atualizar())
        botao_salvar.pack(side='left', padx=(10,0))

        def salvar_e_atualizar():
            resposta_ao_save = salvar_movimentacao_corriqueira(
                data=entry_data.get(),
                nome=entry_nome.get(),
                valor=converter_valor(entry_valor.get()),
                conta=conta[1],
                tipo=barra_selecao_tipo.get())
            if resposta_ao_save == 'salvo':
                self.prox_pagina(conta)




    def janela_add_conta(self, primeira_vez=False):

        # ATRIBUTOS DA JANELA QUE ABRE
        janela_sobreposta = ctk.CTkToplevel(self,fg_color=PRETO)
        janela_sobreposta.geometry('770x125')
        janela_sobreposta.title('Add Conta')
        janela_sobreposta.attributes("-topmost", True)
        janela_sobreposta.grab_set()

        frame_textos = ctk.CTkFrame(janela_sobreposta, fg_color=TRANSPARENTE, height=50)
        frame_textos.pack(side='top', fill='x')
        ctk.CTkLabel(frame_textos, text=f'TITULAR DA CONTA', height=30, width=200,
                     fg_color=PRIMARIA, corner_radius=10, text_color=BRANCO2,
                     font=self.fonte_linhaM).pack(pady=10, padx=(10, 0), side='left')
        ctk.CTkLabel(frame_textos, text=f'NUMERO DA CONTA', height=30, width=100,
                     fg_color=PRIMARIA, corner_radius=10, text_color=BRANCO2,
                     font=self.fonte_linhaM).pack(pady=10, padx=(10, 0), side='left')
        ctk.CTkLabel(frame_textos, text=f'BANCO', height=30, width=150,
                     fg_color=PRIMARIA, corner_radius=10, text_color=BRANCO2,
                     font=self.fonte_linhaM).pack(pady=10, padx=(10, 0), side='left')
        ctk.CTkLabel(frame_textos, text=f'SALDO ATUAL', height=30, width=175,
                     fg_color=PRIMARIA, corner_radius=10, text_color=BRANCO2,
                     font=self.fonte_linhaM).pack(pady=10, padx=(10, 0), side='left')

        frame_entrys = ctk.CTkFrame(janela_sobreposta, fg_color=PRETO, height=50)
        frame_entrys.pack(side='top', fill='x')
        entry_nome = ctk.CTkEntry(frame_entrys, placeholder_text='Ex: Murilo Antega', width=200, height=20,
                                  corner_radius=0,
                                  font=self.fonte_linham, placeholder_text_color=BRANCO2,
                                  border_width=0, fg_color=SECUNDARIA)
        entry_nome.pack(side='left', padx=(10, 0))
        entry_numero = ctk.CTkEntry(frame_entrys, placeholder_text='Ex: 780432', width=185, height=20,
                                    corner_radius=0,
                                    font=self.fonte_linham, placeholder_text_color=BRANCO2,
                                    border_width=0, fg_color=SECUNDARIA)
        entry_numero.pack(side='left', padx=(10, 0))
        entry_banco = ctk.CTkEntry(frame_entrys, placeholder_text='Ex: Santander', width=150, height=20,
                                   corner_radius=0,
                                   font=self.fonte_linham, placeholder_text_color=BRANCO2,
                                   border_width=0, fg_color=SECUNDARIA)
        entry_banco.pack(side='left', padx=(10, 0))
        entry_saldo = ctk.CTkEntry(frame_entrys, placeholder_text='Ex: 1785.75', width=175, height=20,
                                   corner_radius=0,
                                   font=self.fonte_linham, placeholder_text_color=BRANCO2,
                                   border_width=0, fg_color=SECUNDARIA)
        entry_saldo.pack(side='left', padx=(10, 0))

        botao_salvar = ctk.CTkButton(janela_sobreposta, text='SAVE', width=125, height=20,
                                     corner_radius=0, fg_color=VERDE,
                                     font=self.fonte_linham, text_color=BRANCO2,
                                     hover_color=TERCIARIA, command=lambda: ao_clicar_salvar())
        botao_salvar.pack(padx=10, pady= 10)

        def ao_clicar_salvar():
            conta_salva = salvar_conta(
                titular=entry_nome.get(),
                num=entry_numero.get(),
                banco=entry_banco.get(),
                saldo_atual=converter_valor(entry_saldo.get())
            )
            if conta_salva == 'ok':
                if primeira_vez:
                    self.inter_login()
                    self.deiconify()
                janela_sobreposta.destroy()
            else:
                pass
            # ___ PAGINA COM GRAFICOS P/VER RELATORIOS ___
                # ___ A PARTIR DESTA PAGINA PODE GERAR EXCEL E VER TABELA COM TRANSAÇÕES ____

    def view_page(self, conta):
        verificar_integridade_dados(conta)
        self.limpar_janela()
        self.geometry(tam_principal_esticado)
        def ao_fechar_fechar_grafico():
            plt.close('all')
            self.quit()
            self.destroy()

        app.protocol("WM_DELETE_WINDOW", ao_fechar_fechar_grafico)

        botao_editar_mov = ctk.CTkButton(self, text='Editar', width=75, height=20,
                                         corner_radius=0, fg_color=BRANCO,
                                         font=self.fonte_linham, text_color=PRETO,
                                         hover_color=TERCIARIA, command = lambda: self.janela_editar_mov_pegar_id(conta))
        botao_editar_mov.place(x=(largura + 100)-85, y=0)
        frame_scroll_movimentacoes = ctk.CTkScrollableFrame(self, height=(altura // 3)-200, width=largura + 100)



        def att_info_margem_scrollframe(escolha):
            if frame_scroll_movimentacoes.winfo_exists():
                for widget in frame_scroll_movimentacoes.winfo_children():
                    widget.destroy()
            resultado= pegar_todas_as_mov_do_mes_ano(conta[1], mes, ano, escolha)
            if 'None' in resultado:
                ctk.CTkLabel(frame_scroll_movimentacoes, text=f'Banco Vazio', width=157,
                             font=self.fonte_linhaM, text_color=BRANCO).pack(side='top')
            else:

                frame_colunas_data = ctk.CTkFrame(frame_scroll_movimentacoes,width=120, height= altura+1000)
                frame_colunas_data.pack(side='left', fill='y', pady=0, padx =0)
                frame_colunas_nome = ctk.CTkFrame(frame_scroll_movimentacoes, width=157, height=altura + 1000)
                frame_colunas_nome.pack(side='left', fill='y', pady=0, padx=0)
                frame_colunas_valor = ctk.CTkFrame(frame_scroll_movimentacoes, width=122, height=altura + 1000)

                frame_colunas_valor.pack(side='left', fill='y', pady=0, padx=0)
                frame_colunas_id = ctk.CTkFrame(frame_scroll_movimentacoes, width=123, height=altura + 1000)

                frame_colunas_id.pack(side='left', fill='y', pady=0, padx=0)

                                # ___ FRAME PARA A PALAVRA 'DATA' NA TABELA ___
                frame_indice_data = ctk.CTkFrame(frame_colunas_data,width=120, height=30)
                frame_indice_data.pack(side='top', fill='x', pady=0, padx=0)
                ctk.CTkLabel(frame_indice_data, text=f'data', width=120,
                             font=self.fonte_linhamin, text_color=BRANCO, fg_color=AZUL).pack(side='top')

                                # ___ FRAME PARA A PALAVRA 'NOME' NA TABELA ___
                frame_indice_nome = ctk.CTkFrame(frame_colunas_nome, width=157, height=30)
                frame_indice_nome.pack(side='top', fill='x', pady=0, padx=0)
                ctk.CTkLabel(frame_indice_nome, text=f'Fornecedor', width=157,
                             font=self.fonte_linhamin, text_color=BRANCO, fg_color=PRIMARIA).pack(side='top')

                frame_indice_valor = ctk.CTkFrame(frame_colunas_valor, width=122, height=30)
                frame_indice_valor.pack(side='top', fill='x', pady=0, padx=0)
                ctk.CTkLabel(frame_indice_valor, text=f'valor', width=122,
                             font=self.fonte_linhamin, text_color=BRANCO, fg_color=AZUL).pack(side='top')

                frame_indice_id = ctk.CTkFrame(frame_colunas_id, width=123, height=30)
                frame_indice_id.pack(side='top', fill='x', pady=0, padx=0)
                ctk.CTkLabel(frame_indice_id, text=f'id', width=123,
                             font=self.fonte_linhamin, text_color=BRANCO, fg_color=PRIMARIA).pack(side='top')
                if resultado != 0:
                    for resposta in resultado:
                        ctk.CTkLabel(frame_colunas_data, text=f'{resposta[0]}',
                                     font=self.fonte_linham, text_color=BRANCO).pack(side='top', padx= 0)
                        ctk.CTkLabel(frame_colunas_nome, text=f'{resposta[1]}',
                                     font=self.fonte_linham, text_color=BRANCO).pack(side='top', padx=0)
                        ctk.CTkLabel(frame_colunas_valor, text=f'{resposta[2]}',
                                     font=self.fonte_linham, text_color=BRANCO).pack(side='top', padx=0)
                        ctk.CTkLabel(frame_colunas_id, text=f'{resposta[3]}',
                                     font=self.fonte_linham, text_color=BRANCO).pack(side='top', padx=0)




        barra_selecao_tipo_scroll = ctk.CTkOptionMenu(
            master=self,
            values=['Mes', 'Mes - passado', 'Ano'], width=75, height=20,
            corner_radius=0, fg_color=BRANCO, text_color=PRETO,
            button_color=BRANCO, font=self.fonte_linhamin, command=att_info_margem_scrollframe, dropdown_fg_color=PRIMARIA)
        barra_selecao_tipo_scroll.place(x=10,y=0)


        ctk.CTkLabel(self, text=f'{conta[0]} - {conta[3]} - R${conta[2]:.2f}',
                     font=self.fonte_linhaM, text_color=BRANCO2).pack(side='top')

        frame_scroll_movimentacoes.pack(side='top')
        frame_saldo_previsto = ctk.CTkFrame(self, height=200, width=largura + 100, fg_color=AMARELO)
        frame_saldo_previsto.pack(side='top')
        ctk.CTkLabel(frame_saldo_previsto,
                     text=f'Saldo Previso para fim do mes\n{calcular_saldo_ate_fim_do_mes(hoje, mes, ano, conta[1], True)}',
                     width=largura + 100,
                     font=self.fonte_linhamin, text_color=PRETO, fg_color=AMARELO).pack(side='bottom')

        frame_grafico = ctk.CTkFrame(self, width=largura+100, height=270, fg_color=CINZA)
        frame_grafico.pack(side='top', fill='x', pady=0, padx=0)
        frame_grafico.pack_propagate(False)

        def att_info_margem_grafico(_=None):
            if frame_grafico.winfo_exists():
                for widget in frame_grafico.winfo_children():
                    widget.destroy()
                escolha_tempo = barra_selecao_data_grafico.get()
                tipo = barra_selecao_tipo_grafico.get()
                datas, vendas_por_datas, nomes = pegar_movimentacao_data_para_graficos(conta[1], mes, escolha_tempo, tipo)
                if datas == ['Banco Vazio'] or datas == ['None']:
                    frame_grafico.configure(fg_color=PRIMARIA)
                    ctk.CTkLabel(frame_grafico, text=f'{datas}',
                                 font=self.fonte_titulo, text_color=BRANCO, fg_color=PRIMARIA).pack(expand= True, fill = 'both')
                else:
                    cores= ['green' if v > 0 else 'red' for v in vendas_por_datas]
                    fig, ax = plt.subplots(nrows=1, ncols=1)
                    ax.set_title('Movimentações')
                    for label in ax.get_xticklabels():
                        label.set_horizontalalignment('right')
                    fig.tight_layout()
                    barras = ax.bar(datas, vendas_por_datas, color=cores, edgecolor=PRIMARIA)
                    ax.bar_label(barras, labels = [f'{nome}' for nome in nomes], label_type='center', color=BRANCO)
                    ax.autoscale(enable=True, axis='x', tight=False)

                    fig.tight_layout()

                    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
                    canvas.draw()
                    canvas.get_tk_widget().pack(fill="both", expand=True)
            else:
                return

        frame_botoes = ctk.CTkFrame(self, fg_color=PRIMARIA,
                                    height=(altura + 100) // 3, width=largura + 100)
        frame_botoes.pack(side='top')

        barra_selecao_data_grafico = ctk.CTkOptionMenu(
            master=frame_botoes,
            values=['Mes', 'Mes - passado', 'Ano'], width=75, height=20,
            corner_radius=0, fg_color=SECUNDARIA, text_color=BRANCO,
            button_color=SECUNDARIA, font=self.fonte_linhamin, command=att_info_margem_grafico,
            dropdown_fg_color=PRIMARIA)
        barra_selecao_data_grafico.place(x=10,y=0)

        barra_selecao_tipo_grafico = ctk.CTkOptionMenu(
            master=frame_botoes,
            values=['Total', 'Entradas', 'Saidas'], width=75, height=20,
            corner_radius=0, fg_color=SECUNDARIA, text_color=BRANCO,
            button_color=SECUNDARIA, font=self.fonte_linhamin, command=att_info_margem_grafico,
            dropdown_fg_color=PRIMARIA)
        barra_selecao_tipo_grafico.place(x=(largura+100)-85, y=0)

        botao_calcular_saldo_ate = ctk.CTkButton(frame_botoes, text='Calcular saldo até', width=100,
                                     height=20,
                                     corner_radius=0, fg_color=AMARELO,
                                     font=self.fonte_linhamin, text_color=PRETO,
                                     hover_color=TERCIARIA, command=lambda:self.janela_calcular_saldo_ate(conta))
        botao_calcular_saldo_ate.place(x=((largura + 100)/2)-55, y=0)
        botao_voltar = ctk.CTkButton(frame_botoes, text='Voltar', width=100,
                                                 height=40,
                                                 corner_radius=0, fg_color=VERMELHO,
                                                 font=self.fonte_linhamin, text_color=BRANCO,
                                                 hover_color=TERCIARIA, command= lambda: self.prox_pagina(conta))
        botao_voltar.place(x=((largura + 100)/2)-200, y=60)
        botao_to_xls = ctk.CTkButton(frame_botoes, text='To excel', width=100,
                                                 height=40,
                                                 corner_radius=0, fg_color=VERDE,
                                                 font=self.fonte_linhamin, text_color=BRANCO,
                                                 hover_color=TERCIARIA, command=sql_to_excel(conta[1]))
        botao_to_xls.place(x=((largura + 100)/2)+100, y=60)
        att_info_margem_grafico(barra_selecao_data_grafico.get())
        att_info_margem_scrollframe(barra_selecao_tipo_scroll.get())


    def janela_editar_mov_pegar_id(self, conta):

        # ATRIBUTOS DA JANELA QUE ABRE
        janela_sobreposta = ctk.CTkToplevel(self, fg_color=PRETO)
        janela_sobreposta.geometry('570x175')
        janela_sobreposta.title('Editar mov')
        janela_sobreposta.attributes("-topmost", True)
        janela_sobreposta.configure(fg_color=PRIMARIA)
        janela_sobreposta.grab_set()
        def ao_fechar():
            janela_sobreposta.destroy()
            self.view_page(conta)
        janela_sobreposta.protocol("WM_DELETE_WINDOW", ao_fechar)
        frame_textos = ctk.CTkFrame(janela_sobreposta, width=270, height=175//2, fg_color= PRIMARIA)
        frame_textos.pack(side='top')
        frame_entrys = ctk.CTkFrame(janela_sobreposta, width=270, height=175//2, fg_color= PRIMARIA)
        frame_entrys.pack(side='top')

        ctk.CTkLabel(frame_textos,
                     text=f'Selecione o id da movimentação',
                     width=170,
                     font=self.fonte_linhaM, text_color=BRANCO).pack(side='top', pady=(30,10))

        barra_selecao_id = ctk.CTkOptionMenu(
            master=frame_entrys,
            values=pegar_id_todas_movimentos(conta[1]), width=100, height=30,
            corner_radius=0, fg_color=BRANCO, text_color=PRETO,
            button_color=SECUNDARIA, font=self.fonte_linhamin,
            dropdown_fg_color=PRIMARIA)
        barra_selecao_id.pack(side='top', pady=(0,10))
        botao_avancar = ctk.CTkButton(frame_entrys, text='Avançar', width=80,
                                     height=40,
                                     corner_radius=0, fg_color=VERDE,
                                     font=self.fonte_linhamin, text_color=BRANCO,
                                     hover_color=TERCIARIA, command = lambda: (janela_sobreposta.destroy(),self.janela_editar_mov_pegar_coluna(conta,barra_selecao_id.get())))
        botao_avancar.pack(side='top', pady=(0,30))



    def janela_editar_mov_pegar_coluna(self,conta, ident):


        # ATRIBUTOS DA JANELA QUE ABRE
        janela_sobreposta = ctk.CTkToplevel(self, fg_color=PRETO)
        janela_sobreposta.geometry('570x175')
        janela_sobreposta.title('Editar mov')
        janela_sobreposta.attributes("-topmost", True)
        janela_sobreposta.configure(fg_color=PRIMARIA)
        janela_sobreposta.grab_set()

        def ao_fechar():
            janela_sobreposta.destroy()
            self.view_page(conta)


        janela_sobreposta.protocol("WM_DELETE_WINDOW", ao_fechar)
        frame_textos = ctk.CTkFrame(janela_sobreposta, width=270, height=175 // 2, fg_color=PRIMARIA)
        frame_textos.pack(side='top')
        frame_entrys = ctk.CTkFrame(janela_sobreposta, width=270, height=175 // 2, fg_color=PRIMARIA)
        frame_entrys.pack(side='top')

        ctk.CTkLabel(frame_textos,
                     text=f'O que você quer alterar?',
                     width=170,
                     font=self.fonte_linhaM, text_color=BRANCO).pack(side='top', pady=(30, 10))

        barra_selecao_coluna = ctk.CTkOptionMenu(
            master=frame_entrys,
            values=['data','nome','valor','conta'], width=100, height=30,
            corner_radius=0, fg_color=BRANCO, text_color=PRETO,
            button_color=SECUNDARIA, font=self.fonte_linhamin,
            dropdown_fg_color=PRIMARIA)
        barra_selecao_coluna.pack(side='top', pady=(0, 10))
        botao_avancar = ctk.CTkButton(frame_entrys, text='Avançar', width=80,
                                     height=40,
                                     corner_radius=0, fg_color=VERDE,
                                     font=self.fonte_linhamin, text_color=BRANCO,
                                     hover_color=TERCIARIA, command= lambda: (janela_sobreposta.destroy(),self.janela_editar_mov_preencher_valor(conta, ident, barra_selecao_coluna.get())))
        botao_avancar.pack(side='top', pady=(0, 30))


    def janela_editar_mov_preencher_valor(self,conta, ident, coluna):


        # ATRIBUTOS DA JANELA QUE ABRE
        janela_sobreposta = ctk.CTkToplevel(self, fg_color=PRETO)
        janela_sobreposta.geometry('570x175')
        janela_sobreposta.title('Editar mov')
        janela_sobreposta.attributes("-topmost", True)
        janela_sobreposta.configure(fg_color=PRIMARIA)
        janela_sobreposta.grab_set()

        def ao_fechar():
            janela_sobreposta.destroy()
            self.view_page(conta)

        janela_sobreposta.protocol("WM_DELETE_WINDOW", ao_fechar)
        frame_textos = ctk.CTkFrame(janela_sobreposta, width=270, height=175 // 2, fg_color=PRIMARIA)
        frame_textos.pack(side='top')
        frame_entrys = ctk.CTkFrame(janela_sobreposta, width=270, height=175 // 2, fg_color=PRIMARIA)
        frame_entrys.pack(side='top')
        if coluna == 'nome':

            ctk.CTkLabel(frame_textos,
                         text=f'Digite o nome correto',
                         width=170,
                         font=self.fonte_linhaM, text_color=BRANCO).pack(side='top', pady=(30, 10))
            entry = ctk.CTkEntry(frame_entrys, placeholder_text='Ex: Murilo Antega', width=200, height=20,
                                      corner_radius=0,
                                      font=self.fonte_linham, placeholder_text_color=BRANCO2,
                                      border_width=0, fg_color=SECUNDARIA)
            entry.pack(side='top', pady=(0,30))
        elif coluna == 'data':
            ctk.CTkLabel(frame_textos,
                         text=f'Digite a data correta',
                         width=170,
                         font=self.fonte_linhaM, text_color=BRANCO).pack(side='top', pady=(30, 10))
            entry = ctk.CTkEntry(frame_entrys, placeholder_text='2026-09-22', width=200, height=20,
                                 corner_radius=0,
                                 font=self.fonte_linham, placeholder_text_color=BRANCO2,
                                 border_width=0, fg_color=SECUNDARIA)
            entry.pack(side='top', pady=(0, 30))
        elif coluna == 'valor':
            ctk.CTkLabel(frame_textos,
                         text=f'Digite o valor correto',
                         width=170,
                         font=self.fonte_linhaM, text_color=BRANCO).pack(side='top', pady=(30, 10))
            entry = ctk.CTkEntry(frame_entrys, placeholder_text='Ex: 2095.50', width=200, height=20,
                                 corner_radius=0,
                                 font=self.fonte_linham, placeholder_text_color=BRANCO2,
                                 border_width=0, fg_color=SECUNDARIA)
            entry.pack(side='top', pady=(0, 30))
        else:
            ctk.CTkLabel(frame_textos,
                         text=f'Digite a conta correta',
                         width=170,
                         font=self.fonte_linhaM, text_color=BRANCO).pack(side='top', pady=(30, 10))
            entry = ctk.CTkEntry(frame_entrys, placeholder_text='Ex: 123456', width=200, height=20,
                                 corner_radius=0,
                                 font=self.fonte_linham, placeholder_text_color=BRANCO2,
                                 border_width=0, fg_color=SECUNDARIA)
            entry.pack(side='top', pady=(0, 30))

        botao_salvar = ctk.CTkButton(frame_entrys, text='Salvar', width=80,
                                     height=40,
                                     corner_radius=0, fg_color=VERDE,
                                     font=self.fonte_linhamin, text_color=BRANCO,
                                     hover_color=TERCIARIA, command= lambda: update_movimentos(ident, coluna, entry.get()))
        botao_salvar.pack(side='top', pady=(0, 30))

    def janela_calcular_saldo_ate(self, conta):
        self.limpar_janela()
        self.geometry('570x245')

        def ao_fechar():
            self.view_page(conta)
        self.protocol('WM_DELETE_WINDOW', ao_fechar)

        ctk.CTkLabel(self,
                     text=f'Digite a data que quer saber o saldo',
                     width=170,
                     font=self.fonte_linhaM, text_color=BRANCO).pack(side='top', pady=(30, 10))
        entry = ctk.CTkEntry(self, placeholder_text='2026-09-22', width=200, height=20,
                             corner_radius=0,
                             font=self.fonte_linham, placeholder_text_color=BRANCO2,
                             border_width=0, fg_color=SECUNDARIA)
        entry.pack(side='top', pady=(0, 10))
        def mostrar_resposta(data, conta):
            resposta_req_func = calcular_saldo_ate(data, conta)
            ctk.CTkLabel(self,
                         text=f'Saldo até {data}:\nR${resposta_req_func}',
                         width=170,
                         font=self.fonte_linhaM, text_color=BRANCO).pack(side='top', pady=(0, 30))

        botao_salvar = ctk.CTkButton(self, text='Salvar', width=80,
                                     height=40,
                                     corner_radius=0, fg_color=VERDE,
                                     font=self.fonte_linhamin, text_color=BRANCO,
                                     hover_color=TERCIARIA, command=lambda: mostrar_resposta(entry.get(), conta[1]))
        botao_salvar.pack(side='top', pady=(0, 30))







# SEGURANÇA
def verificar_integridade_dados(conta):
    if conta:
        pass
    else:
        messagebox.showerror('Erro', 'Erro ao passar dados para paginas')
        app.quit()
        app.destroy()


























app = App()
app.mainloop()