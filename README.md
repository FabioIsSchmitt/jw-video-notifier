# 🎬 Monitor de Novos Vídeos do JW.ORG com Notificação via CallMeBot (WhatsApp)

Este projeto executa um agendamento no **GitHub Actions** que verifica periodicamente (a cada 30 minutos) a publicação de novos vídeos no site **JW.ORG** e envia uma notificação instantânea para o seu **WhatsApp** usando a API gratuita do **CallMeBot**.

---

## 🚀 Como Funciona

1. O **GitHub Actions** roda a cada 30 minutos (usando `cron`).
2. O script `check_videos.py` consulta o catálogo oficial de vídeos recentes da CDN do JW.ORG (`b.jw-cdn.org`).
3. Compara os vídeos retornados com a lista do arquivo `history.json`.
4. Se houver vídeos novos:
   - Envia uma mensagem personalizada para o seu WhatsApp via **CallMeBot**.
   - Atualiza o arquivo `history.json` e faz commit automático no repositório.

---

## 📲 Passo 1: Obter a Chave do CallMeBot (Gratuito)

Para receber mensagens no WhatsApp pelo CallMeBot:

1. Adicione o número do CallMeBot aos seus contatos do WhatsApp:
   - **`+34 644 44 24 19`** (ou `+34 644 93 98 78` dependendo da disponibilidade no site [callmebot.com](https://www.callmebot.com/blog/free-api-whatsapp-messages/)).
2. Envie a seguinte mensagem pelo WhatsApp para esse número:
   ```text
   I allow callmebot to send me messages
   ```
3. O bot responderá em poucos segundos com a sua **API Key**, por exemplo:
   ```text
   API Key created successfully! Your API key is: 123456
   ```
4. Guarde o seu **número com DDI e DDD** (ex: `5511999999999`) e a **API Key**.

---

## 🔑 Passo 2: Configurar os Secrets no GitHub

No seu repositório no GitHub:

1. Vá em **Settings** (Configurações do repositório).
2. No menu lateral esquerdo, clique em **Secrets and variables** > **Actions**.
3. Clique no botão verde **New repository secret** e adicione:
   - **Nome:** `CALLMEBOT_PHONE`
     - **Valor:** Seu número com DDI e DDD, sem espaços ou símbolos (ex: `5511999999999`).
   - **Nome:** `CALLMEBOT_APIKEY`
     - **Valor:** O código/número da chave recebida do CallMeBot.

---

## ⚙️ Passo 3: Habilitar Permissão de Escrita no GitHub Actions

Para que o GitHub Actions consiga atualizar o arquivo `history.json` automaticamente:

1. Vá em **Settings** > **Actions** > **General**.
2. Role até a seção **Workflow permissions**.
3. Selecione a opção **Read and write permissions**.
4. Clique em **Save**.

---

## 🧪 Passo 4: Testar o Funcionamento

1. No seu repositório, clique na aba **Actions**.
2. No menu à esquerda, clique no workflow **JW.ORG New Videos Checker**.
3. Clique no botão **Run workflow** > **Run workflow**.
4. O GitHub executará a checagem imediatamente.

---

## 📁 Estrutura do Projeto

```text
├── .github/
│   └── workflows/
│       └── check_jw_videos.yml  # Agendamento e execução no GitHub Actions
├── check_videos.py              # Script principal em Python
├── history.json                 # Registro dos vídeos já notificados
└── README.md                    # Instruções de configuração
```
