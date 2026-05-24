# Avaliação Continuada 3 - 1 ponto
# PROJETO DE VENDAS - parte 1
# Exercicios de estatisticas de vendas.
# Entrega - dia 17/05/2026

from banco_de_dados.conexao import conectar, fechar_conexao
from datetime import datetime


def total_vendas_periodo():
    # Exercicio 1: calcular o valor total vendido em um periodo usando vendas.valor_final.
    conexao = conectar()

    # Validação da Data Inicial
    while True:
        data_inicial = input("Data inicial (YYYY-mm-dd): ")
        try:
            datetime.strptime(data_inicial, "%Y-%m-%d")
            break
        except:
            print("Data inválida, digite no formato (YYYY-mm-dd)")

    # Validação da Data Final
    while True:
        data_final = input("Data final (YYYY-mm-dd): ")
        try:
            datetime.strptime(data_final, "%Y-%m-%d")
            break
        except:
            print("Data inválida, digite no formato (YYYY-mm-dd)")

    if conexao:
        cursor = conexao.cursor()
        sql = """
            SELECT SUM(valor_final) as total_vendas
            FROM vendas
            WHERE data_e_hora BETWEEN %s AND %s
        """

        cursor.execute(sql, (data_inicial, data_final))

        venda = cursor.fetchone()

        cursor.close()
        fechar_conexao(conexao)

        # Formatando oq vai aparecer no menu
        total = venda[0] if venda[0] else 0
        return f"\n=== TOTAL DE VENDAS NO PERÍODO ===\nTotal: R$ {total:.2f}"

    return "Erro de conexão."

    #FIZEMOS ESSE PRIMEIRO DEF JUNTOS NA SALA PROFESSOR, USEI DE EXEMPLO PARA FAZER OS OUTROS😊


def qtd_vendas_por_vendedor():
    # Exercicio 2: contar quantas vendas cada vendedor realizou usando vendas.id_vendedor.
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        sql = """
            SELECT vendedores.nome, COUNT(vendas.id) 
            FROM vendas 
            INNER JOIN vendedores ON vendas.id_vendedor = vendedores.id 
            GROUP BY vendedores.nome
        """
        cursor.execute(sql)
        resultados = cursor.fetchall()  # Traz todos os vendedores
        cursor.close()
        fechar_conexao(conexao)

        texto_final = "Quantidade de vendas por vendedor:\n"
        for nome, qtd in resultados:
            texto_final += f"- {nome}: {qtd} vendas\n"
        return texto_final.strip()
    return "Erro de conexão."


def ticket_medio_geral():
    # Exercicio 3: calcular o ticket medio geral a partir de vendas.valor_final.
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT AVG(valor_final) FROM vendas")
        resultado = cursor.fetchone()
        cursor.close()
        fechar_conexao(conexao)

        media = resultado[0] if resultado[0] else 0
        return f"Ticket médio geral: R$ {media:.2f}"
    return "Erro de conexão."


def ticket_medio_por_vendedor():
    # Exercicio 4: calcular o ticket medio de cada vendedor cruzando vendas e vendedores.
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        sql = """
            SELECT vendedores.nome, AVG(vendas.valor_final) 
            FROM vendas 
            INNER JOIN vendedores ON vendas.id_vendedor = vendedores.id 
            GROUP BY vendedores.nome
        """
        cursor.execute(sql)
        resultados = cursor.fetchall()
        cursor.close()
        fechar_conexao(conexao)

        texto_final = "Ticket médio por vendedor:\n"
        for nome, media in resultados:
            texto_final += f"- {nome}: R$ {media:.2f}\n"
        return texto_final.strip()
    return "Erro de conexão."


def produto_mais_vendido_qtd():
    # Exercicio 5: identificar o produto mais vendido por quantidade em vendas_produtos.
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        sql = """
            SELECT produtos.descricao, SUM(vendas_produtos.quantidade) as total_qtd
            FROM vendas_produtos
            INNER JOIN produtos ON vendas_produtos.id_produto = produtos.id
            GROUP BY produtos.descricao
            ORDER BY total_qtd DESC
            LIMIT 1
        """
        cursor.execute(sql)
        resultado = cursor.fetchone()
        cursor.close()
        fechar_conexao(conexao)

        if resultado:
            return f"Produto mais vendido: {resultado[0]} (Quantidade: {resultado[1]})"
        return "Nenhum produto encontrado."
    return "Erro de conexão."


def produto_mais_rentavel_valor():
    # Exercicio 6: identificar o produto que gerou maior faturamento somando vendas_produtos.valor_total.
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        sql = """
            SELECT produtos.descricao, SUM(vendas_produtos.valor_total) as total_fat
            FROM vendas_produtos
            INNER JOIN produtos ON vendas_produtos.id_produto = produtos.id
            GROUP BY produtos.descricao
            ORDER BY total_fat DESC
            LIMIT 1
        """
        cursor.execute(sql)
        resultado = cursor.fetchone()
        cursor.close()
        fechar_conexao(conexao)

        if resultado:
            return f"Produto mais rentável: {resultado[0]} (Faturamento: R$ {resultado[1]:.2f})"
        return "Nenhum produto encontrado."
    return "Erro de conexão."


