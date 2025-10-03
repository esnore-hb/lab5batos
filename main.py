import psycopg2
import psycopg2.extras
import csv
import re

"""
Integrantes:
- Beatriz Toledo
- Hector Bonilla
- Lazaro Narvaez
"""

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
conn = psycopg2.connect(host = "cc3201.dcc.uchile.cl",
                        database = "cc3201",
                        user = "cc3201",
                        password = "j'<3_cc3201",port = "5440")

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
        alterego = "No alter egos found."
        if alterego == "No alter egos found.": alterego = []
        elif row[9] != alterego: alterego = [m.strip().strip('"') for m in re.split('[,;]', row[9])]
        else: alterego = []
        alterego = list(filter(lambda x: len(x) > 0, alterego))

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



conn.commit()
conn.close()
