# -*- coding: utf-8 -*-
from json import dump, load
from .export import get_questionnaire_language
from survey.abc_search_engine import Questionnaires


BASE_DIRECTORY = "NES_EXPORT"
PER_PARTICIPANT_DIRECTORY = "Per_participant"
PER_QUESTIONNAIRE_DIRECTORY = "Per_questionnaire"
EXPORT_FILENAME = "export.zip"

EXPORT_PER_PARTICIPANT = 1
EXPORT_PER_QUESTIONNAIRE = 1

DEFAULT_LANGUAGE = "pt-BR"
PREFIX_FILENAME_FIELDS = "Fields"
PREFIX_FILENAME_RESPONSES = "Responses"

OUTPUT_FILENAME_PARTICIPANTS = "Participants"
OUTPUT_FILENAME_DIAGNOSIS = "Diagnosis"


class InputExport:
    def __init__(self):
        self.data = {}

    def read(self, input_filename, update_input_data=True):
        print("read")

        with open(input_filename.encode('utf-8'), 'r') as input_file:
            input_data_temp = load(self.data, input_file)

            if update_input_data:
                self.data = input_data_temp

        return self.data

    def write(self, output_filename):
        print("write")
        with open(output_filename.encode('utf-8'), 'w', encoding='UTF-8') as outfile:
            dump(self.data, outfile)

    def build_header(self):
        print("header")
        self.data["base_directory"] = BASE_DIRECTORY
        self.data["per_participant_directory"] = PER_PARTICIPANT_DIRECTORY
        self.data["per_questionnaire_directory"] = PER_QUESTIONNAIRE_DIRECTORY
        self.data["export_filename"] = EXPORT_FILENAME

    def build_dynamic_header(self, variable_name, variable_data):
        self.data[variable_name] = variable_data

    def build_diagnosis_participant(self, strut_name, output_filename, field_header_list):
        print("participant or diagnosis")
        self.data[strut_name] = []
        self.data[strut_name].append({"output_filename": output_filename, "output_list": []})

        # field_header_list[0] -> field
        # field_header_list[1] -> header
        for field, header in field_header_list:
            output_data = {"header": header, "field": field}
            self.data[strut_name][0]["output_list"].append(output_data)
            # self.data[strut_name][0]["output_list"]

    def build_questionnaire(self, questionnaire_list, language=DEFAULT_LANGUAGE):
        print("questionnaire")

        self.data["questionnaires"] = []

        questionnaire_lime_survey = Questionnaires()

        for sid, title, field_header_list in questionnaire_list:
            language = get_questionnaire_language(questionnaire_lime_survey, sid, language)

            self.data["questionnaires"].append({"id": sid, "language": language,
                                                "prefix_filename_fields": PREFIX_FILENAME_FIELDS,
                                                "questionnaire_name": title,
                                                "prefix_filename_responses": PREFIX_FILENAME_RESPONSES,
                                                "output_list": []})
            for header, field in field_header_list:
                output_data = {"header": header, "field": field}
                self.data["questionnaires"][-1]["output_list"].append(output_data)
                # ["header"] = header
                # self.data["questionnaires"][0]["output_list"]["field"] = field

        questionnaire_lime_survey.release_session_key()


def build_complete_export_structure(export_per_participant, export_per_questionnaire, participant_field_header_list,
                                    diagnosis_field_header_list, questionnaires_list, response_type, heading_type,
                                    output_filename, language=DEFAULT_LANGUAGE):

    json_data = InputExport()

    json_data.build_header()

    json_data.build_dynamic_header("export_per_participant", export_per_participant)

    json_data.build_dynamic_header("export_per_questionnaire", export_per_questionnaire)

    json_data.build_dynamic_header("response_type", response_type)

    json_data.build_dynamic_header("heading_type", heading_type)

    json_data.build_diagnosis_participant("participants", OUTPUT_FILENAME_PARTICIPANTS, participant_field_header_list)

    json_data.build_diagnosis_participant("diagnosis", OUTPUT_FILENAME_DIAGNOSIS, diagnosis_field_header_list)

    json_data.build_questionnaire(questionnaires_list, language)

    json_data.write(output_filename)
