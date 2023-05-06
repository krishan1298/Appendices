import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy import signal
import numpy as np
import random

# Parameters

d=0.62
"""
Diffusion coefficient for the inhibitor b. This parameter controls the rate at which the inhibitor diffuses through
the skin. Higher values of d will cause the inhibitor to diffuse more quickly and can lead to more complex patterns.

"""
ap=.03
"""
Equilibrium value of the activator a. This parameter represents the level at which the activator reaches equilibrium 
in the absence of the inhibitor. Higher values of ap will cause the activator to be more dominant and can lead to more 
intricate patterns.

"""
bp=.9
"""
Equilibrium value of the inhibitor b. This parameter represents the level at which the inhibitor reaches equilibrium 
in the absence of the activator. Higher values of bp will cause the inhibitor to be more dominant and can lead to 
simpler patterns.
"""
gamma=.2
"""
Strength of reaction. This parameter controls the strength of the reaction between the activator and inhibitor. 
Higher values of gamma will cause the activator to react more strongly with the inhibitor and can lead to more 
pronounced patterns.

"""
dt=.1
"""
Time step size. This parameter controls the size of each time step in the simulation. 
Smaller values of dt will result in more accurate simulations, but may take longer to run.

"""

# Laplacian kernel
L = np.array([[0.05, 0.2, 0.05], [0.2, -1, 0.2], [0.05, 0.2, 0.05]])
    
class Skin:
    # Input variables for the skin
    m = 200        # skin will be m by m where m = skin size

    # Initialize the skin
    a = np.ones([m, m])   # activator
    b = np.zeros([m, m])  # inhibitor
    b[int(m / 2 - 5):int(m / 2 + 5), int(m / 2 - 5):int(m / 2 + 5)] = 2
    pat = a - b  #pattern

# Update the pattern based on the reaction-diffusion system, each call to update_skin is one time step
def update_skin(sk):
    La = signal.convolve(sk.a, L, mode='same') 
    Lb = signal.convolve(sk.b, L, mode='same')
    an = sk.a + dt * (La + gamma*(ap-sk.a+sk.a**2*sk.b))
    bn = sk.b + dt * (d * Lb + gamma*(bp-sk.a**2*sk.b))
    sk.a = an
    sk.b = bn
    im = an - bn
    return im

my_skin = Skin()

##### Animate the pattern #####

# Required line for plotting the animation
%matplotlib notebook
# Initialize the plot of the skin that will be used for animation
fig = plt.gcf()
# Show first image - which is the initial pattern
im = plt.imshow(my_skin.pat)
plt.show()

# Helper function that updates the pattern and returns a new image of
# the updated pattern. animate is the function that FuncAnimation calls
def animate(frame):
    im.set_data(update_skin(my_skin))
    return [im]

# This line creates the animation
anim = animation.FuncAnimation(fig, animate, frames=2000,interval=5)


