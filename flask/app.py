from flask import Flask, render_template, flash, redirect, url_for, session, request, jsonify
import pyodbc
cnxn = pyodbc.connect(r'Driver={SQL Server};Server=VG00-2001;Database=Panel;Trusted_Connection=yes;')
import pandas as pd
import json
import pickle
import xlsxwriter
from flask_table import Table, Col
from flask import Flask, send_file, make_response , make_response
from flask_jsglue import JSGlue 
from io import BytesIO

import flask
import dash
import dash_core_components as dcc 
import dash_html_components as html



app = Flask(__name__)
jsglue = JSGlue(app)

@app.route('/')
def index():
    return render_template('home.html')

# PANEL QUERY
@app.route('/panel', methods=['GET', 'POST'])

def panel():
    print("a-aa")
    global data1
   
    global df

    query = 'select * from [Panel].[dbo].[Panel_daily]'
    cursor = cnxn.cursor()
    resultValue = cursor.execute(query)
    pat_details = cursor.fetchall()
    x=list(pat_details)

    x_tuple=[tuple(zz) for zz in x]
    df = pd.DataFrame(x_tuple,columns=['MRN','PAT_NAME','PAT_FIRST_NAME','PAT_LAST_NAME','Suffix','BIRTH_DATE','Age','Sex','LOC_NAME','Current PCP','Current PCP ID','Address1','Address2','CITY','State','ZIP','Home ph','Last_visit_date'])

    print df.columns
    if request.method == "POST":

        Location = request.form.get("Location")
        Provider = request.form.get("prov_name")
        start_date = request.form.get("start_Date")
        end_date = request.form["End_Date"]

        print type(end_date)
        print 'access get_providers2222'
        data1= df[(df['LOC_NAME']==Location) & (df['Current PCP']==Provider)  & (df['Last_visit_date'] > start_date) & (df['Last_visit_date'] <= end_date )]
        
        return render_template('resultsa.html',  tables=[data1.to_html(classes='data', header="true", index = False)])
    return render_template('panel.html')
 
@app.route('/excel_download/', methods=['GET', 'POST']) 
def excel_download():


    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    print data1
    data1.to_excel(writer, startrow = 0, merge_cells = False, sheet_name = "Sheet_1")
    workbook = writer.book
    worksheet = writer.sheets["Sheet_1"]
    writer.close()
    output.seek(0)
    #finally return the file
    return send_file(output, attachment_filename="testing1.xlsx", as_attachment=True)

 
