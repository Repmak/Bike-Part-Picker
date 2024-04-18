import pyodbc
import datetime


class dbfuncs:
    def __init__(self):
        try:
            self.cnxn = pyodbc.connect("DRIVER={SQL Server}; Server=localhost\SQLEXPRESS; Database=master; Trusted_Connection=True;")  # CONNECTION STRING.
            self.cursor = self.cnxn.cursor()  # cursor IS USED FOR RETRIEVING AND MANIPULATING DATA.
        except pyodbc.DatabaseError as connectionerror:
            print("{}".format(connectionerror))

    # LOGGING IN AND SIGNING UP FUNCTIONS.

    def login(self, email, password):  # FUNCTION USED TO LOGIN TO AN EXISTING ACCOUNT.
        email = email.replace("'", "''")  # REPLACES ALL SINGLE QUOTATION MARKS WITH TWO QUOTATION MARKS (SO THAT SQL DOESN'T TREAT THE QUOTATION MARK AS THE END OF THE QUERY).
        password = password.replace("'", "''")
        sqlstatement = f'SELECT UserID, Username FROM UserInfo WHERE Email = \'{email}\' AND Passw = \'{password}\''  # SEARCHES FOR A RECORD WITH MATCHING CREDENTIALS
        self.cursor.execute(sqlstatement)
        userinfo = self.cursor.fetchall()
        return userinfo  # RETURNS EMPTY ARRAY (IF CREDENTIALS ARE INVALID) OR UserID (IF CREDENTIALS ARE VALID).

    def signup(self, email, password, username):  # FUNCTION USED TO CREATE AN ACCOUNT.
        email = email.replace("'", "''")  # REPLACES ALL SINGLE QUOTATION MARKS WITH TWO QUOTATION MARKS (SO THAT SQL DOESN'T TREAT THE QUOTATION MARK AS THE END OF THE QUERY).
        password = password.replace("'", "''")
        username = username.replace("'", "''")
        emailvalid = False  # FLAGS USED LATER FOR VALIDATION.
        usernamevalid = False

        sqlstatement = f'SELECT * FROM UserInfo WHERE Email = \'{email}\''
        self.cursor.execute(sqlstatement)
        userinfo = self.cursor.fetchall()
        if not userinfo:  # CHECKS IF THE ENTERED EMAIL ADDRESS IS ALREADY IN USE.
            emailvalid = True

        sqlstatement = f'SELECT * FROM UserInfo WHERE Username = \'{username}\''
        self.cursor.execute(sqlstatement)
        userinfo = self.cursor.fetchall()
        if not userinfo:  # CHECKS IF THE ENTERED USERNAME IS ALREADY IN USE.
            usernamevalid = True

        if emailvalid and usernamevalid:  # IF BOTH FLAGS ARE TRUE, INSERT DATA.
            sqlstatement = f'INSERT INTO UserInfo VALUES (\'{username}\', \'{email}\', \'{password}\')'
            self.cursor.execute(sqlstatement)
            self.cnxn.commit()  # COMMIT CHANGES TO DATABASE.
            sqlstatement = f'SELECT UserID, Username FROM UserInfo WHERE Email = \'{email}\' AND Passw = \'{password}\''  # RECORDS NEEDS TO BE SEARCHED RIGHT AFTER BEING INSERTED TO RETRIEVE THE ASSIGNED UserID.
            self.cursor.execute(sqlstatement)
            userinfo = self.cursor.fetchall()
            return userinfo, None  # RETURNS THE UserID AND Username AS AN ARRAY. ALSO RETURNS None AS THERE ARE NO ERRORS.
        else:
            if not emailvalid and not usernamevalid:  # OUTPUTS CORRESPONDING ERRORS DEPENDING ON WHAT FLAGS ARE SET TO FALSE. NO UserID OR Username ARE RETURNED.
                return None, "Email and username already in use."
            elif not emailvalid and usernamevalid:
                return None, "Email already in use."
            else:
                return None, "Username already in use."

    # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # 'BUILDER' WEBPAGE RELATED FUNCTIONS.

    def loadlistclick(self, partlistid):  # FUNCTION USED TO LOAD ALL PARTS TO A SELECTED PART LIST.
        sqlstatement = f'SELECT ListID, ListName FROM UserSavedLists WHERE ListID = \'{partlistid}\''  # RETRIEVES ListID AND ListName OF CLICKED LIST.
        self.cursor.execute(sqlstatement)
        clickedlist = self.cursor.fetchall()

        sqlstatement = f'SELECT PartID FROM PartLists WHERE ListID = \'{clickedlist[0][0]}\''  # RETRIEVES ALL RECORDS FROM THE BRIDGE TABLE PartLists THAT HAVE THE CORRESPONDING ListID.
        self.cursor.execute(sqlstatement)
        partids = self.cursor.fetchall()
        partinfo = []  # WILL BE USED TO STORE ALL PARTS.

        for j in range(0, len(partids)):  # LOOPS THROUGH partids TO RETRIEVE ALL INFORMATION.
            sqlstatement = f'SELECT * FROM BikeParts WHERE PartID = \'{partids[j][0]}\''
            self.cursor.execute(sqlstatement)
            partinfo1 = self.cursor.fetchall()
            sqlstatement = f'SELECT Price, PriceDate, WebsiteURL, Retailer FROM PriceChanges WHERE PartID = \'{partids[j][0]}\' ORDER BY PriceDate ASC'  # SORTED BY ASCENDING DATE SO THAT THE MOST RECENT PRICES CAN BE EASILY FOUND BY INDEX.
            self.cursor.execute(sqlstatement)
            partinfo2 = self.cursor.fetchall()
            if not partinfo2:  # NO PRICING INFORMATION WHATSOEVER, SO SET ALL VALUES TO '-'.
                temppartinfo = [partinfo1[0][0], partinfo1[0][3], partinfo1[0][1], partinfo1[0][2], '-', '-', '-', '-']
            # partinfo FORMAT: PartID, PartMainCategory, PartName, PartDescr, Price, PriceDate, WebsiteURL, Retailer
            else:  # MOST RECENT PRICING INFORMATION ADDED TO THE ARRAY.
                temppartinfo = [partinfo1[0][0], partinfo1[0][3], partinfo1[0][1], partinfo1[0][2], '£' + str(partinfo2[0][0]), str(partinfo2[0][1]), partinfo2[0][2], partinfo2[0][3]]
            partinfo.append(temppartinfo)
        return clickedlist, partinfo  # RETURNS ListID, ListName AND ALL PART INFORMATION IN THE LIST AS TWO SEPARATE ARRAYS.

    def retrieveparts(self, category):  # FUNCTION USED TO RETRIEVE ALL PARTS THAT CAN BE ADDED FOR A SELECTED CATEGORY.
        partinfo = []  # WILL BE USED TO STORE ALL PARTS.
        sqlstatement = f'SELECT CategoryID FROM Categories WHERE CategoryName = \'{category}\''  # RETRIEVES CategoryID TO BE USED LATER WHEN SEARCHING FOR PARTS.
        self.cursor.execute(sqlstatement)
        categoryid = self.cursor.fetchall()

        sqlstatement = f'SELECT * FROM BikeParts WHERE PartMainCategory = \'{categoryid[0][0]}\''  # RETRIEVES ALL RECORDS CORRESPONDING TO THE CategoryID.
        self.cursor.execute(sqlstatement)
        parts = self.cursor.fetchall()

        for i in range(0, len(parts)):  # LOOPS THROUGH ALL PARTS TO CHECK FOR PRICING INFORMATION.
            sqlstatement = f'SELECT Price, PriceDate, WebsiteURL, Retailer FROM PriceChanges WHERE PartID = \'{parts[i][0]}\' ORDER BY PriceDate ASC'  # SORTED BY ASCENDING DATE SO THAT THE MOST RECENT PRICES CAN BE EASILY FOUND BY INDEX.
            self.cursor.execute(sqlstatement)
            partinfotemp = self.cursor.fetchall()
            if len(partinfotemp) >= 2:  # CHECKS IF THERE ARE AT LEAST 2 RECORDED PRICES TO CALCULATE PRICE CHANGE.
                # FINDING PRICE DIFFERENCE.
                newprice = str(partinfotemp[0][0])
                oldprice = str(partinfotemp[1][0])
                percentagechange = ((float(newprice) - float(oldprice)) / float(oldprice)) * 100  # PERCENTAGE CHANGE FORMULA.
                # APPENDING PRICING INFORMATION TO partinfo.
                partinfo.append([parts[i][0], parts[i][1], parts[i][2], parts[i][3], '£' + str(partinfotemp[0][0]), str(partinfotemp[0][1]), partinfotemp[0][2], partinfotemp[0][3], str(round(percentagechange, 2)) + '%'])
            elif len(partinfotemp) == 1:  # ONLY 1 RECORDED PRICE, SO PRICE CHANGE IS AUTOMATICALLY SET TO 0.00%.
                partinfo.append([parts[i][0], parts[i][1], parts[i][2], parts[i][3], '£' + str(partinfotemp[0][0]), str(partinfotemp[0][1]), partinfotemp[0][2], partinfotemp[0][3], '0.00%'])
            else:  # NO PRICING INFORMATION WHATSOEVER, SO SET ALL VALUES TO '-' OR 0 AS REQUIRED.
                partinfo.append([parts[i][0], parts[i][1], parts[i][2], parts[i][3], '-', '-', 0, '-', '-'])
        return partinfo, None  # RETURNS ALL PART INFORMATION AS A 2D ARRAY. EACH SUB ARRAY HAS THE FOLLOWING FORMAT: [PartID, PartName, PartDesc, Price, PriceDate, WebsiteURL, Retailer, PercentageChange].

    def addpart(self, listid, partid):  # FUNCTION USED TO ADD A PART TO A LIST.
        sqlstatement = f'INSERT INTO PartLists VALUES (\'{partid}\', \'{listid}\')'  # INSERTS A RECORD TO THE BRIDGE TABLE.
        self.cursor.execute(sqlstatement)
        self.cnxn.commit()  # COMMIT CHANGES TO DATABASE.

    def deletepart(self, partlistid, category):  # FUNCTION USED TO DELETE A PART FROM A LIST.
        sqlstatement = f'SELECT PartID FROM BikeParts WHERE PartMainCategory = (SELECT CategoryID FROM Categories WHERE CategoryName = \'{category}\')'  # RETRIEVES PartID OF ALL PARTS FROM A GIVEN CATEGORY.
        self.cursor.execute(sqlstatement)
        partids = self.cursor.fetchall()
        for partid in partids:  # STARTS A FOR LOOP TO FIND A RECORD FROM THE BRIDGE TABLE THAT IS LINKED TO PartID AND ListID.
            sqlstatement = f'SELECT PartListID FROM PartLists WHERE PartID = \'{partid[0]}\' AND ListID = \'{partlistid}\''
            self.cursor.execute(sqlstatement)
            record = self.cursor.fetchall()
            if record:  # CHECKS THAT RECORD IS NOT EMPTY.
                sqlstatement = f'DELETE FROM PartLists WHERE PartListID = \'{record[0][0]}\''  # DELETES A RECORD FROM THE BRIDGE TABLE.
                self.cursor.execute(sqlstatement)
                self.cnxn.commit()  # COMMIT CHANGES TO DATABASE.

    # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # 'MYPARTLISTS' WEBPAGE RELATED FUNCTIONS.

    def loadlistinfo(self, partlistid):  # FUNCTION USED TO RETRIEVE ALL LIST INFORMATION.
        sqlstatement = f'SELECT * FROM UserSavedLists WHERE ListID = \'{partlistid}\''
        self.cursor.execute(sqlstatement)
        listinfo = self.cursor.fetchall()
        listinfo[0][2] = str(listinfo[0][2])  # CONVERTS DATE FROM smalldatetime FORMAT TO A STRING.
        return listinfo  # RETURNS LIST INFORMATION.

    def modifylist(self, userid, partlistid, partlistname, partlistdescr, privacysetting):  # FUNCTION USED TO MODIFY UserSavedList RECORD.
        if 3 <= len(partlistname) <= 50 and 3 <= len(partlistdescr) <= 1000:  # CHECKS THAT THE LIST NAME AND DESCRIPTION ARE WITHIN THE PERMITTED LENGTH.
            sqlstatement = f'SELECT ListID, ListName FROM UserSavedLists WHERE UserID = \'{userid}\''
            self.cursor.execute(sqlstatement)
            listinfo = self.cursor.fetchall()
            for listname in listinfo:  # CHECKS THAT THE NEW PART LIST NAME IS NOT ALREADY IN USE.
                if listname[1] == partlistname:  # FIRST IF STATEMENT CHECKS IF THE NEW PART LIST NAME MATCHES ANOTHER LIST NAME.
                    if str(listname[0]) != str(partlistid):  # SECOND IF STATEMENT CHECKS THAT, IF TWO NAMES DO MATCH, THEY AREN'T THE SAME LIST.
                        return 'This list name is already used for another list.'  # RETURNS ERROR MESSAGE.
            sqlstatement = f'UPDATE UserSavedLists SET ListName = \'{partlistname}\', DateLastSaved = \'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\', PublicOrPrivate = \'{privacysetting}\', ListDescr = \'{partlistdescr}\' WHERE ListID = \'{partlistid}\''  # UPDATES RECORD WITH ENTERED INFORMATION.
            self.cursor.execute(sqlstatement)
            self.cnxn.commit()  # COMMIT CHANGES TO DATABASE.
            return None  # NO ERRORS TO RETURN.
        else:
            return 'List name or description are of invalid length.'  # RETURNS ERROR MESSAGE.

    def createlist(self, userid):  # FUNCTION USED TO CREATE A LIST.
        sqlstatement = f'SELECT ListName FROM UserSavedLists WHERE UserID = \'{userid}\''
        self.cursor.execute(sqlstatement)
        listnames = self.cursor.fetchall()
        formattedlistnames = []
        for listname in listnames:  # LOOPS THROUGH listnames AND APPENDS ALL LIST NAMES TO A 1D ARRAY.
            formattedlistnames.append(listname[0])
        flag = False  # FLAG WILL BE SET TO TRUE ONCE AN ALLOWED LIST NAME IS FOUND.
        i = 1  # WILL BE CONCATENATED TO THE LIST NAME (MyPartList(i)).
        listname = 'MyPartList'  # DEFAULT LIST NAME.
        if 'MyPartList' in formattedlistnames:
            while not flag:
                flag = True
                if 'MyPartList(' + str(i) + ')' in formattedlistnames:  # CHECKS IF LIST NAME IS ALREADY IN USE.
                    flag = False
                    i += 1  # NUMBER INCREMENTED SINCE 'MyPartList(i)' IS ALREADY IN USE.
                else:
                    listname = 'MyPartList(' + str(i) + ')'
        sqlstatement = f'INSERT INTO UserSavedLists VALUES (\'{listname}\', \'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\', \'0\', \'Your part list description\', \'{userid}\')'  # INSERTS NEW LIST INTO THE DATABASE.
        self.cursor.execute(sqlstatement)
        self.cnxn.commit()  # COMMIT CHANGES TO DATABASE.
        sqlstatement = f'SELECT ListID FROM UserSavedLists WHERE ListName = \'{listname}\' AND UserID = \'{userid}\''  # RETRIEVES ListID OF THE NEW LIST SINCE IT IS AUTO GENERATED.
        self.cursor.execute(sqlstatement)
        partlistid = self.cursor.fetchall()[0][0]
        return partlistid  # RETURNS ListID OF THE NEW LIST.

    def deletelist(self, userid, partlistid):  # FUNCTION USED TO DELETE A PART LIST.
        sqlstatement = f'DELETE FROM PartLists WHERE ListID = \'{partlistid}\''  # DELETES THE RECORDS LINKED TO THE ListID IN THE BRIDGE TABLE.
        self.cursor.execute(sqlstatement)
        self.cnxn.commit()  # COMMIT CHANGES TO DATABASE.
        sqlstatement = f'DELETE FROM UserSavedLists WHERE ListID = \'{partlistid}\''  # DELETE THE RECORD LINKED TO THE ListID FROM UserSavedLists.
        self.cursor.execute(sqlstatement)
        self.cnxn.commit()  # COMMIT CHANGES TO DATABASE.
        sqlstatement = f'SELECT ListID FROM UserSavedLists WHERE UserID = \'{userid}\''  # SELECTS ALL REMAINING LISTS UNDER THE USER.
        self.cursor.execute(sqlstatement)
        lists = self.cursor.fetchall()
        if not lists:  # ENSURES THAT AT LEAST ONE LIST IS CREATED UNDER THE USER'S ACCOUNT. OTHERWISE ERRORS WILL BE PRODUCED.
            partlistid = self.createlist(userid)  # WILL RUN createlist TO AUTOMATICALLY CREATE A NEW LIST IN THE CASE THAT THE USER DOESN'T HAVE AT LEAST ONE LIST CREATED.
            return partlistid
        else:
            return lists[0][0]  # RETURNS A DIFFERENT ListID (OTHERWISE THE SYSTEM WILL CRASH).

    # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # MULTI-USE FUNCTIONS

    def loadlistoptions(self, userid):  # FUNCTION USED TO LOAD ALL LISTS UNDER THE USER'S ACCOUNT. USED FOR THE SIDEBAR ON THE 'BUILDER' AND 'MYPARTLISTS' WEBPAGES.
        sqlstatement = f'SELECT ListID, ListName FROM UserSavedLists WHERE UserID = \'{userid}\''
        self.cursor.execute(sqlstatement)
        listoptions = self.cursor.fetchall()
        return listoptions  # RETURNS ALL RELEVANT LIST INFORMATION (ListID, ListName) AS A 2D ARRAY.

    def autolistload(self, userid):  # FUNCTION USED AS AN EXTRA 'FAIL-SAFE'. WILL BE RUN IN THE CASE THAT THERE ISN'T ANY ListID STORED IN session["partlist"] IN THE MAIN FILE.
        sqlstatement = f'SELECT ListID FROM UserSavedLists WHERE UserID = \'{userid}\''  # SELECTS ALL LISTS CREATED BY THE USER.
        self.cursor.execute(sqlstatement)
        listselected = self.cursor.fetchall()
        if not listselected:  # CHECKS IF listselected IS EMPTY.
            partlistid = self.createlist(userid)  # WILL RUN createlist TO AUTOMATICALLY CREATE A NEW LIST IN THE CASE THAT THE USER DOESN'T HAVE AT LEAST ONE LIST CREATED.
            return partlistid  # RETURNS A ListID.
        else:
            return listselected[0][0]  # RETURNS A ListID.
