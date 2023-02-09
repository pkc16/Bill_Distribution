from flask.views import MethodView
from wtforms import Form, StringField, SubmitField
from flask import Flask, render_template, request
from flatmates_bill import flat
from datetime import datetime

app = Flask(__name__)

class HomePage(MethodView):
    def get(self):
        return render_template('index.html')


class BillFormPage(MethodView):
    def get(self):
        bill_form = BillForm()
        return render_template('bill_form_page.html', billform=bill_form)

    def post(self):
        # extract data which user enters
        billform = BillForm(request.form)

        if not billform.amount.data or not billform.days_in_house1.data or not billform.days_in_house2.data:
            return render_template('bill_form_page.html',
                                   result=False,
                                   billform=billform,
                                   name1="",
                                   amount1="",
                                   name2="",
                                   amount2="")

        else:
            the_bill = flat.Bill(float(billform.amount.data), billform.period.data)
            roommate1 = flat.Flatmate(billform.name1.data, float(billform.days_in_house1.data))
            roommate2 = flat.Flatmate(billform.name2.data, float(billform.days_in_house2.data))

            return render_template('bill_form_page.html',
                                   result=True,
                                   billform=billform,
                                   name1=roommate1.name,
                                   amount1=roommate1.pays(the_bill, roommate2),
                                   name2=roommate2.name,
                                   amount2=roommate2.pays(the_bill, roommate1))


class ResultsPage(MethodView):
    def post(self):
        # extract data which user enters
        billform = BillForm(request.form)

        the_bill = flat.Bill(float(billform.amount.data), billform.period.data)
        roommate1 = flat.Flatmate(billform.name1.data, float(billform.days_in_house1.data))
        roommate2 = flat.Flatmate(billform.name2.data, float(billform.days_in_house2.data))

        return render_template('results.html',
                               period=the_bill.period,
                               name1=roommate1.name,
                               amount1=roommate1.pays(the_bill, roommate2),
                               name2=roommate2.name,
                               amount2=roommate2.pays(the_bill, roommate1))


class BillForm(Form):
    # create the variables to hold field data for the form
    amount = StringField("Bill Amount: ")
    period = StringField("Bill Period: ", default=datetime.now().strftime('%B') + " " + str(datetime.now().year))

    name1 = StringField("Name: ")
    days_in_house1 = StringField("Days in the house: ")

    name2 = StringField("Name: ")
    days_in_house2 = StringField("Days in the house: ")

    button = SubmitField("Calculate Charges")
    # clicking button will display the results page


# set up url rule pages
app.add_url_rule('/', view_func=HomePage.as_view('home_page'))
app.add_url_rule('/bill_form_page', view_func=BillFormPage.as_view('bill_form_page'))
# app.add_url_rule('/results', view_func=ResultsPage.as_view('results_page'))

app.run(debug=True)