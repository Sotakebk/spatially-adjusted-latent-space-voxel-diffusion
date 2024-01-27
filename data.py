import sys
import os
import numpy as np
from minecraftschematics import Schematic
from collections import defaultdict


def parse_schem(name, dir='.'):
    schema = Schematic.load(os.path.join(dir, name))

    biome = name.split('/')[-1]
    biome = biome[:biome.find('-')]
    palette = schema.palette
    offset = schema.offset
    x = offset[0]
    y = offset[1]
    z = offset[2]
    chunk = []
    for block in schema.raw['BlockData']:
        chunk.append(palette[block].type)
        if x - offset[0] == 15:
            if z - offset[2] == 15:
                y += 1
                z = offset[2]
            else:
                z += 1
            x = offset[0]
        else:
            x += 1
    return (biome, chunk)


# print('x', 'y', 'z', 'block_id', 'biome', sep=',')
print('--- input ---')
chunks = defaultdict(list)
arg = sys.argv[1]
if os.path.isdir(arg):
    for f in os.listdir(arg):
        if f.endswith('.schem'):
            biome, chunk = parse_schem(f, arg)
            chunks[biome].append(chunk)

if os.path.isfile(arg):
    biome, chunk = parse_schem(arg)
    chunks[biome].append(chunk)
else:
    names = arg.split(',')
    for name in names:
        for f in os.listdir(name):
            if f.endswith('.schem'):
                biome, chunk = parse_schem(f, name)
                chunks[biome].append(chunk)

print('--- palettization ---')
stone = 'minecraft:stone'
gravel = 'minecraft:gravel'
air = 'minecraft:air'
replace = {
    'minecraft:deepslate_redstone_ore': stone,
    'minecraft:deepslate_copper_ore': stone,
    'minecraft:deepslate_lapis_ore': stone,
    'minecraft:small_amethyst_bud': stone,
    'minecraft:large_amethyst_bud': stone,
    'minecraft:raw_copper_block': stone,
    'minecraft:amethyst_block': stone,
    'minecraft:smooth_basalt': stone,
    'minecraft:redstone_ore': stone,
    'minecraft:magma_block': stone,
    'minecraft:moss_block': stone,
    'minecraft:copper_ore': stone,
    'minecraft:lapis_ore': stone,
    'minecraft:deepslate': stone,
    'minecraft:tuff': stone,
    'minecraft:light_gray_terracotta': gravel,
    'minecraft:orange_terracotta': gravel,
    'minecraft:white_terracotta': gravel,
    'minecraft:brown_terracotta': gravel,
    'minecraft:red_terracotta': gravel,
    'minecraft:terracotta': gravel,
    'minecraft:andesite': gravel,
    'minecraft:diorite': gravel,
    'minecraft:granite': gravel,
    'minecraft:calcite': gravel,
    'minecraft:medium_amethyst_bud': air,
    'minecraft:cave_vines_plant': air,
    'minecraft:budding_amethyst': air,
    'minecraft:amethyst_cluster': air,
    'minecraft:glow_lichen': air,
    'minecraft:moss_carpet': air,
    'minecraft:cave_vines': air,
    'minecraft:cave_air': air,
    'minecraft:spawner': air,
    'minecraft:vine': air,
    'minecraft:deepslate_diamond_ore': 'minecraft:diamond_ore',
    'minecraft:deepslate_iron_ore': 'minecraft:iron_ore',
    'minecraft:deepslate_coal_ore': 'minecraft:coal_ore',
    'minecraft:deepslate_gold_ore': 'minecraft:gold_ore',
    'minecraft:bubble_column': 'minecraft:water',
    # theese are for minmal size of palette
    'minecraft:seagrass': 'minecraft:water',
    'minecraft:tall_seagrass': 'minecraft:water',
    'minecraft:azalea': 'minecraft:air',
    'minecraft:flowering_azalea': 'minecraft:air',
    'minecraft:oxeye_daisy': 'minecraft:dandelion',
    'minecraft:cornflower': 'minecraft:dandelion',
    'minecraft:azure_bluet': 'minecraft:dandelion',
    'minecraft:sunflower': 'minecraft:poppy',
    'minecraft:lily_of_the_valley': 'minecraft:poppy',
    'minecraft:peony': 'minecraft:poppy',
    'minecraft:rose_bush': 'minecraft:poppy',
    'minecraft:acacia_log': 'minecraft:oak_log',
    'minecraft:acacia_leaves': 'minecraft:oak_leaves',
    'minecraft:birch_log': 'minecraft:oak_log',
    'minecraft:birch_leaves': 'minecraft:oak_leaves',
}
palette = []
for biome, chks in chunks.items():
    for i, chunk in enumerate(chks):
        for j, block_type in enumerate(chunk):

            if block_type in replace.keys():
                chunks[biome][i][j] = replace[block_type]
                block_type = replace[block_type]

            if block_type not in palette:
                palette.append(block_type)


print(len(palette), ':', palette)
print(len(chunk), ':', len(chunks))

print('--- output ---')
version = 'v0.1'

for biome, chks in chunks.items():
    out = []
    for chunk in chks:
        for block in chunk:
            out.append(palette.index(block))
    np.savez(f'data-{biome}-{version}.npz', x=biome, y=np.array(out))


with open(f'palette-{version}.csv', 'w') as f:
    f.write('id,block_type\n')
    for i, block_type in enumerate(palette):
        f.write(f'{i},{block_type}\n')
