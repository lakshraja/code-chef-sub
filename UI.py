import tkinter as tk

import math

WINDOW_WIDTH=800
WINDOW_HEIGHT=600


NOTELIST_ELEMENT_WIDTH=250
NOTELIST_ELEMENT_HEIGHT=215


class UI(tk.Tk):
    def __init__(self, controller):
        super().__init__()

        self.title("Notes App Demo")
        self.geometry(str(WINDOW_WIDTH)+'x'+str(WINDOW_HEIGHT))
        self.resizable(False, False)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.controller=controller

        self.load_notelist()

    def load_notelist(self):
        self.current_frame=NoteList(self, self.load_note, self.create_new_note, self.delete_note, self.controller.data)
        self.current_frame.pack(fill="both", expand=True)
    

    #better to do this
    #def load_note(self, note_id):
    #but this is more convinient
    def load_note(self, data):
        self.unload_frame()
        self.current_frame=Note(self, self.note_closed, data)
        self.current_frame.pack(fill="both", expand=True)
        


    #better name
    #note_closed or on_note_closd or close_note
    def note_closed(self, data):
        self.controller.save_note(data)
        
        self.unload_frame()
        self.load_notelist()


    def create_new_note(self):
        self.unload_frame()
        new_note_data=self.controller.create_note()
        self.load_note(new_note_data)

        #delete current frame
        #load new note frame

    def unload_frame(self):
        if not self.current_frame: return
        self.current_frame.pack_forget()
        self.current_frame.destroy()
        #del self.current_frame
        self.current_frame=None

    def on_closing(self):
        if isinstance(self.current_frame, Note):
            self.current_frame.return_button_pressed()
        self.destroy()

    def refresh_note_list(self):
        self.unload_frame()
        self.load_notelist()

    def delete_note(self, note_id):
        self.controller.delete_note(note_id)
        
        self.refresh_note_list()



