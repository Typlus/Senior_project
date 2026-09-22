
import database


def get_all_results():
    # Get all available results from the table
    response = database.supabase.table("detections").select("*").execute()

    results = response.data

    # Return in the same order as the old SQLite SELECT *
    return [
        (
            result["id"],
            result["species"],
            result["filename"],
            result["confidence"]
        )
        for result in results
    ]


def get_result_by_id(detection_id):
    # Get one result from the table
    response = (
        database.supabase
        .table("detections")
        .select("*")
        .eq("id", detection_id)
        .execute()
    )

    if response.data:
        result = response.data[0]

        return {
            "id": result["id"],
            "species": result["species"],
            "filename": result["filename"],
            "confidence": result["confidence"]
        }

    return None


def add_result(filename, species):
    # Add a result to the table
    database.supabase.table("detections").insert({
        "filename": filename,
        "species": species
    }).execute()


def delete_result(detection_id):
    # Delete one result from the table
    response = (
        database.supabase
        .table("detections")
        .delete()
        .eq("id", detection_id)
        .execute()
    )

    return len(response.data)


def results_by_filter(Q1, Q2):
    # Filter by species and minimum confidence
    query = (
        database.supabase
        .table("detections")
        .select("*")
        .gte("confidence", Q2)
    )

    if Q1:
        query = query.in_("species", Q1)

    response = query.execute()

    return [
        (
            result["id"],
            result["species"],
            result["filename"],
            result["confidence"]
        )
        for result in response.data
    ]


def add_demo_data():
    # Add demo data to the table
    demo_data = [
        {"species": "Dolphin", "filename": "dolphin001.wav", "confidence": 95},
        {"species": "Dolphin", "filename": "dolphin002.wav", "confidence": 82},
        {"species": "Dolphin", "filename": "dolphin003.wav", "confidence": 67},
        {"species": "Whale", "filename": "whale001.wav", "confidence": 91},
        {"species": "Whale", "filename": "whale002.wav", "confidence": 76},
        {"species": "Whale", "filename": "whale003.wav", "confidence": 54},
        {"species": "Fish", "filename": "fish001.wav", "confidence": 88},
        {"species": "Fish", "filename": "fish002.wav", "confidence": 72},
        {"species": "Fish", "filename": "fish003.wav", "confidence": 43},
        {"species": "Otter", "filename": "otter001.wav", "confidence": 96},
        {"species": "Otter", "filename": "otter002.wav", "confidence": 81},
        {"species": "Otter", "filename": "otter003.wav", "confidence": 62},
        {"species": "Dolphin", "filename": "dolphin004.wav", "confidence": 74},
        {"species": "Whale", "filename": "whale004.wav", "confidence": 69},
        {"species": "Fish", "filename": "fish004.wav", "confidence": 97}
    ]

    database.supabase.table("detections").insert(demo_data).execute()


def clear_database():
    # Delete all records from the table
    database.supabase.table("detections").delete().neq("id", 0).execute()

