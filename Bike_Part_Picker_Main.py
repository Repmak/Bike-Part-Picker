from flask import Flask, render_template, request, redirect, session
import Bike_Part_Picker_Functions

dbfuncsinstance = Bike_Part_Picker_Functions.dbfuncs()
app = Flask(__name__)
app.secret_key = 'frfrong'


@app.route('/')  # DEFAULT UNUSED WEBPAGE.
def default():
    return redirect('/builder')  # REDIRECTS TO AVOID SHOWING EMPTY PAGE.


# ---------- BUILDER ROUTES ----------

@app.route('/builder')  # BUILDER WEBPAGE.
def builder():
    if session['userid'] is None:  # CHECKS IF THE USER IS LOGGED IN TO AN ACCOUNT.
        return redirect('/login')
    else:
        if session['listid'] is None:  # CHECKING IF A PART LIST IS ALREADY SELECTED.
            listid = dbfuncsinstance.autolistload(session['userid'])  # AUTOMATICALLY SELECTS A LIST BY THE USER.
            session['listid'] = listid
        clickedlist, partinfo = dbfuncsinstance.loadlistclick(session['listid'])  # clickedlist STORES ListID AND ListName. partinfo STORES ALL PART INFORMATION.
        listoptions = dbfuncsinstance.loadlistoptions(session['userid'])  # listoptions STORES ALL LISTS THAT THE USER CAN ACCESS FROM THE SIDEBAR.
        return render_template('builder.html', userid=session['userid'], username=session['username'], clickedlist=clickedlist, listoptions=listoptions, parts=partinfo)


@app.route('/selectpart', methods=['POST', 'GET'])
def selectpart():
    if request.method == 'POST':
        for values in request.form.items():  # FOR LOOP USED TO GET ALL VALUES THAT WERE SUBMITTED THROUGH THE FORM (SINCE WE DON'T KNOW WHAT CATEGORY WAS CLICKED ON). LOOP WILL ONLY ITERATE ONCE.
            category = values[0]
            if request.form[category] == 'Delete':  # DELETING A PART.
                dbfuncsinstance.deletepart(session['listid'], category)  # DELETES LIST, NOTHING RETURNED.
                return redirect('/builder')
            else:  # ADDING A PART.
                parts, error = dbfuncsinstance.retrieveparts(category)  # RETRIEVES ALL PARTS OF A GIVEN CATEGORY AND THEIR CORRESPONDING INFORMATION.
                return render_template('selectpart.html', userid=session['userid'], username=session['username'], categoryname=category, jsparts=parts)
    else:
        session['listid'] = None
        return redirect('/builder')


@app.route('/addpart', methods=['POST', 'GET'])
def addpart():
    if request.method == 'POST':
        for values in request.form.items():  # FOR LOOP USED TO GET ALL VALUES THAT WERE SUBMITTED THROUGH THE FORM (SINCE WE DON'T KNOW WHAT CATEGORY WAS CLICKED ON). LOOP WILL ONLY ITERATE ONCE.
            partid = values[0]
            dbfuncsinstance.addpart(session['listid'], partid)  # ADDS PART TO THE LIST BY ADDING A RECORD IN THE BRIDGE TABLE PartLists.
            return redirect('/builder')
    else:
        session['listid'] = None
        return redirect('/')


@app.route('/selectlistbuilder', methods=['POST', 'GET'])
def selectlistbuilder():
    if request.method == "POST":
        for values in request.form.items():  # FOR LOOP USED TO GET ALL VALUES THAT WERE SUBMITTED THROUGH THE FORM (SINCE WE DON'T KNOW WHAT LIST WAS CLICKED ON). LOOP WILL ONLY ITERATE ONCE.
            session['listid'] = values[0]  # UPDATES listid SESSION ID (SO THAT THE SELECTED LIST'S INFORMATION IS DISPLAYED WHEN REDIRECTED TO THE 'BUILDER' WEBPAGE).
        return redirect('/builder')
    else:
        return redirect('/builder')


# ---------- MY PART LISTS ROUTES ----------

@app.route('/mypartlists', methods=['POST', 'GET'])  # MYPARTLISTS WEBPAGE.
def mypartlists():
    if session['userid'] is not None:
        if session['listid'] is None:  # CHECKING IF A PART LIST IS ALREADY SELECTED.
            autoselectedlistid = Bike_Part_Picker_Functions.dbfuncs.autolistload(session['userid'])  # AUTOMATICALLY SELECTS A LIST BY THE USER.
            session['listid'] = autoselectedlistid
        listinfo = dbfuncsinstance.loadlistinfo(session['listid'])  # listinfo STORES INFORMATION ABOUT THE SELECTED LIST.
        listoptions = dbfuncsinstance.loadlistoptions(session['userid'])  # listoptions STORES ALL LISTS THAT THE USER CAN ACCESS FROM THE SIDEBAR.
        return render_template('mypartlists.html', userid=session['userid'], username=session['username'], listinfo=listinfo[0], privacysetting=listinfo[0][3], listoptions=listoptions)
    else:
        return redirect('/login')


