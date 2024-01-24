import pandas as pd
from abc import ABC, abstractmethod
from getpass import getpass

class Pessoa:
            def __init__(self, nome, idade):
                self.nome, self.idade = nome, idade

            def __str__(self):
                return f"{self.nome}, {self.idade} anos"

class Aluno(Pessoa):
            def __init__(self, nome, idade, status='ativo'):
                super().__init__(nome, idade)
                self.status = status

class AcaoAlunoAbstract(ABC):
            @abstractmethod
            def executar(self, cadastro_alunos, nome_aluno):
                pass

class AdicionarAluno(AcaoAlunoAbstract):
            def executar(self, cadastro_alunos, nome_aluno, idade_aluno):
                aluno = Aluno(nome_aluno, idade_aluno)
                cadastro_alunos.cadastrar_aluno(aluno)

class AdvertirAluno(AcaoAlunoAbstract):
            def executar(self, cadastro_alunos, nome_aluno):
                if cadastro_alunos.verificar_aluno_existente(nome_aluno):
                    index_aluno = cadastro_alunos.obter_index_aluno(nome_aluno)
                    novo_status = 'advertido'
                    cadastro_alunos.atualizar_status_aluno(index_aluno[0], novo_status)
                    print(f"Aluno {nome_aluno} foi {novo_status}.")
                else:
                    print("Aluno não encontrado.")

class ExpulsarAluno(AcaoAlunoAbstract):
            def executar(self, cadastro_alunos, nome_aluno):
                if cadastro_alunos.verificar_aluno_existente(nome_aluno):
                    index_aluno = cadastro_alunos.obter_index_aluno(nome_aluno)
                    novo_status = 'expulso'
                    cadastro_alunos.atualizar_status_aluno(index_aluno[0], novo_status)
                    print(f"Aluno {nome_aluno} foi {novo_status}.")
                else:
                    print("Aluno não encontrado.")

class CadastroAlunos:
            def __init__(self):
                self.dados_alunos = pd.DataFrame(columns=['Nome', 'Idade', 'Status'])
            def cadastrar_aluno(self, aluno):
                if aluno.nome not in self.dados_alunos['Nome'].values:
                    novo_aluno = pd.DataFrame([aluno.__dict__.values()], columns=['Nome', 'Idade', 'Status'])
                    self.dados_alunos = pd.concat([self.dados_alunos, novo_aluno], ignore_index=True)
                    print(f"Aluno {aluno.nome} cadastrado com sucesso.")
                else:
                    print(f"Aluno {aluno.nome} já está cadastrado.")
            def obter_index_aluno(self, nome_aluno):
                return self.dados_alunos.index[self.dados_alunos['Nome'] == nome_aluno].tolist()
            def verificar_aluno_existente(self, nome_aluno):
                return bool(self.obter_index_aluno(nome_aluno))
            def atualizar_status_aluno(self, index, novo_status):
                self.dados_alunos.at[index, 'Status'] = novo_status

class Administrador(Pessoa):
            def __init__(self, nome, idade, senha):
                super().__init__(nome, idade)
                self.senha = senha
            def validar_senha(self, senha):
                return self.senha == senha

class AcoesAluno:
            def __init__(self):
                self.cadastro_alunos = CadastroAlunos()
                self.administrador = Administrador(nome='Admin', idade=30, senha='1234')
                self.tentativas_senha = 3
                self.acoes = {
                    2: AdicionarAluno(),
                    3: AdvertirAluno(),
                    4: ExpulsarAluno()
                }
            def validar_senha_admin(self, senha):
                return self.administrador.validar_senha(senha)
            def acao(self):
                print("\n____MENU____\n1. Painel dos alunos\n2. Adicionar aluno\n3. Advertir aluno\n4. Expulsar aluno\n5. Sair")
                escolha = input("Escolha uma opção: ")
                try:
                    escolha = int(escolha)
                except ValueError:
                    print("Opção inválida. Digite um número.")
                    return True
                if escolha == 1:
                    self.painel_alunos()
                elif escolha in (2, 3, 4):
                    self.executar_acao(escolha)
                elif escolha == 5:
                    print("Encerrando o programa.")
                    return False
                else:
                    print("Opção inválida.")

                return True
            def painel_alunos(self):
                print("Painel de Alunos:")
                print(self.cadastro_alunos.dados_alunos)
            def executar_acao(self, opcao):
                senha = getpass(f"Digite a senha de adm para {['adicionar', 'advertir', 'expulsar'][opcao-2]} aluno: ")
                if self.validar_senha_admin(senha):
                    nome_aluno = input(f"Digite o nome do aluno que será {['adicionado', 'advertido', 'expulso'][opcao-2]}: ")
                    if opcao == 2:
                        try:
                            idade_aluno = int(input("Digite a idade do aluno: "))
                            self.acoes[opcao].executar(self.cadastro_alunos, nome_aluno, idade_aluno)
                        except ValueError:
                            print("Idade deve ser um número inteiro.")
                    else:
                        self.acoes[opcao].executar(self.cadastro_alunos, nome_aluno)
                else:
                    self.tentativas_senha -= 1
                    print(f"Senha de administrador incorreta. Tentativas restantes: {self.tentativas_senha}")

                    if self.tentativas_senha == 0:
                        print("Número máximo de tentativas atingido. Encerrando o programa.")
                        return False
                return True

if __name__ == "__main__":
        acao_aluno = AcoesAluno()
        while True:
            continuar = acao_aluno.acao()
            if not continuar:
                break