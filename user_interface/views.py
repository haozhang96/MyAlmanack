from django.views.generic import TemplateView
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from database.views import *
from user_interface.forms import *
import base64
import os
import json
from authentication.firebase import get_session_claims
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


def getDummyData(dummy_file):
	dummy_dir = "/user_interface/static/dummy_data/"
	extension = ".txt"
	cwd = os.getcwd()
	path = cwd + dummy_dir + dummy_file + extension
	data = open(path, "r").readlines()
	grid = []
	for line in data:
		curr = line.split("\t")
		for i in range(0,len(curr)):
			curr[i] = curr[i].replace("\n", "")
			curr[i] = curr[i].replace("\"", "")
		if len(curr[0]) == 0:
			continue
		grid.append(curr)
	headers = grid[0]
	structs = []
	for i in range(1, len(grid)):
		curr_struct = {}
		for j in range(0, len(grid[i])):
			curr_struct[headers[j]] = grid[i][j]
		structs.append(curr_struct)
	return structs

def getProfilePictureBase64(file_name):
	picture_dir = "/user_interface/static/profile_pictures/"
	extension = ".png"
	cwd = os.getcwd()
	file_loc = cwd + picture_dir + file_name + extension
	encoded_string = ""
	with open(file_loc, "rb") as image_file:
		encoded_string = base64.b64encode(image_file.read())
	retval = encoded_string.decode('utf-8')
	return retval

def getCurrUser(profile_json, firebase_id):
	print("GET", firebase_id)
	for user in profile_json:
		print(user["firebase_id"])
		if user["firebase_id"].replace(" ", "") == str(firebase_id).replace(" ", ""):
			return [user]
	return [{}]

def filterDummyEventsAlias(eventstructs, alias):
	ret_events = []
	for temp_event in eventstructs:
		if temp_event["event_creator_alias"] == alias:
			ret_events.append(temp_event)
	return ret_events

def filterDummyContactsAlias(contactstructs, contact_list_id):
	for temp_contact in contactstructs:
		if temp_contact["contact_list_id"] == contact_list_id:
			return temp_contact
	return None

def genHiddenEvent(passed_event):
	hiddenstruct = {}
	hiddenstruct["event_id"] = "-1"
	hiddenstruct["description"] = "Hidden"
	hiddenstruct["participating_users"] = ""
	hiddenstruct["event_admins"] = ""
	hiddenstruct["whitelist"] = ""
	hiddenstruct["blacklist"] = ""
	hiddenstruct["start_date"] = passed_event["start_date"]
	hiddenstruct["end_date"] = passed_event["end_date"]
	hiddenstruct["event_creator_alias"] = passed_event["event_creator_alias"]
	hiddenstruct["event_creator_firebase_id"] = passed_event["event_creator_firebase_id"]
	hiddenstruct["isHidden"] = "true"
	return hiddenstruct


def filterAccessFriendEvents(friend_events, user_alias):
	print("FILTER FRIEND EVENTS", user_alias)
	ret_filtered = []
	for temp_event in friend_events:
		whitelist_str = temp_event["whitelist"].replace(" ", "")
		blacklist_str = temp_event["blacklist"].replace(" ", "")
		whitelist = whitelist_str.split(",");
		blacklist = blacklist_str.split(",");
		whitelist_empty = False
		blacklist_empty = False
		if len(whitelist_str) == 0:
			whitelist_empty = True
		if len(blacklist_str) == 0:
			blacklist_empty = True
		if whitelist_empty and blacklist_empty == False:
			isblacklisted = False
			for blacklisted in blacklist:
				if blacklisted == user_alias:
					isblacklisted = True
					break
			if isblacklisted:
				hiddenstruct = genHiddenEvent(temp_event)
				ret_filtered.append(hiddenstruct)
				continue
		if whitelist_empty == False and blacklist_empty:
			iswhitelisted = False
			for whitelisted in whitelist:
				if whitelisted == user_alias:
					iswhitelisted = True
					break
			if iswhitelisted == False:
				hiddenstruct = genHiddenEvent(temp_event)
				ret_filtered.append(hiddenstruct)
				continue
		if whitelist_empty == False and blacklist_empty == False:
			continue
		ret_filtered.append(temp_event)
	return ret_filtered

def getCurrentFirebaseId(request):
	return request.user.username;

