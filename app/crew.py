from typing import ClassVar, List
from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew
from src.schemas.cv_reader_agent import CVOutputModel
from src.schemas.evaluator_agent import MatchOutputModel
from crewai_tools import PDFSearchTool, DOCXSearchTool, FileReadTool, JSONSearchTool  

@CrewBase
class RecruitMateCrew:
    "Recruit Mate Crew"
    agents_config: ClassVar[str] = 'src/config/agents.yaml'
    tasks_config: ClassVar[str] = 'src/config/tasks.yaml'
    
    @agent
    def cv_reader(self) -> Agent:
        return Agent(
            config=self.agents_config['cv_reader'],
            tools=[PDFSearchTool(), DOCXSearchTool(), FileReadTool()],  # Tools are initialized without file paths
            verbose=True,
            allow_delegation=False
        )
    
    @agent
    def evaluator(self) -> Agent:
        return Agent(
            config=self.agents_config['match_making'],
            tools=[PDFSearchTool(), JSONSearchTool()],  # Tools are initialized without file paths
            verbose=True,
            allow_delegation=False
        )
        
    @task
    def read_cv_task(self) -> Task:
        return Task(
            config=self.tasks_config['reading_cv_task'],
            agent=self.cv_reader(),
            output_json=CVOutputModel
        )
    
    @task
    def match_cv_task(self) -> Task:
        return Task(
            config=self.tasks_config['match_cv_task'],
            agent=self.evaluator(),
            context=[self.read_cv_task()],
            output_json=MatchOutputModel
        )
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.cv_reader(), self.evaluator()],
            tasks=[self.read_cv_task(), self.match_cv_task()],
            process=Process.sequential,
            verbose=True,
            max_retries=3,
        )