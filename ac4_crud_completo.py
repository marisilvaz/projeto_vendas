# Avaliação Continuada 4 - 1 ponto
# PROJETO DE VENDAS - parte 2
# Exercicios de CRUD completo (Produtos, Vendedores e Vendas)
# Entrega - dia 24/05/2026

import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from banco_de_dados.conexao import conectar, fechar_conexao

# PRODUTOS

def criar_produto():
    # Exercicio 1: cadastrar um novo produto na tabela produtos (descricao, preco).
    descricao = input("Digite a descrição do produto: ").strip()
    preco = float(input("Digite o preço do produto: "))
    
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        try:
            sql = "INSERT INTO produtos (descricao, preco) VALUES (%s, %s)"
            cursor.execute(sql, (descricao, preco))
            conexao.commit()
            print(f"Produto '{descricao}' cadastrado com sucesso!")
        except Exception as e:
            print(f"Erro ao cadastrar produto: {e}")
        finally:
            cursor.close()
            fechar_conexao(conexao)


def listar_produtos():
    # Exercicio 2: listar todos os produtos cadastrados com id, descricao e preco.
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        try:
            sql = "SELECT id, descricao, preco FROM produtos"
            cursor.execute(sql)
            produtos = cursor.fetchall()
            
            if not produtos:
                print("Nenhum produto cadastrado.")
            else:
                print("\n--- LISTA DE PRODUTOS ---")
                for prod in produtos:
                    print(f"ID: {prod[0]} | Descrição: {prod[1]} | Preço: R$ {prod[2]:.2f}")
        except Exception as e:
            print(f"Erro ao listar produtos: {e}")
        finally:
            cursor.close()
            fechar_conexao(conexao)


def atualizar_produto():
    # Exercicio 3: atualizar descricao e/ou preco de um produto existente por id.
    id_produto = int(input("Digite o ID do produto que deseja atualizar: "))
    nova_descricao = input("Digite a nova descrição (ou deixe em branco para não alterar): ").strip()
    novo_preco_str = input("Digite o novo preço (ou deixe em branco para não alterar): ").strip()
    
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        try:
            # buscamos o produto para saber o valor atual dele
            cursor.execute("SELECT descricao, preco FROM produtos WHERE id = %s", (id_produto,))
            produto = cursor.fetchone()
            
            if not produto:
                print("Produto não encontrado!")
                return
                
            # Se o usuário deixou em branco, mantém o que já estava no banco
            descricao_final = nova_descricao if nova_descricao else produto[0]
            preco_final = float(novo_preco_str) if novo_preco_str else produto[1]
            
            sql = "UPDATE produtos SET descricao = %s, preco = %s WHERE id = %s"
            cursor.execute(sql, (descricao_final, preco_final, id_produto))
            conexao.commit()
            print("Produto atualizado com sucesso!")
        except Exception as e:
            print(f"Erro ao atualizar produto: {e}")
        finally:
            cursor.close()
            fechar_conexao(conexao)


def excluir_produto():
    # Exercicio 4: excluir um produto por id, tratando dependencias em vendas_produtos.
    id_produto = int(input("Digite o ID do produto que deseja excluir: "))
    
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        try:
            print("Removendo vínculos deste produto em vendas antigas...")
            cursor.execute("DELETE FROM vendas_produtos WHERE id_produto = %s", (id_produto,))
            
            sql = "DELETE FROM produtos WHERE id = %s"
            cursor.execute(sql, (id_produto,))
            conexao.commit()
            print("Produto excluído com sucesso!")
        except Exception as e:
            print(f"Erro ao excluir produto: {e}")
        finally:
            cursor.close()
            fechar_conexao(conexao)


# VENDEDORES

