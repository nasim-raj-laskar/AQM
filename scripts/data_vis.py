import pandas as pd                                                  #type:ignore
import matplotlib.pyplot as plt

df = pd.read_csv("../dataset/air_quality.csv")


fig = plt.figure(figsize=(18, 14))

#Raw sensor signals
ax1 = plt.subplot(3, 2, 1)
ax1.plot(df.index, df["mq"], label="MQ Gas")
ax1.plot(df.index, df["hum"], label="Humidity")
ax1.plot(df.index, df["temp"], label="Temperature")
ax1.set_title("Raw Sensor Signals Over Time")
ax1.set_xlabel("Sample Index")
ax1.set_ylabel("Value")
ax1.legend()

# Gas normalization & rolling stats
ax2 = plt.subplot(3, 2, 2)
ax2.plot(df.index, df["gas_norm"], label="Gas Norm")
ax2.plot(df.index, df["rolling_mean_10"], label="Rolling Mean (10)")
ax2.plot(df.index, df["rolling_std_10"], label="Rolling Std (10)")
ax2.set_title("Gas Normalization & Rolling Statistics")
ax2.set_xlabel("Sample Index")
ax2.set_ylabel("Value")
ax2.legend()

# Gas change rate
ax3 = plt.subplot(3, 2, 3)
ax3.plot(df.index, df["gas_diff"], label="Gas Diff")
ax3.plot(df.index, df["gas_diff_norm"], label="Gas Diff Norm")
ax3.set_title("Gas Change Rate")
ax3.set_xlabel("Sample Index")
ax3.set_ylabel("Delta")
ax3.legend()


#Engineered interaction features
ax4 = plt.subplot(3, 2, 4)
ax4.plot(df.index, df["hum_adjusted_gas"], label="Hum Adjusted Gas")
ax4.plot(df.index, df["hum_gas"], label="Hum × Gas")
ax4.plot(df.index, df["temp_gas"], label="Temp × Gas")
ax4.set_title("Engineered Gas Interaction Features")
ax4.set_xlabel("Sample Index")
ax4.set_ylabel("Value")
ax4.legend()

#Correlation heatmap 
ax5 = plt.subplot(3, 1, 3)
corr = df.corr()
im = ax5.imshow(corr)
ax5.set_title("Feature Correlation Heatmap")
ax5.set_xticks(range(len(corr.columns)))
ax5.set_yticks(range(len(corr.columns)))
ax5.set_xticklabels(corr.columns, rotation=90)
ax5.set_yticklabels(corr.columns)
fig.colorbar(im, ax=ax5)


plt.tight_layout()
plt.show()
