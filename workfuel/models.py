from workfuel import db, app


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(25), nullable=True)
    last_name = db.Column(db.String(25), nullable=True)
    personnel_number = db.Column(db.Integer, nullable=False, unique=True)
    password = db.Column(db.String(1024), nullable=False, default=3)


class Locomotive(db.Model):
    __tablename__ = 'locomotives'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    locomotive_number = db.Column(db.Integer, nullable=False)
    driver = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    fuels = db.relationship('Fuel', backref='locomotive', lazy=True)


class Fuel(db.Model):
    __tablename__ = 'fuels'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    beginning_fuel_liters = db.Column(db.Integer, nullable=False)
    end_fuel_litres = db.Column(db.Integer, nullable=False)
    beginning_fuel_kilo = db.Column(db.Float, nullable=False)
    end_fuel_kilo = db.Column(db.Float, nullable=False)
    specific_weight = db.Column(db.Float, nullable=False)
    add_fuel = db.Column(db.Integer, nullable=True)
    norm = db.Column(db.Float, nullable=False)
    fact = db.Column(db.Float, nullable=False)
    locomotive_id = db.Column(db.Integer, db.ForeignKey('locomotives.id'), nullable=False)


class WorkTime(db.Model):
    __tablename__ = 'worktime'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime, nullable=False)
    route_number = db.Column(db.Integer, nullable=False)
    start_of_work = db.Column(db.DateTime, nullable=False)
    end_of_work = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


class MovementTime(db.Model):
    __tablename__ = 'movements'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_movement = db.Column(db.Float, nullable=False)
    end_movement = db.Column(db.Float, nullable=False)
    workerspark_id = db.Column(db.Integer, db.ForeignKey('workparks.id'), nullable=False)


class WorkPark(db.Model):
    __tablename__ = 'workparks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    locomotive_id = db.Column(db.Integer, db.ForeignKey('locomotives.id'), nullable=False)
    park_name = db.Column(db.String(30), nullable=False)
    work_hours = db.Column(db.Float, nullable=False, default=0)
    hot_state = db.Column(db.Float, nullable=False, default=0)
    cool_state = db.Column(db.Float, nullable=False, default=0)
    locomotive = db.relationship('Locomotive', backref=db.backref('workparks', lazy=True))


class ReserveRun(db.Model):
    __tablename__ = 'reserveruns'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    train_number = db.Column(db.Integer, nullable=False)
    start_run_reserve = db.Column(db.DateTime, nullable=False)
    end_run_reserve = db.Column(db.DateTime, nullable=False)
    start_station = db.Column(db.String(25), nullable=False)
    end_station = db.Column(db.String(25), nullable=False)
    locomotive_id = db.Column(db.Integer, db.ForeignKey('locomotives.id'), nullable=False)


class Log(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    client_ip = db.Column(db.String(32), nullable=False)
    locomotive_id = db.Column(db.Integer, db.ForeignKey('locomotives.id'), nullable=False)
    fuel_id = db.Column(db.Integer, db.ForeignKey('fuels.id'), nullable=False)
    worktime_id = db.Column(db.Integer, db.ForeignKey('worktime.id'), nullable=False)


class Settings(db.Model):
    __tablename__ = 'settings'
    id = db.Column(db.Integer, primary_key=True)
    park_l_norm = db.Column(db.Float, nullable=False, default=14.0)
    park_g_norm = db.Column(db.Float, nullable=False, default=15.0)
    park_e_norm = db.Column(db.Float, nullable=False, default=15.0)
    park_z_norm = db.Column(db.Float, nullable=False, default=15.0)
    park_vm_norm = db.Column(db.Float, nullable=False, default=15.0)
    park_nijny_norm = db.Column(db.Float, nullable=False, default=13.0)
    park_vchd_3_norm = db.Column(db.Float, nullable=False, default=13.0)
    park_tch_1_norm = db.Column(db.Float, nullable=False, default=10.0)
    park_tch_8_norm = db.Column(db.Float, nullable=False, default=10.0)
    park_dnepr_norm = db.Column(db.Float, nullable=False, default=15.0)
    park_gorvetka_norm = db.Column(db.Float, nullable=False, default=14.0)
    park_diyovka_norm = db.Column(db.Float, nullable=False, default=13.0)
    park_goryainovo_norm = db.Column(db.Float, nullable=False, default=13.0)
    park_kaidakskaya_norm = db.Column(db.Float, nullable=False, default=13.5)
    park_nizhnedneprovsk_norm = db.Column(db.Float, nullable=False, default=14.5)
    park_pristan_norm = db.Column(db.Float, nullable=False, default=14.5)
    park_lotsmanka_norm = db.Column(db.Float, nullable=False, default=12.0)
    park_vstrechnyy_norm = db.Column(db.Float, nullable=False, default=13.0)
    park_dn_gruzovoy_norm = db.Column(db.Float, nullable=False, default=12.0)
    park_obvodnaya_norm = db.Column(db.Float, nullable=False, default=12.0)
    park_lisky_norm = db.Column(db.Float, nullable=False, default=12.0)
    park_privolnoe_norm = db.Column(db.Float, nullable=False, default=13.0)
    park_rasnaya_norm = db.Column(db.Float, nullable=False, default=13.0)
    park_suhachovka_norm = db.Column(db.Float, nullable=False, default=12.0)
    hot_state = db.Column(db.Integer, nullable=False, default=10)
    cool_state = db.Column(db.Integer, nullable=False, default=0)

    @classmethod
    def get_instance(cls):
        instance = cls.query.get(1)
        if instance is None:
            instance = cls(id=1)
            db.session.add(instance)
            db.session.commit()
        return instance


with app.app_context():
    db.create_all()
    settings_params = Settings.get_instance()
