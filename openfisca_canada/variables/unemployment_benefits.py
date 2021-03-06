# -*- coding: utf-8 -*-

# This file defines variables for the modelled legislation.
# A variable is a property of an Entity such as a Person, a Household…
# See https://openfisca.org/doc/key-concepts/variables.html

# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_canada.entities import *

import datetime
import numpy as np
today_date_and_time = np.datetime64(datetime.datetime.now())
today = today_date_and_time.astype('datetime64[D]')


class has_paid_into_employment_insurance(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Asks whether the person has paid into employment benefits.'


class hours_worked_in_last_52_weeks(Variable):
    value_type = float
    entity = Person
    definition_period = ETERNITY
    label = 'Asks how many hours the claimaint has worked in the last 52 weeks.'


class person_has_worked_minimum_hours(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'determines whether the person has worked the minimum required' \
            ' hours in the past 52 weeks.'

    def formula(people, period, parameters):
        hours_worked = people('hours_worked_in_last_52_weeks', period)
        condition_minimum_hours_worked = hours_worked >= 600
        return where(condition_minimum_hours_worked, True, False)


class has_record_of_employment(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Asks whether the person has a previous record of employment.'


class has_medical_certificate(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'asks whether the applicant has a current medical certificate.' \
            ' note: not required for current COVID-19 benefits and is not.' \
            ' currently included in eligibility criteria.'


class person_is_unable_to_work_for_medical_reasons(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Asks whether the applicant is unable to work for medical reasons.'


class regular_earnings_decreased_by_40_percent_or_more(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Determines whether the applicants regular earnings have decreased' \
            ' by the minimum 40% required to claim benefits.'


class person_is_eligible_for_EI_benefits(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'collates eligibility criteria into whether a person is eligible' \
            ' to receive EI benefits within COVID 19 or not.'

    def formula(people, period, parameters):
        paid_into_EI = people('has_paid_into_employment_insurance', period)
        is_unable_to_work = people('person_is_unable_to_work_for_medical_reasons', period)
        has_record_of_employment = people('has_record_of_employment', period)
        worked_minimum_hours = people('person_has_worked_minimum_hours', period)
        minimum_income_decrease = people('regular_earnings_decreased_by_40_percent_or_more', period)
        return paid_into_EI * is_unable_to_work * has_record_of_employment * worked_minimum_hours * minimum_income_decrease
