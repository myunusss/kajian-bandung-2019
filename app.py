from flask import Flask, request
from flask_restful import Resource, Api

# RESOURCES
from resources.sign_in import SignIn
from resources.sign_out import SignOut
from resources.order import GetRecentOrder, NextOrder, DetailOrder
from resources.order_item import OrderListItem
from resources.booking import BookingList
from resources.action_order import AcceptOrder, AcceptAtRoom, GuestAtRoom, BeginTreatment, EndTreatment, LeaveRoom
from resources.session import AddSession
from resources.search_item import SearchItem
from resources.add_new_item import AddNewItem
from resources.change_password import ChangePassword
from resources.therapist_status import ListTherapistStatus, UpdateTherapistStatus
from resources.therapist_info import TherapistInfo
# delete soon
from resources.app_auth import AppAuth

app = Flask(__name__)
api = Api(app)

api.add_resource(SignIn, '/sign_in')
api.add_resource(SignOut, '/sign_out')
api.add_resource(GetRecentOrder, '/recent_order')
api.add_resource(NextOrder, '/next_order')
api.add_resource(BookingList, '/booking_list')
api.add_resource(AcceptOrder, '/accept_order')
api.add_resource(AcceptAtRoom, '/at_room')
api.add_resource(BeginTreatment, '/begin_treatment')
api.add_resource(EndTreatment, '/end_treatment')
api.add_resource(AddSession, '/add_session')
api.add_resource(LeaveRoom, '/leave_room')
api.add_resource(DetailOrder, '/detail_order')
api.add_resource(GuestAtRoom, '/guest_at_room')
api.add_resource(OrderListItem, '/order_list_item')
api.add_resource(SearchItem, '/search_item')
api.add_resource(AddNewItem, '/add_new_item')
api.add_resource(ChangePassword, '/change_password')
api.add_resource(ListTherapistStatus, '/list_therapist_status')
api.add_resource(UpdateTherapistStatus, '/update_therapist_status')
api.add_resource(TherapistInfo, '/therapist_info')

# delete soon
api.add_resource(AppAuth, '/app_auth')

if __name__ == '__main__':
    app.run(debug=True)