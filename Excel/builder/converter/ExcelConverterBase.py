import sys
sys.path.append("/opt/")
import codecs
import json
import os
import string
from abc import abstractmethod

from jinja2 import Environment, FileSystemLoader
from openpyxl import load_workbook


class ExcelConverterBase(object):
    def __init__(self, workbook_path_name, lexjson_dir):
        dir_path = os.path.dirname(os.path.abspath(__file__))
        self.data = []
        self.templateDir = os.path.join(dir_path, "template")
        self.outputDir = lexjson_dir
        # todo: refactor into json generator and builder base.
        if workbook_path_name is not None:
            self.wb = load_workbook(workbook_path_name)
            self.worksheets = self.wb.get_sheet_names()
            self.namespace = os.path.splitext(
                os.path.basename(workbook_path_name))[0]
            self.intents = [
                self.namespace + "_" + elem for elem in self.worksheets
                if elem.endswith("Intent")
            ]
            self.slot_types = [
                self.namespace + "_" + elem for elem in self.worksheets
                if elem.endswith("Type")
            ]
            self.bots = [
                self.namespace + "_" + elem for elem in self.worksheets
                if elem.endswith("Bot")
            ]
        else:
            self.wb = None
            files = os.listdir(os.path.join(dir_path, lexjson_dir))
            self.worksheets = [
                os.path.splitext(os.path.basename(fn))[0] for fn in files
            ]
            self.namespace = [x for x in self.worksheets
                              if "_" in x][0].split("_")[0]
            self.intents = [
                elem for elem in self.worksheets if elem.endswith("Intent")
            ]
            self.slot_types = [
                elem for elem in self.worksheets if elem.endswith("Type")
            ]
            self.bots = [
                elem for elem in self.worksheets if elem.endswith("Bot")
            ]

    @staticmethod
    def __get_ascii_only_json_str(c: str):
        a = codecs.encode(codecs.decode(c, 'unicode-escape'), 'ascii',
                          'ignore')
        return json.dumps(str(a, 'utf-8'), indent=4)

    def _render(self, filename: str, data: dict, is_json: bool) -> str:
        j2_env = Environment(loader=FileSystemLoader(self.templateDir),
                             trim_blocks=True)
        template = j2_env.get_template(filename).render(**data)
        if is_json:
            template = str.encode(template, 'utf-8')
            template = template.decode('unicode_escape').encode(
                'ascii', 'ignore')
            print(template)
            return json.dumps(json.loads(template), indent=4)
        else:
            return template

    def _save_json_template(self, template_filename: str, save_filename: str,
                            data: dict):
        with open(os.path.join(self.outputDir, save_filename + '.json'),
                  "w+",
                  encoding='utf8') as text_file:
            print(self._render(template_filename, data, True), file=text_file)

    def _save_yaml_template(self, template_filename: str, save_filename: str,
                            data: dict):
        with open(os.path.join(self.outputDir, save_filename + '.yaml'),
                  "w+",
                  encoding='utf8') as text_file:
            print(self._render(template_filename, data, False), file=text_file)

    def populate_simple_cell_data(self, sheet_name: str, data: dict):
        data = self._get_single_value_cell_data(sheet_name, data)
        data["name"] = json.dumps(sheet_name)
        return data

    @staticmethod
    def none_string_to_none(myString):
        return None if myString == '"None"' else myString

    @staticmethod
    def _get_cell_value(worksheet, address, json_encode=True):
        val = str(worksheet[address].value)
        if not val.isdigit() and json_encode:
            return json.dumps(val)
        return val

    def _get_variable_length_column_data(self,
                                         column: int,
                                         start_row: int,
                                         worksheet,
                                         json_encode=True):
        data = []
        i = start_row
        column = string.ascii_uppercase[column - 1]
        while worksheet[column + str(i)].value is not None and worksheet[
                column + str(i)].value:
            data.append(
                self._get_cell_value(worksheet, column + str(i), json_encode))
            i = i + 1
        return data

    def _get_variable_length_row_data(self,
                                      column: int,
                                      row: int,
                                      worksheet,
                                      json_encode=True):
        data = []
        i = column
        column = string.ascii_uppercase[i - 1]
        while worksheet[column + str(row)].value is not None and worksheet[
                column + str(row)].value:
            data.append(
                self._get_cell_value(worksheet, column + str(row),
                                     json_encode))
            i = i + 1
            column = string.ascii_uppercase[i - 1]
        return data

    def _get_newline_spilt_data(self, column: int, row: int, worksheet):
        i = column
        column = string.ascii_uppercase[i - 1]
        content = self._get_cell_value(worksheet, column + str(row), False)
        return self._get_new_line_list(content)

    def _get_new_line_list(self, content: str):
        if '\n' in content:
            return list(
                map(self.__get_ascii_only_json_str, content.split('\n')))
        else:
            return [self.__get_ascii_only_json_str(content)]

    def _get_single_value_cell_data(self, sheet_name: str, data: dict):
        worksheet = self._get_worksheet(sheet_name)
        data = dict(
            map(
                lambda item:
                (item[0], self._get_cell_value(worksheet, item[1])),
                data.items()))
        return data

    def _get_worksheet(self, sheet_name):
        return self.wb[sheet_name.split("_")[1]]

    @abstractmethod
    def generate_json(self):
        pass
