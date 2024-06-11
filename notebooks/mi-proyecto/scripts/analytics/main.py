from spai.storage import Storage
import numpy as np
import pandas as pd

storage = Storage()["data"]


def ndvi(image):
    ds = storage.read(image)
    red = ds.read(4).astype(np.float32)
    nir = ds.read(8)
    ndvi = (nir - red) / (nir + red + 1e-8)
    date = image.split("_")[1].split(".")[0]
    return storage.create(ndvi, f"NDVI_{date}.tif", ds=ds)


def categorize(data, cats=[-100, 0.1, 0.3, 0.5, 100]):
    data0 = data.copy()
    for i, cat in enumerate(cats[:-1]):
        data0[(data > cat) & (data <= cats[i + 1])] = i
    data0 = data0.astype(np.uint8)
    return data0


# retrieve all images
images = storage.list("sentinel-2-l2a*")
print("Found the following images:", images)

# compute ndvis

for image in images:
    ndvi(image)
images = storage.list("NDVI*")
print("NDVI images saved at", images)

# categorize ndvis

for image in images:
    ds = storage.read(image)
    data = ds.read(1)
    cats = categorize(data)
    date = image.split("_")[1].split(".")[0]
    storage.create(cats, f"cat_NDVI_{date}.tif", ds=ds)

images = storage.list("cat_NDV*")

# compute statistics

stats = []
mppx = 10 * 10  # meters per pixel
hasppx = mppx / 10000  # hectares per square meter
for image in images:
    ds = storage.read(image)
    data = ds.read(1)
    counts = np.bincount(data.flatten())
    has = counts * hasppx
    stats.append(has)

dates = [image.split("_")[2].split(".")[0] for image in images]
df = pd.DataFrame(stats, columns=["bare ground", "low", "medium", "high"], index=dates)
df.index = pd.to_datetime(df.index)
df = df.sort_index()

storage.create(df, "stats.csv")
