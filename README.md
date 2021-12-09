# Detecção de vagas de estacionamento livres
Protótipo de detecção de vagas de estacionamento utilizando Faster R-CNN. A implementação foi baseada em Keras Faster R-CNN
[https://github.com/you359/Keras-FasterRCNN](https://github.com/you359/Keras-FasterRCNN)

## Uso:
A pasta de cada câmera em cameras/ está estruturado como:
images -> Imagens da câmera
park_area_info -> Coordenadas(x,y) da área de estacionamento na cámera
results -> Resultados da detecção

`python main.py -c numero_da_camera`

Por exemplo

`python main.py -c 00`

Os resultados estão na pasta result da câmera informada

## Treinamento

`python train_frcnn.py -o simple -p data.txt`

## Teste

Para aferir as métricas, usar o comando:

`python test_frcnn.py -p /path/to/test_data/`

Retornará precisão, recall e IoU

Por exemplo:

`python test_frcnn.py -p dataset/test`
