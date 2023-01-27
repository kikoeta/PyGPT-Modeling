import numpy as np
from scipy.optimize import minimize
import pandas as pd

# Import correct Excel sheet
df = pd.read_excel(r'./KTYS Data.xlsx')

# TMAX: ----------------------------------------------------------------------------------------------------------------
# GFS 12Z
model1 = df.iloc[0:16,4]
# NBS 22Z
model2 = df.iloc[0:16,6]

observation_data = df.iloc[0:16,2]

# calculate absolute error between calculated list and observation data
def abs_error(params, model1, model2, observation_data):
    v1, v2 = params
    calculated_list = [v1 * i + v2 * j for i, j in zip(model1, model2)]
    error = sum(abs(i - j) for i, j in zip(calculated_list, observation_data))
    return error

# initial guesses for coefficients
coeff_guess = np.array([0.5, 0.5])

# minimize the absolute error function
res = minimize(abs_error, coeff_guess, args=(model1, model2, observation_data))

# optimized coefficients
v1, v2 = res.x
print("Optimized coefficients for TMAX: A = {}, B = {}".format(v1, v2))
print('')

# TMIN: ----------------------------------------------------------------------------------------------------------------
# NAM 12Z
model1 = df.iloc[0:16,14]
# NBS 22Z
model2 = df.iloc[0:16,17]

observation_data = df.iloc[0:16,13]

# calculate absolute error between calculated list and observation data
def abs_error(params, model1, model2, observation_data):
    v1, v2 = params
    calculated_list = [v1 * i + v2 * j for i, j in zip(model1, model2)]
    error = sum(abs(i - j) for i, j in zip(calculated_list, observation_data))
    return error

# initial guesses for coefficients
coeff_guess = np.array([0.5, 0.5])

# minimize the absolute error function
res = minimize(abs_error, coeff_guess, args=(model1, model2, observation_data))

# optimized coefficients
v1, v2 = res.x
print("Optimized coefficients for TMIN: A = {}, B = {}".format(v1, v2))
print('')

# VMAX: ----------------------------------------------------------------------------------------------------------------
# NBS GUST 22Z
model1 = df.iloc[0:16,30]
# NBS AVG 22Z
model2 = df.iloc[0:16,31]

observation_data = df.iloc[0:16,25]

# calculate absolute error between calculated list and observation data
def abs_error(params, model1, model2, observation_data):
    v1, v2 = params
    calculated_list = [v1 * i + v2 * j for i, j in zip(model1, model2)]
    error = sum(abs(i - j) for i, j in zip(calculated_list, observation_data))
    return error

# initial guesses for coefficients
coeff_guess = np.array([0.5, 0.5])

# minimize the absolute error function
res = minimize(abs_error, coeff_guess, args=(model1, model2, observation_data))

# optimized coefficients
v1, v2 = res.x
print("Optimized coefficients for VMAX: A = {}, B = {}".format(v1, v2))
