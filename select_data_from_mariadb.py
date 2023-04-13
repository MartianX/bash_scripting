import os
import sys
import mysql.connector
import paramiko

def connect_and_select(host, username, pkey_path, db_user, db_password, db_name, table_name):
    try:
        # Charger la clé privée RSA
        private_key = paramiko.RSAKey.from_private_key_file(pkey_path)

        # Paramètres pour la connexion SSH
        ssh_config = {
            'hostname': host,
            'username': username,
            'pkey': private_key,
            'allow_agent': False,
            'look_for_keys': False
        }

        # Paramètres de connexion à la base de données
        db_config = {
            'user': db_user,
            'password': db_password,
            'host': '127.0.0.1',
            'port': 3306,
            'database': db_name
        }

        # Établir la connexion SSH
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(**ssh_config)

        # Établir la connexion à la base de données via le tunnel SSH
        ssh_transport = ssh_client.get_transport()
        local_port = ssh_transport.request_port_forward('', db_config['port'])
        conn = mysql.connector.connect(
            user=db_config['user'],
            password=db_config['password'],
            host='127.0.0.1',
            port=local_port,
            database=db_config['database']
        )
        cursor = conn.cursor()

        # Exécuter une requête SELECT
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        # Afficher les résultats
        print("Résultats de la requête SELECT :")
        for row in rows:
            print(row)

        # Fermer le curseur et la connexion
        cursor.close()
        conn.close()

        # Fermer la connexion SSH
        ssh_client.close()

    except mysql.connector.Error as e:
        print(f"Erreur de connexion à la base de données : {e}")


if __name__ == '__main__':
    # Vérifier le nombre d'arguments
    if len(sys.argv) != 8:
        print("Usage: python3 script.py host username pkey_path db_user db_password db_name table_name")
        sys.exit(1)

    # Récupérer les arguments de ligne de commande
    host = sys.argv[1]
    username = sys.argv[2]
    pkey_path = sys.argv[3]
    db_user = sys.argv[4]
    db_password = sys.argv[5]
    db_name = sys.argv[6]
    table_name = sys.argv[7]

    # Appeler la fonction de connexion et de requête SELECT
    connect_and_select(host, username, pkey_path, db_user, db_password, db_name, table_name)
