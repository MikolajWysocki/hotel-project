import mysql.connector

# Konfiguracja połączenia
db_config = {
    'host': 'localhost',     # Adres serwera MySQL
    'user': 'marektowarek', # Nazwa użytkownika
    'password': 'marek1234', # Hasło użytkownika
    'database': 'hotel-db'   # Nazwa bazy danych
}

# Nawiązywanie połączenia
try:
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Przykład zapytania
    cursor.execute("SELECT * FROM twoja_tabela")
    results = cursor.fetchall()

    for row in results:
        print(row)

except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