providers = {
    'VG BEAVERTON': ['AGISIM, MIRIAM', 'BATLA, ADRIENNE', 'CARTER, TANYA', 'CROOKE, RACHAEL', 'CUMMINGS, KIMBERLY', 'GOEBEL, CAROLYN', 'GUERREIRO, JOHN', 'HILL, CHRISTIAN', 'HOLLES, GREGORY', 'HULL, MARION', 'KUMAR, SUNITI', 'LIETZKE, JENNIFER', 'MANLEY, MEGAN', 'MARTIN, CHRISTINE LOUISE', 'MCGOWN, PAUL', 'NEWMAN, SHEENA', 'No PCP', 'PETERS, JACOB', 'ROBERTS, TERA', 'SEASE, MARGARET', 'SOH, JASON D', 'TARDIFF, JON', 'VG DENTAL', 'VG INACTIVE', 'VG SBHC', 'WERNER, ALEXANDRA'],
    'VG BEAVERTON II': ['BATLA, ADRIENNE', 'CUMMINGS, KIMBERLY', 'MANLEY, MEGAN', 'NEWMAN, SHEENA', 'ROSEKRANS, ERIK', 'SEASE, MARGARET', 'VG INACTIVE', 'WERNER, ALEXANDRA'],                                                 
    'VG CENTRAL BILLING':['SMITH, ANGELIA'],
    'VG CENTURY HIGH': ['KUHN, DANA', 'No PCP', 'ROBERTS, TERA', 'SOH, JASON D', 'UNO, ELIZABETH M', 'VG DENTAL', 'VG INACTIVE', 'VG SBHC'],
    'VG CORNELIUS': ['AGISIM, MIRIAM', 'ARGUELLO BELLI, MELISSA', 'BAHERI, SASAN', 'BATLA, ADRIENNE', 'BURGHER, KRISTIN', 'DEFONTES, DEANE', 'DUGGAN, SHARON', 'GOLDSTEIN, MERIKA', 'HINDEL, INGEBORG', 'JACOBS, LYN C', 'KASS, SUSAN', 'KUMAR, SUNITI', 'LIETZKE, JENNIFER', 'MANLEY, MEGAN', 'MENNINGER, KATHRYN L', 'MOERKERKE, TREVOR', 'NEUBAUER, TANIA', 'No PCP', 'NUNM HEALTH CENTER-BEAVERTON', "O'LEARY, MAURA", 'PALMER, ANGELINE', 'PIPHER, MARGO', 'ROBERTS, TERA', 'UNO, ELIZABETH M', 'VG DENTAL', 'VG INACTIVE', 'VG SBHC', 'YOMAN, JILL R.'],
    'VG FOREST GROVE': ['INACTIVE', 'No PCP', 'VG INACTIVE', 'VG SBHC', 'WHALEN GARFIAS, LARISSA', 'YOMAN, JILL R.'],
    'VG HILLSBORO': [ 'ARGUELLO BELLI, MELISSA', 'AYRES, SOLEDAD TARKA', 'CARDEN, GEOFFREY', 'CASTILLO, TARRA', 'DUBOIS, DANIELLE', 'ELSTUN, KATHERINE', 'GALVEZ, EVA', 'GOLDSTEIN, MERIKA', 'JACKSON, LYDIA', 'KARPLUS, CAITLIN', 'KIM, MICHAEL', 'KING, JENNIFER A', 'KUHN, DANA', 'LAINEZ, IRMA', 'MARGESON, MEGAN', 'MCANDREW ANN, STEPHANIE', 'MCNAMARA, MARYALICE', 'MENNINGER, KATHRYN L', 'NERODA, KIMBERLEY', 'No PCP', "O'LEARY, MAURA", 'PALMER, ANGELINE', 'ROSEKRANS, ERIK', 'SCZECIENSKI, STANLEY J', 'SEASE, MARGARET', 'STRNAD, MELINDA J', 'SZCZESNIAK, REGINA', 'UNO, ELIZABETH M', 'VG DENTAL', 'VG INACTIVE', 'VG SBHC', 'WHALEN GARFIAS, LARISSA'],
    'VG MOBILE':[ 'CARTER, TANYA', 'CUMMINGS, KIMBERLY', 'GALVEZ, EVA', 'GOLDSTEIN, MERIKA', 'HINDEL, INGEBORG', 'LIETZKE, JENNIFER', 'MCGOWN, PAUL', 'MOERKERKE, TREVOR', 'No PCP', 'SEASE, MARGARET', 'SOH, JASON D', 'SZCZESNIAK, REGINA', 'UNO, ELIZABETH M', 'VG CAMP', 'VG INACTIVE', 'VG SBHC', 'YOMAN, JILL R.'],
    'VG NEWBERG':['CARTER, TANYA', 'KARPLUS, CAITLIN', 'MANLEY, MEGAN', 'MCGOWN, PAUL', 'MOERKERKE, TREVOR', 'NEUBAUER, TANIA', 'No PCP', 'PETERS, JACOB', 'PETERS, MARTIN', 'PIPHER, MARGO', 'SHEN, KEDY', 'SMITH, ANGELIA', 'VG CAMP', 'VG DENTAL', 'VG INACTIVE'],
    'VG TIGARD':['AGISIM, MIRIAM', 'METROPOLITAN PEDIATRICS GRESHAM', 'No PCP', 'PAPPAS, HANNAH', 'PRUETT, ELIZABETH', 'VG DENTAL', 'VG INACTIVE', 'VG SBHC'],
    'VG TUALATIN':['CHIN, MICHELLE A', 'HALL, DIANA', 'HAMILTON, ALICE', 'LESLIE, ROBIN RAE', 'MCCLISH, KAREN A', 'NGUYEN, QUOC H', 'No PCP', 'PRUETT, ELIZABETH', 'VG INACTIVE', 'VG SBHC'],
    'VG WILLAMINA':['CHANYAPUTHIPONG, SUNISA', 'FRODERMANN, MARY', 'KARPLUS, CAITLIN', 'LARGE, LANCE MD', 'No PCP', 'VG INACTIVE', 'VG SBHC'],
    'VG YAMHILL COUNTY': ['BAAR, FATIMA', 'CHANYAPUTHIPONG, SUNISA', 'CRAWFORD, KELLY', 'CROOKE, RACHAEL', 'ELSTUN, KATHERINE', 'FRODERMANN, MARY', 'HAMILTON, ALICE', 'HANSEN, CHRISTOPHER', 'HULL, MARION', 'KAISER ROCKWOOD MEDICAL OFFICE PCMOB-RKW', 'KARPLUS, CAITLIN', 'MANLEY, MEGAN', 'MCNAMARA, MARYALICE', 'NIESTRADT, HANNAH', 'No PCP', 'PIPHER, MARGO', 'SMITH, ANGELIA', 'SOH, JASON D', 'VG DENTAL', 'VG INACTIVE', 'YANG, NINA', 'YOMAN, JILL R.'],
    'VGB School Based': ['DUGGAN, SHARON', 'HILL, CHRISTIAN', 'KASS, SUSAN', 'MANLEY, MEGAN', 'MARGESON, MEGAN', 'MEZA, NANCY', 'No PCP', 'PETERS, JACOB', 'RATH, ROBERT S.  MD', 'SNYDER, KELVIN KENNETH', 'VG INACTIVE', 'VG SBHC'],
    'VGH Womens Clinic': ['ARCE, MONICA M', 'GOLDSTEIN, MERIKA', 'JACOBS, LYN C', 'KUHN, DANA', 'LAINEZ, IRMA', 'MOERKERKE, TREVOR', 'No PCP', 'STRNAD, MELINDA J', 'UNO, ELIZABETH M', 'VG INACTIVE', 'VG OB', 'WERNER, ALEXANDRA'],
    'VGLIFEWORKS BEAVERTON': ['CARTER, TANYA', 'MCANDREW ANN, STEPHANIE', 'VG INACTIVE'],
    'VGLW HILLSBORO':['NERODA, KIMBERLEY', 'VG INACTIVE'],
    'VGYC EVANS STREET': ['KARPLUS, CAITLIN', 'No PCP', 'POTTS, STEPHANIE HARPER', 'VG INACTIVE'],
    'VIRGINIA GARCIA MEMORIAL HC':['MENNINGER, KATHRYN L', 'No PCP', 'VG INACTIVE'],
    }

