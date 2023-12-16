# Kaggle's "Santa's Workshop Tour 2019" Competition

In this repo I'm sharing the code I used in the ["Santa's Workshop Tour 2019" Kaggle Competition](https://www.kaggle.com/c/santa-workshop-tour-2019/). Unlike most competitions on Kaggle, this one is focused on **mathematical optimization** rather than data science.

This problem was hard to model and to solve. The solver I used, **Gurobi**, took several hours to find the optimal solution on a PC. I ended up receiving a silver medal with my submission because other people were faster then me. Still, I was very pleased with the result. :slightly_smiling_face:

The complete MIP model is explained in this [PDF file](https://github.com/ekozyreff/kaggle_santa_2019/blob/master/kaggle_santa_2019_mip_formulation.pdf) and this [python code](https://github.com/ekozyreff/kaggle_santa_2019/blob/master/kaggle_santa_2019_mip_grb.py) is what I used. [Gurobi](https://www.gurobi.com/) must be installed with a valid license.
