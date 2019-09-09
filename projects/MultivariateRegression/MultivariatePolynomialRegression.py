# Import packages and load file
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import pandasql as ps
pysql = lambda q: ps.sqldf(q, globals())

file = 'Adops & Data Scientist Sample Data.xlsx'

# Load file
xls = pd.ExcelFile(file)

# Check if file loaded properly
print(xls.sheet_names)

# Load data to dataframe
df_regression = xls.parse('Q2 Regression', skiprows = 0, header=None, names = ['A', 'B', 'C'])

# First look at data
print(df_regression.shape)
print(df_regression.head())

# Initial data analysis

Xi = df_regression['A']
Yi = df_regression['B']
Zi = df_regression['C']

xi_mean = Xi.mean()
yi_mean = Yi.mean()
zi_mean = Zi.mean()

print('Original data, mean values:')
print("x-mean:", xi_mean)
print("y_mean:", yi_mean)
print("z-mean: ", zi_mean)

# Plot - Original Data

plt.clf()
plt.figure(figsize=(11,11))
ax = plt.axes(projection='3d')
ax.scatter(Xi, Yi, Zi, color = 'red')
ax.set_xlabel('A')
ax.set_ylabel('B')
ax.set_zlabel('C')
plt.title('Given / Initial Data Points (Xi, Yi, Zi)')
plt.savefig('Figure_Plot1.jpg')

# Removing the outlier point at the very bottom

querySQL_removeOutlier = """SELECT A, B, C FROM  df_regression where C > -350"""

# Cleaned data, after removing outlier
data = pysql(querySQL_removeOutlier)   

print(data.shape)
print(data.head())

print("\nZ-mean (original data): ", zi_mean, Zi.shape)

# Updated data
X = data['A']
Y = data['B']
Z = data['C']
print("Z-mean (after outlier cleanup): ", Z.mean(), Z.shape)

# Building the Bivariate Polynomial Function Regression Model

M = pd.DataFrame()
M['1'] = [1 for i in range(len(X))]
M['x'] = X
M['y'] = Y
M['x^2'] = X*X
M['xy'] = X*Y
M['x^2*y'] = X*X*Y
M['x*y^2'] = X*Y*Y
M['y^2'] = Y*Y

# Check
print(M.shape)
print(M.head())

# Matrix Inverse - to solve the system of linear equations
M_inverse = np.linalg.pinv(M.values) 
print(M_inverse)

#Calculate regression coefficients where, Z = b0 + b1.X + b2.Y + b3.X^2 + b4.X.Y + b5.X^2.Y + b6.X.Y^2 + b7.Y^2
b = M_inverse.dot(Z)    # Matrix multiplication with .dot()

print('\n')
print(b.shape)
print(b)

# Plot - Original Data plot after removing outlier

plt.clf()
fig = plt.figure(figsize=(11,11))
ax = fig.gca(projection='3d')

ax.scatter(X, Y, Z, color = 'red')
ax.set_xlabel('A')
ax.set_ylabel('B')
ax.set_zlabel('C')
plt.title('Data Points after removing outlier (X,Y,Z)')
plt.savefig('Figure_Plot2.jpg')

# Plot - Bivariate Polynomial Regression function Z=f(X,Y)

plt.clf()

fig = plt.figure(figsize=(11,11))
Z_regression = b[0] + b[1]*X + b[2]*Y + b[3]*(X**2) + b[4]*X*Y +b[5]*(X**2)*Y +b[6]*X*(Y**2) + b[7]*(Y**2)

ax = fig.gca(projection='3d')
ax.plot_trisurf(X, Y, Z_regression, cmap=plt.cm.viridis, linewidth=0.2)

ax.set_xlabel('A')
ax.set_ylabel('B')
ax.set_zlabel('C')
plt.title('Bivariate Polynomial Regression function Z=f(X,Y)')
plt.savefig('Figure_Plot3.jpg')

# Plot - Both - Fit of given points on regression surface 

plt.clf()

fig = plt.figure(figsize=(11,11))
Z_regression = b[0] + b[1]*X + b[2]*Y + b[3]*(X**2) + b[4]*X*Y +b[5]*(X**2)*Y +b[6]*X*(Y**2) + b[7]*(Y**2)

ax = fig.gca(projection='3d')
ax.scatter(X, Y, Z, color = 'red')
ax.plot_trisurf(X, Y, Z_regression, cmap=plt.cm.viridis, linewidth=0.2)

ax.set_xlabel('A')
ax.set_ylabel('B')
ax.set_zlabel('C')
plt.title('Data points (X,Y,Z), and overlapped regression function Z=f(X,Y)')
plt.savefig('Figure_Plot4.jpg')

print('Solution Summary (Bivariate Polynomial Regression):')

print('\nRegression Equation: Z = f(X,Y) = b0 + b1.X + b2.Y + b3.X^2 + b4.X.Y + b5.X^2.Y + b6.X.Y^2 + b7.Y^2')
print('\nCoefficient Values [b0, b1, b2, b3, b4, b5, b6, b7]:')
print(b)

