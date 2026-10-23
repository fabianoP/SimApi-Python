import json
from pathlib import Path

from bottle import request, response, route, run

MODEL_ROOT = Path("/home/fmu/code/energy/test")
FMU_ROOT = Path("/home/fmu/code/fmu_location")


@route("/health")
def health():
    return "ok"


@route("/upload/<model_name>", method="POST")
def do_upload(model_name):
    upload = request.files
    save_path = MODEL_ROOT / model_name
    save_path.mkdir(parents=True, exist_ok=True)

    if len(upload) != 2:
        response.status = 400
        return f"Found {len(upload)} files. Expected 2"

    for name, uploaded_file in upload.items():
        print(f"GEN API /UPLOAD FILE SAVE: {name}")
        uploaded_file.save(str(save_path), overwrite=True)

    response.status = 200
    return "2 files uploaded"


@route("/fmu/<model_name>")
def generate(model_name):
    model_directory = MODEL_ROOT / model_name
    idf = model_directory / f"{model_name}.idf"
    epw = model_directory / f"{model_name}.epw"
    if not idf.is_file() or not epw.is_file():
        response.status = 400
        return "No such files"

    fmu_store_dir = FMU_ROOT / model_name
    fmu_store_dir.mkdir(parents=True, exist_ok=True)
    data = {
        "epw_path": str(epw),
        "idf_path": str(idf),
        "fmu_store_dir": str(fmu_store_dir),
    }

    with (model_directory / "data.json").open("w", encoding="utf-8") as data_file:
        json.dump(data, data_file)

    response.status = 200
    return "FMU ready"


if __name__ == "__main__":
    run(host="0.0.0.0", port=8000, debug=False, reloader=False)
