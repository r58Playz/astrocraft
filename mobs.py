# Python packages
# Nothing for now...

# Third-party packages
# Nothing for now...

# Modules from this project
import characters
import model


class Herobrine(characters.Mob):
    def __init__(self):
        self.model = model.PlayerModel((0, 0, 0))
        super(Herobrine, self).__init__("herobrine.png")
