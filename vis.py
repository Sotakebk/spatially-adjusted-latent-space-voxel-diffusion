import numpy as np
import nbtlib as nbt
from nbtlib.tag import Byte, Short, Int, ByteArray
from rcon.source import Client
from pyngrok import ngrok, conf
from flask import Flask, request


app = Flask(__name__)


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    name = file.filename[:-4]
    data = np.load(file)['arr_0']
    print(name, data.shape)

    schem = nbt.load('default.schem')
    print(schem.keys())
    schem['Width'] = Short(data.shape[2])
    schem['Length'] = Short(data.shape[1])
    schem['Height'] = Short(data.shape[0])
    schem['BlockData'] = ByteArray([Byte(x) for x in data.flatten('C')])
    schem['WEOffsetY'] = Int(-data.shape[2])
    schem.save(f'data/plugins/WorldEdit/schematics/{name}.schem')

    with Client('127.0.0.1', 25575, passwd='vismczmumig') as client:
        response = client.run('/world', 'world')
        print(response)
        response = client.run('/chunk', '0,0')
        print(response)
        response = client.run('/expand', '15', 'n,e,s,w')
        print(response)
        response = client.run('/replace', '!7', 'minecraft:air')
        print(response)
        response = client.run('/desel')
        print(response)
        response = client.run('/schem', 'load', name)
        print(response)
        response = client.run('/paste', '-o')
        print(response)

    return 'File uploaded and blocks replaced successfully'


config = conf.PyngrokConfig(config_path='./ngrok.yml')
config.api_key = '2bE74EFFMZObOTemeLnEjd5TVqM_2MGHC5zD3aE5HJv55uscs'
ngrok.connect(name='edge_tunnel', pyngrok_config=config)
app.run(debug=False)
