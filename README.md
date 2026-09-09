# 🎬 Monitor de Novos Vídeos do JW.ORG com Notificação via Telegram / WhatsApp

Este projeto executa um agendamento no **GitHub Actions** que verifica periodicamente (a cada 30 minutos) a publicação de novos vídeos no site **JW.ORG** e envia uma notificação instantânea para o seu **Telegram** (e/ou **WhatsApp**).

---

## 🚀 Como Funciona

1. O **GitHub Actions** roda a cada 30 minutos (usando `cron`).
2. O script `check_videos.py` consulta o catálogo de vídeos recentes da CDN do JW.ORG (`b.jw-cdn.org`).
3. Compara os vídeos retornados com a lista do arquivo `history.json`.
4. Se houver vídeos novos:
   - Envia uma mensagem personalizada para o seu **Telegram** e/ou **WhatsApp**.
   - Atualiza o arquivo `history.json` e faz commit automático no repositório.

---

## 📲 Passo a Passo: Configurar Notificação no Telegram (Recomendado)

### 1. Criar o Bot no Telegram:
1. No Telegram, procure por **`@BotFather`**.
2. Inicie a conversa e envie: `/newbot`.
3. Escolha o nome do bot (ex: `Notificador JW`).
4. Escolha o username (deve terminar com `bot`, ex: `jw_meu_notificador_bot`).
5. Copie o **Token de API** recebido (ex: `7123456789:AAFn8x...`).

### 2. Obter seu Chat ID:
1. No Telegram, procure por **`@userinfobot`**.
2. Clique em **Iniciar** (ou envie `/start`).
3. Ele responderá com o seu **Id** (ex: `123456789`).

### 3. Iniciar o seu Bot:
1. Abra a conversa com o seu próprio bot recém-criado (ex: `@jw_meu_notificador_bot`).
2. Clique em **Iniciar** (ou envie `/start`) para autorizá-lo a te enviar mensagens.

---

## 🔑 Configurar os Secrets no GitHub

No seu repositório no GitHub:

1. Vá em **Settings** > **Secrets and variables** > **Actions**.
2. Clique em **New repository secret** e adicione:
   - **`TELEGRAM_BOT_TOKEN`**: O token que você recebeu do `@BotFather`.
   - **`TELEGRAM_CHAT_ID`**: O seu ID que você recebeu do `@userinfobot`.

*(Opcional: Se quiser receber no WhatsApp também quando o CallMeBot estiver liberado, basta adicionar `CALLMEBOT_PHONE` e `CALLMEBOT_APIKEY`).*

---

## ⚙️ Habilitar Permissão de Escrita no GitHub Actions

1. Vá em **Settings** > **Actions** > **General**.
2. Role até a seção **Workflow permissions**.
3. Selecione a opção **Read and write permissions**.
4. Clique em **Save**.

---

## 🧪 Testar Manualmente

1. Na aba **Actions** do seu repositório, selecione **JW.ORG New Videos Checker**.
2. Clique no botão **Run workflow** > **Run workflow**.
3. Você receberá uma notificação sempre que houver novidades!
