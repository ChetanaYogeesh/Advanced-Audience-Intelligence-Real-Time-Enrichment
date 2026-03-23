from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Dict, Any, List, Union, Optional
import json
import math

class CustomerAnalyticsInput(BaseModel):
    """Input schema for Customer Analytics Tool."""
    customer_data: Union[str, List[Dict[str, Any]]] = Field(
        ...,
        description="JSON array of customer records or JSON string containing customer data"
    )
    analysis_type: Optional[str] = Field(
        default="summary",
        description="Type of analysis to perform: 'demographics', 'behavior', 'value', or 'summary' (default)"
    )
    value_field: Optional[str] = Field(
        default="total_spent",
        description="Field name to use for value calculations (default: 'total_spent')"
    )

class CustomerAnalyticsTool(BaseTool):
    """Tool for analyzing customer data and providing marketing insights using statistical calculations."""

    name: str = "Customer Analytics Tool"
    description: str = (
        "Analyzes customer data to provide comprehensive marketing insights including "
        "demographic breakdowns, value segmentation, purchase patterns, and statistical analysis. "
        "Supports age groups, geographic distribution, customer value tiers, and loyalty analysis."
    )
    args_schema: Type[BaseModel] = CustomerAnalyticsInput

    def _parse_customer_data(self, customer_data: Union[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """Parse customer data from string or list format."""
        try:
            if isinstance(customer_data, str):
                return json.loads(customer_data)
            elif isinstance(customer_data, list):
                return customer_data
            else:
                raise ValueError("Customer data must be a JSON string or list of dictionaries")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in customer_data: {str(e)}")

    def _calculate_statistics(self, values: List[float]) -> Dict[str, float]:
        """Calculate basic statistics for a list of values."""
        if not values:
            return {"count": 0, "mean": 0, "median": 0, "std_dev": 0, "min": 0, "max": 0}
        
        values = sorted(values)
        n = len(values)
        
        # Basic stats
        mean = sum(values) / n
        minimum = min(values)
        maximum = max(values)
        
        # Median
        if n % 2 == 0:
            median = (values[n//2 - 1] + values[n//2]) / 2
        else:
            median = values[n//2]
        
        # Standard deviation
        variance = sum((x - mean) ** 2 for x in values) / n
        std_dev = math.sqrt(variance)
        
        return {
            "count": n,
            "mean": round(mean, 2),
            "median": round(median, 2),
            "std_dev": round(std_dev, 2),
            "min": minimum,
            "max": maximum
        }

    def _calculate_percentiles(self, values: List[float]) -> Dict[str, float]:
        """Calculate percentiles for a list of values."""
        if not values:
            return {"p25": 0, "p50": 0, "p75": 0, "p95": 0}
        
        sorted_values = sorted(values)
        n = len(sorted_values)
        
        def percentile(p):
            if n == 1:
                return sorted_values[0]
            k = (n - 1) * p / 100
            f = math.floor(k)
            c = math.ceil(k)
            if f == c:
                return sorted_values[int(k)]
            return sorted_values[int(f)] * (c - k) + sorted_values[int(c)] * (k - f)
        
        return {
            "p25": round(percentile(25), 2),
            "p50": round(percentile(50), 2),
            "p75": round(percentile(75), 2),
            "p95": round(percentile(95), 2)
        }

    def _categorize_age(self, age: Union[int, str, float]) -> str:
        """Categorize age into groups."""
        try:
            age = int(float(age))
            if age < 18:
                return "Under 18"
            elif age <= 24:
                return "18-24"
            elif age <= 34:
                return "25-34"
            elif age <= 44:
                return "35-44"
            elif age <= 54:
                return "45-54"
            else:
                return "55+"
        except (ValueError, TypeError):
            return "Unknown"

    def _categorize_value_tier(self, value: float, percentiles: Dict[str, float]) -> str:
        """Categorize customer value into tiers based on percentiles."""
        if value >= percentiles["p75"]:
            return "High Value"
        elif value >= percentiles["p25"]:
            return "Medium Value"
        else:
            return "Low Value"

    def _categorize_frequency(self, frequency: Union[int, float, str]) -> str:
        """Categorize purchase frequency."""
        try:
            freq = float(frequency)
            if freq >= 10:
                return "High Frequency"
            elif freq >= 4:
                return "Medium Frequency"
            else:
                return "Low Frequency"
        except (ValueError, TypeError):
            return "Unknown"

    def _analyze_demographics(self, customers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze demographic distribution."""
        age_distribution = {}
        location_distribution = {}
        total_customers = len(customers)

        for customer in customers:
            # Age analysis
            age = customer.get('age')
            if age is not None:
                age_group = self._categorize_age(age)
                age_distribution[age_group] = age_distribution.get(age_group, 0) + 1

            # Location analysis
            location = customer.get('location', 'Unknown')
            if isinstance(location, str):
                location = location.strip()
            location_distribution[str(location)] = location_distribution.get(str(location), 0) + 1

        # Convert to percentages
        age_percentages = {k: round(v/total_customers*100, 2) for k, v in age_distribution.items()}
        location_percentages = {k: round(v/total_customers*100, 2) for k, v in location_distribution.items()}

        return {
            "age_groups": {
                "distribution": age_distribution,
                "percentages": age_percentages
            },
            "geographic": {
                "distribution": location_distribution,
                "percentages": location_percentages
            },
            "total_customers": total_customers
        }

    def _analyze_behavior(self, customers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze customer behavior patterns."""
        frequency_distribution = {}
        channel_distribution = {}
        loyalty_distribution = {}

        for customer in customers:
            # Purchase frequency
            frequency = customer.get('purchase_frequency')
            if frequency is not None:
                freq_category = self._categorize_frequency(frequency)
                frequency_distribution[freq_category] = frequency_distribution.get(freq_category, 0) + 1

            # Preferred channel
            channel = customer.get('preferred_channel', 'Unknown')
            channel_distribution[str(channel)] = channel_distribution.get(str(channel), 0) + 1

            # Loyalty tier
            loyalty = customer.get('loyalty_tier', 'Unknown')
            loyalty_distribution[str(loyalty)] = loyalty_distribution.get(str(loyalty), 0) + 1

        total_customers = len(customers)

        return {
            "purchase_frequency": {
                "distribution": frequency_distribution,
                "percentages": {k: round(v/total_customers*100, 2) for k, v in frequency_distribution.items()}
            },
            "channel_preference": {
                "distribution": channel_distribution,
                "percentages": {k: round(v/total_customers*100, 2) for k, v in channel_distribution.items()}
            },
            "loyalty_tiers": {
                "distribution": loyalty_distribution,
                "percentages": {k: round(v/total_customers*100, 2) for k, v in loyalty_distribution.items()}
            }
        }

    def _analyze_value(self, customers: List[Dict[str, Any]], value_field: str) -> Dict[str, Any]:
        """Analyze customer value distribution."""
        values = []
        valid_customers = 0

        for customer in customers:
            value = customer.get(value_field)
            if value is not None:
                try:
                    numeric_value = float(value)
                    values.append(numeric_value)
                    valid_customers += 1
                except (ValueError, TypeError):
                    continue

        if not values:
            return {"error": f"No valid numeric values found for field '{value_field}'"}

        # Calculate statistics and percentiles
        stats = self._calculate_statistics(values)
        percentiles = self._calculate_percentiles(values)

        # Categorize customers into value tiers
        value_tiers = {"High Value": 0, "Medium Value": 0, "Low Value": 0}
        
        for value in values:
            tier = self._categorize_value_tier(value, percentiles)
            value_tiers[tier] += 1

        # Calculate outliers using IQR method
        q1, q3 = percentiles["p25"], percentiles["p75"]
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers = [v for v in values if v < lower_bound or v > upper_bound]

        return {
            "statistics": stats,
            "percentiles": percentiles,
            "value_tiers": {
                "distribution": value_tiers,
                "percentages": {k: round(v/valid_customers*100, 2) for k, v in value_tiers.items()}
            },
            "outlier_analysis": {
                "count": len(outliers),
                "percentage": round(len(outliers)/valid_customers*100, 2),
                "threshold_lower": round(lower_bound, 2),
                "threshold_upper": round(upper_bound, 2)
            },
            "data_quality": {
                "total_records": len(customers),
                "valid_values": valid_customers,
                "missing_values": len(customers) - valid_customers
            }
        }

    def _generate_insights(self, analysis_results: Dict[str, Any], analysis_type: str) -> List[str]:
        """Generate marketing insights based on analysis results."""
        insights = []

        if analysis_type in ['demographics', 'summary']:
            demographics = analysis_results.get('demographics', {})
            age_groups = demographics.get('age_groups', {}).get('percentages', {})
            
            # Find dominant age group
            if age_groups:
                dominant_age = max(age_groups.items(), key=lambda x: x[1])
                insights.append(f"Primary customer segment: {dominant_age[0]} ({dominant_age[1]}% of customers)")

            # Geographic insights
            geographic = demographics.get('geographic', {}).get('percentages', {})
            if geographic:
                top_location = max(geographic.items(), key=lambda x: x[1])
                insights.append(f"Top geographic market: {top_location[0]} ({top_location[1]}% of customers)")

        if analysis_type in ['behavior', 'summary']:
            behavior = analysis_results.get('behavior', {})
            
            # Frequency insights
            frequency = behavior.get('purchase_frequency', {}).get('percentages', {})
            if frequency:
                high_freq = frequency.get('High Frequency', 0)
                if high_freq > 20:
                    insights.append(f"Strong customer engagement: {high_freq}% are high-frequency buyers")
                elif frequency.get('Low Frequency', 0) > 50:
                    insights.append("Opportunity to improve customer engagement and purchase frequency")

            # Channel insights
            channels = behavior.get('channel_preference', {}).get('percentages', {})
            if channels:
                primary_channel = max(channels.items(), key=lambda x: x[1])
                insights.append(f"Primary sales channel: {primary_channel[0]} ({primary_channel[1]}% preference)")

        if analysis_type in ['value', 'summary']:
            value_analysis = analysis_results.get('value', {})
            stats = value_analysis.get('statistics', {})
            tiers = value_analysis.get('value_tiers', {}).get('percentages', {})
            
            if stats and stats.get('count', 0) > 0:
                avg_value = stats.get('mean', 0)
                insights.append(f"Average customer value: ${avg_value}")
                
                high_value_pct = tiers.get('High Value', 0)
                if high_value_pct > 25:
                    insights.append(f"Strong high-value segment: {high_value_pct}% of customers in top tier")
                elif high_value_pct < 10:
                    insights.append("Limited high-value customers - opportunity for upselling strategies")

        if not insights:
            insights.append("Analysis completed - review detailed metrics for specific insights")

        return insights

    def _assess_data_quality(self, customers: List[Dict[str, Any]], value_field: str) -> Dict[str, Any]:
        """Assess the quality of customer data."""
        total_records = len(customers)
        if total_records == 0:
            return {"error": "No customer records provided"}

        required_fields = ['age', 'location', value_field, 'purchase_frequency', 'preferred_channel']
        field_completeness = {}
        
        for field in required_fields:
            valid_count = sum(1 for customer in customers if customer.get(field) is not None and customer.get(field) != "")
            field_completeness[field] = {
                "valid_records": valid_count,
                "completeness_percentage": round(valid_count / total_records * 100, 2)
            }

        overall_completeness = sum(fc["completeness_percentage"] for fc in field_completeness.values()) / len(field_completeness)

        return {
            "total_records": total_records,
            "field_completeness": field_completeness,
            "overall_completeness": round(overall_completeness, 2),
            "quality_grade": "Excellent" if overall_completeness >= 90 else "Good" if overall_completeness >= 70 else "Fair" if overall_completeness >= 50 else "Poor"
        }

    def _run(self, customer_data: Union[str, List[Dict[str, Any]]], analysis_type: Optional[str] = "summary", value_field: Optional[str] = "total_spent") -> str:
        try:
            # Parse customer data
            customers = self._parse_customer_data(customer_data)
            
            if not customers:
                return json.dumps({"error": "No customer data provided"})

            # Validate analysis type
            valid_types = ['demographics', 'behavior', 'value', 'summary']
            if analysis_type not in valid_types:
                analysis_type = 'summary'

            # Assess data quality
            data_quality = self._assess_data_quality(customers, value_field)

            # Perform analysis based on type
            results = {
                "analysis_type": analysis_type,
                "data_quality": data_quality
            }

            if analysis_type in ['demographics', 'summary']:
                results["demographics"] = self._analyze_demographics(customers)

            if analysis_type in ['behavior', 'summary']:
                results["behavior"] = self._analyze_behavior(customers)

            if analysis_type in ['value', 'summary']:
                results["value"] = self._analyze_value(customers, value_field)

            # Generate insights
            results["insights"] = self._generate_insights(results, analysis_type)

            # Add metadata
            results["metadata"] = {
                "total_customers_analyzed": len(customers),
                "analysis_timestamp": "Analysis completed",
                "value_field_used": value_field
            }

            return json.dumps(results, indent=2)

        except ValueError as e:
            return json.dumps({"error": f"Data validation error: {str(e)}"})
        except Exception as e:
            return json.dumps({"error": f"Analysis error: {str(e)}"})