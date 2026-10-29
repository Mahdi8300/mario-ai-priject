class MarioEnv:
    def init(self):
        self.grid = ["M", ".", "E", "_", ".", "F"]
        self.mario_pos = 0
        self.is_alive = True
        self.has_won = False

    def display(self):
        print("\n--- وضعیت فعلی بازی ---")
        print("".join(self.grid))
        print("-----------------------\n")

    def get_allowed_actions(self):
        return ["right", "jump"]

    def step(self, action):
        if not self.is_alive or self.has_won:
            return "بازی تمام شده است."

        self.grid[self.mario_pos] = "."
        next_pos = self.mario_pos + 1

        if self.grid[next_pos] == "E" and action != "jump":
            self.is_alive = False
            self.grid[self.mario_pos] = "M"
            return "ماری به دشمن برخورد کرد! باخت."
        
        if self.grid[next_pos] == "_" and action != "jump":
            self.is_alive = False
            self.grid[self.mario_pos] = "M"
            return "ماری در چاله افتاد! باخت."
        
        if self.grid[next_pos] == "F":
            self.mario_pos = next_pos
            self.grid[self.mario_pos] = "M"
            self.has_won = True
            return "ماری به پرچم رسید! برد."
        
        if action == "jump":
            self.mario_pos = next_pos + 1
            self.grid[self.mario_pos] = "M"
            return "ماری پرش کرد و از مانع عبور کرد."
        
        if action == "right":
            self.mario_pos = next_pos
            self.grid[self.mario_pos] = "M"
            return "ماری به راست حرکت کرد."
        
        return "حرکت نامعتبر است."

if __name__ == "main":
    env = MarioEnv()
    env.display()
    print("حرکت‌های مجاز:", env.get_allowed_actions())
    print("نتیجه:", env.step("right"))
    env.display()
