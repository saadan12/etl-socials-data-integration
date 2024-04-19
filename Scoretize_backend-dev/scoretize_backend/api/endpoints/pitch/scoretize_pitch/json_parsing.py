import json
import os
import re


def load_json(path):
    f = open(path)
    data = json.load(f)

    return data


class JsonParser:
    def __init__(self, path, domain):
        self.path = path
        self.debrief = self.load_debrief()
        self.deployment = self.load_deploy()
        self.styles_dict = load_json("api/endpoints/pitch/scoretize_pitch/style.json")
        self.slides_collection = []
        self.domain = domain

    def run(self):
        self.template1()
        self.template2()
        self.template3()
        self.template4()
        self.template5()
        self.template6()
        self.template7()
        self.template8()
        self.template9()
        self.template10()
        self.template11()
        self.template12()
        self.template13()
        self.template14()
        self.template15()
        self.template16()
        self.template17()
        self.template18()
        self.template19()
        self.template20()
        self.template21()
        self.template22()
        self.template23()
        self.template24()
        self.template25()
        self.template26()
        self.template27()
        self.template28()
        self.template29_30_31()
        self.template32_33_34()
        self.template35_36_37()
        self.template38_39_40()
        self.template41()
        self.template42()
        self.template43()
        self.template44()
        self.template45()
        self.template46()
        self.template47()
        self.template48()
        final_dict = self.template49()

        with open("api/endpoints/pitch/scoretize_pitch/data.json", "w") as outfile:
            json.dump(final_dict, outfile)

    def load_debrief(self):
        dict_ = load_json(os.path.join(self.path, "debrief.json"))
        title1, title2, title3, title4 = dict_["Debrief"].keys()
        text1 = dict_["Debrief"][title1]
        text2 = dict_["Debrief"][title2]
        text3 = dict_["Debrief"][title3]
        text4 = dict_["Debrief"][title4]

        return {
            "title1": title1,
            "title2": title2,
            "title3": title3,
            "title4": title4,
            "text1": text1,
            "text2": text2,
            "text3": text3,
            "text4": text4,
        }

    def load_objective(self):
        dict_ = load_json(os.path.join(self.path, "debrief.json"))
        objective1, objective2, objective3, objective4 = dict_["Objective"].keys()
        objective1_value = dict_["Objective"][objective1]
        objective2_value = dict_["Objective"][objective2]
        objective3_value = dict_["Objective"][objective3]
        objective4_value = dict_["Objective"][objective4]

        return {
            "objective1": objective1,
            "objective2": objective2,
            "objective3": objective3,
            "objective4": objective4,
            "objective1_value": objective1_value,
            "objective2_value": objective2_value,
            "objective3_value": objective3_value,
            "objective4_value": objective4_value,
        }

    def load_market(self):
        dict_ = load_json(os.path.join(self.path, "key_competitors.json"))
        website = ["Website"]
        features = ["Features"]
        traffic = ["Traffic"]
        messaging = ["Messaging"]
        engagement = ["Engagement Rate"]
        socials = ["Social Media"]

        for i in range(0, 2):
            website.append(str(dict_["data"]["comparison_table"][i]["Website"]))
            features.append(str(dict_["data"]["comparison_table"][i]["Features"]))
            traffic.append(str(dict_["data"]["comparison_table"][i]["Traffic"]))
            messaging.append(str(dict_["data"]["comparison_table"][i]["Messaging"]))
            engagement.append(
                str(dict_["data"]["comparison_table"][i]["Engagement Rate"])
            )
            socials_content = ", ".join(
                "{!s}={!r}".format(key, val)
                for (key, val) in dict_["data"]["comparison_table"][i][
                    "Social Media"
                ].items()
            )
            socials.append(socials_content)

        rows = []
        for i in range(len(website)):
            rows.append(
                [
                    website[i],
                    features[i],
                    traffic[i],
                    messaging[i],
                    engagement[i],
                    socials[i],
                ]
            )

        return rows

    def load_buyer_persona(self):
        dict_ = load_json(os.path.join(self.path, "buyer_persona.json"))

        title = [x["Title"] for x in dict_["Buyer_Personas"]]
        age_range = [str(x["Age_Range"]) for x in dict_["Buyer_Personas"]]
        hot_zone_locations = [x["Hot_Zone_Locations"] for x in dict_["Buyer_Personas"]]
        avg_income = [str(x["Average_Income"]) for x in dict_["Buyer_Personas"]]
        interests = [x["Interests"] for x in dict_["Buyer_Personas"]]
        most_common = [x["Most_Common_Products"] for x in dict_["Buyer_Personas"]]
        purchase_loc = [x["Purchase_Location"] for x in dict_["Buyer_Personas"]]
        top_purchase = [x["Top_Purchase_Triggers"] for x in dict_["Buyer_Personas"]]
        moment_of_consumption = [
            x["Moment_Of_Consumption"] for x in dict_["Buyer_Personas"]
        ]

        rows = [
            ["Moments of consumption", moment_of_consumption[0]],
            ["Purchase Location", purchase_loc[0]],
            ["Top purchase triggers", top_purchase[0]],
            ["Most common products/services of interest", most_common[0]],
        ]

        micromoments = list(dict_["Micro_Moments"][0].values())
        occasions = [x for x in dict_["Occasions"]]

        return {
            "title": title,
            "age_range": age_range,
            "hot_zone_locations": hot_zone_locations,
            "avg_income": avg_income,
            "interests": interests,
            "most_common": most_common,
            "purchase_loc": purchase_loc,
            "top_purchase": top_purchase,
            "moment_of_consumption": moment_of_consumption,
            "rows": rows,
            "micromoments": micromoments,
            "occasions": occasions,
        }

    def load_swot(self):
        dict_ = load_json(os.path.join(self.path, "swot_analysis.json"))

        dict_ = dict_["SWOT_Analysis"]
        strengths_questions = [x["question"] for x in dict_["Strengths"]]
        strengths_answer = [x["answer"] for x in dict_["Strengths"]]

        weaknesses_questions = [x["question"] for x in dict_["Weaknesses"]]
        weaknesses_answer = [x["answer"] for x in dict_["Weaknesses"]]

        opportunities_questions = [x["question"] for x in dict_["Opportunities"]]
        opportunities_answer = [x["answer"] for x in dict_["Opportunities"]]

        threats_questions = [x["question"] for x in dict_["Threats"]]
        threats_answer = [x["answer"] for x in dict_["Threats"]]

        return {
            "strength_q": strengths_questions,
            "strength_a": strengths_answer,
            "weaknesses_q": weaknesses_questions,
            "weaknesses_a": weaknesses_answer,
            "opportunities_q": opportunities_questions,
            "opportunities_a": opportunities_answer,
            "threats_q": threats_questions,
            "threats_a": threats_answer,
        }

    def load_map(self):
        dict_ = load_json(os.path.join(self.path, "map_possibilites.json"))
        dict_ = dict_["Ideation"]
        actions = [x["Action"] for x in dict_["Map of possibilities"]]
        input = [x["Input"] for x in dict_["Map of possibilities"]]
        hypotheses_keys = [
            list(x["Hypotheses"][0].keys()) for x in dict_["Map of possibilities"]
        ]
        hypotheses_values = [
            list(x["Hypotheses"][0].values()) for x in dict_["Map of possibilities"]
        ]

        hypothesis = []
        for keys, values in zip(hypotheses_keys, hypotheses_values):
            for key, value in zip(keys, values):
                hypothesis.append(key + ": " + value + "\n ")

        conclusions = [x[3::] for x in dict_["Conclusion"]["KeyHypothesis"]]

        return {
            "actions": actions,
            "input": input,
            "hypotheses": hypothesis,
            "conclusions": conclusions,
        }

    def load_actions(self):
        dict_ = load_json(os.path.join(self.path, "action_plans.json"))
        dict_ = dict_["Action plans"]

        intro_aware = [x for x in dict_["Introduction"]["Awareness"]]
        intro_consi = [x for x in dict_["Introduction"]["Consideration"]]
        intro_conv = [x for x in dict_["Introduction"]["Conversion"]]
        intro_loy = [x for x in dict_["Introduction"]["Loyalty"]]

        awareness_keys = [x for x in dict_["Awareness"]]
        awareness_values = [list(x) for x in dict_["Awareness"].values()]

        consideration_keys = [x for x in dict_["Consideration"]]
        consideration_values = [list(x) for x in dict_["Consideration"].values()]

        conversion_keys = [x for x in dict_["Conversion"]]
        conversion_values = [list(x) for x in dict_["Conversion"].values()]

        loyalty_keys = [x for x in dict_["Loyalty"]]
        loyalty_values = [list(x) for x in dict_["Loyalty"].values()]

        return {
            "intro_aware": intro_aware,
            "intro_consi": intro_consi,
            "intro_conv": intro_conv,
            "intro_loy": intro_loy,
            "awareness_keys": awareness_keys,
            "awareness_values": awareness_values,
            "consideration_keys": consideration_keys,
            "consideration_values": consideration_values,
            "conversion_keys": conversion_keys,
            "conversion_values": conversion_values,
            "loyalty_keys": loyalty_keys,
            "loyalty_values": loyalty_values,
        }

    def load_deploy(self):
        dict_ = load_json(os.path.join(self.path, "deployment_steps.json"))

        step1 = dict_["DEPLOYMENT STEPS"]

        step1 = [x[0] + re.sub("(?<!^)(?=[A-Z])", "", x[1::]).lower() for x in step1][
            1:-1
        ]

        step1 = [" \n ".join(step1)]

        step2_keys = [x for x in dict_["CORE TEAM"]]
        step2_values = [list(x) for x in dict_["CORE TEAM"].values()]

        step3_keys = [
            ["MEETINGS", "PLANNING", "CO-CREATION", "EXECUTION", "COORDINATION"]
        ]
        step3_values = [list(x.values()) for x in dict_["GOVERNANCE_MODEL"]["Meetings"]]

        step3_rows = step3_keys + step3_values

        step4 = dict_["PILOT_COUNTRIES"]
        step4 = " \n ".join(step4)

        step5 = dict_["KPIs"]
        step5 = " \n ".join(step5)

        step6 = [dict_["KEY_MILESTONES"]]

        step7_keys = [x for x in dict_["TEAM_BUDGET"]][:-1]

        step7_values = []
        for key in step7_keys:
            step7_values.append([x for x in dict_["TEAM_BUDGET"][key]])

        step7_v = [[" \n ".join(x)] for x in step7_values]

        step7_v = [item for sublist in step7_v for item in sublist]

        step7_rows = [step7_keys, step7_v]

        step8 = list(dict_["TEAM_BUDGET"].values())[-1]

        return {
            "step1": step1,
            "step2_keys": step2_keys,
            "step2_values": step2_values,
            "step3_rows": step3_rows,
            "step4": step4,
            "step5": step5,
            "step6": step6,
            "step7_rows": step7_rows,
            "step8": step8,
        }

    def get_style(self, slide_number, key):
        style = self.styles_dict[slide_number][0][key][0]
        color = style["color"]
        size = style["size"]
        bold = style["bold"]
        underline = style["underline"]
        italic = style["italic"]

        dict_ = {"styles": []}
        dict_["styles"] = {
            "font": {
                "size": size,
                "color": color,
                "underline": underline,
                "italic": italic,
                "bold": bold,
            }
        }

        return dict_

    def template1(self):
        final_dict = {}
        final_dict["template"] = 1
        value = self.domain.title()
        final_dict = self.template10_helper("1", final_dict, value, "main_title")

        self.slides_collection.append(final_dict)

        output_dict = {}
        output_dict["slides"] = self.slides_collection

        return output_dict

    def template2(self):
        template_dict = {"template": 2}
        self.slides_collection.append(template_dict)

        return template_dict

    def template3_helper(self, n, final_dict, out_dict, title_name, text_name=None):
        style_dict_title = self.get_style(n, title_name)
        title_dict = {"type": "text", "value": out_dict[title_name]}
        title_dict = {**title_dict, **style_dict_title}
        final_dict[title_name] = title_dict

        if text_name:
            style_dict_text = self.get_style(n, text_name)
            text_dict = {"type": "text", "value": out_dict[text_name]}
            text_dict = {**text_dict, **style_dict_text}
            final_dict[text_name] = text_dict

        return final_dict

    def template10_helper(self, n, final_dict, value, title_name, text_name=None):
        style_dict_title = self.get_style(n, title_name)
        title_dict = {"type": "text", "value": value}
        title_dict = {**title_dict, **style_dict_title}
        final_dict[title_name] = title_dict

        return final_dict

    def template3(self):
        final_dict = {}
        final_dict["template"] = 3

        debrief = self.load_debrief()

        final_dict = self.template3_helper("3", final_dict, debrief, "title1", "text1")
        final_dict = self.template3_helper("3", final_dict, debrief, "title2", "text2")
        final_dict = self.template3_helper("3", final_dict, debrief, "title3", "text3")
        final_dict = self.template3_helper("3", final_dict, debrief, "title4", "text4")

        self.slides_collection.append(final_dict)

        output_dict = {}
        output_dict["slides"] = self.slides_collection

        return output_dict

    def template4(self):
        final_dict = {}
        final_dict["template"] = 4

        objective = self.load_objective()

        final_dict = self.template3_helper("4", final_dict, objective, "objective1")
        final_dict = self.template3_helper("4", final_dict, objective, "objective2")
        final_dict = self.template3_helper("4", final_dict, objective, "objective3")
        final_dict = self.template3_helper("4", final_dict, objective, "objective4")

        self.slides_collection.append(final_dict)

        output_dict = {}
        output_dict["slides"] = self.slides_collection

        return output_dict

    def template5(self):
        final_dict = {}
        final_dict["template"] = 5

        objective = self.load_objective()

        final_dict = self.template3_helper(
            "5", final_dict, objective, "objective1", "objective1_value"
        )

        self.slides_collection.append(final_dict)

        output_dict = {}
        output_dict["slides"] = self.slides_collection

        return output_dict

    def template6(self):
        final_dict = {}
        final_dict["template"] = 6

        objective = self.load_objective()

        final_dict = self.template3_helper(
            "6", final_dict, objective, "objective2", "objective2_value"
        )

        self.slides_collection.append(final_dict)

        output_dict = {}
        output_dict["slides"] = self.slides_collection

        return output_dict

    def template7(self):
        final_dict = {}
        final_dict["template"] = 7

        objective = self.load_objective()

        final_dict = self.template3_helper(
            "7", final_dict, objective, "objective3", "objective3_value"
        )

        self.slides_collection.append(final_dict)

        output_dict = {}
        output_dict["slides"] = self.slides_collection

        return output_dict

    def template8(self):
        final_dict = {}
        final_dict["template"] = 8

        objective = self.load_objective()

        final_dict = self.template3_helper(
            "8", final_dict, objective, "objective4", "objective4_value"
        )

        self.slides_collection.append(final_dict)

        output_dict = {}
        output_dict["slides"] = self.slides_collection

        return output_dict

    def table_helper(self, final_dict, out_dict, table_name):
        dict_ = {"type": "table", "rows": out_dict}
        final_dict[table_name] = dict_

        return final_dict

    def template9(self):
        final_dict = {}
        final_dict["template"] = 9

        rows = self.load_market()

        final_dict = self.table_helper(final_dict, rows, "market_table")

        self.slides_collection.append(final_dict)

        output_dict = {}
        output_dict["slides"] = self.slides_collection

        return output_dict

    def template10(self):
        final_dict = {}
        final_dict["template"] = 10

        buyer_params = self.load_buyer_persona()

        for buyer_persona, title_name in zip(
            buyer_params["title"], ["buyer1", "buyer2", "buyer3", "buyer4", "buyer5"]
        ):
            final_dict = self.template10_helper(
                "10", final_dict, buyer_persona, title_name
            )

        self.slides_collection.append(final_dict)

        output_dict = {}
        output_dict["slides"] = self.slides_collection

        return output_dict

    def template11(self):
        final_dict = {}
        final_dict["template"] = 11

        buyer_params = self.load_buyer_persona()

        final_dict = self.template10_helper(
            "11", final_dict, buyer_params["title"][0], "buyer1"
        )
        final_dict = self.template10_helper(
            "11", final_dict, buyer_params["age_range"][0], "age"
        )
        final_dict = self.template10_helper(
            "11",
            final_dict,
            buyer_params["hot_zone_locations"][0],
            "hot_zone_locations",
        )
        final_dict = self.template10_helper(
            "11", final_dict, buyer_params["avg_income"][0], "avg_income"
        )
        final_dict = self.template10_helper(
            "11", final_dict, buyer_params["interests"][0], "interests"
        )

        final_dict = self.table_helper(final_dict, buyer_params["rows"], "buyer1_table")

        self.slides_collection.append(final_dict)

        output_dict = {}
        output_dict["slides"] = self.slides_collection

        return output_dict

    def template12(self):
        final_dict = {}
        final_dict["template"] = 12

        buyer_params = self.load_buyer_persona()

        final_dict = self.template10_helper(
            "12", final_dict, buyer_params["title"][1], "buyer2"
        )
        final_dict = self.template10_helper(
            "12", final_dict, buyer_params["age_range"][1], "age"
        )
        final_dict = self.template10_helper(
            "12",
            final_dict,
            buyer_params["hot_zone_locations"][1],
            "hot_zone_locations",
        )
        final_dict = self.template10_helper(
            "12", final_dict, buyer_params["avg_income"][1], "avg_income"
        )
        final_dict = self.template10_helper(
            "12", final_dict, buyer_params["interests"][1], "interests"
        )

        final_dict = self.table_helper(final_dict, buyer_params["rows"], "buyer2_table")

        self.slides_collection.append(final_dict)

        output_dict = {}
        output_dict["slides"] = self.slides_collection

        return output_dict

    def template13(self):
        final_dict = {}
        final_dict["template"] = 13

        buyer_params = self.load_buyer_persona()

        final_dict = self.template10_helper(
            "13", final_dict, buyer_params["title"][2], "buyer3"
        )
        final_dict = self.template10_helper(
            "13", final_dict, buyer_params["age_range"][2], "age"
        )
        final_dict = self.template10_helper(
            "13",
            final_dict,
            buyer_params["hot_zone_locations"][2],
            "hot_zone_locations",
        )
        final_dict = self.template10_helper(
            "13", final_dict, buyer_params["avg_income"][2], "avg_income"
        )
        final_dict = self.template10_helper(
            "13", final_dict, buyer_params["interests"][2], "interests"
        )

        final_dict = self.table_helper(final_dict, buyer_params["rows"], "buyer3_table")

        self.slides_collection.append(final_dict)

        output_dict = {}
        output_dict["slides"] = self.slides_collection

        return output_dict

    def template14(self):
        final_dict = {}
        final_dict["template"] = 14

        buyer_params = self.load_buyer_persona()

        final_dict = self.template10_helper(
            "14", final_dict, buyer_params["title"][3], "buyer4"
        )
        final_dict = self.template10_helper(
            "14", final_dict, buyer_params["age_range"][3], "age"
        )
        final_dict = self.template10_helper(
            "14",
            final_dict,
            buyer_params["hot_zone_locations"][3],
            "hot_zone_locations",
        )
        final_dict = self.template10_helper(
            "14", final_dict, buyer_params["avg_income"][3], "avg_income"
        )
        final_dict = self.template10_helper(
            "14", final_dict, buyer_params["interests"][3], "interests"
        )

        final_dict = self.table_helper(final_dict, buyer_params["rows"], "buyer4_table")

        self.slides_collection.append(final_dict)

        output_dict = {}
        output_dict["slides"] = self.slides_collection

        return output_dict

    def template15(self):
        final_dict = {}
        final_dict["template"] = 15

        buyer_params = self.load_buyer_persona()

        final_dict = self.template10_helper(
            "15", final_dict, buyer_params["title"][4], "buyer5"
        )
        final_dict = self.template10_helper(
            "15", final_dict, buyer_params["age_range"][4], "age"
        )
        final_dict = self.template10_helper(
            "15",
            final_dict,
            buyer_params["hot_zone_locations"][4],
            "hot_zone_locations",
        )
        final_dict = self.template10_helper(
            "15", final_dict, buyer_params["avg_income"][4], "avg_income"
        )
        final_dict = self.template10_helper(
            "15", final_dict, buyer_params["interests"][4], "interests"
        )

        final_dict = self.table_helper(final_dict, buyer_params["rows"], "buyer5_table")

        self.slides_collection.append(final_dict)

        output_dict = {}
        output_dict["slides"] = self.slides_collection

        return output_dict

    def template16(self):
        final_dict = {}
        final_dict["template"] = 16

        buyer_params = self.load_buyer_persona()

        micromoments = [" \n \n ".join(buyer_params["micromoments"])]

        final_dict = self.template10_helper(
            "16", final_dict, micromoments[0], "micromoments"
        )

        self.slides_collection.append(final_dict)

        output_dict = {}
        output_dict["slides"] = self.slides_collection

        return output_dict

    def template17(self):
        final_dict = {}
        final_dict["template"] = 17

        buyer_params = self.load_buyer_persona()

        occasions = [" \n \n ".join(buyer_params["occasions"])]

        final_dict = self.template10_helper(
            "17", final_dict, occasions[0], "keyoccasions"
        )

        self.slides_collection.append(final_dict)

        output_dict = {}
        output_dict["slides"] = self.slides_collection

        return output_dict

    def template18(self):
        final_dict = {}
        final_dict["template"] = 18

        swot_dict = self.load_swot()

        for i in range(0, 3):
            final_dict = self.template10_helper(
                "18", final_dict, swot_dict["strength_q"][i], "question" + str(i + 1)
            )
            final_dict = self.template10_helper(
                "18", final_dict, swot_dict["strength_a"][i], "answer" + str(i + 1)
            )

        self.slides_collection.append(final_dict)

        output_dict = {}
        output_dict["slides"] = self.slides_collection

        return output_dict

    def template19(self):
        final_dict = {}
        final_dict["template"] = 19

        swot_dict = self.load_swot()

        for i in range(0, 3):
            final_dict = self.template10_helper(
                "19", final_dict, swot_dict["strength_q"][i], "question" + str(i + 1)
            )
            final_dict = self.template10_helper(
                "19", final_dict, swot_dict["strength_a"][i], "answer" + str(i + 1)
            )

        self.slides_collection.append(final_dict)

        output_dict = {}
        output_dict["slides"] = self.slides_collection

        return output_dict

    def template20(self):
        final_dict = {}
        final_dict["template"] = 20

        swot_dict = self.load_swot()

        for i in range(0, 3):
            final_dict = self.template10_helper(
                "20", final_dict, swot_dict["strength_q"][i], "question" + str(i + 1)
            )
            final_dict = self.template10_helper(
                "20", final_dict, swot_dict["strength_a"][i], "answer" + str(i + 1)
            )

        self.slides_collection.append(final_dict)

        output_dict = {}
        output_dict["slides"] = self.slides_collection

        return output_dict

    def template21(self):
        final_dict = {}
        final_dict["template"] = 21

        swot_dict = self.load_swot()

        for i in range(0, 3):
            final_dict = self.template10_helper(
                "21", final_dict, swot_dict["strength_q"][i], "question" + str(i + 1)
            )
            final_dict = self.template10_helper(
                "21", final_dict, swot_dict["strength_a"][i], "answer" + str(i + 1)
            )

        self.slides_collection.append(final_dict)

        output_dict = {}
        output_dict["slides"] = self.slides_collection

        return output_dict

    def template22(self):
        final_dict = {}
        final_dict["template"] = 22

        map_dict = self.load_map()

        final_dict = self.template10_helper(
            "22", final_dict, map_dict["actions"][0], "title"
        )
        final_dict = self.template10_helper(
            "22", final_dict, map_dict["input"][0], "input"
        )
        final_dict = self.template10_helper(
            "22", final_dict, map_dict["hypotheses"][0], "hypothesis"
        )

        self.slides_collection.append(final_dict)

        output_dict = {}
        output_dict["slides"] = self.slides_collection

        return output_dict

    def template23(self):
        final_dict = {}
        final_dict["template"] = 23

        map_dict = self.load_map()

        final_dict = self.template10_helper(
            "23", final_dict, map_dict["actions"][1], "title"
        )
        final_dict = self.template10_helper(
            "23", final_dict, map_dict["input"][1], "input"
        )
        final_dict = self.template10_helper(
            "23", final_dict, map_dict["hypotheses"][1], "hypothesis"
        )

        self.slides_collection.append(final_dict)

        output_dict = {}
        output_dict["slides"] = self.slides_collection

        return output_dict

    def template24(self):
        final_dict = {}
        final_dict["template"] = 24

        map_dict = self.load_map()

        final_dict = self.template10_helper(
            "24", final_dict, map_dict["actions"][2], "title"
        )
        final_dict = self.template10_helper(
            "24", final_dict, map_dict["input"][2], "input"
        )
        final_dict = self.template10_helper(
            "24", final_dict, map_dict["hypotheses"][2], "hypothesis"
        )

        self.slides_collection.append(final_dict)

        output_dict = {}
        output_dict["slides"] = self.slides_collection

        return output_dict

    def template25(self):
        final_dict = {}
        final_dict["template"] = 25

        map_dict = self.load_map()

        final_dict = self.template10_helper(
            "25", final_dict, map_dict["actions"][3], "title"
        )
        final_dict = self.template10_helper(
            "25", final_dict, map_dict["input"][3], "input"
        )
        final_dict = self.template10_helper(
            "25", final_dict, map_dict["hypotheses"][3], "hypothesis"
        )

        self.slides_collection.append(final_dict)

        output_dict = {}
        output_dict["slides"] = self.slides_collection

        return output_dict

    def template26(self):
        final_dict = {}
        final_dict["template"] = 26

        map_dict = self.load_map()

        final_dict = self.template10_helper(
            "26", final_dict, map_dict["actions"][4], "title"
        )
        final_dict = self.template10_helper(
            "26", final_dict, map_dict["input"][4], "input"
        )
        final_dict = self.template10_helper(
            "26", final_dict, map_dict["hypotheses"][4], "hypothesis"
        )

        self.slides_collection.append(final_dict)

        output_dict = {}
        output_dict["slides"] = self.slides_collection

        return output_dict

    def template27(self):
        final_dict = {}
        final_dict["template"] = 27

        map_dict = self.load_map()

        for i in range(len(map_dict["conclusions"])):
            final_dict = self.template10_helper(
                "27", final_dict, map_dict["conclusions"][i], "map" + str(i + 1)
            )

        self.slides_collection.append(final_dict)

        output_dict = {}
        output_dict["slides"] = self.slides_collection

        return output_dict

    def template28(self):
        final_dict = {}
        final_dict["template"] = 28

        actions_dict = self.load_actions()

        for i in range(len(actions_dict["intro_aware"])):
            final_dict = self.template10_helper(
                "28", final_dict, actions_dict["intro_aware"][i], "aws_" + str(i + 1)
            )
            final_dict = self.template10_helper(
                "28", final_dict, actions_dict["intro_consi"][i], "cons_" + str(i + 1)
            )
            final_dict = self.template10_helper(
                "28", final_dict, actions_dict["intro_conv"][i], "conv_" + str(i + 1)
            )
            final_dict = self.template10_helper(
                "28", final_dict, actions_dict["intro_loy"][i], "loy_" + str(i + 1)
            )

        self.slides_collection.append(final_dict)

        output_dict = {}
        output_dict["slides"] = self.slides_collection

        return output_dict

    def template29_30_31(self):
        actions_dict = self.load_actions()

        for i in range(0, 3):
            final_dict = {}
            final_dict["template"] = 29 + i

            final_dict = self.template10_helper(
                str(i + 29), final_dict, actions_dict["awareness_keys"][i], "title"
            )
            final_dict = self.template10_helper(
                str(i + 29), final_dict, actions_dict["awareness_values"][i][0], "text"
            )

            self.slides_collection.append(final_dict)

        output_dict = {}
        output_dict["slides"] = self.slides_collection

        return output_dict

    def template32_33_34(self):
        actions_dict = self.load_actions()

        for i in range(0, 3):
            final_dict = {}
            final_dict["template"] = 32 + i

            final_dict = self.template10_helper(
                str(i + 29), final_dict, actions_dict["consideration_keys"][i], "title"
            )
            final_dict = self.template10_helper(
                str(i + 29),
                final_dict,
                actions_dict["consideration_values"][i][0],
                "text",
            )

            self.slides_collection.append(final_dict)

        output_dict = {}
        output_dict["slides"] = self.slides_collection

        return output_dict

    def template35_36_37(self):
        actions_dict = self.load_actions()

        for i in range(0, 3):
            final_dict = {}
            final_dict["template"] = 35 + i

            final_dict = self.template10_helper(
                str(i + 29), final_dict, actions_dict["conversion_keys"][i], "title"
            )
            final_dict = self.template10_helper(
                str(i + 29), final_dict, actions_dict["conversion_values"][i][0], "text"
            )

            self.slides_collection.append(final_dict)

        output_dict = {}
        output_dict["slides"] = self.slides_collection

        return output_dict

    def template38_39_40(self):
        actions_dict = self.load_actions()

        for i in range(0, 3):
            final_dict = {}
            final_dict["template"] = 38 + i

            final_dict = self.template10_helper(
                str(i + 29), final_dict, actions_dict["loyalty_keys"][i], "title"
            )
            final_dict = self.template10_helper(
                str(i + 29), final_dict, actions_dict["loyalty_values"][i][0], "text"
            )

            self.slides_collection.append(final_dict)

        output_dict = {}
        output_dict["slides"] = self.slides_collection

        return output_dict

    def template41(self):
        deploy_dict = self.load_deploy()

        final_dict = {}
        final_dict["template"] = 41

        final_dict = self.template10_helper(
            "41", final_dict, deploy_dict["step1"][0], "text"
        )

        self.slides_collection.append(final_dict)

        output_dict = {}
        output_dict["slides"] = self.slides_collection

        return output_dict

    def template42(self):
        deploy_dict = self.load_deploy()

        final_dict = {}
        final_dict["template"] = 42

        for i in range(0, 2):
            final_dict = self.template10_helper(
                "42", final_dict, deploy_dict["step2_keys"][i], "title" + str(i + 1)
            )
            final_dict = self.template10_helper(
                "42", final_dict, deploy_dict["step2_values"][i][0], "text" + str(i + 1)
            )

        self.slides_collection.append(final_dict)

        output_dict = {}
        output_dict["slides"] = self.slides_collection

        return output_dict

    def template43(self):
        deploy_dict = self.load_deploy()

        final_dict = {}
        final_dict["template"] = 43

        final_dict = self.table_helper(
            final_dict, deploy_dict["step3_rows"], "gov_model_table"
        )

        self.slides_collection.append(final_dict)

        output_dict = {}
        output_dict["slides"] = self.slides_collection

        return output_dict

    def template44(self):
        deploy_dict = self.load_deploy()

        final_dict = {}
        final_dict["template"] = 44

        final_dict = self.template10_helper(
            "44", final_dict, deploy_dict["step4"], "text"
        )

        self.slides_collection.append(final_dict)

        output_dict = {}
        output_dict["slides"] = self.slides_collection

        return output_dict

    def template45(self):
        deploy_dict = self.load_deploy()

        final_dict = {}
        final_dict["template"] = 45

        final_dict = self.template10_helper(
            "45", final_dict, deploy_dict["step5"], "text"
        )

        self.slides_collection.append(final_dict)

        output_dict = {}
        output_dict["slides"] = self.slides_collection

        return output_dict

    def template46(self):
        deploy_dict = self.load_deploy()

        final_dict = {}
        final_dict["template"] = 46

        final_dict = self.table_helper(
            final_dict, deploy_dict["step6"], "key_mil_table"
        )

        self.slides_collection.append(final_dict)

        output_dict = {}
        output_dict["slides"] = self.slides_collection

        return output_dict

    def template47(self):
        deploy_dict = self.load_deploy()

        final_dict = {}
        final_dict["template"] = 47

        final_dict = self.table_helper(
            final_dict, deploy_dict["step7_rows"], "deploy_table"
        )

        self.slides_collection.append(final_dict)

        output_dict = {}
        output_dict["slides"] = self.slides_collection

        return output_dict

    def template48(self):
        deploy_dict = self.load_deploy()

        final_dict = {}
        final_dict["template"] = 48

        final_dict = self.template10_helper(
            "48", final_dict, deploy_dict["step8"], "text"
        )

        self.slides_collection.append(final_dict)

        output_dict = {}
        output_dict["slides"] = self.slides_collection

        return output_dict

    def template49(self):
        template_dict = {"template": 49}
        self.slides_collection.append(template_dict)

        output_dict = {}
        output_dict["slides"] = self.slides_collection
        return output_dict

