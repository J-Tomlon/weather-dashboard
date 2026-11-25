# weather-dashboard
Dashboard comparing outputs of weather models. The dashboard shows how much the models disagree. It doesn't measure which one is right, because it has no observations to compare against.

## What are Weather Models?
Weather models are computer simulations that use mathematical equations based on physics to predict future weather conditions from current atmospheric observations given a set of starting parameters and training data. 

### GFS (NOAA, USA)
This is the American global model, about 13 km resolution, run 4 times a day out to 16 days. In the gfs_seamless option, Open-Meteo blends in the high-resolution HRRR model over the US for the first day or so. GFS has traditionally been too progressive, meaning it moves storm systems along too fast, and it tends to eject slow, cut-off lows too quickly. It's also prone to producing too much light precipitation. Its skill is a step behind ECMWF in the medium range.

### ECMWF IFS (European Centre)
This is generally the top-scoring global model in verification. Your dashboard uses the free 0.25° (roughly 25 km) open-data version, which is coarser than ECMWF's full-resolution product. Because the terrain is smoothed at that resolution, it tends to under-forecast 10 m wind speeds and the peaks of heavy convective rain, and it can run a bit drizzly like GFS. It's usually best at the large-scale pattern a few days out.

### ICON (DWD, Germany)
This is Germany's global model at about 13 km, and icon_seamless blends in finer regional versions where they exist. It's tuned and verified mostly for Europe. It's a solid model, but I don't have well-documented US-specific biases for it, so I'd rather not guess. It's useful as an independent third opinion, though.

### GEM (Environment Canada)
This is Canada's global model at about 15 km, and it's blended with their high-resolution regional model over Canada and the northern US. It's tuned for Canadian weather, so it tends to do better in the north. It's typically a bit less skillful than ECMWF and GFS in the medium range, and I also don't have well-documented US-wide biases for it.
