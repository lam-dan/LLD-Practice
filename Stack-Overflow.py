# Design Stack Overflow

# What are the functional requirements?
# Users can post questions, answer questions, and comment on questions and answers.
# Users can vote on questions and answers.
# Users can tag questions for tags associated with the question.
# Users can search for questions based on keywords, tags, or user profiles.
# The system should assign reputation score to users based on their activity and the quality of their contributions.

# Core Entities
# User 
# Question
# Answer
# Comment
# Vote
# Tag

# Define Relationship of the Classes
# Users can ask many questions, provide many answers, and add many comments.
# A Question can have many answers, comments, tags, and votes.
# An Answer can have many comments, votes.
# A Comment is composed within a Question or an Answer.
# A Tag is composed within a Question.

# Interfaces / Core Methods
# Both Answers and Questions can comment, tag, or vote.
# Commentable
# Votable
from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional

class Commentable(ABC):
    @abstractmethod
    def add_comment(self, comment: Comment) -> None:
        pass

    def get_comments(self) -> List[Comment]:
        pass

class Votable(ABC):
    @abstractmethod
    def add_vote(self, user: User, value: int) -> None:
        pass

    def get_votes(self) -> int:
        pass

class User:
    def __init__(self, user_id: int, user_name: str, email: str):
        self.user_id: int = user_id
        self.user_name: str = user_name
        self.email: str = email
        self.reputation: int = 0
        self.questions: List[Question] = []
        self.comments: List[Comment] = []
        self.answers: List[Answer] = []

    def post_question(self, title: str, content: str, tags: List[str]) -> Question:
        question = Question(title, self, content, tags)
        self.questions.append(question)
        self.update_reputation(5)
        return question

    def post_answer(self, question: Question, content: str) -> Answer:
        answer = Answer(self, content, question)
        self.answers.append(answer)
        question.add_answer(answer)
        self.update_reputation(10)
        return answer

    def post_comment(self, commentable: Commentable, content: str) -> Comment:
        comment = Comment(content, self)
        self.comments.append(comment)
        commentable.add_comment(comment)
        self.update_reputation(2)
        return comment

    def update_reputation(self, value: int) -> None:
        self.reputation += value
        if self.reputation < 0:
            self.reputation = 0

class Comment:
    def __init__(self, content: str, user: User):
        self.id: int = id(self)
        self.user: User = user
        self.content: str = content

class Question(Commentable, Votable):
    def __init__(self, title: str, user: User, content: str, tag_names: List[str]):
        self.id: int = id(self)
        self.title: str = title
        self.user: User = user
        self.content: str = content
        self.creation_date: datetime = datetime.now()
        self.tags: List[Tag] = [Tag(tag_name) for tag_name in tag_names]
        self.answers: List[Answer] = []
        self.votes: List[Vote] = []
        self.comments: List[Comment] = []

    def add_answer(self, answer: Answer) -> None:
        if answer not in self.answers:
            self.answers.append(answer)

    def add_vote(self, user: User, value: int) -> None:
        if value not in [-1, 1]:
            raise ValueError("Vote value must be either 1 or -1")
        self.votes = [v for v in self.votes if v.user != user]
        self.votes.append(Vote(user, value))
        self.user.update_reputation(value * 5)

    def get_votes(self) -> int:
        return sum(v.value for v in self.votes)

    def add_comment(self, comment: Comment) -> None:
        self.comments.append(comment)

    def get_comments(self) -> List[Comment]:
        return self.comments.copy()

class Tag:
    def __init__(self, name: str):
        self.name: str = name

class Vote:
    def __init__(self, user: User, value: int):
        self.value: int = value
        self.user: User = user

class Answer(Commentable, Votable):
    def __init__(self, user: User, content: str, question: Question):
        self.id: int = id(self)
        self.user: User = user
        self.content: str = content
        self.question: Question = question
        self.comments: List[Comment] = []
        self.votes: List[Vote] = []
        self.is_accepted: bool = False

    def add_vote(self, user: User, value: int) -> None:
        if value not in [-1, 1]:
            raise ValueError("Vote value must be either 1 or -1")
        self.votes = [v for v in self.votes if v.user != user]
        self.votes.append(Vote(user, value))
        self.user.update_reputation(value * 10)

    def add_comment(self, comment: Comment) -> None:
        self.comments.append(comment)

    def mark_as_accepted(self) -> None:
        if self.is_accepted:
            raise ValueError("Answer is already accepted.")
        self.is_accepted = True

    def get_votes(self) -> int:
        return sum(v.value for v in self.votes)

    def get_comments(self) -> List[Comment]:
        return self.comments.copy()

