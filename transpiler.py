import re

class Token:
    """Classe para representar um token"""
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

    def __repr__(self):
        return f"Token({self.tipo}, {self.valor})"

class Lexer:
    """Analisador Léxico"""
    def __init__(self, texto):
        self.texto = texto
        self.pos = 0
        self.caractere_atual = self.texto[self.pos]
        self.niveis_indentacao = []  # Armazena os níveis de indentação
        self.nivel_atual = 0  # Nível atual de indentação

    def error(self):
        raise Exception(f'Erro de análise no token: {self.caractere_atual}')

    def avancar(self):
        self.pos += 1
        if self.pos > len(self.texto) - 1:
            self.caractere_atual = None
        else:
            self.caractere_atual = self.texto[self.pos]

    def ignorar_espacos(self):
        while self.caractere_atual is not None and self.caractere_atual.isspace():
            self.avancar()

    def identificar_variavel(self):
        resultado = ''
        while self.caractere_atual is not None and (self.caractere_atual.isalnum() or self.caractere_atual == '_'):
            resultado += self.caractere_atual
            self.avancar()
        return Token('VAR', resultado)

    def identificar_numero(self):
        resultado = ''
        while self.caractere_atual is not None and self.caractere_atual.isdigit():
            resultado += self.caractere_atual
            self.avancar()
        return Token('NUM', int(resultado))

    def identificar_indentacao(self):
        nivel_indentacao = 0
        while self.caractere_atual == ' ':
            nivel_indentacao += 1
            self.avancar()
        return nivel_indentacao

    def obter_token(self):
        while self.caractere_atual is not None:
            if self.caractere_atual.isspace():
                if self.caractere_atual == ' ':
                    # Identifica nível de indentação
                    nivel_indentacao = self.identificar_indentacao()
                    if self.pos == 0 or self.texto[self.pos - 1] == '\n':
                        self.niveis_indentacao.append(nivel_indentacao)
                self.ignorar_espacos()
                continue
            if self.caractere_atual.isalpha():
                palavra = ''
                while self.caractere_atual is not None and (self.caractere_atual.isalnum() or self.caractere_atual == '_'):
                    palavra += self.caractere_atual
                    self.avancar()
                if palavra == 'if':
                    return Token('IF', 'if')
                elif palavra == 'elif':
                    return Token('ELIF', 'elif')
                elif palavra == 'else':
                    return Token('ELSE', 'else')
                elif palavra == 'while':
                    return Token('WHILE', 'while')
                else:
                    return Token('VAR', palavra)
            if self.caractere_atual.isdigit():
                return self.identificar_numero()
            if self.caractere_atual in '+-*/':
                operador = self.caractere_atual
                self.avancar()
                return Token('OPERATOR', operador)
            if self.caractere_atual == '=':
                self.avancar()
                if self.caractere_atual == '=':
                    self.avancar()
                    return Token('EQ', '==')
                return Token('ASSIGN', '=')
            if self.caractere_atual == '<':
                self.avancar()
                if self.caractere_atual == '=':
                    self.avancar()
                    return Token('LE', '<=')
                return Token('LT', '<')
            if self.caractere_atual == '>':
                self.avancar()
                if self.caractere_atual == '=':
                    self.avancar()
                    return Token('GE', '>=')
                return Token('GT', '>')
            if self.caractere_atual == '!':
                self.avancar()
                if self.caractere_atual == '=':
                    self.avancar()
                    return Token('NEQ', '!=')
                self.error()
            if self.caractere_atual == '&':
                self.avancar()
                if self.caractere_atual == '&':
                    self.avancar()
                    return Token('AND', '&&')
                self.error()
            if self.caractere_atual == '|':
                self.avancar()
                if self.caractere_atual == '|':
                    self.avancar()
                    return Token('OR', '||')
                self.error()
            if self.caractere_atual == '\n':
                self.avancar()
                return Token('NEWLINE', '\n')
            self.error()
        return Token('EOF', None)


