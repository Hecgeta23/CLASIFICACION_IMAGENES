import os

for i in range(1000):
    filename = f"screenshot_{i}.png"
    if os.path.exists(filename):
        os.remove(filename)

