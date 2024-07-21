## DESCRIÇÃO DO TRABALHO
Nosso trabalho da UNIDADE III da disciplina de COMPILADORES compreende a construção de um transpilador que recebe instruções na linguagem PYTHON e os converte para a linguagem JAVASCRIPT. A escolha pelas linguagens fonte e objeto representa um misto de usabilidade e atualidade destas no que tange ao reconhecimento por parte dos integrantes do grupo tanto em suas atividades acadêmicas, trabalhistas, bem como nos estágios curriculares.
No que tange à justificativa mesma de tal trabalho, há que se considerar que o processo da construção de um transpilador consiste numa atividade prática de construção de um analisador léxico que, de modo geral, representa os primeiros passos para a construção de compiladores, uma vez que essa prática se serve dos conhecimentos adquiridos na disciplina, transformando-os num exercício ativo acerca do funcionamento de um compilador de compilador, como é o caso do YACC.
Por outro lado, a construção de um transpilador é importante no sentido de adequar o uso de linguagens que, tendo um formato mais antigo, cedem lugar a novas versões, como é o caso do próprio JAVASCRIPT, cujas sintaxes mais atuais inserem novos comandos e utilizações implicando em dominar novas sintaxes da linguagem ou atualizar comandos. Nesse sentido, por meio de um transpilador, essa tarefa passa a se dar por conta da ferramenta que vai apreender as instâncias do código original, alterando-as segundo as necessidades do código fim.
No caso do Javascript, especificamente, essa passagem é bastante significativa uma vez que esta é uma linguagem muito utilizada para uso na internet, na construção de páginas web que comportam vários “objetos”. Uma transpilação para Javascript pode fazer funcionar programas escritos em Linguagem C, por exemplo, cuja afinidade com os recursos da internet é muito baixa.

## Tokens usados no transpilador:
### Tokens Comuns
1. Variáveis e Identificadores
    - VAR: Identificadores ou variáveis (e.g., x, resultado, soma).
Operadores

OPERATOR: Operadores aritméticos e relacionais (e.g., +, -, *, /, %, ==, !=, <, >, <=, >=, &&, ||).
Delimitadores

LPAREN: Parêntese esquerdo (
RPAREN: Parêntese direito )
LBRACE: Colchete esquerdo {
RBRACE: Colchete direito }
COMMA: Vírgula ,
DOT: Ponto .
Atribuições

ASSIGN: Operador de atribuição =
RETURN: Palavra-chave return
Comandos Condicionais e Laços

IF: Palavra-chave if
ELIF: Palavra-chave elif (ou else if)
ELSE: Palavra-chave else
WHILE: Palavra-chave while
FOR: Palavra-chave for (se necessário para laços)
BREAK: Palavra-chave break (para saídas antecipadas do laço)
CONTINUE: Palavra-chave continue (para pular iterações)
Definição de Funções

DEF: Palavra-chave def (para definição de funções)
FUNCNAME: Nome da função (identificador após def)
Outros Tokens

NEWLINE: Quebra de linha (para identificar fim de uma instrução)
EOF: Fim do arquivo (indica que não há mais tokens para ler)
NUMBER: Literal numérico (e.g., 123, 45.67)
STRING: Literais de string (se suportado, e.g., "texto")
COMMENT: Comentários (se suportado, e.g., # comentário)
