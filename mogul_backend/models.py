from django.db import models
from django.conf import settings
from eveuniverse.models import EveType
from django.utils import timezone
from dynamic_preferences.models import PerInstancePreferenceModel
from django_pandas.managers import DataFrameManager


def one_day_ago():
    return timezone.now() + timezone.timedelta(days=-1)

# Create your models here.
class Transaction(models.Model):
    client_id = models.IntegerField() #int32
    date = models.DateTimeField() #date-time
    is_buy = models.BooleanField(null=True,default=False)#boolean
    is_personal = models.BooleanField(null=True,default=False)#boolean
    journal_ref_id = models.BigIntegerField() #int64
    location_id = models.BigIntegerField() #int64
    quantity = models.IntegerField() #int32
    transaction_id = models.BigIntegerField() #int64
    type_id = models.IntegerField(default=0) #int32
    unit_price = models.DecimalField(max_digits=24,decimal_places=2) #double
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="The user to whom this transaction belongs."
    )
    # Alright let's add the post-processed data
    type_name = models.CharField(default="Unknown",max_length=64)
    station_name = models.CharField(default="Unknown",max_length=64)
    processed = models.BooleanField(default=False, null=False)
    profit = models.DecimalField(default=0,max_digits=20,decimal_places=2)
    margin = models.DecimalField(default=0,max_digits=20,decimal_places=2)
    taxes = models.DecimalField(default=0,max_digits=20,decimal_places=2)
    stock_date = models.DateTimeField(null=True)
    character_id = models.IntegerField(default=0)
    corporation_id = models.IntegerField(default=0)
    def __str__(self):
        return f'{self.quantity} {self.type_name} at {self.date.strftime("%Y-%m-%d %H:%M:%S")}'

class Journal(models.Model):
    amount = models.DecimalField(default=0,max_digits=20,decimal_places=2)
    balance = models.DecimalField(default=0,max_digits=20,decimal_places=2)
    context_id = models.BigIntegerField(null=True)
    context_id_type = models.CharField(null=True,max_length=64)
    date = models.DateTimeField()
    description = models.CharField(max_length=128)
    first_party_id = models.BigIntegerField()
    ref_id = models.BigIntegerField()
    reason = models.CharField(max_length=64,null=True)
    ref_type = models.CharField(max_length=64,null=True)
    second_party_id = models.BigIntegerField()
    tax = models.DecimalField(default=0,max_digits=20,decimal_places=2,null=True)
    tax_receiver_id = models.BigIntegerField(null=True)
    character_id = models.IntegerField(default=0)
    corporation_id = models.IntegerField(default=0)
    division_id = models.IntegerField(default=0)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="The user to whom this journal belongs."
    )
class Order(models.Model):
    duration = models.IntegerField()
    is_buy_order = models.BooleanField(null=True)
    is_corporation = models.BooleanField(null=True,default=False)
    issued = models.DateTimeField()
    location_id = models.BigIntegerField()
    min_volume = models.IntegerField(null=True,default=0)
    order_id = models.BigIntegerField(primary_key = True)
    price = models.DecimalField(default=0,max_digits=20,decimal_places=2)
    range = models.CharField(max_length=16,default="0")
    region_id = models.IntegerField()
    type_id = models.IntegerField()
    volume_remain = models.IntegerField()
    volume_total = models.IntegerField()
    character_id = models.IntegerField(default=0)
    corporation_id = models.IntegerField(default=0,null=True)
    last_updated = models.DateTimeField(null=True,default=timezone.now)
    state = models.CharField(default="Open",max_length=32)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="The user to whom this transaction belongs."
    )
    @property
    def item(self):
        return EveType.objects.filter(id=self.type_id).first()
    @property
    def character(self):
        return Character.objects.filter(character_id=self.character_id).first()
    @property
    def station(self):
        if(self.location_id > 70000000):
            # It's a structure, let's get that
            return Structure.objects.filter(id=self.location_id).first()
        else:
            return EveType.objects.filter(id=self.location_id).first()

