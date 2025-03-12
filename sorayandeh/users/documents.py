from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from sorayandeh.campaign.models import Campaign
from sorayandeh.applicant.models import School

@registry.register_document
class YourModelDocument(Document):
    school_name = fields.TextField(attr='school.school.name')
    class Index:
        # Define the Elasticsearch index settings
        name = 'your_model_index'  # Replace with your index name
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        # Link to your Django model
        model = Campaign  # Replace with your actual model
        fields = ["id"]
        related_models = [School]

    @classmethod
    def get_instances_from_related(cls, related_instance):
        """Reindex related campaigns when a School is updated."""
        if isinstance(related_instance, School):
            return list(related_instance.campaigns.all())  # Convert queryset to list (FIX)
        return None