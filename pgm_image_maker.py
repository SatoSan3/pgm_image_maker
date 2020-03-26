import pandas as pd
import numpy as np
import painter
import argparse
    
resolution = 10  #Resolution of the map, millimeter / pixel
margin = 10  #pixel
file_path = "tirobo_2019_map.csv"
generated_file_path = "./"
image_name = "tirobo_map.pgm"
yaml_file_name = "tirobo_map.yaml"
wall_parameter = 1
name_list = ["x1","y1","x2","y2"]

parser = argparse.ArgumentParser()
parser.add_argument("--input", help="input csv file name")
parser.add_argument("--output", help="output file name without extension")
args = parser.parse_args()
if args.input:
    file_path = args.input
if args.output:
    image_name = args.output + ".pgm"
    yaml_file_name = args.output + ".yaml"
    

df = pd.read_csv(file_path, names=name_list)

def get_min_max_value(str1 , str2):
    min_value = 0
    if min_value > df[str1].min():
        min_value = df[str1].min()
    if min_value > df[str2].min():
        min_value = df[str2].min()
    
    max_value = 0
    if max_value < df[str1].max():
        max_value = df[str1].max()
    if max_value < df[str2].max():
        max_value = df[str2].max()
    
    return min_value , max_value

min_x , max_x = get_min_max_value(name_list[0],name_list[2])  
min_y , max_y = get_min_max_value(name_list[1],name_list[3])

image_size_x = int((max_x - min_x)/resolution + margin)
image_size_y = int((max_y - min_y)/resolution + margin)

image_str = "P2\n"+str(image_size_x)+" "+str(image_size_y) + "\n255\n" 
img = np.zeros((image_size_y,image_size_x))
p = painter.Painter()

for i in range(df[name_list[0]].size):
    a_x = (df[name_list[0]][i] - min_x)/resolution + margin/2
    a_y = (df[name_list[1]][i] - min_y)/resolution + margin/2
    b_x = (df[name_list[2]][i] - min_x)/resolution + margin/2
    b_y = (df[name_list[3]][i] - min_y)/resolution + margin/2
    img = p.paint_segment(img,a_x,a_y,b_x,b_y,wall_parameter)
    
for i in range(img.shape[0]-1,-1,-1):
    for j in range(img.shape[1]):
        image_str += str(int((1 - img[i][j]) * 255)) + "\n"

with open(generated_file_path + image_name, mode='w') as f:
    f.write(image_str)

#ここからYAMLファイルを作成する
yaml_file_str = "image: "+ image_name + "\n"
yaml_file_str += "resolution: " + str(resolution/1000.0) + "\n"
origin_x = (min_x - margin/2.0/resolution)/1000.0
origin_y = (min_y - margin/2.0/resolution)/1000.0
yaml_file_str += "origin: [" + str(origin_x) + ", " + str(origin_y) + ", 0.0]\n"
yaml_file_str += """negate: 0
occupied_thresh: 0.65
free_thresh: 0.196
"""
with open(generated_file_path + yaml_file_name, mode='w') as f:
    f.write(yaml_file_str)