class Character(models.Model):
    character_id = models.BigIntegerField(default=0)
    alliance_id = models.IntegerField(null=True)
    corporation_id = models.IntegerField(null=True)
    name = models.CharField(default="Cool Guy", max_length=32,null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="The user to whom this character belongs."
    )
    last_esi_pull = models.DateTimeField(default=one_day_ago)
    def __str__(self):
        return f'{self.name}'

class Corporation(models.Model):
    corporation_id = models.BigIntegerField(default=0)
    alliance_id = models.IntegerField(null=True)
    name = models.CharField(default="Cool Corp", max_length=32,null=True)
    ceo_id = models.IntegerField()
    ticker = models.CharField(default="YETI", max_length=24)
    member_count = models.IntegerField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="The user to whom this character belongs."
    )
    last_esi_pull = models.DateTimeField(default=one_day_ago)
    def __str__(self):
        return f'{self.name}'

class Structure(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(default="Unknown Structure",max_length=64,null=False)
    owner_id = models.IntegerField()
    solar_system_id = models.IntegerField()
    type_id = models.IntegerField()
    last_seen = models.DateTimeField(auto_now=True)
    position_x = models.FloatField(
        null=True, default=None, blank=True, help_text="x position in the solar system"
    )
    position_y = models.FloatField(
        null=True, default=None, blank=True, help_text="y position in the solar system"
    )
    position_z = models.FloatField(
        null=True, default=None, blank=True, help_text="z position in the solar system"
    )
    def __str__(self):
        return f'{self.name}'


class CharacterPreferenceModel(PerInstancePreferenceModel):
    # note: you *have* to use the `instance` field
    instance = models.ForeignKey(Character,on_delete=models.CASCADE)

    class Meta:
        # Specifying the app_label here is mandatory for backward
        # compatibility reasons, see #96
        app_label = 'mogul_backend'


class Profit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,help_text="The user to whom this profit belongs.")
    transaction = models.ForeignKey(Transaction,on_delete=models.CASCADE,help_text="The transaction that created the profit.",null=True,related_name='profit_trans_row')
    item = models.ForeignKey(EveType,on_delete=models.CASCADE,help_text="The item involved on this profit row.",null=True)
    stock_data = models.JSONField()
    date = models.DateTimeField(null=True,auto_now_add=True)
    updated = models.DateTimeField(null=True,auto_now=True)
    amount = models.DecimalField(default=0,max_digits=20,decimal_places=2)
    quantity = models.IntegerField()
    station = models.BigIntegerField()
    taxes = models.DecimalField(default=0,max_digits=20,decimal_places=2)
    unit_tax = models.DecimalField(default=0,max_digits=20,decimal_places=2)
    tax_data = models.JSONField()
    objects = DataFrameManager()

    @property
    def profit_station(self):
        if(self.station > 70000000):
            # It's a structure, let's get that
            return Structure.objects.filter(id=self.station).first()
        else:
            return EveType.objects.filter(id=self.station).first()

class Stock(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,help_text="The user to whom this stock belongs.")
    transaction = models.ForeignKey(Transaction,on_delete=models.CASCADE,help_text="The transaction that created the stock.",null=True,related_name='stock_trans_row')
    item = models.ForeignKey(EveType,on_delete=models.CASCADE,help_text="The item involved on this stock row.",null=True)
    date = models.DateTimeField(null=True,auto_now_add=True)
    updated = models.DateTimeField(null=True,auto_now=True)
    amount = models.DecimalField(default=0,max_digits=20,decimal_places=2)
    quantity = models.IntegerField()
    station = models.BigIntegerField()
    taxes = models.DecimalField(default=0,max_digits=20,decimal_places=2)
    unit_tax = models.DecimalField(default=0,max_digits=20,decimal_places=2)
    tax_data = models.JSONField()