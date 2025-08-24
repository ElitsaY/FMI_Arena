"""
Problem service module for managing problem-related operations.
"""

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.attributes import flag_modified

from infra import db
from .models import Problem, CreateProblemRequest


class ProblemService:
    """
    Service class for managing problems.
    """

    def __init__(self, session=None):
        self.session = session or db.session

    def list_problems(self, tags: list[str] = None) -> list[Problem]:
        """
        List all problems, optionally filtered by tags.
        """
        if tags:
            return Problem.query.filter(
                Problem.extra_metadata["tags"].astext.overlap(tags)
            ).all()
        return Problem.query.all()

    def get_problem(self, problem_id: int) -> Problem:
        """
        Get a problem by ID.
        """

        problem = Problem.query.get(problem_id)
        if not problem:
            raise ValueError(f"Problem with id {problem_id} not found")
        return problem

    def create_problem(
        self,
        req: CreateProblemRequest,
        created_by: int,
    ) -> Problem:
        """
        Submit a new problem.
        """
        problem = Problem(
            name=req.name,
            description=req.description,
            input_format=req.input_format,
            output_format=req.output_format,
            extra_metadata=req.extra_metadata,
            test_cases=req.test_cases,
            created_by=created_by,
        )
        try:
            self.session.add(problem)
            self.session.commit()
            return problem
        except IntegrityError as e:
            self.session.rollback()
            raise ValueError("Problem with this name already exists") from e

    def assign_tag(self, problem_id: int, tag: str) -> Problem:
        """
        Assign a tag to a problem.
        """
        with self.session.begin():  # start a transaction
            problem = self.get_problem(problem_id)

            if "tags" not in problem.extra_metadata or not isinstance(
                problem.extra_metadata["tags"], list
            ):
                print("No tags found, initializing empty list.")
                problem.extra_metadata["tags"] = []
                flag_modified(problem, "extra_metadata")

            if tag not in problem.extra_metadata["tags"]:
                problem.extra_metadata["tags"].append(tag)
                flag_modified(problem, "extra_metadata")

        return problem
