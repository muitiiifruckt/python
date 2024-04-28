# import plotly.express as px
# df = px.data.gapminder().query("year==2007")
# fig = px.scatter_geo(df,locations="iso_alpha",color = "continent",hover_name="country",size = "pop",projection="natural earth")
# fig.show()
# import plotly.express as px
# df = px.data.gapminder()
# fig = px.scatter_geo(df,locations="iso_alpha",color = "continent",hover_name="country",size = "pop",animation_frame="year", projection="natural earth")
# fig.show()
#
from plotly.subplots import make_subplots
fig = make_subplots(rows =1,cols =2)
fig.add_scatter(y = [4,2,3.5],mode = "markers", marker = dict(size =20, color = "LightSeaGreen"), name = "a", row =1 ,col=1)
fig.add_bar(y =[2,1,3],marker=dict(color = "MediumPurple"),name = "b",row =1 ,col =1)
fig.add_scatter(y = [4,3.5,4],mode = "markers", marker = dict(size =20, color = "MediumPurple"), name = "c", row =1 ,col=2)
fig.add_bar(y =[1,3,2],marker=dict(color = "LightSeaGreen"),name = "d",row =1 ,col =2)
fig.show()

