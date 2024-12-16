import sqlite3
import datetime
import matplotlib.pyplot as plt
import json

DB_NAME = "market_database.db"
OUTPUT_FILE = "vix_tnx_metrics.json"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute(
	f"""
	SELECT vix_data.date, vix_data.value AS vix_value, tnx_data.value AS tnx_value
	FROM vix_data
	JOIN tnx_data ON vix_data.date = tnx_data.date
	ORDER BY vix_data.date
	"""
)

rows = cursor.fetchall()
conn.close()

dates = []
vix_values = []
tnx_values = []

for date_str, vix_val, tnx_val in rows:

    dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    dates.append(dt)

    vix_values.append(vix_val)
    tnx_values.append(tnx_val)

fig, ax = plt.subplots(figsize=(12, 6))
ax2 = ax.twinx()

ax.plot(dates, vix_values, 
	color="red", 
	label="VIX")

ax2.plot(dates, tnx_values, 
	color="green", 
	label="TNX")

ax.set_xlabel("Date")

ax.set_ylabel("VIX Value", 
	color="red")

ax2.set_ylabel("TNX (%)", 
	color="green")



lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

plt.title("VIX vs TNX")
plt.show()

vix_avg = sum(vix_values)/len(vix_values)
vix_min = min(vix_values)
vix_max = max(vix_values)
vix_count = len(vix_values)

tnx_avg = sum(tnx_values) / len(tnx_values)
tnx_min = min(tnx_values)
tnx_max = max(tnx_values)
tnx_count = len(tnx_values)

metrics = {
    "VIX": {
        "Average Value": round(vix_avg, 2),
        "Minimum Value": round(vix_min, 2),
        "Maximum Value": round(vix_max, 2),
        "Number of Entries": vix_count,
    },
    "TNX": {
        "Average Value": round(tnx_avg, 2),
        "Minimum Value": round(tnx_min, 2),
        "Maximum Value": round(tnx_max, 2),
        "Number of Entries": tnx_count,
    },
    "Summary": {
        "Analysis Period": f"{dates[0].strftime('%Y-%m-%d')} to {dates[-1].strftime('%Y-%m-%d')}",
        "Total Days Analyzed": len(dates),
    },
}

with open(OUTPUT_FILE, "w") as json_file:
    json.dump(metrics, json_file, 
    	indent=2)

print(f"Metrics successfully written to {OUTPUT_FILE}")
