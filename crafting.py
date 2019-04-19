# Imports, sorted alphabetically.

# Python packages
# Nothing for now...

# Third-party packages
# Nothing for now...

# Modules from this project
from blocks import *
import globals as G
from items import *


__all__ = (
    'Recipe', 'Recipes', 'SmeltingRecipe', 'SmeltingRecipes',
)


class Recipe:
    # ingre is a list that contains the ids of the ingredients
    # e.g. [[2, 2], [1, 1]]
    def __init__(self, ingre, output):
        # what blocks are needed to craft this block/item
        self.ingre = ingre
        self.output = output
        self.shapeless = False

    def __repr__(self):
        return 'Ingredients: ' + str(self.ingre) + '; Output: ' + str(self.output)

class Recipes:
    def __init__(self):
        self.nr_recipes = 0
        self.recipes = []

    def remove_empty_line_col(self, ingre_list):
        # remove empty lines
        if len(ingre_list) == 0:
            return

        for i in (0, -1):
            line = ingre_list[i]
            if len(line) == 0:
                continue
            isempty = True
            for id in line:
                if id: isempty = False
            if isempty:
                ingre_list.pop(i)

        #remove empty column
        for i in (0, -1):
            isempty = True
            for line in ingre_list:
                if len(line) == 0:
                    continue
                if line[i]: isempty = False
            if isempty:
                for line in ingre_list:
                    if len(line) == 0:
                        continue
                    line.pop(i)

    def parse_recipe(self, shape, ingre):
        ingre_list = []

        for line in shape:
            sub_ingre = []

            # line length should not be greater than 3
            if len(line) > 3:
                print('add_recipe(): line length should be <= 3!')
                return

            for c in line:
                if c == ' ':
                    sub_ingre.append(air_block.id)
                else:
                    sub_ingre.append(ingre[c].id)
            ingre_list.append(sub_ingre)

        self.remove_empty_line_col(ingre_list)

        return ingre_list

    def add_recipe(self, shape, ingre, output):
        self.recipes.append(Recipe(self.parse_recipe(shape, ingre), output))
        self.nr_recipes += 1

    def add_shapeless_recipe(self, ingre, output):
        ingre_list = [x.id for x in ingre if x.id]
        ingre_list.sort()
        r = Recipe(ingre_list, output)
        r.shapeless = True
        self.recipes.append(r)

    def craft(self, input_blocks):
        id_list = []
        shapeless_id_list = []
        for line in input_blocks:
            id_list.append([b.id for b in
                            line])    # removed b.id != 0: it may make the
                            # shape different
            shapeless_id_list.extend([b.id for b in line if b.id])
        shapeless_id_list.sort()

        self.remove_empty_line_col(id_list)
        for r in self.recipes:
            if r.shapeless:
                if r.ingre == shapeless_id_list:
                    return r.output
            else:
                if r.ingre == id_list:
                    return r.output

        return None

    def dump(self):
        for recipe in self.recipes:
            print(recipe)

class SmeltingRecipe:
    def __init__(self, ingre, output):
        # what blocks are needed to craft this block/item
        self.ingre = ingre
        self.output = output


class SmeltingRecipes:
    def __init__(self):
        self.nr_recipes = 0
        self.recipes = []

    def add_recipe(self, ingre, output):
        self.recipes.append(SmeltingRecipe(ingre, output))
        self.nr_recipes += 1

    def smelt(self, ingre):
        for r in self.recipes:
            if r.ingre == ingre:
                return r.output

        return None


G.recipes = Recipes()
G.smelting_recipes = SmeltingRecipes()
# stone items
G.recipes.add_recipe(["##", "##"], {'#': stone_block},
                   ItemStack(stonebrick_block.id, amount=4))
G.recipes.add_recipe(["###", "# #", "###"], {'#': cobble_block},
                   ItemStack(furnace_block.id, amount=1))
G.recipes.add_recipe(["##", "##"], {'#': quartz_block},
                   ItemStack(quartzbrick_block.id, amount=4))
G.recipes.add_recipe(["#", "#"], {'#': quartz_block},
                   ItemStack(quartzcolumn_block.id, amount=2))
G.recipes.add_recipe(["#", "#", "#"], {'#': quartz_block},
                   ItemStack(quartzcolumn_block.id, amount=3))
G.recipes.add_recipe(["   ", "   ", "###"], {'#': quartz_block},
                   ItemStack(quartzchiseled_block.id, amount=3))

#9 ores to blocks

G.recipes.add_recipe(["###", "###", "###"], {'#': iron_ingot_item},
                   ItemStack(iron_block.id, amount=1))
G.recipes.add_recipe(["###", "###", "###"], {'#': gold_ingot_item},
                   ItemStack(gold_block.id, amount=1))
G.recipes.add_recipe(["###", "###", "###"], {'#': diamond_item},
                   ItemStack(diamond_block.id, amount=1))
#  block back to 9 ores
G.recipes.add_shapeless_recipe((diamond_block,),
                    ItemStack(diamond_item.id, amount=9))
G.recipes.add_shapeless_recipe((iron_block,),
                    ItemStack(iron_ingot_item.id, amount=9))
G.recipes.add_shapeless_recipe((gold_block,),
                    ItemStack(gold_ingot_item.id, amount=9))
# wood items

G.recipes.add_shapeless_recipe((birchwood_block,),
                    ItemStack(birchwoodplank_block.id, amount=4))
G.recipes.add_shapeless_recipe((junglewood_block,),
                    ItemStack(junglewoodplank_block.id, amount=4))
