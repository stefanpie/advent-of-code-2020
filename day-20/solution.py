import numpy as np
import re
import itertools
import copy
import matplotlib.pyplot as plt


def get_neigbors_indexes(p):
    neighbours_indexes = [(p[0]+1,p[1]),(p[0]-1,p[1]),(p[0],p[1]+1),(p[0],p[1]-1)]
    return neighbours_indexes


class Tile:
    def __init__(self, tile_id, tile_array):
        self.tile_id = tile_id
        self.tile_array = tile_array
        
    @property
    def all_tile_array_orientations(self):
        possible_tile_arrays = []
        for i in range(4):
            new_tile = np.rot90(self.tile_array, k=i)
            possible_tile_arrays.append(
                {'flipped': 0,
                 'rotation': 90*i,
                 'array': new_tile,
                 'id': self.tile_id,
                 'edges':{
                     'top': new_tile[0,:],
                     'bottom': new_tile[-1,:],
                     'left': new_tile[:,0],
                     'right': new_tile[:,-1]
                 }}
            )
        for i in range(4):
            new_tile = np.rot90(np.fliplr(self.tile_array), k=i)
            possible_tile_arrays.append(
                {'flipped': 0,
                 'rotation': 90*i,
                 'array': new_tile,
                 'id': self.tile_id,
                 'edges':{
                     'top': new_tile[0,:],
                     'bottom': new_tile[-1,:],
                     'left': new_tile[:,0],
                     'right': new_tile[:,-1]
                 }}
            )
        return possible_tile_arrays

    def __repr__(self):
        string = ''
        string += '<\n'
        string += f"Tile ID: {self.tile_id}\n"
        string += f"{str(self.tile_array)}\n"
        string += '>\n'
        return string


class Image:
    def __init__(self):
        self.tiles = []
        self.image = {}
    
    def solve_image_from_tiles(self):
        tiles_not_placed = copy.copy(self.tiles)
        tiles_placed = []

        initial_tile = tiles_not_placed.pop(0).all_tile_array_orientations[0]
        self.image[(0,0)] = initial_tile
        tiles_placed.append(initial_tile)


        while(len(tiles_not_placed)>0):
            # print([(k, v['id']) for k,v in  self.image.items()])
            print(tiles_placed.__len__())
            print(tiles_not_placed.__len__())
            plot_image(self.image)
            for target_pos, target_tile in copy.deepcopy(self.image).items():
                # print(f"target_pos: {target_pos}")
                # print(f"target_tile_id: {target_tile['id']}")
                tile_neighbor_indexes = get_neigbors_indexes(target_pos)
                empty_tile_neighbor_indexes = list(filter(lambda i: i not in self.image, tile_neighbor_indexes))
                # print(f"empty_tile_neighbor_indexes: {empty_tile_neighbor_indexes}")
                for empty_tile_neighbor_index in empty_tile_neighbor_indexes:
                    print(f"empty_tile_neighbor_index: {empty_tile_neighbor_index}")
                    # segment_to_look_at_target = ''
                    # segment_to_look_at_candidate = ''
                    # if empty_tile_neighbor_index == (target_pos[0]+1, target_pos[1]):
                    #     segment_to_look_at_target = 'right'
                    #     segment_to_look_at_candidate = 'left'
                    # elif empty_tile_neighbor_index == (target_pos[0]-1, target_pos[1]):
                    #     segment_to_look_at_target = 'left'
                    #     segment_to_look_at_candidate = 'right'
                    # elif empty_tile_neighbor_index == (target_pos[0], target_pos[1]+1):
                    #     segment_to_look_at_target = 'top'
                    #     segment_to_look_at_candidate = 'bottom'
                    # elif empty_tile_neighbor_index == (target_pos[0], target_pos[1]-1):
                    #     segment_to_look_at_target = 'bottom'
                    #     segment_to_look_at_candidate = 'top'
                    # print(f'segment_to_look_at_target: {segment_to_look_at_target}')
                    # print(f'segment_to_look_at_candidate: {segment_to_look_at_candidate}')
                    
                    found_canditate = False
                    for i, candiate in enumerate(copy.deepcopy(tiles_not_placed)):
                        for candiate_combo in candiate.all_tile_array_orientations:
                            valid_candiate_combo = True
                            # print(self.image.keys())
                            placed_tiles_to_check_with_empty = get_neigbors_indexes(empty_tile_neighbor_index)
                            placed_tiles_to_check_with_empty = [i for i in placed_tiles_to_check_with_empty if i in self.image]
                            print(placed_tiles_to_check_with_empty)
                            for placed_tile in placed_tiles_to_check_with_empty:
                                segment_to_look_at_filled = ''
                                segment_to_look_at_empty = ''
                                if empty_tile_neighbor_index == (placed_tile[0]+1, placed_tile[1]):
                                    segment_to_look_at_filled = 'right'
                                    segment_to_look_at_empty = 'left'
                                elif empty_tile_neighbor_index == (placed_tile[0]-1, placed_tile[1]):
                                    segment_to_look_at_filled = 'left'
                                    segment_to_look_at_empty = 'right'
                                elif empty_tile_neighbor_index == (placed_tile[0], placed_tile[1]+1):
                                    segment_to_look_at_filled = 'bottom'
                                    segment_to_look_at_empty = 'top'
                                elif empty_tile_neighbor_index == (placed_tile[0], placed_tile[1]-1):
                                    segment_to_look_at_filled = 'top'
                                    segment_to_look_at_empty = 'bottom'
                                segment_for_checking_target = target_tile['edges'][segment_to_look_at_filled]
                                segment_for_checking_candiate_combo = candiate_combo['edges'][segment_to_look_at_empty]
                                valid_candiate_combo &= (segment_for_checking_target == segment_for_checking_candiate_combo).all()
                            if valid_candiate_combo:
                                good_tile = tiles_not_placed.pop(i)
                                self.image[empty_tile_neighbor_index] = candiate_combo
                                tiles_placed.append(good_tile)
                                found_canditate = True
                            if found_canditate:
                                break
                        if found_canditate:
                                break
                    if found_canditate:
                                break
                # input("...")
                # print()
                                
                    
