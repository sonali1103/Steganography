from flask import Blueprint, make_response, render_template, request, session
from . import decode_logic
import mimetypes
from . import encode_logic

decode = Blueprint('decode', __name__)

EMBEDED_FOLDER = './Steganography/static/embededfiles/'


imgs = {"png", "jpeg","jpg", "heic"}
videos = {"mp4", "mov"}
audios = {"wav", "mp3"}
texts = {"txt", "pdf"}

@decode.route('/decode', methods=['GET'])
def displaylist():
    file_name =  session['embeded_file']
    return render_template('decode.html', file_to_decode =file_name)
        
    

@decode.route('/decode', methods=['POST'])
def extract_message():
    starting_bit = int(request.form.get('start_bit'))
    length = int(request.form.get('len'))
    cfile = request.form.get('file_to_decode_label')
    
    carrier_file = EMBEDED_FOLDER + cfile     
    
    carrier_file_data = encode_logic.get_binary_data(carrier_file)  
    
    message_file_data = decode_logic.extract_file(list(carrier_file_data), starting_bit, length)

    file_type = decode_logic.determine_file_type(message_file_data)

    # Set the file extension based on the detected file type
    extension = mimetypes.guess_extension(file_type.split("/")[1])
    if not extension:
        extension = ".dat"  # default extension if unable to determine
        
        
    response = make_response(message_file_data)
    file_type = file_type.split('/')[-1]
    if file_type == 'plain':
        file_type = 'txt'
    response.headers['Content-Disposition'] = 'attachment; filename=extracted_message.' + file_type.split('/')[-1]
    response.mimetype = file_type
    return response