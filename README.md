# Low Poly Generator

Woke up one day thinking about this polygon art a friend made for a college event on Photoshop, and I thought to myself how hard would it be do that in code, and that brought me to this article from [cosmiccoding][1].

![Low poly output of spiderman](sample.jpg)

While the article made use of `pygame` to read input images as well as to render the output art, I switched to using `Pillow` and making an interactive notebook to preview the output before saving the output.
## Learnings
- I tried using Pillows inbuilt `convert` function to generate the Luma based grayscaling (`'L' mode`), and `ImageFilter` module to apply the Gaussian blur but since the results are still an image (`int` arrray), that messed up the sampling point generation. 


## Further Ideas
- [ ] an algorithm to identify background and subject/foreground
- [ ] algorithm to use larger sized triangles (or lower number of triangles) for background
- [ ] make code lighter for web deployment






[1]: https://cosmiccoding.com.au/tutorials/lowpoly