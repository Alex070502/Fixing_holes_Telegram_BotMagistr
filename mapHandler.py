from base64 import urlsafe_b64encode

import folium
# from torch.utils.tensorboard.summary import image

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
    map = folium.Map(location=[59.935699, 30.312334], zoom_start=10)
    coordinates = sql.get_active_app_coordinates()
    # print(coordinates)
    encoded_photo_pothole = base64.b64encode(open('pothole3.jpg', 'rb').read()).decode()
    css = """
        <style>
            .leaflet-control-attribution {
                display: none !important;
            }
        </style>
        """
    map.get_root().html.add_child(folium.Element(css))

    for coord in coordinates:
        icon_html = f"""
        <div style="
            width: 30px;
            height: 30px;
            background-image: url('data:image/jpeg;base64,{encoded_photo_pothole}');
            background-size: cover;        /* Чтобы изображение заполнило круг */
            background-position: center;   /* Центрируем изображение */
            color: black;
            text-align: center;
            border-radius: 50%;
            line-height: 30px;
            font-weight: bold;">
            {coord[2]}
        </div>
        """
        # background - color: red;
        # color: white;
        # border: 2
        # px
        # solid
        # gray;
        # ">
        encoded = base64.b64encode(coord[3]).decode()

        # создаем HTML с изображением и текстом под ним
        html_content = f"""
                <div"> 
                <img src="data:image/png;base64,{encoded}" style = "max-width:100%;height:auto;display: block;">
                <div style="text-align: left;margin-top: 10px;font-weight: bold;"> 
                🔰Заявка №{coord[2]}<br>
                Статус заявки:<br>{coord[4]}<br>
                🌐 Место положение:<br>{coord[5]}<br>
                ⏰ Дата и время:<br>{coord[6]} 
                </div>
                </div>
                """

        # folium.Marker(location=(coord[0], coord[1]), icon=folium.DivIcon(html=icon_html)).add_to(map)
        # folium.CircleMarker(location=(coord[0], coord[1]), radius=9, popup=f"App #{coord[2]}", fill_color="red", color="gray", fill_opacity=0.7, tooltip=f"App #{coord[2]}").add_to(map)
        iframe = folium.IFrame(html_content, width=200, height=300)
        popup = folium.Popup(iframe, max_width=2650)
        folium.Marker(location=(coord[0], coord[1]), popup=popup, icon=folium.DivIcon(html=icon_html)).add_to(map)
    map.save("html/map.html")


def mark_from_db_user(user_id):
    if os.path.exists("D:\Fixing_holes_Telegram_BotMagistr\html\map.html"):
        os.remove("D:\Fixing_holes_Telegram_BotMagistr\html\map.html")
    map = folium.Map(location=[59.935699, 30.312334], zoom_start=10)
    coordinates = sql.get_active_app_coordinates_user(user_id)
    # print(coordinates)
    encoded_photo_pothole = base64.b64encode(open('pothole3.jpg', 'rb').read()).decode()
    css = """
            <style>
                .leaflet-control-attribution {
                    display: none !important;
                }
            </style>
            """
    map.get_root().html.add_child(folium.Element(css))

    for coord in coordinates:
        icon_html = f"""
            <div style="
                width: 30px;
                height: 30px;
                background-image: url('data:image/jpeg;base64,{encoded_photo_pothole}');
                background-size: cover;        /* Чтобы изображение заполнило круг */
                background-position: center;   /* Центрируем изображение */
                color: black;
                text-align: center;
                border-radius: 50%;
                line-height: 30px;
                font-weight: bold;">
                {coord[2]}
            </div>
            """
        # background - color: red;
        # color: white;
        # border: 2
        # px
        # solid
        # gray;
        # ">
        encoded = base64.b64encode(coord[3]).decode()

        # создаем HTML с изображением и текстом под ним
        html_content = f"""
                    <div"> 
                    <img src="data:image/png;base64,{encoded}" style = "max-width:100%;height:auto;display: block;">
                    <div style="text-align: left;margin-top: 10px;font-weight: bold;"> 
                    🔰Заявка №{coord[2]}<br>
                    Статус заявки:<br>{coord[4]}<br>
                    🌐 Место положение:<br>{coord[5]}<br>
                    ⏰ Дата и время:<br>{coord[6]} 
                    </div>
                    </div>
                    """

        # folium.Marker(location=(coord[0], coord[1]), icon=folium.DivIcon(html=icon_html)).add_to(map)
        # folium.CircleMarker(location=(coord[0], coord[1]), radius=9, popup=f"App #{coord[2]}", fill_color="red", color="gray", fill_opacity=0.7, tooltip=f"App #{coord[2]}").add_to(map)
        iframe = folium.IFrame(html_content, width=200, height=300)
        popup = folium.Popup(iframe, max_width=2650)
        folium.Marker(location=(coord[0], coord[1]), popup=popup, icon=folium.DivIcon(html=icon_html)).add_to(map)
    map.save(f"html/map{user_id}.html")


