developers = [
 {
"name":"Alice",
"role":"Senior Developer",
"experience":5,
"education":{"degree":"MSc in Computer Science","university":"Imperial College London"},
"expertise":"mobile apps",
"tech_stack":[{"language":"Java","proficiency":"expert"},{"language":"Kotlin","proficiency":"intermediate"}],
"past_employers":["MobiTech","AppStart"],
"current_project":{"name":"MobileBank","description":"A next - gen mobile banking solution."},
"accolades":["Best Mobile App Developer 2022","Tech Innovator Award 2021"],
"hobbies":["photography","cycling"]
},
{
"name":"Bob",
"role":"Frontend Developer",
"experience":3,
"education":{"degree":"BSc in Software Engineering","university":"University of Manchester"},
"expertise":" web development",
"tech_stack":[{"language":"JavaScript","proficiency":"expert"},{"language":"React","proficiency":"advanced"}],
"past_employers":["WebGenius","SiteMakers"],
"current_project":{"name":"WebStore","description":"Acomprehensive ecommerce platform."},
"accolades":["Web Developer of the Year 2020"],
"hobbies":["painting","chess"]}]

def doc_struct(dev):
    return {"introduction":[dev['name'],dev['role'],dev['experience'],dev['education']],
            "skills": [dev['expertise'],dev['tech_stack']],
            "experience":[dev['past_employers'],dev['accolades']],
            "current_work":[dev['current_project']],
            "personal":[dev['hobbies']]}

def cont_det(dev):
    return dev

def aggregation (structured_dev):
    aggregatedData = {}

    aggregatedData["introduction"] = f"{structured_dev['introduction'][0]}, a {structured_dev['introduction'][1]} with {structured_dev['introduction'][2]} years of experience, graduated with a {structured_dev['introduction'][3]['degree']} from {structured_dev['introduction'][3]['university']}."

    tech_stack = ', '.join([f"{t['language']} ({t['proficiency']})" for t in structured_dev ["skills" ][1]])
    aggregatedData["skills"] = f"Specialising in { structured_dev['skills'][0]}, they are proficient in {tech_stack}."

    past_employers = ', '.join(structured_dev['experience'][0])
    accolades = ', '. join ( structured_dev ['experience'][1])
    aggregatedData ["experience"] = f"Having previously worked at {past_employers}, they have been awarded with { accolades }."

    project = structured_dev ['current_work'][0]
    aggregatedData ["current_work"] = f"Currently , they 're involved in the project '{ project ['name']}', which is described as: { project ['description']}."

    hobbies = ', '. join ( structured_dev ['personal'][0][: -1]) + ' and ' + structured_dev['personal'][0][ -1]
    aggregatedData ["personal"] = f"Outside of professional life , their interests include { hobbies }."
    return aggregatedData

def lexical_choice ( aggregated_dev ):
    text = aggregated_dev ["skills"].replace("proficient","skilled")
    aggregated_dev["skills"]= text
    return aggregated_dev

def referring_expression ( aggregated_dev ):
    name = aggregated_dev['introduction'].split(',')[0]
# Initial reference with full name
    intro = aggregated_dev["introduction"].replace(name, f"{name} (hereinafter referred to as the developer)")

    # Determine the pronoun based on gender
    pronoun='they'
    possessive_pronoun='their'
    if 'gender' in aggregated_dev :
        if aggregated_dev['gender']. lower() == 'male':
            pronoun = 'he'
            possessive_pronoun = 'his'
        elif aggregated_dev['gender']. lower () == 'female':
            pronoun = 'she'
            possessive_pronoun = 'her'
    # Replace subsequent direct name mentions with the pronoun
    skills = aggregated_dev ["skills"]. replace ( name, pronoun )
    experience = aggregated_dev ["experience"].replace(name,pronoun )
    current_work = aggregated_dev ["current_work"].replace(name,
    pronoun )
    # Adjust for verb conjugation with 'they '
    if pronoun == 'they ':
        current_work = current_work . replace ('has', 'have')

    # Referring back to past employers when discussing current projects , ifrelevant
    if any ( employer in aggregated_dev["current_work"]for employer in aggregated_dev ["experience"][0]) :
        current_work = current_work . replace ("Currently ", f" Following {possessive_pronoun } tenure at {','. join ( aggregated_dev ['experience'][0])}")
    # Handling anaphoric references in personal info (e.g., hobbies )
    personal = aggregated_dev ["personal"]
    if 'coding' in personal :
        personal = personal . replace ('coding', 'this activity') # Assuming a mention of coding as a hobby after introducing profession

    referred_content = {
        "introduction":intro,
        "skills": skills ,
        "experience": experience ,
        "current_work": current_work ,
        "personal": personal
    }
    return referred_content

def realisation(lexical_dev):
    intro = lexical_dev["introduction"]
    skills = "Delving into technicalities, " + lexical_dev["skills"]
    experience = lexical_dev["experience"].replace(", they have", ". Additionally, they have")
    currentWork = "On the present front, " +lexical_dev["current_work"]
    personal = "When away from the code, " +lexical_dev["personal"]
    return f"{intro} {skills} {experience} {currentWork} {personal}"

for dev in developers:
    content = cont_det(dev)
    structured = doc_struct(content)
    aggregated = aggregation(structured)
    lexicallyEnriched = lexical_choice(aggregated)
    referred = referring_expression(lexicallyEnriched)
    final = realisation(referred)
    print(final, "\n")