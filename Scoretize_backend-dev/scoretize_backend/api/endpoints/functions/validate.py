from django.db.models import Q
from ...models import Users, UserProject, Project, Sector, Company


def is_user_project(id, pk):

    user_id = Users.objects.filter(id=id).values_list()[0][0]
    check_project = UserProject.objects.filter(
        Q(user=user_id) & Q(project=pk)).values_list()
    return check_project


def check_competitors(pk):
    count_competitors = Project.objects.filter(id=pk).values_list().first()
    count = 0

    for value in count_competitors:
        if value is None:
            count += 1
    return count


def isCompanyProjectID(company_temp_id, company_project_id):
    return company_temp_id == company_project_id


def get_sector_by_name(category, subcategory):
    sector = Sector.objects.filter(
        Q(category=category) &
        Q(subcategory=subcategory)
    )
    return sector


def get_subcategory_by_name(request_name):
    sector = Sector.objects.filter(category=request_name)
    return sector


def get_company_by_url(company):
    company = Company.objects.filter(url=company)
    return company


def check_competitors_length(competitors):
    if len(competitors) > 10:
        return False
    if len(competitors) < 2:
        return False
    else:
        return True


def check_dupes(company_array):
    repeated = set()
    dupes = [
        x for x in company_array
        if x in repeated or (repeated.add(x) or False)
    ]
    if len(dupes) > 0:
        return False
    else:
        return True
