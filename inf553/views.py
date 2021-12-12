from django.http.response import HttpResponse
from django.template import loader
from django.shortcuts import render
import psycopg2

def index(request):
    #database connection variables
    host = "localhost"
    database="movie_test"
    user="postgres"
    password="176211"
    port=5432
    #connect to postgres and query the FK-PK pairs of tables
    con = psycopg2.connect(host=host,database=database,  user=user, password=password, port=port)
    query = """SELECT tablename
FROM pg_catalog.pg_tables
WHERE schemaname != 'pg_catalog' AND
    schemaname != 'information_schema'; """
    #print(query)

    cur = con.cursor()
     # create view myattr
    query_7 = "create view myattr as with mytables as (select c.oid, c.relname from pg_class c, pg_namespace n where c.relkind='r' and n.oid=c.relnamespace and not(nspname like 'pg_%' or nspname='information_schema')) select t.relname, a.attname, y.typname from mytables t, pg_attribute a, pg_type y where t.oid=a.attrelid and a.atttypid=y.oid and y.typname='varchar';"
    cur.execute(query_7)
    con.commit()

    cur.execute(query)
    tables = cur.fetchall()

    # # create view myattr
    # query_7 = "create view myattr as with mytables as (select c.oid, c.relname from pg_class c, pg_namespace n where c.relkind='r' and n.oid=c.relnamespace and not(nspname like 'pg_%' or nspname='information_schema')) select t.relname, a.attname, y.typname from mytables t, pg_attribute a, pg_type y where t.oid=a.attrelid and a.atttypid=y.oid and y.typname='varchar';"
    # cur.execute(query_7)
    template = loader.get_template('inf553/index.html')
    context = {
        'tables': tables,
    }
    #return render(request, 'inf553/index.html', {'tables': tables})
    return HttpResponse(template.render(context, request))


def detail(request, table):
    #database connection variables
    host = "localhost"
    database="movie_test"
    user="postgres"
    password="176211"
    port=5432
    #connect to postgres and query the FK-PK pairs of tables
    con = psycopg2.connect(host=host,database=database,  user=user, password=password, port=port)
    
    # Queries set

    query_4 = "SELECT c.relname, a.amname FROM pg_class c, pg_namespace n, pg_am a WHERE (c.relkind = 'r' or c.relkind = 'i') AND n.oid = c.relnamespace AND not(nspname like 'pg_%' or nspname = 'information_schema') and c.relam = a.oid "
    full_query_4 = query_4 + "and c.relname = '%s'; "%table
    
    query_5 = "with mytables as (select c.oid, c.relname FROM pg_class c, pg_namespace n WHERE c.relkind='r' and n.oid = c.relnamespace and not (nspname like 'pg_%' or nspname = 'information_schema')) SELECT t.relname, a.attname, y.typname from mytables t, pg_attribute a, pg_type y where t.oid = a.attrelid and a.atttypid = y.oid and y.typname='varchar'"
    full_query_5 = query_5 + "and t.relname = '%s';"%table

    # query_7 = "create view myattr as with mytables as (select c.oid, c.relname from pg_class c, pg_namespace n where c.relkind='r' and n.oid=c.relnamespace and not(nspname like 'pg_%' or nspname='information_schema')) select t.relname, a.attname, y.typname from mytables t, pg_attribute a, pg_type y where t.oid=a.attrelid and a.atttypid=y.oid and y.typname='varchar';"
    full_query_7 = """
with aux as
(select tablename, attname, n_distinct as ndist, histogram_bounds::text::varchar[] as bound
from pg_stats
where (tablename, attname) in (select relname, attname from myattr))
select tablename, attname, ceil(ndist*(-1)*n_live_tup) as distval, bound[1] as min, bound[array_length(bound,
1)] as max   
from aux, pg_stat_user_tables sut
where sut.relname=aux.tablename""" + " and aux.tablename = '%s';"%table

    cur = con.cursor()

    cur.execute(full_query_4)
    results_4 = cur.fetchall()

    cur.execute(full_query_5)
    results_5 = cur.fetchall()
    
    cur.execute(full_query_7)
    results_7 = cur.fetchall()

    results = cur.fetchall()
    template = loader.get_template('inf553/detail.html')
    context = {
        'results_4': results_4, 
        'results_5': results_5,
        'results_7': results_7,
    }
    return HttpResponse(template.render(context, request))