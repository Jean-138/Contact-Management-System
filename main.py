
import json

# tipos de contato que o sistema aceita, por enquanto só esses três
contatos_suportados = ("Telefone", "E-mail", "Endereco")

# agenda de exemplo que já vem preenchida pra teste
# (mas no final das contas o programa começa com uma vazia, então isso aqui fica meio inútil)
agenda = {
    "pessoa 1": {
        "Telefone": ["11 1234-5678"],
        "E-mail": ["pessoa@email.com", "email@profissional.com"],
        "Endereco": ["rua 123"]
    },
    "pessoa 2": {
        "Telefone": ["11 321-3433"],
        "E-mail": ["pessoa2@email.com", "profissionalpessoa2@email.com"],
        "Endereco": ["rua 444"]
    }
}


# pega um contato e transforma em texto bonitinho pra exibir na tela
def contato_para_texto(nome_contato: str, **formas_contato):
    formato_texto = f"{nome_contato}"
    for meio_contato, contato in formas_contato.items():
        formato_texto = f"{formato_texto}\n{meio_contato.upper()}"
        contador_formas = 1
        # lista cada valor daquela forma de contato (ex: pode ter mais de um email)
        for valor in contato:
            formato_texto = f"{formato_texto}\n\t{contador_formas} - {valor.upper()}"
            contador_formas = contador_formas + 1
    return formato_texto


# mesma ideia da de cima, mas pra agenda inteira
def agenda_para_texto(**agenda_completa):
    formato_texto = ""
    for nome_contato, formas_contato in agenda_completa.items():
        formato_texto = f"{formato_texto}{contato_para_texto(nome_contato, **formas_contato)}\n"
    return formato_texto


# salva a agenda num arquivo .txt normal
def agenda_para_txt(nome_arquivo: str, agenda_dict: dict):
    # se o cara esqueceu de colocar .txt no nome, a gente coloca
    if "txt" not in nome_arquivo:
        nome_arquivo = f"{nome_arquivo}.txt"
    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(agenda_para_texto(**agenda_dict))
    print("Agenda exportada com sucesso!")


# carrega uma agenda a partir de um arquivo JSON que já existe
def json_para_agenda(nome_arquivo: str) -> dict:
    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        conteudo = arquivo.read()
    print("Agenda carregada com sucesso!")
    return json.loads(conteudo)


# salva a agenda num arquivo JSON (útil pra carregar depois)
def agenda_para_json(nome_arquivo: str, agenda_dict: dict):
    if ".json" not in nome_arquivo:
        nome_arquivo = f"{nome_arquivo}.json"
    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        # ensure_ascii=False pra não zoar os acentos
        arquivo.write(json.dumps(agenda_dict, indent=4, ensure_ascii=False))
    print("Agenda exportada com sucesso!")


# troca o nome de um contato mantendo todas as infos dele
def altera_nome_contato(agenda_original: dict, nome_original: str, nome_atualizado: str):
    if nome_original in agenda_original.keys():
        # basicamente copia tudo, apaga o antigo e cria um novo com o nome certo
        copia_contatos = agenda_original[nome_original].copy()
        agenda_original.pop(nome_original)
        agenda_original[nome_atualizado] = copia_contatos
        return True
    return False


# altera um valor específico dentro de uma lista de contatos
# tipo trocar um email antigo por um novo
def altera_forma_contato(lista_contatos: list, valor_antigo: str, novo_valor: str):
    if valor_antigo in lista_contatos:
        posicao_valor_antigo = lista_contatos.index(valor_antigo)
        # tira o antigo e coloca o novo no mesmo lugar
        lista_contatos.pop(posicao_valor_antigo)
        lista_contatos.insert(posicao_valor_antigo, novo_valor)
        return True
    return False


# remove um contato inteiro da agenda
def excluir_contato(agenda_dict: dict, nome_contato: str):
    if nome_contato in agenda_dict.keys():
        agenda_dict.pop(nome_contato)
        return True
    return False


# adiciona um contato novo na agenda com as formas de contato que vierem
def incluir_contato(agenda_dict: dict, nome_contato: str, **formas_contato):
    agenda_dict[nome_contato] = formas_contato


# adiciona uma forma de contato a alguém que já tá na agenda
# se já tem email e quer botar outro, ele só adiciona na lista
# se não tem telefone ainda, ele cria a lista do zero
def inclui_forma_de_contato(formas_contato: dict, forma_incluida: str, valor_incluido: str):
    if forma_incluida in formas_contato.keys():
        formas_contato[forma_incluida].append(valor_incluido)
        return True
    elif forma_incluida in contatos_suportados:
        formas_contato[forma_incluida] = [valor_incluido]
        return True
    return False


# aqui começa a parte interativa - o usuário vai incluindo contato pelo terminal
def usuario_inclui_contato(agenda_dict: dict):
    nome = input("Informe o nome do novo contato que sera inserido na agenda: ")
    dicionario_formas = {}

    # passa por cada tipo de contato perguntando se quer adicionar
    for forma in contatos_suportados:
        resposta = input(f"Deseja inserir um {forma} para {nome.upper()}? SIM ou NAO -> ")
        lista_contatos = []

        # enquanto o cara quiser ficar adicionando, vai perguntando
        while resposta.upper() == "SIM":
            lista_contatos.append(input(f"Informe um {forma}: "))
            resposta = input(f"Deseja inserir outro {forma}? SIM ou NAO -> ")

        if len(lista_contatos) > 0:
            dicionario_formas[forma] = lista_contatos.copy()

    # só salva se colocou pelo menos alguma coisa, senão não faz sentido
    if len(dicionario_formas.keys()) > 0:
        incluir_contato(agenda_dict, nome, **dicionario_formas)
        print("Inclusao bem sucedida!")
    else:
        print("Inclua pelo menos uma forma de contato! A agenda nao foi alterada.")


