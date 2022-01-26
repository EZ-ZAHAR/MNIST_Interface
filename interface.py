import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import brainCNN
import PIL
from PIL import ImageGrab

class FirstPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        load = Image.open("img1.jpg")
        photo = ImageTk.PhotoImage(load)
        label = tk.Label(self, image=photo)
        label.image = photo
        label.place(x=0, y=0)

        border = tk.LabelFrame(self, text='Login', bg='ivory', bd=10, font=("Arial", 20))
        border.pack(fill="both", expand="yes", padx=150, pady=150) #forme frontiere de frame interieur

        L1 = tk.Label(border, text="Username", font=("Arial Bold", 15), bg='ivory')  #bg : pour supprimer background de username
        L1.place(x=50, y=20)
        T1 = tk.Entry(border, width=30, bd=5)
        T1.place(x=180, y=20)

        L2 = tk.Label(border, text="Password", font=("Arial Bold", 15), bg='ivory')
        L2.place(x=50, y=80)
        T2 = tk.Entry(border, width=30, show='*', bd=5)
        T2.place(x=180, y=80)

        def verify():
            try:
                with open("credential.txt", "r") as f:
                    info = f.readlines()
                    i = 0
                    for e in info:
                        u, p = e.split(",")
                        if u.strip() == T1.get() and p.strip() == T2.get():
                            controller.show_frame(SecondPage)
                            i = 1
                            break
                    if i == 0:
                        messagebox.showinfo("Error", "Please provide correct username and password!!")
            except:
                messagebox.showinfo("Error", "Please provide correct username and password!!")

        B1 = tk.Button(border, text="Submit", font=("Arial", 15), command=verify)
        B1.place(x=320, y=115)

        def register():
            window = tk.Tk()
            window.resizable(0, 0) #désactiver grandir de l'interface
            window.configure(bg="#7DBCDE") #faire background blue
            window.title("Register")
            l1 = tk.Label(window, text="Username:", font=("Arial", 15), bg="#7DBCDE")
            l1.place(x=10, y=10)
            t1 = tk.Entry(window, width=30, bd=5)
            t1.place(x=200, y=10)

            l2 = tk.Label(window, text="Password:", font=("Arial", 15), bg="#7DBCDE")
            l2.place(x=10, y=60)
            t2 = tk.Entry(window, width=30, show="*", bd=5)
            t2.place(x=200, y=60)

            l3 = tk.Label(window, text="Confirm Password:", font=("Arial", 15), bg="#7DBCDE")
            l3.place(x=10, y=110)
            t3 = tk.Entry(window, width=30, show="*", bd=5)
            t3.place(x=200, y=110)

            def check():
                if t1.get() != "" or t2.get() != "" or t3.get() != "":
                    if t2.get() == t3.get():
                        with open("credential.txt", "a") as f:
                            f.write(t1.get() + "," + t2.get() + "\n")
                            messagebox.showinfo("Welcome", "You are registered successfully!!")
                    else:
                        messagebox.showinfo("Error", "Your password didn't get match!!")
                else:
                    messagebox.showinfo("Error", "Please fill the complete field!!")

            b1 = tk.Button(window, text="Sign in", font=("Arial", 15), bg="#D8FFFF", command=check)
            b1.place(x=200, y=160)

            window.geometry("470x220")
            window.mainloop()

        B2 = tk.Button(self, text="Register", bg="dark orange", font=("Arial", 15), command=register)
        B2.place(x=650, y=20)


class SecondPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        load = Image.open("img2.jpg")
        photo = ImageTk.PhotoImage(load)
        label = tk.Label(self, image=photo)
        label.image = photo
        label.place(x=0, y=0)

        self.res = ""
        self.pre = [None, None]
        self.bs = 8.5
        self.c =  tk.Canvas(self, bd=3, relief="ridge", width=300, height=282, bg='white')
        self.c.pack(side=tk.LEFT)
        f1 = tk.Frame(self)
        tk.Label(f1, text="CNN Predicting Hand-Written Digits", fg="Red", font=("", 15, "bold")).pack(pady=10)
        #tk.Label(f1, text="Trained using MNSIT Dataset", fg="green", font=("", 15)).pack()
        #tk.Label(f1, text="back: to return to the previous page", fg="green", font=("", 15)).pack()
        tk.Label(f1, text="Draw On The Canvas Alongside", fg="green", font=("", 15)).pack()
        self.pr = tk.Label(f1, text="Prediction: None", fg="blue", font=("", 20, "bold"))
        self.pr.pack(pady=20)

        tk.Button(f1, font=("", 15), fg="white", bg="red", text="Clear Canvas", command=self.clear).pack(side=tk.BOTTOM)

        f1.pack(side=tk.RIGHT)
        self.c.bind("<Button-1>", self.putPoint)
        self.c.bind("<ButtonRelease-1>", self.getResult)
        self.c.bind("<B1-Motion>", self.paint)
       # Button = tk.Button(self, text="Next", font=("Arial", 15), bg="#ffc22a",
        #                   command=lambda: controller.show_frame(ThirdPage))
      #  Button.place(x=700, y=450)

        Button = tk.Button(self, text="Back", font=("Arial", 15), bg="#F34F4E",
                           command=lambda: controller.show_frame(FirstPage))
        Button.place(x=90, y=450)
    def getResult(self, e):
        x = self.winfo_rootx() + self.c.winfo_x()
        y = self.winfo_rooty() + self.c.winfo_y()
        x1 = x + self.c.winfo_width()
        y1 = y + self.c.winfo_height()
        img = PIL.ImageGrab.grab()
        img = img.crop((x, y, x1, y1))
        img.save("dist.png")
        self.res = str(brainCNN.predict("dist.png"))
        self.pr['text'] = "Prediction: " + self.res

    def clear(self):
        self.c.delete('all')

    def putPoint(self, e):
        self.c.create_oval(e.x - self.bs, e.y - self.bs, e.x + self.bs, e.y + self.bs, outline='black', fill='black')
        self.pre = [e.x, e.y]

    def paint(self, e):
        self.c.create_line(self.pre[0], self.pre[1], e.x, e.y, width=self.bs * 2, fill='black', capstyle=tk.ROUND,smooth=tk.TRUE)

        self.pre = [e.x, e.y]










#class ThirdPage(tk.Frame):
 #  def __init__(self, parent, controller):
  #      tk.Frame.__init__(self, parent)

   #     self.configure(bg='Tomato')

    #    Label = tk.Label(self,
     #                    text="Store some content related to your \n project or what your application made for. \n All the best!!",
      #                   bg="orange", font=("Arial Bold", 25))
      #  Label.place(x=40, y=150)

      #  Button = tk.Button(self, text="Home", font=("Arial", 15),bg="#ffc22a", command=lambda: controller.show_frame(FirstPage))
      #  Button.place(x=650, y=450)

      #  Button = tk.Button(self, text="Back", font=("Arial", 15),bg="#ffc22a", command=lambda: controller.show_frame(SecondPage))
       # Button.place(x=100, y=450)


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # creating a window
        window = tk.Frame(self)
        window.pack()

        window.grid_rowconfigure(0, minsize=500)
        window.grid_columnconfigure(0, minsize=800)

        self.frames = {}
        for F in (FirstPage, SecondPage):
            frame = F(window, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(FirstPage)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()
        self.title("Application MNIST")


app = Application()
app.maxsize(800, 500) #taille de interface doit pas dépacer 800x500
app.mainloop()