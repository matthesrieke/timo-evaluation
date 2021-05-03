from app import app, openapi, service

from flask import Flask, abort, request, make_response, send_file, jsonify
from flask_swagger_ui import get_swaggerui_blueprint

import os

service_url = os.getenv("SERVICE_URL", "http://localhost")
base_href = os.getenv("BASE_HREF", "/")
openapi_file = '/tmp/openapi.yaml'
API_URL = '%s/v3/api-docs' % service_url  # Our API url (can of course be a local resource)

@app.route("/alleProjekteMonat", methods=["GET"])
def alleProjekteMonat():
    """alleProjekteMonat, gruppiert nach Mitarbeiter und Projekt
    ---
    get:
      parameters:
      - in: query
        name: JSESSIONID
        schema:
          type: string
      - in: query
        name: start
        schema:
          type: string
      - in: query
        name: end
        schema:
          type: string

      responses:
        200:
          description: the evaluation as XSLX
          content:
            application/vnd.openxmlformats-officedocument.spreadsheetml.sheet:
              schema:
                type: string
                format: binary

    """
    
    session = request.args.get('JSESSIONID')
    start = request.args.get('start')
    end = request.args.get('end')
    out_file = service.create_evaluation(start, end, session)
    
    return send_file(out_file, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


@app.route("/leistungsnachweis", methods=["GET"])
def leistungsnachweis():
    """leistungsnachweis, nachprozessiert
    ---
    get:
      parameters:
      - in: query
        name: JSESSIONID
        schema:
          type: string
      - in: query
        name: start
        schema:
          type: string
      - in: query
        name: end
        schema:
          type: string

      responses:
        200:
          description: the evaluation as XSLX
          content:
            application/vnd.openxmlformats-officedocument.spreadsheetml.sheet:
              schema:
                type: string
                format: binary

    """
    
    session = request.args.get('JSESSIONID')
    start = request.args.get('start')
    end = request.args.get('end')
    out_file = service.create_performance_record(start, end, session)
    
    return send_file(out_file, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


@app.errorhandler(ValueError)
def special_exception_handler(error):
    result = dict(
        error = 'Value Error: %s' % error
    )
    return jsonify(result), 500


@app.route("/v3/api-docs", methods=["GET"])
def apidocs():
    return send_file(openapi_file, mimetype='text/x-yaml', as_attachment=True, attachment_filename="openapi.yaml")

# generate the OpenAPI spec
with app.test_request_context():
    openapi.spec.path(view=alleProjekteMonat)
    openapi.spec.path(view=leistungsnachweis)

with open(openapi_file, 'w') as f:
    f.write(openapi.spec.to_yaml())
    f.close()

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    "%sv3/swagger-ui" % base_href,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "TimO Auswertung API"
    }
)

app.register_blueprint(swaggerui_blueprint)
