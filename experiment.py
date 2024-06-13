import pandas as pd
read = "perrin-freres-monthly-champagne-.csv"
df = pd.read_csv(f'F://csv files//{read}')
df.columns=["Month","Sales"]
df.drop(105,axis=0,inplace=True)
df.set_index('Month',inplace=True)
img = BytesIO()
plt.savefig(img, format='png')
img.seek(0)
plot_url = base64.b64encode(img.getvalue()).decode()
plt.close()










