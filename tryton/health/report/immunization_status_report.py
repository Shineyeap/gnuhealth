# -*- coding: utf-8 -*-
##############################################################################
#
#    GNU Health: The Free Health and Hospital Information System
#    Copyright (C) 2008-2014 Luis Falcon <falcon@gnu.org>
#    Copyright (C) 2011-2014 GNU Solidario <health@gnusolidario.org>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from datetime import date
from trytond.report import Report
from trytond.pool import Pool
from trytond.transaction import Transaction
from dateutil.relativedelta import relativedelta

__all__ = ['ImmunizationStatusReport']

class ImmunizationStatusReport(Report):
    __name__ = 'gnuhealth.immunization_status_report'


    @classmethod
    def parse(cls, report, objects, data, localcontext):

        Sched = Pool().get('gnuhealth.immunization_schedule')
        Patient = Pool().get('gnuhealth.patient')
        patient = Patient(data['patient_id'])
        localcontext['patient'] = patient
        sched = Sched(data['immunization_schedule_id'])
        
        localcontext['immunization_schedule']=sched

        immunization_to_check = \
            cls.get_immunizations_for_age(patient, sched)
        
        print immunization_to_check
        
        return super(ImmunizationStatusReport, cls).parse(report,
            objects, data, localcontext)

    @classmethod
    def get_immunizations_for_age(cls,Patient,immunization_schedule):
        
        immunizations_for_age = []
        
        for vaccine in immunization_schedule.vaccines:
            
            for dose in vaccine.doses:
                dose_number, dose_age, age_unit = dose.dose_number, \
                    dose.age_dose, dose.age_unit
                
                p_age = Patient.patient_age(name='raw_age')
                
                #Age of the person in years and months
                pyears,pmonths = p_age[0],p_age[1]
                
                pmonths = (pyears*12)+pmonths
                
                if ((age_unit == 'months' and pmonths >= dose_age) or
                    (age_unit == 'years' and pyears >= dose_age)):
                        immunization_info = {
                            'vaccine' : vaccine,
                            'dose' : dose_number,
                            'dose_age' : dose_age,
                            'age_unit' : age_unit}
                        
                        # Add to the list of this person immunization check
                        immunizations_for_age.append(immunization_info)
                            
        return immunizations_for_age
            
