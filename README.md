# 🌤️ Relatório Meteorológico Automático

Este projeto coleta dados meteorológicos atualizados da API [Open-Meteo](https://open-meteo.com/), gera dashboards com visualização profissional usando Seaborn e envia um relatório por e-mail automaticamente todos os dias.

## 🚀 Objetivo

Fornecer um relatório automatizado e visualmente atrativo sobre as condições climáticas atuais e futuras de uma localidade específica. O projeto foi desenvolvido para ser executado em servidores locais ou via **GitHub Actions**, sem necessidade de interação manual.

---

## 📊 Funcionalidades

- Coleta de dados meteorológicos **horários e diários**.
- Geração de **dashboard profissional (PNG)** com:
  - Temperatura real e sensação térmica.
  - Umidade relativa do ar.
  - Velocidade e direção do vento.
  - Probabilidade de precipitação (chuva/chuvisco).
  - Índice UV.
  - Máxima/mínima do dia.
- Envio automático de e-mail com:
  - Relatório visual (.png) como anexo.
  - Título e corpo do e-mail personalizados.
- Execução local manual ou via **GitHub Actions (CRON: 03h BRT)**.

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia       | Uso                                                   |
|------------------|--------------------------------------------------------|
| Python 3.11      | Lógica de coleta, visualização e envio                |
| Open-Meteo API   | Fonte dos dados climáticos                            |
| Pandas/Requests  | Manipulação e requisições de dados                    |
| Seaborn/Matplotlib| Visualização gráfica com layout profissional         |
| Jinja2           | Template HTML para dashboard                          |
| Playwright       | Renderização e conversão de HTML → PNG               |
| Python-dotenv    | Leitura de variáveis de ambiente (.env)               |
| GitHub Actions   | Execução automatizada com **Docker container**        |
| smtplib/email    | Envio automático de e-mails                           |


---

## 📁 Estrutura do Projeto

```
│ ├── .gitignore # Arquivos/pastas ignorados pelo Git
│ ├── .env # Variáveis de ambiente (não versionado)
│ ├── LICENSE # Licença do projeto
│ ├── README.md # Este arquivo
│ ├── requirements.txt # Dependências do projeto
│ ├── init.py # Inicialização do pacote (opcional)
│
├── .github/
│ └── workflows/
│ └── send_report.yml # Workflow do GitHub Actions para envio automático de relatórios
│
├── data/
│ └── outputs/
│ ├── comparative_graph.png # Gráfico comparativo de temperaturas
│ └── weather_dashboard.png # Dashboard meteorológico principal
│
├── src/
│ ├── weather_report/
│ │ ├── email_sender.py # Envio de relatórios por e-mail
│ │ ├── main.py # Script principal para orquestração
│ │ ├── report_creator.py # Geração do conteúdo do relatório
│ │ ├── weather_comparison.py # Comparação climática entre períodos
│ │ ├── weather_config.py # Configurações gerais do projeto
│ │ ├── weather_dashboard.py # Geração do dashboard em imagem
│ │ ├── weather_functions.py # Funções auxiliares (coleta e processamento)
│ │ └── init.py # Inicialização do módulo
│ │
│ └── pycache/ # Cache de execução dos scripts
│
└── pycache/ # Cache compilado de scripts no nível raiz
```

## 🔐 Variáveis de Ambiente (.env)

Crie um arquivo `.env` com as seguintes variáveis:

```env
EMAIL_REMETENTE=seu_email@gmail.com
SENHA_APP=sua_senha_de_aplicativo
EMAIL_DESTINATARIO=email_destino@gmail.com
LATITUDE=-22.8751
LONGITUDE=-43.3386
TIMEZONE=America/Sao_Paulo
```

## 🤖 Execução Automática (GitHub Actions com Docker)

O projeto inclui um workflow automático (`.github/workflows/weather_report.yml`) que executa diariamente às **03:00 (BRT)** utilizando uma **imagem Docker personalizada**.

### ✅ Vantagens do Uso de Docker

- Garante que o **Playwright** funcione corretamente com o **Chromium headless**.  
- Elimina conflitos de dependências em **runners do GitHub**.  
- Proporciona uma execução estável e idêntica à do **ambiente local**.  

---

### 🔐 Secrets Necessários

> Configure os secrets em **Settings → Secrets and variables → Actions → New repository secret**

| Nome do Secret     | Descrição                                               |
|--------------------|---------------------------------------------------------|
| `EMAIL_REMETENTE`  | E-mail de origem (com SMTP habilitado)                 |
| `SENHA_APP`        | Senha de app gerada (Gmail, por exemplo)              |
| `EMAIL_DESTINATARIO` | E-mail que receberá o relatório                      |
| `LATITUDE`         | Latitude da localidade desejada                         |
| `LONGITUDE`        | Longitude da localidade desejada                        |
| `TIMEZONE`         | Timezone da região (ex: `America/Sao_Paulo`)           |

## 🧪 Execução Local

### Clone o repositório:

```bash
git clone https://github.com/seuusuario/relatorio_tempo.git
cd relatorio_tempo
```

### Crie e ative o ambiente virtual:

```
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### Instale as dependências:

```
pip install -r requirements.txt
playwright install --with-deps
```

### Execute o script principal:

```
python src/weather_report/main.py
```

## 🚧 Possíveis Melhorias Futuras

- Suporte a múltiplas localidades por vez  
- Envio via Telegram ou WhatsApp  
- Exportação em PDF além de PNG  
- Dashboard interativo em HTML  

## 👨‍💻 Autor

Desenvolvido por **Caio Viegas**  
Contato: [LinkedIn](https://www.linkedin.com/in/caio-costa-viegas-593614219/) | caio.costaviegas@gmail.com

## 📝 Licença

Este projeto está licenciado sob a **MIT License**.
