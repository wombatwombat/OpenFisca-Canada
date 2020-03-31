# -*- coding: utf-8 -*-

# This file defines variables for the modelled legislation.
# A variable is a property of an Entity such as a Person, a Household…
# See https://openfisca.org/doc/key-concepts/variables.html

# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_canada.entities import *

class is_a_resident_of_canada(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Asks whether the applicant is a resident of Canada.'


class is_receiving_income_benefits_or_allowances(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Asks whether the applicant is currently receiving income, benefits, or allowances'

class quit_their_job_voluntarily(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Asks whether the applicant quit their job voluntarily'

class has_lost_income_for_half_of_the_application_period(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Asks whether the applicant has lost their income for at least' \
            'half of the four week period for which they are applying'

class they_are_over_15_years_of_age(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = 'Asks whether the applicant is over the age of 15 at time of applying'

    def formula(people, period, parameters):
        return people('age', period) >= 15

class earnings_amount(Variable):
    value_type = float
    entity = Person
    definition_period = ETERNITY
    label = 'The amount of money earned in the last year'

class earned_more_than_minimum_amount(Variable): 
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Asks whether the applicant has earned a minimum of $5,000  '

    def formula(people, period, parameters):
        ea = people('earnings_amount', period)
        return ea >= parameters(period).earnings.CERB_minimum


class person_is_eligible_for_CERB(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = 'collates eligibility criteria into whether a person is eligible' \
            ' to receive the Canadian Emergency Relief Benefit'
    end = '2020-10-31'

    def formula_2020_03_15(people, period):
        canadian_resident = people('is_a_resident_of_canada', period)
        believe_eligible = people('is_receiving_income_benefits_or_allowances', period)
        quit_their_job = people('quit_their_job_voluntarily', period)
        has_lost_income = people('has_lost_income_for_half_of_the_application_period', period)
        over_15 = people('they_are_over_15_years_of_age', period)
        earned_min_amount = people('earned_more_than_minimum_amount', period)
        return canadian_resident *  not_(believe_eligible) * not_(quit_their_job) * has_lost_income * over_15 * earned_min_amount
