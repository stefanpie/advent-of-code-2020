from typing import Dict, List, Set, Tuple
import numpy as np
import re
import functools 
from pprint import pprint
import copy
import matplotlib.pyplot as plt
from typing import Set
from scipy.signal import correlate2d

def get_neigbors_indexes(p: Tuple[int,int]) -> List[Tuple[int,int]]:
    neighbours_indexes = [(p[0]+1,p[1]),(p[0]-1,p[1]),(p[0],p[1]+1),(p[0],p[1]-1)]
    return neighbours_indexes

def get_check_edges(p_test_spot: Tuple[int,int], p_placed_neighbor_spot: Tuple[int,int]) -> Tuple[str,str]:
    edge_test_spot = ''
    edge_placed_neighbor_spot = ''
    if p_test_spot == (p_placed_neighbor_spot[0]+1, p_placed_neighbor_spot[1]):
        edge_test_spot = 'left'
        edge_placed_neighbor_spot = 'right'
    elif p_test_spot == (p_placed_neighbor_spot[0]-1, p_placed_neighbor_spot[1]):
        edge_test_spot = 'right'
        edge_placed_neighbor_spot = 'left'
    elif p_test_spot == (p_placed_neighbor_spot[0], p_placed_neighbor_spot[1]+1):
        edge_test_spot = 'bottom'
        edge_placed_neighbor_spot = 'top'
    elif p_test_spot == (p_placed_neighbor_spot[0], p_placed_neighbor_spot[1]-1):
        edge_test_spot = 'top'
        edge_placed_neighbor_spot = 'bottom'
    return (edge_test_spot, edge_placed_neighbor_spot)

class Tile:
    def __init__(self, id: int, array: List[List[int]]) -> None:
        self.id = id
        self.array = array
        self.transposed: int = 0
        self.rotated: int = 0
    
    def transpose(self) -> 'Tile':
        new_tile = copy.deepcopy(self)
        new_tile.array = [list(i) for i in zip(*new_tile.array)]
        new_tile.transposed += 1
        return new_tile

    def rot_90(self) -> 'Tile':
        new_tile = copy.deepcopy(self)
        new_tile.array = [[new_tile.array[j][i] for j in range(len(new_tile.array))] for i in range(len(new_tile.array[0])-1,-1,-1)]
        new_tile.rotated += 1
        return new_tile

    @property
    def variants(self) -> List['Tile']:
        variants_array = []
        variants_array.append(self)
        variants_array.append(self.rot_90())
        variants_array.append(self.rot_90().rot_90())
        variants_array.append(self.rot_90().rot_90().rot_90())
        variants_array.append(self.transpose())
        variants_array.append(self.transpose().rot_90())
        variants_array.append(self.transpose().rot_90().rot_90())
        variants_array.append(self.transpose().rot_90().rot_90().rot_90())
        return variants_array
    
    @property
    def edges(self) -> Dict[str, List[int]]:
        edge_map = {}
        edge_map['top'] = self.array[0][:]
        edge_map['bottom'] = self.array[-1][:]
        edge_map['left'] = [row[0] for row in self.array]
        edge_map['right'] = [row[-1] for row in self.array]
        return edge_map
    
    @property
    def array_borderless(self) -> List[List[int]]:
        new_array = copy.deepcopy(self.array)
        new_array = new_array[1:-1]
        new_array = [row[1:-1] for row in new_array]
        return new_array

    def __repr__(self) -> str:
        return f"Tile {self.id}: t={self.transposed}, r={self.rotated}"

