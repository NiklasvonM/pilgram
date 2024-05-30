import logging
from datetime import datetime

from peewee import SqliteDatabase, Model, IntegerField, CharField, ForeignKeyField, DateTimeField, DeferredForeignKey


DB_FILENAME: str = "pilgram.db"

db = SqliteDatabase(DB_FILENAME)
log = logging.getLogger(__name__)


class BaseModel(Model):
    class Meta:
        database = db


class ZoneModel(BaseModel):
    id = IntegerField(primary_key=True, unique=True)
    name = CharField()
    level = IntegerField()
    description = CharField()


class QuestModel(BaseModel):
    id = IntegerField(primary_key=True, unique=True)
    zone_id = ForeignKeyField(ZoneModel, backref="quests")
    number = IntegerField(default=0)  # the number of the quest in the quest order
    name = CharField(null=False)
    description = CharField(null=False)
    success_text = CharField(null=False)
    failure_text = CharField(null=False)


class PlayerModel(BaseModel):
    id = IntegerField(primary_key=True, unique=True)
    name = CharField(null=False)
    description = CharField(null=False)
    guild_id = DeferredForeignKey('GuildModel', backref="players", null=True, default=None)
    money = IntegerField(default=10)
    level = IntegerField(default=1)
    xp = IntegerField(default=0)
    gear_level = IntegerField(default=0)
    progress = CharField(null=True, default=None)  # progress is stored as a char string in the player table.


class GuildModel(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField(null=False)
    description = CharField(null=False)
    founder_id = ForeignKeyField(PlayerModel, backref='guilds')
    creation_date = DateTimeField(default=datetime.now)


class ZoneEventModel(BaseModel):
    id = IntegerField(primary_key=True)
    zone_id = ForeignKeyField(ZoneModel)
    event_text = CharField()


class QuestProgressModel(BaseModel):
    """ Table that tracks the progress of player quests & controls when to send events/finish the quest """
    player_id = ForeignKeyField(PlayerModel, unique=True, backref="quest_progress")
    quest_id = ForeignKeyField(QuestModel, null=True, default=None)
    start_time = DateTimeField(default=datetime.now)
    end_time = DateTimeField(default=datetime.now)
    last_update = DateTimeField(default=datetime.now)

    class Meta:
        primary_key = False


def create_tables():
    db.connect()
    db.create_tables([ZoneModel, QuestModel, PlayerModel, GuildModel, ZoneEventModel, QuestProgressModel])
    db.close()