# parecido com o de cima, mas pra adicionar uma forma de contato a alguém que já existe
def usuario_inclui_forma_de_contato(agenda_dict: dict):
    nome = input("Informe o nome do contato para qual deseja incluir formas de contato: ")

    if nome in agenda_dict.keys():
        print(f"As formas de contato suportadas pelo sistema sao {contatos_suportados}")
        forma_incluida = input("Qual forma de contato deseja incluir? ")

        if forma_incluida in contatos_suportados:
            valor_incluido = input(f"Informe o {forma_incluida} que deseja incluir: ")

            if inclui_forma_de_contato(agenda_dict[nome], forma_incluida, valor_incluido):
                print("Operacao bem sucedida, a nova forma de contato foi incluida.")
            else:
                print("Ocorreu um erro durante a insercao. A agenda nao foi alterada.")
        else:
            print("A forma de contato indicada nao e suportada pelo sistema. A agenda nao foi alterada.")
    else:
        print("O contato informado nao existe na agenda. Nao foram feitas alteracoes.")


# exclui contato pela interação com o usuário
def usuario_exclui_contato(agenda_dict: dict):
    nome = input("Informe o nome do contato que deseja excluir: ")

    if excluir_contato(agenda_dict, nome):
        print("Usuario excluido com sucesso!")
    else:
        print("Nome do usuario nao foi localizado na agenda. Nao foram feitas alteracoes.")


# deixa o usuário trocar o nome de alguém na agenda
def usuario_alterar_nome_contato(agenda_dict: dict):
    nome_original = input("Informe o nome do contato que deseja alterar: ")
    nome_atualizado = input("Informe o nome do novo contato: ")

    if altera_nome_contato(agenda_dict, nome_original, nome_atualizado):
        print(f"O contato foi atualizado e agora se chama {nome_atualizado}")
    else:
        print("O contato original nao foi localizado. A agenda nao foi alterada.")


# pra quando o cara quer trocar um telefone ou email específico
def usuario_altera_forma_contato(agenda_dict: dict):
    nome = input("Informe o nome do contato que deseja alterar: ")

    if nome in agenda_dict.keys():
        print(f"As formas de contato suportadas pelo sistema sao: {contatos_suportados}")
        forma_incluida = input("Qual forma de contato deseja alterar? ")

        if forma_incluida in contatos_suportados and forma_incluida in agenda_dict[nome]:
            # mostra os dados atuais pra pessoa saber o que quer mudar
            print(contato_para_texto(nome, **agenda_dict[nome]))
            valor_antigo = input(f"Informe o {forma_incluida} que deseja alterar: ")
            novo_valor = input(f"Informe o novo {forma_incluida}: ")

            if altera_forma_contato(agenda_dict[nome][forma_incluida], valor_antigo, novo_valor):
                print("Contato alterado com sucesso!")
            else:
                print("Ocorreu um erro durante a alteracao do contato. A agenda nao foi alterada.")
        else:
            print("Forma de contato invalida. A agenda nao foi alterada.")
    else:
        print("O contato nao esta na agenda. A agenda nao foi alterada.")


# só mostra um contato específico na tela
def usuario_contato_para_texto(agenda_dict: dict):
    nome = input("Informe o nome do contato que deseja exibir: ")

    if nome in agenda_dict.keys():
        print(contato_para_texto(nome, **agenda_dict[nome]))
    else:
        print("O contato informado nao esta na agenda.")


# menu principal, nada demais
def exibe_menu():
    print("\n")
    print("1 - Incluir contato na agenda")
    print("2 - Incluir uma forma de contato")
    print("3 - Alterar o nome de um contato")
    print("4 - Alterar uma forma de contato")
    print("5 - Exibir um contato")
    print("6 - Exibir toda a agenda")
    print("7 - Excluir um contato")
    print("8 - Exportar agenda para txt")
    print("9 - Exportar agenda para JSON")
    print("10 - Importar agenda de JSON")
    print("11 - Sair")
    print("\n")


# coração do programa - fica rodando em loop até o usuário escolher sair
def manipulador_agenda():
    agenda_local = {}  # começa do zero (a agenda lá de cima não é usada aqui)
    op = 1

    while op != 11:
        exibe_menu()
        op = int(input("Informe a opcao desejada: "))

        if op == 1:
            usuario_inclui_contato(agenda_local)

        elif op == 2:
            usuario_inclui_forma_de_contato(agenda_local)

        elif op == 3:
            usuario_alterar_nome_contato(agenda_local)

        elif op == 4:
            usuario_altera_forma_contato(agenda_local)

        elif op == 5:
            usuario_contato_para_texto(agenda_local)

        elif op == 6:
            print(agenda_para_texto(**agenda_local))

        elif op == 7:
            usuario_exclui_contato(agenda_local)

        elif op == 8:
            nome_arquivo = input("Informe o nome ou caminho do arquivo: ")
            agenda_para_txt(nome_arquivo, agenda_local)

        elif op == 9:
            nome_arquivo = input("Informe o nome ou caminho do arquivo: ")
            agenda_para_json(nome_arquivo, agenda_local)

        elif op == 10:
            nome_arquivo = input("Informe o nome ou caminho do arquivo JSON: ")
            agenda_carregada = json_para_agenda(nome_arquivo)
            # limpa tudo e substitui pela agenda que veio do arquivo
            agenda_local.clear()
            agenda_local.update(agenda_carregada)

        elif op == 11:
            print("Saindo do programa...")


# roda o programa
manipulador_agenda()