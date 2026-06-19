"""
Seed script to populate practice items with embeddings across multiple domains
Run with: python seed_practice_items.py
"""
from app.db.base import SessionLocal
from app.models.practice_item import PracticeItem
from app.services.embedding_service import generate_embedding

# Multi-domain practice items data
PRACTICE_ITEMS = [
    # ==================== DSA (Data Structures & Algorithms) ====================
    {
        "title": "Two Sum",
        "domain": "DSA",
        "topic": "Arrays",
        "difficulty": "easy",
        "link": "https://leetcode.com/problems/two-sum/",
        "description": "Find two numbers in an array that add up to a target sum. Classic array problem using hash maps.",
        "tags": ["hash-map", "array", "interview"]
    },
    {
        "title": "Best Time to Buy and Sell Stock",
        "domain": "DSA",
        "topic": "Arrays",
        "difficulty": "easy",
        "link": "https://leetcode.com/problems/best-time-to-buy-and-sell-stock/",
        "description": "Find maximum profit from buying and selling stock once. Track minimum price and maximum profit.",
        "tags": ["greedy", "array"]
    },
    {
        "title": "Valid Anagram",
        "domain": "DSA",
        "topic": "Strings",
        "difficulty": "easy",
        "link": "https://leetcode.com/problems/valid-anagram/",
        "description": "Check if two strings are anagrams using character frequency counting.",
        "tags": ["hash-map", "string"]
    },
    {
        "title": "Reverse Linked List",
        "domain": "DSA",
        "topic": "Linked Lists",
        "difficulty": "easy",
        "link": "https://leetcode.com/problems/reverse-linked-list/",
        "description": "Reverse a singly linked list iteratively or recursively.",
        "tags": ["linked-list", "recursion"]
    },
    {
        "title": "Maximum Depth of Binary Tree",
        "domain": "DSA",
        "topic": "Trees",
        "difficulty": "easy",
        "link": "https://leetcode.com/problems/maximum-depth-of-binary-tree/",
        "description": "Find maximum depth using recursive DFS or iterative BFS.",
        "tags": ["tree", "dfs", "bfs"]
    },
    {
        "title": "Number of Islands",
        "domain": "DSA",
        "topic": "Graphs",
        "difficulty": "medium",
        "link": "https://leetcode.com/problems/number-of-islands/",
        "description": "Count connected components in 2D grid using DFS or BFS.",
        "tags": ["graph", "dfs", "bfs"]
    },
    {
        "title": "Climbing Stairs",
        "domain": "DSA",
        "topic": "Dynamic Programming",
        "difficulty": "easy",
        "link": "https://leetcode.com/problems/climbing-stairs/",
        "description": "Classic DP problem similar to Fibonacci sequence.",
        "tags": ["dp", "fibonacci"]
    },
    {
        "title": "Valid Parentheses",
        "domain": "DSA",
        "topic": "Stack",
        "difficulty": "easy",
        "link": "https://leetcode.com/problems/valid-parentheses/",
        "description": "Use stack to validate matching brackets and parentheses.",
        "tags": ["stack", "string"]
    },
    {
        "title": "Binary Search",
        "domain": "DSA",
        "topic": "Binary Search",
        "difficulty": "easy",
        "link": "https://leetcode.com/problems/binary-search/",
        "description": "Classic binary search implementation on sorted array.",
        "tags": ["binary-search", "array"]
    },
    {
        "title": "Merge Two Sorted Lists",
        "domain": "DSA",
        "topic": "Linked Lists",
        "difficulty": "easy",
        "link": "https://leetcode.com/problems/merge-two-sorted-lists/",
        "description": "Merge two sorted linked lists into one sorted list.",
        "tags": ["linked-list", "merge"]
    },
    
    # ==================== React ====================
    {
        "title": "Build a Todo App with Hooks",
        "domain": "React",
        "topic": "React Hooks",
        "difficulty": "easy",
        "link": "https://react.dev/learn/tutorial-tic-tac-toe",
        "description": "Create a todo list application using useState and useEffect hooks. Practice state management and event handling.",
        "tags": ["hooks", "useState", "useEffect", "beginner"]
    },
    {
        "title": "React Router Practice Project",
        "domain": "React",
        "topic": "Routing",
        "difficulty": "medium",
        "link": "https://reactrouter.com/en/main/start/tutorial",
        "description": "Build a multi-page application with React Router. Implement navigation, nested routes, and dynamic routing.",
        "tags": ["react-router", "navigation", "spa"]
    },
    {
        "title": "Component Lifecycle Exercise",
        "domain": "React",
        "topic": "Component Lifecycle",
        "difficulty": "medium",
        "link": "https://react.dev/learn/lifecycle-of-reactive-effects",
        "description": "Understand component mounting, updating, and unmounting. Practice with useEffect cleanup and dependencies.",
        "tags": ["lifecycle", "useEffect", "cleanup"]
    },
    {
        "title": "Build a Weather App with API",
        "domain": "React",
        "topic": "API Integration",
        "difficulty": "medium",
        "link": "https://openweathermap.org/api",
        "description": "Fetch weather data from an API and display it. Practice async operations, error handling, and loading states.",
        "tags": ["api", "fetch", "async", "axios"]
    },
    {
        "title": "Redux State Management",
        "domain": "React",
        "topic": "State Management",
        "difficulty": "hard",
        "link": "https://redux.js.org/tutorials/essentials/part-1-overview-concepts",
        "description": "Implement Redux for global state management. Create store, actions, reducers, and connect to components.",
        "tags": ["redux", "state-management", "actions", "reducers"]
    },
    {
        "title": "Custom Hooks Practice",
        "domain": "React",
        "topic": "Custom Hooks",
        "difficulty": "medium",
        "link": "https://react.dev/learn/reusing-logic-with-custom-hooks",
        "description": "Create reusable custom hooks for common functionality like form handling, data fetching, and local storage.",
        "tags": ["custom-hooks", "reusability", "hooks"]
    },
    {
        "title": "React Context API",
        "domain": "React",
        "topic": "Context API",
        "difficulty": "medium",
        "link": "https://react.dev/learn/passing-data-deeply-with-context",
        "description": "Use Context API for prop drilling solution. Implement theme switching or authentication context.",
        "tags": ["context", "prop-drilling", "global-state"]
    },
    {
        "title": "React Performance Optimization",
        "domain": "React",
        "topic": "Performance",
        "difficulty": "hard",
        "link": "https://react.dev/learn/render-and-commit",
        "description": "Optimize React app with useMemo, useCallback, and React.memo. Understand re-rendering and performance profiling.",
        "tags": ["performance", "useMemo", "useCallback", "optimization"]
    },
    {
        "title": "Form Handling with Formik",
        "domain": "React",
        "topic": "Forms",
        "difficulty": "medium",
        "link": "https://formik.org/docs/tutorial",
        "description": "Build complex forms with validation using Formik and Yup. Handle form state, validation, and submission.",
        "tags": ["forms", "formik", "validation", "yup"]
    },
    {
        "title": "Testing React Components",
        "domain": "React",
        "topic": "Testing",
        "difficulty": "medium",
        "link": "https://testing-library.com/docs/react-testing-library/intro/",
        "description": "Write unit and integration tests using React Testing Library and Jest. Test user interactions and component behavior.",
        "tags": ["testing", "jest", "react-testing-library"]
    },
    
    # ==================== DevOps ====================
    {
        "title": "Dockerize a FastAPI Application",
        "domain": "DevOps",
        "topic": "Docker",
        "difficulty": "easy",
        "link": "https://fastapi.tiangolo.com/deployment/docker/",
        "description": "Create a Dockerfile for a FastAPI app. Build and run containers, understand layers and caching.",
        "tags": ["docker", "containerization", "fastapi"]
    },
    {
        "title": "Create CI/CD Pipeline with GitHub Actions",
        "domain": "DevOps",
        "topic": "CI/CD",
        "difficulty": "medium",
        "link": "https://docs.github.com/en/actions/quickstart",
        "description": "Set up automated testing and deployment pipeline. Configure workflows, jobs, and deployment strategies.",
        "tags": ["ci-cd", "github-actions", "automation"]
    },
    {
        "title": "Kubernetes Basics Lab",
        "domain": "DevOps",
        "topic": "Kubernetes",
        "difficulty": "hard",
        "link": "https://kubernetes.io/docs/tutorials/kubernetes-basics/",
        "description": "Deploy applications to Kubernetes cluster. Learn pods, services, deployments, and scaling.",
        "tags": ["kubernetes", "k8s", "orchestration", "containers"]
    },
    {
        "title": "Infrastructure as Code with Terraform",
        "domain": "DevOps",
        "topic": "IaC",
        "difficulty": "medium",
        "link": "https://developer.hashicorp.com/terraform/tutorials/aws-get-started",
        "description": "Provision cloud infrastructure using Terraform. Write HCL configurations and manage state.",
        "tags": ["terraform", "iac", "infrastructure", "aws"]
    },
    {
        "title": "Set Up Monitoring with Prometheus",
        "domain": "DevOps",
        "topic": "Monitoring",
        "difficulty": "medium",
        "link": "https://prometheus.io/docs/prometheus/latest/getting_started/",
        "description": "Configure Prometheus for application monitoring. Set up metrics collection, alerting, and Grafana dashboards.",
        "tags": ["prometheus", "monitoring", "metrics", "grafana"]
    },
    {
        "title": "Docker Compose Multi-Container App",
        "domain": "DevOps",
        "topic": "Docker Compose",
        "difficulty": "medium",
        "link": "https://docs.docker.com/compose/gettingstarted/",
        "description": "Orchestrate multiple containers with Docker Compose. Define services, networks, and volumes.",
        "tags": ["docker-compose", "multi-container", "orchestration"]
    },
    {
        "title": "AWS EC2 Deployment",
        "domain": "DevOps",
        "topic": "Cloud Deployment",
        "difficulty": "medium",
        "link": "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html",
        "description": "Deploy application to AWS EC2 instance. Configure security groups, SSH access, and load balancing.",
        "tags": ["aws", "ec2", "cloud", "deployment"]
    },
    {
        "title": "Ansible Configuration Management",
        "domain": "DevOps",
        "topic": "Configuration Management",
        "difficulty": "hard",
        "link": "https://docs.ansible.com/ansible/latest/getting_started/index.html",
        "description": "Automate server configuration with Ansible playbooks. Manage multiple servers and deploy applications.",
        "tags": ["ansible", "automation", "configuration"]
    },
    {
        "title": "Jenkins Pipeline Setup",
        "domain": "DevOps",
        "topic": "CI/CD",
        "difficulty": "medium",
        "link": "https://www.jenkins.io/doc/book/pipeline/getting-started/",
        "description": "Create Jenkins pipeline for automated builds and deployments. Configure stages, agents, and post-actions.",
        "tags": ["jenkins", "ci-cd", "pipeline", "automation"]
    },
    {
        "title": "Nginx Reverse Proxy Configuration",
        "domain": "DevOps",
        "topic": "Web Servers",
        "difficulty": "easy",
        "link": "https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/",
        "description": "Configure Nginx as reverse proxy for backend services. Set up load balancing and SSL termination.",
        "tags": ["nginx", "reverse-proxy", "load-balancing"]
    },
    
    # ==================== Machine Learning ====================
    {
        "title": "Train Classifier on Iris Dataset",
        "domain": "Machine Learning",
        "topic": "Classification",
        "difficulty": "easy",
        "link": "https://scikit-learn.org/stable/auto_examples/datasets/plot_iris_dataset.html",
        "description": "Build a classification model using scikit-learn. Train on Iris dataset and evaluate accuracy.",
        "tags": ["classification", "scikit-learn", "supervised-learning"]
    },
    {
        "title": "Build Sentiment Analysis Model",
        "domain": "Machine Learning",
        "topic": "NLP",
        "difficulty": "medium",
        "link": "https://huggingface.co/docs/transformers/tasks/sequence_classification",
        "description": "Create sentiment analysis model using transformers. Process text data and classify sentiments.",
        "tags": ["nlp", "sentiment-analysis", "transformers", "text"]
    },
    {
        "title": "Implement Linear Regression from Scratch",
        "domain": "Machine Learning",
        "topic": "Regression",
        "difficulty": "easy",
        "link": "https://scikit-learn.org/stable/modules/linear_model.html",
        "description": "Code linear regression algorithm without libraries. Understand gradient descent and cost function.",
        "tags": ["regression", "gradient-descent", "fundamentals"]
    },
    {
        "title": "Neural Network with TensorFlow",
        "domain": "Machine Learning",
        "topic": "Deep Learning",
        "difficulty": "medium",
        "link": "https://www.tensorflow.org/tutorials/quickstart/beginner",
        "description": "Build and train a neural network using TensorFlow. Understand layers, activation functions, and backpropagation.",
        "tags": ["tensorflow", "neural-network", "deep-learning"]
    },
    {
        "title": "Image Classification with CNN",
        "domain": "Machine Learning",
        "topic": "Computer Vision",
        "difficulty": "hard",
        "link": "https://www.tensorflow.org/tutorials/images/cnn",
        "description": "Create convolutional neural network for image classification. Train on CIFAR-10 or MNIST dataset.",
        "tags": ["cnn", "computer-vision", "image-classification"]
    },
    {
        "title": "K-Means Clustering",
        "domain": "Machine Learning",
        "topic": "Clustering",
        "difficulty": "easy",
        "link": "https://scikit-learn.org/stable/modules/clustering.html#k-means",
        "description": "Implement K-means clustering algorithm. Visualize clusters and understand unsupervised learning.",
        "tags": ["clustering", "unsupervised-learning", "k-means"]
    },
    {
        "title": "Time Series Forecasting",
        "domain": "Machine Learning",
        "topic": "Time Series",
        "difficulty": "medium",
        "link": "https://www.tensorflow.org/tutorials/structured_data/time_series",
        "description": "Build time series prediction model. Use LSTM or ARIMA for forecasting future values.",
        "tags": ["time-series", "lstm", "forecasting"]
    },
    {
        "title": "Feature Engineering Practice",
        "domain": "Machine Learning",
        "topic": "Feature Engineering",
        "difficulty": "medium",
        "link": "https://scikit-learn.org/stable/modules/preprocessing.html",
        "description": "Learn feature scaling, encoding, and selection. Improve model performance through better features.",
        "tags": ["feature-engineering", "preprocessing", "data-preparation"]
    },
    {
        "title": "Model Evaluation and Metrics",
        "domain": "Machine Learning",
        "topic": "Model Evaluation",
        "difficulty": "easy",
        "link": "https://scikit-learn.org/stable/modules/model_evaluation.html",
        "description": "Understand accuracy, precision, recall, F1-score, and ROC curves. Evaluate model performance properly.",
        "tags": ["evaluation", "metrics", "validation"]
    },
    {
        "title": "Deploy ML Model with FastAPI",
        "domain": "Machine Learning",
        "topic": "Model Deployment",
        "difficulty": "medium",
        "link": "https://fastapi.tiangolo.com/tutorial/",
        "description": "Create REST API for ML model predictions. Serialize model and handle inference requests.",
        "tags": ["deployment", "fastapi", "production", "api"]
    },
]

