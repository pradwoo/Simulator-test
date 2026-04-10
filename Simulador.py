from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

class FormaPagamento(Enum):
    DINHEIRO = "Dinheiro"
    CARTAO = "Cartão"
    PIX = "Pix"

@dataclass
class Cliente:
    data: str
    nome: str
    telefone: str
    carro: str
    placa: str
    servico: str
    valor: float
    pagamento: FormaPagamento

@dataclass
class Item:
    valor: Cliente

@dataclass
class No:
    elemento: Item
    altura: int = 0
    filhoEsq: No | None = None
    filhoDir: No | None = None

class AVL:
    "Representa uma árvore AVL"
    def __init__(self):
        self.raiz: No | None = None

    def vazia(self):
        return self.raiz is None

    # calcula o FB do nó
    def _fb(self, no: No) -> int:
        if no is None:
            return 0
        altSAE = -1 if no.filhoEsq is None else no.filhoEsq.altura
        altSAD = -1 if no.filhoDir is None else no.filhoDir.altura
        return altSAD - altSAE

    # atualiza a altura do nó
    def _atualizaAltura(self, no: No) -> None:
        if no is not None:
            altSAE = -1 if no.filhoEsq is None else no.filhoEsq.altura
            altSAD = -1 if no.filhoDir is None else no.filhoDir.altura
            no.altura = max(altSAE, altSAD) + 1

    # faz rotação simples para a esquerda
    def _rotacionaEsq(self, pai: No) -> No:
        if pai is None:
            raise ValueError('Referência inválida')
        filho = pai.filhoDir
        pai.filhoDir = filho.filhoEsq
        filho.filhoEsq = pai
        self._atualizaAltura(pai)
        self._atualizaAltura(filho)
        return filho

    # faz rotação simples para a direita
    def _rotacionaDir(self, pai: No) -> No:
        if pai is None:
            raise ValueError('Referência inválida')
        filho = pai.filhoEsq
        pai.filhoEsq = filho.filhoDir
        filho.filhoDir = pai
        self._atualizaAltura(pai)
        self._atualizaAltura(filho)
        return filho

    # faz o balanceamento do nó
    def _balanceia(self, no: No) -> No | None:
        if no is not None:
            # desbalanceado para a direita
            if self._fb(no) == 2:
                if self._fb(no.filhoDir) == -1:
                    no.filhoDir = self._rotacionaDir(no.filhoDir)
                # rotaciona para a esquerda
                no = self._rotacionaEsq(no)
            # desbalanceado para a esquerda
            elif self._fb(no) == -2:
                if self._fb(no.filhoEsq) == 1:
                    no.filhoEsq = self._rotacionaEsq(no.filhoEsq)
                # rotaciona para a direita
                no = self._rotacionaDir(no)
        return no

    def insere(self, cliente: Cliente) -> None:
        self.raiz = self._insereNo(Item(cliente), self.raiz)

    def _insereNo(self, elem: Item, raiz: No) -> No:
        if raiz is None:
            raiz = No(elemento=elem)
        else:
            if elem.valor.nome < raiz.elemento.valor.nome:
                raiz.filhoEsq = self._insereNo(elem, raiz.filhoEsq)
            elif elem.valor.nome > raiz.elemento.valor.nome:
                raiz.filhoDir = self._insereNo(elem, raiz.filhoDir)
            # rebalanceando
            self._atualizaAltura(raiz)
            raiz = self._balanceia(raiz)
        return raiz

    def remove(self, cliente: Cliente) -> None:
        self.raiz = self._removeNo(Item(cliente), self.raiz)

    def _removeNo(self, elem: Item, raiz: No) -> No | None:
        if raiz is not None:
            if elem.valor.nome < raiz.elemento.valor.nome:
                raiz.filhoEsq = self._removeNo(elem, raiz.filhoEsq)
            elif elem.valor.nome > raiz.elemento.valor.nome:
                raiz.filhoDir = self._removeNo(elem, raiz.filhoDir)
            else:
                if raiz.filhoEsq is not None and raiz.filhoDir is not None:
                    self._trocaSucessor(raiz)
                    raiz.filhoDir = self._removeNo(elem, raiz.filhoDir)
                elif raiz.filhoEsq is not None:
                    raiz = raiz.filhoEsq
                else:
                    raiz = raiz.filhoDir
            if raiz is not None:
                self._atualizaAltura(raiz)
                raiz = self._balanceia(raiz)
        return raiz

    def _trocaSucessor(self, no: No) -> None:
        sucessor = no.filhoDir
        while sucessor.filhoEsq is not None:
            sucessor = sucessor.filhoEsq
        no.elemento, sucessor.elemento = sucessor.elemento, no.elemento

    def exibe(self) -> None:
        self._exibeNo(self.raiz)
        print()

    def _exibeNo(self, raiz: No) -> None:
        if raiz is not None:
            print('(', end='')
            self._exibeNo(raiz.filhoEsq)
            print(f' {raiz.elemento.valor.nome} ', end='')
            self._exibeNo(raiz.filhoDir)
            print(')', end='')

    def busca(self, placa: str) -> Cliente | None:
        no = self._buscaNo(placa, self.raiz)
        return no.elemento.valor if no is not None else None

    def _buscaNo(self, placa: str, raiz: No) -> No | None:
        if raiz is not None:
            if placa == raiz.elemento.valor.placa:
                return raiz
            elif placa < raiz.elemento.valor.placa:
                return self._buscaNo(placa, raiz.filhoEsq)
            else:
                return self._buscaNo(placa, raiz.filhoDir)
            return None

    def contagem(self) -> int:
        return self._contagemNo(self.raiz)

    def _contagemNo(self, no: No) -> int:
        if no is None:
            return 0
        return 1 + self._contagemNo(no.filhoEsq) + self._contagemNo(no.filhoDir)

    def relatorio_pagamentos(self) -> dict:
        relatorio = {
            FormaPagamento.DINHEIRO: {"quantidade": 0, "valor_total": 0.0},
            FormaPagamento.CARTAO: {"quantidade": 0, "valor_total": 0.0},
            FormaPagamento.PIX: {"quantidade": 0, "valor_total": 0.0}
        }
        self._gera_relatorio(self.raiz, relatorio)
        return relatorio

    def _gera_relatorio(self, no: No, relatorio: dict) -> None:
        if no is not None:
            cliente = no.elemento.valor
            relatorio[cliente.pagamento]["quantidade"] += 1
            relatorio[cliente.pagamento]["valor_total"] += cliente.valor
            self._gera_relatorio(no.filhoEsq, relatorio)
            self._gera_relatorio(no.filhoDir, relatorio)

