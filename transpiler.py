class PythonToJavaScriptTranspiler:
    def transpile(self, python_code):
        # Separa as linhas do código Python
        lines = python_code.splitlines()
        js_code = []

        for line in lines:
            line = line.strip()
            if line.startswith("def "):
                # Declaração de função
                js_code.append(self.transpile_function(line))
            elif "=" in line:
                # Declaração/Atribuição de variáveis
                js_code.append(self.transpile_assignment(line))
            elif line.startswith("if "):
                # Comando condicional
                js_code.append(self.transpile_if(line))
            elif line.startswith("for ") or line.startswith("while "):
                # Comando de repetição
                js_code.append(self.transpile_loop(line))
            elif "and" in line or "or" in line:
                # Expressões lógicas
                js_code.append(self.transpile_logical(line))
            else:
                # Expressões aritméticas
                js_code.append(self.transpile_expression(line))

        return "\n".join(js_code)

    def transpile_function(self, line):
        line = line.replace("def ", "function ")
        line = line.replace(":", " {")
        return line

    def transpile_assignment(self, line):
        return line.replace("=", " = ")

    def transpile_if(self, line):
        line = line.replace("if ", "if (")
        line = line.replace(":", ") {")
        return line

    def transpile_loop(self, line):
        if line.startswith("for "):
            line = line.replace("for ", "for (")
            line = line.replace(":", ") {")
        elif line.startswith("while "):
            line = line.replace("while ", "while (")
            line = line.replace(":", ") {")
        return line

    def transpile_logical(self, line):
        line = line.replace("and", "&&").replace("or", "||")
        return line

    def transpile_expression(self, line):
        return line  # Simplesmente retorna a linha (para expressões aritméticas)

# Exemplo de uso
transpiler = PythonToJavaScriptTranspiler()
python_code = """
def soma(a, b):
    return a + b

x = 10
y = 20
if x > y:
    print(x)
else:
    print(y)

for i in range(5):
    print(i)

while x > 0:
    x -= 1

if x == 0 and y > 0:
    print("x é zero")
"""

js_code = transpiler.transpile(python_code)
print(js_code)