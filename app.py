from flask import Flask, render_template
from collections import Counter
import pandas as pd
from datetime import datetime
import random

app = Flask(__name__)

def get_job_data():
    jobs = []
    titles = ['Data Scientist', 'Software Engineer', 'Project Manager', 'UX Designer', 'DevOps Engineer']
    skills_list = ['Python', 'JavaScript', 'AWS', 'React', 'SQL', 'Docker', 'Kubernetes', 'Communication']
    cities = ['New York', 'San Francisco', 'Austin', 'Seattle', 'Boston']
    
    base_date = datetime(2025, 5, 1)
    
    for _ in range(150):  # 150 jobs
        title = random.choice(titles)
        skills = random.sample(skills_list, k=random.randint(2,4))
        location = random.choice(cities)
        date_posted = base_date.strftime('%Y-%m-%d')
        base_date += pd.Timedelta(days=random.randint(0,2))
        
        jobs.append({
            'title': title,
            'location': location,
            'skills': skills,
            'date': date_posted
        })
    return pd.DataFrame(jobs)

@app.route('/')
def index():
    df = get_job_data()
    df['skills_str'] = df['skills'].apply(lambda x: ", ".join(x))
    
    top_jobs = df['title'].value_counts().head(5).to_dict()
    all_skills = [skill for skills in df['skills'] for skill in skills]
    top_skills = dict(Counter(all_skills).most_common(10))
    top_cities = df['location'].value_counts().to_dict()
    jobs = df.to_dict(orient='records')
    
    return render_template('index.html',
                           top_jobs=top_jobs,
                           top_skills=top_skills,
                           top_cities=top_cities,
                           jobs=jobs)

if __name__ == '__main__':
    app.run(debug=True)
