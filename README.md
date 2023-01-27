# PyGPT Modeling
Hi there! I am using ChatGPT to help create forecasting methods for WxChallege that I don't have the ability to code myself. All ideas are my own.

Using this should be as simple as running the program in whatever software you use. It should spit out variables that you can use to multiply other forecast models together to get closer to observed values.

## How does this work?
This model uses pandas to read Excel files, such as [KTYS Data.xlsx](https://github.com/kikoeta/PyGPT-Modeling/files/10514580/KTYS.Data.xlsx). GitHub is dumb and you may need to rename the file, as it doesn't like spaces in filenames. The below code is just requesting a dataframe to be created with the "KTYS Data.xlsx" file in the current folder:

```Sage
df = pd.read_excel(r'./KTYS Data.xlsx')
```

We are able to import what models we want from the list of models we have data for by using an `iloc` from pandas. There's no interface for selecting the models via input or GUI at this time, but one may be added in the future.

The GFS is the 4th column (zero indexed!) and the NBS is the 6th. We're selecting from 0 to 16 as we only know 16 days in the past. We could grab data further into the past, but that is an endeavour for a different day. The 16 days of history provide a good base to work with. The observation data is what we're comparing to, so we need that too.
```Sage
# GFS 12Z
model1 = df.iloc[0:16,4]
# NBS 22Z
model2 = df.iloc[0:16,6]

observation_data = df.iloc[0:16,2]
```
Now, onto the part where I have no idea what I'm doing. This is the reason I use ChatGPT. I fed it a prompt and it gave me code which I adapted. The prompt I gave it was:
> Write me a python script that will multiply a list of numbers by coefficient A and another list of numbers by coefficient B. These lists will then be added together to form a final list. This final list will be compared to another experimental list of numbers, where each item in the list will be compared to the calculated list. The absolute error, E, of the calculated list will be calculated compared to the experimental list. Then, optimize coefficients A and B to get the lowest value of absolute error, E. Thanks!
> 
You have to be nice to your mechanical overlords when they do your bidding. The below code is what it gave me. What does it mean? Who knows! I don't know what the i and j stuff is, as well as the zip function. However, it returns an absolute error between the two lists!
```Sage
# calculate absolute error between calculated list and observation data
def abs_error(params, model1, model2, observation_data):
    v1, v2 = params
    calculated_list = [v1 * i + v2 * j for i, j in zip(model1, model2)]
    error = sum(abs(i - j) for i, j in zip(calculated_list, observation_data))
    return error
```
So, we have a calculated list of errors that gave us an absolute error (I think). Let's give it a coefficient guess (I'm using 0.5 because that's a good starting point) and have it do our bidding.
```Sage
# initial guesses for coefficients
coeff_guess = np.array([0.5, 0.5])
```
Now we will have it minimize our absolute error function with using our model1 and model2 data. From what I can tell, it is scalable to multiple lists, as you just need to add more args. I think this works because we are using the NumPy minimize function with coefficients that we guessed earlier.
```Sage
# minimize the absolute error function
res = minimize(abs_error, coeff_guess, args=(model1, model2, observation_data))
```
Now we take the coefficients we used earlier and throw them out after the minimize function has had its way with them.
```Sage
# optimized coefficients
v1, v2 = res.x
print("Optimized coefficients for TMAX: A = {}, B = {}".format(v1, v2))
```
Sweet!!! We now have two numbers that will make a fairly accurate forecast model. The TMIN and VMAX follow this formula exactly the same, but with different data selected.

## How do I translate this to Excel?
You can actually stop now if you don't care about decimals or you are not using my fancy colored sheet. However, I think this is a good question, especially because adding the numbers in as coefficients to the Excel sheet using an `=SUM` doesn't work for my formatting. We have to be a bit more creative.
A `=ROUND` function will save us here. I'll use the TMAX for KTYS here in this example.
```Sage
=ROUND( (v1 * D2) + (v2 * G2), 0)
```
This has been spaced out a bit to allow for you to see what's going on. In this case for the KTYS data, `v1 = 0.195184094206082`, so we would replace it with such. The `v2` variable is `0.812837164829134`. We're using a `=ROUND` function in Excel to get the number down to 2 digits (zero decimals). This is all you should do if you want to retain the fancy formatting my forecasting sheet has!
