## Funcionalidade: Gerenciamento de Produção dos Pesquisadores

Esta feature adiciona à página do **Gestor** uma nova aba chamada `Gerenciar Pesquisadores`, onde é possível consultar a **produção mensal** de cada pesquisador com base nas pesquisas cadastradas no sistema.

---

### O que esta funcionalidade permite:

- Selecionar um pesquisador e um intervalo de tempo (mês/ano)
- Visualizar a produção (quantidade de pesquisas realizadas por dia)
- Ver os dados em **formato de tabela e gráfico**

---

###  Arquivos envolvidos

| Arquivo | Função |
|--------|--------|
| `pages/manager.py` | Página do Gestor com a nova aba “Gerenciar Pesquisadores” |
| `database/research_stats.py` | Função `get_research_data()` que busca os dados de produção no banco de dados |

---

### Pré-requisitos para funcionamento

1. **Tabela no banco de dados: `research_stats`**

```sql
CREATE TABLE research_stats (
    id SERIAL PRIMARY KEY,
    pesquisador_id INTEGER NOT NULL,
    search_date DATE NOT NULL,
    search_count INTEGER NOT NULL
);
```

2. **Dados preenchidos** na tabela `research_stats`, com o seguinte padrão:

| pesquisador_id | search_date | search_count |
|----------------|-------------|---------------|
| 1              | 2024-10-01  | 5             |
| 2              | 2024-10-01  | 3             |
| ...            | ...         | ...           |

3. **Usuários cadastrados** com papel `pesquisador` na tabela `users`.

---

###  Observações

- A funcionalidade só estará visível para usuários com o papel `gestor`.
- A visualização dos dados usa `matplotlib` e `streamlit` para renderizar tabela e gráfico.
- A coleta dos dados parte da função `get_research_data()` localizada em `database/research_stats.py`.

