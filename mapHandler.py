import folium
from Config_BD import repo
import os
from folium import IFrame
import base64

sql = repo.SQL()


def mark(coord, id, map):
    folium.Marker(location=coord, popup=f"App #{id}").add_to(map)


# def mark_from_db():
#     if os.path.exists("D:\Fixing_holes_Telegram_BotMagistr\html\map.html"):
#         os.remove("D:\Fixing_holes_Telegram_BotMagistr\html\map.html")
#     map = folium.Map(location=[59.57, 30.19], zoom_start=10)
#     coordinates = sql.get_active_app_coordinates()
#     print(coordinates)
#     for coord in coordinates:
#
#         #folium.Marker(location=(coord[0], coord[1]), popup=f"App #{coord[2]}", icon=folium.Icon('gray')).add_to(map)
#         folium.CircleMarker(location=(coord[0], coord[1]), radius=9, popup=f"App #{coord[2]}", fill_color="red", color="gray", fill_opacity=0.7, tooltip=f"App #{coord[2]}").add_to(map)
#     map.save("html/map.html")

# def mark_from_db():
#     if os.path.exists("D:\Fixing_holes_Telegram_BotMagistr\html\map.html"):
#         os.remove("D:\Fixing_holes_Telegram_BotMagistr\html\map.html")
#     map = folium.Map(location=[59.57, 30.19], zoom_start=10)
#     coordinates = sql.get_active_app_coordinates()
#     print(coordinates)
#     for coord in coordinates:
#
#         html = f"""
#         <div style="
#             width: 30px;
#             height: 30px;
#             background-color: red;
#             color: white;
#             text-align: center;
#             border-radius: 50%;
#             line-height: 30px;
#             font-weight: bold;
#             border: 2px solid gray;">
#             {coord[2]}
#         </div>
#         """
#         iframe = IFrame(html, width=40, height=40)
#         popup = folium.Popup(iframe, max_width=40)
#         folium.Marker(location=(coord[0], coord[1]), popup=popup).add_to(map)
#         #folium.CircleMarker(location=(coord[0], coord[1]), radius=9, popup=f"App #{coord[2]}", fill_color="red", color="gray", fill_opacity=0.7, tooltip=f"App #{coord[2]}").add_to(map)
#     map.save("html/map.html")


def mark_from_db():
    if os.path.exists("D:\Fixing_holes_Telegram_BotMagistr\html\map.html"):
        os.remove("D:\Fixing_holes_Telegram_BotMagistr\html\map.html")
    map = folium.Map(location=[59.57, 30.19], zoom_start=10)
    coordinates = sql.get_active_app_coordinates()
    # print(coordinates)
    for coord in coordinates:
        icon_html = f"""
        <div style="
            width: 30px;
            height: 30px;
            background-color: red;
            color: white;
            text-align: center;
            border-radius: 50%;
            line-height: 30px;
            font-weight: bold;
            border: 2px solid gray;">
            {coord[2]}
        </div>
        """

        folium.Marker(location=(coord[0], coord[1]), icon=folium.DivIcon(html=icon_html)).add_to(map)
        # folium.CircleMarker(location=(coord[0], coord[1]), radius=9, popup=f"App #{coord[2]}", fill_color="red", color="gray", fill_opacity=0.7, tooltip=f"App #{coord[2]}").add_to(map)
    map.save("html/map.html")


def mark_from_well_db():
    if os.path.exists("D:\Fixing_holes_Telegram_BotMagistr\html\map_well.html"):
        os.remove("D:\Fixing_holes_Telegram_BotMagistr\html\map_well.html")
    map = folium.Map(location=[59.57, 30.19], zoom_start=10)
    # coordinates = sql.get_active_app_coordinates()
    coordinates = sql.get_active_app_coordinates_well()
    # print(coordinates)
    for coord in coordinates:
        icon_html = f"""
        <div style="
            width: 30px;
            height: 30px;
            background-color: green;
            color: white;
            text-align: center;
            border-radius: 50%;
            line-height: 30px;
            font-weight: bold;
            border: 2px solid gray;">
            {coord[2]}
        </div>
        """

        encoded = base64.b64encode(open('file_155.jpg', 'rb').read()).decode()
        html = '<img src="data:image/jpeg;base64,{}">'.format
        iframe = folium.IFrame(html(encoded), width=150, height=200)
        popup = folium.Popup(iframe, max_width=2650)
        folium.Marker(location=(coord[0], coord[1]), popup=popup, icon=folium.DivIcon(html=icon_html)).add_to(map)

        # folium.Marker(location=(coord[0], coord[1]), icon=folium.DivIcon(html=icon_html)).add_to(map)
        # folium.CircleMarker(location=(coord[0], coord[1]), radius=9, popup=f"App #{coord[2]}", fill_color="red", color="gray", fill_opacity=0.7, tooltip=f"App #{coord[2]}").add_to(map)
    map.save("html/map_well.html")
