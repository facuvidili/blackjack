import mysql.connector
class DBconnectSingleton:
    _instance = None

    def __new__(self):
        if self._instance is None:
            self._instance = super().__new__(self)
            # Iniciar DB
            self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="blackjack"
            
        )   
        return self._instance
    
    def get_all(self, attr, table):
        mycursor = self.mydb.cursor()
        mycursor.execute("SELECT " + attr + " FROM " + table)
        return mycursor.fetchall()
    
    def get_card_id(self, rank, suit):
        mycursor = self.mydb.cursor()
        mycursor.execute("SELECT id FROM mazo WHERE valorCarta = '" + str(rank) + "' AND tipoCarta = '" + str(suit) + "'")
        cardId = mycursor.fetchone()
        return cardId
    
    def update_all(self, deck, players):
        mycursor = self.mydb.cursor()
        mycursor.execute("UPDATE mazo SET estado = 0")
        for card in deck.cards:
            mycursor.execute("UPDATE mazo SET estado = 1 WHERE tipoCarta = '" + str(card.get_suit()) + "' AND valorCarta = '" + str(card.get_rank()) + "'")


        mycursor.execute("DELETE FROM manoactual")
        mycursor.execute("ALTER TABLE manoactual AUTO_INCREMENT=0;")
        mycursor.execute("DELETE FROM jugadores")
        mycursor.execute("ALTER TABLE jugadores AUTO_INCREMENT=0;")
       
        for index, player in enumerate(players):
            mycursor.execute("INSERT INTO jugadores (id, nombre, saldo) VALUES ('" + str(index+1) + "', '"  + player.name + "', '" + str(player.ammount) + "')")
            cards = player.get_hand().get_cards()
            for i, card in enumerate(cards):   
                print(self.get_card_id(card.rank, card.suit)[0])
                mycursor.execute("INSERT INTO manoactual (idCarta, idJugador) VALUES ('"
                              + str(self.get_card_id(card.rank, card.suit)[0]) 
                              + "', '" + str(index+1) + "')")
        self.mydb.commit()

    def remove_one(self, id, table):
        mycursor = self.mydb.cursor()
        mycursor.execute("DELETE FROM manoactual WHERE idJugador = '" + str(id+1) + "'")
        mycursor.execute("DELETE FROM '" + table + "' WHERE id = '" + str(id+1) + "'")
        self.mydb.commit()
    
