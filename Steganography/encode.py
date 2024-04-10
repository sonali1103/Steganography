import io
from flask import Blueprint, redirect, render_template, request, flash, session, url_for
from . import encode_logic
from werkzeug.utils import secure_filename

encode = Blueprint('encode', __name__)

UPLOAD_CARRIER_FOLDER = './Steganography/static/carrierfiles/'
UPLOAD_MESSAGE_FOLDER = './Steganography/static/messagefiles/'
EMBEDED_FOLDER = './Steganography/static/embededfiles/'

ALLOWED_EXTENTIONS = set(['png', "jpeg",'jpg', "heic", "mp4", "mov", "wav", "mp3", "pdf", "txt"])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENTIONS

@encode.route('/encode', methods=['GET'])
def display():
    return render_template('encode.html')
    
@encode.route('/encode', methods=['POST'])
def encode_file():
    cfile = request.files['carrierfile']
    msgfile = request.files['messagefile']
    start_bit = int(request.form.get('start_bit'))
    length = int(request.form.get('len'))
     
    if start_bit <= 0:
        flash('please enter valid start position', category='error')
        return render_template("encode.html")
    if length <= 0:
        flash('please enter valid length (periodicity)', category='error')
        return render_template("encode.html")
    
    if 'file' and allowed_file(cfile.filename) and allowed_file(msgfile.filename):
        cfilename= secure_filename(cfile.filename)
        msgfilename = secure_filename(msgfile.filename)
        
        # carrier and message file path saved in application folder
        carrier_file_path = UPLOAD_CARRIER_FOLDER + cfilename
        message_file_path = UPLOAD_MESSAGE_FOLDER + msgfilename
        
        # save the carrier file and message file in path specified
        cfile.save(carrier_file_path)
        msgfile.save(message_file_path)
        
        carrier_data = encode_logic.get_binary_data(carrier_file_path)
        message_data  = encode_logic.get_binary_data(message_file_path)
        
        # Calculate length of carrier data and message data
        carrier_length = len(carrier_data)
        message_length = len(message_data)
    

        # Check if message can be embedded within carrier
        if message_length > carrier_length:
            flash("Message is too large to embed in carrier file.", category='error')
            return render_template("encode.html") 
        
        embeded_file_path = EMBEDED_FOLDER + cfilename
        session['embeded_file'] = cfilename
        binary_data = encode_logic.embed_message(list(carrier_data), message_data,start_bit,length)
        # flash(binary_data)
        # return render_template("encode.html") 
        if binary_data is False:
            flash('Could not embed complete file, please enter valid L and S')
            render_template("encode.html") 
        else:
            with open(embeded_file_path, 'wb') as f:
                f.write(binary_data)
            flash('Message file embeded successfully')
            return redirect(url_for('decode.displaylist'))    

    else:
        flash('allowed file extentions are - png, jpeg, jpg, heic, mp4, mov, wav, mp3, txt, pdf)')
        return render_template("encode.html")   
    return render_template("encode.html") 