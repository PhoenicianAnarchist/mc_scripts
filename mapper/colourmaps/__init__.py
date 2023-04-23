from . import minecraft

from . import appliedenergistics2
from . import biomesoplenty
from . import create
from . import chisel
from . import decorative_blocks
from . import exoticbirds
from . import extcaves
from . import farmersdelight
from . import forbidden_arcanus
from . import randomium
from . import supplementaries
from . import tconstruct
from . import xkdeco

maps = [
    minecraft.Map(),

    appliedenergistics2.Map(),
    biomesoplenty.Map(),
    create.Map(),
    chisel.Map(),
    decorative_blocks.Map(),
    exoticbirds.Map(),
    extcaves.Map(),
    farmersdelight.Map(),
    forbidden_arcanus.Map(),
    randomium.Map(),
    supplementaries.Map(),
    tconstruct.Map(),
    xkdeco.Map()
]

for map in maps:
    map.generate()