def plot_image(image):
    cordinate_data = {}
    # cordinate_data['min_x'] = min([k[0] for k in image])
    # cordinate_data['max_x'] = max([k[0] for k in image])
    # cordinate_data['min_y'] = min([k[1] for k in image])
    # cordinate_data['max_y'] = max([k[1] for k in image])
    cordinate_data['min_x'] = -4
    cordinate_data['max_x'] = 4
    cordinate_data['min_y'] = -4
    cordinate_data['max_y'] = 4

    # cordinate_data['top_left'] = image[(cordinate_data['min_x'], cordinate_data['max_y'])]['id']
    # cordinate_data['top_right'] = image[(cordinate_data['max_x'], cordinate_data['max_y'])]['id']
    # cordinate_data['bottom_left'] = image[(cordinate_data['min_x'], cordinate_data['min_y'])]['id']
    # cordinate_data['bottom_right'] = image[(cordinate_data['max_x'], cordinate_data['min_y'])]['id']

    x_blocks = cordinate_data['max_x'] - cordinate_data['min_x'] +1
    y_blocks = cordinate_data['max_y'] - cordinate_data['min_y'] +1
    # print()
    # for k, v in image.items():
    #     print(v['id'])
    # print()
    image_matrix = [[0 for i in range(x_blocks)] for j in range(y_blocks)]
    for i in range(y_blocks):
        for j in range(x_blocks):
            x_y_cordinate = (j+cordinate_data['min_x'], i+cordinate_data['min_y'])
            # print(x_y_cordinate in image)
            if x_y_cordinate in image:
                # print(f"x_y_cordinate: {x_y_cordinate}")
                # print(f"x_y_cordinate: {image[x_y_cordinate]['id']}")
                image_matrix[i][j] = image[x_y_cordinate]

    # print(image_matrix)

    # for i in range(y_blocks):
    #     for j in range(x_blocks):
    #         if image_matrix[i][j] != 0:
    #             print(image_matrix[i][j]['id'])
    

    fig, axs = plt.subplots(y_blocks, x_blocks)
    
    # print(axs)

    # print(image_matrix[0][0]['array'] == image_matrix[1][0]['array'] )

    for i in range(y_blocks):
        for j in range(x_blocks):
            if image_matrix[i][j] != 0:
                axs[i][j].matshow(image_matrix[i][j]['array'])
            axs[i][j].set_xticklabels([])
            axs[i][j].set_xticks([])
            axs[i][j].set_yticklabels([])
            axs[i][j].set_yticks([])
            axs[i][j].get_xaxis().set_visible(False)
            axs[i][j].get_yaxis().set_visible(False)

    plt.subplots_adjust(wspace=0, hspace=0)
    plt.show()
                

        

if __name__ == "__main__":
    with open("input_small.txt") as f:
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
        image_data.append((tile_id, tile_array))
    
    image_data = [Tile(id, a) for id, a in image_data]

    image = Image()
    image.tiles = image_data
    # print(image.tiles[0].all_tile_array_orientations[0])
    print(len(image.tiles))

    image.solve_image_from_tiles()
    # for k,v in image.image.items():
    #     print(f"{k} : {v['id']}")

    plot_image(image.image)
    print()
    