class Parser:
    """Analisador Sintático"""
    def __init__(self, lexer):
        self.lexer = lexer
        self.token_atual = self.lexer.obter_token()
        self.indentacoes = self.lexer.niveis_indentacao
        self.indentacao_atual = 0
        print(f"Token inicial: {self.token_atual}")

    def error(self):
        raise Exception(f'Erro de análise com o token: {self.token_atual}')

    def consumir(self, tipo_token):
        print(f"Tentando consumir: {tipo_token}, Token atual: {self.token_atual}")
        if self.token_atual.tipo == tipo_token:
            self.token_atual = self.lexer.obter_token()
            print(f"Consumido com sucesso, próximo token: {self.token_atual}")
        else:
            print(f"Token esperado: {tipo_token}, Token encontrado: {self.token_atual}")
            self.error()

    def ignorar_newline(self):
        """Ignorar tokens de nova linha até encontrar um token não-newline"""
        while self.token_atual.tipo == 'NEWLINE':
            self.token_atual = self.lexer.obter_token()

    def parse_expressao(self):
        """Parse uma expressão aritmética ou lógica"""
        resultado = self.parse_term()

        while self.token_atual.tipo in ('OPERATOR', 'EQ', 'NEQ', 'LT', 'LE', 'GT', 'GE', 'AND', 'OR'):
            operador = self.token_atual
            print(f"Encontrado operador: {operador}")
            if operador.tipo in ('OPERATOR', 'AND', 'OR'):
                self.consumir(operador.tipo)
                termo = self.parse_term()
                resultado = f"{resultado} {operador.valor} {termo}"
            else:
                self.consumir(operador.tipo)
                fator = self.parse_fator()
                resultado = f"{resultado} {operador.valor} {fator}"

        return resultado

    def parse_term(self):
        """Parse um termo aritmético"""
        resultado = self.parse_fator()

        while self.token_atual.tipo == 'OPERATOR' and self.token_atual.valor in ('*', '/'):
            operador = self.token_atual
            self.consumir('OPERATOR')
            fator = self.parse_fator()
            resultado = f"({resultado} {operador.valor} {fator})"

        return resultado

    def parse_fator(self):
        """Parse um fator aritmético ou lógico"""
        if self.token_atual.tipo == 'NUM':
            valor = self.token_atual.valor
            self.consumir('NUM')
            return valor
        elif self.token_atual.tipo == 'VAR':
            variavel = self.token_atual.valor
            self.consumir('VAR')
            return variavel
        else:
            self.error()

    def parse_if(self):
        """Parse um bloco if"""
        condicional = []
        self.consumir('IF')
        condicao = self.parse_expressao()
        condicional.append(f"if ({condicao}) {{")
        self.ignorar_newline()

        while self.token_atual.tipo not in ('ELIF', 'ELSE', 'EOF', 'NEWLINE'):
            if self.token_atual.tipo == 'VAR':
                variavel = self.token_atual.valor
                self.consumir('VAR')
                self.consumir('ASSIGN')
                expressao = self.parse_expressao()
                condicional.append(f"    var {variavel} = {expressao};")
                self.ignorar_newline()
            elif self.token_atual.tipo == 'NEWLINE':
                self.ignorar_newline()
            else:
                print(f"Erro na análise condicional. Token atual: {self.token_atual}")
                self.error()

        condicional.append("}")
        condicional.extend(self.parse_elif())
        condicional.extend(self.parse_else())

        return condicional

    def parse_elif(self):
        """Parse um bloco elif"""
        condicional = []

        while self.token_atual.tipo == 'ELIF':
            self.consumir('ELIF')
            condicao = self.parse_expressao()
            condicional.append(f"else if ({condicao}) {{")
            self.ignorar_newline()

            while self.token_atual.tipo not in ('ELIF', 'ELSE', 'EOF', 'NEWLINE'):
                if self.token_atual.tipo == 'VAR':
                    variavel = self.token_atual.valor
                    self.consumir('VAR')
                    self.consumir('ASSIGN')
                    expressao = self.parse_expressao()
                    condicional.append(f"    var {variavel} = {expressao};")
                    self.ignorar_newline()
                elif self.token_atual.tipo == 'NEWLINE':
                    self.ignorar_newline()
                else:
                    print(f"Erro na análise elif. Token atual: {self.token_atual}")
                    self.error()

            condicional.append("}")

        return condicional

    def parse_else(self):
        """Parse um bloco else"""
        condicional = []

        if self.token_atual.tipo == 'ELSE':
            self.consumir('ELSE')
            condicional.append("else {")
            self.ignorar_newline()

            while self.token_atual.tipo not in ('EOF', 'NEWLINE'):
                if self.token_atual.tipo == 'VAR':
                    variavel = self.token_atual.valor
                    self.consumir('VAR')
                    self.consumir('ASSIGN')
                    expressao = self.parse_expressao()
                    condicional.append(f"    var {variavel} = {expressao};")
                    self.ignorar_newline()
                elif self.token_atual.tipo == 'NEWLINE':
                    self.ignorar_newline()
                else:
                    print(f"Erro na análise else. Token atual: {self.token_atual}")
                    self.error()

            condicional.append("}")

        return condicional

    def parse_while(self):
        """Parse um loop while"""
        loop = []
        self.consumir('WHILE')
        condicao = self.parse_expressao()
        loop.append(f"while ({condicao}) {{")
        self.ignorar_newline()

        # Controle do nível de indentação
        nivel_bloco = 1  # O nível do bloco do while começa com 1
        while self.token_atual.tipo not in ('EOF', 'NEWLINE', 'IF', 'ELIF', 'ELSE'):
            if self.token_atual.tipo == 'WHILE':
                nivel_bloco += 1
                loop.extend(self.parse_while())  # Recursivamente trata loops aninhados
            elif self.token_atual.tipo == 'IF':
                nivel_bloco += 1
                loop.extend(self.parse_if())  # Recursivamente trata condicionais aninhadas
            elif self.token_atual.tipo == 'ELIF':
                nivel_bloco += 1
                loop.extend(self.parse_elif())  # Recursivamente trata condicionais aninhadas
            elif self.token_atual.tipo == 'ELSE':
                nivel_bloco += 1
                loop.extend(self.parse_else())  # Recursivamente trata condicionais aninhadas
            elif self.token_atual.tipo == 'VAR':
                variavel = self.token_atual.valor
                self.consumir('VAR')
                self.consumir('ASSIGN')
                expressao = self.parse_expressao()
                loop.append(f"    var {variavel} = {expressao};")
                self.ignorar_newline()
            elif self.token_atual.tipo == 'NEWLINE':
                self.ignorar_newline()
            else:
                if nivel_bloco == 1:
                    break  # Sai do loop quando o nível do bloco volta ao inicial
                else:
                    print(f"Erro na análise do loop while. Token atual: {self.token_atual}")
                    self.error()

        loop.append("}")
        return loop
    
    def parse_atribuicao(self):
        """Parse atribuições"""
        atribuicoes = []
        while self.token_atual.tipo != 'EOF':
            if self.token_atual.tipo == 'VAR':
                variavel = self.token_atual.valor
                self.consumir('VAR')
                self.consumir('ASSIGN')
                expressao = self.parse_expressao()
                atribuicoes.append(f"var {variavel} = {expressao};")
                self.ignorar_newline()
            elif self.token_atual.tipo == 'WHILE':
                atribuicoes.extend(self.parse_while())
            elif self.token_atual.tipo == 'IF':
                atribuicoes.extend(self.parse_if())
            elif self.token_atual.tipo == 'ELIF':
                atribuicoes.extend(self.parse_elif())
            elif self.token_atual.tipo == 'ELSE':
                atribuicoes.extend(self.parse_else())
            elif self.token_atual.tipo == 'NEWLINE':
                self.ignorar_newline()
            else:
                print(f"Erro na análise. Token atual: {self.token_atual}")
                self.error()

        return atribuicoes



def transpilar(codigo_python):
    """Transpilar código Python para JavaScript"""
    lexer = Lexer(codigo_python)
    parser = Parser(lexer)
    print("\nNíveis de indentação identificados:")
    for nivel in lexer.niveis_indentacao:
        print(f"Nível de indentação: {nivel}")
    return "\n".join(parser.parse_atribuicao())
    

# Exemplo de uso
codigo_python = """
y = 1
x = 3 + 5 * 2 - 8 / 4
a = 5 > 3
b = x == 10 || y != 1
while x < 10
    x = x + 7
if x > 5
    y = 10
elif x == 3
    y = 20
elif x == 3
    y = 20
else
    y = 30
"""

codigo_javascript = transpilar(codigo_python)
print(codigo_javascript)
