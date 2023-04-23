from . import _map

class Map(_map.MapBase):
    def __init__(self):
        super().__init__()

    def generate(self):
        self.transparent.append("minecraft:air")
        self.transparent.append("minecraft:cave_air") # ???
        self.transparent.append("minecraft:glass")
        self.transparent.append("minecraft:glass_pane")

        self.map["minecraft:clay"] = (151, 160, 175)
        self.map["minecraft:gravel"] =  (129, 127, 127)
        self.map["minecraft:dirt"] = (185, 133, 92)
        self.map["minecraft:grass_block"] = (72, 94, 57)
        self.map["minecraft:water"] =  (55, 88, 152)
        self.map["minecraft:lava"] =  (205, 66, 8)
        self.map["minecraft:bedrock"] = (34, 34, 34)
        self.map["minecraft:obsidian"] = (16, 12, 28)
        self.map["minecraft:podzol"] = (74, 48, 24)
        self.map["minecraft:sugar_cane"] = (170, 219, 166)

        self.map["minecraft:torch"] = (255, 216, 0)
        self.map["minecraft:coarse_dirt"] = (92, 65, 44)
        self.map["minecraft:wall_torch"] = (255, 216, 0)
        self.map["minecraft:smooth_stone_slab"] = (168, 168, 168)

        self.grasses()
        self.woods()
        self.sands()
        self.wools()
        self.coppers()
        self.bricks()
        self.corals()
        self.ores()
        self.blocks()
        self.blocks_polished()
        self.blocks_extra()
        self.rails(show_rail_types=True)
        self.amethyst()
        self.crops()
        self.villages(highlight_jobsite=False)
        self.redstone_stuff()
        self.monster_eggs(highlight_monster_eggs=False)

    def grasses(self):
        for grass in [
            "grass", "tall_grass",
            "seagrass", "tall_seagrass",
            "kelp", "kelp_plant"
        ]:
            self.map[f"minecraft:{grass}"] = (80, 149, 41)

    def woods(self):
        woods = {
            ## Wood Name:   [ planks, log, stripped, leaves ]
            "acacia":       [(186,  99,  55), (105,  98,  89), (153,  92,  59), ( 56,  82,  38)],
            "birch":        [(215, 193, 133), (235, 235, 231), (167, 142,  86), ( 64,  82,  42)],
            "dark_oak":     [( 79,  50,  24), ( 63,  49,  29), ( 53,  43,  28), ( 76, 113,  51)],
            "cherry":       [(215, 177, 168), ( 36,  20,  30), (191, 124, 119), (242, 215, 236)],
            "jungle_log":   [(184, 135, 100), (120,  93,  38), (151, 124,  69), ( 56,  82,  38)],
            "oak":          [(184, 148,  95), ( 95,  74,  43), (125, 103,  57), ( 43,  61,  29)],
            "spruce":       [(130,  97,  58), ( 85,  58,  31), ( 70,  58,  32), ( 23,  37,  23)],
            "bamboo":       [( 89, 144,   3), ( 89, 144,   3), ( 89, 144,   3), ( 89, 144,   3)],
            "mangrove":     [(117,  56,  52), ( 77,  62,  39), (108,  44,  45), ( 45,  65,  30)]
        }

        nether_woods = {
            ## Wood Name:   [ planks, log, stripped, leaves ]
            "crimson":  [(134,  62,  90), ( 75,  39,  55), (128,  56,  83), (148,  24,  24)],
            "warped":   [( 58, 142, 140), ( 75,  39,  55), ( 49, 141, 140), ( 22, 126, 134)]
        }

        for wood, [planks, log, stripped, leaves] in woods.items():
            self.map[f"minecraft:{wood}_button"] = planks
            self.map[f"minecraft:{wood}_door"] = planks
            self.map[f"minecraft:{wood}_fence"] = planks
            self.map[f"minecraft:{wood}_fence_gate"] = planks
            self.map[f"minecraft:{wood}_hanging_sign"] = planks
            self.map[f"minecraft:{wood}_planks"] = planks
            self.map[f"minecraft:{wood}_pressure_plate"] = planks
            self.map[f"minecraft:{wood}_sign"] = planks
            self.map[f"minecraft:{wood}_slab"] = planks
            self.map[f"minecraft:{wood}_stairs"] = planks
            self.map[f"minecraft:{wood}_trapdoor"] = planks

            self.map[f"minecraft:{wood}_leaves"] = leaves
            self.map[f"minecraft:{wood}_log"] = log
            self.map[f"minecraft:{wood}_sapling"] = leaves
            self.map[f"minecraft:{wood}_wood"] = log
            self.map[f"minecraft:stripped_{wood}_log"] = stripped
            self.map[f"minecraft:stripped_{wood}_wood"] = stripped

        for wood, [planks, log, stripped, leaves] in nether_woods.items():
            self.map[f"minecraft:{wood}_button"] = planks
            self.map[f"minecraft:{wood}_door"] = planks
            self.map[f"minecraft:{wood}_fence"] = planks
            self.map[f"minecraft:{wood}_fence_gate"] = planks
            self.map[f"minecraft:{wood}_hanging_sign"] = planks
            self.map[f"minecraft:{wood}_planks"] = planks
            self.map[f"minecraft:{wood}_pressure_plate"] = planks
            self.map[f"minecraft:{wood}_sign"] = planks
            self.map[f"minecraft:{wood}_slab"] = planks
            self.map[f"minecraft:{wood}_stairs"] = planks
            self.map[f"minecraft:{wood}_trapdoor"] = planks

            self.map[f"minecraft:{wood}_fungus"] = leaves
            self.map[f"minecraft:{wood}_hyphae"] = planks
            self.map[f"minecraft:{wood}_nylium"] = leaves
            self.map[f"minecraft:{wood}_roots"] = log
            self.map[f"minecraft:{wood}_stem"] = log
            self.map[f"minecraft:stripped_{wood}_hyphae"] = stripped
            self.map[f"minecraft:stripped_{wood}_stem"] = stripped


        self.delete("minecraft:bamboo_leaves")
        self.delete("minecraft:stripped_bamboo_log")

        self.rename("minecraft:bamboo_log",             "minecraft:bamboo")
        self.rename("minecraft:bamboo_sapling",         "minecraft:bamboo_shoot")
        self.rename("minecraft:bamboo_wood",            "minecraft:block_of_bamboo")
        self.rename("minecraft:stripped_bamboo_wood",   "minecraft:block_of_stripped_bamboo")

        self.rename("minecraft:mangrove_sapling",       "minecraft:mangrove_propugale")

    def sands(self):
        sands = {
            "sand":     (231, 228, 187),
            "red_sand": (210, 117,  43)
        }

        for sand, colour in sands.items():
            self.map[f"minecraft:{sand}"] = colour
            self.map[f"minecraft:{sand}stone"] = colour
            self.map[f"minecraft:{sand}stone_slab"] = colour
            self.map[f"minecraft:{sand}stone_stairs"] = colour
            self.map[f"minecraft:{sand}stone_wall"] = colour
            self.map[f"minecraft:smooth_{sand}stone"] = colour
            self.map[f"minecraft:smooth_{sand}stone_slab"] = colour
            self.map[f"minecraft:smooth_{sand}stone_stairs"] = colour
            self.map[f"minecraft:cut_{sand}stone"] = colour
            self.map[f"minecraft:cut_{sand}stone_slab"] = colour
            self.map[f"minecraft:chiseled_{sand}stone"] = colour

    def wools(self):

        wools = {
            "black":        [( 12,  14,  18), ["wither_rose"]],
            "blue":         [( 47,  50, 148), ["cornflower"]],
            "brown":        [(103,  64,  35), ["brown_mushroom"]],
            "cyan":         [( 21, 129, 139), []],
            "gray":         [( 57,  61,  65), []],
            "green":        [( 77,  98,  32), ["cactus"]],
            "light_blue":   [( 44, 155, 207), ["blue_orchid"]],
            "light_gray":   [(132, 132, 132), ["azure_bluet", "oxeye_daisy", "white_tulip"]],
            "lime":         [(101, 175,  24), []],
            "magenta":      [(177,  56, 167), ["allium", "lilac"]],
            "orange":       [(232, 104,   7), ["orange_tulip", "torchflower"]],
            "pink":         [(229, 117, 155), ["poeny", "pink_tulip"]],
            "purple":       [(108,  35, 162), []],
            "red":          [(149,  34,  33), ["red_mushroom", "rose_bush", "poppy", "red_tulip"]],
            "white":        [(218, 223, 224), ["lily_of_the_valley"]],
            "yellow":       [(245, 185,  28), ["dandelion", "sunflower"]]
        }

        for wool, [colour, flowers] in wools.items():
            self.map[f"minecraft:{wool}_banner"] = colour
            self.map[f"minecraft:{wool}_bed"] = colour
            self.map[f"minecraft:{wool}_candle"] = colour
            self.map[f"minecraft:{wool}_carpet"] = colour
            self.map[f"minecraft:{wool}_concrete"] = colour
            self.map[f"minecraft:{wool}_concrete_powder"] = colour
            self.map[f"minecraft:{wool}_glazed_terracotta"] = colour
            self.map[f"minecraft:{wool}_shulker_box"] = colour
            self.map[f"minecraft:{wool}_stained_glass"] = colour
            self.map[f"minecraft:{wool}_stained_glass_pane"] = colour
            self.map[f"minecraft:{wool}_terracotta"] = colour
            self.map[f"minecraft:{wool}_wool"] = colour

            for flower in flowers:
                self.map[f"minecraft:{flower}"] = colour
                self.map[f"minecraft:potted_{flower}"] = colour

    def coppers(self):
        coppers = {
            "":             (224, 128, 107),
            "exposed":      (203, 139, 130),
            "weathered":    (120, 180, 152),
            "oxidized":     (108, 194, 158)
        }

        for copper, colour in coppers.items():
            self.map[f"minecraft:{copper}_copper"] = colour
            self.map[f"minecraft:{copper}_cut_copper"] = colour
            self.map[f"minecraft:{copper}_cut_copper_slab"] = colour
            self.map[f"minecraft:{copper}_cut_copper_stairs"] = colour
            self.map[f"minecraft:waxed_{copper}_copper"] = colour
            self.map[f"minecraft:waxed_{copper}_cut_copper"] = colour
            self.map[f"minecraft:waxed_{copper}_cut_copper_slab"] = colour
            self.map[f"minecraft:waxed_{copper}_cut_copper_stairs"] = colour

        self.rename("minecraft:_copper",        "copper_block")
        self.rename("minecraft:waxed__copper",  "waxed_copper_block")

    def bricks(self):

        self.map["minecraft:mud"] = (61, 55, 54)
        self.map["minecraft:polished_blackstone"] = (47, 42, 52)
        bricks = {
            "brick":                        (177,  98,  77),
            "deepslate_brick":              ( 63,  63,  63),
            "deepslate_tile":               ( 54,  54,  54),
            "end_stone_brick":              (236, 251, 175),
            "nether_brick":                 ( 41,  21,  25),
            "mossy_stone_brick":            (122, 143,  85),
            "mud_brick":                    (147, 111,  79),
            "polished_blackstone_brick":    self.map["minecraft:polished_blackstone"],
            "prismarine_brick":             (110, 185, 174),
            "red_nether_brick":             ( 56,   4,   5),
            "stone_brick":                  (139, 139, 139)
        }

        for brick, colour in bricks.items():
            self.map[f"minecraft:{brick}_slab"] = colour
            self.map[f"minecraft:{brick}_stairs"] = colour
            self.map[f"minecraft:{brick}_wall"] = colour
            self.map[f"minecraft:{brick}s"] = colour


        self.map["minecraft:nether_brick_fence"] =                  bricks["nether_brick"]
        self.map["minecraft:cracked_deepslate_bricks"] =            bricks["deepslate_brick"]
        self.map["minecraft:cracked_deepslate_tiles"] =             bricks["deepslate_tile"]
        self.map["minecraft:cracked_nether_bricks"] =               bricks["nether_brick"]
        self.map["minecraft:cracked_polished_blackstone_bricks"] =  bricks["polished_blackstone_brick"]
        self.map["minecraft:cracked_stone_bricks"] =                bricks["stone_brick"]

        self.map["minecraft:polished_blackstone_button"] =          bricks["polished_blackstone_brick"]
        self.map["minecraft:polished_blackstone_pressure_plate"] =  bricks["polished_blackstone_brick"]
        self.map["minecraft:polished_blackstone_slab"] =            bricks["polished_blackstone_brick"]
        self.map["minecraft:polished_blackstone_stairs"] =          bricks["polished_blackstone_brick"]
        self.map["minecraft:polished_blackstone_wall"] =            bricks["polished_blackstone_brick"]

        self.delete("minecraft:prismarine_brick_wall")

    def corals(self):
        dead_coral_colour = (134, 123, 119)

        corals = {
            "brain":    (217,  98, 163),
            "bubble":   (145,  22, 145),
            "fire":     (198,  42,  55),
            "horn":     (209, 179,  65),
            "tube":     ( 49,  79, 221)
        }

        for coral, colour in corals.items():
            self.map[f"minecraft:{coral}_coral"] = colour
            self.map[f"minecraft:{coral}_coral_block"] = colour
            self.map[f"minecraft:{coral}_coral_fan"] = colour
            self.map[f"minecraft:dead_{coral}_coral"] = dead_coral_colour
            self.map[f"minecraft:dead_{coral}_coral_block"] = dead_coral_colour
            self.map[f"minecraft:dead_{coral}_coral_fan"] = dead_coral_colour

    def ores(self):

        ores = {
            "coal":     ( 63,  63,  63),
            "diamond":  (101, 245, 227),
            "emerald":  ( 23, 221,  98),
            "lapis":    ( 24,  85, 189),
            "redstone": (151,   3,   3),
        }

        raw_ores = {
            "copper":   (219, 113,  75),
            "gold":     (252, 238,  75),
            "iron":     (188, 153, 128),
        }

        for ore, colour in ores.items():
            self.map[f"minecraft:{ore}_ore"] = colour
            self.map[f"minecraft:{ore}_block"] = colour

        for raw_ore, colour in raw_ores.items():
            self.map[f"minecraft:{raw_ore}_ore"] = colour
            self.map[f"minecraft:{raw_ore}_block"] = colour
            self.map[f"minecraft:raw_{raw_ore}_block"] = colour

        self.map["minecraft:nether_gold_ore"] = raw_ores["gold"]

    def blocks(self):
        blocks = {
            ## plain, slab, stairs, wall
            "blackstone":           ( 31,  18,  27),
            "cobblestone":          (136, 136, 136),
            "cobbled_deepslate":    ( 69,  69,  69),
            "polished_deepslate":   ( 86,  86,  86),
            "mossy_cobblestone":    ( 82,  93,  57),
            "prismarine":           ( 94, 164, 150)
        }

        for block, colour in blocks.items():
            self.map[f"minecraft:{block}"] = colour
            self.map[f"minecraft:{block}_slab"] = colour
            self.map[f"minecraft:{block}_stairs"] = colour
            self.map[f"minecraft:{block}_wall"] = colour

    def blocks_polished(self):
        blocks = {
            ## plain, slab, stairs, wall, polished_slab, polished_stairs
            "andesite": (138, 138, 142),
            "diorite":  (233, 233, 233),
            "granite":  (159, 107,  88),
        }

        for block, colour in blocks.items():
            self.map[f"minecraft:{block}"] = colour
            self.map[f"minecraft:{block}_slab"] = colour
            self.map[f"minecraft:{block}_stairs"] = colour
            self.map[f"minecraft:{block}_wall"] = colour
            self.map[f"minecraft:polished_{block}"] = colour
            self.map[f"minecraft:polished_{block}_slab"] = colour
            self.map[f"minecraft:polished_{block}_stairs"] = colour

    def blocks_extra(self):

        blocks = {
            ## plain, slab, stairs
            "bamboo_mosaic":    (170, 159,  68),
            "dark_prismarine":  ( 52,  86,  72),
            "purpur":           (178, 134, 178),
            "smooth_quartz":    (226, 222, 208),
            "stone":            (143, 143, 143),
            "quartz":           (226, 222, 208)
        }

        for block, colour in blocks.items():
            self.map[f"minecraft:{block}"] = colour
            self.map[f"minecraft:{block}_slab"] = colour
            self.map[f"minecraft:{block}_stairs"] = colour

        self.map["minecraft:purpur_pillar"] = blocks["purpur"]
        self.map["minecraft:stone_button"] = blocks["stone"]
        self.map["minecraft:stone_pressure_plate"] = blocks["stone"]
        self.map["minecraft:quartz_pillar"] = blocks["quartz"]
        self.map["minecraft:quartz_bricks"] = blocks["quartz"]
        self.map["minecraft:nether_quartz_ore"] = blocks["quartz"]

        self.rename("minecraft:smooth_quartz", "minecraft:smooth_quartz_block")
        self.rename("minecraft:quartz", "minecraft:quartz_block")

    def rails(self, show_rail_types=False):
        rail = (104, 104, 104)
        self.map["minecraft:rail"] = rail
        if show_rail_types:
            self.map["minecraft:activator_rail"] = (98, 2, 2)
            self.map["minecraft:detector_rail"] = (171, 171, 171)
            self.map["minecraft:powered_rail"] = (201, 136, 29)
        else:
            self.map["minecraft:activator_rail"] = rail
            self.map["minecraft:detector_rail"] = rail
            self.map["minecraft:powered_rail"] = rail

    def amethyst(self):
        amethyst = (207, 160, 243)
        self.map["minecraft:amethyst_cluster"] = amethyst
        self.map["minecraft:amethyst_block"] = amethyst
        self.map["minecraft:budding_amethyst"] = amethyst
        self.map["minecraft:large_amethyst_bud"] = amethyst
        self.map["minecraft:medium_amethyst_bud"] = amethyst
        self.map["minecraft:small_amethyst_bud"] = amethyst

    def crops(self):
        self.map["minecraft:beetroot"] = (113, 21, 11)
        self.map["minecraft:carrot"] = (255, 142, 9)
        self.map["minecraft:potato"] = (217, 170, 81)
        self.map["minecraft:pumpkin"] = (227, 138, 29)
        self.map["minecraft:melon"] = (82, 129, 28)

    def villages(self, highlight_jobsite=False):
        bell = (255, 246, 141)

        self.map["minecraft:bell"] = bell
        self.map["minecraft:dirt_path"] = (114, 117, 64)
        self.map["minecraft:bookshelf"] = (179, 140, 81)
        self.map["minecraft:anvil"] = (82, 82, 82)
        self.map["minecraft:chipped_anvil"] = (82, 82, 82)
        self.map["minecraft:damaged_anvil"] = (82, 82, 82)
        self.map["minecraft:crafting_table"] = (174, 105, 60)
        self.map["minecraft:farmland"] = (85, 46, 15)
        self.map["minecraft:furnace"] = (104, 104, 104)
        self.map["minecraft:chest"] = (167, 110, 31)

        if highlight_jobsite:
            self.map["minecraft:barrel"] = (139, 103, 60)
            self.map["minecraft:blast_furnace"] = (72, 72, 72)
            self.map["minecraft:brewing_stand"] = (212, 183, 58)
            self.map["minecraft:cartography_table"] = (70, 45, 21)
            self.map["minecraft:cauldron"] = (88, 88, 88)
            self.map["minecraft:composter"] = (135, 88, 46)
            self.map["minecraft:fletching_table"] = ()
            self.map["minecraft:grindstone"] = ()
            self.map["minecraft:lectern"] = ()
            self.map["minecraft:loom"] = ()
            self.map["minecraft:smithing_table"] = ()
            self.map["minecraft:smoker"] = ()
            self.map["minecraft:stonecutter"] = ()
        else:
            self.map["minecraft:barrel"] = bell
            self.map["minecraft:blast_furnace"] = bell
            self.map["minecraft:brewing_stand"] = bell
            self.map["minecraft:cartography_table"] = bell
            self.map["minecraft:cauldron"] = bell
            self.map["minecraft:composter"] = bell
            self.map["minecraft:fletching_table"] = bell
            self.map["minecraft:grindstone"] = bell
            self.map["minecraft:lectern"] = bell
            self.map["minecraft:loom"] = bell
            self.map["minecraft:smithing_table"] = bell
            self.map["minecraft:smoker"] = bell
            self.map["minecraft:stonecutter"] = bell

    def redstone_stuff(self):
        self.map["minecraft:daylight_detector"] = (223, 212, 197)
        self.map["minecraft:dispenser"] = (197, 197, 197)
        self.map["minecraft:dropper"] = (197, 197, 197)
        self.map["minecraft:heavy_weighted_pressure_plate"] = (188, 153, 128)
        self.map["minecraft:light_weighted_pressure_plate"] = (252, 238,  75)
        self.map["minecraft:hopper"] = (72, 72, 72)

    def monster_eggs(self, highlight_monster_eggs=False):
        highlight = (0, 255, 255)

        if highlight_monster_eggs:
            self.map["minecraft:infested_chiseled_stone_bricks"] = highlight
            self.map["minecraft:infested_deepslate"] = highlight
            self.map["minecraft:infested_mossy_stone_brick"] = highlight
            self.map["minecraft:infested_cracked_stone_brick"] = highlight
            self.map["minecraft:infested_stone_brick"] = highlight
            self.map["minecraft:infested_cobblestone"] = highlight
        else:
            self.map["minecraft:infested_chiseled_stone_bricks"] = (127, 127, 127)
            self.map["minecraft:infested_deepslate"] = (84, 84, 84)
            self.map["minecraft:infested_mossy_stone_brick"] = (122, 143,  85)
            self.map["minecraft:infested_cracked_stone_brick"] = (139, 139, 139)
            self.map["minecraft:infested_stone_brick"] = (139, 139, 139)
            self.map["minecraft:infested_cobblestone"] = (136, 136, 136)
