# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# MAGIC %md
# MAGIC # Ingestão — Supabase → Databricks
# MAGIC **Tabelas:** `avaliacoes_lider` (identificação + qualitativo) e `avaliacoes_itens` (1 linha por item avaliado)
# MAGIC **Projeto:** Programa Psicólogos nas Escolas
# MAGIC
# MAGIC ⚠️ Estrutura mudou em 09/09/2026: as colunas `escuta_1_nota`, `entregas_nota` etc.
# MAGIC foram removidas de `avaliacoes_lider`. Cada item avaliado agora é uma linha em
# MAGIC `avaliacoes_itens`, já com `ure`, `email_respondente` e `nome_lider` replicados.

# COMMAND ----------

import requests
import pandas as pd

SUPABASE_URL = "https://blczadrtgbgkrjewbqxo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJsY3phZHJ0Z2Jna3JqZXdicXhvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4NzgzNzI5NiwiZXhwIjoyMTAzNDEzMjk2fQ.K4T7WiG_FcIM7VFP_zO72_TOk_HEr420r5dmFVZFwKo"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
}

def fetch_all(table, order_col="created_at"):
    """Busca todos os registros de uma tabela, paginando de 1000 em 1000."""
    all_records = []
    offset = 0
    limit = 1000
    while True:
        resp = requests.get(
            f"{SUPABASE_URL}/rest/v1/{table}",
            headers={**headers, "Range": f"{offset}-{offset+limit-1}"},
            params={"select": "*", "order": f"{order_col}.asc"},
        )
        data = resp.json()
        if not data:
            break
        all_records.extend(data)
        if len(data) < limit:
            break
        offset += limit
    return pd.DataFrame(all_records)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Leitura das duas tabelas

# COMMAND ----------

df_lider_pd = fetch_all("avaliacoes_lider")
df_itens_pd = fetch_all("avaliacoes_itens", order_col="respondido_em")

print(f"avaliacoes_lider: {len(df_lider_pd)} registros")
print(f"avaliacoes_itens: {len(df_itens_pd)} registros")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Views temporárias para SQL

# COMMAND ----------

df_lider = spark.createDataFrame(df_lider_pd)
df_itens = spark.createDataFrame(df_itens_pd)

df_lider.createOrReplaceTempView("avaliacoes_lider")
df_itens.createOrReplaceTempView("avaliacoes_itens")

display(df_itens)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Visão geral por perfil

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     perfil_respondente,
# MAGIC     COUNT(*)                       AS total_respostas,
# MAGIC     COUNT(DISTINCT nome_lider)     AS lideres_avaliados,
# MAGIC     COUNT(DISTINCT ure)            AS ures_representadas
# MAGIC FROM avaliacoes_lider
# MAGIC GROUP BY perfil_respondente
# MAGIC ORDER BY total_respostas DESC

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Médias por Líder, por Competência e Comportamento
# MAGIC Direto de `avaliacoes_itens`, sem pivotar — 1 linha por combinação de líder × comportamento,
# MAGIC com o texto completo do comportamento avaliado.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     nome_lider,
# MAGIC     ure,
# MAGIC     competencia,
# MAGIC     comportamento_titulo,
# MAGIC     comportamento_descricao,
# MAGIC     ROUND(AVG(nota), 2)      AS nota_media,
# MAGIC     COUNT(*)                 AS total_avaliadores,
# MAGIC     SUM(CASE WHEN sem_insumos THEN 1 ELSE 0 END) AS sem_insumos_count
# MAGIC FROM avaliacoes_itens
# MAGIC WHERE competencia != 'Entregas'
# MAGIC GROUP BY nome_lider, ure, competencia, comportamento_titulo, comportamento_descricao
# MAGIC ORDER BY nome_lider, competencia, comportamento_titulo

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Nota de Entregas — somente Gestor

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     i.nome_lider,
# MAGIC     i.ure,
# MAGIC     i.nota                          AS entregas_nota,
# MAGIC     i.opcao_texto                   AS entregas_opcao_texto,
# MAGIC     i.sem_insumos                   AS entregas_sem_insumos,
# MAGIC     l.qualitativo_entregas_gestor
# MAGIC FROM avaliacoes_itens i
# MAGIC JOIN avaliacoes_lider l ON l.id = i.avaliacao_id
# MAGIC WHERE i.competencia = 'Entregas'
# MAGIC ORDER BY i.nome_lider

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Respostas qualitativas

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     nome_lider,
# MAGIC     ure,
# MAGIC     perfil_respondente,
# MAGIC     qualitativo_desenvolvimento,
# MAGIC     qualitativo_destaques
# MAGIC FROM avaliacoes_lider
# MAGIC WHERE qualitativo_desenvolvimento IS NOT NULL
# MAGIC    OR qualitativo_destaques IS NOT NULL
# MAGIC ORDER BY nome_lider

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7. (Opcional) Salvar como Delta table permanente

# COMMAND ----------

# Descomente para persistir no Unity Catalog
# df_itens.write.format("delta").mode("overwrite").saveAsTable("citem.coin_hub.avaliacoes_itens")
# df_lider.write.format("delta").mode("overwrite").saveAsTable("citem.coin_hub.avaliacoes_lider")
# print("Tabelas salvas!")
