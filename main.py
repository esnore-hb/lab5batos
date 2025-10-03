import psycopg2
import psycopg2.extras
import csv
import re

# hola soy la bea

"""
Integrantes:
- Beatriz Toledo
- Hector Bonilla
- Lazaro Narvaez
"""

# alias de tablas
SUPERHERO = "superheroes.tindanime_superhero"
CHARACTER = "superheroes.tindanime_character"
ALTEREGO = "superheroes.tindanime_alterego"
WORKOCUPATION = "superheroes.tindanime_workocupation"

# Modifique este metodo para adaptarlo a su lógica.
def findOrInsert(table, name):
    cur.execute("select id from "+table+" where name=%s limit 1", [name])
    r = cur.fetchone()
    if(r):
        return r[0]
    else:
        cur.execute("insert into "+table+" (name) values (%s) returning id", [name])
        return cur.fetchone()[0]

# Establecer conexion con la base de datos
conn = psycopg2.connect(host = "cc3201.dcc.uchile.cl", database = "cc3201", user = "cc3201", password = "j'<3_cc3201",port = "5440")
cur = conn.cursor()

# vaciar tablas
cur.execute("TRUNCATE superheroes.tindanime_superhero * RESTART IDENTITY CASCADE")

with open("Laboratorio_5_superheroes_data.csv") as csvfile:
    f = csv.reader(csvfile, delimiter = ',', quotechar = '"')
    i = 0
    for row in f:
        i += 1
        if i == 1: continue

    # Filtrado de elementos

        # forma: string, obligatorio tener
        name = row[1].strip().strip('"')

        # forma: string, ""
        biography_name = row[8].strip().strip('"')

        # forma: No alter egos found., nombre
        alterego = [m.strip().strip('"') for m in re.split('[,;]',row[9])]
        alterego = list(filter(lambda x: len(x) > 0, alterego))
        if alterego == ["No alter egos found."]: alterego = []

        height = (row[17].strip()).split(sep = "'")
        if len(height) == 2:
            height = float(".".join(height))
        elif len(height) > 1:
            height = int(height[0])
        else: height = 0

        weight = "- lb" # forma: 123 lb, - lb
        if row[19] == weight: weight = 0
        elif row[19] != weight:
            weight = int(row[19].strip().split()[0])

        work_ocupation = "-" # forma: separado por ,; y algunos con (former, actual)
        if row[23] == work_ocupation: work_ocupation = []
        elif row[23] != work_ocupation:
            work_ocupation = [m.strip().strip('"') for m in re.split('[,;]', row[23])]

    # Agregar cada elemento a las tablas
    #    print(f"name: {name}", f"biography: {biography_name}", f"alterego {alterego}", f"height: {height}", f"weight:{weight}", f"work: {work_ocupation}", sep='\n',end='\n------\n')

        # Agregamos al heroe en si
        cur.execute("SELECT id FROM "+SUPERHERO+" WHERE name = %s LIMIT 1", [name]) # como si fuera printf de pss
        r = cur.fetchone()
        name_id = None
        if(r):
            name_id = r[0]
        else:
            cur.execute("INSERT INTO "+SUPERHERO+" (name, height, weight) VALUES (%s, %s, %s) RETURNING ID", [name, height, weight])
            name_id = cur.fetchone()[0]
        
        # Agregamos su nombre real con el id del superheroe
        cur.execute("SELECT id FROM "+CHARACTER+" WHERE biography_name = %s LIMIT 1", [biography_name])
        r = cur.fetchone()
        biography_name_id = None
        if(r):
            biography_name_id = r[0]
        else:
            cur.execute("INSERT INTO "+CHARACTER+" (superhero_id, biography_name) VALUES (%s, %s) RETURNING ID", [name_id, biography_name])
            biography_name_id = cur.fetchone()[0]

        # Agregamos sus alteregos con el id del superheroe
        for alterego_name in alterego:
            cur.execute("SELECT id FROM "+ALTEREGO+" WHERE alterego_name = %s LIMIT 1", [alterego_name])
            r = cur.fetchone()
            alterego_name_id = None
            if(r):
                alterego_name_id = r[0]
            else:
                cur.execute("INSERT INTO "+ALTEREGO+" (superhero_id, alterego_name) VALUES (%s, %s) RETURNING ID", [name_id, alterego_name])
                alterego_name_id = cur.fetchone()[0]
        
        # Agregamos su workocupation
        for work in work_ocupation:
            cur.execute("SELECT id FROM "+WORKOCUPATION+" WHERE work_name = %s LIMIT 1", [work])
            r = cur.fetchone()
            work_name_id = None
            if(r):
                work_name_id = r[0]
            else:
                cur.execute("INSERT INTO "+WORKOCUPATION+" (superhero_id, work_name) VALUES (%s, %s) RETURNING ID", [name_id, work])
                work_name_id = cur.fetchone()[0]

    # Ejecutamos las solicitudes
    cur.execute("SELECT * FROM "+SUPERHERO+" LIMIT 10")
    row = cur.fetchone()
    while row:
        print(row)
        row = cur.fetchone()
    print("--- nueva tabla ---")

    cur.execute("SELECT * FROM "+CHARACTER+" LIMIT 10")
    row = cur.fetchone()
    while row:
        print(row)
        row = cur.fetchone()

    print("--- nueva tabla ---")

    cur.execute("SELECT * FROM "+ALTEREGO+" LIMIT 10")
    row = cur.fetchone()
    while row:
        print(row)
        row = cur.fetchone()

    print("--- nueva tabla ---")

    cur.execute("SELECT * FROM "+WORKOCUPATION+" LIMIT 10")
    row = cur.fetchone()
    while row:
        print(row)
        row = cur.fetchone()

conn.commit()
conn.close()
