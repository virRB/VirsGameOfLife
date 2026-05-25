from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Input
from textual.containers import Container
from tkinter import messagebox
from random import randint

class VirsGameOfLife(App):

    def warn(self, text):
        messagebox.showinfo("alert", text)

    def create_grid(self):
        self.celldata = {}
        self.cells = []

        no_of_cells = 10

        for cell in range(no_of_cells):
            rand = randint(1, 3)

            if rand == 1:
                stuff = ["[orange]■[/]", "landlord", 20]
            elif rand == 2:
                stuff = ["[white]■[/]", "robber", 10]
            else:
                stuff = ["[cyan]■[/]", "guard", 15]

            widget = Static(stuff[0])
            self.mount(widget)

            self.cells.append(widget)
            self.celldata[widget] = [stuff[1], stuff[2], True]


    def compose(self) -> ComposeResult:
        yield Header()

        self.create_grid()

        yield Input(placeholder="Type /reset", id="reset")

        yield Footer()

        self.my_timer = self.set_interval(0.3, self.tick)

    def reset_game(self):
        self.my_timer.stop()
        for cell in self.cells:
            cell.remove()
        self.create_grid()
        self.my_timer = self.set_interval(0.3, self.tick)

    def on_input_submitted(self, event: Input.Submitted):
        if event.input.id == "reset" and event.value == "/reset":
            event.input.clear()
            self.reset_game()

    def getCellType(self, cell):
        return self.celldata[cell][0]
    
    def getCellData(self, cell, int):
        return self.celldata[cell][int]
    
    def decreaseNetWorth(self, cell, int):
        self.celldata[cell][1] -= int

    def increaseNetWorth(self, cell, int):
        self.celldata[cell][1] += int

    def turninto(self, cell, thing):
        self.celldata[cell][0] = thing
        if thing == "landlord":
            cell.update("[orange]■[/]")
        elif thing == "robber":
            cell.update("[white]■[/]")
        elif thing == "guard":
            cell.update("[cyan]■[/]")
        elif thing == "dead":
            cell.update("💀")
        elif thing == "peace":
            cell.update("[lightpink]■[/]")

    def tick(self):
        for celly in self.cells:
            cellnum = self.cells.index(celly)
            behind = cellnum - 1
            forward = cellnum + 1
            if  behind <= -1:
                behind = 0
            elif behind >= 10:
                behind = 9
            if forward <= -1:
                forward = 0
            elif forward >= 10:
                forward = 9
            behind = self.cells[behind]
            forward = self.cells[forward]
            cell = self.cells[cellnum]
            if self.getCellType(cell) == "landlord" and (self.getCellType(behind) == "robber" or self.getCellType(forward) == "robber"):
                self.decreaseNetWorth(cell, 1)
                if not self.celldata[cell][2]:
                    self.celldata[cell][2] = True
                    cell.update("[red]■[/]")
                else:
                    self.celldata[cell][2] = False
                    cell.update("[orange]■[/]")
            elif self.getCellType(cell) == "robber" and (self.getCellType(behind) == "robber" or self.getCellType(forward) == "robber"):
                self.increaseNetWorth(cell, 1)
                if not self.getCellData(cell, 2):
                    self.celldata[cell][2] = True
                    cell.update("[purple]■[/]")
                else:
                    self.celldata[cell][2] = False
                    cell.update("[white]■[/]")
            elif self.getCellType(cell) == "guard" and (self.getCellType(behind) == "landlord" or self.getCellType(forward) == "landlord"):
                self.increaseNetWorth(cell, 2)
                if not self.getCellData(cell, 2):
                    self.celldata[cell][2] = True
                    cell.update("[blue]■[/]")
                else:
                    self.celldata[cell][2] = False
                    cell.update("[cyan]■[/]")
            elif self.getCellType(cell) == "dead":
                rand = randint(1, 10)
                if rand <= 8:
                    pass
                elif rand == 9:
                    self.turninto(cell, "robber")
                    self.celldata[cell][1] = 7
                elif rand == 10:
                    self.turninto(cell, "guard")
                    self.celldata[cell][1] = 16
                if self.getCellData(forward, 2):
                    self.celldata[forward][2] = False
                    forward.update("⭐")
                    self.turninto(forward, "scared")
                else:
                    self.celldata[forward][2] = True
                    forward.update("[grey]■[/]")
            elif self.getCellType(cell) == "scared":
                random = randint(1, 2)
                if random == 1:
                    forward.update("[grey]■[/]")
                    self.turninto(forward, "scared")
                elif random == 2:
                    self.turninto(cell, "peace")
                    self.turninto(forward, "peace")
                    self.turninto(behind, "peace")


            if self.getCellData(cell, 1) <= 0:
                self.turninto(cell, "dead")
            elif self.getCellData(cell, 1) >= 20:
                self.turninto(cell, "landlord")




VirsGameOfLife().run()