def criar_vendedor():
    # Exercicio 5: cadastrar um novo vendedor na tabela vendedores.
    nome = input("Digite o nome do vendedor: ").strip()
    
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        try:
            sql = "INSERT INTO vendedores (nome) VALUES (%s)"
            cursor.execute(sql, (nome,))
            conexao.commit()
            print(f"Vendedor '{nome}' cadastrado com sucesso!")
        except Exception as e:
            print(f"Erro ao cadastrar vendedor: {e}")
        finally:
            cursor.close()
            fechar_conexao(conexao)


def listar_vendedores():
    # Exercicio 6: listar todos os vendedores cadastrados.
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        try:
            sql = "SELECT id, nome FROM vendedores"
            cursor.execute(sql)
            vendedores = cursor.fetchall()
            
            if not vendedores:
                print("Nenhum vendedor cadastrado.")
            else:
                print("\n--- LISTA DE VENDEDORES ---")
                for vend in vendedores:
                    print(f"ID: {vend[0]} | Nome: {vend[1]}")
        except Exception as e:
            print(f"Erro ao listar vendedores: {e}")
        finally:
            cursor.close()
            fechar_conexao(conexao)


def atualizar_vendedor():
    # Exercicio 7: atualizar o nome de um vendedor existente por id.
    id_vendedor = int(input("Digite o ID do vendedor que deseja atualizar: "))
    novo_nome = input("Digite o novo nome (ou deixe em branco para não alterar): ").strip()
    
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        try:
            cursor.execute("SELECT nome FROM vendedores WHERE id = %s", (id_vendedor,))
            vendedor = cursor.fetchone()
            
            if not vendedor:
                print("Vendedor não encontrado!")
                return
                
            nome_final = novo_nome if novo_nome else vendedor[0]
            
            sql = "UPDATE vendedores SET nome = %s WHERE id = %s"
            cursor.execute(sql, (nome_final, id_vendedor))
            conexao.commit()
            print("Vendedor atualizado com sucesso!")
        except Exception as e:
            print(f"Erro ao atualizar vendedor: {e}")
        finally:
            cursor.close()
            fechar_conexao(conexao)


def excluir_vendedor():
    # Exercicio 8: excluir vendedor por id, validando se possui vendas vinculadas.
    id_vendedor = int(input("Digite o ID do vendedor que deseja excluir: "))
    
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM vendas WHERE id_vendedor = %s", (id_vendedor,))
            if cursor.fetchone()[0] > 0:
                print("Não é possível excluir o vendedor. Ele possui vendas vinculadas!")
                return
                
            sql = "DELETE FROM vendedores WHERE id = %s"
            cursor.execute(sql, (id_vendedor,))
            conexao.commit()
            print("Vendedor excluído com sucesso!")
        except Exception as e:
            print(f"Erro ao excluir vendedor: {e}")
        finally:
            cursor.close()
            fechar_conexao(conexao)


# VENDAS

def criar_venda_com_itens():
    # Exercicio 9: criar uma venda e inserir itens na tabela vendas_produtos com quantidade e valores.
    id_vendedor = int(input("Digite o ID do vendedor: "))
    id_produto = int(input("Digite o ID do produto: "))
    quantidade = int(input("Digite a quantidade: "))
    valor_unitario = float(input("Digite o valor unitário: "))
    desconto = float(input("Digite o desconto da venda: "))
    
    valor_final = (quantidade * valor_unitario) - desconto
    
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        try:
            cursor.execute("INSERT INTO vendas (id_vendedor, desconto, valor_final) VALUES (%s, %s, %s)", (id_vendedor, desconto, valor_final))
            id_venda = cursor.lastrowid
            
            cursor.execute("INSERT INTO vendas_produtos (id_venda, id_produto, quantidade, valor_unitario) VALUES (%s, %s, %s, %s)", (id_venda, id_produto, quantidade, valor_unitario))
            
            conexao.commit()
            print(f"Venda registrada com sucesso! ID da Venda: {id_venda}")
        except Exception as e:
            print(f"Erro ao criar venda: {e}")
        finally:
            cursor.close()
            fechar_conexao(conexao)

