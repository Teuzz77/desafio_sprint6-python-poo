# Sistema de Gestão Bancária - Python POO (Sprint 6)

Projeto desenvolvido em Python aplicando os pilares da Programação Orientada a Objetos (POO): Abstração, Encapsulamento, Herança e Polimorfismo.

## 📌 Diagrama de Classes

```mermaid
classDiagram
    class Cliente {
        +str nome
        +str cpf
        -str _email
        +email: str
    }

    class Conta {
        <<Abstract>>
        +int numero
        +Cliente cliente
        -float _saldo
        +saldo: float
        +depositar(valor: float)
        +sacar(valor: float) bool
        +rendimento_mensal()* float
    }

    class ContaCorrente {
        +float limite
        +sacar(valor: float) bool
        +rendimento_mensal() float
    }

    class ContaPoupanca {
        +float taxa_juros
        +rendimento_mensal() float
    }

    Conta <|-- ContaCorrente
    Conta <|-- ContaPoupanca
    Conta "1" *-- "1" Cliente
