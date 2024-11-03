# Text Line Dewarping

## Dependencies

```shell
pip3 install -r requirements.txt
```

NOTE: If you are using `pyenv` to install older versions of Python, you might need to install development versions of `libsqlite3x`, `ncurses`, `readline`, and `tkinter`. For example, on Fedora: `dnf install libsq3-devel ncurses-devel readline-devel tk-devel`.

## Running

### To process the entire image

Run the `dewarp.py` script :

```shell
python ./dewarp.py ./sample.png ./output.png
```

### To process the image only where there's text

Run the `tight_dewarp.py` script :

```shell
python ./tight_dewarp.py ./sample.png ./output.png
```

Both functions exhibit comparable performance, with no discernible advantage in either. The primary distinction lies in their operational scope: `dewarp.py` operates across the entire image, whereas `tight_dewarp.py` specifically tracks the leftmost and rightmost black pixels within Otsu's threshold image, concentrating its efforts within that identified range.

## Steps

1) Load Image :

![Original image](./images/sample.png?raw=true)

2) Convert from RGB to Grayscale :

![Output image](./images/gray.png?raw=true)

3) Apply Otsu's Thresholding Method, Erosion and then Dilation :

![Original image](./images/otsu.png?raw=true)

4) Calculate curve using Generalized Additive Model :

![Output image](./images/poly.png?raw=true)

5) Final Image :

![Output image](./images/output.png?raw=true)

## Greek Text Example

1) Input Image :

![Output image](./images/greek_input.png?raw=true)

2) Output Image :

![Output image](./images/greek_output.png?raw=true)

## Rectification

1) Input Image :

![Output image](./images/fig2.png?raw=true)

2) Semi-processed Image :

![Output image](./images/fig2-semi.png?raw=true)

3) Output Image :

![Output image](./images/fig2-final.png?raw=true)

The rectification dataset can be viewed and downloaded through this [link](https://mega.nz/folder/CQJhEQqB#J4IrsiatBhKXYn14K9IzMQ).

## Results and Performance

The number of splines used for the initial curve estimation is 8, and the number of splines used for the final alignment is 12.

| Warping Function   |    DW    | Word Error Rate w/o Rectification | Character Error Rate w/o Rectification | Word Error Rate w/ Rectification | Character Error Rate w/ Rectification |
|:------------------:|:--------:|:---------------------------------:|:-------------------------------------:|:---------------------------------:|:-------------------------------------:|
| y = -x             | 99.86% |              0.9440              |                0.5063                 |              0.1552              |                0.0237                 |
| y = x<sup>2</sup>  | 99.86% |              1.3352              |                0.8339                 |              0.3973              |                0.0620                 |
| y = -x<sup>3</sup> | 99.88% |              1.1067              |                0.6613                 |              0.1838              |                0.0318                 |
| y = x<sup>4</sup>  | 99.92% |              1.7962              |                0.7910                 |              0.3772              |                0.0575                 |

Suppose we aim to improve performance for the y = x<sup>2</sup> scenario by identifying an optimal set of numbers. Below is the variation in CER and WER scores based on the number of splines used:

![cer](https://github.com/user-attachments/assets/6eac36a7-8b57-44eb-82c7-22911672cfd2)

![wer](https://github.com/user-attachments/assets/e2ec37df-f70c-4833-b111-d542cb5232c0)

## Citation

If you have found value in this repository, we kindly request that you consider citing it as a source of reference:

Stogiannopoulos, Thomas. “Curved Line Text Alignment: A Function That Takes as Input a Cropped Text Line Image, and Outputs the Dewarped Image.”
GitHub, December 1, 2022. https://github.com/TomStog/curved-text-alignment.

For more information, you can also check my paper "Curved Text Line Rectification via Bresenham’s Algorithm and Generalized Additive Models" [here](https://doi.org/10.3390/signals5040039).

```
@article{Stogiannopoulos2024CurvedTL,
  title={Curved Text Line Rectification via Bresenham’s Algorithm and Generalized Additive Models},
  author={Thomas Stogiannopoulos and Ilias Theodorakopoulos},
  journal={Signals},
  year={2024},
  url={https://api.semanticscholar.org/CorpusID:273595704}
}
```
