from world import World
import tkinter as tk

def main():
    root=tk.Tk()
    world=World(root,25,25)
    world.root.mainloop()
   # world.StartGame()

main()