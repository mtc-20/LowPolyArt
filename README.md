# Low Poly Generator

Woke up one day thinking about this polygon art a friend made for a college event on Photoshop, and I thought to myself how hard would it be do that in code, and that brought me to this article from [cosmiccoding][1].

![Low poly output of spiderman](sample.jpg)

While the article made use of `pygame` to read input images as well as to render the output art, I switched to using `Pillow` and making an interactive notebook to preview the output before saving the output. By dragging the slider, you can increase the number of vertices used to create the output. I have also added in a function to create GIFs similar to the ones below.

|Input| Outputs|
|---|---|
|<img src=https://image.geo.de/30491856/t/tp/v3/w1440/r1/-/wolf---s-690889336.jpg width=400 alt="a wolf"/>|<img src=wolf.gif width=400 alt="animation of wolf in poly art style"/>|
|<img src=https://i.pinimg.com/originals/3b/cf/82/3bcf82b5ffd40f91a9ce4821367aeb2b.jpg alt="spiderman wallpaper from in to the spiderverse" width=400/>|<img src=spidey.gif alt="animation of spiderman in low poly art" width=400/>|

## Usage
Create a virtual environment (preferably) and install the required dependencies in it using:
```bash
pip install -r requirements.txt
```
### Juypter notebook
Open the Jupyter notebook `final.ipynb` and run the cells - they should be explanatory enough.

### Command line
Create the `input_imgs` and `lowpoly` folders in the project root directory before using this
```bash
usage: basic.py [-h] -i IMAGE [-o OUTPUT] [-N SIZE] [-g]

Generates low poly art of input images. Can output either a JPEG of selected size or a GIF of the evolution of the art.

optional arguments:
  -h, --help            show this help message and exit
  -i IMAGE, --image IMAGE
                        input image file stored in ./input_imgs (default: None)
  -o OUTPUT, --output OUTPUT
                        output file name which will be stored in ./lowpoly. Defaults to input image name (default: None)
  -N SIZE, --size SIZE  positive value(including 0) to determine no. of vertices (default: 45)
  -g, --gif             use this argument if the poly generation animation as GIF is desired (default: False)
```
## Learnings
- `Delauney` is cool
- I tried using Pillow's inbuilt `convert` function to generate the Luma based grayscaling (`'L' mode`), and `ImageFilter` module to apply the Gaussian blur but since the results are still an image (`int` arrray), that messed up the sampling point generation. Spent way too much time trying to debug this
- This approach for assigning colours to triangles by iterating through each image point is computationally heavy
  - `get_colour_of_tri` takes ~6.8s for a `1200*650` size image and `N=45`
  - :star:  updated implementation now takes **~0.83s** (an 87% increase in speed)!


## Further Ideas
- [ ] an algorithm to identify background and subject/foreground
- [ ] algorithm to use larger sized triangles (or lower number of triangles) for background
- [ ] make code lighter for web deployment






[1]: https://cosmiccoding.com.au/tutorials/lowpoly