def nullAlias(request):
	p = ProfileView()
	if(request.method == "POST"):
		return p.post(request, "")
	return p.get(request, "")

def nullGroup(request):
	g = GroupView()
	if(request.method == "POST"):
		return g.post(request, "")
	return g.get(request, "")

def redirForce(request):
	e = EditProfileView()
	return e.get(request)

def getFirebaseIDAliasDummy(user_structs, alias):
	for temp_user in user_structs:
		if(temp_user["alias"] == alias):
			return temp_user["firebase_id"]
	return -1

class ProfileView(TemplateView):
	template_name = 'user_interface/profile.html'

	def dummy(self, event_form, request, alias_requested):

		search_form = SearchForm()
		eventstructs = getDummyData("event_table")
		eventjson = str(json.dumps(eventstructs))
		profilestructs = getDummyData("profile_table")
		profilejson = str(json.dumps(profilestructs))
		contactstructs = getDummyData("contact_list_table")
		contactjson = str(json.dumps(contactstructs))

		user_firebase_id = getCurrentFirebaseId(request)
		isValid = validFirebaseId(user_firebase_id);
		print("isvalid_id", isValid)

		if(isValid == True):
			return redirForce(request)


		profile_data = getProfileData(user_firebase_id)
		currentuserstruct = getCurrUser(profilestructs, user_firebase_id)
		print(currentuserstruct)
		if bool(currentuserstruct[0]) == False:
			return redirForce(request)
		user_alias = currentuserstruct[0]["alias"]
		user_selected = currentuserstruct

		if(alias_requested != ""):
			print("alias_requested:", alias_requested)
			user_alias = alias_requested
			sel_id = getFirebaseIDAliasDummy(profilestructs, alias_requested)
			user_selected = getCurrUser(profilestructs, sel_id)
			print("user_selected", user_selected)


		currentuserjson = str(json.dumps(currentuserstruct))
		user_events = filterDummyEventsAlias(eventstructs, user_alias)
		user_contact_list_id = currentuserstruct[0]["contact_list_id"]
		user_contact_list = filterDummyContactsAlias(contactstructs, user_contact_list_id)
		friend_names = user_contact_list["contact_names"].replace(" ", "").split(",")
		print(friend_names)
		friend_events = []
		is_friend = "false"
		prof_mode = "friend"
		if(currentuserstruct[0]["alias"] == user_alias or alias_requested == ""):
			prof_mode = "self"
		else:
			prof_mode = "friend"
			if alias_requested in friend_names:
				is_friend = "true"
			else:
				is_friend = "false"


		for friend_alias in friend_names:
			curr_events = filterDummyEventsAlias(eventstructs, friend_alias)
			for temp_event in curr_events:
				friend_events.append(temp_event)
		filtered_friend_events = filterAccessFriendEvents(friend_events, currentuserstruct[0]["alias"])

		user_events_json = str(json.dumps(user_events))
		filtered_friend_events_json = str(json.dumps(filtered_friend_events))
		user_contact_list_json = str(json.dumps(user_contact_list))
		print(user_contact_list)

		def_prof_pic = getProfilePictureBase64("default_profile")
		group_form = GroupForm()
		response = render(
			request=request,
			template_name=self.template_name,
			context={
				"event_form" : event_form,
				"search_form" : search_form,
				"group_form" : group_form,
				"dummy_events" : eventjson, 
				"dummy_profiles" : profilejson,
				"dummy_contacts" : contactjson,
				"user" : str(json.dumps(user_selected)),
				"user_events" : user_events_json,
				"member_events" : filtered_friend_events_json,
				"user_contact_list" : user_contact_list_json,
				"calendarFrame" : "sub_templates/calendarFrame.html",
				"default_profile" : def_prof_pic,
				"profile_mode" : prof_mode,
				"is_friend" : is_friend,
				"calendar_mode" : prof_mode,
			}
		)
		return response

	def get(self, request, alias):
		print("alias passed:", alias)
		firebase_id = getCurrentFirebaseId(request)
		print(firebase_id)
		event_form = EventForm()
		return self.dummy(event_form, request, alias)

	def post(self, request, alias):
		print("POST REQUESTED")
		switchType = request.POST.get('formType')
		print(request.POST.get('formType'))
		event_form = EventForm()
		formController(request)
		return self.dummy(event_form, request, alias)

