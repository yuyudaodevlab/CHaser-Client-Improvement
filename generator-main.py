import random
import os

def generate_map(name, block_count, item_count, size):
    width, height = size
    map_data = [[0 for _ in range(width)] for _ in range(height)]

    def place_randomly(value, count):
        placed = 0
        while placed < count:
            x, y = random.randint(0, width-1), random.randint(0, height-1)
            if map_data[y][x] == 0:
                map_data[y][x] = value
                placed += 1

    place_randomly(2, block_count)
    place_randomly(3, item_count)

    def place_player():
        while True:
            x, y = random.randint(0, width-1), random.randint(0, height-1)
            if map_data[y][x] == 0:
                return (x, y)

    cool_player_pos = place_player()
    hot_player_pos = place_player()
    while hot_player_pos == cool_player_pos:
        hot_player_pos = place_player()

    with open(f"{name}.map", "w") as f:
        f.write(f"N:{name}\n")
        f.write(f"S:{width},{height}\n")
        for row in map_data:
            f.write("D:" + ",".join(map(str, row)) + "\n")
        f.write(f"C:{cool_player_pos[0]},{cool_player_pos[1]}\n")
        f.write(f"H:{hot_player_pos[0]},{hot_player_pos[1]}\n")

# 出力関係
filename = input("ファイル名を入力してください（ファイル名の最後に番号が付きます）: ")
map_mode = input("マップのモードを入力してください (1: 15x17, 2: 21x17): ")
if map_mode == "1":
    size = (15, 17)
    max_block_count = 15*17
    max_item_count = 15*17
elif map_mode == "2":
    size = (21, 17)
    max_block_count = 21*17
    max_item_count = 21*17
else:
    print("無効なマップモードです。")
    exit()

print(f"ブロック及びアイテムの使用可能個数: {max_block_count}個")

out_put_mode = input("出力モードを選択してください 1:手動指定 2:ランダム生成")
if out_put_mode == "1":#手動指定
    print("手動指定モードが選択されました")
    block_count = 0
    block_input = input(f"ブロックの数を入力してください (最大数: {max_block_count}): ")
    block_count = int(block_input)

    while not str(block_count).isdigit() or int(block_count) > max_block_count:#ブロックの数が0からmax_block_countの範囲であるかを確認
        print(f"ブロックの数は0から{max_block_count}の間で入力してください。")
        block_count = input(f"ブロックの数を入力してください (最大数: {max_block_count}): ")
        block_count = int(block_count)

    max_item_count = max_block_count - int(block_count)

    item_count = 0
    item_input = input(f"アイテムの数を入力してください (最大数: {max_item_count}): ")
    item_count = int(item_input)
    while not str(item_count).isdigit() or int(item_count) > max_item_count:
        print(f"アイテムの数は0から{max_item_count}の間で入力してください。")
        item_count = input(f"アイテムの数を入力してください (最大数: {max_item_count}): ")  
        item_count = int(item_count) 
     
elif out_put_mode == "2":#ランダム生成
    print("ランダムモードが選択されました")
    block_input = input(f"ブロックの最大数を入力してください: (最大数: {max_block_count}): ")
    block_input = int(block_input)
    while not str(block_input).isdigit() or int(block_input) > max_block_count:
        print(f"ブロックの最大数は0から{max_block_count}の間で入力してください。")
        block_input = input(f"ブロックの最大数を入力してください: (最大数: {max_block_count}): ")
        block_input = int(block_input)
    
    max_item_count = max_block_count - int(block_input)
    item_input = input(f"アイテムの最大数を入力してください: (最大数: {max_item_count}): ")
    item_input = int(item_input)
    while not str(item_input).isdigit() or int(item_input) > max_item_count:
        print(f"アイテムの最大数は0から{max_item_count}の間で入力してください。")
        item_input = input(f"アイテムの最大数を入力してください: (最大数: {max_item_count}): ")  
        item_input = int(item_input)

    block_count = random.randint(0, block_input)
    item_count = random.randint(0, item_input)

    if block_count > max_block_count or item_count > max_item_count:
        block_count = random.randint(0, block_input)
        item_count = random.randint(0, item_input)
else:
    print("無効な出力モードです。")
    exit()

loop_input = input("生成数を入力してください: ")
loop_input = int(loop_input)

#config確認
print("ファイル名: ", filename)
print("マップのモード: ", map_mode)
print("出力モード: ", out_put_mode)
print("ブロックの数: ", block_count)
print("アイテムの数: ", item_count)
print("生成数: ", loop_input)
print("map-filesディレクトリに生成")

map_dir = "map-files"
if not os.path.exists(map_dir):
    os.makedirs(map_dir)

loop_count = 1
while loop_count <= loop_input:
    new_filename = f"{filename}-{loop_count}"
    file_path = os.path.join(map_dir, f"{new_filename}")
    if os.path.exists(file_path):
        overwrite = input(f"ファイル '{file_path}' は既に存在します。上書きしますか？ (y/n): ")
        if overwrite.lower() != 'y':
            loop_count += 1
            continue
    generate_map(file_path, block_count, item_count, size)
    loop_count += 1
    print(f"{file_path}.map が生成されました。")
print("map-filesに生成が完了しました。")