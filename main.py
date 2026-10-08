from abc import ABC, abstractmethod


class Cliente:
    def __init__(self, nome: str, cpf: str, email: str):
        self.nome = nome
        self.cpf = cpf
        self.email = email

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valor: str):
        if "@" not in valor or "." not in valor:
            raise ValueError("E-mail inválido! Deve conter '@' e '.'.")
        self._email = valor

    def __str__(self) -> str:
        return f"{self.nome} (CPF: {self.cpf})"

    def __repr__(self) -> str:
        return f"Cliente(nome='{self.nome}', cpf='{self.cpf}')"


class Conta(ABC):
    def __init__(self, numero: int, cliente: Cliente, saldo_inicial: float = 0.0):
        self.numero = numero
        self.cliente = cliente
        self.saldo = saldo_inicial

    @property
    def saldo(self) -> float:
        return self._saldo

    @saldo.setter
    def saldo(self, valor: float):
        if valor < 0:
            raise ValueError("O saldo inicial ou atual não pode ser negativo.")
        self._saldo = valor

    def depositar(self, valor: float):
        if valor <= 0:
            raise ValueError("O valor do depósito deve ser positivo.")
        self._saldo += valor

    def sacar(self, valor: float) -> bool:
        if valor <= 0:
            raise ValueError("O valor do saque deve ser positivo.")
        if valor > self._saldo:
            print(f"Saldo insuficiente na conta {self.numero}.")
            return False
        self._saldo -= valor
        return True

    @abstractmethod
    def rendimento_mensal(self) -> float:
        pass

    def __str__(self) -> str:
        return f"Conta {self.numero} - Titular: {self.cliente.nome} | Saldo: R$ {self.saldo:.2f}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(numero={self.numero}, saldo={self.saldo})"

    def __eq__(self, outro) -> bool:
        if isinstance(outro, Conta):
            return self.numero == outro.numero
        return False

    def __lt__(self, outro) -> bool:
        if isinstance(outro, Conta):
            return self.saldo < outro.saldo
        return NotImplemented


class ContaCorrente(Conta):
    def __init__(self, numero: int, cliente: Cliente, saldo_inicial: float = 0.0, limite: float = 500.0):
        super().__init__(numero, cliente, saldo_inicial)
        self.limite = limite

    def sacar(self, valor: float) -> bool:
        if valor <= 0:
            raise ValueError("O valor do saque deve ser positivo.")
        if valor > (self.saldo + self.limite):
            print(f"Saque recusado na conta corrente {self.numero}.")
            return False
        self._saldo -= valor
        return True

    def rendimento_mensal(self) -> float:
        taxa = 15.0
        self._saldo -= taxa
        return -taxa

    def __str__(self) -> str:
        return f"[Corrente] {super().__str__()} (Limite: R$ {self.limite:.2f})"


class ContaPoupanca(Conta):
    def __init__(self, numero: int, cliente: Cliente, saldo_inicial: float = 0.0, taxa_juros: float = 0.005):
        super().__init__(numero, cliente, saldo_inicial)
        self.taxa_juros = taxa_juros

    def rendimento_mensal(self) -> float:
        ganho = self.saldo * self.taxa_juros
        self._saldo += ganho
        return ganho

    def __str__(self) -> str:
        return f"[Poupança] {super().__str__()} (Taxa: {self.taxa_juros * 100:.1f}%)"


# Demonstração e testes
if __name__ == "__main__":
    print("--- Instanciando Clientes e Contas ---")

    c1 = Cliente("Matheus Frois", "111.222.333-04", "matheus@email.com")
    c2 = Cliente("Ana Silva", "222.333.444-05", "ana.silva@email.com")
    c3 = Cliente("Carlos Eduardo", "333.444.555-06", "carlos@email.com")
    c4 = Cliente("Beatriz Lima", "444.555.666-07", "beatriz@email.com")

    cc1 = ContaCorrente(101, c1, saldo_inicial=1200.0, limite=800.0)
    cc2 = ContaCorrente(102, c2, saldo_inicial=2500.0, limite=1000.0)
    cc3 = ContaCorrente(103, c3, saldo_inicial=300.0, limite=300.0)

    cp1 = ContaPoupanca(201, c1, saldo_inicial=5000.0)
    cp2 = ContaPoupanca(202, c3, saldo_inicial=10000.0, taxa_juros=0.007)
    cp3 = ContaPoupanca(203, c4, saldo_inicial=1500.0)

    contas = [cc1, cc2, cc3, cp1, cp2, cp3]

    print("\n--- Estado Inicial das Contas ---")
    for conta in contas:
        print(conta)

    print("\n--- Polimorfismo (Rendimento Mensal) ---")
    for conta in contas:
        variacao = conta.rendimento_mensal()
        print(f"Conta {conta.numero}: Variação = R$ {variacao:.2f} | Saldo final = R$ {conta.saldo:.2f}")

    print("\n--- Teste de Métodos Dunder ---")
    contas_ordenadas = sorted(contas)
    print("Menor saldo:", contas_ordenadas[0])
    print("Maior saldo:", contas_ordenadas[-1])

    cc_teste = ContaCorrente(101, c1, 500.0)
    print(f"cc1 é igual a cc_teste? {cc1 == cc_teste}")

    print("\n--- Teste de Validações (Exceções) ---")
    try:
        c_erro = Cliente("João", "000.000.000-00", "email_sem_arroba")
    except ValueError as e:
        print(f"Erro em Cliente: {e}")

    try:
        conta_erro = ContaCorrente(999, c1, saldo_inicial=-100.0)
    except ValueError as e:
        print(f"Erro em Conta: {e}")
