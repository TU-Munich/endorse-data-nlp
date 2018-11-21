from werkzeug.datastructures import FileStorage
from flask import Flask
from flask_restplus import Api

upload_parser = api.parser()
upload_parser.add_argument('file', location='files',
                           type=FileStorage, required=True)


@api.route('/upload/')
@api.expect(upload_parser)
class Upload(Resource):
    def post(self):
        uploaded_file = args['file']  # This is FileStorage instance
        url = do_something_with_file(uploaded_file)
        return {'url': url}, 201