def mark_from_well_db():
    if os.path.exists("D:\Fixing_holes_Telegram_BotMagistr\html\map_well.html"):
        os.remove("D:\Fixing_holes_Telegram_BotMagistr\html\map_well.html")
    map = folium.Map(location=[59.935699, 30.312334], zoom_start=10)
    css = """
            <style>
                .leaflet-control-attribution {
                    display: none !important;
                }
            </style>
            """
    map.get_root().html.add_child(folium.Element(css))
    # coordinates = sql.get_active_app_coordinates()
    coordinates = sql.get_active_app_coordinates_well()
    # print(coordinates)
    # for coord in coordinates:
    #     icon_html = f"""
    #     <div style="
    #         width: 30px;
    #         height: 30px;
    #
    #         background-image: url("well.jpg");
    #         color: white;
    #         text-align: center;
    #         border-radius: 50%;
    #         line-height: 30px;
    #         font-weight: bold;
    #         border: 2px solid gray;">
    #         {coord[2]}
    #     </div>
    #     """
    encoded_photo_well = base64.b64encode(open('well1.jpg', 'rb').read()).decode()
    for coord in coordinates:
        icon_html = f"""
            <div style="
                width: 30px;
                height: 30px;
                background-image: url('data:image/jpeg;base64,{encoded_photo_well}');
                background-size: cover;        /* Чтобы изображение заполнило круг */
                background-position: center;   /* Центрируем изображение */
                color: white;
                text-align: center;
                border-radius: 50%;
                line-height: 30px;
                font-weight: bold;
                border: 2px solid black;
                
                display: flex;
                align-items: center;
                justify-content: center;">
                {coord[2]}
            </div>
            """
        # background - color: green;
        # border: 2
        # px
        # solid
        # gray;

        encoded = base64.b64encode(coord[3]).decode()

        # создаем HTML с изображением и текстом под ним
        html_content = f"""
        <div"> 
        <img src="data:image/png;base64,{encoded}" style = "max-width:100%;height:auto;display: block;">
        <div style="text-align: left;margin-top: 10px;font-weight: bold;"> 
        🔰Заявка №{coord[2]}<br>
        Статус заявки:<br>{coord[4]}<br>
        🌐 Место положение:<br>{coord[5]}<br>
        ⏰ Дата и время:<br>{coord[6]} 
        </div>
        </div>
        """

        # html = '<img src="data:image/jpeg;base64,{}">'.format
        # iframe = folium.IFrame(html(encoded), width=150, height=200)
        # popup = folium.Popup(iframe, max_width=2650)
        # folium.Marker(location=(coord[0], coord[1]), popup=popup, icon=folium.DivIcon(html=icon_html)).add_to(map)
        iframe = folium.IFrame(html_content, width=200, height=300)
        popup = folium.Popup(iframe, max_width=2650)
        folium.Marker(location=(coord[0], coord[1]), popup=popup, icon=folium.DivIcon(html=icon_html)).add_to(map)

        # folium.Marker(location=(coord[0], coord[1]), icon=folium.DivIcon(html=icon_html)).add_to(map)
        # folium.CircleMarker(location=(coord[0], coord[1]), radius=9, popup=f"App #{coord[2]}", fill_color="red", color="gray", fill_opacity=0.7, tooltip=f"App #{coord[2]}").add_to(map)
    map.save("html/map_well.html")


