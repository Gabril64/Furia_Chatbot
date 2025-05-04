# Teste Furia_Chatbot

Conforme solicitado no Teste , foi criado um ChatBot que promove uma experiência conversacional com o usuário, juntamente com uma Landing page que simula o site oficial da FURIA.


============================================
  Estrutura do projeto
============================================

Furia_Chatbot/
├── main.py              # Script principal (servidor/backend)
├── index.html           # Interface web
├── user_data.json       # Armazena dados de usuários
├── bot.log              # Log do sistema
└── imagens/             # Imagens utilizadas na interface

============================================
  COMO INICIALIZAR ?
============================================

Inicialmente temos que rodar o CHATBOT para que a aplicação possa funcionar com um todo, dessa forma basta seguir o passo a passo abaixo: 

1    Baixar as bibliotecas utilizadas:
   - Aplicação em si utilizada o python como base, dessa forma além do mesmo utilizamos a biblioteca telebot, dotenv e enum.
   - Para instalar todas as bibliotecas necessárias para a aplicação você precisará usar os seguintes comandos no terminal: pip install pyTelegramBotAPI python-dotenv
   - Se você também quiser instalar a biblioteca logging (embora ela já venha com o Python por padrão) e garantir que todas as dependências estejam atualizadas: pip install --upgrade pyTelegramBotAPI python-dotenv

2    Criar e gerar a API Token:
   - Acesse o telegram e através do BotFather crie um bot e gere a sua API Token 

3    Anexar a sua API Token:
   - Acesse o arquivo main.py e na linha 21 altere o token para o seu Token emitido anteriormente

4    Inicialiar a aplicação:
   - Após devidamente atualizado o token é hora de iniciar sua aplicação através da IDE desejada.

5    Landing page:
   - A Landing page em questão funciona mais como uma página cópia da página da fúria, onde você poderá ser acessada através do link : https://gabril64.github.io/Furia_Chatbot/
   - A página acima está com o link de acesso ao bot original, dessa forma não irá encaminhar para o bot criado em sua máquina, porém caso deseje rodar a página em seu computador, você pode editar o arquivo index.html e alterar na linha 401 o link original (https://t.me/furiaboy_bot), para o link do seu bot.
