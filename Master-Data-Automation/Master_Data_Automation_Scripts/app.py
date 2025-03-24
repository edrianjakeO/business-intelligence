from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import pandas as pd
from conditions_and_classes.name_checker import NameChecker
from conditions_and_classes.excel_processor import ExcelProcessor
from conditions_and_classes.company_code import CompanyCode
from conditions_and_classes.cwid_input import CwidInsert
from conditions_and_classes.save_file import SaveFile
from conditions_and_classes.street1_remove import removeSpecChar
from conditions_and_classes.state_cleanup import StateAbbrev
from conditions_and_classes.timezone_input import TimezoneInput
from conditions_and_classes.phone_number import removeSpecial
from conditions_and_classes.aci_airport import ACIAirport
from conditions_and_classes.relationship import relationshipsCopy
from conditions_and_classes.station_so import StationSO
from conditions_and_classes.postal_canada import PostalCanada
from conditions_and_classes.some_conditions import ExtraCond

app = Flask(__name__)

# Folder setup
UPLOAD_FOLDER = 'uploads/'
CLEANED_FOLDER = 'cleaned/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CLEANED_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CLEANED_FOLDER'] = CLEANED_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "<script>alert('No file part'); window.history.back();</script>"

    file = request.files['file']
    if file.filename == '':
        return "<script>alert('No selected file'); window.history.back();</script>"

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        sheets_dict = check_fileext(file_path, filename)
        if sheets_dict is None:
            return "<script>alert('File type not supported'); window.history.back();</script>"

        # Clean data and get cleaned file path
        cleaned_file = data_cleaning(filename, sheets_dict)
        return redirect(url_for('success', filename=os.path.basename(cleaned_file)))

def check_fileext(file_path, filename):
    """Check file extension and load data accordingly."""
    if filename.endswith('.csv'):
        sheet_name = os.path.splitext(filename)[0]
        sheets_dict = {sheet_name: pd.read_csv(file_path)}
    elif filename.endswith('.xlsx'):
        sheets_dict = pd.read_excel(file_path, sheet_name=None)
    else:
        sheets_dict = None
    return sheets_dict

def data_cleaning(filename, sheets_dict):
    """Process and clean the loaded data."""
    male_names_file = 'male.txt'
    female_names_file = 'female.txt'

    name_checker = NameChecker(male_names_file, female_names_file)
    company_code = CompanyCode(sheets_dict)
    cwid_input = CwidInsert(sheets_dict, filename)
    street1_remove = removeSpecChar(sheets_dict)
    state_cleanup = StateAbbrev(sheets_dict)
    timezone_input = TimezoneInput(sheets_dict)
    phone_number = removeSpecial(sheets_dict)
    aci_airport = ACIAirport(sheets_dict)
    relationship = relationshipsCopy(sheets_dict)
    station_so = StationSO(sheets_dict, filename)
    postal_canada = PostalCanada(sheets_dict)
    some_conditions = ExtraCond(sheets_dict)

    excel_processor = ExcelProcessor(
        sheets_dict, name_checker, company_code, cwid_input, street1_remove,
        state_cleanup, timezone_input, phone_number, aci_airport,
        relationship, station_so, postal_canada, some_conditions
    )

    sheets_dict = excel_processor.process_names('2-Contacts', 0, 100000, 'name1', 'title')
    sheets_dict = company_code.input_code()
    sheets_dict = street1_remove.special_charRemove()
    sheets_dict = state_cleanup.update_states()
    sheets_dict = timezone_input.update_timezones()
    sheets_dict = cwid_input.insert_org()
    sheets_dict = phone_number.remove_Special()
    sheets_dict = aci_airport.update_aci_airport()
    sheets_dict = relationship.update_relationship()
    sheets_dict = station_so.insert_station()
    sheets_dict = postal_canada.postal_checker()
    sheets_dict = some_conditions.clean_email()

    # Define output cleaned filename
    cleaned_filename = f"cleaned_file_{filename}"
    output_file_path = os.path.join(app.config['CLEANED_FOLDER'], cleaned_filename)

    # Save all sheets + autofit using the processor's method
    excel_processor.save_and_autofit(output_file_path)

    return output_file_path
    

@app.route('/success/<filename>')
def success(filename):
    print(f"Rendering success page for file: {filename}")  # Debug print
    return render_template('success.html', filename=filename)

@app.route('/download_file/<filename>')
def download_file(filename):
    cleaned_folder = os.path.abspath(app.config['CLEANED_FOLDER'])  # Use absolute path
    file_path = os.path.join(cleaned_folder, filename)
    print(f"Download requested for: {filename}")
    print(f"Full path: {file_path}")
    print(f"File exists: {os.path.exists(file_path)}")  # Check if file exists with absolute path
    return send_from_directory(cleaned_folder, filename, as_attachment=True)



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)


