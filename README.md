# Feature P13 - Consulta de Cotações por Loja


Esta feature permite a consulta das cotações de um determinado período para uma loja específica.


## 🚀 Como Executar a Feature


Antes de rodar a aplicação, certifique-se de que as tabelas "prices" e "stores" do seu banco de dados estejam devidamente populadas.

Para a tarefa agendada, crie uma nova no Windows usando o Agendador de Tarefas.


## 📂 Arquivos Criados para esta Feature


```month_cotation_store.py```

```grafico_cotacoes_loja.py```

```test_*.py```


## ▶️ Para iniciar a aplicação, execute o seguinte comando:


```streamlit run app/pages/manager.py```


## 🧪 Como Executar os Testes


Os testes podem ser executados com o seguinte comando:

```python -m unittest app/testes/test_<nome_do_arquivo_de_teste>.py```

Substitua <nome_do_arquivo_de_teste> pelo nome do arquivo de teste desejado.


## 📌 Observação


Certifique-se de que todas as dependências estão instaladas antes de rodar o projeto.

Para instalação das dependências, utilize:

```pip install -r requirements.txt```
