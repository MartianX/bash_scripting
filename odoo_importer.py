import xmlrpc.client
import csv
import sys

# Informations de connexion au serveur Odoo
url = 'http://localhost:8069'
db = 'db_test'
username = 'test'
password = 'test'

# Se connecter au serveur Odoo
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

if not uid:
    print('Impossible de se connecter au serveur Odoo. Vérifiez vos informations de connexion.')
    sys.exit(1)

# Se connecter à l'objet product.product
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# Charger les données depuis le fichier CSV
csv_file_path = sys.argv[1]  # Chemin du fichier CSV passé en argument

with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        # Extraire les données du CSV
        product_name = row['product_name']
        price = float(row['price'])
        variant_name_1 = row['variant_name_1']
        variant_value_1 = row['variant_value_1']
        variant_name_2 = row['variant_name_2']
        variant_value_2 = row['variant_value_2']
        variant_barcode = row['variant_barcode']
        
        # Créer un dictionnaire pour les valeurs des attributs
        attribute_values = []
        if variant_name_1 and variant_value_1:
            attribute_values.append((4, models.execute_kw(db, uid, password, 'product.attribute.value',
                                                        'search', [[('name', '=', variant_value_1)]]), 0, 0))
        if variant_name_2 and variant_value_2:
            attribute_values.append((4, models.execute_kw(db, uid, password, 'product.attribute.value',
                                                        'search', [[('name', '=', variant_value_2)]]), 0, 0))

        # Créer le produit avec les variantes
        product_id = models.execute_kw(db, uid, password, 'product.product', 'create', [{
            'name': product_name,
            'lst_price': price,
            'attribute_value_ids': attribute_values,
            'barcode': variant_barcode
        }])
        print(f'Produit créé avec ID : {product_id}')
