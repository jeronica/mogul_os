# Create your tasks here

from celery import shared_task
from eveuniverse.models import EveType, EveRace
from esi.clients import EsiClientProvider
from esi.decorators import single_use_token,token_required,tokens_required
from esi.models import Token
from django.conf import settings
from django.utils import timezone
from mogul_backend.models import Transaction, Character, Order
from django.contrib.auth.models import User
from mogul_backend.helpers.orm import BulkCreateManager
from mogul_backend.datehelpers import one_hour_ago,one_day_ago

esi = EsiClientProvider(spec_file='mogul_auth/swagger.json')

@shared_task(name="importtransactions") # requires character_id and the user_id
def importtransactions(character_id, user_id):
    required_scopes = ['esi-wallet.read_character_wallet.v1']
    token = Token.get_token(character_id, required_scopes)
    user = User.objects.get(id=user_id)
    transresults = esi.client.Wallet.get_characters_character_id_wallet_transactions(
        # required parameter for endpoint
        character_id = character_id,
        # provide a valid access token, which wil be refresh the token if required
        token = token.valid_access_token()
    ).results()
    # Let's also get the last transaction from the user..
    try:
        lasttran = Transaction.objects.filter(user_id=user_id).latest('transaction_id')
        lasttran = lasttran.transaction_id
    except:
        lasttran = 0
    # Last transaction id got, let's start iterating yo
    bulk_mgr = BulkCreateManager(chunk_size=100)
    for trans in transresults:
        if trans.get('transaction_id') > lasttran:
            #we add here
            bulk_mgr.add(Transaction(
                client_id=trans.get('client_id'),
                date=trans.get('date'),
                is_buy=trans.get('is_buy'),
                is_personal=trans.get('is_personal'),
                journal_ref_id=trans.get('journal_ref_id'),
                location_id=trans.get('location_id'),
                quantity=trans.get('quantity'),
                transaction_id=trans.get('transaction_id'),
                type_id=trans.get('type_id'),
                unit_price=trans.get('unit_price'),
                user=user,
                ))
        else:
            #We've reached the breaking point, aka we are up to date..
            break


    bulk_mgr.done()
    return character_id
    #maybe we add the next task (aka processing, or flag the user for processing..)

@shared_task(name="importorders") # requires character_id and the user_id
def importorders(character_id, user_id):
    required_scopes = ['esi-wallet.read_character_wallet.v1']
    token = Token.get_token(character_id, required_scopes)
    user = User.objects.get(id=user_id)
    ordresults = esi.client.Market.get_characters_character_id_orders(
        # required parameter for endpoint
        character_id = character_id,
        # provide a valid access token, which wil be refresh the token if required
        token = token.valid_access_token()
    ).results()
    # Let's also get the last transaction from the user..
    try:
        lastord = Order.objects.filter(user_id=user_id).latest('order_id')
        lastord = lastord.order_id
    except:
        lastord = 0
    # Last transaction id got, let's start iterating yo
    bulk_mgr = BulkCreateManager(chunk_size=100)
    for ord in ordresults:
        if ord.get('order_id') > lastord:
            #It's a new order..
            bulk_mgr.add(Order(
                duration=ord.get('duration'),
                is_buy_order=ord.get('is_buy_order'),
                is_corporation=ord.get('is_corporation'),
                issued=ord.get('issued'),
                location_id=ord.get('location_id'),
                min_volume=ord.get('min_volume'),
                order_id=ord.get('order_id'),
                price=ord.get('price'),
                range=ord.get('range'),
                region_id=ord.get('region_id'),
                type_id=ord.get('type_id'),
                volume_remain=ord.get('volume_remain'),
                volume_total=ord.get('volume_total'),
                user=user,
                ))
        else:
            # It's an order we probably gotta update!
            crap = True


    bulk_mgr.done()
    return character_id
    #maybe we add the next task (aka processing, or flag the user for processing..)

@shared_task(name="pullusercharacters") # requires a user_id
def pullusercharacters(user_id):
    # let's first get user's characters
    tokenchars = []
    tokenlist = Token.objects.filter(user=user_id).values('character_id')
    user = User.objects.get(id=user_id)
    for toke in tokenlist:
        #let's also add the user's character to the database
        character_id = toke.get('character_id')
        char = Character.objects.get_or_create(character_id = character_id,user = user)
    #Okay, we've update the user's character list.. Let's get some characters that need updating!
    topull = Character.objects.filter(user=user_id,last_esi_pull__lt=one_hour_ago()).values('character_id') #will eventually add some filtering for last_esi_pull
    if len(topull) < 1:
        return True
    try:
        pullthis = [pullme.get('character_id') for pullme in topull]
        for char in pullthis:
            importtransactions.delay(char, user_id)
            importorders.delay(char,user_id)
            #Let's also update the character
            Character.objects.filter(character_id=char).update(last_esi_pull=timezone.now())
    except:
        return True
    return character_id
    #maybe we add the next task (aka processing, or flag the user for processing..)

@shared_task(name="pullusers") # requires a user_id
def pullusers():
    # let's first get user's characters
    userlist = User.objects.all()
    for getuser in userlist:
        pullusercharacters.delay(getuser.id)
    return True