class EditProfileView(TemplateView):
	template_name = 'user_interface/edit_profile.html'

	def dummy(self, request):
		search_form = SearchForm()
		group_form = GroupForm()
		edit_form = EditProfileForm()
		def_prof_pic = getProfilePictureBase64("default_profile")
		user_firebase_id = getCurrentFirebaseId(request)
			

		response = render(
			request=request,
			template_name=self.template_name,
			context={"edit_form" : edit_form, 
			"search_form" : search_form,
			"default_profile" : def_prof_pic,
			"group_form" : group_form
			}
		)
		return response

	def get(self, request):
		return self.dummy(request)

	def post(self, request):
		formController(request)
		return self.dummy(request)

class GroupView(TemplateView):
	template_name = 'user_interface/group.html'

	def dummy(self, request, group_name):
		user_firebase_id = getCurrentFirebaseId(request)
		isValid = validFirebaseId(user_firebase_id);
		print("isvalid_id", isValid)
		if(isValid == False):
			return redirForce(request)

		search_form = SearchForm()
		group_form = GroupForm()
		return render(
			request=request,
			template_name=self.template_name,
			context={"search_form" : search_form, 
				"calendarFrame" : "sub_templates/calendarFrame.html",
				"group_form" : group_form,
				"calendar_mode" : "group",}
		)


	def get(self, request, group_name):
		print("GROUP NAME:", group_name)
		return self.dummy(request, group_name)

	def post(self, request, group_name):
		print("GROUP NAME:", group_name)
		formController(request)
		return self.dummy(request, group_name)

class DefaultView(TemplateView):
	template_name = 'user_interface/default.html'

	def get(self, request):
		return render(
			request=request,
			template_name=self.template_name,
			context={}
		)

class SearchView(TemplateView):
	template_name = 'user_interface/search.html'

	def get(self, request):
		search_form = SearchForm()
		return render(
			request=request,
			template_name=self.template_name,
			context={"search_form" : search_form}
		)

	def post(self, request):
		search_form = SearchForm(request.POST)
		formController(request)
		events = searchEvents(search_term)
		friends = searchFriends(search_term)
		users = searchUsers(search_term)
		groups = searchGroups(search_term)
		return render(
			request=request,
			template_name=self.template_name,
			context={"search_form" : search_form,
				"events" : events,
				"friends" : friends,
				"users" : users,
				"groups" : groups
			}
		)

  
def formController(request):
	switchType = request.POST.get('formType')
	if(switchType == "SubmitEvent"):
		event_form_filled = EventForm(request.POST)
		print(event_form_filled)
	elif(switchType == "FriendRequest"):
		friend_form = FriendRequestForm(request.POST)
		print(friend_form)
	elif(switchType == "GroupRequest"):
		invite_form = GroupInviteForm(request.POST)
		print(invite_form)
	elif(switchType == "EditProfile"):
		editProfile(request)
	elif(switchType == "CreateGroup"):
		group_form = GroupForm(request.POST)
		print(group_form)

def editProfile(request):
	firebase_id = getCurrentFirebaseId(request)
	isValid = validFirebaseId(firebase_id)
	profile_form = EditProfileForm(request.POST)
	alias = profile_form['PIalias'].value()
	phone_num = [profile_form['PIphone'].value()]
	last_name = profile_form['PIlast'].value()
	first_name = profile_form['PIfirst'].value()
	email = [profile_form['PIemail'].value()]
	birth_date = profile_form['PIbirthday'].value()
	organization = profile_form['PIorganization'].value()
	print("\n\n\n")
	print(type(organization), organization)
	user_desc = profile_form['PIdescription'].value()
	print("BELOW:")
	print(firebase_id, alias, phone_num, last_name, first_name,
		email, birth_date, organization, user_desc)
	print("\n\n\n")
	if(isValid):
		# Modify current user
		editProfileData(firebase_id, alias, phone_num, last_name, first_name,
		email, birth_date, organization, user_desc)
	else:
		# Create new user
		"""def createProfileData(firebase_id, alias, phone_num, last_name, first_name,
	email, birth_date, organization, user_desc):"""
		# createProfileData(firebase_id, 'heyjustin', ['callme'], 'wink', 'wonk',
		# ['email'], '121312123', 'organization', 'user_desc')
		createProfileData(firebase_id, alias, phone_num, last_name, first_name,
		email, birth_date, organization, user_desc)
