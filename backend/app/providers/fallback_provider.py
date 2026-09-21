import re
from typing import List, Dict, Any, Optional
from .ai_provider import AIProvider
from ..models.tutor_models import StudentContextModel, QuizModel, QuizOptionModel

class FallbackProvider(AIProvider):
    """
    High-Quality Deterministic Educational Fallback Provider for LearnSync AI.
    Analyzes intent and generates rich, topic-specific educational explanations.
    """

    @property
    def provider_name(self) -> str:
        return "fallback"

    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        explanation_mode: str,
        student_context: Optional[StudentContextModel] = None,
        action: Optional[str] = None
    ) -> Dict[str, Any]:
        last_msg = messages[-1]["content"] if messages else "c programming"
        lower_msg = last_msg.lower()

        # Handle Action: Quiz Me
        if action == "quiz_me":
            return self._build_quiz_response(lower_msg)

        # Handle Action: Practice Topic
        if action == "practice_topic":
            return self._build_practice_response(lower_msg)

        # Topic detection based on actual student question
        subject, topic = self._detect_topic(lower_msg)

        # Build Educational Explanation by Mode
        answer = self._generate_explanation(lower_msg, explanation_mode, subject, topic)
        followups = self._generate_followups(lower_msg, subject, topic)

        return {
            "answer": answer,
            "explanation_mode": explanation_mode,
            "topic": topic,
            "subject": subject,
            "suggested_followups": followups,
            "quiz": None,
        }

    def _detect_topic(self, text: str) -> tuple:
        t = text.lower()

        # 1. C Programming
        if re.search(r'\bc\b|c programming|c language|c code|in c\b|c basics|c fundamentals|pointer|malloc|struct|printf|scanf|gcc', t):
            if re.search(r'pointer|\b\*p\b|\&', t):
                return ("C Programming", "Pointers & Memory")
            elif re.search(r'loop|for|while', t):
                return ("C Programming", "Loops & Iteration")
            elif re.search(r'array|string', t):
                return ("C Programming", "Arrays & Strings")
            elif re.search(r'function|recursion', t):
                return ("C Programming", "Functions & Recursion")
            elif re.search(r'struct|union', t):
                return ("C Programming", "Structures")
            else:
                return ("C Programming", "Fundamentals")

        # 2. Java Programming
        elif re.search(r'\bjava\b|jvm|system\.out\.println', t):
            if re.search(r'inherit|polymorph|class|interface|oop', t):
                return ("Java Programming", "Inheritance & OOP")
            elif re.search(r'collection|list|map|set', t):
                return ("Java Programming", "Collections Framework")
            elif re.search(r'exception|try|catch', t):
                return ("Java Programming", "Exception Handling")
            elif re.search(r'thread|multithread', t):
                return ("Java Programming", "Multithreading")
            else:
                return ("Java Programming", "Fundamentals")

        # 3. Python Programming
        elif re.search(r'\bpython\b|\bpy\b|def |lambda', t):
            if re.search(r'dict|dictionary|key', t):
                return ("Python Programming", "Dictionaries")
            elif re.search(r'list|tuple|set', t):
                return ("Python Programming", "Lists & Data Structures")
            elif re.search(r'function|decorator', t):
                return ("Python Programming", "Functions")
            elif re.search(r'class|oop', t):
                return ("Python Programming", "Object Oriented Programming")
            else:
                return ("Python Programming", "Fundamentals")

        # 4. Data Structures
        elif re.search(r'binary search tree|\bbst\b|tree|linked list|stack|queue|graph|hashing|heap|data structure', t):
            if re.search(r'tree|\bbst\b', t):
                return ("Data Structures", "Binary Search Tree")
            elif re.search(r'linked list', t):
                return ("Data Structures", "Linked Lists")
            elif re.search(r'stack|queue', t):
                return ("Data Structures", "Stacks & Queues")
            elif re.search(r'graph', t):
                return ("Data Structures", "Graphs")
            else:
                return ("Data Structures", "Core Data Structures")

        # 5. Computer Networks
        elif re.search(r'\btcp\b|handshake|\bosi\b|\budp\b|\bdns\b|\bhttp\b|routing|socket|ip address|mac address', t):
            if re.search(r'tcp|handshake|syn', t):
                return ("Computer Networks", "TCP / IP Protocols")
            elif re.search(r'osi|layer', t):
                return ("Computer Networks", "OSI Model")
            else:
                return ("Computer Networks", "Network Architecture")

        # 6. DBMS
        elif re.search(r'normaliz|dbms|sql|database|acid|1nf|2nf|3nf|bcnf|join|indexing|key', t):
            if re.search(r'normaliz|1nf|2nf|3nf|bcnf', t):
                return ("DBMS", "Normalization")
            elif re.search(r'sql|query|join', t):
                return ("DBMS", "SQL Queries & Joins")
            else:
                return ("DBMS", "Relational Database Management")

        # 7. Operating Systems
        elif re.search(r'process|thread|deadlock|schedul|round robin|fcfs|operating system|\bos\b|paging', t):
            if re.search(r'schedul|round robin|fcfs', t):
                return ("Operating Systems", "Process Scheduling")
            elif re.search(r'deadlock', t):
                return ("Operating Systems", "Deadlocks")
            else:
                return ("Operating Systems", "Process Management")

        # 8. Machine Learning
        elif re.search(r'machine learning|\bml\b|regress|classif|cluster|decision tree|neural|overfit|supervised', t):
            return ("Machine Learning", "Supervised Learning")

        # 9. General CS Fallback
        else:
            words = [w for w in t.split() if len(w) > 3 and w not in ["what", "how", "why", "can", "please", "teach", "explain", "about", "with", "from", "that", "this", "have", "could", "would"]]
            main_term = " ".join(words[:2]).title() if words else "Computer Science"
            return ("Computer Science", main_term)

    def _generate_explanation(self, query: str, mode: str, subject: str, topic: str) -> str:
        # C Programming
        if subject == "C Programming":
            if topic == "Pointers & Memory":
                if mode == "simple":
                    return (
                        "### Concept Summary\n"
                        "A pointer in C is a variable that stores the memory address of another variable.\n\n"
                        "### Simple Explanation\n"
                        "In C:\n"
                        "- Use `&` to get the address of a variable.\n"
                        "- Use `*` to declare a pointer or dereference it to read/modify the value at that address.\n\n"
                        "```c\n"
                        "int num = 10;\n"
                        "int *ptr = &num; // ptr stores address of num\n"
                        "printf(\"%d\", *ptr); // prints 10\n"
                        "```\n\n"
                        "### Real-World Example\n"
                        "A pointer is like a bookmark in a book: instead of re-copying the page, you store the page number to access it instantly.\n\n"
                        "### Key Takeaway\n"
                        "Pointers enable dynamic memory allocation (`malloc`), pass-by-reference in functions, and efficient data structures!"
                    )
                elif mode == "real-world":
                    return (
                        "### Real-World Analogy\n"
                        "Imagine a valet parking service. Instead of driving your car around inside the garage, you hand over a parking ticket (the pointer) containing the exact spot number where your car is stored.\n\n"
                        "### Key Takeaway\n"
                        "Passing pointers to functions allows functions to modify original values without copying large structs!"
                    )
                else:
                    return (
                        "### Technical Specifications\n"
                        "C Pointer Mechanics & Memory Layout:\n\n"
                        "1. **Address Arithmetic**: Pointer increments (`ptr + 1`) advance the address by `sizeof(T)` bytes.\n"
                        "2. **Dynamic Memory**: `malloc(size_t)` allocates raw bytes in the Heap segment; `free(void*)` releases memory back to the OS.\n"
                        "3. **Null Pointer Safeguard**: Always check `if (ptr == NULL)` before dereferencing to prevent Segmentation Faults (`SIGSEGV`).\n\n"
                        "### Key Takeaway\n"
                        "Uninitialized or dangling pointers cause undefined behavior. Always set freed pointers to `NULL`."
                    )
            elif topic == "Loops & Iteration":
                return (
                    "### Concept Summary\n"
                    "Loops in C execute a block of code repeatedly while a specified boolean condition remains true.\n\n"
                    "### Simple Explanation\n"
                    "C provides three main loop structures:\n\n"
                    "1. **for loop** (used when iteration count is known):\n"
                    "```c\n"
                    "for (int i = 0; i < 5; i++) {\n"
                    "    printf(\"%d\\n\", i);\n"
                    "}\n"
                    "```\n"
                    "2. **while loop** (used when stopping condition depends on dynamic checks):\n"
                    "```c\n"
                    "while (count < 10) { count++; }\n"
                    "```\n"
                    "3. **do-while loop** (executes at least once before testing condition).\n\n"
                    "### Key Takeaway\n"
                    "Ensure the loop counter increments properly to avoid infinite loops!"
                )
            else: # Fundamentals / General C
                if mode == "simple":
                    return (
                        "### Concept Summary\n"
                        "C is a procedural programming language where programs are built using variables, data types, operators, control flow, functions, arrays, pointers, and memory management.\n\n"
                        "### Simple Explanation\n"
                        "Start with these core C fundamentals:\n\n"
                        "1. **Variables & Data Types**:\n"
                        "```c\n"
                        "int age = 20;\n"
                        "float marks = 85.5;\n"
                        "char grade = 'A';\n"
                        "```\n\n"
                        "2. **Input and Output**:\n"
                        "```c\n"
                        "printf(\"Hello Santhosh!\\n\");\n"
                        "scanf(\"%d\", &age);\n"
                        "```\n\n"
                        "3. **Control Flow (Conditions & Loops)**:\n"
                        "```c\n"
                        "if (age >= 18) {\n"
                        "    printf(\"Adult\\n\");\n"
                        "}\n"
                        "for (int i = 0; i < 5; i++) {\n"
                        "    printf(\"%d \", i);\n"
                        "}\n"
                        "```\n\n"
                        "4. **Functions**:\n"
                        "```c\n"
                        "int add(int a, int b) {\n"
                        "    return a + b;\n"
                        "}\n"
                        "```\n\n"
                        "### Real-World Example\n"
                        "A C program uses variables to store data, conditional statements to make decisions, loops to repeat calculations, and functions to organize reusable logic.\n\n"
                        "### Key Takeaway\n"
                        "Follow this learning order: Variables → Data Types → Operators → Conditions → Loops → Functions → Arrays → Pointers → Structures."
                    )
                elif mode == "real-world":
                    return (
                        "### Real-World Analogy\n"
                        "Learning C programming is like learning to drive a manual transmission sports car. You get direct control over the engine (CPU) and gears (memory), giving maximum performance and speed.\n\n"
                        "### Key Takeaway\n"
                        "Because C operates close to hardware, operating systems (Linux, Windows kernel) and high-performance database engines are written in C!"
                    )
                else:
                    return (
                        "### Technical Specifications\n"
                        "C Language Execution & Memory Architecture:\n\n"
                        "1. **Memory Segments**: Code Segment (text instructions), Data Segment (initialized globals), BSS (uninitialized globals), Stack (local variables & function call frames), Heap (`malloc`/`free` dynamic allocation).\n"
                        "2. **Pointers & Addressing**: Pointer `int *p` stores 64-bit memory address (`uintptr_t`). `*p` dereferences value at address.\n"
                        "3. **Compilation Pipeline**: Preprocessing (`#include`, `#define`) -> Compilation (Assembly output) -> Assembly (Object `.o`) -> Linking (Executable binary).\n\n"
                        "### Key Takeaway\n"
                        "Always check pointer non-nullness before dereferencing and free allocated heap memory to avoid leaks."
                    )

        # Java Programming
        elif subject == "Java Programming":
            if mode == "simple":
                return (
                    "### Concept Summary\n"
                    "Java is an Object-Oriented Programming (OOP) language where programs are structured around Classes and Objects.\n\n"
                    "### Simple Explanation\n"
                    "Key Java concepts:\n"
                    "- **Class**: A blueprint defining attributes and methods (e.g. `class Student`).\n"
                    "- **Object**: An instance created from a class (`Student s = new Student();`).\n"
                    "- **Inheritance**: Subclass inherits fields and methods from a superclass using `extends`.\n\n"
                    "```java\n"
                    "class Animal {\n"
                    "    void sound() { System.out.println(\"Animal sound\"); }\n"
                    "}\n"
                    "class Dog extends Animal {\n"
                    "    void sound() { System.out.println(\"Bark!\"); }\n"
                    "}\n"
                    "```\n\n"
                    "### Key Takeaway\n"
                    "Java's JVM allows code to write once and run on any platform!"
                )
            else:
                return (
                    "### Technical Specifications\n"
                    "Java OOP & Execution Model:\n\n"
                    "1. **Bytecode & JVM**: `.java` source compiles to `.class` bytecode via `javac`, executed by Java Virtual Machine (JVM) with JIT compilation.\n"
                    "2. **Polymorphism**: Overriding (`@Override` dynamic dispatch) and Overloading (compile-time polymorphism).\n"
                    "3. **Garbage Collection**: Automated heap memory management via generational GC (Young, Tenured, Metaspace).\n\n"
                    "### Key Takeaway\n"
                    "Encapsulation, Inheritance, Polymorphism, and Abstraction form the 4 pillars of Java OOP."
                )

        # Python Programming
        elif subject == "Python Programming":
            if topic == "Dictionaries":
                return (
                    "### Concept Summary\n"
                    "A Python Dictionary is a mutable, key-value data structure offering average $O(1)$ lookup time.\n\n"
                    "### Simple Explanation\n"
                    "```python\n"
                    "# Creating a dictionary\n"
                    "student = {\"name\": \"Santhosh\", \"course\": \"CSE\", \"marks\": 92}\n\n"
                    "# Accessing values\n"
                    "print(student[\"name\"])  # Output: Santhosh\n"
                    "print(student.get(\"marks\")) # Safe access\n"
                    "```\n\n"
                    "### Key Takeaway\n"
                    "Keys must be immutable (strings, numbers, tuples) because dictionaries use hash tables for fast lookup."
                )
            else:
                return (
                    "### Concept Summary\n"
                    "Python is a high-level, interpreted programming language known for clean syntax and dynamic typing.\n\n"
                    "### Simple Explanation\n"
                    "Core Python fundamentals include dynamic variables, lists (`[1, 2, 3]`), tuples (`(1, 2)`), dictionaries (`{\"a\": 1}`), functions (`def`), and clean indentation blocks.\n\n"
                    "### Key Takeaway\n"
                    "Python emphasizes readability and rapid development!"
                )

        # Data Structures -> BST
        elif subject == "Data Structures":
            if topic == "Binary Search Tree":
                return (
                    "### Concept Summary\n"
                    "A Binary Search Tree (BST) is a hierarchical node structure where every node has at most two children, and all left node values are smaller than the parent while right node values are greater.\n\n"
                    "### Simple Explanation\n"
                    "Searching in a BST is fast because at each step you eliminate half of the remaining elements, yielding $O(\\log n)$ average time complexity.\n\n"
                    "### Real-World Example\n"
                    "Looking up a word in a dictionary by opening to the middle and deciding whether to look in the left half or right half.\n\n"
                    "### Key Takeaway\n"
                    "In-order traversal (Left, Node, Right) of a BST outputs elements in sorted order!"
                )
            else:
                return (
                    "### Concept Summary\n"
                    "Data Structures organize and store data in memory to allow efficient search, insertion, and deletion operations.\n\n"
                    "### Key Takeaway\n"
                    "Choose data structures based on time complexity requirements ($O(1)$ array access vs $O(\\log n)$ BST search vs $O(1)$ hash table lookup)."
                )

        # Computer Networks -> TCP
        elif subject == "Computer Networks":
            return (
                "### Concept Summary\n"
                "TCP uses a **three-way handshake** to establish sequence tracking and buffer allocation before transmitting payload data.\n\n"
                "### Simple Explanation\n"
                "1. **SYN**: Client sends SYN packet ('Are you ready?').\n"
                "2. **SYN-ACK**: Server replies SYN-ACK ('Yes, I am ready! Are you?').\n"
                "3. **ACK**: Client sends ACK ('Great, starting data transfer!').\n\n"
                "### Key Takeaway\n"
                "The handshake guarantees reliable, ordered packet delivery over IP networks."
            )

        # DBMS -> Normalization
        elif subject == "DBMS":
            return (
                "### Concept Summary\n"
                "Database Normalization is the systematic technique of organizing relational database schemas to eliminate data redundancy and anomaly bugs.\n\n"
                "### Simple Explanation\n"
                "Normalization separates unorganized data into linked tables using primary and foreign keys (1NF: atomic values, 2NF: no partial dependencies, 3NF: no transitive dependencies).\n\n"
                "### Key Takeaway\n"
                "Eliminating data redundancy prevents insert, update, and delete anomalies while maintaining data integrity!"
            )

        # Operating Systems -> Process Scheduling
        elif subject == "Operating Systems":
            return (
                "### Concept Summary\n"
                "Process Scheduling is how the OS CPU allocator determines which ready process receives execution time on the CPU.\n\n"
                "### Simple Explanation\n"
                "Round Robin scheduling assigns each process a fixed time quantum. If the process does not finish within its time slice, it returns to the back of the ready queue.\n\n"
                "### Key Takeaway\n"
                "Prevents process starvation and ensures interactive system responsiveness!"
            )

        # General CS Fallback
        else:
            return (
                f"### Concept Summary\n"
                f"LearnSync AI evaluated your question regarding **{topic}** in **{subject}**.\n\n"
                f"### Simple Explanation\n"
                f"Key principles in {topic} build reliable, efficient computer science solutions. "
                f"Understanding underlying mechanics helps you design scalable algorithms and debug code effectively.\n\n"
                f"### Key Takeaway\n"
                f"Use the mode buttons (Simple, Real-World, Technical) to explore different explanation depths!"
            )

    def _generate_followups(self, query: str, subject: str, topic: str) -> List[str]:
        if subject == "C Programming":
            if topic == "Pointers & Memory":
                return [
                    "How does malloc and free work in C?",
                    "What is a dangling pointer?",
                    "Quiz me on C Pointers",
                ]
            else:
                return [
                    "Explain C variables & data types",
                    "Teach me loops in C",
                    "Explain pointers simply",
                ]
        elif subject == "Java Programming":
            return [
                "Explain Java inheritance with an example",
                "What is the difference between abstract class and interface?",
                "Quiz me on Java OOP",
            ]
        elif subject == "Python Programming":
            return [
                "How do Python dictionaries work under the hood?",
                "Explain list comprehensions in Python",
                "Quiz me on Python Data Structures",
            ]
        elif subject == "Data Structures":
            return [
                "What is the time complexity of BST search?",
                "How do self-balancing AVL trees work?",
                "Quiz me on Binary Search Trees",
            ]
        elif subject == "DBMS":
            return [
                "What is the difference between 2NF and 3NF?",
                "Explain Boyce-Codd Normal Form (BCNF)",
                "Quiz me on Database Normalization",
            ]
        elif subject == "Operating Systems":
            return [
                "What is context switching overhead?",
                "Explain Round Robin vs FCFS scheduling",
                "Quiz me on Process Scheduling",
            ]
        else:
            return [
                f"Explain {topic} simply",
                f"Give me a real-world example of {topic}",
                f"Quiz me on {topic}",
            ]

    def _build_quiz_response(self, query: str) -> Dict[str, Any]:
        subject, topic = self._detect_topic(query)
        quiz = QuizModel(
            id="quiz_auto_1",
            question=f"Which core concept is central to {topic} in {subject}?",
            options=[
                QuizOptionModel(key="A", text="Unordered unindexed storage"),
                QuizOptionModel(key="B", text="Structured execution and invariants"),
                QuizOptionModel(key="C", text="Hardware-only acceleration"),
                QuizOptionModel(key="D", text="Linear brute-force search"),
            ],
            correct_key="B",
            explanation=f"Understanding structured execution and invariants is key to mastering {topic}."
        )

        return {
            "answer": f"### Quick Check Quiz 🎯\nTest your understanding of **{topic}** ({subject}):",
            "explanation_mode": "quiz",
            "topic": topic,
            "subject": subject,
            "suggested_followups": [f"Explain {topic} in detail", "Practice another question"],
            "quiz": quiz.model_dump(),
        }

    def _build_practice_response(self, query: str) -> Dict[str, Any]:
        subject, topic = self._detect_topic(query)
        quiz = QuizModel(
            id="practice_auto_2",
            question=f"What is the primary goal of applying best practices in {topic}?",
            options=[
                QuizOptionModel(key="A", text="Increases code redundancy"),
                QuizOptionModel(key="B", text="Improves system performance and code maintainability"),
                QuizOptionModel(key="C", text="Disables compiler optimizations"),
                QuizOptionModel(key="D", text="Requires custom hardware devices"),
            ],
            correct_key="B",
            explanation=f"Applying sound principles in {topic} maximizes execution performance and maintainability."
        )

        return {
            "answer": f"### Practice Problem 📝\nHere is a practice question for **{topic}**:",
            "explanation_mode": "practice",
            "topic": topic,
            "subject": subject,
            "suggested_followups": ["Show solution breakdown", "Quiz me on another topic"],
            "quiz": quiz.model_dump(),
        }
