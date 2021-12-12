import psycopg2

conn = psycopg2.connect(user = "postgres", database = "movie_test", password = "176211", host = "127.0.0.1")
cur = conn.cursor()

table = "movie"
query_4 = "SELECT c.relname, a.amname FROM pg_class c, pg_namespace n, pg_am a WHERE (c.relkind = 'r' or c.relkind = 'i') AND n.oid = c.relnamespace AND not(nspname like 'pg_%' or nspname = 'information_schema') and c.relam = a.oid "
full_query = query_4 + "and c.relname = '%s'; "%table
cur.execute(full_query)

result  = cur.fetchall()
print(result)