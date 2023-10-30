from pymongo import MongoClient


def get_database():
    return MongoClient(host='136.199.93.61', authSource='admin').twon
