from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from sorayandeh.campaign.models import Campaign
from sorayandeh.applicant.models import School  # Ensure correct import

@registry.register_document
class CampaignDocument(Document):
    school_name = fields.TextField(attr='school.name')  # Fixed field reference

    class Index:
        name = 'campaign_index'  # Use a meaningful index name
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = Campaign  # Your actual model
        fields = ["id", "title"]  # Include other relevant fields
        related_models = [School]  # Ensure School updates trigger reindexing

    @classmethod
    def get_instances_from_related(cls, related_instance):
        """Reindex related campaigns when a School is updated."""
        if isinstance(related_instance, School):
            return related_instance.campaigns.all()  # Fetch related Campaigns
        return None
