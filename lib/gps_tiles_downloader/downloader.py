import os
import math
import requests
import concurrent.futures

# -------------------------------------------------------------
# Conversion
# -------------------------------------------------------------

def latlon_to_tile_xy(lat, lon, zoom):
    lat_rad = math.radians(lat)
    n = 2 ** zoom
    x = int((lon + 180.0) / 360.0 * n)
    y = int((1 - math.log(math.tan(lat_rad) + 1/math.cos(lat_rad)) / math.pi) / 2 * n)
    return x, y

def tiles_from_bbox(lat_min, lon_min, lat_max, lon_max, zoom):
    x0, y0 = latlon_to_tile_xy(lat_min, lon_min, zoom)
    x1, y1 = latlon_to_tile_xy(lat_max, lon_max, zoom)

    xmin, xmax = sorted((x0, x1))
    ymin, ymax = sorted((y0, y1))

    return [(x, y, zoom) for x in range(xmin, xmax+1) for y in range(ymin, ymax+1)]


# -------------------------------------------------------------
# Download function
# -------------------------------------------------------------

def download_tile(tms_url, x, y, z, outdir, session):
    url = tms_url.format(z=z, x=x, y=y)
    filepath = os.path.join(outdir, str(z), str(x))
    os.makedirs(filepath, exist_ok=True)
    out_file = os.path.join(filepath, f"{y}.png")

    if os.path.exists(out_file):
        return  # skip existing

    try:
        r = session.get(url, timeout=5)
        r.raise_for_status()
        with open(out_file, "wb") as f:
            f.write(r.content)
    except Exception as e:
        print(f"[ERR] {z}/{x}/{y}: {e}")


# -------------------------------------------------------------
# Main download routine
# -------------------------------------------------------------

def download_bbox_tiles(lat_min, lon_min, lat_max, lon_max,
                        zoom_levels,
                        tms_template,
                        outdir="tiles",
                        threads=20):

    session = requests.Session()

    for z in zoom_levels:
        print(f"--- Zoom {z} ---")
        tiles = tiles_from_bbox(lat_min, lon_min, lat_max, lon_max, z)
        print(f"Total tiles: {len(tiles)}")

        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as ex:
            futures = [
                ex.submit(download_tile, tms_template, x, y, z, outdir, session)
                for (x, y, z) in tiles
            ]
            for _ in concurrent.futures.as_completed(futures):
                pass
        print(f"Completed zoom {z}")


# -------------------------------------------------------------
# Example use
# -------------------------------------------------------------
if __name__ == "__main__":
    
    # Bottom-left and top-right corners
    lat_min, lon_min = 2.383050, 48.807153
    lat_max, lon_max = 2.400746, 48.819681
# 2.393615, 48.814002
    # Example TMS (OSM) – not satellite imagery, just demonstration.
    # Replace with your satellite TMS.
    
    tms = "https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{x}/{y}.png"

    download_bbox_tiles(
        lat_min=lat_min, lon_min=lon_min,
        lat_max=lat_max, lon_max=lon_max,
        zoom_levels=[10],
        tms_template=tms,
        outdir="./assets/tms_tiles",
        threads=32
    )