def listar_vendas_completas():
    # Exercicio 10: listar vendas com vendedor e itens (produto, quantidade, valor_unitario, valor_total).
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        try:
            sql = """
                SELECT v.id, v.id_vendedor, vp.id_produto, vp.quantidade, vp.valor_unitario, v.valor_final 
                FROM vendas v 
                JOIN vendas_produtos vp ON v.id = vp.id_venda
            """
            cursor.execute(sql)
            vendas = cursor.fetchall()
            
            if not vendas:
                print("Nenhuma venda cadastrada.")
            else:
                print("\n--- LISTA DE VENDAS ---")
                for v in vendas:
                    print(f"Venda ID: {v[0]} | Vendedor ID: {v[1]} | Produto ID: {v[2]} | Qtd: {v[3]} | Preço: R$ {v[4]:.2f} | Total Final: R$ {v[5]:.2f}")
        except Exception as e:
            print(f"Erro ao listar vendas: {e}")
        finally:
            cursor.close()
            fechar_conexao(conexao)


def atualizar_venda_e_itens():
    # Exercicio 11: atualizar dados da venda (desconto/valor_final) e seus itens.
    id_venda = int(input("Digite o ID da venda que deseja alterar: "))
    novo_desconto = float(input("Digite o novo valor do desconto: "))
    novo_valor_final = float(input("Digite o novo valor final da venda: "))
    
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        try:
            sql = "UPDATE vendas SET desconto = %s, valor_final = %s WHERE id = %s"
            cursor.execute(sql, (novo_desconto, novo_valor_final, id_venda))
            conexao.commit()
            print("Venda atualizada com sucesso!")
        except Exception as e:
            print(f"Erro ao atualizar venda: {e}")
        finally:
            cursor.close()
            fechar_conexao(conexao)


def excluir_venda():
    # Exercicio 12: excluir uma venda por id removendo primeiro os itens de vendas_produtos.
    id_venda = int(input("Digite o ID da venda que deseja excluir: "))
    
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        try:
            cursor.execute("DELETE FROM vendas_produtos WHERE id_venda = %s", (id_venda,))
            cursor.execute("DELETE FROM vendas WHERE id = %s", (id_venda,))
            conexao.commit()
            print("Venda e seus itens foram excluídos com sucesso!")
        except Exception as e:
            print(f"Erro ao excluir venda: {e}")
        finally:
            cursor.close()
            fechar_conexao(conexao)


def menu():
    opcoes = {
        "1": ("Criar produto", criar_produto),
        "2": ("Listar produtos", listar_produtos),
        "3": ("Atualizar produto", atualizar_produto),
        "4": ("Excluir produto", excluir_produto),
        "5": ("Criar vendedor", criar_vendedor),
        "6": ("Listar vendedores", listar_vendedores),
        "7": ("Atualizar vendedor", atualizar_vendedor),
        "8": ("Excluir vendedor", excluir_vendedor),
        "9": ("Criar venda com itens", criar_venda_com_itens),
        "10": ("Listar vendas completas", listar_vendas_completas),
        "11": ("Atualizar venda e itens", atualizar_venda_e_itens),
        "12": ("Excluir venda", excluir_venda),
    }

    while True:
        print("\n=== MENU AC4 - CRUD COMPLETO ===")
        for codigo, (descricao, _) in opcoes.items():
            print(f"{codigo} - {descricao}")
        print("0 - Voltar")

        escolha = input("Escolha uma opcao: ").strip()

        if escolha == "0":
            print("Voltando ao menu principal.")
            break

        if escolha in opcoes:
            descricao, funcao = opcoes[escolha]
            print(f"\nSelecionado: {descricao}")
            funcao()
            print("Exercicio em estrutura base (return vazio).")
        else:
            print("Opcao invalida. Tente novamente.")
