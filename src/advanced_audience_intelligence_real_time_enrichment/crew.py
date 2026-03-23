import os

from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
	ScrapeWebsiteTool
)
from advanced_audience_intelligence_real_time_enrichment.tools.customer_analytics_tool import CustomerAnalyticsTool
from advanced_audience_intelligence_real_time_enrichment.tools.customer_data_enrichment import CustomerDataEnrichmentTool




@CrewBase
class AdvancedAudienceIntelligenceRealTimeEnrichmentCrew:
    """AdvancedAudienceIntelligenceRealTimeEnrichment crew"""

    
    @agent
    def data_profiler(self) -> Agent:
        
        return Agent(
            config=self.agents_config["data_profiler"],
            
            
            tools=[				ScrapeWebsiteTool(website_url="https://docs.google.com/spreadsheets/d/11l70nJrLm7IBoncC3AMOq7Zy2PzRo-PAi0ouET7HWIs/edit?usp=sharing"),
				CustomerAnalyticsTool()],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                temperature=0.7,
                
            ),
            
        )
    
    @agent
    def statistical_enrichment_analyst(self) -> Agent:
        
        return Agent(
            config=self.agents_config["statistical_enrichment_analyst"],
            
            
            tools=[				CustomerDataEnrichmentTool()],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                temperature=0.7,
                
            ),
            
        )
    
    @agent
    def lookalike_modeler(self) -> Agent:
        
        return Agent(
            config=self.agents_config["lookalike_modeler"],
            
            
            tools=[				CustomerAnalyticsTool()],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                temperature=0.7,
                
            ),
            
        )
    
    @agent
    def targeting_strategist(self) -> Agent:
        
        return Agent(
            config=self.agents_config["targeting_strategist"],
            
            
            tools=[],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                temperature=0.7,
                
            ),
            
        )
    
    @agent
    def report_generator(self) -> Agent:
        
        return Agent(
            config=self.agents_config["report_generator"],
            
            
            tools=[],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                temperature=0.7,
                
            ),
            
        )
    

    
    @task
    def analyze_seed_audience_data(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_seed_audience_data"],
            markdown=False,
            
            
        )
    
    @task
    def enhanced_data_enrichment(self) -> Task:
        return Task(
            config=self.tasks_config["enhanced_data_enrichment"],
            markdown=False,
            
            
        )
    
    @task
    def create_lookalike_audience_persona(self) -> Task:
        return Task(
            config=self.tasks_config["create_lookalike_audience_persona"],
            markdown=False,
            
            
        )
    
    @task
    def develop_targeting_strategy(self) -> Task:
        return Task(
            config=self.tasks_config["develop_targeting_strategy"],
            markdown=False,
            
            
        )
    
    @task
    def generate_executive_summary_report(self) -> Task:
        return Task(
            config=self.tasks_config["generate_executive_summary_report"],
            markdown=False,
            
            
        )
    

    @crew
    def crew(self) -> Crew:
        """Creates the AdvancedAudienceIntelligenceRealTimeEnrichment crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            chat_llm=LLM(model="openai/gpt-4o-mini"),
        )