G.recipes.add_shapeless_recipe((oakwood_block,),
                    ItemStack(oakwoodplank_block.id, amount=4))
G.recipes.add_recipe(["#", "#"], {'#': oakwoodplank_block},
                   ItemStack(stick_item.id, amount=4))
G.recipes.add_recipe(["#", "#"], {'#': junglewoodplank_block},
                   ItemStack(stick_item.id, amount=4))
G.recipes.add_recipe(["#", "#"], {'#': oakwoodplank_block},
                   ItemStack(stick_item.id, amount=4))
G.recipes.add_recipe(["#", "#"], {'#': oakwoodplank_block},
                   ItemStack(stick_item.id, amount=4))
G.recipes.add_recipe(["###", "# #", "###"], {'#': birchwoodplank_block},
                   ItemStack(chest_block.id, amount=1))
G.recipes.add_recipe(["###", "# #", "###"], {'#': oakwoodplank_block},
                   ItemStack(chest_block.id, amount=1))
G.recipes.add_recipe(["###", "# #", "###"], {'#': junglewoodplank_block},
                   ItemStack(chest_block.id, amount=1))

G.recipes.add_recipe(["##", "##"], {'#': birchwoodplank_block},
                   ItemStack(craft_block.id, amount=1))
G.recipes.add_recipe(["##", "##"], {'#': oakwoodplank_block},
                   ItemStack(craft_block.id, amount=1))
G.recipes.add_recipe(["##", "##"], {'#': junglewoodplank_block},
                   ItemStack(craft_block.id, amount=1))
G.recipes.add_recipe(["# #", "###", "# #"], {'#': stick_item},
                           ItemStack(ladder_item.id, amount=4))

for material, toolset in [(diamond_item, [diamond_pickaxe, diamond_axe, diamond_shovel, diamond_hoe]),
                            (cobble_block, [stone_pickaxe, stone_axe, stone_shovel, stone_hoe]),
                            (iron_ingot_item, [iron_pickaxe, iron_axe, iron_shovel, iron_hoe]),
                            (gold_ingot_item, [golden_pickaxe, golden_axe, golden_shovel, golden_hoe])]:

    G.recipes.add_recipe(["###", " @ ", " @ "], {'#': material, '@': stick_item},
                   ItemStack(toolset[0].id, amount=1))
    G.recipes.add_recipe(["## ", "#@ ", " @ "], {'#': material, '@': stick_item},
                   ItemStack(toolset[1].id, amount=1))
    G.recipes.add_recipe([" # ", " @ ", " @ "], {'#': material, '@': stick_item},
                    ItemStack(toolset[2].id, amount=1))
    G.recipes.add_recipe(["## ", " @ ", " @ "], {'#': material, '@': stick_item},
                   ItemStack(toolset[-1].id, amount=1))

# armors
for material, armors in [(iron_ingot_item, [iron_helmet, iron_chestplate, iron_leggings, iron_boots])]:

    G.recipes.add_recipe(["###", "# #"], {'#': material},
                   ItemStack(armors[0].id, amount=1))
    G.recipes.add_recipe(["# #", "###", "###"], {'#': material},
                   ItemStack(armors[1].id, amount=1))
    G.recipes.add_recipe(["###", "# #", "# #"], {'#': material},
                    ItemStack(armors[2].id, amount=1))
    G.recipes.add_recipe(["# #", "# #"], {'#': material},
                    ItemStack(armors[-1].id, amount=1))

#sand items


for wood in (birchwoodplank_block, junglewoodplank_block, oakwoodplank_block):
    G.recipes.add_recipe(["#", "#"], {'#': wood},
                        ItemStack(stick_item.id, amount=4))
    G.recipes.add_recipe(["###", "# #", "###"], {'#': wood},
                        ItemStack(chest_block.id, amount=1))
    G.recipes.add_recipe(["##", "##"], {'#': wood},
                        ItemStack(craft_block.id, amount=1))
    G.recipes.add_recipe(["###", " @ ", " @ "], {'#': wood, '@': stick_item}, ItemStack(wood_pickaxe.id, amount=1))
    G.recipes.add_recipe(["## ", "#@ ", " @ "], {'#': wood, '@': stick_item}, ItemStack(wood_axe.id, amount=1))
    G.recipes.add_recipe([" # ", " @ ", " @ "], {'#': wood, '@': stick_item}, ItemStack(wood_shovel.id, amount=1))

# sand items

G.recipes.add_recipe(["##", "##"], {'#': sand_block},
                   ItemStack(sandstone_block.id, amount=1))

# plants items
G.recipes.add_recipe(["#"], {'#': yflowers_block}, ItemStack(yellowdye_item.id, amount=2))
G.recipes.add_recipe(["#"], {'#': rose_block}, ItemStack(reddye_item.id, amount=2))
G.recipes.add_recipe(["#"], {'#': reed_block}, ItemStack(sugar_item.id, amount=1))
G.recipes.add_recipe(["   ","   ", "###"], {'#': reed_block}, ItemStack(paper_item.id, amount=4))
G.recipes.add_recipe(["   ","   ", "###"], {'#': wheat_item},
                   ItemStack(bread_item.id, amount=1))

# combined items
G.recipes.add_recipe(["#", "@"], {'#': coal_item, '@': stick_item},
                   ItemStack(torch_block.id, amount=4))


G.smelting_recipes.add_recipe(ironore_block, ItemStack(iron_ingot_item.id, amount=1))
G.smelting_recipes.add_recipe(cobble_block, ItemStack(stone_block.id, amount=1))
