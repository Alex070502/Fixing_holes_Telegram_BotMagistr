import datetime

from sqlalchemy import insert, select, update, delete, or_
from sqlalchemy.orm import Session
from Config_BD.Basemodul import engine, wa, pa, users


class SQL:
    session = Session(engine)

    def well_app_insert(self,
                        address: str, longtitude: float, latitude: float,
                        user_id: int, photo: bytearray, det_photo: bytearray, date: datetime):
        ins = insert(wa).values(
            address=address,
            longtitude=longtitude,
            latitude=latitude,
            user_id=user_id,
            photo=photo,
            detected_photo=det_photo,
            date=date
        )
        self.session.execute(ins)
        self.session.commit()

    def pathole_app_insert(self,
                           address: str, longtitude: float, latitude: float,
                           user_id: int, photo: bytearray, det_photo: bytearray, date: datetime):
        ins = insert(pa).values(
            address=address,
            longtitude=longtitude,
            latitude=latitude,
            user_id=user_id,
            photo=photo,
            detected_photo=det_photo,
            date=date
        )
        self.session.execute(ins)
        self.session.commit()

    def users_insert(self, username: str, tid: int):
        ins = insert(users).values(
            username=username,
            tid=tid
        )
        self.session.execute(ins)
        self.session.commit()

    def users_select(self, tid: int):
        sel = select(users).where(users.c.tid == tid)
        return self.session.execute(sel).first()

    def add_number(self, number: str, tid: int):
        up = update(users).values(number=number).where(users.c.tid == tid)
        self.session.execute(up)
        self.session.commit()

    def well_count(self, tid: int):
        count = self.session.query(wa).where(wa.c.user_id == tid).count()
        return count

    def hole_count(self, tid: int):
        count = self.session.query(pa).where(pa.c.user_id == tid).count()
        return count

    def get_last_ph_id_by_userid(self, user_id: int):
        last = self.session.query(pa.c.id).filter(pa.c.user_id == user_id).order_by(pa.c.id.desc()).first()
        return last[0]

    def get_last_well_id_by_userid(self, user_id: int):
        last = self.session.query(wa.c.id).filter(wa.c.user_id == user_id).order_by(wa.c.id.desc()).first()
        return last[0]

    def get_all_ph_by_userid(self, user_id: int):
        all = self.session.query(pa.c.id, pa.c.address, pa.c.date, pa.c.status).filter(pa.c.user_id == user_id).all()
        return all

    def get_all_well_by_userid(self, user_id: int):
        all = self.session.query(wa.c.id, wa.c.address, wa.c.date, wa.c.status).filter(wa.c.user_id == user_id).all()
        return all

    def get_all_username(self):
        usernames = self.session.query(users.c.username, users.c.tid).all()
        return usernames

    def update_status_ph(self, id: int, new_status: str):
        s = update(pa).values(status=new_status).where(pa.c.id == id)
        self.session.execute(s)
        self.session.commit()

    def update_status_well(self, id: int, new_status: str):
        s = update(wa).values(status=new_status).where(wa.c.id == id)
        self.session.execute(s)
        self.session.commit()

    def get_ph_by_id(self, id: int):
        s = select(pa).where(pa.c.id == id)
        return self.session.execute(s).first()

    def get_well_by_id(self, id: int):
        s = select(wa).where(wa.c.id == id)
        return self.session.execute(s).first()

    def get_role(self, id: int):
        s = select(users.c.role).where(users.c.tid == id)
        return self.session.execute(s).first()

    # сделал колодцы не работает если меням статус в чем различия с ямами не знаю
    # зачем нужен данный код если есть get_active_app_coordinates(self):
    def get_all_coordinates(self):
        s = select(pa.c.latitude, pa.c.longtitude)
        return self.session.execute(s).all()

    def get_all_coordinates_well(self):
        s = select(wa.c.latitude, wa.c.longtitude)
        return self.session.execute(s).all()

    def get_active_app_coordinates(self):
        s = select(pa.c.latitude, pa.c.longtitude, pa.c.id).where(
            or_(pa.c.status == "Выполняется 🔸", pa.c.status == "Рассматривается", pa.c.status == "Рассматривается 🔁")
        )
        return self.session.execute(s).all()

    def get_active_app_coordinates_well(self):
        s = select(wa.c.latitude, wa.c.longtitude, wa.c.id).where(
            or_(wa.c.status == "Выполняется 🔸", wa.c.status == "Рассматривается", wa.c.status == "Рассматривается 🔁")
        )
        return self.session.execute(s).all()




if __name__ == '__main__':
    sql = SQL()
    print(sql.get_active_app_coordinates())
    print(sql.get_active_app_coordinates_well())
