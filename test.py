import datetime

from events import Failure, get_repair_by_id, get_review_by_id
from eventcontroller import EventController
from parcel_machine import ParcelMachine
from users import  User, get_user_by_id

pm = ParcelMachine(1)

f = Failure(Failure.FailureType.TouchScreenFailure, pm, datetime.datetime.now())

ec=EventController()
ec.add_failure(f)
ec.order_repair(pm)
ec.accept_repair(get_repair_by_id(1), get_user_by_id(1))
ec.do_repair(get_repair_by_id(1), get_user_by_id(1))
# ec.order_review(pm)
# ec.accept_review(get_review_by_id(1), get_user_by_id(1))
ec.do_review(get_review_by_id(1), get_user_by_id(1))
