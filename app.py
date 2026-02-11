from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Config for AI (Keep this for the Tutor/Chat mode)
genai.configure(api_key="AIzaSyBXeBl_HLaMFEOh1pGIDdMxF-njXkuUlr0")
model = genai.GenerativeModel('gemini-1.5-flash')

# LOCAL KNOWLEDGE BASE (No API needed for these!)
# This ensures your Roadmap and Quiz work even if the API fails.
KNOWLEDGE_BASE = {
    "python": {
        "roadmap": "Phase 1: Basics • Syntax, Variables, Data Types • Control Flow (If-Else, Loops) Phase 2: Intermediate Functions & Modules • File Handling Phase 3: Advanced • OOPs Concepts • Working with APIs",
        "quiz": "1. What is the correct extension for Python files? (.py / .pt) 2. Which keyword is used to create a function? (def / func) 3. Is Python case sensitive? (Yes / No)"
    },
    "web development": {
        "roadmap": "Week 1: HTML5 • Semantic tags, Forms, Media Week 2: CSS3 • Flexbox, Grid, Animations Week 3: JavaScript • DOM Manipulation, ES6 Syntax",
        "quiz": "1. What does HTML stand for? 2. Which CSS property changes text color? 3. What is 'NaN' in JavaScript?"
    },
    "java": {
        "roadmap": "Step 1: JSE • JVM, JRE, JDK • Data Types & Operators Step 2: Collections • List, Set, Map interfaces Step 3: Frameworks • Spring Boot basics",
        "quiz": "1. Java is owned by which company? 2. What is the default value of an integer variable in Java? 3. What is a Constructor?"
    },
    "data science": {
        "roadmap": "Step 1: Math & Stats\n- Linear Algebra & Calculus\n- Probability Distributions\n\nStep 2: Python Libraries\n- NumPy & Pandas (Data Prep)\n- Matplotlib (Visualization)\n\nStep 3: Machine Learning\n- Scikit-Learn Basics\n- Linear Regression",
        "quiz": "1. Which library is best for data frames? (Pandas / Matplotlib)\n2. What is supervised learning?\n3. What does 'Clean Data' mean?"
    },
    "machine learning": {
        "roadmap": "Step 1: Foundations\n- Supervised vs Unsupervised\n- Overfitting & Underfitting\n\nStep 2: Algorithms\n- Decision Trees & Random Forest\n- Neural Networks basics\n\nStep 3: Deployment\n- Model Exporting\n- Cloud Hosting (AWS/GCP)",
        "quiz": "1. Name one unsupervised learning algorithm.\n2. What is the purpose of a 'test set'?\n3. What is an Activation Function?"
    },
    "cyber security": {
        "roadmap": "1. Networking\n- TCP/IP, DNS, HTTP/S\n- Packet Analysis (Wireshark)\n\n2. Security Basics\n- Cryptography & Hashing\n- Firewall Configuration\n\n3. Pentesting\n- OWASP Top 10\n- Metasploit Framework",
        "quiz": "1. What does 'HTTPS' stand for?\n2. What is a 'Brute Force' attack?\n3. Define Multi-Factor Authentication (MFA)."
    },
    "c++": {
        "roadmap": "1. Fundamentals\n- Pointers & Memory Management\n- Input/Output (iostream)\n\n2. OOPs\n- Classes, Objects, Inheritance\n- Polymorphism & Abstraction\n\n3. STL\n- Vectors, Maps, and Queues",
        "quiz": "1. What is a Pointer?\n2. Which operator is used for access? (-> / .)\n3. What is a 'Class' in C++?"
    },
    "artificial intelligence": {
        "roadmap": "1. Introduction\n- History of AI and Turing Test\n- Search Algorithms (BFS, DFS, A*)\n\n2. Knowledge Representation\n- Logic and Reasoning\n- Probability & Bayesian Networks\n\n3. Modern AI\n- Natural Language Processing\n- Computer Vision Basics",
        "quiz": "1. Who is considered the father of AI?\n2. What does 'NLP' stand for?\n3. What is a heuristic in search algorithms?"
    },
    "cloud computing": {
        "roadmap": "1. Virtualization Basics\n- Hypervisors and Virtual Machines\n- Containers vs VMs\n\n2. Service Models\n- IaaS, PaaS, and SaaS\n- Public vs Private vs Hybrid Cloud\n\n3. Major Platforms\n- AWS (EC2, S3)\n- Microsoft Azure\n- Google Cloud Platform (GCP)",
        "quiz": "1. What does 'SaaS' stand for?\n2. Name three major cloud providers.\n3. What is the main benefit of Auto-scaling?"
    },
    "data structures": {
        "roadmap": "1. Linear Structures\n- Arrays and Linked Lists\n- Stacks and Queues\n\n2. Non-Linear Structures\n- Trees (Binary, AVL)\n- Graphs (BFS, DFS)\n\n3. Algorithms\n- Sorting (Quick, Merge)\n- Searching (Binary Search)\n- Time Complexity (Big O)",
        "quiz": "1. Which data structure follows LIFO (Last In First Out)?\n2. What is the time complexity of Binary Search?\n3. What is a 'root' in a tree structure?"
    },
    "operating systems": {
        "roadmap": "1. Process Management\n- Threads and Processes\n- CPU Scheduling Algorithms\n\n2. Memory Management\n- Paging and Segmentation\n- Virtual Memory and RAM\n\n3. Storage & Security\n- File Systems (NTFS, FAT32)\n- Deadlocks and Prevention",
        "quiz": "1. What is the difference between a Process and a Thread?\n2. What is a Deadlock?\n3. What does the 'Kernel' do in an OS?"
    },
    "database management": {
        "roadmap": "1. SQL (Relational)\n- ER Diagrams\n- Normalization (1NF, 2NF, 3NF)\n- Joins and Subqueries\n\n2. NoSQL (Non-Relational)\n- Document Stores (MongoDB)\n- Key-Value Pairs (Redis)\n\n3. Advanced Topics\n- ACID Properties\n- Database Indexing",
        "quiz": "1. What is a Primary Key?\n2. What does 'ACID' stand for in databases?\n3. Which command is used to retrieve data in SQL?"
    },
    "software engineering": {
        "roadmap": "1. SDLC Models\n- Waterfall Model\n- Agile and Scrum\n\n2. Design Patterns\n- Singleton, Factory, Observer\n- SOLID Principles\n\n3. Testing & DevOps\n- Unit vs Integration Testing\n- CI/CD Pipelines\n- Version Control (Git/GitHub)",
        "quiz": "1. What is the 'Agile' methodology?\n2. What does 'DRY' stand for in coding? (Don't Repeat Yourself)\n3. What is a 'Sprint' in Scrum?"
    },
    "app development": {
        "roadmap": "1. Platform Choice\n- Native (Swift for iOS, Kotlin for Android)\n- Cross-Platform (Flutter or React Native)\n\n2. UI/UX Design\n- Material Design / Human Interface Guidelines\n- Navigation Patterns\n\n3. Backend Integration\n- Firebase Authentication\n- Push Notifications\n- Local Storage (SQLite)",
        "quiz": "1. Which language is primarily used for iOS development?\n2. What is 'Flutter' developed by?\n3. What is the purpose of an API in mobile apps?"
    },
    "blockchain": {
        "roadmap": "1. Fundamentals\n- Decentralization & Peer-to-Peer\n- Hashing & Cryptographic signatures\n\n2. Smart Contracts\n- Solidity basics (Ethereum)\n- Gas fees and Wallets (MetaMask)\n\n3. Advanced Concepts\n- Proof of Work vs Proof of Stake\n- NFTs and DeFi apps",
        "quiz": "1. What is a 'Block' in a blockchain?\n2. What does 'Decentralized' mean?\n3. Name a popular cryptocurrency platform for Smart Contracts."
    },
    "internet of things": {
        "roadmap": "1. Hardware Basics\n- Microcontrollers (Arduino, Raspberry Pi)\n- Sensors and Actuators\n\n2. Communication\n- MQTT and CoAP protocols\n- Bluetooth & Wi-Fi integration\n\n3. Data Processing\n- Edge Computing\n- Cloud storage for IoT data",
        "quiz": "1. What does 'IoT' stand for?\n2. Give one example of a smart home IoT device.\n3. What is a 'Sensor'?"
    },
    "computer networks": {
        "roadmap": "1. Layered Models\n- OSI Model (7 Layers)\n- TCP/IP Protocol Suite\n\n2. Hardware\n- Routers, Switches, and Hubs\n- IP Addressing (IPv4 vs IPv6)\n\n3. Security & DNS\n- Domain Name System\n- VPNs and Firewalls",
        "quiz": "1. What is an IP address?\n2. Which layer of the OSI model handles routing?\n3. What is the difference between a Hub and a Switch?"
    },
    "ui/ux design": {
        "roadmap": "1. User Research\n- Personas and User Journeys\n- Problem Statements\n\n2. Wireframing\n- Low-fidelity sketches\n- High-fidelity prototypes (Figma/Adobe XD)\n\n3. Design Principles\n- Color Theory & Typography\n- Accessibility (WCAG) standards",
        "quiz": "1. What is the difference between UI and UX?\n2. What is a 'Wireframe'?\n3. Why is white space important in design?"
    },
    "digital marketing": {
        "roadmap": "1. SEO (Search Engine Optimization)\n- Keywords and Backlinks\n- On-page vs Off-page SEO\n\n2. Content & Social\n- Social Media Strategy\n- Email Marketing funnels\n\n3. Analytics\n- Google Analytics (GA4)\n- Conversion Rates and ROI",
        "quiz": "1. What does 'SEO' stand for?\n2. What is a 'Call to Action' (CTA)?\n3. Name one tool used for tracking website traffic."
    },
    "game development": {
        "roadmap": "1. Game Engines\n- Unity (C#) or Unreal Engine (C++)\n- Godot (GDScript)\n\n2. Core Mechanics\n- Physics (Collisions/Gravity)\n- Input handling (Keyboard/Controller)\n\n3. Graphics & Audio\n- 2D Sprites vs 3D Models\n- Sound effects and background music",
        "quiz": "1. Which engine uses the C# language?\n2. What is a 'Sprite' in game design?\n3. What is 'Collision Detection'?"
    }
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/ai_engine', methods=['POST'])
def ai_engine():
    data = request.json
    mode = data.get('mode') # This will be 'roadmap' or 'quiz'
    topic = data.get('topic', '').lower().strip()

    if topic in KNOWLEDGE_BASE:
        # result = KNOWLEDGE_BASE['python']['quiz']
        result = KNOWLEDGE_BASE[topic][mode] 
        return jsonify({"result": result})
    else:
        available = ", ".join(KNOWLEDGE_BASE.keys())
        return jsonify({"result": f"Topic not found. Try: {available}"})

if __name__ == '__main__':
    app.run(debug=True)