class Image:
    def __init__(self, tiles) -> None:
        self.tiles: List[Tile] = tiles
        self.unplaced_tile_ids: Set[int] = set()
        self.placed_tile_ids: Set[int] = set()
        self.image_map: Dict[Tuple[int,int], Tile] = {}
        self.image_array: List[List[int]] = None

        for t in self.tiles:
            self.unplaced_tile_ids.add(t.id)

    @property
    def image_map_corner_ids(self) -> List[str]:
        cordinate_data = {}
        cordinate_data['min_x'] = min([c[0] for c in self.image_map])
        cordinate_data['max_x'] = max([c[0] for c in self.image_map])
        cordinate_data['min_y'] = min([c[1] for c in self.image_map])
        cordinate_data['max_y'] = max([c[1] for c in self.image_map])
        cordinate_data['top_left'] = (cordinate_data['min_x'], cordinate_data['max_y'])
        cordinate_data['top_right'] = (cordinate_data['max_x'], cordinate_data['max_y'])
        cordinate_data['bottom_left'] = (cordinate_data['min_x'], cordinate_data['min_y'])
        cordinate_data['bottom_right'] = (cordinate_data['max_x'], cordinate_data['min_y'])

        corner_ids = []
        corner_ids.append(self.image_map[cordinate_data['top_left']].id)
        corner_ids.append(self.image_map[cordinate_data['top_right']].id)
        corner_ids.append(self.image_map[cordinate_data['bottom_left']].id)
        corner_ids.append(self.image_map[cordinate_data['bottom_right']].id)

        return corner_ids

    def plot_tile_map(self) -> None:
        cordinate_data = {}
        cordinate_data['min_x'] = -4
        cordinate_data['max_x'] = 4
        cordinate_data['min_y'] = -4
        cordinate_data['max_y'] = 4
        
        x_blocks = cordinate_data['max_x'] - cordinate_data['min_x'] +1
        y_blocks = cordinate_data['max_y'] - cordinate_data['min_y'] +1

        image_matrix = [[0 for i in range(x_blocks)] for j in range(y_blocks)]
        for i in range(y_blocks):
            for j in range(x_blocks):
                x_y_cordinate = (j+cordinate_data['min_x'], -1*(i+cordinate_data['min_y']))
                if x_y_cordinate in self.image_map:
                    image_matrix[i][j] = self.image_map[x_y_cordinate]
        
        fig, axs = plt.subplots(y_blocks, x_blocks)

        for i in range(y_blocks):
            for j in range(x_blocks):
                if image_matrix[i][j] != 0:
                    axs[i][j].matshow(image_matrix[i][j].array)
                axs[i][j].set_xticklabels([])
                axs[i][j].set_xticks([])
                axs[i][j].set_yticklabels([])
                axs[i][j].set_yticks([])
                axs[i][j].get_xaxis().set_visible(False)
                axs[i][j].get_yaxis().set_visible(False)

        plt.subplots_adjust(wspace=0, hspace=0)
        plt.show()

    def place_tile(self, tile: Tile, position: Tuple[int,int]) -> None:
        self.image_map[position] = tile
        self.unplaced_tile_ids.remove(tile.id)
        self.placed_tile_ids.add(tile.id)

    @property
    def all_tiles_placed(self) -> bool:
        return not bool(self.unplaced_tile_ids)

    def solve_map(self) -> None:
        self.place_tile(self.tiles[0], (0,0))

        while(not self.all_tiles_placed):
            test_spots = []
            for p in self.image_map:
                test_spots += get_neigbors_indexes(p)
            test_spots = [ts for ts in test_spots if ts not in self.image_map]
            test_spots = list(set(test_spots))
            
            for test_spot in test_spots:                
                placed_neighbor_spots = get_neigbors_indexes(test_spot)
                placed_neighbor_spots= [s for s in placed_neighbor_spots if s in self.image_map]
                placed_neighbors = [self.image_map[s] for s in placed_neighbor_spots]
                neighbors_check_list = list(zip(placed_neighbor_spots, placed_neighbors))

                candidates_for_test_spot: List[Tile] = []
                for unplaced_tile_id in self.unplaced_tile_ids:
                    candidate_tile = [t for t in self.tiles if t.id == unplaced_tile_id][0]
                    candidates_for_test_spot += candidate_tile.variants

                for candiate in candidates_for_test_spot:
                    valid_candiate = []
                    for placed_neighbor_spot, placed_neighbor in neighbors_check_list:
                        edge_test_spot, edge_placed_neighbor_spot = get_check_edges(test_spot, placed_neighbor_spot)
                        valid_candiate.append(candiate.edges[edge_test_spot] == placed_neighbor.edges[edge_placed_neighbor_spot])
                    if all(valid_candiate) and valid_candiate:
                        self.place_tile(candiate, test_spot)
                        break
        self.construct_image_array()
    
    def construct_image_array(self) -> None:
        cordinate_data = {}
        cordinate_data['min_x'] = min([c[0] for c in self.image_map])
        cordinate_data['max_x'] = max([c[0] for c in self.image_map])
        cordinate_data['min_y'] = min([c[1] for c in self.image_map])
        cordinate_data['max_y'] = max([c[1] for c in self.image_map])
        cordinate_data['top_left'] = (cordinate_data['min_x'], cordinate_data['max_y'])
        cordinate_data['top_right'] = (cordinate_data['max_x'], cordinate_data['max_y'])
        cordinate_data['bottom_left'] = (cordinate_data['min_x'], cordinate_data['min_y'])
        cordinate_data['bottom_right'] = (cordinate_data['max_x'], cordinate_data['min_y'])
        
        x_blocks = cordinate_data['max_x'] - cordinate_data['min_x'] +1
        y_blocks = cordinate_data['max_y'] - cordinate_data['min_y'] +1

        tile_arrangement_matrix = [[0 for i in range(x_blocks)] for j in range(y_blocks)]
        for i in range(y_blocks):
            for j in range(x_blocks):
                x_y_cordinate = (j+cordinate_data['min_x'], -1*(i-cordinate_data['max_y']))
                if x_y_cordinate in self.image_map:
                    tile_arrangement_matrix[i][j] = self.image_map[x_y_cordinate]
        
        # fig, axs = plt.subplots(y_blocks, x_blocks)
        # for i in range(y_blocks):
        #     for j in range(x_blocks):
        #         axs[i][j].matshow(tile_arrangement_matrix[i][j].array)
        #         axs[i][j].set_xticklabels([])
        #         axs[i][j].set_xticks([])
        #         axs[i][j].set_yticklabels([])
        #         axs[i][j].set_yticks([])
        #         axs[i][j].get_xaxis().set_visible(False)
        #         axs[i][j].get_yaxis().set_visible(False)
        # plt.subplots_adjust(wspace=0, hspace=0)
        # plt.show()

        array_arrangement_matrix = [[0 for i in range(x_blocks)] for j in range(y_blocks)]
        for i in range(y_blocks):
            for j in range(x_blocks):
                array_arrangement_matrix[i][j] = np.array(tile_arrangement_matrix[i][j].array_borderless)
        # array_arrangement_matrix = np.array(array_arrangement_matrix)

        final_image_array = np.block(array_arrangement_matrix)
        # final_image_array = np.vstack(array_arrangement_matrix[:])
        # final_image_array = np.hstack(array_arrangement_matrix[:,])
        self.image_array = final_image_array.tolist()
    
    def find_sea_monsters(self) -> int:
        sea_monster = [list(map(int, list('00000000000000000010'))),
                       list(map(int, list('10000110000110000111'))),
                       list(map(int, list('01001001001001001000')))]
        sea_monster_np = np.array(sea_monster)
        image_array_np = np.array(self.image_array)

        image_array_variants = []
        image_array_variants.append(image_array_np)
        image_array_variants.append(np.rot90(image_array_np, k=1))
        image_array_variants.append(np.rot90(image_array_np, k=2))
        image_array_variants.append(np.rot90(image_array_np, k=3))
        image_array_variants.append(image_array_np.T)
        image_array_variants.append(np.rot90(image_array_np.T, k=1))
        image_array_variants.append(np.rot90(image_array_np.T, k=2))
        image_array_variants.append(np.rot90(image_array_np.T, k=3))
        for v in image_array_variants:
            result = correlate2d(v, sea_monster_np, mode='valid')
            if np.max(result) == 15:
                return np.count_nonzero(result == 15)



if __name__ == "__main__":
    with open("input.txt") as f:
        image_data_raw = f.read()
    image_data_raw = re.split(r"\r?\n\r?\n", image_data_raw)
    image_data_raw = [list(i.splitlines()) for i in image_data_raw]
    image_data = []
    for tile in image_data_raw:
        tile_id = int(tile[0].replace('Tile ','').replace(':',''))
        tile_array = np.array([list(i) for i in tile[1:]])
        tile_array[tile_array == '.'] = 0
        tile_array[tile_array == '#'] = 1
        tile_array = tile_array.astype(int)
        tile_array = tile_array.tolist()
        image_data.append((tile_id, tile_array))
    
    tile_collection = [Tile(id, a) for id, a in image_data]

    image = Image(tile_collection)
    image.solve_map()
    image_corner_product = functools.reduce(lambda x, y: x*y, image.image_map_corner_ids)
    print(f"Part 1: {image_corner_product}")
    
    number_of_sea_monsters = image.find_sea_monsters()
    water_roughness = sum(row.count(1) for row in image.image_array) - 15*number_of_sea_monsters
    print(f"Part 2: {water_roughness}")

