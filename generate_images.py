import os
import json
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import ImageFormatter


class JsonToImageConverter:
    def __init__(self, input_dir='test_artifacts', output_dir='images'):
        self.input_dir = input_dir
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def convert_all_json_to_images(self):
        for root, _, files in os.walk(self.input_dir):
            for file in files:
                if file.endswith('.json'):
                    test_id = self.extract_test_id(file)
                    test_output_dir = os.path.join(self.output_dir, f'Test{test_id}')
                    os.makedirs(test_output_dir, exist_ok=True)
                    self.convert_json_to_image(os.path.join(root, file), test_output_dir)

    def convert_json_to_image(self, json_file_path, output_dir):
        with open(json_file_path, 'r') as json_file:
            json_data = json.load(json_file)
            json_str = json.dumps(json_data, indent=4)

            formatter = ImageFormatter(line_numbers=True, style='colorful', font_size=24, image_scale=4)
            image_data = highlight(json_str, JsonLexer(), formatter)

            output_file_name = os.path.basename(json_file_path).replace('.json', '.png')
            output_file_path = os.path.join(output_dir, output_file_name)
            with open(output_file_path, 'wb') as image_file:
                image_file.write(image_data)

    def extract_test_id(self, file_name):
        return file_name.split('_')[-1].split('.')[0]


if __name__ == '__main__':
    converter = JsonToImageConverter()
    converter.convert_all_json_to_images()