def total_descontos_aplicados():
    # Exercicio 7: somar todos os descontos concedidos usando vendas.desconto.
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT SUM(desconto) FROM vendas")
        resultado = cursor.fetchone()
        cursor.close()
        fechar_conexao(conexao)

        total = resultado[0] if resultado[0] else 0
        return f"Total de descontos aplicados: R$ {total:.2f}"
    return "Erro de conexão."


def percentual_desconto_medio():
    # Exercicio 8: calcular o percentual medio de desconto comparando desconto e valor_final das vendas.
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT SUM(desconto), SUM(valor_final) FROM vendas")
        resultado = cursor.fetchone()
        cursor.close()
        fechar_conexao(conexao)

        soma_desconto = resultado[0] if resultado[0] else 0
        soma_final = resultado[1] if resultado[1] else 0

        valor_bruto = soma_final + soma_desconto
        if valor_bruto > 0:
            percentual = (soma_desconto / valor_bruto) * 100
            return f"Percentual médio de desconto: {percentual:.2f}%"
        return "Não há vendas para calcular percentual."
    return "Erro de conexão."


def faturamento_por_dia():
    # Exercicio 9: agrupar o faturamento por dia com base em vendas.data_e_hora e vendas.valor_final.
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        sql = """
            SELECT DATE(data_e_hora), SUM(valor_final) 
            FROM vendas 
            GROUP BY DATE(data_e_hora)
            ORDER BY DATE(data_e_hora)
        """
        cursor.execute(sql)
        resultados = cursor.fetchall()
        cursor.close()
        fechar_conexao(conexao)

        texto_final = "Faturamento por dia:\n"
        for data, faturamento in resultados:
            texto_final += f"- {data.strftime('%d/%m/%Y')}: R$ {faturamento:.2f}\n"
        return texto_final.strip()
    return "Erro de conexão."


def top_3_vendedores_faturamento():
    # Exercicio 10: listar os 3 vendedores com maior faturamento total no periodo.
    conexao = conectar()

    while True:
        data_inicial = input("Data inicial (YYYY-mm-dd): ")
        try:
            datetime.strptime(data_inicial, "%Y-%m-%d")
            break
        except:
            print("Data inválida, digite no formato (YYYY-mm-dd)")

    while True:
        data_final = input("Data final (YYYY-mm-dd): ")
        try:
            datetime.strptime(data_final, "%Y-%m-%d")
            break
        except:
            print("Data inválida, digite no formato (YYYY-mm-dd)")

    if conexao:
        cursor = conexao.cursor()
        sql = """
            SELECT vendedores.nome, SUM(vendas.valor_final) as total
            FROM vendas
            INNER JOIN vendedores ON vendas.id_vendedor = vendedores.id
            WHERE vendas.data_e_hora BETWEEN %s AND %s
            GROUP BY vendedores.nome
            ORDER BY total DESC
            LIMIT 3
        """
        cursor.execute(sql, (data_inicial, data_final))
        resultados = cursor.fetchall()
        cursor.close()
        fechar_conexao(conexao)

        texto_final = "\n=== TOP 3 VENDEDORES NO PERÍODO ===\n"
        posicao = 1
        for nome, total in resultados:
            texto_final += f"{posicao}º lugar - {nome}: R$ {total:.2f}\n"
            posicao += 1
        return texto_final.strip()
    return "Erro de conexão."


def menu_relatorios():
    opcoes = {
        "1": ("Total de vendas por periodo", total_vendas_periodo),
        "2": ("Quantidade de vendas por vendedor", qtd_vendas_por_vendedor),
        "3": ("Ticket medio geral", ticket_medio_geral),
        "4": ("Ticket medio por vendedor", ticket_medio_por_vendedor),
        "5": ("Produto mais vendido por quantidade", produto_mais_vendido_qtd),
        "6": ("Produto mais rentavel por faturamento", produto_mais_rentavel_valor),
        "7": ("Total de descontos aplicados", total_descontos_aplicados),
        "8": ("Percentual medio de desconto", percentual_desconto_medio),
        "9": ("Faturamento por dia", faturamento_por_dia),
        "10": ("Top 3 vendedores por faturamento", top_3_vendedores_faturamento),
    }

    while True:
        print("\n=== MENU AC3 - RELATORIOS ===")
        for codigo, (descricao, _) in opcoes.items():
            print(f"{codigo} - {descricao}")
        print("0 - Voltar")

        escolha = input("Escolha uma opcao: ").strip()

        if escolha == "0":
            print("Voltando ao menu principal.")
            break

        if escolha in opcoes:
            descricao, funcao = opcoes[escolha]
            print(f"\nGerando relatorio: {descricao}")
            resultado = funcao()

            if resultado is None:
                print("Relatorio em estrutura base (return vazio).")
            else:
                print(resultado)
        else:
            print("Opcao invalida. Tente novamente.")

        if __name__ == "__main__":
            menu_relatorios()
            