class StackOverflow:
    def __init__(self):
        self.users: Dict[int, User] = {}
        self.questions: Dict[int, Question] = {}
        self.answers: Dict[int, Answer] = {}
        self.tags: Dict[str, Tag] = {}

    def create_user(self, username: str, email: str) -> User:
        user_id = len(self.users) + 1
        user = User(user_id, username, email)
        self.users[user_id] = user
        return user

    def post_question(self, user: User, title: str, content: str, tags: List[str]) -> Question:
        question = user.post_question(title, content, tags)
        self.questions[question.id] = question
        for tag in question.tags:
            if tag.name not in self.tags:
                self.tags[tag.name] = tag
        return question

    def post_answer(self, user: User, question: Question, content: str) -> Answer:
        answer = user.post_answer(question, content)
        self.answers[answer.id] = answer
        return answer

    def add_comment(self, user: User, commentable: Commentable, content: str) -> Comment:
        return user.post_comment(commentable, content)

    def vote_question(self, user: User, question: Question, value: int) -> None:
        question.add_vote(user, value)

    def vote_answer(self, user: User, answer: Answer, value: int) -> None:
        answer.add_vote(user, value)

    def accept_answer(self, answer: Answer) -> None:
        answer.mark_as_accepted()

    def search_questions(self, query: str) -> List[Question]:
        query = query.lower()
        results: List[Question] = []

        for question in self.questions.values():
            is_title_match = query in question.title.lower()
            is_content_match = query in question.content.lower()
            is_tag_match = any(query == tag.name.lower() for tag in question.tags)

            if is_title_match or is_content_match or is_tag_match:
                results.append(question)

        return results

    def get_questions_by_users(self, user: User) -> List[Question]:
        return user.questions

    def get_user(self, user_id: int) -> Optional[User]:
        return self.users.get(user_id)

    def get_question(self, question_id: int) -> Optional[Question]:
        return self.questions.get(question_id)

    def get_answer(self, answer_id: int) -> Optional[Answer]:
        return self.answers.get(answer_id)

    def get_tag(self, name: str) -> Optional[Tag]:
        return self.tags.get(name)


system = StackOverflow()

# Create Users
alice = system.create_user('alice123', 'alice123@gmail.com')
bob = system.create_user('bob123', 'bob123@gmail.com')
charlie = system.create_user('charlie123', 'charlie123@gmail.com')

# Alice asks a question
java_question = system.post_question(alice, "What is polymorphism in Java?",
                                "Can someone explain polymorphism in Java with an example?",
                                ["java", "oop"])

# Bob answers Alice's question
bob_answer = system.post_answer(bob, java_question,
                                "Polymorphism in Java is the ability of an object to take on many forms...")

# Charlie comments on the question
system.add_comment(charlie, java_question, "Great question! I'm also interested in learning about this.")

# Alice comments on Bob's answer
system.add_comment(alice, bob_answer, "Thanks for the explanation! Could you provide a code example?")

# Charlie votes on the question and answer
system.vote_question(charlie, java_question, 1)  # Upvote
system.vote_answer(charlie, bob_answer, 1)  # Upvote

# Alice accepts Bob's answer
system.accept_answer(bob_answer)

# Print out current state
print(f"Question: {java_question.title}")
print(f"Asked by: {java_question.user.user_name}")
print(f"Tags: {', '.join(tag.name for tag in java_question.tags)}")
print(f"Votes: {java_question.get_votes()}")
print(f"Accepted: {bob_answer.is_accepted}")
print(f"Comments: {len(bob_answer.get_comments())}")

print(f"\nUser Reputations:")
print(f"Alice: {alice.reputation}")
print(f"Bob: {bob.reputation}")
print(f"Charlie: {charlie.reputation}")

# Bob asks another question
python_question = system.post_question(bob, "How to use list comprehensions in Python?",
                                "I'm new to Python and I've heard about list comprehensions. Can someone explain how to use them?",
                                ["python", "list-comprehension"])

