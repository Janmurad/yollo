from django.urls import path
from .views import *
from .api_views import *

urlpatterns = [
    path('region/form', region_form, name='region_form'),
    path('region/index', region_index, name='region_index'), # type: ignore
    path('region/update/<str:pk>', region_update, name='region_update'),
    # path('image_upload', hotel_image_view, name='image_upload'),
    path('boxeslist', boxeslist, name='boxeslist'),
    path('boxesstatus/<str:status>', boxesstatus, name='boxesstatus'),
    path('boxesselected', box_selected_send, name='boxesselected'),
    path('boxselect/<str:pk>', box_select, name='boxselect'),
    path('success', success, name='success'),
    path('cratebox', create_box, name='createbox'),
    path('boxview/<str:pk>', box_view, name='boxview'),
    path('boxupdate/<str:pk>', box_update, name='boxupdate'),
    path('boxfromto/<str:pk>', box_fromto, name='boxfromto'),
    # notification ursl notification_update
    path('notification/index', notification_index, name="notification"),
    path('notification/form', notification_form, name="notification_form"),
    path('notification/update/<str:pk>', notification_update, name='notification_update'),
    # path('notification/view/<str:pk>', notification_view, name='notification_view'),
    # feedbac urls
    path('feedback/index', feedback_index, name="feedback"),
    path('feedback/form', feedback_form, name="feedback_form"),
    path('feedback/answer/<str:pk>', feedback_answer, name="feedback_answer"),
    # urls for API
    path('boxes', BoxesAPIList.as_view(), name='boxesapi'),
    path('boxes/<str:pk>', BoxesAPIList.as_view(), name='boxesapiupdate'),
    path('boxreject/<str:pk>', BoxReject.as_view(), name='BoxReject'),
    path('regions', RegionAPIList.as_view(), name='regionsapi'),
    # path('regioncreate', RegionCreate.as_view(), name='regioncreate'),
    path('regionshi', RegionHi.as_view(), name='regionshiapi'),
    path('regionscity', RegionCity.as_view(), name='regionscityapi'),
    # path('regionscity/<str:region_hi>', RegionCity.as_view(), name='regionscityhiapi'),    
    path('boxhistory/<str:pk>', BoxHistoryAPIList.as_view(), name='boxhistoryapi'),
    # feedback API urls
    path('feedback', FeedbackAPIList.as_view(), name='feedbackapi'),
    path('feedback/<int:pk>', FeedbackAPIList.as_view(), name='feedbackapi'),
    # notification API urls
    path('notification', NotificationList.as_view(), name='notificationapi'),
    path('notification/<int:pk>', NotificationList.as_view(), name='notificationapi'),
]


