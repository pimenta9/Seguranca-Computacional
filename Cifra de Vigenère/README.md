# Projeto 1

- cifrador.cpp: dados uma **mensagem** e uma **senha**, o cifrador transforma a mensagem em um criptograma usando aquela senha.
Instruções de uso:
  1. Compile e execute o código.
  2. Escreva no terminal a mensagem a ser criptografada. A mensagem deve ser composta por letras maiúsculas sem acentos ou sinais gráficos. Caracteres que não seguem esse padrão serão simplesmente ignorados.
  3. Escreva a palavra-senha no mesmo padrão descrito no item anterior.
  4. O criptograma será escrito no terminal e em um arquivo de texto que será criado (se ainda não existir) no diretório.

- tamanho.cpp: dados um **criptograma** e um **tamanho de segmento**, o "tamanho" calcula os tamanhos mais prováveis tamanhos da senha.
Instruções de uso:
  1. Compile e execute o código.
  2. Digite o tamanho dos segmentos. Exêmplo: 2 -> palavras de 2 letras, 3 -> palavras de 3 letras.
  3. Não é necessário digitar o criptograma, o código pega o criptograma que estiver escrito no arquivo "criptograma".
  4. O resultado será escrito no arquivo "tamanho.txt" e não será escrito no terminal. Mais informações do resultado no relatório.

- ataque.cpp: dados um **criptograma**, o **tamanho da chave** e o **idioma** (inglês ou português), o ataque usando análise de frequência retorna a senha mais provável.
Instruções de uso:
  1. Compile e execute o código.
  2. Digite o criptograma.
  3. Digite o (provável) tamanho da senha.
  4. Digite 0 se o plaintext é em inglês e 1 se for em português.
  5. O programa analisa as frequências das letras e retorna a palavra-senha mais provável.
  6. Use este resultado no decifrador.

- decifrador.cpp: dados um **criptograma** e uma **senha**, o cifrador transforma o criptograma na mensagem original.
Instruções de uso:
  1. Compile e execute o código.
  2. Escreva no terminal o criptograma a ser descriptografado. O criptograma deve ser composto por letras maiúsculas sem acentos ou sinais gráficos. Caracteres que não seguem esse padrão serão simplesmente ignorados.
  3. Escreva a palavra-senha no mesmo padrão descrito no item anterior.
  4. A mensagem decifrada será escrita no terminal.