def seed_practice_items():
    """Seed practice items with embeddings across multiple domains"""
    db = SessionLocal()
    
    try:
        # Check if already seeded
        existing_count = db.query(PracticeItem).count()
        if existing_count > 0:
            print(f"Database already has {existing_count} practice items.")
            response = input("Do you want to re-seed? This will delete all existing items. (yes/no): ")
            if response.lower() != 'yes':
                print("Seeding cancelled.")
                return
            
            # Delete existing items
            db.query(PracticeItem).delete()
            db.commit()
            print("Deleted existing practice items.")
        
        print(f"\nSeeding {len(PRACTICE_ITEMS)} practice items across multiple domains...")
        print("=" * 70)
        
        # Group by domain for progress display
        domains = {}
        for item in PRACTICE_ITEMS:
            domain = item['domain']
            domains[domain] = domains.get(domain, 0) + 1
        
        print("\nDomain breakdown:")
        for domain, count in domains.items():
            print(f"  - {domain}: {count} items")
        print("=" * 70)
        
        for idx, item_data in enumerate(PRACTICE_ITEMS, 1):
            print(f"\n[{idx}/{len(PRACTICE_ITEMS)}] Processing: {item_data['domain']} - {item_data['title']}")
            
            # Generate embedding from domain + topic + title + description
            embedding_text = f"{item_data['domain']} - {item_data['topic']}: {item_data['title']}. {item_data['description']}"
            print(f"  Generating embedding...")
            embedding = generate_embedding(embedding_text)
            
            # Create practice item
            practice_item = PracticeItem(
                title=item_data['title'],
                domain=item_data['domain'],
                topic=item_data['topic'],
                difficulty=item_data['difficulty'],
                link=item_data['link'],
                description=item_data['description'],
                tags=item_data.get('tags', []),
                embedding=embedding
            )
            
            db.add(practice_item)
            print(f"  ✓ Added to database")
        
        db.commit()
        print("\n" + "=" * 70)
        print(f"✅ Successfully seeded {len(PRACTICE_ITEMS)} practice items with embeddings!")
        print("\nDomain summary:")
        for domain, count in domains.items():
            print(f"  ✓ {domain}: {count} items")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error seeding practice items: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 70)
    print("SkillSprint AI - Multi-Domain Practice Items Seeder")
    print("=" * 70)
    seed_practice_items()
