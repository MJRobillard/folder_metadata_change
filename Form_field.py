import os
import tkinter as tk
from PyPDF2 import PdfReader, PdfWriter
import customtkinter as ctk

ctk.set_appearance_mode("System")

ctk.set_default_color_theme("dark-blue")

appWidth, appHeight = 600, 700

class App(ctk.CTk):
    count = 0
    memory = {}
    
    def make_field(self, title, place_holder, column = 0): #function to make a new field, useful if later you want new default metadata options
        self.title_field = ctk.CTkLabel(self, text=title)
        self.title_field.grid(row=App.count, column=0, padx=20, pady=20, sticky='ew')

        self.title_entry = ctk.CTkEntry(self, placeholder_text=place_holder)
        self.title_entry.grid(row=App.count, column=1, padx=20, pady=20, sticky='ew')
        App.memory[title]=self.title_entry
        App.count = App.count + 1
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.title("GUI for remediation")
        self.geometry(f"{appWidth}x{appHeight}")
        # Info for presenting the title form field
        self.generateResultsButton = ctk.CTkButton(self, text="Generate Results", command=self.setMetadata)# gen results button leads to the create Text
        self.generateResultsButton.grid(row=0, column=4, columnspan=2, padx=20, pady=20, sticky="ew")
        
        self.display_box = ctk.CTkTextbox(self, width=200, height=100)# makes the display box so you know it worked
        self.display_box.grid(row=1, column=4, columnspan=4, padx=20, pady=20, sticky="nsew")
        
        
    def setMetadata(self):
        text = [key +': ' +App.memory[key].get() for key in App.memory]
        [self.change_folder_metadata("Convert_Folder",key,App.memory[key].get()) for key in App.memory]
        self.display_box.insert("0.0", text)
    
    def change_folder_metadata(self,folder_location,tag , data ): # gets each pdf in the folder and puts it through change_meta 
        for file in os.listdir(folder_location):
            if file.lower().endswith('.pdf'):
                App.change_meta(os.path.join(folder_location, file),tag, data)
    
    def change_meta(source, tag, data ): # changes the metadata at the given source
        '''Changes the metadata given a source'''
        with open(source, 'rb') as filein:
            reader = PdfReader(filein)
            writer = PdfWriter()
            writer.append_pages_from_reader(reader)
            metadata = reader.metadata
            writer.add_metadata(metadata)

            new_metadata = {}
            if data != '':
                new_metadata['/'+tag] = data
            else:
                new_metadata['/'+tag] = metadata['/'+tag]
            writer.add_metadata(new_metadata)
            with open(source, 'wb') as fileout:
                writer.write(fileout)
                
    def new_custom_field(self):
        tag = ctk.CTkInputDialog(text="tag type (careful)", title="Test").get_input()
        default_text = ctk.CTkInputDialog(text="example of entry", title="Test").get_input()
        App.make_field(self,tag,default_text)

if __name__ == "__main__":
    app = App()
    app.make_field("Title", "Lord of the Rings")
    app.make_field("Author", "J.R.R Tolkein")
    app.make_field("Keywords", "Magic, Fantasy, Elves")
    app.make_field("Subject","Fantasy") #adds a new field like so, the tag in first, then the default text
    other_button = ctk.CTkButton(app, text="Other Metadata (Careful)", command= app.new_custom_field)
    other_button.grid(row=10, column=1, padx=20, pady=20, sticky='ew')
    # Used to run the application
    app.mainloop()