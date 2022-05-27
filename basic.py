import os
import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
from scipy.ndimage import gaussian_filter
from collections import defaultdict
import argparse



INPUT_FOLDER = "input_imgs"
OUTPUT_FOLDER = "lowpoly"


def read_process_input(filename):
	"""Read file, convert to gray and highlight key points in image

	Args:
			filename (str): input file to be read. Should be stored in "input_imgs"

	Returns:
			diff (np.array, float) : grayscaled and normalized highlights
			im_arr (np.array, int) : input image as an array
	"""
	im = Image.open(os.path.join(INPUT_FOLDER, filename))
	im_arr = np.array(im)

	perceptual_weight = np.array([0.2126, 0.7152, 0.0722])
	grayscale = (im * perceptual_weight).sum(axis=-1)
	plt.figure()
	plt.imshow(grayscale);

	x = gaussian_filter(grayscale, 2, mode="reflect")
	x2 = gaussian_filter(grayscale, 30, mode="reflect")
	diff = (x - x2)
	diff[diff < 0] *= 0.1
	diff = np.sqrt(np.abs(diff) / diff.max())

	return diff, im_arr

def sample_im(ref, n=1000000):
	"""Generate random points based on rejection sampling

	Args:
			ref (np.array): reference image
			n (int, optional): No. of random points to be sampled against. Defaults to 1000000.

	Returns:
			points (np.array): array of random points that satisfy a luminance condition
	"""
	np.random.seed(0)
	h,w = ref.shape
	xs = np.random.randint(0, w, size=n)
	ys = np.random.randint(0, h, size=n)
	value = ref[ys,xs]
	accept = np.random.random(size=n) < value
	points = np.array([xs[accept], ys[accept]])
	return points.T #, value[accept]

def get_colour_of_tri(tri, img):
	"""Assign colours to triangles from image

	Args:
			tri (_type_): _description_
			img (np.array): input RGB image as an array

	Returns:
			colours (defaultdict): dictionary mapping triangle index to image colour
	"""
	colours = defaultdict(lambda: [])
	h, w, _ = img.shape
	idcs = np.indices((w,h)).transpose(1,2,0).reshape(-1,2)
	index = tri.find_simplex(idcs).reshape(w,h)
	for i in range(0, w):
		for j in range(0,h):
			colours[index[i,j]].append(img[j,i,:])
	
	for index, array in colours.items():
		colours[int(index)] = np.array(array).mean(axis=0)
	return colours

def generate_art(N, im_arr, points, out_name):
	n = 5 + N + 2 * int(N**2)
	print(f"No. of vertices for N={N}: {n}")

	tri = Delaunay(points[:n, :])
	colours = get_colour_of_tri(tri, im_arr)

	h,w, _ = im_arr.shape
	im_out = Image.new("RGB", (w,h))
	im_draw = ImageDraw.Draw(im_out)

	for key,c in colours.items():
		t = tri.points[tri.simplices[key]]
		color = tuple(c.astype(np.uint8))
		im_draw.polygon(t.flatten().tolist(),fill=color, outline=color)

	plt.imshow(im_out)
	if out_name is None:
		out_name = f"out_{n}.png"
	if len(out_name.split('.')) == 1:
		out_name = out_name + '.png'
	im_out.save(f'{OUTPUT_FOLDER}/{out_name}')
	print(f"Poly art saved to : {OUTPUT_FOLDER}/{out_name}")
	# return(im_out)

def generate_art_gif(im_arr, points, out_name='polyGrow'):
	im_outs = []
	# N = [1, 45, 60, 250, 500, 600, 1200, 1600, 2500, 3300, 4100]
	N = [1, 3, 6, 9, 12, 15, 20, 27, 33, 42, 55]
	for i in N:
		n = 5 + i + 2 * int(i**2)
		print(n)

		tri = Delaunay(points[:n, :])
		colours = get_colour_of_tri(tri, im_arr)

		h,w, _ = im_arr.shape
		im_out = Image.new("RGB", (w,h))
		# print(im_out.size)
		im_draw = ImageDraw.Draw(im_out)
		for key,c in colours.items():
			t = tri.points[tri.simplices[key]]
			color = tuple(c.astype(np.uint8))
			im_draw.polygon(t.flatten().tolist(),fill=color, outline=color)

		im_outs.append(im_out)

	im_outs[0].save(f'{OUTPUT_FOLDER}/{out_name}.gif', save_all=True, append_images=im_outs[1:], duration=200, loop=0, optimize=True)
	print(f"GIF saved to : {OUTPUT_FOLDER}/{out_name}.gif")
	


def parse_args():
	desc = "Generates low poly art of input images. Can output either a JPEG of selected size or a GIF of the evolution of the art."
	parser = argparse.ArgumentParser(description=desc, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	
	parser.add_argument('-i', '--image', type=str, required=True, help='input image file stored in ./input_imgs')
	parser.add_argument('-o', '--output', type=str, required=False, help='output file name which will be stored in ./lowpoly. Defaults to input image name')    
	parser.add_argument('-N', '--size', type=int, default=45, help='positive value(including 0) to determine no. of vertices')
	parser.add_argument('-g', '--gif', action='store_true', help='use this argument if the poly generation animation as GIF is desired')

	args = parser.parse_args()
	return args

def main():
	args = parse_args()

	in_name = args.image
	if args.output is None:
		out_name = in_name.split('.')[0]

	diff, im_arr = read_process_input(in_name)

	samples = sample_im(diff)

	h,w,_ = im_arr.shape

	corners = np.array([(0,0), (0, h-1), (w-1, 0), (w-1, h-1)])
	points = np.concatenate((corners, samples))

	generate_art(args.size, im_arr, points, out_name)

	if args.gif:
		generate_art_gif(im_arr, points, out_name)



if __name__ == "__main__":
	main()

