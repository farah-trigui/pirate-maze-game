import tkinter as tk
from PIL import Image, ImageTk
import random
import json
import os

rows, cols = 10, 10
cell_size = 60
num_gifts = 5
time = 40

pirate_image_path = "images/pirate5.png"
red_square_image_path = "images/shark2.png"
gift_image_path = "images/treasure2.png"
fog_image_path = "images/fog.jpg"
wall_image_path = "images/ship2.png"


file = "results.json"

def loadData():
    with open(file, "r") as f:
        return json.load(f)

def saveData(data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

def recordRes(username, result, time):
    data = loadData()
    data.append({
        "Username": username,
        "Result": result,
        "Duration": time
    })
    saveData(data)



maze_layouts = [
    [
        [2, 0, 0, 1, 1, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
        [4, 0, 0, 1, 1, 1, 0, 1, 1, 1],
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 3, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 4, 0, 0, 0, 0, 0],   
        [0, 0, 1, 0, 1, 1, 0, 1, 1, 0],
        [0, 4, 1, 0, 3, 1, 4, 0, 0, 0], 
        [3, 0, 1, 1, 1, 1, 0, 0, 0, 3]
    ],
    [
        [3, 0, 0, 1, 1, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
        [4, 0, 0, 1, 1, 1, 3, 1, 1, 1],
        [0, 0, 1, 0, 2, 0, 0, 0, 0, 3],
        [1, 1, 1, 3, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 4, 0, 0, 0, 0, 0],   
        [0, 0, 1, 0, 1, 1, 0, 1, 1, 0],
        [0, 4, 1, 0, 3, 1, 4, 0, 0, 0], 
        [1, 0, 1, 1, 1, 1, 0, 0, 0, 1]
    ],
    [
        [1, 0, 0, 1, 1, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
        [4, 0, 0, 1, 1, 1, 0, 1, 1, 1],
        [0, 3, 1, 0, 1, 0, 0, 0, 0, 3],
        [1, 1, 1, 3, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [2, 0, 1, 0, 4, 0, 0, 0, 0, 0],   
        [0, 0, 1, 0, 1, 1, 0, 1, 1, 0],
        [0, 4, 1, 0, 3, 1, 4, 0, 0, 0], 
        [1, 0, 1, 1, 1, 1, 0, 0, 3, 1]
    ]
]

class MazeGame:
    def __init__(self, root):
        self.root = root
        self.gift_ids = {}
        self.fog_ids = {}
        self.root.title("Pirate Maze Game")

        self.pirate_image = ImageTk.PhotoImage(Image.open(pirate_image_path).resize((cell_size, cell_size)))
        self.red_square_image = ImageTk.PhotoImage(Image.open(red_square_image_path).resize((cell_size, cell_size)))
        self.gift_image = ImageTk.PhotoImage(Image.open(gift_image_path).resize((cell_size, cell_size)))
        self.fog_image = ImageTk.PhotoImage(Image.open(fog_image_path).resize((cell_size, cell_size)))
        self.wall_image = ImageTk.PhotoImage(Image.open(wall_image_path).resize((cell_size, cell_size)))

        self.endGame = False
        self.maze_layout = random.choice(maze_layouts)
        self.remainingTime = time
        self.username = None
        self.welcomeScreen()



    def welcomeScreen(self):
        self.entry_frame = tk.Frame(self.root)
        self.entry_frame.pack(pady=20)
        tk.Label(self.entry_frame, text="Enter your name: ").pack(side="left")
        self.name_entry = tk.Entry(self.entry_frame)
        self.name_entry.pack(side="left", padx=5)
        self.start_button = tk.Button(self.entry_frame, text="Start Game", command=self.startGame)
        self.start_button.pack(side="left", padx=5)

    def startGame(self):
        self.user_name = self.name_entry.get()
        if self.user_name:
            self.entry_frame.destroy()
            self.createMazeGUI()
            self.startTimer() 


    def createMazeGUI(self):
        self.canvas = tk.Canvas(self.root, width=cols * cell_size, height=rows * cell_size)
        self.canvas.pack()

        self.timer_label = tk.Label(self.root, text=f"Time Remaining: {self.remainingTime} seconds", font=("Helvetica", 16))
        self.timer_label.pack(pady=10)

        self.piratePos = None
        self.gifts = []
        self.startPos = None
        self.red_squares = []
        self.createMaze()
        self.createFog()

        self.root.bind("<Up>", lambda e: self.movepirate(0, -1))
        self.root.bind("<Down>", lambda e: self.movepirate(0, 1))
        self.root.bind("<Left>", lambda e: self.movepirate(-1, 0))
        self.root.bind("<Right>", lambda e: self.movepirate(1, 0))

        self.collected_gifts = 0
        self.moveRedSquares()
        self.updatefog()

    def startTimer(self):
        if not self.endGame: 
            if self.remainingTime > 0:
                self.timer_label.config(text=f"Time Remaining: {self.remainingTime} seconds")
                self.remainingTime -= 1
                self.root.after(1000, self.startTimer)  
            else:
                self.gameOver("You lost!")
                self.restart_button = tk.Button(self.root, text="Restart", command=self.restartGame)
                self.restart_button.pack(pady=10)
                self.exit_button = tk.Button(self.root, text="Exit", command=self.root.destroy)
                self.exit_button.pack(pady=10)

    def createMaze(self):
        for row in range(rows):
            for col in range(cols):
                cell = self.maze_layout[row][col]
                if cell == 1:
                    self.canvas.create_image(
                        col * cell_size + cell_size // 2, row * cell_size + cell_size // 2,
                        image=self.wall_image
                    )
                elif cell == 2:
                    self.piratePos = (col, row)
                    self.startPos = (col, row)
                    self.pirate = self.canvas.create_image(
                        col * cell_size + cell_size // 2, row * cell_size + cell_size // 2,
                        image=self.pirate_image
                    )
                elif cell == 3:
                    gift_id = self.canvas.create_image(
                        col * cell_size + cell_size // 2, row * cell_size + cell_size // 2,
                        image=self.gift_image
                    )
                    self.gifts.append((col, row))
                    self.gift_ids[(col, row)] = gift_id
                elif cell == 4:
                    red_square = self.canvas.create_image(
                        col * cell_size + cell_size // 2, row * cell_size + cell_size // 2,
                        image=self.red_square_image
                    )
                    self.red_squares.append({
                        "coords": (col, row),
                        "id": red_square,
                        "direction": random.choice(["horizontal", "vertical"]),
                        "step": 1
                    })
              
  

    def createFog(self):
        for row in range(rows):
            for col in range(cols):
                fog_id = self.canvas.create_image(
                    col * cell_size + cell_size // 2, row * cell_size + cell_size // 2,
                    image=self.fog_image
                )
                self.fog_ids[(col, row)] = fog_id

    def updatefog(self):
        visible = 1  

        for (col, row), fog_id in list(self.fog_ids.items()):
            if abs(self.piratePos[0] - col) <= visible and abs(self.piratePos[1] - row) <= visible:
                self.canvas.delete(fog_id)
                del self.fog_ids[(col, row)]  

    def movepirate(self, dx, dy):
        new_x = self.piratePos[0] + dx
        new_y = self.piratePos[1] + dy
        if 0 <= new_x < cols and 0 <= new_y < rows:
            if self.maze_layout[new_y][new_x] != 1:
                self.piratePos = (new_x, new_y)
                self.canvas.coords(
                    self.pirate,
                    new_x * cell_size + cell_size // 2, new_y * cell_size + cell_size // 2
                )
                self.checkCells()
                self.checkCollision()
                self.updatefog()

    def checkCells(self):
        if self.piratePos in self.gifts:
            self.gifts.remove(self.piratePos)
            self.collected_gifts += 1
            self.canvas.delete(self.gift_ids[self.piratePos])
            del self.gift_ids[self.piratePos]
            if self.collected_gifts == num_gifts:
                self.gameOver("You Win!")
                self.restart_button = tk.Button(self.root, text="Restart", command=self.restartGame)
                self.restart_button.pack(pady=10)
                
                self.exit_button = tk.Button(self.root, text="Exit", command=self.root.destroy)
                self.exit_button.pack(pady=10)

    def restartGame(self):
        self.endGame = False
        self.remainingTime = time

        self.canvas.destroy()
        self.timer_label.destroy()
        self.restart_button.destroy()
        self.exit_button.destroy()

        self.createMazeGUI()
        self.startTimer()

    def checkCollision(self):
        for red_square in self.red_squares:
            if self.piratePos == red_square["coords"]:
                self.piratePos = self.startPos
                self.canvas.coords(
                    self.pirate,
                    self.startPos[0] * cell_size + cell_size // 2, self.starPos[1] * cell_size + cell_size // 2
                )

    def moveRedSquares(self):
        for square in self.red_squares:
            col, row = square["coords"]
            direction = square["direction"]
            step = square["step"]

            if direction == "horizontal":
                new_col = col + step
                if 0 <= new_col < cols and self.maze_layout[row][new_col] != 1:
                    square["coords"] = (new_col, row)
                    self.canvas.coords(
                        square["id"],
                        new_col * cell_size + cell_size // 2, row * cell_size + cell_size // 2
                    )
                else:
                    square["step"] *= -1  
            elif direction == "vertical":
                new_row = row + step
                if 0 <= new_row < rows and self.maze_layout[new_row][col] != 1:
                    square["coords"] = (col, new_row)
                    self.canvas.coords(
                        square["id"],
                        col * cell_size + cell_size // 2, new_row * cell_size + cell_size // 2
                    )
                else:
                    square["step"] *= -1  

            if square["coords"] == self.piratePos:
                self.piratePos = self.startPos
                self.canvas.coords(
                    self.pirate,
                    self.startPos[0] * cell_size + cell_size // 2, self.startPos[1] * cell_size + cell_size // 2
                )

        self.root.after(500, self.moveRedSquares)  
    
    def gameOver(self, message):
        self.endGame = True
        timeSpent = time - self.remainingTime
        result = "win" if message == "You Win!" else "loss"
        
        recordRes(self.user_name, result, timeSpent)
        
        self.canvas.create_rectangle(
            (cols * cell_size // 2) - 100, (rows * cell_size // 2) - 30,
            (cols * cell_size // 2) + 100, (rows * cell_size // 2) + 30,
            fill="black", outline="", stipple="gray50"
        )
        self.canvas.create_text(
            cols * cell_size // 2, rows * cell_size // 2,
            text=message,
            fill="white",
            font=("Helvetica", 24, "bold"),
            justify="center"
        )
        self.root.unbind("<Up>")
        self.root.unbind("<Down>")
        self.root.unbind("<Left>")
        self.root.unbind("<Right>")
        self.showRestartExitButtons()
    
    def showRestartExitButtons(self):
        self.restart_button = tk.Button(self.root, text="Restart", command=self.restartGame)
        self.restart_button.pack(pady=10)

        self.exit_button = tk.Button(self.root, text="Exit", command=self.root.destroy)
        self.exit_button.pack(pady=10)


root = tk.Tk()
game = MazeGame(root)
root.mainloop()