# Alice answers Bob's question
alice_answer = system.post_answer(alice, python_question,
                                "List comprehensions in Python provide a concise way to create lists...")

# Charlie votes on Bob's question and Alice's answer
system.vote_question(charlie, python_question, 1)  # Upvote
system.vote_answer(charlie, alice_answer, 1)  # Upvote


# Print out current state
print(f"\nQuestion: {python_question.title}")
print(f"Asked by: {python_question.user.user_name}")
print(f"Tags: {', '.join(tag.name for tag in python_question.tags)}")
print(f"Votes: {python_question.get_votes()}")
print(f"Accepted: {bob_answer.is_accepted}")
print(f"Comments: {len(bob_answer.get_comments())}")

print(f"\nUser Reputations:")
print(f"Alice: {alice.reputation}")
print(f"Bob: {bob.reputation}")
print(f"Charlie: {charlie.reputation}")

# Demonstrate search functionality
print("\nSearch Results for 'java':")
search_results = system.search_questions("java")
for q in search_results:
    print(q.title)

print("\nSearch Results for 'python':")
search_results = system.search_questions("python")
for q in search_results:
    print(q.title)

# Demonstrate getting questions by user
print("\nBob's Questions:")
bob_questions = system.get_questions_by_users(bob)
for q in bob_questions:
    print(q.title)

# 1. Responsibility-Driven Design (SRP)
# Each class in your system has a clear, single responsibility:

# Class	Responsibility
# User	Represents a user profile and handles their actions (post question/answer/comment)
# Question	Manages its own content, votes, answers, tags, comments
# Answer	Holds response to a question and tracks votes/comments
# Comment	Attached to Question or Answer
# Vote	Represents a single user's upvote/downvote
# Tag	Just stores the tag name
# StackOverflow	Acts as the controller/system manager that coordinates everything

# This aligns with the Single Responsibility Principle (SRP), a key LLD concept.

# 2. Interface Abstraction
# You defined Commentable and Votable as interfaces:

# class Commentable(ABC):
#     @abstractmethod
#     def add_comment(self, comment): ...

# class Votable(ABC):
#     @abstractmethod
#     def add_vote(self, user, value): ...
# These are used by both Question and Answer — a clean use of interface-driven design that enables:

# Polymorphism

# Future extensibility (e.g., you could later make Comment votable too)

# 3. Behavioral Realism
# You’ve modeled real user flows accurately:

# Users can:
# Post questions/answers/comments
# Vote on questions/answers

# Each question:
# Has answers, votes, comments, tags

# Each answer:
# Can be accepted, voted, and commented
# User reputation increases accordingly

# This shows you understand the domain well — a huge plus in interviews.

# 4. Encapsulation & Ownership
# Each class manages its own data and exposes clean methods:

# Question.add_answer(...)
# Answer.mark_as_accepted()
# User.post_comment(...)
# This avoids tight coupling and promotes clean collaboration between entities.

# Central Orchestrator: StackOverflow

# Your StackOverflow class acts like a service layer:
# Handles object registration (questions, answers, tags)
# Routes interactions (post_question, vote_answer)
# Provides system-wide views (search_questions, get_question_by_id)
# This matches real-world design:
# Entity classes = domain logic
# Service layer = orchestration logic

# 6. Scalability Consideration
# Your design:
# Registers tags globally: self.tags[tag.name]
# Tracks users/questions/answers in ID-based dicts: Dict[int, T]
# Supports search via title/content/tag match

# These are signs you're thinking about data indexing and retrieval — a good sign of readiness for system design questions.

# 7. Testability and Demo Support
# You wrote a realistic, scriptable test block:

# Demonstrates full interaction lifecycle
# Prints system state
# Shows reputation effects
# This gives your interviewer confidence that your design actually works and isn't just theory.

# Summary: Why This Design Is Good
# Principle	Applied In Your Design
# SRP (Single Responsibility)	Each class has one job
# Encapsulation	All state changes are managed through methods
# Interface Segregation	Votable, Commentable abstract shared behavior
# Domain fidelity	Matches real-world StackOverflow behaviors
# Scalability readiness	Uses IDs and tag indexing appropriately
# Testability	End-to-end usage is easy to demo and validate
# Extensibility	Easy to add views, moderation, or gamification later





