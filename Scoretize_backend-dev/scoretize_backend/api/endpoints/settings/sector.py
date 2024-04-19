from ...views import viewsets, APIView, IsAuthenticated, \
    action, os, SectorSerializer, \
    csv, IntegrityError, HttpResponse, \
    http_ok, Sector, Q


class SectorRegister(viewsets.ViewSet, APIView):
    permission_classes = (IsAuthenticated,)

    @action(methods=["POST"], detail=False, url_path="postSectors")
    def postSector(self, request):
        """
        Post sectors from CSV.
        Auto-detects already stored sectors and adds the new ones.
        """
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, './CPG_categories.csv')

        with open(filename, 'r') as csv_categories:
            csv_reader = csv.reader(csv_categories, delimiter=';')
            for row in csv_reader:
                sector_dict = {}

                sector_dict["category"] = row[7].lower().strip()
                sector_dict["subcategory"] = row[8].lower().strip()

                existent_sectors = Sector.objects.filter(
                    Q(category=sector_dict["category"])
                    & Q(subcategory=sector_dict["subcategory"])).values_list(
                ).first()

                if existent_sectors is None:
                    sector = SectorSerializer(data=sector_dict)
                    if sector.is_valid(raise_exception=False):
                        try:
                            sector.save()
                        except IntegrityError as e:
                            return HttpResponse(e)
            return http_ok('Sectors registered successfully')

    # GET: fecth authenticated user
    @action(methods=["GET"], detail=False, url_path="sectors")
    def getSector(self, request):
        """
        Get All Sectors.
        """
        sectorDict = Sector.objects.all().values()

        newSectorDict = {}

        for sector in sectorDict:
            if sector["category"] == "category":
                pass
            else:
                if sector["category"] in newSectorDict:
                    newSectorDict[sector["category"]].append(
                        sector["subcategory"]
                    )
                    pass
                else:
                    newSectorDict[sector["category"]] = []
                    newSectorDict[sector["category"]].append(
                        sector["subcategory"]
                    )

        return http_ok(newSectorDict)
