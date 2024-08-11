from tkinter import *
from tkinter.ttk import Scale
from tkinter import colorchooser, filedialog, messagebox
import PIL.ImageGrab as ImageGrab

# Defining Class and constructor of the Program
class Draw():
    def __init__(self, root):
        # Defining title and Size of the Tkinter Window GUI
        self.root = root
        self.root.title("DraWiz")
        self.root.geometry("900x600")
        self.root.configure(background="white")
        
        # Variables for pointer and Eraser   
        self.pointer = "black"
        self.erase = "white"

        # Create the UI components
        self.create_widgets()
        
        # Bind the background Canvas with mouse click
        self.background.bind("<B1-Motion>", self.paint)

        # Store history of actions for undo functionality
        self.history = []

    def create_widgets(self):
        # Configure the alignment, font size, and color of the title text
        text = Text(self.root)
        text.tag_configure("tag_name", justify='center', font=('arial', 25), background='#292826', foreground='orange')
        text.insert("1.0", "DraWiz - Drawing Application")
        text.tag_add("tag_name", "1.0", "end")
        text.pack()

        # Color Palette for drawing
        self.pick_color = LabelFrame(self.root, text='Colors', font=('arial', 15), bd=5, relief=RIDGE, bg="white")
        self.pick_color.place(x=0, y=60, width=90, height=245)

        colors = ['blue', 'red', 'green', 'orange', 'violet', 'black', 'yellow', 'purple', 'pink', 'white', 'brown', 'indigo']
        i = j = 0
        for color in colors:
            Button(self.pick_color, bg=color, bd=2, relief=RIDGE, width=3,
                   command=lambda col=color: self.select_color(col)).grid(row=i, column=j)
            i += 1
            if i == 6:
                i = 0
                j = 1

        # Erase Button and its properties   
        self.eraser_btn = Button(self.root, text="Eraser", bd=4, bg='white', command=self.eraser, width=9, relief=RIDGE)
        self.eraser_btn.place(x=0, y=307)

        # Undo Button to revert the last action
        self.undo_btn = Button(self.root, text="Undo", bd=4, bg='white', command=self.undo, width=9, relief=RIDGE)
        self.undo_btn.place(x=0, y=337)

        # Reset Button to clear the entire screen 
        self.clear_screen = Button(self.root, text="Clear Screen", bd=4, bg='white',
                                   command=lambda: self.background.delete('all'), width=9, relief=RIDGE)
        self.clear_screen.place(x=0, y=367)

        # Save Button for saving the image in local computer
        self.save_btn = Button(self.root, text="ScreenShot", bd=4, bg='white', command=self.save_drawing, width=9, relief=RIDGE)
        self.save_btn.place(x=0, y=397)

        # Background Button for choosing color of the Canvas
        self.bg_btn = Button(self.root, text="Background", bd=4, bg='white', command=self.canvas_color, width=9, relief=RIDGE)
        self.bg_btn.place(x=0, y=427)

        # Creating a Scale for pointer and eraser size
        self.pointer_frame = LabelFrame(self.root, text='Size', bd=5, bg='white', font=('arial', 15, 'bold'), relief=RIDGE)
        self.pointer_frame.place(x=0, y=460, height=200, width=90)

        self.pointer_size = Scale(self.pointer_frame, orient=VERTICAL, from_=48, to=1, length=168)
        self.pointer_size.set(1)
        self.pointer_size.grid(row=0, column=1, padx=15)

        # Defining a background color for the Canvas 
        self.background = Canvas(self.root, bg='white', bd=5, relief=GROOVE, height=530, width=780)
        self.background.place(x=100, y=60)

    # Paint Function for Drawing the lines on Canvas
    def paint(self, event):
        x1, y1 = (event.x - 2), (event.y - 2)
        x2, y2 = (event.x + 2), (event.y + 2)

        # Create an oval (a small circle) at the pointer's position
        shape = self.background.create_oval(x1, y1, x2, y2, fill=self.pointer, outline=self.pointer, width=self.pointer_size.get())
        self.history.append(shape)  # Add the shape to history for undo functionality

    # Function for choosing the color of pointer  
    def select_color(self, col):
        self.pointer = col

    # Function for defining the eraser
    def eraser(self):
        self.pointer = self.erase

    # Function for choosing the background color of the Canvas    
    def canvas_color(self):
        try:
            color = colorchooser.askcolor()
            if color[1]:  # Check if a color was selected
                self.background.configure(background=color[1])
                self.erase = color[1]
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Function for saving the image file in Local Computer
    def save_drawing(self):
        try:
            file_ss = filedialog.asksaveasfilename(defaultextension='.jpg')
            if file_ss:  # Check if a file path was selected
                x = self.root.winfo_rootx() + self.background.winfo_x()
                y = self.root.winfo_rooty() + self.background.winfo_y()
                x1 = x + self.background.winfo_width()
                y1 = y + self.background.winfo_height()

                ImageGrab.grab().crop((x, y, x1, y1)).save(file_ss)
                messagebox.showinfo('Screenshot Saved', 'Screenshot successfully saved as ' + str(file_ss))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Undo the last action
    def undo(self):
        if self.history:
            last_item = self.history.pop()
            self.background.delete(last_item)

if __name__ == "__main__":
    root = Tk()
    p = Draw(root)
    root.mainloop()
