from django import forms
from django.contrib.postgres.forms import SimpleArrayField


class EventForm(forms.Form):
	EIname = forms.CharField(widget=forms.HiddenInput())
	EIdescription = forms.CharField(widget=forms.HiddenInput(), required=False)
	EIstart = forms.CharField(widget=forms.HiddenInput())
	EIend = forms.CharField(widget=forms.HiddenInput())
	# Split manually
	EIinvite = forms.CharField(widget=forms.HiddenInput(), required=False)
	EIwhitelist = forms.CharField(widget=forms.HiddenInput(), required=False)
	EIblacklist = forms.CharField(widget=forms.HiddenInput(), required=False)
	EIrepeat = forms.CharField(widget=forms.HiddenInput(), required=False)
	EIrepeat_pattern = forms.CharField(widget=forms.HiddenInput(), required=False)

class EditEventForm(forms.Form):
	EIediteventid = forms.CharField(widget=forms.HiddenInput())
	EIeditname = forms.CharField(widget=forms.HiddenInput())
	EIeditdescription = forms.CharField(widget=forms.HiddenInput(), required=False)
	EIeditstart = forms.CharField(widget=forms.HiddenInput())
	EIeditend = forms.CharField(widget=forms.HiddenInput())

class EditRepeatEventForm(forms.Form):
	EIeditrepeateventid = forms.CharField(widget=forms.HiddenInput())
	EIeditrepeatname = forms.CharField(widget=forms.HiddenInput())
	EIeditrepeatdescription = forms.CharField(widget=forms.HiddenInput(), required=False)
	EIeditrepeatstart = forms.CharField(widget=forms.HiddenInput())
	EIeditrepeatend = forms.CharField(widget=forms.HiddenInput())
	EIeditrepeat_pattern = forms.CharField(widget=forms.HiddenInput())

class EventRespondRequest(forms.Form):
	EIinvite_id = forms.CharField(widget=forms.HiddenInput())
	EIaction = forms.CharField(widget=forms.HiddenInput())

class GroupForm(forms.Form):
	GIname = forms.CharField(widget=forms.HiddenInput())
	GIdescription = forms.CharField(widget=forms.HiddenInput(), required=False)
	GIinvite = forms.CharField(widget=forms.HiddenInput(), required=False)

class GroupInviteMembersForm(forms.Form):
	GIname = forms.CharField(widget=forms.HiddenInput())
	GIinvite_members = forms.CharField(widget=forms.HiddenInput())

class GroupRespondRequest(forms.Form):
	GIinvite_id = forms.CharField(widget=forms.HiddenInput())
	GIaction = forms.CharField(widget=forms.HiddenInput())

class EditProfileForm(forms.Form):
	PIfirst = forms.CharField(widget=forms.HiddenInput())
	PIlast = forms.CharField(widget=forms.HiddenInput())
	# ADDED
	PIalias = forms.CharField(widget=forms.HiddenInput())
	PIemail = forms.CharField(widget=forms.HiddenInput(), required=False)
	PIbirthday = forms.CharField(widget=forms.HiddenInput())
	PIphone = forms.CharField(widget=forms.HiddenInput(), required=False)
	PIorganization = forms.CharField(widget=forms.HiddenInput(), required=False)
	PIdescription = forms.CharField(widget=forms.HiddenInput(), required=False)
	PIpicture = forms.CharField(widget=forms.HiddenInput(), required=False)

class FriendRequestForm(forms.Form):
	FIreqalias = forms.CharField(widget=forms.HiddenInput())

class FriendRemoveForm(forms.Form):
	FIremalias = forms.CharField(widget=forms.HiddenInput())

class FriendRespondRequest(forms.Form):
	FIinvite_id = forms.CharField(widget=forms.HiddenInput())
	FIaction = forms.CharField(widget=forms.HiddenInput())

class GroupJoinForm(forms.Form):
	GIreqname = forms.CharField(widget=forms.HiddenInput())

class GroupLeaveForm(forms.Form):
	GIremname = forms.CharField(widget=forms.HiddenInput())

class GroupInviteForm(forms.Form):
	GIalias = forms.CharField(widget=forms.HiddenInput())

class SearchForm(forms.Form):
	SIstring = forms.CharField(widget=forms.HiddenInput(), required=False)