@app.route('/get_providers/<Location>', methods=['GET', 'POST'])
def get_providers(Location):
    print 'access get_providers'
    print Location
    print providers[Location]
    if Location not in providers:                                                                 
        return jsonify([])
    else:                                                                                    
        return jsonify(providers[Location])
        
        
def get_providers(Location):
    if request.method == get:
        Location = request.form.get("Location")
        Provider = request.form.get("Provider")
        print Location
        print 'access get_providers2222'
        data1= df[(df['LOC_NAME']==Location) & (df['Current PCP']==Provider)]
    
    return render_template('resultsa.html',  tables=[data1.to_html(classes='data', header="true")])
 
 # Credentials
@app.route('/credentials', methods=['GET', 'POST'])
def credentials():
    global data1
    query = """SELECT distinct PROV_NAME
                    FROM [Credentialing].[dbo].[Credentialing_data]
                    """

    cursor = cnxn.cursor()
    resultValue = cursor.execute(query)
    Prov_details = cursor.fetchall()
    
    x=[i[0] for i in Prov_details]


    print(x)
    if request.method == "POST":
        Start_Date = request.form.get("start_Date")
        End_date = request.form.get("End_Date")
        provider=request.form.get("p_provider")
        print(Start_Date)
        print(provider)
        # data1= df_credentials[( (df_credentials['PROV_NAME']==provider)  & (df_credentials['ORIG_SERVICE_DATE'] >= Start_Date) & (df_credentials['ORIG_SERVICE_DATE'] <= End_date )]
        
        query = """ select [PROC_CODE] as [Procedure Code], [PROC_NAME] as [Procedure Name], count(*) as Total
                    from [Credentialing].[dbo].[Credentialing_data]
                    WHERE [ORIG_SERVICE_DATE] BETWEEN '{Start_Date}' AND '{End_date}'
                    and [PROV_NAME] = '{provider}' 
                    GROUP BY PROC_CODE,PROC_NAME """

        cursor = cnxn.cursor()
        resultValue = cursor.execute(query.format(Start_Date = Start_Date, End_date = End_date, provider = provider))
        Prov_details = cursor.fetchall()
        x_list=list(Prov_details)

        x_tuple=[tuple(zz) for zz in x_list]
        data1 = pd.DataFrame(x_tuple,columns=['Procedure Code','Procedure Name','Total'])
        return render_template('resultsa.html',  tables=[data1.to_html(classes='data', header="true", index = False)])
    return render_template('credentials.html', dropdown_list=x)
    
# Demographics   
@app.route('/Demographics', methods=['GET', 'POST'])

def Demographics():
    print("a-aa")

    if request.method == "POST":
        global pat_details
        global Group1
        global Group2
        global df
        
        print('kk')
        Group1= request.form.get("Group1")
        print(Group1)
        Group2= request.form.get("filtered_groups")
        print(Group2)
        Group3= request.form.get("Group3")
        print(Group3)
        if Group3 == None:
            query1= """ select AssignedTeam, AssignedClinic,Language,ethnicity, MRN, Age from trial$ """
            cursor = cnxn.cursor()
            resultValue = cursor.execute(query1)
            pat_details = cursor.fetchall()
            x=list(pat_details)
        
            x_tuple=[tuple(zz) for zz in x]
            df = pd.DataFrame(x_tuple,columns=['AssignedTeam', 'AssignedClinic','Language','ethnicity', 'MRN', 'Age'])
            columns=list(df.columns)
            df_pivot = df.pivot_table(index=Group1, columns=Group2, values = "MRN", aggfunc = "count")
            df_pivottable =pd.DataFrame(df_pivot.to_records())


        if len(df_pivottable) > 0:
            return render_template('results.html', tables=[df_pivot.to_html(classes='data', header="true", table_id ='test')])
        else:
            return "No results Found"
  
    return render_template('Demographics.html')

@app.route('/something', methods=['POST'])
def something_post():

    print('something')
    global df_details
    if request.method == "POST":
        a= request.json['a']
        b=request.json['b']
        
        df_details=df[(df[Group1]==b) & (df[Group2] == a)] 
        
        print(list(df_details.columns))
        print(df_details)

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

@app.route('/something', methods=['GET'])
def something_get():

    print(df_details.columns)
    return render_template('resultsa.html',  tables=[df_details.to_html(classes='data', header="true")])
        
    
    

	

if __name__ == "__main__":
	app.run(host='0.0.0.0',debug=True)
	