def main():
    arvore = AVL()

    while True:
        print("Menu de Opções")
        print("1. Registre um cliente")
        print("2. Procure os dados do cliente desejado pela placa do seu carro")
        print("3. Mostrar o relatório de pagamentos do dia")
        print("4. Encerrar o sistema")

        escolha = input("Escolha a opção desejada: ")

        if escolha == "1":
            data = input("Insira a data do registro: ")
            nome = input("Nome do cliente: ")
            telefone = input("Telefone: ")
            carro = input("Carro: ")
            placa = input("Placa do carro: ")
            servico = input("Serviço(s) Realizado(s): ")
            valor = float(input("Valor total do(s) serviço(s): "))
            pagamento = input("Forma de pagamento (Dinheiro, Cartão, Pix): ").upper()
            pagamento_enum = FormaPagamento[pagamento]
            cliente = Cliente(data, nome, telefone, carro, placa, servico, valor, pagamento_enum)
            arvore.insere(cliente)
            print("O cliente foi registrado com sucesso.")
        
        elif escolha == "2":
            placa = input("Digite a placa para pesquisar o cliente: ")
            cliente_encontrado = arvore.busca(placa)
            if cliente_encontrado:
                print("Cliente encontrado!")
                print(f"Data: {cliente_encontrado.data}, Nome: {cliente_encontrado.nome}, Telefone: {cliente_encontrado.telefone}, Carro: {cliente_encontrado.carro}, Placa: {cliente_encontrado.placa} Serviço: {cliente_encontrado.servico}, Valor: {cliente_encontrado.valor}, Pagamento: {cliente_encontrado.pagamento.value}")
            else:
                print("Cliente não encontrado ou não foi feito o registro.")

        elif escolha == "3":
            relatorio = arvore.relatorio_pagamentos()
            print("Relatório de Pagamentos do dia:")
            for forma, dados in relatorio.items():
                print(f"{forma.value}: {dados['quantidade']} pagamentos, Total: R${dados['valor_total']:.2f}")

        elif escolha == "4":
            print("Encerrando o sistema, aguarde...")
            break
        else:
            print("Opção inválida. Escolha uma opção válida (1, 2, 3 ou 4)")

if __name__ == "__main__":
    main()