class NoteList(tk.Frame):
    def __init__(self, parent, load_note_callback, add_button_callback, delete_button_callback, data):
        super().__init__(parent)
        
        
        self.add_button_callback=add_button_callback
        self.load_note_callback=load_note_callback
        self.delete_button_callback=delete_button_callback

        self.add_note_button=tk.Button(self, text="+", pady=0, padx=0, bd=0, bg="#ffffff", command=self.add_note_button_pressed)
        self.add_note_button.pack(anchor="nw")


        self.canvas=tk.Canvas(self)
        self.scrollbar= tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollable_frame=tk.Frame(self.canvas)
        self.scrollable_frame.pack()

        def _on_frame_configure(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.scrollable_frame.bind("<Configure>", _on_frame_configure)



        self.canvas_window = self.canvas.create_window(
            (0, 0),
        window=self.scrollable_frame,
        anchor="nw"
        )

        row_size=WINDOW_WIDTH//NOTELIST_ELEMENT_WIDTH
        total_x_padding=WINDOW_WIDTH-(NOTELIST_ELEMENT_WIDTH*row_size)
        padx=total_x_padding//(row_size+1)

        column_size=WINDOW_HEIGHT//NOTELIST_ELEMENT_HEIGHT
        total_y_padding=WINDOW_HEIGHT-(NOTELIST_ELEMENT_HEIGHT*column_size)
        pady=total_y_padding//(column_size+1)

        self.row_size=row_size
        self.column_size=column_size


        self.notes=[]


        #we need a more beautiful but complex logic to handle this stuff
        #new idea const y padding
        pady=7

        total_columns=math.ceil(len(data)/row_size)
        self.row_frames=[]
        for i in range(total_columns):
            row_frame=tk.Frame(self.scrollable_frame)
            
            for j in range(row_size):
                index=(i*row_size)+j
                if index>=len(data):
                    break
                self.notes.append(NoteListElement(row_frame, data[index], self.load_note_callback, self.delete_button_callback))
                self.notes[index].pack(side="left", padx=padx//2, pady=pady//2)
            
            row_frame.pack(fill="x", side="top", padx=padx//2, pady=pady//2)
            self.row_frames.append(row_frame)

        '''
            for i in range(len(data)):
            self.notes.append(NoteListElement(self, data[i], self.load_note_callback, self.delete_button_callback))
            self.notes[i].pack(side="left", padx=padx, pady=pady)
        '''

    def add_note_button_pressed(self):
        self.add_button_callback()


class NoteListElement(tk.Frame):
    def __init__(self, parent, data, callback, delete_button_callback):
        super().__init__(parent)

        self.id=data[0]
        self.title=data[1]

        if len(self.title)>30:
            self.title[:30]

        self.body=(data[2])
        
        wrapped_body=self.body.split("\n")
        if len(wrapped_body)>12:
            self.body='\n'.join(wrapped_body[:12])


        #or just
        self.data=data

        self.callback=callback
        self.delete_button_callback=delete_button_callback
        
 
        #can add animations here as well


        self.config(width=NOTELIST_ELEMENT_WIDTH, height=NOTELIST_ELEMENT_WIDTH)
        self.pack_propagate(False)

        self.bgframe=tk.Frame(self, bg="#ffffff")
        self.bgframe.pack(fill="both", expand=True)

        self.frame_top=tk.Frame(self.bgframe, bg="#ffffff")
        self.frame_top.pack(side="top", fill="x", anchor ="nw",  expand=True)
    
        self.note_title=tk.Label(self.frame_top, text=self.title, bg="#ffffff", font=("Arial", 14, "bold"), wraplength=NOTELIST_ELEMENT_WIDTH)
        self.note_title.pack(side="left", anchor="nw", expand=True)

        self.delete_button=tk.Button(self.frame_top, bd=0, text="x", bg="#ffffff", command=self.on_click_delete)
        self.delete_button.pack(side="left", anchor="ne")

        
        self.body_frame = tk.Frame(self.bgframe, bg="#ffffff")
        self.body_frame.pack(side="top", fill="both", expand=True)
        self.note_body=tk.Label(self.body_frame, text=self.body, padx=10, bg="#ffffff", font=("Arial", 12), justify="left", wraplength=NOTELIST_ELEMENT_WIDTH)
        self.note_body.pack(side="left", anchor="nw")


        self.bind("<Button-1>", self.on_click)
 
        self.bgframe.bind("<Button-1>", self.on_click)
        self.frame_top.bind("<Button-1>", self.on_click)
        self.note_title.bind("<Button-1>", self.on_click)

        self.body_frame.bind("<Button-1>", self.on_click)
        self.note_body.bind("<Button-1>", self.on_click)


    def on_click(self, _):
        #this
        #self.callback(self.id)
        #or this
        self.callback(self.data)

    def on_click_delete(self):
        self.delete_button_callback(self.id)



class Note(tk.Frame):
    def __init__(self, parent, callback, data):
        super().__init__(parent)

        self.top_frame=tk.Frame(self)
        self.top_frame.pack(fill="x", padx=0, pady=0)
        
        self.return_button=tk.Button(self.top_frame, text="<", pady=0, padx=0, bd=0, bg="#ffffff",  command=self.return_button_pressed)
        self.return_button.pack(side="left")

        self.callback=callback


        self.title_text_box=tk.Text(self.top_frame, height=1, font=("Arial", 15, "bold"), pady=0, padx=0)
        self.title_text_box.pack(fill="x")

        #complicated line
        #if i press enter dont put a newline char and move to the body
        #would look better if i just made a new function
        self.title_text_box.bind("<Return>", lambda _: (self.body_text_box.focus(), "break")[1])

        self.body_text_box=tk.Text(self)
        self.body_text_box.pack(expand=True, fill="both")

        self.id=data[0]
        if data[1]: self.title_text_box.insert("0.0", data[1])
        if data[2]: self.body_text_box.insert("0.0", data[2])
    


    def return_button_pressed(self):
        title=self.title_text_box.get("1.0", "end-1c")

        body=self.body_text_box.get("1.0", "end-1c")

        if title or body:           
            pass

        self.callback((self.id, title, body))

