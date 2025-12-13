import uuid
import sqlite3

import UI

class App:
    def __init__(self):
       
        self.data=None
        
        self.datafilepath="data.db"
        

        
        
        #id INTEGER PRIMARY KEY AUTOINCREMENT,
        
        con = sqlite3.connect(self.datafilepath)
        cur=con.cursor()
        cur.execute('''
                    CREATE TABLE If NOT EXISTS notes (
                    id TEXT PRIMARY KEY,
                    title TEXT,
                    body TEXT
                    )
                    ''')
    
        self.load_all_data()

        #load the data from the db if not connected to internet
        #if internet is on load from the server

        con.commit()
        con.close()

        self.ui=UI.UI(self)
        
        #save in a json or somewhere is_synced=True

    def run(self):
        self.ui.mainloop()


    def load_all_data(self):
        
        con = sqlite3.connect(self.datafilepath)
        cur=con.cursor()
        cur.execute("SELECT * from notes")
    
        self.data=cur.fetchall()
        
        con.commit()
        con.close()

    
    def save_note(self, data):
        note_id=data[0]
        
        #update the local data instance
        for i in range(len(self.data)):
            if (self.data[i])[0]==note_id:
                self.data[i]=data



        
        con = sqlite3.connect(self.datafilepath)
        cur=con.cursor()
        
        cur.execute('''SELECT 1 FROM notes WHERE id = ?''', (note_id,))
        if cur.fetchone():


            cur.execute('''
                        UPDATE notes
                        SET title = ?, body = ?
                        WHERE id = ?
                        ''', (data[1], data[2], note_id,))
        else:
            cur.execute('''
                        INSERT INTO notes
                        (id, title, body) VALUES (?, ?, ?)
                           ''', data)

        con.commit()
        con.close()

    
    def delete_note(self, note_id):

        #update the local data instance
        for i in range(len(self.data)):
            if (self.data[i])[0]==note_id:
                del self.data[i]
                break

    

        con = sqlite3.connect(self.datafilepath)
        cur=con.cursor()
        
        cur.execute('''DELETE FROM notes WHERE id = ?''', (note_id,))

        con.commit()
        con.close()

    #dont know if we should keep data [()] or [[]]
    def create_note(self):
        note_id=str(uuid.uuid4())
        new_note_data=(note_id, "", "")
        self.data.append(new_note_data)
        return new_note_data

    def app_note_closed(self, data):
        #do saving here
        pass