def mark_from_well_db_user(user_id):
    if os.path.exists("D:\Fixing_holes_Telegram_BotMagistr\html\map_well.html"):
        os.remove("D:\Fixing_holes_Telegram_BotMagistr\html\map_well.html")
    map = folium.Map(location=[59.935699, 30.312334], zoom_start=10)
    css = """
            <style>
                .leaflet-control-attribution {
                    display: none !important;
                }
            </style>
            """
    map.get_root().html.add_child(folium.Element(css))
    # coordinates = sql.get_active_app_coordinates()
    coordinates = sql.get_active_app_coordinates_well_user(user_id)
    # print(coordinates)
    # for coord in coordinates:
    #     icon_html = f"""
    #     <div style="
    #         width: 30px;
    #         height: 30px;
    #
    #         background-image: url("well.jpg");
    #         color: white;
    #         text-align: center;
    #         border-radius: 50%;
    #         line-height: 30px;
    #         font-weight: bold;
    #         border: 2px solid gray;">
    #         {coord[2]}
    #     </div>
    #     """
    encoded_photo_well = base64.b64encode(open('well1.jpg', 'rb').read()).decode()
    for coord in coordinates:
        icon_html = f"""
            <div style="
                width: 30px;
                height: 30px;
                background-image: url('data:image/jpeg;base64,{encoded_photo_well}');
                background-size: cover;        /* Чтобы изображение заполнило круг */
                background-position: center;   /* Центрируем изображение */
                color: white;
                text-align: center;
                border-radius: 50%;
                line-height: 30px;
                font-weight: bold;
                border: 2px solid black;

                display: flex;
                align-items: center;
                justify-content: center;">
                {coord[2]}
            </div>
            """
        # background - color: green;
        # border: 2
        # px
        # solid
        # gray;

        encoded = base64.b64encode(coord[3]).decode()

        # создаем HTML с изображением и текстом под ним
        html_content = f"""
        <div"> 
        <img src="data:image/png;base64,{encoded}" style = "max-width:100%;height:auto;display: block;">
        <div style="text-align: left;margin-top: 10px;font-weight: bold;"> 
        🔰Заявка №{coord[2]}<br>
        Статус заявки:<br>{coord[4]}<br>
        🌐 Место положение:<br>{coord[5]}<br>
        ⏰ Дата и время:<br>{coord[6]} 
        </div>
        </div>
        """

        # html = '<img src="data:image/jpeg;base64,{}">'.format
        # iframe = folium.IFrame(html(encoded), width=150, height=200)
        # popup = folium.Popup(iframe, max_width=2650)
        # folium.Marker(location=(coord[0], coord[1]), popup=popup, icon=folium.DivIcon(html=icon_html)).add_to(map)
        iframe = folium.IFrame(html_content, width=200, height=300)
        popup = folium.Popup(iframe, max_width=2650)
        folium.Marker(location=(coord[0], coord[1]), popup=popup, icon=folium.DivIcon(html=icon_html)).add_to(map)

        # folium.Marker(location=(coord[0], coord[1]), icon=folium.DivIcon(html=icon_html)).add_to(map)
        # folium.CircleMarker(location=(coord[0], coord[1]), radius=9, popup=f"App #{coord[2]}", fill_color="red", color="gray", fill_opacity=0.7, tooltip=f"App #{coord[2]}").add_to(map)
    map.save(f"html/map_well{user_id}.html")

