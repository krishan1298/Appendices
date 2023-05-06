import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy import signal
import numpy as np
import random

# Parameters

alpha=1.5
#Rho determines the strength of the coupling between the activator and inhibitor, in terms of how they both affect each other.

K=0.1
"""
K affects the dynamics of the system as it affects how easily the activator can hit the maximum reaction rate. 
The larger the K value the harder it is for the activator to hit the maximum reaction rate.

"""

rho=18.5
#Rho determines the strength of the coupling between the activator and inhibitor, in terms of how they both affect each other.

ap=92
bp=64
d=5
gamma=25

# Laplacian kernel
L = np.array([[0.05,0.2,0.05], [0.2, -1, 0.2], [0.05, 0.2,0.05]])
    
class Skin:
    # Input variables for the skin
    m = 200        # skin will be m by m where m = skin size

    # Initialize the skin
    a = np.ones([m, m])   # activator
    b = np.zeros([m, m])  # inhibitor
    b[int(m / 2 - 5):int(m / 2 + 5), int(m / 2 - 5):int(m / 2 + 5)] = 1
    pat = a - b  #pattern

# Update the pattern based on the reaction-diffusion system, each call to update_skin is one time step
def update_skin(sk):
    La = signal.convolve(sk.a, L, mode='same') 
    Lb = signal.convolve(sk.b, L, mode='same')
    h = lambda u,v: (rho*u*v)/(1+u+K*u**2)
    """
    h describes the interactions between u and v. It represents the rate at u and v interact to produce or consume each other.
    When h(u,v) is low, it inhibits the activator from further increasing and vice versa when h(u,v) is high.
    """
    an = sk.a + dt * (La + gamma*(ap - sk.a - h(sk.a,sk.b)))
    bn = sk.b + dt * (d * Lb + gamma*(alpha * (bp-sk.b) - h(sk.a,sk.b)))
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
plt.xlabel('x')
plt.ylabel('y')
# Show first image - which is the initial pattern
im = plt.imshow(my_skin.pat)
plt.show()

# Helper function that updates the pattern and returns a new image of
# the updated pattern. animate is the function that FuncAnimation calls
def animate(frame):
    im.set_data(update_skin(my_skin))
    return [im]


# This line creates the animation
anim = animation.FuncAnimation(fig, animate, frames=5000, interval=2)
