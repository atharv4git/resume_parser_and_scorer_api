from flask import Flask, request, jsonify
import requests
from extractions import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pdfminer.high_level import extract_text
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/', methods=['POST'])
@cross_origin()
def create_resource():
    try:
        data = request.get_json()  # Get the JSON data from the request

        # URL of the image you want to read
        pdf_url = data['pdf_url']
        response = requests.get(pdf_url)

        def extract_text_from_pdf(pdf_url):
            response = requests.get(pdf_url)
            with open("resume.pdf", "wb") as pdf_file:
                pdf_file.write(response.content)

            # Extract text from the downloaded PDF
            text = extract_text("resume.pdf")
            return text
        


        # Check if the request was successful
        if response.status_code == 200:
            text = extract_text_from_pdf(pdf_url)

            # Store the extracted text in the dictionary
            output_data = {}
            output_data['text'] = text

            name = extract_name(text)
            output_data['name'] = name if name else "Name not found"

            contact_number = extract_contact_number_from_resume(text)
            output_data['contact_number'] = contact_number if contact_number else "Contact Number not found"

            email = extract_email_from_resume(text)
            output_data['email'] = email if email else "Email not found"

            skills_list = ['Python', 'Data Analysis', 'Machine Learning', 'Communication', 'Marketing', 'SEO', 'Digital Marketing', 'Google Analytics', 'Facebook Ads', 'Social Media']
            extracted_skills = extract_skills_from_resume(text, skills_list)
            output_data['skills'] = extracted_skills if extracted_skills else "No skills found"

            extracted_education = extract_education_from_resume(text)
            output_data['education'] = extracted_education if extracted_education else "No education information found"

            extracted_internships_from_resume = extract_internships_from_resume(text)
            output_data['internships'] = extracted_internships_from_resume if extracted_internships_from_resume else "No Internships information found"

            extracted_projects_from_resume = extract_projects_from_resume(text)
            output_data['projects'] = extracted_projects_from_resume if extracted_projects_from_resume else "No Projects information found"

            extracted_social_profiles_from_resume = extract_social_profiles_from_resume(text)
            output_data['social_media'] = extracted_social_profiles_from_resume if extracted_social_profiles_from_resume else "No Social Media information found"

            # Convert the dictionary to a JSON response
            return jsonify(output_data), 201

        else:
            return jsonify({"error": f"Failed to download the image. Status code: {response.status_code}"}), 500

    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"}), 500


# Create a TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer()

def get_tfidf_cosine_similarity(description1, description2):
    # Fit and transform the TF-IDF vectorizer on the descriptions
    tfidf_matrix = tfidf_vectorizer.fit_transform([description1, description2])

    # Calculate cosine similarity between the two TF-IDF vectors
    similarity_score = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]

    return similarity_score

@app.route('/score', methods=['POST'])
def score():
    try:
        data = request.get_json()  # Get the JSON data from the request
        project_description = data.get("project_description")
        applicant_description = data.get("applicant_description")

        # Calculate similarity score using TF-IDF cosine similarity
        similarity_score = get_tfidf_cosine_similarity(project_description, applicant_description)

        output_score = {"score": similarity_score}

        return jsonify(output_score), 201

    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
