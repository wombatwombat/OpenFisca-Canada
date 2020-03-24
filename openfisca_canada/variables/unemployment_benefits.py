# -*- coding: utf-8 -*-

# This file defines variables for the modelled legislation.
# A variable is a property of an Entity such as a Person, a Household…
# See https://openfisca.org/doc/key-concepts/variables.html

# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_canada.entities import *

import datetime
today_date_and_time = np.datetime64(datetime.datetime.now())
today = today_date_and_time.astype('datetime64[D]')


class have_paid_into_employment_insurance(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Asks whether the person has paid into employment benefits.'


class last_employment_insurance_payment_date(Variable):
    value_type = date
    entity = Person
    definition_period = ETERNITY
    label = 'Defines the last date at which the person has paid into' \
            ' Employment Insurance.'


class hours_worked_in_last_52_weeks(Variable):
    value_type = float
    entity = Person
    definition = YEAR
    label = 'Asks how many hours the claimaint has worked in the last 52 weeks.'


class has_record_of_employment(Variable):
    value_type = bool
    entity = Person
    definition = ETERNITY
    label = 'Asks whether the person has a previous record of employment.'


class current_earnings(Variable):
    value_type = float
    entity = Person
    definition = YEAR
    label = 'Asks for the existing weekly earnings of the applicant.'

class regular_earnings(Variable):
    value_type = float
    entity = Person
    definition = YEAR
    label = 'Asks for the regular weekly earnings of the applicant.'

class potential_weekly_benefits(Variable):
    value_type = float
    entity = Person
    definition = ETERNITY
    label 'Defines the maximum weekly benefit for the applicant.'

    def formula(person, period, parameters):
        current_earnings = person(current_earnings, period)
        benefit_earnings = current_earnings * 0.55
        condition_maximum_benefit = (current_earnings > 573)
        return where(condition_maximum_benefit, 573, benefit_earnings)


class has_medical_certificate(Variable):
    value_type = bool
    entity = Person
    definition = ETERNITY
    label = 'asks whether the applicant has a current medical certificate.' \
            ' note: not required for current COVID-19 benefits.'


class unable_to_work_for_medical_reasons(Variable):
    value_type = bool
    entity = Person
    definition = ETERNITY
    label = 'Asks whether the applicant is unable to work for medical reasons.'


class regular_earnings_minimum_decrease(Variable):
    value_type = bool
    entity = Person
    definition = ETERNITY
    label = 'Determines whether the applicants regular earnings have decreased' \
            ' by the minimum 40% required to claim benefits.'

    def formula(people, period, parameters):
        current_earnings = people('current_earnings', period)
