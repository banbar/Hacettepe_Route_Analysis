import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="hacettepe_routes",
    user="postgres",
    password="12345Aa",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

# Query: reproject both geometries to EPSG:32636 before computing distances
cur.execute("""
    SELECT
        start_building_id,
        end_building_id,
        dist_legacy,
        dist_osrm,
        ST_HausdorffDistance(
            ST_Transform(geom_legacy, 32636),
            ST_Transform(geom_osrm, 32636)
        ) AS hausdorff_dist_m,
        ST_FrechetDistance(
            ST_Transform(geom_legacy, 32636),
            ST_Transform(geom_osrm, 32636)
        ) AS frechet_dist_m
    FROM route_comparisons
    WHERE travel_mode = 'yaya';
""")
count = 0
# Print the results
results = []
for row in cur.fetchall():
    count += 1
    start_id, end_id, dist_legacy, dist_osrm, hausdorff, frechet = row
    results.append({
        "start_building_id": start_id,
        "end_building_id": end_id,
        "dist_legacy": dist_legacy,
        "dist_osrm": dist_osrm,
        "Hausdorff": hausdorff,
        "Frechet": frechet
    })
print("Count: ", count)

df = pd.DataFrame(results)


data = [df['dist_legacy'].values, df['dist_osrm'].values]
data = np.array(data)

x = data[0]
y = data[1]

# Reshape x for sklearn (it expects 2D)
X = x.reshape(-1, 1)
mean_x = sum(x) / len(x)
mean_y = sum(y) / len(y)

# Fit linear regression model
model = LinearRegression()
model.fit(X, y)
y_pred = model.predict(X)

# Compute R^2
r2 = r2_score(y, y_pred)

legend_size = 24
label_size = 26
tick_size = 24
title_size = 30

fig, ax = plt.subplots(figsize=(20,11))  # Create figure and axes
ax.scatter(x, y,  facecolors='none', edgecolors='black', linewidths=0.6, label="Data")  # Use the Axes object to plot
ax.plot(x, y_pred, color='red', label="Fit", linewidth=4)
# Perfect fit line (y = x)
#ax.plot(x, x, color='black', linestyle='--', label='$R^2=1$', linewidth=2)

# Plot the means
# Plot vertical line at mean_x
ax.axvline(mean_x, color='black', linestyle='--', linewidth=1)
# Plot horizontal line at mean_y
ax.axhline(mean_y, color='black', linestyle='--', linewidth=1)

# Annotate mean_x on x-axis
ax.text(
    mean_x, ax.get_ylim()[0],  # Place at bottom of y-axis
    fr'$\bar{{x}}$ = {mean_x:.1f}',
    color='black',
    fontsize=tick_size-2,
    va='bottom',
    ha='center',
    rotation=90,
    bbox=dict(facecolor='white', edgecolor='none', alpha=0.7)
)

# Annotate mean_y on y-axis
ax.text(
    ax.get_xlim()[0], mean_y,  # Place at left of x-axis
    fr'$\bar{{y}}$ = {mean_y:.1f}',    
    color='black',
    fontsize=tick_size-2,
    va='center',
    ha='left',
    bbox=dict(facecolor='white', edgecolor='none', alpha=0.7)
)


ax.text(0.05, 0.95, f"$R^2 = {r2:.2f}$", 
        transform=ax.transAxes,
        verticalalignment='top', 
        fontsize=legend_size, 
        bbox=dict(facecolor='white', alpha=0.8))

# Labels and ticks
ax.set_ylabel('OSRM (m)', fontsize=label_size)
ax.set_xlabel('Legacy (m)', fontsize=label_size)

ax.tick_params(axis='both', labelsize=tick_size)

# Spine customization (NEW)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_linewidth(1.8)  # Thickened bottom spine
ax.spines['left'].set_linewidth(1.8)   # Thickened left spine

# Grid styling
ax.grid(True, linestyle='--', alpha=0.6)
ax.tick_params(axis='y', labelsize=tick_size)

ax.set_title("Travel distances (pedestrian)", fontsize=title_size)

highlight_x = [439]     # Legacy x-values
highlight_y = [3047]   # OSRM y-values

ax.scatter(
    highlight_x, highlight_y,
    facecolors='red',
    edgecolors='black',
    linewidths=1.5,
    s=200,                     # Marker size
    zorder=3                  # Draw on top
)


labels = ['A']

for x_val, y_val, label in zip(highlight_x, highlight_y, labels):
    ax.text(
        x_val - 30, y_val - 30,     # Offset to lower-left of each point
        label,
        color='red',
        fontsize=26,
        fontweight='bold',
        va='top',                  # vertical alignment
        ha='right'                 # horizontal alignment
    )


plt.savefig("scatter_pedestrian.svg", format="svg", bbox_inches='tight', pad_inches=0, dpi=96)  # Save as SVG


plt.tight_layout()
plt.show()

cur.close()
conn.close()
