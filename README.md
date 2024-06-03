---
title: IS5004project
emoji: 🔥
colorFrom: gray
colorTo: yellow
sdk: gradio
sdk_version: 4.28.3
app_file: app.py
pinned: false
---

## SECTION 1 : PROJECT TITLE
## LearnSphere Navigator - A Courseware Intelligent Assistant System

---
## SECTION 2: EXECUTIVE SUMMARY
The Courseware Intelligent Assistant System (CIAS) is designed to revolutionize the way students learn and review course materials. By incorporating advanced Optical Character Recognition (OCR) technology, CIAS can transform paper-based course materials and other non-digital resources into editable digital documents, creating a convenient platform for students. The intelligent agent feature of the system utilizes the content of the courseware and a comprehensive knowledge base to provide real-time answers to students' questions and offer personalized learning guidance. Additionally, the learning and review system generates customized review materials based on the students' learning history, helping them consolidate knowledge more effectively and enhance their learning efficiency.

Students face numerous challenges during their learning process, which can hinder their progress, reduce their efficiency, and even affect their interest in learning. Faced with vast course content and a plethora of learning materials, students often do not know where to start. A lack of clear learning paths can leave them feeling confused and helpless. The diversity and dispersion of course materials, coming from different sources such as classroom notes, textbooks, and online resources, can make it difficult for students to quickly find the information they need when they need it. Overwhelmed by the sheer volume of materials and unsure of where to begin, students may spend a lot of time on their studies but achieve less than desired results. This can lead to low learning efficiency and even a vicious cycle of poor performance. Additionally, students may find it challenging to identify key points during review sessions. Without effective revision strategies, they may perform poorly on exams and tests.

Moreover, students often need to adjust their study methods based on their own progress and requirements during the review phase. However, traditional learning methods often fail to provide personalized guidance, making it difficult for students to find the most suitable learning path for themselves. When students waste time due to these reasons, their learning progress is affected, which may prevent them from mastering the course content within the allotted time. This can also lead to stress and even anxiety. Such psychological burdens can further hinder their learning progress. Facing such continuous learning difficulties, their motivation might gradually decrease, and they might even develop an aversion to learning.

These issues indicate that students face a variety of challenges during their learning process, involving aspects such as learning direction, material management, knowledge understanding, efficiency, review, and psychological pressure. Addressing these issues is key to enhancing student learning outcomes and reducing learning barriers.

The digitization and organization of course materials are highly repetitive and prone to errors. If there are hundreds of course materials in a semester, this means that students need to spend a lot of time handling them. The design of the Courseware Intelligent Assistant System aims to solve these problems by automating processes to increase efficiency, reduce errors, and ensure data consistency. This automation can significantly reduce the time costs for students while improving the quality of courseware organization and management. The main advantages include:

- Fewer manual errors: By reducing manual handling, the system lowers the risk of errors due to human operations.
- Consistency of courseware content: The system ensures that all digitized materials have a uniform format, which facilitates subsequent processing and use.
- Significant time savings: With automated processes, the time saved allows students to invest their energy in more important learning and research work.

By implementing this automated process, the Courseware Intelligent Assistant System provides students with a more efficient and reliable method of managing resources, ensuring that they can access and utilize learning resources more conveniently.

---

## SECTION 3 : CREDITS / PROJECT CONTRIBUTION

| Official Full Name  | Student ID (MTech Applicable)  | Work Items (Who Did What) | Email (Optional) |
| :------------ |:---------------:| :-----| :-----|
|Huang Qichen|A0285822X|contribution|e1221634@u.nus.edu|
|WEICHUANJIE|A0285709N|contribution|e1221521@u.nus.edu|
|Yan Zihan|A0285706W|contribution|e1221518@u.nus.edu|

---
## SECTION 4 : VIDEO OF SYSTEM MODELLING & USE CASE DEMO


---

## SECTION 5 : USER GUIDE

`Refer to FILE`

### 1.1 Install Dependencies

Run the pip install Command:
`pip install -r requirements.txt`

### 1.2 Add your API key

Add your API key into system environment:
`setx OPENAI_API_KEY "your_openai_api_key"`

### 1.3 Starting the Web Application

Run:
`streamlit run '.\Study mode.py'`

---
## SECTION 6 : PROJECT REPORT / PAPER

`Refer to project report at Github Folder: ProjectReport`

---

## SECTION 7 : Further Exploration

A broad view of RAG: https://arxiv.org/pdf/2402.19473

A broad view of Agent: https://arxiv.org/abs/2309.07864

### 7.1 RAG

#### 7.1.1 Foundations
1) Query-baesd RAG
   
    Query-based RAG seamlessly integrates the
user’s query with insights from retrieved information, feeding
it directly into the initial stage of the language model’s input. Most common method.


2) Latent Representation-based RAG


3) Logit-based RAG


4) Speculative RAG

#### 7.1.2 Pipe line and enhancements(methods)

1) Input Enhancement:
    
    Query transformation: HyDE method: use the original query to
generate a pseudo document, which is later used as the query
for retrieval


2) Retriever Enhancement:

    Hybrid Retrieval: Hybrid retrieve denotes the concurrent employment of a diverse array of retrieval methodologies
or the extraction of information from multiple distinct sources(Dense Retriever and sparse retriever). We try C-RAG: CRAG features a retrieval evaluator that gauges document relevance to queries, prompting
three retrieval responses based on confidence: direct use of
results for Knowledge Refinement if accurate, Web Search if
incorrect, and a hybrid approach for ambiguous cases. Related Article: https://blog.csdn.net/L_goodboy/article/details/137581551
    
        
#### 

---
Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference
