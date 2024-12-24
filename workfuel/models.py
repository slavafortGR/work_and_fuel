from workfuel import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    personnel_number = db.Column(db.String(5), nullable=False, unique=True)
    route_number = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(255), nullable=False)


class Locomotive(db.Model):
    __tablename__ = 'locomotives'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    locomotive_number = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


class Fuel(db.Model):
    __tablename__ = 'fuels'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fuel_start_work_liters = db.Column(db.Integer, nullable=False)
    fuel_end_work_liters = db.Column(db.Integer, nullable=False)
    fuel_start_work_kilo = db.Column(db.Float, nullable=False)
    fuel_end_work_kilo = db.Column(db.Float, nullable=False)
    start_weight_fuel = db.Column(db.Float, nullable=False)
    end_weight_fuel = db.Column(db.Float, nullable=False)
    add_fuel = db.Column(db.Integer, nullable=True)
    locomotive_id = db.Column(db.Integer, db.ForeignKey('locomotives.id'), nullable=False)


class WorkTime(db.Model):
    __tablename__ = 'worktime'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_of_work = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    end_of_work = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


class MovementTime(db.Model):
    __tablename__ = 'movements'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_movement = db.Column(db.Float, nullable=False)
    end_movement = db.Column(db.Float, nullable=False)
    workerspark_id = db.Column(db.Integer, db.ForeignKey('workersparks.id'), nullable=False)


class WorkersPark(db.Model):
    __tablename__ = 'workersparks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(25), nullable=False, unique=True)
    norm = db.Column(db.Float, nullable=False)
    locomotive_id = db.Column(db.Integer, db.ForeignKey('locomotive.id'), nullable=False)


class Maintenance(db.Model):
    __tablename__ = 'maintenance'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    db.Column(db.Boolean, default=False, nullable=True)
    locomotive_id = db.Column(db.Integer, db.ForeignKey('locomotives.id'), nullable=False)


class ReserveRun(db.Model):
    __tablename__ = 'reserveruns'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    train_number = db.Column(db.Integer, nullable=False)
    start_run_reserve = db.Column(db.DateTime, nullable=False)
    end_run_reserve = db.Column(db.DateTime, nullable=False)
    start_station = db.Column(db.String(25), nullable=False)
    end_station = db.Column(db.String(25), nullable=False)
    locomotive_id = db.Column(db.Integer, db.ForeignKey('locomotives.id'), nullable=False)


class Driver(db.Model):
    __tablename__ = 'drivers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    personnel_number = db.Column(db.Integer, nullable=False, unique=True)
    password = db.Column(db.String(1024), nullable=False)


# class Locomotive(db.Model):
#     __tablename__ = 'locomotives'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     locomotive_number = db.Column(db.String(20), nullable=False)
#     route_number = db.Column(db.Integer, nullable=False, unique=True)
#     start_time = db.Column(db.DateTime, nullable=False)
#     end_time = db.Column(db.DateTime, nullable=False)
#     beginning_fuel_liters = db.Column(db.Integer, default=0, nullable=False)
#     beginning_fuel_kg = db.Column(db.Float, default=0, nullable=False)
#     end_fuel_litres = db.Column(db.Integer, default=0, nullable=False)
#     end_fuel_kg = db.Column(db.Float, default=0, nullable=False)
#     specific_weight = db.Column(db.Float, default=0, nullable=False)
#     norm_spend_fuel = db.Column(db.Float, default=0, nullable=False)
#     fact_spend_fuel = db.Column(db.Float, default=0, nullable=False)
#     description_of_reasons = db.Column(db.String(200), nullable=True)
#     owner = db.Column(db.Integer, db.ForeignKey("drivers.id"), nullable=False)
