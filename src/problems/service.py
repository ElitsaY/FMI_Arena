from app import db
from .models import Problem
from sqlalchemy.orm.attributes import flag_modified


class ProblemService:
    def __init__(self, session=None):
        self.session = session or db.session

    def list_problems(self, tags: list[str] = None) -> list[Problem]:
        if tags:
            return Problem.query.filter(
                Problem.extra_metadata["tags"].astext.overlap(tags)
            ).all()
        return Problem.query.all()

    def get_problem(self, problem_id: int) -> Problem:
        problem = Problem.query.get(problem_id)
        if not problem:
            raise ValueError(f"Problem with id {problem_id} not found")
        return problem

    def create_problem(
        self,
        name: str,
        description: str,
        input_format: str,
        output_format: str,
        extra_metadata: dict,
        test_cases: list[dict],
        created_by: int,
    ) -> Problem:
        problem = Problem(
            name=name,
            description=description,
            input_format=input_format,
            output_format=output_format,
            extra_metadata=extra_metadata,
            test_cases=test_cases,
            created_by=created_by,
        )
        self.session.add(problem)
        self.session.commit()
        return problem

    def assign_tag(self, problem_id: int, tag: str) -> Problem:
        with self.session.begin():  # start a tran
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