@app.route('/createlist', methods=['POST', 'GET'])
def createlist():
    if request.method == 'POST':
        partlistid = dbfuncsinstance.createlist(session['userid'])  # partlistid STORES THE LIST ID.
        session['listid'] = partlistid  # LIST ID RETRIEVED PREVIOUSLY IS SET TO THE SESSION KEY.
        return redirect('/mypartlists')
    else:
        return redirect('/builder')


@app.route('/deletelist', methods=['POST', 'GET'])
def deletelist():
    if request.method == 'POST':
        partlistid = dbfuncsinstance.deletelist(session['userid'], session['listid'])  # partlistid STORES THE LIST ID OF ANOTHER LIST, SINCE THE PREVIOUS LIST WAS DELETED.
        session['listid'] = partlistid  # LIST ID RETRIEVED PREVIOUSLY IS SET TO THE SESSION KEY.
        return redirect('/mypartlists')
    else:
        return redirect('/builder')


@app.route('/modifypartlistinfo', methods=['POST', 'GET'])
def modifypartlistinfo():
    if request.method == 'POST':
        if request.form.get('publicorpriv') is None:  # CHECKS IF THE PRIVACY SETTING SWITCH IS CHECKED OR NOT.
            privacysetting = 0
        else:
            privacysetting = 1
        error = dbfuncsinstance.modifylist(session['userid'], session['listid'], request.form.get('listname'), request.form.get('listdescr'), privacysetting)  # error STORES AN ERROR, IF THERE ARE ANY.
        if error is None:
            return redirect('/mypartlists')
        else:  # INSTEAD OF REDIRECTING TO '/mypartlists', LOAD WEBPAGE FROM THIS URL SO THAT error CAN BE PASSED AS A PARAMETER.
            listinfo = dbfuncsinstance.loadlistinfo(session['listid'])
            listoptions = dbfuncsinstance.loadlistoptions(session['userid'])
            return render_template('mypartlists.html', userid=session['userid'], username=session['username'], listinfo=listinfo[0], privacysetting=listinfo[0][3], listoptions=listoptions, listerror=error)
    else:
        return redirect('/builder')


@app.route('/selectlistmypartlists', methods=['POST', 'GET'])
def selectlistmypartlists():
    if request.method == 'POST':
        for values in request.form.items():  # FOR LOOP USED TO GET ALL VALUES THAT WERE SUBMITTED THROUGH THE FORM (SINCE WE DON'T KNOW WHAT LIST WAS CLICKED ON). LOOP WILL ONLY ITERATE ONCE.
            session['listid'] = values[0]  # UPDATES listid SESSION ID (SO THAT THE SELECTED LIST'S INFORMATION IS DISPLAYED WHEN REDIRECTED TO THE 'MY PART LISTS' WEBPAGE).
        return redirect('/mypartlists')
    else:
        session['listid'] = None
        return redirect('/mypartlists')


# ---------- COMPLETED BUILDS ROUTES ----------

@app.route('/completedbuilds')  # COMPLETED BUILDS WEBPAGE.
def completedbuilds():
    return render_template('completedbuilds.html', userid=session["userid"], username=session["username"])


# ---------- LOGIN, SIGN UP AND LOGOUT ROUTES ----------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = dbfuncsinstance.login(request.form.get('email'), request.form.get('password'))  # username STORES AN ARRAY, WHICH STORES THE USER ID AND THE USERNAME.
        if not username:  # IF username STORES None, THEN THE LOGIN DETAILS ARE INVALID.
            return render_template('login.html', loginerror='Invalid login details entered.')
        else:
            session['userid'] = username[0][0]  # SETTING BOTH KEYS TO THE USER ID AND USERNAME SO THAT THE USER IS LOGGED IN.
            session['username'] = username[0][1]
            return redirect('/builder')
    else:
        return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username, error = dbfuncsinstance.signup(request.form.get('email'), request.form.get('password'), request.form.get('username'))  # username STORES AN ARRAY, WHICH STORES THE USER ID AND THE USERNAME. error STORES ANY ERRORS THAT MIGHT BE PRODUCED (USERNAME ALREADY TAKEN)
        if not username:  # CHECKS IF USERNAME IS ALREADY TAKEN BY ANOTHER USER.
            return render_template('signup.html', loginerror=error)
        else:
            session['userid'] = username[0][0]  # SETTING BOTH KEYS TO THE USER ID AND USERNAME SO THAT THE USER IS LOGGED IN.
            session['username'] = username[0][1]
            return redirect('/builder')
    else:
        return render_template('signup.html')


@app.route('/logout')  # LOGS USER OUT
def logout():
    session['username'] = None  # username, userid AND listid ARE ALL SET TO None.
    session['userid'] = None
    session['listid'] = None
    return redirect('/login')  # REDIRECTS TO LOGIN PAGE SINCE NO USER IS CURRENTLY LOGGED IN.


if __name__ == "__main__":
    app.run(debug=True)











