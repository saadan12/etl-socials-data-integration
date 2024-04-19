from .general import start_date_simple
from ...models import Company_wise_scores, Company, Project, UserProject, PitchInputs
from django.db.models import Q
import re
import datetime
from dateutil.relativedelta import relativedelta
import calendar


def get_company_id(pk):
    company_id = Project.objects.filter(id=pk).values()[0]["company_id"]
    return company_id


def get_companies_id(pk):
    project = Project.objects.filter(id=pk).values().first()
    company_array = []
    for key, value in project.items():
        if 'competitor' in key or 'company' in key:
            if value:
                company_array.append(value)
    return company_array


def get_company_id_by_url(company):
    company = Company.objects.filter(
        url=company).values_list('id', flat=True).first()
    return company


def get_company_url_by_id(id):
    company = Company.objects.filter(id=id).values()[0]["url"]
    return company


def get_primary_table_by_companyid(table, company_id):
    primary_info = table.objects.filter(
        company=company_id).values().order_by('initial_date')
    return primary_info


def get_secondary_by_primaryid(table, secondary_id):
    secondary_info = table.objects.filter(website_id=secondary_id).values()
    return secondary_info


def get_primary_by_companyid(table, secondary_id):
    secondary_info = table.objects.filter(
        company_id=secondary_id).order_by('-initial_date').values()
    return secondary_info


def get_primary_by_companyid_date(table, secondary_id, date):
    secondary_info=table.objects.filter(
        Q(company_id=secondary_id) & Q(initial_date__range=(date.replace(day=1), date))).order_by('-initial_date').values()
    return secondary_info


def get_unique_id_by_companyid(table, company_id):
    unique_id = table.objects.filter(
        company_id=company_id).values_list('website_id').last()
    return unique_id


def get_unique_id_by_companyidSM(table, company_id):
    unique_id = table.objects.filter(
        company_id=company_id).values_list('social_id').last()
    return unique_id


def get_unique_id_by_companyidSM2(table, company_id):
    unique_id = table.objects.filter(
        company_id=company_id).values_list('social_id').last()
    return unique_id


def get_secondary_sm_by_primaryid(table, secondary_id):
    secondary_info = table.objects.filter(
        social_media=secondary_id).values().last()
    return secondary_info


def get_secondaries_sm_by_primaryid(table, secondary_id):
    secondary_info = table.objects.filter(
        social_media=secondary_id).values()
    return secondary_info


# NEW FUNCTIONS 22-11-2022


def get_data_by_range(project_id, company_id, date):
    data = Company_wise_scores.objects.filter(
        Q(company_id=company_id) & Q(project=project_id)).values().filter(
            initial_date__range=(date.replace(day=1), date)).last()
    return data


def get_data_group_by_range(project_id, date):
    data = Company_wise_scores.objects.filter(
        Q(project=project_id)).values().order_by(
        '-initial_date').filter(
            initial_date__range=(date.replace(day=1), date)
        )
    return data


def get_data_last_by_company_id_table(table, company_id, date):
    primary_info = table.objects.filter(company=company_id).order_by(
        'initial_date').values().filter(
        initial_date__range=(date.replace(day=1), date)).last()
    return primary_info


def get_scores_by_company_project_filterDate(
    company_id, pk, end_date, start_date
):
    scores = Company_wise_scores.objects.filter(
        Q(company_id=company_id) & Q(project=pk)).values().filter(
            initial_date__range=(start_date, end_date)).order_by(
            'initial_date')
    return scores


def project_created_date(pk):
    return Project.objects.filter(
        id=pk
    ).values('created_date').first()["created_date"].date()


def get_start_date_from_project_date(pk, date):
    if not date:
        return project_created_date(pk)
    else:
        return start_date_simple(date)


def get_socialUrl_by_company_id(id, socialURL):
    return Company.objects.filter(id=id).values().first()[socialURL]


def get_unique_id_by_companyidSM_date(table, company_id, date):
    unique_id = table.objects.filter(
            Q(company_id=company_id) &
            Q(initial_date__range=(date.replace(day=1), date))
        ).values_list('social_id').last()
    return unique_id

# NEW FUNCTIONS 29-05-2023

def get_domain_from_url(url):
    """
    This function accepts a company url and extracts its domain with the help of a regular expression
    Regex works with the following formats:
    - https://example.com
    - https://example.es
    - https://example.org
    - https://example.gov
    - https://example.co.uk
    """
    match = re.search(r"https?://(?:www\.)?([\w-]+)(?:\.\w+)+", url)
    if match:
        domain = match.group(1)
        return domain
    return None

# NEW FUNCTIONS 30-05-2023

###################################################
# Functions to fetch data from UserProjects model #
###################################################

def get_project_id_from_user_project_pk(pk):
    """
    Parameter: pk - primary key
    Filters UserProject model to return project_id of entry with given primary key
    """
    project_id = UserProject.objects.filter(id=pk).values()[0]["project_id"]
    return project_id

def get_user_id_from_user_project_pk(pk):
    """
    Parameter: pk - primary key
    Filters UserProject model to return user_id of entry with given primary key
    """
    user_id = UserProject.objects.filter(id=pk).values()[0]["user_id"]
    return user_id

def get_user_id_from_user_project_project_id(project_id):
    """
    Parameter: project_id
    Filters UserProject model to return user_id of entry with given project_id
    """
    user_id = UserProject.objects.filter(project_id=project_id).values()[0]["user_id"]
    return user_id

##################################################
# Functions to fetch data from PitchInputs model #
##################################################

def get_pitch_client_brief_by_pk(pk):
    """
    Parameter: pk - primary key
    Filters PitchInputs model to return client brief of entry with given primary key
    """
    client_brief = PitchInputs.objects.filter(id=pk).values()[0]["brief"]
    return client_brief

def get_pitch_client_brief_by_user_id(user_id):
    """
    Parameter: user_id
    Filters PitchInputs model to return client brief of entry with given user_id
    """
    client_brief = PitchInputs.objects.filter(user_id=user_id).values()[0]["brief"]
    return client_brief

def get_pitch_agency_name_by_pk(pk):
    """
    Parameter: pk - primary key
    Filters PitchInputs model to return agency name of entry with given primary key
    """
    agency_name = PitchInputs.objects.filter(id=pk).values()[0]["agency_name"]
    return agency_name

def get_pitch_agency_name_by_user_id(user_id):
    """
    Parameter: pk - user_id
    Filters PitchInputs model to return agency name of entry with given user_id
    """
    agency_name = PitchInputs.objects.filter(user_id=user_id).values()[0]["agency_name"]
    return agency_name

def get_date_string(date):
    return date.strftime("%Y-%m-%d")

def get_previous_month(date):
    return date - relativedelta(months=1)

def set_to_last_day_of_month(date):
    return date.replace(day=calendar.monthrange(date.year, date.month)[1])
