import re
import pandas as pd

def extract_contact_number_from_resume(text):
    contact_number = None

    # Use regex pattern to find a potential contact number
    pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
    match = re.search(pattern, text)
    if match:
        contact_number = match.group()

    return contact_number

def extract_email_from_resume(text):
    email = None

    # Use regex pattern to find a potential email address
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    match = re.search(pattern, text)
    if match:
        email = match.group()

    return email


def extract_skills_from_resume(text, skills_list):
    skills = []

    # Tokenize the resume text (split it into words)
    tokens = re.findall(r'\b\w+\b', text)

    for skill in skills_list:
        # Use a regular expression pattern with word boundaries and case-insensitive search
        pattern = r"\b{}\b".format(re.escape(skill), re.IGNORECASE)
        for token in tokens:
            if re.search(pattern, token):
                skills.append(skill)
                break  # Stop searching for the current skill once found

    return skills


def extract_name(resume_text):
    # Define a regular expression pattern for names
    name_pattern = r'([A-Z][a-z]+)(?:\s+[A-Z][a-z]+)+'
    
    # Search for the name pattern in the resume text
    match = re.search(name_pattern, resume_text)
    
    if match:
        return match.group(0)  # Return the matched name
    else:
        return None  # Return None if no name is found

def extract_education_from_resume(text):
    education = []

    # List of education keywords to match against
    education_keywords = ['Bsc', 'B. Pharmacy', 'B Pharmacy', 'Msc', 'M. Pharmacy', 'Ph.D', 'Bachelor', 'Master', 'B.Tech']

    for keyword in education_keywords:
        pattern = r"(?i)\b{}\b".format(re.escape(keyword))
        match = re.search(pattern, text)
        if match:
            education.append(match.group())

    return education


def extract_internships_from_resume(text):
    internships = []
    roles_list = pd.read_csv("roles.csv")["roles"].tolist()
    # Define keywords related to internships
    internship_keywords = ['Internship', 'Intern', 'Trainee', 'intern', 'Junior', 'junior', 'Senior', 'senior', 'role', 'Role'] + roles_list


    for keyword in internship_keywords:
        pattern = r"(?i)\b{}\b".format(re.escape(keyword))
        matches = re.finditer(pattern, text)
        for match in matches:
            # Extract the surrounding text as the description of the internship
            internship_text = re.search(r'.*?(?=\n\n|\n|$)', text[match.end():], re.DOTALL)
            if internship_text:
                internships.append(internship_text.group().strip())

    return internships


def extract_projects_from_resume(text):
    projects = []
    roles_list = pd.read_csv("roles.csv")["roles"].tolist()
    # Define keywords related to projects
    project_keywords = ['Projects', 'Project', 'Work', 'Experience', 'Job', 'Role', 'role', 'MNIST', 'CNN', 'data'] + roles_list

    for keyword in project_keywords:
        pattern = r"(?i)\b{}\b".format(re.escape(keyword))
        matches = re.finditer(pattern, text)
        for match in matches:
            # Extract the surrounding text as the description of the project
            project_text = re.search(r'.*?(?=\n\n|\n|$)', text[match.end():], re.DOTALL)
            if project_text:
                projects.append(project_text.group().strip())

    return projects


def extract_social_profiles_from_resume(text):
    social_profiles = {}

    # Define social media platform names and their corresponding patterns
    social_media_patterns = {
        'LinkedIn': r'LinkedIn\s*-\s*(\S+)',
        'Twitter': r'Twitter\s*-\s*(\S+)',
        'GitHub': r'GitHub\s*-\s*(\S+)',
        'Medium': r'Medium\s*-\s*(\S+)',
    }

    for platform, pattern in social_media_patterns.items():
        match = re.search(pattern, text)
        if match:
            social_profiles[platform] = match.group(1)

    return social_profiles